# Loom Framework Scripts

This directory contains core automation scripts for the Loom framework.

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

See update-setup.md for integration with the update workflow.

---

## sync-loom-files.sh

**Purpose**: Intelligently copy agent templates, command templates, and skills from the Loom framework source to a target project directory.

### Quick Start

```bash
# Sync to current directory
bash scripts/sync-loom-files.sh .

# Sync to specific project
bash scripts/sync-loom-files.sh /path/to/my-project

# Dry run (preview changes)
bash scripts/sync-loom-files.sh /path/to/my-project true
```

### What Gets Synced

The script syncs these directories from Loom framework to target project:

- **Agent templates**: `.claude/agents/*.md` → `.claude/agents/*.md`
- **Command templates**: `.claude/commands/*.md` → `.claude/commands/*.md`
- **Skills**: `.claude/skills/*` → `.claude/skills/*`

### Features

- **Hash-based detection**: Uses SHA256 to detect file changes
- **Smart updates**: Only copies when source differs from target
- **Color-coded output**:
  - GREEN: File created
  - YELLOW: File updated
  - (Quiet): File skipped (no changes)
- **Dry run mode**: Preview changes without modifying files
- **Source:target mapping**: Flexible path mapping syntax

### Usage

```bash
bash scripts/sync-loom-files.sh [TARGET_DIR] [DRY_RUN]
```

**Parameters**:
- `TARGET_DIR`: Target project directory (required)
- `DRY_RUN`: "true" for dry run, "false" for actual sync (default: "false")

**Examples**:

```bash
# Sync to current directory
bash scripts/sync-loom-files.sh .

# Dry run to preview changes
bash scripts/sync-loom-files.sh /path/to/project true

# Sync to specific directory
bash scripts/sync-loom-files.sh /path/to/project false
```

### Output Example

```
================================================
      Loom Framework Files Synchronization
================================================
Source:  /Users/dev/loom
Target:  /Users/dev/my-project
Dry Run: false
================================================

Syncing directory: .claude/agents → .claude/agents
  CREATE:  coordinator.md
  CREATE:  senior-developer.md
  UPDATE:  test-specialist.md (hashes differ)
  ...

Syncing directory: .claude/commands → .claude/commands
  CREATE:  dev.md
  CREATE:  commit.md
  ...

✅ Synchronization complete.
```

### Integration

This script is used by setup.md and update-setup.md workflows to copy framework files into user projects.

---

## deploy-claude-md.sh

**Purpose**: Deploy the CLAUDE.md operating manual to user projects with project-specific customization.

### Quick Start

```bash
bash scripts/deploy-claude-md.sh \
  "." \
  "My Project" \
  "Next.js 14, TypeScript, Prisma" \
  "STRICT" \
  "npm run dev" \
  "npm test" \
  "npm run build"
```

### What It Does

1. Creates CLAUDE.md in target project root
2. Inserts project-specific configuration
3. Uses marker-based template system
4. Preserves custom sections between markers

### Features

- **Template-based**: Uses `prompts/reference/claude-md-template.md`
- **Marker system**: `<!-- LOOM_FRAMEWORK_START -->` and `<!-- LOOM_FRAMEWORK_END -->`
- **Project customization**: Injects project name, tech stack, TDD level, commands
- **Safe updates**: Preserves content outside markers

### Usage

```bash
bash scripts/deploy-claude-md.sh \
  [TARGET_DIR] \
  [PROJECT_NAME] \
  [TECH_STACK] \
  [TDD_LEVEL] \
  [PREVIEW_CMD] \
  [TEST_CMD] \
  [BUILD_CMD]
```

**Parameters**:
- `TARGET_DIR`: Target project directory (absolute path or ".")
- `PROJECT_NAME`: Name of the project
- `TECH_STACK`: Technology stack description
- `TDD_LEVEL`: STRICT | RECOMMENDED | OPTIONAL
- `PREVIEW_CMD`: Development server command (e.g., "npm run dev")
- `TEST_CMD`: Test execution command (e.g., "npm test")
- `BUILD_CMD`: Build command (e.g., "npm run build")

**Example**:

```bash
bash /path/to/loom/scripts/deploy-claude-md.sh \
  "." \
  "E-Commerce Platform" \
  "Next.js 14, React 18, TypeScript, Prisma, PostgreSQL" \
  "STRICT" \
  "npm run dev" \
  "npm test" \
  "npm run build"
```

### Integration

This script is used by setup.md workflow (Phase 4) to deploy CLAUDE.md during initial project setup.
