# Update Workflow Fix Plan

**Status**: COMPREHENSIVE FIX FOR CLAUDE CODE UPDATE FAILURES

**Purpose**: Fix the update workflow to ensure ALL agents, commands, and features are created/updated correctly

**Date Created**: 2025-10-22

---

## Executive Summary

The previous update workflow had critical gaps that prevented Claude Code from:
1. Creating all 13 required agents
2. Creating all 12+ required commands (especially `/dev-yolo`)
3. Properly migrating/organizing stories to correct folder structure

This plan provides **mechanical, checkpoint-based fixes** with explicit checklists and hard stops.

---

## Part 1: Root Causes Identified

### Root Cause 1: Vague Validator Instructions
- Validators told to "read meta prompt section" without specifying exact source
- No mechanical checklist format for validation reports
- Reports were narrative instead of actionable

### Root Cause 2: No Hard Stop Enforcement
- Update phase completed incompletely without stopping at checkpoints
- No verification that critical agents/commands were created
- Assumed optional components were truly optional

### Root Cause 3: Conflicting Story Location Instructions
- Phase-6 said stories go in `docs/development/features/[feature]/epics/[epic]/stories/`
- But old code had stories in `docs/stories/`
- Update workflow never forced migration

### Root Cause 4: "/dev-yolo" Command Ambiguity
- Validator said "11+ commands" (vague count)
- Claude Code created `/dev` and `/yolo` as separate commands
- Never created the combined `/dev-yolo` command

### Root Cause 5: Missing Mechanical Verification
- Validation reports couldn't be mechanically executed by updaters
- No "create exactly these X items" checklists
- Updaters relied on human judgment instead of automation

---

## Part 2: Files to Update

### Section A: Prompt Files to Update

| File | Change | Type |
|------|--------|------|
| `prompts/update-mode/validation-workflow.md` | Add mechanical validation checklists | CRITICAL |
| `prompts/phases/phase-4-commands.md` | Add explicit command list with counts | CRITICAL |
| `prompts/phases/phase-3-agents.md` | Add explicit agent list with counts | CRITICAL |
| `prompts/phases/phase-6-features-setup.md` | Add story migration instructions | CRITICAL |
| `prompts/reference/core-agents.md` | Verify agent list is authoritative | REFERENCE |
| `prompts/reference/status-xml.md` | Verify status.xml location is clear | REFERENCE |

### Section B: Documentation to Create

| File | Purpose |
|------|---------|
| `docs/UPDATE-WORKFLOW-ENHANCEMENTS.md` | Detailed enhancement specifications |
| `docs/MECHANICAL-VALIDATION-SPEC.md` | How validators should work mechanically |
| `docs/STORY-MIGRATION-GUIDE.md` | Step-by-step story migration process |

---

## Part 3: Detailed Fix Actions

### Fix Group 1: Validation Workflow Enhancements

**Target File**: `prompts/update-mode/validation-workflow.md`

**Changes Required**:

#### 1.1 Add "Authoritative Source Reading" Section

Add after line 85 (before Agent 1):

```markdown
### Authoritative Sources (READ THESE FIRST)

Before validating, each validator MUST read these authoritative references:

**For Agents**:
- `prompts/reference/core-agents.md` - Lists all 13 required core agents by name
- Extract agent names into a mechanical checklist

**For Commands**:
- `prompts/phases/phase-4-commands.md` - Lists all 12+ required commands by name
- Extract command names into a mechanical checklist (lines 17-32)

**For Features**:
- `prompts/phases/phase-6-features-setup.md` - Specifies exact folder structure
- `prompts/reference/status-xml.md` - Specifies status.xml structure

**For Documentation**:
- `prompts/templates/doc-templates.md` - Lists all 12+ required documentation files

This prevents validators from guessing or estimating. Everything is explicit.
```

#### 1.2 Replace Agent 2 Validator Instructions with Mechanical Checklist

Replace current "Agent 2: Agent Structure Validator" section with:

```markdown
**Agent 2: Agent Structure Validator - MECHANICAL CHECKLIST**

```markdown
Task: Validate all agents against authoritative spec using mechanical checklist

**STEP 1: Read Authoritative Source**
- Read `prompts/reference/core-agents.md`
- Extract the 13 core agent names: coordinator, senior-developer, test-writer, code-reviewer, bug-finder, refactor-specialist, qa-tester, git-helper, architecture-advisor, performance-optimizer, documentation-writer, agent-creator, skill-creator

