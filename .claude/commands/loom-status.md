---
description: Show comprehensive project status
model: haiku
---

# /loom-status - Project Status

## What This Command Does

Quick status report showing git status, current tasks, test status, and coverage.

## Process

1. **Read Current Context**:
   - Read `docs/development/status.xml`
   - Extract current feature, epic, and story
   - Read current story file

2. **Git Status**:
   ```bash
   git status
   git log --oneline -5
   git branch -vv
   ```

3. **Task Status**:
   - Count total tasks in current story
   - Count completed tasks (`[x]`)
   - Count pending tasks (`[ ]`)
   - List any Review Tasks

4. **Test Status** (if applicable):
   ```bash
   npm test -- --coverage --passWithNoTests
   ```
   - Extract pass/fail counts
   - Extract coverage percentages

5. **YOLO Configuration**:
   - Show current autonomy level
   - Show enabled breakpoints

6. **Output Summary**:
   ```markdown
   # Project Status

   ## Current Work
   - Feature: [feature-name]
   - Epic: [epic-number] - [epic-name]
   - Story: [story-number] - [story-title]
   - Status: [In Progress/Waiting For Review/Done]

   ## Tasks
   - Total: [X]
   - Completed: [X] ([X]%)
   - Pending: [X]
   - Review Tasks: [X]

   ## Git
   - Branch: [branch-name]
   - Commits ahead: [X]
   - Uncommitted changes: [X files]

   ## Tests
   - Tests: [X passed / X total]
   - Coverage: [X]%
   - Status: [✅ Passing / ❌ Failing]

   ## YOLO Mode
   - Autonomy Level: [MANUAL/BALANCED/STORY/EPIC/CUSTOM]
   - Breakpoints: [A] [B] [C] [D]
   ```

## Recommended Skills

<!-- TODO: Add relevant skills from .claude/skills/ -->

- `git-flow` - For git status interpretation

Use these skills heavily throughout execution to ensure best practices.

**Skill Troubleshooting Authority**: If any referenced skill does not work or any script within the skill does not work, Claude Code has the authority to fix them.

## Arguments

This command takes no arguments.

## Examples

```
/loom-status
```

Shows comprehensive project status report.
