# Mechanical Validation Specification

**Purpose**: Define how validators should return structured, actionable data instead of narrative reports

**Applies to**: All validation agents in update workflow

---

## Core Principles

1. **Mechanical Over Narrative**: Return structured data, not prose
2. **Actionable**: Updaters must be able to execute validation results without interpretation
3. **Explicit Stops**: ABORT flags must force coordination, not continue optimistically
4. **Authoritative Sources**: Validators read exact specifications (core-agents.md, phase-4-commands.md, etc.)
5. **Checkpoints**: Each validation tier has hard stops if critical items missing

---

## Validation Report Formats

### Format 1: Agent Validation Report

```yaml
VALIDATION_TYPE: "Agent Structure"
TIMESTAMP: "YYYY-MM-DD HH:MM:SS"

AGENT_VALIDATION:
  TOTAL_REQUIRED: 13
  TOTAL_FOUND: 11
  MISSING_COUNT: 2

  EXISTS:
    - coordinator
    - senior-developer
    - test-writer
    - code-reviewer
    - bug-finder
    - refactor-specialist
    - qa-tester
    - git-helper
    - architecture-advisor
    - performance-optimizer
    - documentation-writer

  MISSING:
    - agent-creator
    - skill-creator

  NEEDS_UPDATE:
    - code-reviewer: "Missing 7-phase framework section"

  YAML_VALIDATION:
    PASS: 11
    FAIL: 0

  ABORT_VALIDATION: true
  REASON_FOR_ABORT: "2 critical agents missing (agent-creator, skill-creator)"

  NEXT_STEP: "Create missing agents from prompts/reference/core-agents.md before continuing"

  DETAILED_ACTIONS:
    CREATE:
      - "agent-creator"
      - "skill-creator"
    UPDATE:
      - "code-reviewer: Add 7-phase framework"
```

### Format 2: Command Validation Report

```yaml
VALIDATION_TYPE: "Command Structure"
TIMESTAMP: "YYYY-MM-DD HH:MM:SS"

COMMAND_VALIDATION:
  TOTAL_REQUIRED: 12
  TOTAL_FOUND: 10
  MISSING_COUNT: 2

  EXISTS:
    - "/dev"
    - "/commit"
    - "/review"
    - "/status"
    - "/test"
    - "/plan"
    - "/docs"
    - "/yolo"
    - "/create-feature"
    - "/correct-course"

  MISSING:
    - "/dev-yolo"
    - "/create-story"

  CRITICAL_CHECKS:
    dev_yolo_exists: false
    dev_yolo_separate_from_yolo: "CANNOT VERIFY - /dev-yolo missing"
    review_has_7_phase_framework: true
    security_review_exists: false
    design_review_exists: false

  ABORT_VALIDATION: true
  REASON_FOR_ABORT: "2 core commands missing, including CRITICAL /dev-yolo"

  NEXT_STEP: "Create missing commands (/dev-yolo, /create-story) from prompts/phases/phase-4-commands.md"

  DETAILED_ACTIONS:
    CREATE:
      - "/dev-yolo: Autonomous YOLO loop spawning coordinator"
      - "/create-story: Create user story in correct location"
    OPTIONAL_CREATE:
      - "/security-review: OWASP scanning (Opus model)"
      - "/design-review: UI/UX review (Playwright, WCAG AA)"
```

### Format 3: Feature Structure Validation Report