**STEP 2: Create Mechanical Checklist**

For EACH agent in the list above, check agent file and complete this checklist:

```
CORE AGENTS (REQUIRED - 13 total):
- [ ] 1. coordinator at .claude/agents/coordinator.md - YAML OK? [ ] - Has MCP? [ ]
- [ ] 2. senior-developer at .claude/agents/senior-developer.md - YAML OK? [ ] - Has MCP? [ ]
- [ ] 3. test-writer at .claude/agents/test-writer.md - YAML OK? [ ] - Has MCP? [ ]
- [ ] 4. code-reviewer at .claude/agents/code-reviewer.md - YAML OK? [ ] - Has 7-phase? [ ]
- [ ] 5. bug-finder at .claude/agents/bug-finder.md - YAML OK? [ ] - Has MCP? [ ]
- [ ] 6. refactor-specialist at .claude/agents/refactor-specialist.md - YAML OK? [ ] - Has MCP? [ ]
- [ ] 7. qa-tester at .claude/agents/qa-tester.md - YAML OK? [ ] - Has MCP? [ ]
- [ ] 8. git-helper at .claude/agents/git-helper.md - YAML OK? [ ] - Has MCP? [ ]
- [ ] 9. architecture-advisor at .claude/agents/architecture-advisor.md - YAML OK? [ ] - Has MCP? [ ]
- [ ] 10. performance-optimizer at .claude/agents/performance-optimizer.md - YAML OK? [ ] - Has MCP? [ ]
- [ ] 11. documentation-writer at .claude/agents/documentation-writer.md - YAML OK? [ ] - Has MCP? [ ]
- [ ] 12. agent-creator at .claude/agents/agent-creator.md - YAML OK? [ ] - Has MCP? [ ]
- [ ] 13. skill-creator at .claude/agents/skill-creator.md - YAML OK? [ ] - Has MCP? [ ]

OPTIONAL AGENTS (RECOMMENDED):
- [ ] security-reviewer at .claude/agents/security-reviewer.md - YAML OK? [ ] - Model = Opus? [ ]
- [ ] design-reviewer at .claude/agents/design-reviewer.md - YAML OK? [ ] - Model = Sonnet? [ ]

STEP 3: Count Existing Agents
ls -la .claude/agents/ | wc -l
Expected: 13+ files

STEP 4: Deliverable

**CRITICAL**: Do NOT return narrative. Return this exact format:

AGENT VALIDATION RESULT:
EXISTS: [list of agent names that exist]
MISSING: [list of agent names that are missing - IF ANY, mark as CRITICAL]
NEEDS_UPDATE: [list of agents missing required content like 7-phase framework]
TOTAL: X/13 core agents exist
ACTION_REQUIRED: [YES if ANY missing, NO if all 13 exist]

IF MISSING ANY CORE AGENT:
ABORT_VALIDATION: true
REPORT_TO_COORDINATOR: "These agents are MISSING and MUST be created before proceeding: [list]"
```

**CRITICAL**: If this checklist shows ANY agent is missing, **STOP and report to coordinator immediately**. Do not continue validation.
```

#### 1.3 Replace Command Validator with Mechanical Checklist

Replace current "Agent 3: Command Structure Validator" with:

```markdown
**Agent 3: Command Structure Validator - MECHANICAL CHECKLIST**

```markdown
Task: Validate all commands against authoritative spec using mechanical checklist

**STEP 1: Read Authoritative Source**
- Read `prompts/phases/phase-4-commands.md` lines 17-32
- Extract the 12 REQUIRED command names

**STEP 2: Create Mechanical Checklist**

For EACH command in the list, check file and complete this checklist:

```
CORE COMMANDS (REQUIRED - 12 total):
- [ ] 1. /dev at .claude/commands/dev.md - YAML OK? [ ]
- [ ] 2. /dev-yolo at .claude/commands/dev-yolo.md - YAML OK? [ ] - Spawns coordinator? [ ]
- [ ] 3. /commit at .claude/commands/commit.md - YAML OK? [ ]
- [ ] 4. /review at .claude/commands/review.md - YAML OK? [ ] - Has 7-phase? [ ]
- [ ] 5. /status at .claude/commands/status.md - YAML OK? [ ]
- [ ] 6. /test at .claude/commands/test.md - YAML OK? [ ]
- [ ] 7. /plan at .claude/commands/plan.md - YAML OK? [ ]
- [ ] 8. /docs at .claude/commands/docs.md - YAML OK? [ ]
- [ ] 9. /yolo at .claude/commands/yolo.md - YAML OK? [ ] - For configuration? [ ]
- [ ] 10. /create-feature at .claude/commands/create-feature.md - YAML OK? [ ]
- [ ] 11. /correct-course at .claude/commands/correct-course.md - YAML OK? [ ]
- [ ] 12. /create-story at .claude/commands/create-story.md - YAML OK? [ ] - Correct folder path? [ ]

