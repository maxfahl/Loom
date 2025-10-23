---
description: Launch coordinator agent in autonomous YOLO mode to complete stories/epics
allowed-tools: Task
model: claude-sonnet-4-5
---

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
