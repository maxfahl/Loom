# Phase 4: Command Creation

**Part of**: [Project Setup Meta Prompt](../project-setup-meta-prompt.md)

## Purpose

Create 11+ custom slash commands including /dev, /commit, /review, /status, /test, /plan, /docs, /yolo, /create-feature, /correct-course, /create-agent, /create-skill. Includes command templates and creation workflow.

## ⚡ CRITICAL: Parallel Creation (80% Time Savings)

**Total Time: ~6 minutes (vs ~35 minutes sequential)**

**ALWAYS create commands in parallel batches** - see [parallelization-patterns.md](../reference/parallelization-patterns.md)

### Batch Execution (3 batches)

**Batch 1** (4 commands in parallel):
- /dev
- /commit
- /review
- /status

**Batch 2** (4 commands in parallel):
- /test
- /plan
- /docs
- /yolo

**Batch 3** (3 commands in parallel):
- /create-feature
- /correct-course
- /create-story

### What NOT to Do

❌ **WRONG** - Sequential:
```
Create /dev → wait → Create /commit → wait → Create /review → wait...
```

✅ **CORRECT** - Parallel batches:
```
Create 4 commands in parallel (Batch 1) → wait → Create 4 commands in parallel (Batch 2) → wait → Create 3 commands in parallel (Batch 3)
```

## Related Files

- [../templates/command-template.md](../templates/command-template.md) - Generic command structure
- [../reference/core-agents.md](../reference/core-agents.md) - Agents used by commands
- [phase-5-claude-md.md](phase-5-claude-md.md) - Commands documented in CLAUDE.md

## Usage

Read this file:
- In Phase 4 after agents are created
- To understand all 11+ core commands
- For command creation workflow and templates
- To see which commands use which agents

---

## 🎯 Custom Slash Commands to Create

### Core Commands (Always Include)

**1. /dev** - Continue Development

```yaml
---
description: Continue development on current task with automatic task tracking
allowed-tools: Bash(npm:*), Bash(git:*), Read, Write, Edit, Glob, Grep
model: claude-sonnet-4-5
---
```

**Purpose**: Resume coding with context of current task, following project conventions, with automatic task tracking and status updates

**Phase 0 Enhancement: Automatic Task Tracking**

**Process**:

1. **Read Current Context**:
   - Read `status.xml` for active feature
   - Read `<current-story>` value (e.g., "1.2")
   - Read story file at `docs/development/features/[feature]/epics/[epic]/stories/[current-story].md`

2. **Check for Review Tasks** (PRIORITY):
   - Look for "## Review Tasks" section in story file
   - If exists and has uncompleted tasks (`[ ]`):
     - **Prioritize Review Tasks FIRST**
     - Work on highest priority tasks (Fix > Improvement > Nit)
     - Check off tasks as completed (`[ ]` → `[x]`)
   - If all Review Tasks complete, proceed to regular tasks

3. **Work on Regular Tasks**:
   - Read "## Tasks and Subtasks" section
   - Continue from last uncompleted task
   - Check off subtasks as completed (`[ ]` → `[x]`)
   - Update story file with progress

4. **Update Story Status When Complete**:
   - If ALL tasks and subtasks are checked (`[x]`):
     - Update story **Status** to "Waiting For Review"
     - Update **Last Updated** timestamp
     - Add note to status.xml about completion
   - If tasks still pending:
     - Keep status as "In Progress"
     - Update **Last Updated** timestamp

5. **Follow Project Conventions**:
   - Read acceptance criteria from story file
   - Follow TDD methodology (see below)
   - Reference technical details and dependencies
   - Maintain test coverage requirements

**TDD Variations**:

- **Fully Enforced**: "Follow TDD Red-Green-Refactor strictly. Write failing test FIRST, then implement."
- **Recommended**: "Follow TDD Red-Green-Refactor when possible. Consider writing tests first."
- **No TDD**: "Continue implementation. Add tests for critical functionality."

**1.5. /dev-yolo** - Autonomous YOLO Loop (Full Feature Completion)

```yaml
---
description: Launch coordinator agent in autonomous YOLO mode to complete stories/epics
allowed-tools: Task
model: claude-sonnet-4-5
---
```

**Purpose**: Start the autonomous development loop where the coordinator agent completes entire stories, epics, or features following YOLO mode configuration

**CRITICAL: This command spawns the coordinator agent for autonomous execution**

**Process**:

1. **Read YOLO Configuration**:
   - Read `docs/development/status.xml`
   - Find active feature with `<is-active-feature>true</is-active-feature>`
   - Check `<yolo-mode enabled="true|false">`
   - Check `<stopping-granularity>` (story/epic/custom)
   - Read all breakpoint settings (1-9)

2. **Validate Prerequisites**:
   - Ensure active feature exists
   - Ensure current epic is set
   - Ensure current story exists
   - Confirm YOLO mode is properly configured
   - If any missing: ABORT and ask user to configure

