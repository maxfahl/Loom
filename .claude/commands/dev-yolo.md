---
description: Launch coordinator agent in autonomous YOLO mode to complete stories/epics
allowed-tools: Task
model: claude-sonnet-4-5
---

# /dev-yolo - Autonomous YOLO Loop (Full Feature Completion)

**Purpose**: Start the autonomous development loop where the coordinator agent completes entire stories, epics, or features following YOLO mode configuration

**CRITICAL: This command spawns the coordinator agent for autonomous execution**

## Process

### 1. Read YOLO Configuration

Read `docs/development/status.xml` and extract:

- Find active feature with `<is-active-feature>true</is-active-feature>`
- Check `<yolo-mode enabled="true|false">`
- Check `<stopping-granularity>` (story/epic/custom)
- Read all breakpoint settings (1-9)

### 2. Validate Prerequisites

Ensure the following exist, otherwise ABORT:

- ✅ Active feature exists
- ✅ Current epic is set
- ✅ Current story exists
- ✅ YOLO mode is properly configured

If any missing: **ABORT** and ask user to configure

### 3. Spawn Coordinator Agent

Launch the coordinator agent with this comprehensive prompt:

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

### 4. Monitor Progress

- Coordinator agent runs autonomously
- Stops at configured breakpoints
- Returns status report when complete or stopped

### 5. Resume After Stop

- **If stopped at breakpoint**: Run `/dev-yolo` again to continue
- **If user wants to change YOLO config**: Run `/yolo` first, then `/dev-yolo`

## Examples

### Example 1: Start YOLO Loop

```bash
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

### Example 2: Epic-Level Autonomy

```bash
# Configure YOLO mode for epic-level autonomy
/yolo
# Select B (EPIC-LEVEL)

# Start YOLO loop
/dev-yolo

# Coordinator autonomously completes:
# - Story 1.1: Setup authentication routes (commit: abc123)
# - Story 1.2: Implement JWT tokens (commit: def456)
# - Story 1.3: Add password hashing (commit: ghi789)
# - Story 1.4: Create login endpoint (commit: jkl012)
#
# 🎯 YOLO Loop Status Report
# Feature: user-authentication
# Stopped At: Epic 1 Complete (Breakpoint 9)
#
# Completed:
# - ✅ Story 1.1: Setup authentication routes (commit: abc123)
# - ✅ Story 1.2: Implement JWT tokens (commit: def456)
# - ✅ Story 1.3: Add password hashing (commit: ghi789)
# - ✅ Story 1.4: Create login endpoint (commit: jkl012)
#
# Next Steps:
# - Review Epic 1 work
# - Run /dev-yolo again to start Epic 2
```

### Example 3: Story-Level Control

```bash
# Configure YOLO mode for story-level control
/yolo
# Select A (STORY-LEVEL)
# Choose breakpoints: 1, 4

# Start YOLO loop
/dev-yolo

# Coordinator completes story 1.1 and stops at breakpoint 1 (before code review)
#
# 🎯 YOLO Loop Status Report
# Feature: user-authentication
# Stopped At: Breakpoint 1 (After development, before code review)
#
# Completed:
# - ✅ Story 1.1: Setup authentication routes (commit: abc123)
#
# Current State:
# - Epic: epic-1-foundation
# - Story: 1.1
# - Status: Waiting For Review
# - Tests: 45/45 passing, 92% coverage
#
# Next Steps:
# - Review the code
# - Run /dev-yolo to continue to next story
```

## When to Use

- ✅ Starting new feature development (let agents complete stories autonomously)
- ✅ Resuming after reviewing epic completion
- ✅ Running overnight development (high-trust YOLO mode)
- ✅ Rapid prototyping (YOLO mode with minimal breakpoints)

## When NOT to Use

- ❌ Manual single-story development (use `/dev` instead)
- ❌ Need to review each change before proceeding
- ❌ Testing YOLO configuration for first time (start with `/dev` first)
- ❌ Critical production changes (use manual review workflow)

## Stopping Granularities

### Story-Level (Default)

- Stops at specific breakpoints within each story
- Gives maximum control
- Ideal for learning the system or critical features

### Epic-Level (Maximum Autonomy)

- Only stops at epic boundaries (breakpoint 9)
- Agents autonomously complete entire epics
- Ideal for high-trust autonomous development
- User reviews work at logical epic milestones

### Custom

- Select individual breakpoints manually
- Tailored stopping points
- Balance between control and autonomy

## Breakpoint Reference

1. After completing development, before code review
2. After code review, before running tests
3. After tests pass, before user testing
4. After user testing, before committing
5. After commit, before pushing to remote
6. Before making any file changes (very cautious)
7. Before running any tests (very cautious)
8. Before major refactoring
9. After completing epic, before starting next epic (EPIC-LEVEL)

## YOLO Mode Philosophy

**YOLO Mode ON** = Agents work autonomously with minimal intervention
**YOLO Mode OFF** = Maximum control, stop at all breakpoints

**Story-Level** = Stop at logical points within stories
**Epic-Level** = Only stop at epic boundaries (maximum autonomy)

The coordinator reads your configuration and automatically handles the complete TDD cycle:
**Red → Green → Refactor → Review → Test → Commit → Deploy**

## Common Issues

**Issue**: Coordinator stops immediately after starting
- **Cause**: Story file missing or malformed
- **Fix**: Run `/create-story` first, ensure story file exists

**Issue**: Tests fail and loop aborts
- **Cause**: TDD cycle broken, tests not passing
- **Fix**: Manually fix tests, run `/test` to verify, then resume `/dev-yolo`

**Issue**: YOLO mode not respecting breakpoints
- **Cause**: status.xml configuration incorrect
- **Fix**: Run `/yolo` to reconfigure breakpoints

**Issue**: Coordinator skips epic boundary (breakpoint 9)
- **Cause**: Breakpoint 9 disabled in status.xml
- **Fix**: Run `/yolo`, ensure breakpoint 9 is enabled if you want epic-level stops
