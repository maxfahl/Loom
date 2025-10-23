---
description: Create the next user story for the current epic
model: sonnet
---

# /create-story - Create User Story

## What This Command Does

Create the next user story within the current epic with proper structure and tasks.

## Process

1. **Read Current Context**:
   - Read status.xml for current feature and epic
   - Read epic DESCRIPTION.md for goals and context
   - Read existing stories to understand numbering

2. **Determine Story Number**:
   - Find highest story number in current epic
   - Increment by 1 (e.g., if 1.2 exists, next is 1.3)

3. **Gather Story Details**:
   - Ask user for story description
   - Clarify acceptance criteria
   - Understand dependencies
   - Estimate complexity (S/M/L/XL)

4. **Create Story File** (e.g., `1.3.md`):

   ```markdown
   # Story 1.3: [Story Title]

   **Status**: To Do
   **Priority**: [High/Medium/Low]
   **Complexity**: [S/M/L/XL]
   **Created**: [Date]
   **Last Updated**: [Date]

   ## Description

   As a [user type], I want [goal] so that [benefit].

   ## Acceptance Criteria

   - [ ] Criterion 1
   - [ ] Criterion 2
   - [ ] Criterion 3

   ## Technical Notes

   [Any technical considerations or constraints]

   ## Tasks and Subtasks

   ### Task 1: [Task Name]
   - [ ] Subtask 1.1
   - [ ] Subtask 1.2

   ### Task 2: [Task Name]
   - [ ] Subtask 2.1
   - [ ] Subtask 2.2

   ## Dependencies

   - Story 1.2: [Description]

   ## Test Strategy

   - Unit tests: [What to test]
   - Integration tests: [What to test]
   - E2E tests: [What to test]

   ## Definition of Done

   - [ ] All acceptance criteria met
   - [ ] Tests written and passing (80%+ coverage)
   - [ ] Code reviewed and approved
   - [ ] Documentation updated
   - [ ] Deployed to staging
   ```

5. **Update Epic TASKS.md**:
   - Add new story to epic task list

6. **Update status.xml** (optional):
   - If user wants to start immediately, set as current story

## Recommended Skills

<!-- TODO: Add relevant skills from .claude/skills/ -->

- `agile-methodologies` - For story structure
- `requirements-engineering` - For acceptance criteria
- `tdd-red-green-refactor` - For test strategy

Use these skills heavily throughout execution to ensure best practices.

**Skill Troubleshooting Authority**: If any referenced skill does not work or any script within the skill does not work, Claude Code has the authority to fix them.

## Arguments

This command takes no arguments. Creates next story in current epic.

## Examples

```
/create-story
```

Creates next user story in current epic.
