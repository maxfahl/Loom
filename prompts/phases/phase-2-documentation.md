# Phase 2: Documentation Creation

**Part of**: [Project Setup Meta Prompt](../project-setup-meta-prompt.md)

## Overview

Create 12+ documentation files (or ~4-6 if using template project).

## Documentation Templates

All documentation templates are in: [doc-templates.md](../templates/doc-templates.md)

## Creation Order

**IF BROWNFIELD** (existing project):
1. **PROJECT_OVERVIEW.md** (First)
   - Launch Explore agent for comprehensive analysis
   - Foundation for all other docs
   - See Phase 1 for brownfield analysis workflow

**ALL PROJECTS** (brownfield or greenfield):
2. **INDEX.md** - Documentation navigation
3. **PRD.md** - Product requirements
4. **TECHNICAL_SPEC.md** - Technical specifications
5. **ARCHITECTURE.md** - System architecture
6. **DESIGN_SYSTEM.md** - UI/UX guidelines (if applicable)
7. **DEVELOPMENT_PLAN.md** - Development workflow and TDD
8. **CODE_REVIEW_PRINCIPLES.md** - 7-phase code review framework (Phase 1)
9. **SECURITY_REVIEW_CHECKLIST.md** - OWASP security scanning methodology (Phase 2)
10. **DESIGN_PRINCIPLES.md** - UI/UX design review with Playwright and WCAG 2.1 AA (Phase 3)
11. **HOOKS_REFERENCE.md** - Claude Code hooks (if monitoring project)
12. **TASKS.md** - Development tasks
13. **START_HERE.md** - Getting started guide
14. **PROJECT_SUMMARY.md** - Executive summary
15. **Domain-specific docs** (API_REFERENCE.md, etc.)

## ⚡ CRITICAL: Parallel Creation (70% Time Savings)

**Total Time: ~5 minutes (vs ~30 minutes sequential)**

**ALWAYS create docs in parallel batches** - see [parallelization-patterns.md](../reference/parallelization-patterns.md)

### Batch Execution (3 batches)

**Batch 1** (6 docs in parallel):
- PRD.md
- TECHNICAL_SPEC.md
- ARCHITECTURE.md
- DEVELOPMENT_PLAN.md
- DESIGN_SYSTEM.md
- TASKS.md

**Batch 2** (7 docs in parallel):
- INDEX.md (requires other docs for navigation)
- CODE_REVIEW_PRINCIPLES.md
- SECURITY_REVIEW_CHECKLIST.md
- DESIGN_PRINCIPLES.md
- HOOKS_REFERENCE.md
- PROJECT_SUMMARY.md
- EXECUTIVE_SUMMARY.md

**Batch 3** (2 docs in parallel):
- START_HERE.md (requires INDEX.md)
- CLAUDE.md (requires all other docs)

### What NOT to Do

❌ **WRONG** - Sequential:
```
Create PRD → wait → Create TECHNICAL_SPEC → wait → Create ARCHITECTURE → wait...
```

✅ **CORRECT** - Parallel batches:
```
Create 6 docs in parallel (Batch 1) → wait → Create 4 docs in parallel (Batch 2) → wait → Create 2 docs in parallel (Batch 3)
```

## Brownfield vs Greenfield

**Brownfield**:
- Read PROJECT_OVERVIEW.md for all context
- Reference existing architecture, features, stack
- Merge with existing documentation
- **Proceed to Phase 2.5 for legacy doc cleanup**

**Greenfield**:
- Create from user's project description
- Define new architecture and design
- No existing docs to merge
- **Skip Phase 2.5** (no legacy docs to clean up)

---

## Phase 2.5: Legacy Documentation Cleanup (Brownfield Only)

**Run this phase ONLY for brownfield projects after Phase 2 completes.**

**Purpose**: Clean up legacy documentation after new Loom documentation has been created.

### Step 2.5.1: Scan for Legacy Documentation

1. **Read Legacy Mapping from PROJECT_OVERVIEW.md**:
   - Look for "## Existing Documentation" section
   - Review the "Legacy Documentation Mapping" table
   - Identify which files were marked Transform/Merge/Keep

2. **Categorize Legacy Files**:

   **Definitely Can Remove** (content transformed to new docs):
   - Old READMEs that have been replaced
   - Architecture docs merged into ARCHITECTURE.md
   - Design docs merged into DESIGN_SYSTEM.md
   - Development guides merged into DEVELOPMENT_PLAN.md

   **Possibly Can Remove** (check if content is duplicated):
   - API documentation (check if in TECHNICAL_SPEC.md or API_REFERENCE.md)
   - Setup guides (check if in START_HERE.md)
   - Code standards (check if in CLAUDE.md)

   **Should Keep** (unique content not in new docs):
   - Historical decision logs
   - Legacy system migration notes
   - Project-specific edge case documentation
   - External integration details not yet captured