OPTIONAL COMMANDS (RECOMMENDED):
- [ ] /security-review at .claude/commands/security-review.md - YAML OK? [ ] - Spawns Opus? [ ]
- [ ] /design-review at .claude/commands/design-review.md - YAML OK? [ ] - Spawns design-reviewer? [ ]

STEP 3: Count Existing Commands
ls -la .claude/commands/ | wc -l
Expected: 12+ files

STEP 4: Deliverable

**CRITICAL**: Do NOT return narrative. Return this exact format:

COMMAND VALIDATION RESULT:
EXISTS: [list of command names that exist]
MISSING: [list of command names that are missing - IF ANY, mark as CRITICAL]
TOTAL: X/12 core commands exist
ACTION_REQUIRED: [YES if ANY missing, NO if all 12 exist]

CRITICAL_CHECKS:
- /dev-yolo exists: [YES/NO] - This is SEPARATE from /yolo
- /review has 7-phase reference: [YES/NO]
- /security-review exists: [YES/NO]
- /design-review exists: [YES/NO]
- /create-story has correct docs/development/features/.../epics/.../stories/ path: [YES/NO]

IF MISSING ANY CORE COMMAND:
ABORT_VALIDATION: true
REPORT_TO_COORDINATOR: "These commands are MISSING and MUST be created: [list]"
```

**CRITICAL**: If this checklist shows ANY command is missing, **STOP and report immediately**. Do not continue validation.
```

#### 1.4 Add Feature Structure Validator (NEW)

Add new section after Command Validator:

```markdown
**Agent 4: Feature Structure Validator - MECHANICAL CHECKLIST** (NEW)

```markdown
Task: Validate feature folder structure and story locations

**STEP 1: Check for Old/Wrong Story Locations**

```
Check these old/wrong locations and report if stories exist:
- [ ] docs/stories/*.md files exist? [YES/NO] - If YES, these need MIGRATION
- [ ] features/*/stories/*.md files exist? [YES/NO] - If YES, these need MIGRATION
- [ ] docs/development/features/*/stories/*.md files exist? [YES/NO] - If YES, these are in WRONG location

STEP 2: Check for Correct Story Location

For each feature, verify stories are at:
docs/development/features/[feature-name]/epics/[epic-name]/stories/X.Y.md

- [ ] Correct structure exists: [YES/NO]
- [ ] If NO, migration needed

STEP 3: Deliverable

FEATURE STRUCTURE VALIDATION RESULT:
STORIES_AT_OLD_LOCATION: [YES/NO] - Location(s): [list]
STORIES_AT_CORRECT_LOCATION: [YES/NO]
MIGRATION_NEEDED: [YES/NO]
ACTION_REQUIRED: [YES if migration needed, NO otherwise]

IF MIGRATION NEEDED:
ABORT_VALIDATION: true
REPORT_TO_COORDINATOR: "Story migration required: Move stories from [old-location] to docs/development/features/[feature]/epics/[epic]/stories/"
```

---

### Fix Group 2: Phase Files Enhancement

**Target Files**:
- `prompts/phases/phase-4-commands.md` (lines 17-32)
- `prompts/phases/phase-3-agents.md` (beginning)

**Changes Required**:

#### 2.1 Phase 3 Enhancement - Exact Agent List

Add to beginning of phase-3-agents.md, before "Batch Execution":

```markdown
## ⚠️ CRITICAL: Exact Agent Names Required

**You MUST create these EXACT 13 core agents (no more, no less)**:

1. coordinator
2. senior-developer
3. test-writer
4. code-reviewer
5. bug-finder
6. refactor-specialist
7. qa-tester
8. git-helper
9. architecture-advisor
10. performance-optimizer
11. documentation-writer
12. agent-creator
13. skill-creator

**Plus optional agents**:
- security-reviewer (Phase 2)
- design-reviewer (Phase 3)

After creating all agents, verify by running:
```bash
ls -la .claude/agents/ | wc -l
# Expected: 13+ for core, 15+ if including optional
```

If fewer agents exist, you MUST create the missing ones from `prompts/reference/core-agents.md` before proceeding.
```