3. **Spawn Coordinator Agent**:

   ```markdown
   Task: Autonomous development loop following YOLO mode configuration

   Context:
   - Active Feature: [feature-name]
   - Current Epic: [epic-id]
   - Current Story: [story-id]
   - YOLO Mode: [enabled/disabled]
   - Stopping Granularity: [story/epic/custom]
   - Breakpoints: [list enabled breakpoints]

   Instructions:

   You are the coordinator agent executing the autonomous development workflow.
   Follow the complete coordinator workflow documented in:
   - prompts/reference/coordinator-workflow.md
   - prompts/reference/core-agents.md (coordinator section)

   **Your Mission**:
   1. Read current story file for tasks and acceptance criteria
   2. Execute TDD cycle: Red → Green → Refactor
   3. Check off tasks as completed in story file
   4. Run tests and ensure 80%+ coverage
   5. Spawn code-reviewer for review
   6. Handle Review Tasks if issues found
   7. Update story status to "Waiting For Review" when done
   8. Check YOLO breakpoints - stop or continue based on configuration
   9. If story complete and YOLO allows, move to next story
   10. If epic complete and breakpoint 9 enabled, STOP for user review
   11. If epic complete and breakpoint 9 disabled, move to next epic
   12. Loop until: breakpoint triggered, epic boundary (if enabled), or feature complete

   **CRITICAL - Stopping Conditions**:

   - **STORY-LEVEL** (`<stopping-granularity>story</stopping-granularity>`):
     - Stop at enabled breakpoints within each story
     - Check breakpoints 1-8 during story execution

   - **EPIC-LEVEL** (`<stopping-granularity>epic</stopping-granularity>`):
     - Ignore breakpoints 1-8 within stories
     - Only stop at breakpoint 9 (after completing epic)
     - Autonomously complete ALL stories in current epic

   - **CUSTOM**:
     - Check all enabled breakpoints 1-9 as configured

   **Abort Conditions** (Stop immediately and report to user):
   - Cannot find story file
   - Tests fail after 3 attempts
   - Coverage drops below required threshold
   - Circular dependency detected
   - Required file missing
   - Critical blocker in status.xml
   - Manual intervention required (user-specific note in story)

   **Success Report Format**:

   When stopping (either at breakpoint or completion):

   ```
   🎯 YOLO Loop Status Report

   **Feature**: [feature-name]
   **Stopped At**: [Breakpoint X / Epic Complete / Feature Complete]

   **Completed**:
   - ✅ Story 1.1: [title] (commit: abc123)
   - ✅ Story 1.2: [title] (commit: def456)
   - ✅ Story 2.1: [title] (commit: ghi789)

   **Current State**:
   - Epic: [epic-id]
   - Story: [story-id]
   - Status: [In Progress / Waiting For Review / Done]
   - Tests: [X/Y passing, Z% coverage]

   **Next Steps**:
   - [What user should do next or what will happen when resumed]
   ```

   **Remember**:
   - Follow TDD strictly (tests BEFORE implementation)
   - Update story files as you complete tasks
   - Update status.xml with commit hashes
   - Respect breakpoint configuration
   - Report clear status when stopping
   ```

4. **Monitor Progress**:
   - Coordinator agent runs autonomously
   - Stops at configured breakpoints
   - Returns status report when complete or stopped

5. **Resume After Stop**:
   - If stopped at breakpoint: Run `/dev-yolo` again to continue
   - If user wants to change YOLO config: Run `/yolo` first, then `/dev-yolo`

**Examples**:

```bash
# Start YOLO loop for current feature
/dev-yolo

# Output:
# 🚀 Launching coordinator agent in YOLO mode...
# Feature: user-authentication
# YOLO Mode: ON
# Stopping Granularity: EPIC-LEVEL
# Breakpoints: 9 only
#
# Coordinator will autonomously complete all stories in current epic.
# Will stop after Epic 1 completes (breakpoint 9 enabled).
```

**When to Use**:
- Starting new feature development (let agents complete stories autonomously)
- Resuming after reviewing epic completion
- Running overnight development (high-trust YOLO mode)
- Rapid prototyping (YOLO mode with minimal breakpoints)

**When NOT to Use**:
- Manual single-story development (use `/dev` instead)
- Need to review each change before proceeding
- Testing YOLO configuration for first time (start with `/dev` first)
- Critical production changes (use manual review workflow)

**2. /commit [message]** - Smart Commit

```yaml
---
description: Smart commit with tests, linting, and conventional commits
allowed-tools: Bash(npm:*), Bash(git:*)
model: claude-sonnet-4-5
argument-hint: [commit message]
---
```

**Purpose**: Run all checks, review changes, create conventional commit

**3. /review** - Comprehensive Review

