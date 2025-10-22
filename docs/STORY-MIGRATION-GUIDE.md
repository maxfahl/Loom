# Story Migration Guide

**Purpose**: Migrate stories from old/wrong locations to correct location per meta prompt spec

**Created**: 2025-10-22

**Status**: Ready for automated execution

---

## Problem Summary

Stories are currently in wrong locations:
- ❌ `docs/stories/1.1.md`, `docs/stories/1.2.md`, etc.
- ❌ `features/[feature]/stories/` (also wrong)

Correct location per meta prompt:
- ✅ `docs/development/features/[feature-name]/epics/[epic-name]/stories/X.Y.md`

---

## Migration Overview

### What's Being Migrated
- All user story files from old locations
- Named as `X.Y.md` (e.g., `1.1.md`, `1.2.md`, `2.1.md`)
- X = epic number, Y = story number within epic

### Where From
- Primary source: `docs/stories/`
- Secondary source: `features/*/stories/`

### Where To
- Target: `docs/development/features/[feature-name]/epics/epic-[X]-[name]/stories/X.Y.md`

---

## Step-by-Step Migration Process

### Step 1: Identify Active Feature and Old Stories

```bash
# Check what features are in development
cat docs/development/status.xml | grep "<feature-name>"
# Output: <feature-name>my-feature</feature-name>

# Find all old story locations
echo "=== Stories at docs/stories/ ==="
ls -la docs/stories/*.md 2>/dev/null || echo "None found"

echo "=== Stories at features/*/stories/ ==="
find features -name "*.md" -path "*/stories/*" 2>/dev/null || echo "None found"

echo "=== Stories at wrong docs/development/features/*/stories/ ==="
find docs/development/features -name "*.md" -path "*/stories/*" -not -path "*/epics/*" 2>/dev/null || echo "None found"
```

### Step 2: Extract Epic Information

For each story file `X.Y.md`, determine:
- X = epic number
- Y = story number

Examples:
- `1.1.md` → Epic 1, Story 1
- `2.3.md` → Epic 2, Story 3
- `1.10.md` → Epic 1, Story 10

```bash
# List all stories to identify epic numbering
ls -1 docs/stories/*.md 2>/dev/null | xargs -I {} basename {} | sort
# Output:
# 1.1.md
# 1.2.md
# 1.3.md
# 2.1.md
# (etc.)
```

### Step 3: Identify Epic Names

Check for existing epic directories:

```bash
# Look at existing epic structure
find docs/development/features -type d -name "epic-*"

# Example output:
# docs/development/features/my-feature/epics/epic-1-foundation
# docs/development/features/my-feature/epics/epic-2-core
# docs/development/features/my-feature/epics/epic-3-polish
```

If epic directories don't exist, you'll need to create them based on epic planning.

### Step 4: Create Target Directory Structure

For each epic that will contain stories:

```bash
# Template (replace [feature-name] and [epic-number] and [epic-name]):
mkdir -p docs/development/features/[feature-name]/epics/epic-[X]-[name]/stories

# Example for 3 epics:
mkdir -p docs/development/features/my-feature/epics/epic-1-foundation/stories
mkdir -p docs/development/features/my-feature/epics/epic-2-core/stories
mkdir -p docs/development/features/my-feature/epics/epic-3-polish/stories
```

### Step 5: Move Story Files

For each story file, move it to the correct location:

```bash
# Template:
# mv docs/stories/[X].[Y].md docs/development/features/[feature-name]/epics/epic-[X]-[name]/stories/[X].[Y].md

# Example:
mv docs/stories/1.1.md docs/development/features/my-feature/epics/epic-1-foundation/stories/1.1.md
mv docs/stories/1.2.md docs/development/features/my-feature/epics/epic-1-foundation/stories/1.2.md
mv docs/stories/2.1.md docs/development/features/my-feature/epics/epic-2-core/stories/2.1.md
```

### Step 6: Update status.xml References

Edit `docs/development/status.xml`:

**Find and update**:
```xml
<!-- Old reference (if any) -->
<current-story>docs/stories/1.1.md</current-story>

<!-- New reference -->
<current-story>docs/development/features/my-feature/epics/epic-1-foundation/stories/1.1.md</current-story>
```

If using just story number (X.Y format), no change needed. But verify the coordinate structure is correct.

### Step 7: Verify Migration

Run verification commands:

```bash
echo "=== Verify old locations are empty ==="
ls -la docs/stories/ 2>&1 | grep -c "No such file" && echo "✅ docs/stories/ removed or empty" || echo "❌ docs/stories/ still has files"

find features -name "*.md" -path "*/stories/*" | wc -l && echo "❌ Stories still in features/ folder" || echo "✅ No stories in features/ folder"

echo ""
echo "=== Verify new location has all stories ==="
find docs/development/features -name "*.md" -path "*/epics/*/stories/*" | wc -l
echo "Stories now at correct location"

echo ""
echo "=== List all migrated stories ==="
find docs/development/features -name "*.md" -path "*/epics/*/stories/*" | sort
```

### Step 8: Verify No Broken References

```bash
# Check for any remaining references to old story locations in CLAUDE.md
grep -n "docs/stories" CLAUDE.md 2>/dev/null && echo "⚠️ Found reference to docs/stories in CLAUDE.md" || echo "✅ No old references in CLAUDE.md"

# Check for references in documentation
grep -r "docs/stories" docs/ 2>/dev/null && echo "⚠️ Found references to docs/stories in docs/" || echo "✅ No old references in docs/"
```

---

## Automated Migration Script

### script: `scripts/migrate-stories.sh`

Create this script for automated migration:

```bash
#!/bin/bash

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Configuration
FEATURE_NAME="${1:-my-feature}"
DRY_RUN="${2:-false}"

echo -e "${YELLOW}Story Migration Script${NC}"
echo "Feature: $FEATURE_NAME"
echo "Dry Run: $DRY_RUN"
echo ""

# Step 1: Check for stories at old locations
echo -e "${YELLOW}[Step 1] Checking for stories at old locations...${NC}"

OLD_STORIES=$(find docs/stories -name "*.md" 2>/dev/null || echo "")
WRONG_LOCATION_STORIES=$(find features -name "*.md" -path "*/stories/*" 2>/dev/null || echo "")

STORY_COUNT=$(echo "$OLD_STORIES" | grep -c "\.md$" || echo 0)
WRONG_COUNT=$(echo "$WRONG_LOCATION_STORIES" | grep -c "\.md$" || echo 0)

if [ $STORY_COUNT -eq 0 ] && [ $WRONG_COUNT -eq 0 ]; then
  echo -e "${GREEN}✅ No stories found at old locations${NC}"
  exit 0
fi

echo -e "${YELLOW}Found $STORY_COUNT stories at docs/stories/${NC}"
echo -e "${YELLOW}Found $WRONG_COUNT stories at features/*/stories/${NC}"
echo ""

# Step 2: Create epic directories
echo -e "${YELLOW}[Step 2] Creating epic directories...${NC}"

# Extract unique epic numbers from story filenames
EPICS=$(echo "$OLD_STORIES" | xargs -I {} basename {} | cut -d'.' -f1 | sort -u)

for EPIC in $EPICS; do
  EPIC_DIR="docs/development/features/$FEATURE_NAME/epics/epic-$EPIC"
  STORIES_DIR="$EPIC_DIR/stories"

  if [ "$DRY_RUN" = "true" ]; then
    echo -e "${GREEN}[DRY RUN] Would create: $STORIES_DIR${NC}"
  else
    mkdir -p "$STORIES_DIR"
    echo -e "${GREEN}✅ Created: $STORIES_DIR${NC}"
  fi
done

echo ""

# Step 3: Move stories
echo -e "${YELLOW}[Step 3] Moving stories...${NC}"

for STORY_FILE in $OLD_STORIES; do
  FILENAME=$(basename "$STORY_FILE")
  EPIC=$(echo "$FILENAME" | cut -d'.' -f1)
  EPIC_DIR="docs/development/features/$FEATURE_NAME/epics/epic-$EPIC"
  TARGET="$EPIC_DIR/stories/$FILENAME"

  if [ "$DRY_RUN" = "true" ]; then
    echo -e "${GREEN}[DRY RUN] Would move: $STORY_FILE → $TARGET${NC}"
  else
    mv "$STORY_FILE" "$TARGET"
    echo -e "${GREEN}✅ Moved: $FILENAME → epic-$EPIC/stories/${NC}"
  fi
done

echo ""

# Step 4: Clean up empty directories
echo -e "${YELLOW}[Step 4] Cleaning up empty directories...${NC}"

if [ "$DRY_RUN" = "false" ]; then
  rmdir docs/stories 2>/dev/null && echo -e "${GREEN}✅ Removed empty docs/stories/ directory${NC}" || true
fi

echo ""

# Step 5: Verification
echo -e "${YELLOW}[Step 5] Verification...${NC}"

NEW_STORY_COUNT=$(find docs/development/features/$FEATURE_NAME -name "*.md" -path "*/epics/*/stories/*" 2>/dev/null | wc -l)

if [ "$DRY_RUN" = "false" ]; then
  if [ "$NEW_STORY_COUNT" -eq "$STORY_COUNT" ]; then
    echo -e "${GREEN}✅ All $STORY_COUNT stories migrated successfully${NC}"
  else
    echo -e "${RED}❌ Migration count mismatch: Expected $STORY_COUNT, found $NEW_STORY_COUNT${NC}"
    exit 1
  fi
else
  echo -e "${GREEN}[DRY RUN] Would have $STORY_COUNT stories at correct location${NC}"
fi

echo ""
echo -e "${GREEN}Migration complete!${NC}"
```