#### 2.2 Phase 4 Enhancement - Exact Command List

Add to beginning of phase-4-commands.md, before "Batch Execution":

```markdown
## ⚠️ CRITICAL: Exact Command Names Required

**You MUST create these EXACT 12 core commands (no more, no less)**:

### Core Commands (REQUIRED - 12 total)
1. /dev - Continue development with automatic task tracking
2. /dev-yolo - **SEPARATE** autonomous YOLO loop (NOT just /yolo)
3. /commit - Smart commit
4. /review - 7-phase code review
5. /status - Project status
6. /test - Run tests
7. /plan - Plan feature
8. /docs - Update docs
9. /yolo - **Configure** YOLO mode (NOT the same as /dev-yolo)
10. /create-feature - Create new feature
11. /correct-course - Adjust feature direction
12. /create-story - Create user story

### Optional Commands (RECOMMENDED - 2+ total)
13. /security-review - OWASP security scanning (Opus model)
14. /design-review - UI/UX design review (Playwright, WCAG AA)

**CRITICAL DISTINCTION**:
- `/yolo` = Configuration tool (edit breakpoints in status.xml)
- `/dev-yolo` = Execution tool (run coordinator in autonomous mode)
- These are TWO DIFFERENT commands

After creating all commands, verify by running:
```bash
ls -la .claude/commands/ | wc -l
# Expected: 12+ for core, 14+ if including optional
```

If fewer commands exist, you MUST create the missing ones before proceeding.
```

---

### Fix Group 3: Story Migration Instructions

**Target File**: New file `docs/STORY-MIGRATION-GUIDE.md`

**Content**:

```markdown
# Story Migration Guide

**Purpose**: Migrate stories from old/wrong locations to correct location per meta prompt spec

---

## Current Problem

Stories are currently in wrong locations:
- ❌ `docs/stories/1.1.md`, `docs/stories/1.2.md`, etc.
- ❌ `features/[feature]/stories/` (also wrong)

Correct location per meta prompt:
- ✅ `docs/development/features/[feature-name]/epics/[epic-name]/stories/X.Y.md`

---

## Migration Steps

### Step 1: Identify Old Story Locations

```bash
# Find stories in old locations
find docs -name "*.md" -path "*/stories/*" -not -path "*/development/*"
find features -name "*.md" -path "*/stories/*"