### Step 2.5.2: Present Cleanup Options to User

Show user the categorized files and offer 4 options:

```markdown
## Legacy Documentation Cleanup

I've created new Loom documentation. Here's what to do with your legacy docs:

### Definitely Can Remove (content transformed):
- docs/old-readme.md → Transformed to docs/development/README.md
- wiki/architecture.md → Merged into docs/development/ARCHITECTURE.md
- DESIGN.md → Transformed to docs/development/DESIGN_SYSTEM.md

### Possibly Can Remove (check for duplicates):
- api-docs/ → May be in docs/development/TECHNICAL_SPEC.md
- setup.md → May be in docs/development/START_HERE.md

### Should Keep (unique content):
- legacy/migration-notes.md → Historical context
- docs/integrations/ → External API details

---

**Choose cleanup option**:

A) **Archive** - Move all "Definitely" and "Possibly" files to `archive/legacy-docs/` with timestamp
B) **Backup** - Create `.backup/` folder with all legacy docs, then delete originals
C) **Delete** - Delete all "Definitely" files, keep "Possibly" and "Should Keep"
D) **Keep** - Keep everything as-is (no cleanup)

Which option? (A/B/C/D)
```

### Step 2.5.3: Execute Cleanup (Based on User Choice)

**Option A: Archive**

```bash
# Create archive folder
mkdir -p archive/legacy-docs-$(date +%Y%m%d)

# Move definitely removable files
mv docs/old-readme.md archive/legacy-docs-$(date +%Y%m%d)/
mv wiki/architecture.md archive/legacy-docs-$(date +%Y%m%d)/
mv DESIGN.md archive/legacy-docs-$(date +%Y%m%d)/

# Move possibly removable files
mv api-docs/ archive/legacy-docs-$(date +%Y%m%d)/
mv setup.md archive/legacy-docs-$(date +%Y%m%d)/

# Create README in archive
echo "# Legacy Documentation Archive

Archived on $(date)

These documents have been transformed into Loom format.
See docs/development/ for new documentation structure.

## Mapping

- old-readme.md → docs/development/README.md
- architecture.md → docs/development/ARCHITECTURE.md
- DESIGN.md → docs/development/DESIGN_SYSTEM.md
" > archive/legacy-docs-$(date +%Y%m%d)/README.md
```

**Option B: Backup**

```bash
# Create backup folder
mkdir -p .backup/docs-$(date +%Y%m%d)

# Copy all legacy docs
cp -r docs/ .backup/docs-$(date +%Y%m%d)/
cp -r wiki/ .backup/docs-$(date +%Y%m%d)/ 2>/dev/null || true
cp DESIGN.md .backup/docs-$(date +%Y%m%d)/ 2>/dev/null || true

# Delete originals (except "Should Keep")
rm -f docs/old-readme.md
rm -rf wiki/architecture.md
rm -f DESIGN.md
rm -rf api-docs/
rm -f setup.md

echo "✅ Backup created in .backup/docs-$(date +%Y%m%d)/"
```

**Option C: Delete**

```bash
# Delete only "Definitely" removable files
rm -f docs/old-readme.md
rm -rf wiki/architecture.md
rm -f DESIGN.md

# Keep "Possibly" and "Should Keep" files for manual review
echo "✅ Deleted definitely removable files"
echo "⚠️  Please manually review:"
echo "   - api-docs/ (possibly duplicate)"
echo "   - setup.md (possibly duplicate)"
echo "   - legacy/migration-notes.md (unique content, keep)"
```

**Option D: Keep**

```bash
echo "✅ No cleanup performed - all legacy docs retained"
```

### Step 2.5.4: Update README.md

Remove references to deleted documentation:

1. **Read README.md**
2. **Find and remove** links to deleted files
3. **Update** "Documentation" section to point to `docs/development/INDEX.md`
4. **Add note** about archived/backed up docs (if applicable)

Example update:

```markdown
## Documentation

All project documentation is in `docs/development/`. Start with:
- [INDEX.md](docs/development/INDEX.md) - Complete documentation index

Legacy documentation has been archived in `archive/legacy-docs-20251022/`.
```

### Step 2.5.5: Verify Cleanup

1. **Check for broken links**: `grep -r "docs/old-readme" .`
2. **Verify archive/backup**: `ls -la archive/` or `ls -la .backup/`
3. **Confirm no information loss**: Compare legacy mapping with new docs
4. **Report to user**: "✅ Cleanup complete. X files archived/deleted."

---

## Related Files
- [doc-templates.md](../templates/doc-templates.md) - All documentation templates
- [phase-1-discovery.md](phase-1-discovery.md) - Brownfield analysis (includes legacy mapping)
- [template-system.md](../reference/template-system.md) - Template copying
- [parallelization-patterns.md](../reference/parallelization-patterns.md) - Pattern 4: Brownfield Cleanup