```yaml
---
description: Comprehensive review of uncommitted changes with automatic status updates
allowed-tools: Bash(git:*), Read, Write, Edit, Grep
model: claude-sonnet-4-5
---
```

**Purpose**: Full code review checklist before committing, with automatic Review Tasks creation and story status updates

**Phase 0 Enhancement: Automatic Status Management**

**Process**:

1. **Read Current Context**:
   - Read `status.xml` for active feature
   - Read `<current-story>` value
   - Read story file at `docs/development/features/[feature]/epics/[epic]/stories/[current-story].md`
   - Read acceptance criteria and requirements from story

2. **Embed Git Diff for Full Context** (Phase 1 Enhancement):

   Before reviewing, gather ALL changes upfront:

   ```bash
   # Git status
   git status

   # Files modified
   git diff --name-only origin/HEAD...

   # Commits
   git log --no-decorate origin/HEAD...

   # Full diff content
   git diff --merge-base origin/HEAD
   ```

   **Why**: Embedding full context upfront prevents repeated file reads and improves review quality.

3. **Review Code Using 7-Phase Framework** (Phase 1 Enhancement):

   Spawn `code-reviewer` agent with 7-phase hierarchical framework:

   1. **Architectural Design & Integrity** (Critical)
   2. **Functionality & Correctness** (Critical)
   3. **Security** (Non-Negotiable)
   4. **Maintainability & Readability** (High Priority)
   5. **Testing Strategy & Robustness** (High Priority)
   6. **Performance & Scalability** (Important)
   7. **Dependencies & Documentation** (Important)

   **Also check**:
   - Story acceptance criteria are met
   - All tasks are completed
   - TDD requirements followed (tests written first, 80%+ coverage)
   - Component library priority order (Kibo UI → Blocks.so → ReUI → shadcn/ui)

   **Reference**: CODE_REVIEW_PRINCIPLES.md for complete framework

4. **Apply Triage Matrix** (Phase 1 Enhancement):

   Categorize findings using triage matrix:
   - **Blocker**: Must fix before merge (security, architectural regression)
   - **Improvement**: Strong recommendation for better implementation
   - **Nit**: Minor polish, optional

   **Philosophy**: "Net Positive > Perfection" - Merge if it improves code health, even if not perfect

5. **Handle Review Findings**:

   **If Issues Found**:
   - Create/Update "## Review Tasks" section in story file
   - Add tasks with priority prefix:
     - `- [ ] Fix: [Blocking issue description] (file:line)`
     - `- [ ] Improvement: [High priority improvement] (file:line)`
     - `- [ ] Nit: [Low priority polish] (file:line)`
   - Update story **Status** to "In Progress" (back from "Waiting For Review")
   - Update **Last Updated** timestamp
   - Report issues to user with clear actionable feedback

   **If No Issues (Approved)**:
   - Update story **Status** to "Done"
   - Update **Last Updated** timestamp
   - Add completion note to status.xml
   - Congratulate user on completing the story

6. **Output Format** (Enhanced with Triage Matrix):
   ```markdown
   # Code Review Results

   **Story**: [X.Y - Story Title]
   **Status**: [Approved / Issues Found]
   **Framework**: 7-Phase Hierarchical Review

   ## Review Summary

   Reviewed using 7-phase framework:
   - ✅ Phase 1: Architectural Design & Integrity
   - ✅ Phase 2: Functionality & Correctness
   - ✅ Phase 3: Security
   - ⚠️ Phase 4: Maintainability & Readability (2 improvements suggested)
   - ✅ Phase 5: Testing Strategy & Robustness
   - ✅ Phase 6: Performance & Scalability
   - ✅ Phase 7: Dependencies & Documentation

   **Philosophy**: "Net Positive > Perfection" - This code improves the codebase and is ready to merge after addressing blockers.

   ## Issues Found (if any)

   ### Blocker (Must Fix Before Merge)
   - Issue 1: [Specific issue description] (`file:line`)
     - **Why**: [Underlying principle - security/architectural regression]
     - **Fix**: [Actionable suggestion]

   ### Improvement (Strong Recommendation)
   - Issue 2: [Specific issue description] (`file:line`)
     - **Why**: [Underlying principle - SOLID/DRY/KISS/YAGNI]
     - **Suggestion**: [Actionable improvement]

   ### Nit (Minor Polish, Optional)
   - Issue 3: [Specific issue description] (`file:line`)
     - **Note**: [Minor suggestion]

   ## Next Steps
   [What to do next - prioritize Blockers → Improvements → Nits]
   ```

**4. /project-status** - Project Status

```yaml
---
description: Show comprehensive project status
allowed-tools: Bash(git:*), Bash(npm:*), Read
model: claude-haiku-4-5
---
```

**Purpose**: Quick status report (git, tasks, tests, coverage)

**5. /test [pattern]** - Run Tests

```yaml
---
description: Run tests with coverage and detailed reporting
allowed-tools: Bash(npm:*)
model: claude-haiku-4-5
argument-hint: [test pattern]
---
```

