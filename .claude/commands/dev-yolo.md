---
description: Start autonomous YOLO development loop (coordinator runs independently)
---

You are now launching the **COORDINATOR AGENT in AUTONOMOUS YOLO MODE** for Jump workspace manager. 🚀🤖

## Your Mission

You are the **coordinator agent** executing the autonomous development workflow. Your goal is to complete stories/epics following the YOLO mode configuration in `status.xml` without requiring user intervention at each step.

## Critical Distinction

This command (`/dev-yolo`) is the **execution tool** that runs the autonomous loop.

For **configuration** of YOLO mode settings, use `/yolo` instead.

## Phase 1: Read YOLO Configuration

First, gather all necessary context:

1. **Read status.xml**: `docs/development/status.xml`
   - Find active feature with `<is-active-feature>true</is-active-feature>`
   - Check `<yolo-mode enabled="true|false">`
   - Check `<stopping-granularity>` (story/epic/custom)
   - Read all breakpoint settings (1-9)
   - Get `<current-epic>` and `<current-story>` values

2. **Validate Prerequisites**:
   - ✅ Active feature exists
   - ✅ Current epic is set
   - ✅ Current story exists
   - ✅ YOLO mode is properly configured

   **If any missing**: ABORT and ask user to configure using `/yolo` first.

3. **Read current story file**:
   - Location: `docs/stories/story-{current-story}.md`
   - Parse acceptance criteria
   - Parse tasks and subtasks
   - Understand what needs to be done

## Phase 2: Execute Autonomous Development Loop

Follow the complete TDD cycle for the current story:

### Step 1: RED Phase (Write Failing Tests)

1. For each acceptance criterion, write failing tests FIRST
2. Run tests to verify they FAIL (proves tests are valid)
3. Update story file: check off subtask `- [x] 🔴 RED: Write failing tests`

### Step 2: GREEN Phase (Implement)

1. Write MINIMUM code to make tests pass
2. Run tests to verify they PASS
3. Update story file: check off subtask `- [x] 🟢 GREEN: Implement code to pass tests`

### Step 3: REFACTOR Phase (Clean Up)

1. Improve code quality while keeping tests green
2. Run tests to verify still PASSES
3. Update story file: check off subtask `- [x] 🔵 REFACTOR: Clean up code while keeping tests green`

### Step 4: Verify Coverage

1. Run test coverage analysis
2. Ensure coverage ≥80%
3. Update story file: check off subtask `- [x] ✅ VERIFY: Coverage ≥80%`

## Phase 3: Code Review

When all tasks/subtasks are complete:

1. **Spawn code-reviewer agent** for review
2. **If issues found**:
   - Create "## Review Tasks" section in story file
   - Add tasks with priority prefix:
     - `- [ ] Fix: [Blocking issue] (file:line)`
     - `- [ ] Improvement: [High priority] (file:line)`
     - `- [ ] Nit: [Low priority polish] (file:line)`
   - Update story status to "In Progress"
   - Work through Review Tasks
   - Re-run code review when done
3. **If approved**:
   - Update story status to "Done"
   - Proceed to next phase

## Phase 4: Check YOLO Breakpoints

Based on `<stopping-granularity>` configuration:

### STORY-LEVEL Mode

Check breakpoints 1-8 during story execution:

- **Breakpoint 1**: After completing development, before code review
- **Breakpoint 2**: After code review, before running tests
- **Breakpoint 3**: After tests pass, before user testing
- **Breakpoint 4**: After user testing, before committing
- **Breakpoint 5**: After commit, before pushing to remote
- **Breakpoint 6**: Before making any file changes (very cautious)
- **Breakpoint 7**: Before running any tests (very cautious)
- **Breakpoint 8**: Before major refactoring

If breakpoint is **enabled**: STOP and report status to user
If breakpoint is **disabled**: Continue automatically

### EPIC-LEVEL Mode

- **IGNORE** breakpoints 1-8 within stories
- Complete ALL stories in current epic autonomously
- **ONLY** check breakpoint 9 after completing entire epic

### CUSTOM Mode

Check all enabled breakpoints 1-9 as configured

## Phase 5: Move to Next Story (If YOLO Allows)

When story is done:

1. **Check breakpoint 9** (if at epic boundary):
   - If **enabled**: STOP and report epic completion
   - If **disabled**: Move to next epic automatically

2. **If more stories in current epic**:
   - Update `<current-story>` in status.xml to next story
   - Loop back to Phase 1 with new story

3. **If epic complete**:
   - Update epic status to "Done"
   - Check breakpoint 9 configuration
   - If continuing: Move to next epic's first story
   - If stopping: Report completion and exit

## Stopping Conditions (Abort Immediately)

Stop the loop and report to user if:

- ❌ Cannot find story file
- ❌ Tests fail after 3 attempts
- ❌ Coverage drops below required threshold
- ❌ Circular dependency detected
- ❌ Required file missing
- ❌ Critical blocker in status.xml
- ❌ Manual intervention required (user-specific note in story)
- ❌ Enabled breakpoint reached

## Success Report Format

When stopping (either at breakpoint or completion):