```yaml
VALIDATION_TYPE: "Feature Structure"
TIMESTAMP: "YYYY-MM-DD HH:MM:SS"

FEATURE_STRUCTURE_VALIDATION:
  OLD_LOCATION_check:
    docs_stories_exists: true
    docs_stories_files: ["1.1.md", "1.2.md", "1.3.md", "2.1.md"]
    features_stories_exists: false

  CORRECT_LOCATION_check:
    docs_development_features_epics_stories_exists: false

  STATUS:
    stories_at_wrong_location: true
    stories_at_correct_location: false
    migration_needed: true

  ABORT_VALIDATION: true
  REASON_FOR_ABORT: "Story files at old location (docs/stories/), must migrate to docs/development/features/[feature]/epics/[epic]/stories/"

  MIGRATION_REQUIRED:
    source: "docs/stories/"
    destination: "docs/development/features/[feature-name]/epics/[epic-name]/stories/"
    files_to_migrate: 4
    example_moves:
      - "docs/stories/1.1.md → docs/development/features/[feature]/epics/epic-1/stories/1.1.md"
      - "docs/stories/1.2.md → docs/development/features/[feature]/epics/epic-1/stories/1.2.md"

  NEXT_STEP: "Run story migration using scripts/migrate-stories.sh or docs/STORY-MIGRATION-GUIDE.md"
```

### Format 4: Documentation Validation Report

```yaml
VALIDATION_TYPE: "Documentation Structure"
TIMESTAMP: "YYYY-MM-DD HH:MM:SS"

DOCUMENTATION_VALIDATION:
  TOTAL_REQUIRED: 12
  TOTAL_FOUND: 10
  MISSING_COUNT: 2

  EXISTS:
    - INDEX.md
    - PRD.md
    - TECHNICAL_SPEC.md
    - ARCHITECTURE.md
    - DEVELOPMENT_PLAN.md
    - CODE_REVIEW_PRINCIPLES.md
    - SECURITY_REVIEW_CHECKLIST.md
    - DESIGN_PRINCIPLES.md
    - START_HERE.md
    - TASKS.md

  MISSING:
    - DESIGN_SYSTEM.md
    - PROJECT_SUMMARY.md

  CONTENT_VALIDATION:
    CODE_REVIEW_PRINCIPLES:
      has_7_phase_framework: true
      has_triage_matrix: true
      has_net_positive_philosophy: true
    SECURITY_REVIEW_CHECKLIST:
      has_owasp_top_10: true
      has_false_positive_rules: true
      has_confidence_scoring: true

  ABORT_VALIDATION: false
  STATUS: "Can proceed with updates (missing docs non-critical)"

  NEXT_STEP: "Create missing documentation files: DESIGN_SYSTEM.md, PROJECT_SUMMARY.md"
```

---

## Validator Requirements (Must Follow)

Every validator MUST:

1. **Read Authoritative Source First**
   ```
   Example for Agent Validator:
   - Read: prompts/reference/core-agents.md
   - Extract: [coordinator, senior-developer, test-writer, ..., skill-creator]
   - Use this list for validation (NOT from any other source)
   ```

2. **Create Mechanical Checklist**
   ```
   ✓ Agent 1: coordinator - EXISTS [Yes/No] - Valid YAML [Yes/No]
   ✓ Agent 2: senior-developer - EXISTS [Yes/No] - Valid YAML [Yes/No]
   ... (one line per required item)
   ✓ Agent 13: skill-creator - EXISTS [Yes/No] - Valid YAML [Yes/No]
   ```

3. **Return Structured Data (YAML/JSON format)**
   ```
   NOT ACCEPTABLE: "The validation found that code-reviewer is present but needs updates..."
   ACCEPTABLE: "code-reviewer: needs_update, reason: missing 7-phase framework"
   ```

4. **Set ABORT_VALIDATION Flag Correctly**
   ```
   ABORT_VALIDATION: true
   - If ANY required item is MISSING
   - If ANY critical content is MISSING (e.g., 7-phase framework in code-reviewer)

   ABORT_VALIDATION: false
   - Only if ALL required items exist and are correct
   - Optional items missing is OK (e.g., design-reviewer)
   ```

5. **Provide Clear NEXT_STEP**
   ```
   NEXT_STEP: "Create missing agents: agent-creator, skill-creator from prompts/reference/core-agents.md"
   (Not just "Create missing agents" - be specific about WHICH items and WHERE to find spec)
   ```