# Typical output:
# docs/stories/1.1.md
# docs/stories/1.2.md
# docs/stories/1.3.md
# etc.
```

### Step 2: Identify Correct Target Locations

For each story `X.Y.md`:
- X = epic number
- Y = story number within that epic

Example:
- Story `1.1.md` → Epic 1, Story 1 → Target: `docs/development/features/[feature]/epics/epic-1-[name]/stories/1.1.md`
- Story `2.3.md` → Epic 2, Story 3 → Target: `docs/development/features/[feature]/epics/epic-2-[name]/stories/2.3.md`

### Step 3: Create Target Directories

```bash
# For each feature and epic, create the stories folder structure
mkdir -p docs/development/features/[feature-name]/epics/epic-1-[name]/stories
mkdir -p docs/development/features/[feature-name]/epics/epic-2-[name]/stories
# etc.
```

### Step 4: Move Story Files

```bash
# Move each story to correct location
mv docs/stories/1.1.md docs/development/features/[feature-name]/epics/epic-1-[name]/stories/1.1.md
mv docs/stories/1.2.md docs/development/features/[feature-name]/epics/epic-1-[name]/stories/1.2.md
# etc.
```

### Step 5: Update status.xml References

Edit `docs/development/status.xml`:
- Update any story path references to use new location
- Verify `<current-story>` points to correct path

### Step 6: Verify Migration

```bash
# Verify no stories remain at old location
ls -la docs/stories/ # Should be empty or non-existent
ls -la features/*/stories/ # Should have no story files

# Verify stories are at correct location
ls -la docs/development/features/[feature]/epics/epic-*/stories/
# Should show all X.Y.md files
```

---

## Rollback (if needed)

If migration fails, copy stories back to old location:

```bash
cp docs/development/features/[feature-name]/epics/epic-*/stories/*.md docs/stories/
```

---

## Automation Script (Optional)

For large migrations, use this bash script:

```bash
#!/bin/bash

# Move all stories from docs/stories/ to correct locations
for story in docs/stories/*.md; do
  filename=$(basename "$story")
  # Extract epic number from filename (X.Y.md -> X)
  epic_num=$(echo "$filename" | cut -d'.' -f1)

  # Target: docs/development/features/[feature]/epics/epic-{epic_num}/stories/
  target="docs/development/features/[FEATURE-NAME]/epics/epic-${epic_num}/stories/${filename}"

  # Create target directory if needed
  mkdir -p "$(dirname "$target")"

  # Move file
  mv "$story" "$target"
  echo "Moved: $filename -> $target"
done

echo "Migration complete!"
```

---
```

---

## Part 4: Implementation Checklist

### Phase A: Create Plan Documents (THIS STEP)

- [x] Create UPDATE-WORKFLOW-FIX-PLAN.md (this file)
- [ ] Update prompts/update-mode/validation-workflow.md
- [ ] Create docs/STORY-MIGRATION-GUIDE.md
- [ ] Create docs/MECHANICAL-VALIDATION-SPEC.md

### Phase B: Update Prompt Files (PARALLEL AGENTS)

**Agent 1: Validation Workflow Updater**
- [ ] Update prompts/update-mode/validation-workflow.md with mechanical validation
- [ ] Add "Authoritative Sources" section
- [ ] Replace Agent 2 validator with mechanical checklist
- [ ] Replace Agent 3 validator with mechanical checklist
- [ ] Add new Agent 4 Feature Structure Validator
- [ ] Add Phase 3.5 "Hard Verification Checkpoints"

**Agent 2: Phase File Updater**
- [ ] Update prompts/phases/phase-3-agents.md with exact agent list
- [ ] Update prompts/phases/phase-4-commands.md with exact command list
- [ ] Add "CRITICAL DISTINCTION" sections for /yolo vs /dev-yolo
- [ ] Add /dev-yolo command specification to phase-4-commands.md

**Agent 3: Documentation Creator**
- [ ] Create docs/STORY-MIGRATION-GUIDE.md (copy from Part 3 above)
- [ ] Create docs/MECHANICAL-VALIDATION-SPEC.md
- [ ] Update README for update workflow improvements

### Phase C: Verify Prompt Updates (SEQUENTIAL)

- [ ] Read updated validation-workflow.md and verify changes
- [ ] Read updated phase-3-agents.md and verify changes
- [ ] Read updated phase-4-commands.md and verify changes
- [ ] Verify no syntax errors or broken references

### Phase D: Create Story Migration Automation (AGENT)

**Agent 4: Migration Automation Creator**
- [ ] Create migration script in scripts/migrate-stories.sh
- [ ] Add error handling and verification
- [ ] Add rollback capability
- [ ] Test script (dry-run first)

### Phase E: Final Verification (SEQUENTIAL)

- [ ] Verify all prompt files updated correctly
- [ ] Verify all documentation created
- [ ] Verify migration automation works
- [ ] Test mechanical validation logic with example project

---

## Part 5: Detailed Task Breakdown for Sub-Agents

### Agent Task 1: Validation Workflow Updater

**Mission**: Update `prompts/update-mode/validation-workflow.md` with mechanical validation checklists

**Exact Changes**:

1. After line 85 (before Agent 1), add "Authoritative Sources (READ THESE FIRST)" section
2. Replace entire "Agent 2: Agent Structure Validator" section with new mechanical version
3. Replace entire "Agent 3: Command Structure Validator" section with new mechanical version
4. Add new "Agent 4: Feature Structure Validator - MECHANICAL CHECKLIST" section
5. Add new "Phase 3.5: Hard Verification Checkpoints (BLOCKING)" section after Phase 3

**Reference**: See Part 3 of this plan for exact text

---

### Agent Task 2: Phase File Updater

**Mission**: Update phase files with exact lists and critical distinctions

**Exact Changes**:

1. In `prompts/phases/phase-3-agents.md`, add before "Batch Execution" section:
   - "CRITICAL: Exact Agent Names Required" with numbered list of 13 agents
   - Verification command (ls -la)

2. In `prompts/phases/phase-4-commands.md`, add before "Batch Execution" section:
   - "CRITICAL: Exact Command Names Required" with numbered list of 12 commands
   - "CRITICAL DISTINCTION" section explaining /yolo vs /dev-yolo
   - Add full `/dev-yolo` command specification if missing

3. Verify /dev-yolo is documented as separate command from /yolo

**Reference**: See Part 3, Fix Group 2

---

### Agent Task 3: Documentation Creator

**Mission**: Create documentation files for migration and mechanical validation

**Files to Create**:

1. `docs/STORY-MIGRATION-GUIDE.md` - Complete story migration process (see Part 3)
2. `docs/MECHANICAL-VALIDATION-SPEC.md` - Specifications for mechanical validation

**Content for MECHANICAL-VALIDATION-SPEC.md**:

```markdown
# Mechanical Validation Specification

## Purpose

Validators must return structured, actionable data that updaters can execute mechanically.

## Validation Report Format

Instead of narrative reports, use this exact format:

### Agent Validation Report

```
AGENT_VALIDATION:
  TOTAL_REQUIRED: 13
  TOTAL_FOUND: X
  EXISTS: [agent-1, agent-2, ...]
  MISSING: [agent-1, agent-2, ...]
  NEEDS_UPDATE: [agent-1 (reason), agent-2 (reason), ...]
  ABORT_IF_MISSING: true
  NEXT_STEP: "Create missing agents from core-agents.md"
```

### Command Validation Report

```
COMMAND_VALIDATION:
  TOTAL_REQUIRED: 12
  TOTAL_FOUND: X
  EXISTS: [/command-1, /command-2, ...]
  MISSING: [/command-1, /command-2, ...]
  CRITICAL_CHECKS:
    dev_yolo_separate_from_yolo: [YES/NO]
    review_has_7_phase: [YES/NO]
    security_review_exists: [YES/NO]
    design_review_exists: [YES/NO]
  ABORT_IF_MISSING: true
  NEXT_STEP: "Create missing commands"
```

### Feature Structure Validation Report

```
FEATURE_STRUCTURE_VALIDATION:
  OLD_LOCATION_docs_stories: [YES/NO]
  OLD_LOCATION_features_stories: [YES/NO]
  CORRECT_LOCATION: [YES/NO]
  MIGRATION_NEEDED: [YES/NO]
  NEXT_STEP: "Run story migration script"
```

## Validator Requirements

Each validator MUST:
1. Read authoritative source (core-agents.md, phase-4-commands.md, etc.)
2. Create mechanical checklist (NOT narrative)
3. Return structured data (NOT prose report)
4. Return ABORT_IF_MISSING: true if ANY required item is missing
5. Stop validation immediately if critical issue found

## Updater Requirements

Each updater MUST:
1. Check validation report for ABORT_IF_MISSING
2. If true, STOP and report missing items to coordinator
3. If false, proceed with updates using "CREATE/UPDATE" instructions
4. Verify count matches expected count
5. Return verification report with same format
```

---

### Agent Task 4: Migration Automation Creator

**Mission**: Create shell script to automate story migration

**File**: `scripts/migrate-stories.sh`

**Features**:
- Find stories at old locations
- Verify target directories exist
- Move stories with verification
- Update status.xml references
- Provide rollback capability
- Dry-run mode first

**Key Functions**:
```bash
# Dry run first
./scripts/migrate-stories.sh --dry-run

# Actual migration
./scripts/migrate-stories.sh --feature [feature-name]

# Rollback
./scripts/migrate-stories.sh --rollback
```

---

## Part 6: Success Criteria

When all fixes are complete:

### Validation Workflow
- [ ] Validators use mechanical checklists, not narrative
- [ ] Validators read authoritative sources (core-agents.md, phase-4-commands.md)
- [ ] Validators return structured data with ABORT_IF_MISSING flags
- [ ] Validators stop immediately if any required agent/command is missing

### Phase Files
- [ ] Phase 3 explicitly lists all 13 agent names
- [ ] Phase 4 explicitly lists all 12 command names
- [ ] Phase 4 clearly distinguishes /yolo from /dev-yolo
- [ ] Both phases include verification commands (ls -la)

### Story Migration
- [ ] Migration guide created and documented
- [ ] Migration script created and tested
- [ ] Stories moved from old locations to correct locations
- [ ] status.xml updated with new paths
- [ ] Verification confirms all stories at correct locations

### Documentation
- [ ] All plan documents in docs/ folder
- [ ] Mechanical validation specification documented
- [ ] Story migration guide complete
- [ ] Clear hand-off instructions for future updates

---

## Next Steps

1. ✅ Create this plan (DONE)
2. 👉 Spawn 4 parallel sub-agents to execute fixes
3. Monitor progress
4. Verify all changes
5. Test update workflow with mechanical validation
6. Report completion

---