**Purpose**: Execute tests and analyze results

**6. /plan [feature]** - Plan Feature

```yaml
---
description: Plan next feature or task with detailed breakdown
model: claude-sonnet-4-5
argument-hint: [feature name or task]
---
```

**Purpose**: Create detailed implementation plan with TDD breakdown

**7. /docs [type]** - Update Documentation

```yaml
---
description: Update documentation after changes
allowed-tools: Read, Write, Edit, Bash(git:*)
model: claude-haiku-4-5
argument-hint: [doc type: code|api|user|all]
---
```

**Purpose**: Update relevant docs based on code changes

**8. /yolo** - Configure YOLO Mode

```yaml
---
description: Configure YOLO mode breakpoints interactively
allowed-tools: Read, Write, Edit
model: claude-haiku-4-5
---
```

**Purpose**: Configure YOLO mode and breakpoints where agents should stop

**Process**:

1. Read current status.xml for active feature
2. Show current YOLO mode status and breakpoints
3. **Ask about stopping granularity** (NEW):

   ```
   Select your stopping granularity:

   A. STORY-LEVEL: Stop at specific breakpoints within each story (default)
   B. EPIC-LEVEL: Only stop when full epics are completed (autonomous per epic)
   C. CUSTOM: Select individual breakpoints manually

   Enter choice (A/B/C):
   ```

4. **If user selects B (EPIC-LEVEL)**:
   - Enable breakpoint 9 only
   - Disable all other breakpoints (1-8)
   - Set YOLO mode enabled="true"
   - Agents will autonomously complete entire epics before stopping

5. **If user selects A (STORY-LEVEL) or C (CUSTOM)**, present numbered list of common breakpoints:

   ```
   Select breakpoints where agents should STOP and ask for confirmation:

   1. After completing development, before code review
   2. After code review, before running tests
   3. After tests pass, before user testing
   4. After user testing, before committing
   5. After commit, before pushing to remote
   6. Before making any file changes (very cautious)
   7. Before running any tests (very cautious)
   8. Before major refactoring
   9. After completing epic, before starting next epic (EPIC-LEVEL only)

   Enter numbers separated by commas (e.g., "1, 3, 4, 8")
   Or enter "all" for maximum control (stop at all breakpoints)
   Or enter "none" for maximum speed (YOLO mode ON, skip all breakpoints)
   ```

6. Parse user response (e.g., "1, 3, 4, 8")
7. Update status.xml with selected breakpoints
8. Show confirmation:

   ```
   ✅ YOLO mode configured!

   Stopping Granularity: [STORY-LEVEL / EPIC-LEVEL / CUSTOM]
   Mode: [ON/OFF]

   Agents will STOP at these breakpoints:
   - Breakpoint 1: After completing development, before code review
   - Breakpoint 3: After tests pass, before user testing
   - Breakpoint 4: After user testing, before committing
   - Breakpoint 8: Before major refactoring

   Agents will SKIP these breakpoints:
   - Breakpoint 2: After code review, before running tests
   - Breakpoint 5: After commit, before pushing to remote
   - Breakpoint 6: Before making any file changes
   - Breakpoint 7: Before running any tests
   - Breakpoint 9: After completing epic, before starting next epic
   ```

**YOLO Mode Logic**:

- If user selects "none": Set `<yolo-mode enabled="true">`, all breakpoints disabled
- If user selects "all": Set `<yolo-mode enabled="false">`, all breakpoints 1-8 enabled
- If user selects EPIC-LEVEL (B): Set `<yolo-mode enabled="true">`, only breakpoint 9 enabled, set `<stopping-granularity>epic</stopping-granularity>`
- If user selects specific numbers: Configure individual breakpoints

**EPIC-LEVEL Mode Benefits**:

- Agents autonomously complete entire epics without interruption
- Only stops when switching between major epic milestones
- Ideal for high-trust autonomous development
- Agents handle all story-level decisions (dev → review → test → commit)
- User reviews work at logical epic boundaries

**Important**: This command edits `docs/development/status.xml` (SINGLE FILE for all features)

**9. /create-feature [name]** - Create New Feature

```yaml
---
description: Create a new feature with proper setup and documentation
model: claude-sonnet-4-5
argument-hint: [feature name]
---
```

**Purpose**: Set up complete feature structure with epics, documentation, and status tracking

**Process**:

1. Clarify feature details (name, description, priority, complexity)
2. Read meta prompt for setup requirements
3. Review existing project setup (agents/commands are shared)
4. **Divide feature into epics** (logical groupings of related tasks)
5. Create feature directory structure:
   ```
   docs/development/
   └── status.xml        # Feature tracking (SINGLE FILE for ALL features)
   └── features/[feature-name]/
       ├── INDEX.md
       ├── FEATURE_SPEC.md
       ├── TASKS.md
       ├── TECHNICAL_DESIGN.md
       ├── CHANGELOG.md
       └── epics/            # Epic folders with stories
           ├── epic-1-[name]/
           │   ├── DESCRIPTION.md  # Epic overview and goals
           │   ├── TASKS.md        # Epic-specific task list
           │   ├── NOTES.md        # Implementation notes
           │   └── stories/        # Stories for this epic
           │       ├── 1.1.md
           │       ├── 1.2.md
           │       └── 1.3.md
           ├── epic-2-[name]/
           │   ├── DESCRIPTION.md
           │   ├── TASKS.md
           │   ├── NOTES.md
           │   └── stories/
           │       ├── 2.1.md
           │       └── 2.2.md
           └── epic-3-[name]/
               ├── DESCRIPTION.md
               ├── TASKS.md
               ├── NOTES.md
               └── stories/
                   └── 3.1.md
   ```
6. Update status.xml in docs/development/ with new feature section (epics configuration and current-story tracking)
7. **CRITICAL**: Create feature documentation in docs/development/features/[feature-name]/ (FEATURE_SPEC, TASKS, TECHNICAL_DESIGN, etc.)
   - Create directory: `docs/development/features/[feature-name]/`
   - NOT in `features/[feature-name]/docs/`
   - This is separate from the features/ directory
8. **CRITICAL**: Create epic folders in `docs/development/features/[feature-name]/epics/[epic-name]/` with DESCRIPTION.md, TASKS.md, and NOTES.md for each epic
   - NOT in `features/[feature-name]/epics/`
   - ONLY in `docs/development/features/[feature-name]/epics/`
9. **CRITICAL**: Create stories folder inside each epic at `docs/development/features/[feature-name]/epics/[epic-name]/stories/`
   - NOT in `features/[feature-name]/stories/`
   - NOT in `docs/development/features/[feature-name]/stories/`
   - ONLY in `docs/development/features/[feature-name]/epics/[epic-name]/stories/`
10. Handle active feature switching (only ONE active at a time)
11. Populate pending-tasks from TASKS.md into appropriate epics
12. Show summary and next steps (mention using /create-story to create first story)

**Important**:

- Reads `prompts/project-setup-meta-prompt.md` for authoritative instructions
- **Divide all feature tasks into epics** (e.g., epic-1-foundation, epic-2-core, epic-3-polish)
- Each epic has its own folder in `docs/development/features/[feature-name]/epics/[epic-name]/`
- Each epic contains a stories/ subfolder for user stories
- Agents and commands are SHARED across features (don't recreate)
- Sets `<is-active-feature>true/false</is-active-feature>` appropriately
- Sets `<current-epic>` to track which epic is being worked on
- User chooses "now" (develop immediately) or "later" (setup only)

**10. /correct-course [feature]** - Correct Feature Direction

```yaml
---
description: Correct course on a feature based on new requirements or direction changes
model: claude-sonnet-4-5
argument-hint: [feature name or current]
---
```

**Purpose**: Adjust feature direction based on changing requirements, mistakes, or new insights

**Process**:

1. Identify feature (use "current" for active feature)
2. Read current feature state (status.xml + epic docs + feature docs + code + commits)
3. Show user current state summary (including epic breakdown)
4. Understand desired changes from user
5. Analyze impact (code to keep/modify/remove, tests to update, docs to revise, epics to reorganize)
6. **Update epic documentation** with changes (DESCRIPTION.md, TASKS.md in affected epics)
7. Update feature documentation with change log
8. Update status.xml with course correction notes and epic status changes
9. Create action plan (Cleanup → Modify → Add → Update Docs → Verify)
10. Execute corrections based on user's choice (automatic/step-by-step/manual)
11. Handle git history (revert commits if needed)
12. Verify corrections (tests, docs, status.xml)
13. **Update epic task lists** to reflect new direction
14. Update status.xml final state

**Important**:

- Reads `prompts/project-setup-meta-prompt.md` for guidance
- Reviews ALL existing work before making changes (including all epic folders)
- Documents WHY correction was needed in feature docs AND epic NOTES.md
- Updates status.xml to reflect new direction (including epic status)
- Handles cancelled tasks appropriately (mark epic as cancelled if needed)
- May reorganize epics if direction changes significantly
- Updates `<current-epic>` if switching to different epic
- May add `<cancelled-tasks>` section to status.xml

**11. /create-story** - Create Next Story

```yaml
---
description: Create the next user story for the current epic
model: claude-sonnet-4-5
---
```

**Purpose**: Analyze completed work, identify next story, and create comprehensive story file

**Process**:

1. Read status.xml to identify active feature and current epic
2. Read epic TASKS.md in `docs/development/features/[feature-name]/epics/[current-epic]/`
3. Check existing stories in `docs/development/features/[feature-name]/epics/[current-epic]/stories/` to see what's been created
4. Analyze what's been completed vs what's pending in the epic
5. Determine next story number (e.g., if current-story is 2.1, check if 2.1 exists, create 2.2)
6. **CRITICAL**: Create new story file at `docs/development/features/[feature-name]/epics/[current-epic]/stories/[epic.story].md`
   - NOT in `features/[feature-name]/`
   - NOT in `docs/development/features/[feature-name]/stories/`
   - ONLY in `docs/development/features/[feature-name]/epics/[current-epic]/stories/`
7. Update status.xml `<current-story>` to the new story number
8. Update `<last-updated>` timestamp

**Story File Location** (CRITICAL - DO NOT CHANGE):
- **Correct**: `docs/development/features/[feature-name]/epics/[epic-name]/stories/X.Y.md`
- **Wrong**: `features/[feature-name]/stories/X.Y.md`
- **Wrong**: `docs/development/features/[feature-name]/stories/X.Y.md`

**Story File Structure**:

```markdown
# Story [epic].[story]: [Title]

**Status**: In Progress
**Epic**: [epic-id]
**Created**: [YYYY-MM-DD]
**Last Updated**: [YYYY-MM-DD]

## Story Description

[Brief description of what this story achieves]

## Acceptance Criteria

- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

## Tasks and Subtasks

### Task 1: [Name]
- [ ] Subtask 1.1
- [ ] Subtask 1.2

### Task 2: [Name]
- [ ] Subtask 2.1
- [ ] Subtask 2.2

### Task 3: [Name]
- [ ] Subtask 3.1

### Task 4: 🔴🟢🔵 TDD Workflow (MANDATORY)
- [ ] 🔴 RED: Write failing tests
- [ ] 🟢 GREEN: Implement code to pass tests
- [ ] 🔵 REFACTOR: Clean up code while keeping tests green
- [ ] ✅ VERIFY: Coverage ≥80%

## Technical Details

[Implementation notes, architecture considerations, etc.]

## Testing Requirements

- Unit tests: [description]
- Integration tests: [description]
- E2E tests: [description]

---

_Last updated: [YYYY-MM-DD]_
```

---

**12. /security-review** - OWASP Security Scanning

**Phase 2 Enhancement: Security Review**

**Model**: Opus (claude-opus-4-1)

**Purpose**: Comprehensive OWASP-based security scanning with FALSE_POSITIVE filtering

**Process**:

1. **Read Current Context**:
   - Read `status.xml` for active feature
   - Read `<current-story>` value
   - Read story file for security requirements (if applicable)

2. **Embed Git Diff for Full Context**:

   Gather ALL changes upfront:

   ```bash
   # Git status
   git status

   # Files modified
   git diff --name-only origin/HEAD...

   # Commits
   git log --no-decorate origin/HEAD...

   # Full diff content
   git diff --merge-base origin/HEAD
   ```

   **Why**: Embedding full context upfront prevents repeated file reads

3. **Spawn security-reviewer Agent**:

   Launch security-reviewer agent (Opus model) with 3-step analysis workflow:

   ```markdown
   Task: Security review for [story/feature name]

   **Review using 3-step analysis**:

   Step 1: Identify Vulnerabilities
   - Scan for OWASP Top 10 vulnerabilities
   - Check authentication and authorization
   - Review input validation and sanitization
   - Examine cryptographic implementations
   - Assess data exposure risks
   - Identify injection vulnerabilities (SQL, XSS, command)

   Step 2: Filter False Positives (IN PARALLEL)
   - Apply 17 HARD EXCLUSIONS (see SECURITY_REVIEW_CHECKLIST.md)
   - Apply 12 PRECEDENTS for context-specific filtering
   - Assess signal quality criteria
   - Assign confidence score (1-10 scale)

   Step 3: Report High-Confidence Findings
   - Only report findings with confidence ≥8/10
   - Categorize severity: HIGH, MEDIUM, LOW
   - Provide concrete attack path for each finding
   - Include file:line references
   - Suggest remediation

   **Reference**: SECURITY_REVIEW_CHECKLIST.md for complete methodology
   ```

4. **Output Format**:

   ```markdown
   ## Security Review Summary

   - **Verdict**: [PASS | VULNERABILITIES_FOUND]
   - **HIGH Severity**: X findings
   - **MEDIUM Severity**: Y findings
   - **LOW Severity**: Z findings

   ---

   ## Findings

   ### Vuln 1: [Type] - HIGH (Confidence: 9/10)

   **Location**: `file.ts:123`

   **Description**: [Concrete vulnerability description]

   **Attack Path**: [Specific exploitation scenario]

   **Remediation**: [How to fix]

   ---

   ### Vuln 2: [Type] - MEDIUM (Confidence: 8/10)

   **Location**: `file.ts:456`

   **Description**: [Concrete vulnerability description]

   **Attack Path**: [Specific exploitation scenario]

   **Remediation**: [How to fix]

   ---

   ## OWASP Top 10 Coverage

   - [x] A01: Broken Access Control
   - [x] A02: Cryptographic Failures
   - [x] A03: Injection
   - [x] A04: Insecure Design
   - [x] A05: Security Misconfiguration
   - [x] A06: Vulnerable Components
   - [x] A07: Authentication Failures
   - [x] A08: Software/Data Integrity Failures
   - [x] A09: Security Logging Failures
   - [x] A10: Server-Side Request Forgery

   ---

   ## FALSE_POSITIVE Filtering Applied

   - 17 Hard Exclusions: [List which were applied]
   - 12 Precedents: [List which were applied]
   - Filtered out: N findings with confidence <8/10
   ```

5. **Confidence Scoring Guide**:

   - **9-10**: Concrete, exploitable vulnerability with clear attack path
   - **8**: Very likely vulnerability, specific code location, actionable
   - **7**: Probable vulnerability, needs minor investigation
   - **6**: Medium confidence, needs investigation
   - **1-5**: Low confidence, likely false positive (DO NOT REPORT)

6. **Update Story File** (if security issues found):

   If HIGH severity findings:
   - Add "## Security Issues" section to story file
   - List all HIGH severity findings with file:line
   - Update story status to "In Progress" (must fix before merge)

   If MEDIUM/LOW severity only:
   - Add as optional improvements to story notes
   - Do not block merge

**Important Notes**:

- **Model**: MUST use Opus (claude-opus-4-1) for security review
- **Threshold**: Only report findings with confidence ≥8/10
- **FALSE_POSITIVE Rules**: Apply ALL 17 hard exclusions + 12 precedents
- **Attack Path**: Every finding MUST include concrete attack scenario
- **No Theoretical Issues**: Only report exploitable, practical vulnerabilities


---

**13. /design-review** - UI/UX Design Review

**Phase 3 Enhancement: Design Review**

**Model**: Sonnet 4.5

**Purpose**: Comprehensive UI/UX review with Playwright live testing, WCAG 2.1 AA validation, and responsive design checks

**Prerequisites**: Requires Playwright MCP server and live preview environment

**Process**:

1. **Verify Preview Environment**:
   - Confirm dev server is running
   - Get preview URL from user or start dev server
   - Verify MCP Playwright server is connected

2. **Launch design-reviewer Agent**:

   Spawn design-reviewer agent (Sonnet model) with 7-phase design methodology:

   ```markdown
   Task: Design review for [feature/story name]

   **Preview URL**: [URL from user or localhost]

   **Review using 7-phase design methodology**:

   ## Phase 0: Preparation
   - Navigate to preview URL using Playwright
   - Analyze PR description/story for design intent
   - Review code diff for implementation scope
   - Set initial viewport (1440x900 desktop)

   ## Phase 1: Interaction and User Flow
   - Execute primary user flow from story
   - Test all interactive states (hover, active, focus, disabled)
   - Verify destructive action confirmations
   - Assess perceived performance and responsiveness
   - Take screenshots of key states

   ## Phase 2: Responsiveness Testing
   - Desktop viewport (1440px): Capture screenshot, verify layout
   - Tablet viewport (768px): Verify layout adaptation, no horizontal scroll
   - Mobile viewport (375px): Ensure touch optimization, readable text
   - Check element overlap and spacing at each breakpoint

   ## Phase 3: Visual Polish
   - Assess layout alignment and spacing consistency
   - Verify typography hierarchy and legibility
   - Check color palette consistency
   - Ensure visual hierarchy guides user attention
   - Verify image quality and aspect ratios

   ## Phase 4: Accessibility (WCAG 2.1 AA)
   - Test complete keyboard navigation (Tab order logical)
   - Verify visible focus states on all interactive elements
   - Confirm keyboard operability (Enter/Space activation)
   - Validate semantic HTML usage (headings, landmarks, lists)
   - Check form labels and associations
   - Verify image alt text
   - Test color contrast ratios (4.5:1 minimum for normal text, 3:1 for large text)

   ## Phase 5: Robustness Testing
   - Test form validation with invalid inputs
   - Stress test with content overflow scenarios (long text, many items)
   - Verify loading, empty, and error states
   - Check edge case handling (no data, single item, max items)

   ## Phase 6: Code Health
   - Verify component reuse over duplication
   - Check for design token usage (no magic numbers in styles)
   - Ensure adherence to component library priority order (check DESIGN_SYSTEM.md)
   - Verify consistent patterns across similar features

   ## Phase 7: Content and Console
   - Review grammar and clarity of all text
   - Check console for errors/warnings using Playwright
   - Verify no broken images or missing resources

   **Reference**: DESIGN_PRINCIPLES.md for complete methodology
   ```

3. **Playwright Testing Workflow**:

   ```javascript
   // Standard workflow for each phase
   
   // Phase 0: Setup
   await mcp__playwright__browser_navigate({ url: previewURL });
   await mcp__playwright__browser_resize({ width: 1440, height: 900 });
   
   // Phase 1: Interactions
   await mcp__playwright__browser_take_screenshot({ filename: "desktop-initial.png" });
   await mcp__playwright__browser_click({ element: "Primary CTA", ref: "button[data-testid='cta']" });
   await mcp__playwright__browser_take_screenshot({ filename: "desktop-clicked.png" });
   
   // Phase 2: Responsive testing
   await mcp__playwright__browser_resize({ width: 768, height: 1024 }); // Tablet
   await mcp__playwright__browser_take_screenshot({ filename: "tablet-view.png" });
   
   await mcp__playwright__browser_resize({ width: 375, height: 667 }); // Mobile
   await mcp__playwright__browser_take_screenshot({ filename: "mobile-view.png" });
   
   // Phase 7: Console check
   const consoleMessages = await mcp__playwright__browser_console_messages({ onlyErrors: true });
   ```

4. **Output Format**:

   ```markdown
   ## Design Review Summary

   - **Overall Assessment**: [Positive opening statement about what works well]
   - **Blockers**: X critical issues (must fix before merge)
   - **High-Priority**: Y important improvements
   - **Medium-Priority**: Z suggestions
   - **Nitpicks**: N minor polish items

   **Screenshots**: [Number] screenshots attached

   ---

   ## Findings

   ### Blockers (Must Fix Before Merge)

   #### [Blocker 1]: [Problem Description]

   **Problem**: [Describe user-facing impact, not technical implementation]

   **Screenshot**: ![Screenshot](./path/to/screenshot.png)

   **Impact**: [How this affects users - accessibility, usability, visual hierarchy]

   **WCAG Violation**: [If applicable] WCAG 2.1 [Criterion Number] Level AA

   **Viewport**: [Where issue occurs - Desktop/Tablet/Mobile/All]

   ---

   ### High-Priority (Strong Recommendations)

   #### [High 1]: [Problem Description]

   **Problem**: [Describe the issue]

   **Screenshot**: ![Screenshot](./path/to/screenshot.png)

   **Suggestion**: [Let implementer choose solution - describe problem, not prescription]

   ---

   ### Medium-Priority (Suggestions)

   #### [Medium 1]: [Improvement Idea]

   **Current**: [What exists now]

   **Opportunity**: [How it could be better]

   ---

   ### Nitpicks (Minor Polish)

   - Nit: [Small spacing inconsistency at 375px viewport]
   - Nit: [Button label could be more descriptive]

   ---

   ## WCAG 2.1 AA Compliance

   - [x] 1.4.3 Contrast (Minimum) - 4.5:1 for normal text
   - [x] 2.1.1 Keyboard - All functionality available via keyboard
   - [x] 2.4.7 Focus Visible - Focus indicator clearly visible
   - [x] 3.2.4 Consistent Navigation - Navigation consistent across pages
   - [x] 4.1.2 Name, Role, Value - All UI components properly labeled
   - [ ] **FAIL**: 1.4.11 Non-text Contrast - Icon contrast only 2.8:1 (needs 3:1)

   ---

   ## Responsive Testing Results

   | Viewport | Width | Status | Issues |
   |----------|-------|--------|--------|
   | Desktop  | 1440px | ✅ Pass | None |
   | Tablet   | 768px  | ⚠️ Minor | Text wrapping on sidebar |
   | Mobile   | 375px  | ❌ Fail | Button text truncated |

   ---

   ## Console Errors

   - ✅ No console errors detected
   OR
   - ⚠️ Warning: [Description]
   - ❌ Error: [Description]

   ---

   ## Component Library Check

   Verified component library priority order from DESIGN_SYSTEM.md:
   - [x] Checked Kibo UI - [Component] used
   - [ ] Could use Blocks.so [Component] instead of custom implementation
   ```

5. **Triage Categories**:

   - **Blocker**: WCAG violations, broken user flows, major visual bugs
   - **High-Priority**: Inconsistent patterns, poor UX, significant polish issues
   - **Medium-Priority**: Minor improvements, suggestions, optimization opportunities
   - **Nitpick**: Tiny spacing, wording tweaks, micro-interactions

6. **Philosophy: "Problems Over Prescriptions"**:

   - Describe the problem and user impact
   - Let the implementer choose the solution
   - Avoid prescriptive "change X to Y" feedback
   - Focus on what's broken, not how to fix it

**Important Notes**:

- **Playwright Required**: This command requires Playwright MCP server
- **Live Environment First**: Test actual UI before analyzing code
- **WCAG AA**: All findings must reference specific WCAG criteria
- **3 Viewports**: Always test desktop (1440px), tablet (768px), mobile (375px)
- **Screenshots**: Include visual evidence for all findings
- **No Theoretical Issues**: Only report observable UX problems

