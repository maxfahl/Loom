# Story Folder Migration Remedy Prompt

**Purpose**: Fix incorrect story folder structure in existing projects

**Issue**: Stories were created in `features/[name]/` or `features/[name]/docs/stories/` instead of the correct location: `docs/development/features/[name]/stories/`

---

## Instructions for AI Agent

You are tasked with migrating an incorrectly structured feature/story folder system to the correct structure.

### Current Incorrect Structure

Stories may be located at:
- `features/[feature-name]/stories/` (WRONG)
- `features/[feature-name]/docs/stories/` (WRONG)
- `features/[feature-name]/[epic.story].md` files directly (WRONG)

### Correct Target Structure

```
Project Root:

features/
└── [feature-name]/
    ├── status.xml          # Feature tracking metadata
    ├── epics/              # Epic breakdown
    │   ├── epic-1-[name]/
    │   │   ├── DESCRIPTION.md
    │   │   ├── TASKS.md
    │   │   └── NOTES.md
    │   └── epic-2-[name]/
    │       ├── DESCRIPTION.md
    │       ├── TASKS.md
    │       └── NOTES.md
    ├── src/                # Feature implementation code
    └── tests/              # Feature tests

docs/
└── development/
    └── features/
        └── [feature-name]/
            ├── INDEX.md
            ├── FEATURE_SPEC.md
            ├── TECHNICAL_DESIGN.md
            ├── TASKS.md
            ├── CHANGELOG.md
            └── stories/    # Story files go HERE (epic.story format: 1.1.md, 2.3.md)
                ├── 1.1.md
                ├── 1.2.md
                ├── 2.1.md
                └── 2.2.md
```

---

## Migration Steps (Execute in Order)

### Step 1: Analyze Current State

1. **Find all features**:
   ```bash
   ls -la features/
   ```
   Note all feature directory names.

2. **For each feature, identify misplaced files**:
   ```bash
   # Check for stories in features/[name]/
   find features/ -name "*.md" -type f | grep -E "[0-9]+\.[0-9]+\.md"

   # Check for docs folder inside features/
   find features/ -type d -name "docs"

   # Check for stories folder inside features/
   find features/ -type d -name "stories"
   ```

3. **Check if docs/development/features/ exists**:
   ```bash
   ls -la docs/development/features/ 2>/dev/null || echo "Needs to be created"
   ```

4. **Create inventory** of what needs to be moved:
   - List all story files found in wrong locations
   - List all documentation files in wrong locations
   - Note which features need docs/development/features/[name]/ directories created

### Step 2: Create Correct Directory Structure

For each feature found in `features/` directory:

1. **Create the docs directory structure**:
   ```bash
   # Example for feature named "devdev-core"
   mkdir -p docs/development/features/devdev-core/stories
   ```

2. **Repeat for all features**:
   ```bash
   # For each feature directory in features/
   for feature in features/*/; do
       feature_name=$(basename "$feature")
       mkdir -p "docs/development/features/${feature_name}/stories"
       echo "Created docs/development/features/${feature_name}/stories/"
   done
   ```

### Step 3: Move Story Files

**CRITICAL**: Stories must move from `features/[name]/` to `docs/development/features/[name]/stories/`

1. **Move story files** (files matching pattern X.Y.md where X and Y are numbers):
   ```bash
   # For each feature
   for feature in features/*/; do
       feature_name=$(basename "$feature")

       # Move story files from features/[name]/ directly
       find "$feature" -maxdepth 1 -name "[0-9]*.[0-9]*.md" -type f -exec mv {} "docs/development/features/${feature_name}/stories/" \;

       # Move from features/[name]/stories/ if exists
       if [ -d "$feature/stories" ]; then
           find "$feature/stories" -name "*.md" -type f -exec mv {} "docs/development/features/${feature_name}/stories/" \;
           rmdir "$feature/stories" 2>/dev/null
       fi

       # Move from features/[name]/docs/stories/ if exists
       if [ -d "$feature/docs/stories" ]; then
           find "$feature/docs/stories" -name "*.md" -type f -exec mv {} "docs/development/features/${feature_name}/stories/" \;
           rm -rf "$feature/docs"
       fi

       echo "Migrated stories for ${feature_name}"
   done
   ```

2. **Verify story files moved**:
   ```bash
   # Check new location
   find docs/development/features/ -name "*.md" -type f

   # Verify old locations are empty
   find features/ -name "[0-9]*.[0-9]*.md" -type f
   # Should return nothing
   ```

### Step 4: Move Documentation Files

If documentation files (INDEX.md, FEATURE_SPEC.md, etc.) were created in `features/[name]/docs/`:

1. **Move doc files to correct location**:
   ```bash
   for feature in features/*/; do
       feature_name=$(basename "$feature")

       if [ -d "$feature/docs" ]; then
           # Move all markdown files except stories
           find "$feature/docs" -maxdepth 1 -name "*.md" -type f -exec mv {} "docs/development/features/${feature_name}/" \;

           # Remove empty docs folder
           rm -rf "$feature/docs"

           echo "Migrated docs for ${feature_name}"
       fi
   done
   ```

2. **Create missing doc files** if needed:
   ```bash
   # For each feature, check if INDEX.md exists
   for feature_dir in docs/development/features/*/; do
       feature_name=$(basename "$feature_dir")

       if [ ! -f "$feature_dir/INDEX.md" ]; then
           echo "# ${feature_name} - Index" > "$feature_dir/INDEX.md"
           echo "" >> "$feature_dir/INDEX.md"
           echo "## Overview" >> "$feature_dir/INDEX.md"
           echo "" >> "$feature_dir/INDEX.md"
           echo "Documentation index for ${feature_name} feature." >> "$feature_dir/INDEX.md"
       fi

       # Create other required files if missing
       touch "$feature_dir/FEATURE_SPEC.md" 2>/dev/null || true
       touch "$feature_dir/TECHNICAL_DESIGN.md" 2>/dev/null || true
       touch "$feature_dir/TASKS.md" 2>/dev/null || true
       touch "$feature_dir/CHANGELOG.md" 2>/dev/null || true
   done
   ```

### Step 5: Update status.xml Files

**CRITICAL**: Update all status.xml files to reference correct story paths

1. **Find all status.xml files**:
   ```bash
   find features/ -name "status.xml" -type f
   ```

2. **Update story path references in each status.xml**:
   ```bash
   # For each status.xml
   for status_file in features/*/status.xml; do
       feature_name=$(basename $(dirname "$status_file"))

       # Update any story path references
       # Change: features/[name]/stories/X.Y.md
       # To: docs/development/features/[name]/stories/X.Y.md

       sed -i.bak "s|features/${feature_name}/stories/|docs/development/features/${feature_name}/stories/|g" "$status_file"
       sed -i.bak "s|features/${feature_name}/docs/stories/|docs/development/features/${feature_name}/stories/|g" "$status_file"

       # Update comment examples
       sed -i.bak "s|<!-- Story file location: features/|<!-- Story file location: docs/development/features/|g" "$status_file"

       rm "${status_file}.bak"

       echo "Updated status.xml for ${feature_name}"
   done
   ```

3. **Verify status.xml changes**:
   ```bash
   # Check that all story references are correct
   grep -r "Story file location\|<current-story>" features/*/status.xml
   # Should all show: docs/development/features/[name]/stories/
   ```

### Step 6: Update .claude/commands Files

Check if /create-story and /create-feature commands have correct paths:

1. **Check /create-story command**:
   ```bash
   if [ -f ".claude/commands/create-story.md" ]; then
       grep -n "docs/development/features" .claude/commands/create-story.md
       # Should contain references to docs/development/features/[feature-name]/stories/

       # If not, update the command file
       sed -i.bak 's|features/\[feature-name\]/stories/|docs/development/features/[feature-name]/stories/|g' .claude/commands/create-story.md
       sed -i.bak 's|features/\[feature\]/stories/|docs/development/features/[feature]/stories/|g' .claude/commands/create-story.md
       rm .claude/commands/create-story.md.bak
   fi
   ```

2. **Check /create-feature command**:
   ```bash
   if [ -f ".claude/commands/create-feature.md" ]; then
       grep -n "docs/development/features" .claude/commands/create-feature.md
       # Should contain correct structure

       # If not, update the command file
       sed -i.bak 's|features/\[feature-name\]/docs/|docs/development/features/[feature-name]/|g' .claude/commands/create-feature.md
       sed -i.bak 's|features/\[feature-name\]/stories/|docs/development/features/[feature-name]/stories/|g' .claude/commands/create-feature.md
       rm .claude/commands/create-feature.md.bak
   fi
   ```

### Step 7: Update Any Hardcoded References

Search for any hardcoded story paths in the codebase:

1. **Search for incorrect patterns**:
   ```bash
   # Search all markdown files
   grep -r "features/.*stories/" . --include="*.md" | grep -v "docs/development/features"

   # Search all code files (adjust extensions as needed)
   grep -r "features/.*stories/" . --include="*.ts" --include="*.tsx" --include="*.js" --include="*.jsx"
   ```

2. **Update any found references**:
   - Manually review each occurrence
   - Update to use `docs/development/features/[feature-name]/stories/`