```
🎯 YOLO Loop Status Report

**Feature**: {feature-name}
**Stopped At**: {Breakpoint X / Epic Complete / Feature Complete}

**Completed**:
- ✅ Story 1.1: {title} (commit: abc123)
- ✅ Story 1.2: {title} (commit: def456)
- ✅ Story 2.1: {title} (commit: ghi789)

**Current State**:
- Epic: {epic-id}
- Story: {story-id}
- Status: {In Progress / Waiting For Review / Done}
- Tests: {X/Y passing, Z% coverage}

**Next Steps**:
{What user should do next or what will happen when resumed}
```

## Critical Rules (NEVER VIOLATE)

### TDD Enforcement

- ❌ **FORBIDDEN**: Writing implementation before tests
- ✅ **REQUIRED**: Tests MUST be written FIRST (RED phase)
- ✅ **REQUIRED**: Implementation follows tests (GREEN phase)
- ✅ **REQUIRED**: Refactoring while tests pass (REFACTOR phase)

### Swift Safety

- ❌ **FORBIDDEN**: Force unwrapping with `!` operator
- ❌ **FORBIDDEN**: Force casting with `as!` operator
- ❌ **FORBIDDEN**: Implicitly unwrapped optionals (except IBOutlets)
- ✅ **REQUIRED**: Use `guard`, `if-let`, `??`, or optional chaining
- ✅ **REQUIRED**: Return `Result<T, Error>` instead of throwing

### E2E Testing Integrity

- ❌ **FORBIDDEN**: Fake "E2E" tests that don't use XCUIApplication
- ✅ **REQUIRED**: E2E tests MUST launch actual app with XCUIApplication
- ✅ **REQUIRED**: E2E tests MUST be in `TestTools/UITests/` directory

### Story Context Authority

- ✅ **REQUIRED**: Story Context XML is the single source of truth
- ✅ **REQUIRED**: Read Story Context XML BEFORE starting any story
- ✅ **REQUIRED**: Update story files as you complete tasks
- ✅ **REQUIRED**: Update status.xml with commit hashes

## Example Output

```bash
User: /dev-yolo

🚀 Launching coordinator agent in YOLO mode...

**Reading Configuration**:
- Feature: core-workspace-jump
- YOLO Mode: ON
- Stopping Granularity: EPIC-LEVEL
- Breakpoints: 9 only (epic boundaries)

**Current State**:
- Epic: 1
- Story: 1.1
- Status: Not Started

Coordinator will autonomously complete ALL stories in Epic 1.
Will stop after Epic 1 completes (breakpoint 9 enabled).

---

**Starting Story 1.1: Basic workspace model**

🔴 RED: Writing failing tests...
✅ Tests fail (expected)

🟢 GREEN: Implementing minimum code...
✅ Tests pass

🔵 REFACTOR: Cleaning up...
✅ Tests still pass

✅ Coverage: 85% (target: 80%)

📝 Spawning code-reviewer...
✅ Code review: APPROVED

✅ Story 1.1 complete (commit: abc123)

---

**Moving to Story 1.2: Workspace store integration**

🔴 RED: Writing failing tests...
[continues autonomously...]

---

🎯 YOLO Loop Status Report

**Feature**: core-workspace-jump
**Stopped At**: Breakpoint 9 (Epic 1 Complete)

**Completed**:
- ✅ Story 1.1: Basic workspace model (commit: abc123)
- ✅ Story 1.2: Workspace store integration (commit: def456)
- ✅ Story 1.3: Context detection service (commit: ghi789)
- ✅ Story 1.4: Jump action implementation (commit: jkl012)

**Current State**:
- Epic: 1 (Done)
- Story: 1.4 (Done)
- Tests: 48/48 passing, 87% coverage

**Next Steps**:
- Review Epic 1 completion
- Run `/dev-yolo` again to continue to Epic 2
- Or run `/yolo` to adjust breakpoint configuration
```

## When to Use `/dev-yolo`

**Use this command when**:
- ✅ Starting new feature development (let agents work autonomously)
- ✅ Resuming after reviewing epic completion
- ✅ Running overnight development (high-trust YOLO mode)
- ✅ Rapid prototyping (YOLO mode with minimal breakpoints)

**DO NOT use when**:
- ❌ Manual single-story development (use `/dev` instead)
- ❌ Need to review each change before proceeding
- ❌ Testing YOLO configuration for first time (start with `/dev` first)
- ❌ Critical production changes (use manual review workflow)

## Resuming After Stop

If coordinator stopped at a breakpoint:

1. Review the work completed
2. Make any necessary adjustments
3. Run `/dev-yolo` again to continue from current position
4. Or run `/yolo` to adjust breakpoint configuration, then `/dev-yolo`

## Quick Reference

- **Configure YOLO mode**: `/yolo`
- **Run autonomous loop**: `/dev-yolo` (this command)
- **Manual development**: `/dev`
- **Check status**: `/status`
- **Run tests**: `/test`

---

**Remember**: The coordinator agent runs autonomously. Trust the TDD process. The agents will follow the rules strictly. 🤖✨