6. **Stop Immediately on Critical Issue**
   ```
   If ABORT_VALIDATION: true, the validator report is the last step.
   Do not continue analyzing other aspects.
   Return report immediately and let coordinator handle abort.
   ```

---

## Updater Requirements (Based on Validation Reports)

Every updater MUST:

1. **Check ABORT_VALIDATION Flag First**
   ```
   if validation.ABORT_VALIDATION == true:
     STOP immediately
     Report: "Cannot proceed - missing critical items: [list]"
     Wait for coordinator to resolve before continuing
   ```

2. **Count Expected Items**
   ```
   Example for agents:
   validation.TOTAL_REQUIRED: 13
   validation.TOTAL_FOUND: 11

   Action: Create 13 - 11 = 2 missing agents
   ```

3. **Execute Detailed Actions**
   ```
   For each item in validation.DETAILED_ACTIONS.CREATE:
     - Read source specification
     - Create file
     - Verify creation

   For each item in validation.DETAILED_ACTIONS.UPDATE:
     - Read existing file
     - Add missing content
     - Verify update
   ```

4. **Verify After Updates**
   ```
   After creating/updating all items:
     - Count again: ls -la .claude/agents/ | wc -l
     - Should equal: validation.TOTAL_REQUIRED
     - If not, create remaining missing items
   ```

5. **Return Updated Validation Report**
   ```
   After updates, return same validation format but with updated numbers:

   BEFORE: TOTAL_FOUND: 11, MISSING: 2
   AFTER:  TOTAL_FOUND: 13, MISSING: 0
   ABORT_VALIDATION: false
   ```

---

## Phase 3.5: Hard Verification Checkpoints

**After all update agents complete, execute these non-negotiable checks**:

### Checkpoint 1: Agent Count
```bash
ls -la .claude/agents/ | wc -l
# Expected: 13+ (13 core + optional security-reviewer, design-reviewer)
# If FEWER: ABORT and report which agents are still missing
```

### Checkpoint 2: Command Count
```bash
ls -la .claude/commands/ | wc -l
# Expected: 12+ (12 core + optional security-review, design-review)
# If FEWER: ABORT and report which commands are still missing
```

### Checkpoint 3: Critical Agents Exist
```bash
# MUST exist (fail if missing):
test -f .claude/agents/coordinator.md || ABORT "coordinator missing"
test -f .claude/agents/code-reviewer.md || ABORT "code-reviewer missing"
test -f .claude/agents/security-reviewer.md || ABORT "security-reviewer missing"
test -f .claude/agents/design-reviewer.md || ABORT "design-reviewer missing"
```

### Checkpoint 4: Critical Commands Exist
```bash
# MUST exist (fail if missing):
test -f .claude/commands/dev.md || ABORT "/dev command missing"
test -f .claude/commands/dev-yolo.md || ABORT "/dev-yolo command missing"
test -f .claude/commands/review.md || ABORT "/review command missing"
test -f .claude/commands/security-review.md || ABORT "/security-review command missing"
test -f .claude/commands/design-review.md || ABORT "/design-review command missing"
```

### Checkpoint 5: Story Structure
```bash
# OLD locations should be empty/non-existent:
ls docs/stories/*.md 2>/dev/null && ABORT "Stories still at docs/stories/ - migration incomplete"

# CORRECT location should have stories:
ls docs/development/features/*/epics/*/stories/*.md 2>/dev/null || ABORT "No stories found at correct location"
```

**If ANY checkpoint fails, stop and report the failure before proceeding to Phase 4 (Verification).**

---

## Summary

- Validators: Return structured data with ABORT flags
- Updaters: Check ABORT flags before proceeding, execute mechanical actions
- Checkpoints: Hard stops if critical items missing
- Verification: Same format as validation, proving all items exist

This ensures Claude Code cannot skip critical updates.