### Step 8: Clean Up Empty Directories

Remove any empty directories created by the migration:

```bash
# Remove empty stories folders in features/
find features/ -type d -name "stories" -empty -delete

# Remove empty docs folders in features/
find features/ -type d -name "docs" -empty -delete

echo "Cleaned up empty directories"
```

### Step 9: Verify Migration

1. **Check feature structure is correct**:
   ```bash
   # Should only show status.xml, epics/, src/, tests/
   ls -la features/*/
   ```

2. **Check docs structure is correct**:
   ```bash
   # Should show all feature folders with stories/
   ls -la docs/development/features/*/
   ls -la docs/development/features/*/stories/
   ```

3. **Verify no stories remain in features/**:
   ```bash
   find features/ -name "[0-9]*.[0-9]*.md" -type f
   # Should return nothing
   ```

4. **Verify all stories are in docs/**:
   ```bash
   find docs/development/features/ -name "[0-9]*.[0-9]*.md" -type f
   # Should list all story files
   ```

5. **Check status.xml files reference correct paths**:
   ```bash
   grep -h "Story file location" features/*/status.xml
   # All should show: docs/development/features/
   ```

### Step 10: Git Commit

Create a comprehensive git commit documenting the migration:

```bash
git add -A

git commit -m "fix: migrate story files to correct docs/development/features structure

Migrated story folder structure from incorrect locations to correct paths.

Before (WRONG):
- features/[name]/stories/
- features/[name]/docs/stories/
- features/[name]/[epic.story].md (directly)

After (CORRECT):
- docs/development/features/[name]/stories/[epic.story].md

Changes Made:

1. Created docs/development/features/[name]/ for each feature
2. Created stories/ subdirectories in correct location
3. Moved all story files ([epic.story].md format)
4. Moved all documentation files (INDEX.md, FEATURE_SPEC.md, etc.)
5. Updated status.xml files to reference correct story paths
6. Updated .claude/commands/ files with correct paths
7. Removed empty directories from features/
8. Verified all references now point to correct location

Migration completed successfully. All stories now in:
docs/development/features/[feature-name]/stories/

Features directory now only contains:
- status.xml (tracking)
- epics/ (task breakdown)
- src/ (code)
- tests/ (tests)
"
```

---

## Verification Checklist

After completing all steps, verify:

- [ ] All story files moved to `docs/development/features/[name]/stories/`
- [ ] No story files remain in `features/` directory
- [ ] Documentation files in `docs/development/features/[name]/`
- [ ] All `status.xml` files reference correct story paths
- [ ] `.claude/commands/create-story.md` has correct paths
- [ ] `.claude/commands/create-feature.md` has correct structure
- [ ] No empty `docs/` or `stories/` folders in `features/` directory
- [ ] `features/[name]/` only contains: status.xml, epics/, src/, tests/
- [ ] Git commit created documenting migration

---

## Expected Final Structure Example

For a feature named "devdev-core":

```
features/
└── devdev-core/
    ├── status.xml
    ├── epics/
    │   ├── epic-1-foundation/
    │   │   ├── DESCRIPTION.md
    │   │   ├── TASKS.md
    │   │   └── NOTES.md
    │   └── epic-2-core/
    │       ├── DESCRIPTION.md
    │       ├── TASKS.md
    │       └── NOTES.md
    ├── src/
    └── tests/

docs/
└── development/
    └── features/
        └── devdev-core/
            ├── INDEX.md
            ├── FEATURE_SPEC.md
            ├── TECHNICAL_DESIGN.md
            ├── TASKS.md
            ├── CHANGELOG.md
            └── stories/
                ├── 1.1.md
                ├── 1.2.md
                ├── 2.1.md
                └── 2.2.md
```

---

## Troubleshooting

### Issue: Permission denied when moving files
**Solution**: Check file permissions, use `sudo` if necessary (be careful!)

### Issue: status.xml not updating correctly
**Solution**: Manually edit the file, search for any story references and update them

### Issue: Some story files have different naming
**Solution**: Manually move non-standard named files, ensure they follow X.Y.md format

### Issue: Features directory structure varies
**Solution**: Adapt the scripts for your specific structure, main principle: stories go in docs/development/features/[name]/stories/

---

## Notes

- **BACKUP FIRST**: Before running these commands, create a backup of your project
- **TEST ON ONE FEATURE**: Try the migration on one feature first, verify it works
- **ADJUST PATHS**: If your project structure differs, adjust the paths accordingly
- **VERIFY CAREFULLY**: After migration, verify all story references work correctly

This migration is ONE-TIME only. After completion, all future story files will be created in the correct location automatically if you're using the updated meta prompt system.
