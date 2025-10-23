---
description: Continue development on current task with automatic task tracking
allowed-tools: Bash(npm:*), Bash(git:*), Read, Write, Edit, Glob, Grep
model: claude-sonnet-4-5
---

# /dev - Continue Development with Automatic Task Tracking

**Purpose**: Resume coding with context of current task, following project conventions, with automatic task tracking and status updates

## Phase 0 Enhancement: Automatic Task Tracking

### Process

#### 1. Read Current Context

- Read `docs/development/status.xml` for active feature
- Read `<current-story>` value (e.g., "1.2")
- Read story file at `docs/development/features/[feature]/epics/[epic]/stories/[current-story].md`

#### 2. Check for Review Tasks (PRIORITY)

- Look for "## Review Tasks" section in story file
- If exists and has uncompleted tasks (`[ ]`):
  - **Prioritize Review Tasks FIRST**
  - Work on highest priority tasks (Fix > Improvement > Nit)
  - Check off tasks as completed (`[ ]` → `[x]`)
- If all Review Tasks complete, proceed to regular tasks

#### 3. Work on Regular Tasks

- Read "## Tasks and Subtasks" section
- Continue from last uncompleted task
- Check off subtasks as completed (`[ ]` → `[x]`)
- Update story file with progress

#### 4. Update Story Status When Complete

- If ALL tasks and subtasks are checked (`[x]`):
  - Update story **Status** to "Waiting For Review"
  - Update **Last Updated** timestamp
  - Add note to status.xml about completion
- If tasks still pending:
  - Keep status as "In Progress"
  - Update **Last Updated** timestamp

#### 5. Follow Project Conventions

- Read acceptance criteria from story file
- Follow TDD methodology (see below)
- Reference technical details and dependencies
- Maintain test coverage requirements

### TDD Variations

- **Fully Enforced**: "Follow TDD Red-Green-Refactor strictly. Write failing test FIRST, then implement."
- **Recommended**: "Follow TDD Red-Green-Refactor when possible. Consider writing tests first."
- **No TDD**: "Continue implementation. Add tests for critical functionality."

## Usage

```bash
# Continue development on current story
/dev

# The command will:
# 1. Read status.xml and current story file
# 2. Check for Review Tasks (priority)
# 3. Work on next uncompleted task
# 4. Update story file with progress
# 5. Update status when complete
```

## When to Use

- Starting work on a new story
- Resuming work after a break
- Continuing after code review feedback (Review Tasks)
- Making progress on current task

## When NOT to Use

- For autonomous multi-story completion (use `/dev-yolo` instead)
- For creating new stories (use `/create-story` instead)
- For reviewing code (use `/review` instead)
- For committing changes (use `/commit` instead)