### Usage

```bash
# Dry run first (no changes)
bash scripts/migrate-stories.sh my-feature true

# Actual migration
bash scripts/migrate-stories.sh my-feature false

# Or with environment variables
DRY_RUN=true FEATURE=my-feature bash scripts/migrate-stories.sh
```

---

## Rollback Procedure

If migration needs to be reversed:

```bash
#!/bin/bash
# Reverse migration (move stories back to old location)

mkdir -p docs/stories

find docs/development/features -name "*.md" -path "*/epics/*/stories/*" | while read story; do
  filename=$(basename "$story")
  cp "$story" "docs/stories/$filename"
  echo "Recovered: $filename"
done

echo "Stories recovered to docs/stories/"
echo "Note: Original files remain in epics/stories/ - delete manually if needed"
```

---

## Verification Checklist

After migration, verify:

- [ ] Old `docs/stories/` directory is empty or removed
- [ ] No stories remain at `features/*/stories/`
- [ ] All stories now at `docs/development/features/[feature]/epics/epic-X/stories/X.Y.md`
- [ ] `status.xml` updated with correct story paths (if references used)
- [ ] All story files readable and intact
- [ ] Tests still pass (if any reference story paths)
- [ ] Documentation updated (if references old locations)

---

## Troubleshooting

### Problem: "Cannot create directory" error

**Cause**: Parent directories don't exist

**Fix**: Ensure epic parent directories exist first
```bash
mkdir -p docs/development/features/[feature-name]/epics/
```

### Problem: Story file not found after migration

**Cause**: File already moved or wrong path

**Fix**: Search for story file
```bash
find . -name "X.Y.md" -type f
```

### Problem: status.xml references still point to old location

**Cause**: status.xml not updated

**Fix**: Edit status.xml and update story path references

---

## Summary

Migration process:
1. ✅ Identify old story locations
2. ✅ Create target epic directories
3. ✅ Move stories to new locations
4. ✅ Update status.xml (if needed)
5. ✅ Verify migration complete
6. ✅ Clean up old directories

All stories now organized under `docs/development/features/[feature]/epics/[epic]/stories/` per meta prompt spec.

