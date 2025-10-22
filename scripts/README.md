# Migration Scripts

This directory contains automation scripts for maintaining and migrating the AgentDevMetaPrompt repository structure.

## migrate-stories.sh

**Purpose**: Automate the migration of user stories from old/incorrect locations to the correct location per meta prompt specification.

### Quick Start

```bash
# Dry run (recommended first)
bash scripts/migrate-stories.sh my-feature true

# Actual migration
bash scripts/migrate-stories.sh my-feature false
```

### Features

- **Multi-location detection**: Finds stories at:
  - `docs/stories/`
  - `features/*/stories/`
  - `docs/development/features/*/stories/` (wrong location)

- **Smart epic extraction**: Automatically extracts epic numbers from story filenames (X.Y.md → Epic X)

- **Color-coded output**:
  - GREEN: Success messages
  - YELLOW: Status/progress
  - RED: Errors/warnings
  - BLUE: Dry run indicators

- **Dry run mode**: Test migrations without making changes

- **Idempotent**: Safe to run multiple times

- **Error handling**:
  - Validates story filenames
  - Warns about invalid files
  - Verifies migration counts
  - Gracefully handles edge cases

### Usage

```bash
bash scripts/migrate-stories.sh [FEATURE_NAME] [DRY_RUN]
```

**Parameters**:
- `FEATURE_NAME`: Target feature name (default: "my-feature")
- `DRY_RUN`: "true" for dry run, "false" for actual migration (default: "false")

**Examples**:

```bash
# Dry run for 'auth-system' feature
bash scripts/migrate-stories.sh auth-system true

# Migrate stories for 'payment-flow' feature
bash scripts/migrate-stories.sh payment-flow false

# Use defaults (my-feature, no dry run)
bash scripts/migrate-stories.sh
```

### Migration Process

The script follows these steps:

1. **Check for old stories** - Scans all old locations and reports counts
2. **Create epic directories** - Creates target directory structure
3. **Move story files** - Migrates stories to correct locations
4. **Clean up** - Removes empty old directories
5. **Verification** - Validates migration success

### Output Example

```
================================================
         Story Migration Script
================================================
Feature: my-feature
Dry Run: false
================================================

[Step 1] Checking for stories at old locations...
Found 4 stories at docs/stories/
Found 0 stories at features/*/stories/
Found 0 stories at docs/development/features/*/stories/ (wrong location)
Total stories to migrate: 4

[Step 2] Creating epic directories...
✅ Created: docs/development/features/my-feature/epics/epic-1/stories
✅ Created: docs/development/features/my-feature/epics/epic-2/stories

[Step 3] Moving stories...
✅ Moved: 1.1.md → epic-1/stories/
✅ Moved: 1.2.md → epic-1/stories/
✅ Moved: 2.1.md → epic-2/stories/
✅ Moved: 2.2.md → epic-2/stories/

[Step 4] Cleaning up empty directories...
✅ Removed empty: docs/stories/

[Step 5] Verification...
✅ All 4 stories migrated successfully

Migration Summary:
  - Migrated stories: 4
  - New location: docs/development/features/my-feature/epics/epic-*/stories/

Stories by epic:
  - Epic 1: 2 stories
  - Epic 2: 2 stories

================================================
✅ Migration complete!
================================================
```

### Error Handling

The script handles various edge cases:

- **Invalid filenames**: Warns and skips files that don't match X.Y.md pattern
- **Count mismatch**: Exits with error if migration count doesn't match
- **Non-empty directories**: Doesn't remove directories that still contain files
- **Missing directories**: Creates parent directories as needed

### Integration

This script is used by the **Structure Updater** agent in the update workflow. It can also be run manually by developers as needed.

### Reference Documentation

See `/Users/maxfahl/Fahl/Common/AgentDevMetaPrompt/docs/STORY-MIGRATION-GUIDE.md` for complete migration context and manual procedures.
