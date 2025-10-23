---
description: Create the next user story for the current epic
model: claude-sonnet-4-5
---

# /create-story - Create Next Story

**Purpose**: Analyze completed work, identify next story, and create comprehensive story file

## Process

1. **Read status.xml**
   - Identify active feature
   - Identify current epic
   - Check current story number

2. **Read Epic TASKS.md**
   - Location: `docs/development/features/[feature-name]/epics/[current-epic]/TASKS.md`
   - Understand epic scope
   - Review pending tasks

3. **Check Existing Stories**
   - Location: `docs/development/features/[feature-name]/epics/[current-epic]/stories/`
   - See what stories have been created
   - Determine next story number

4. **Analyze Completion Status**
   - Review what's been completed in epic
   - Identify what's pending
   - Determine logical next story

5. **Determine Next Story Number**
   - Example: If current-story is 2.1, check if 2.1 exists
   - If 2.1 exists and is complete, create 2.2
   - Follow [epic].[story] naming pattern

6. **CRITICAL: Create New Story File**
   - **Correct location**: `docs/development/features/[feature-name]/epics/[current-epic]/stories/[epic.story].md`
   - **NOT**: `features/[feature-name]/stories/`
   - **NOT**: `docs/development/features/[feature-name]/stories/`
   - **ONLY**: `docs/development/features/[feature-name]/epics/[current-epic]/stories/`

7. **Update status.xml**
   - Set `<current-story>` to new story number
   - Update `<last-updated>` timestamp
   - Add note about story creation

## Story File Location (CRITICAL - DO NOT CHANGE)

- ✅ **Correct**: `docs/development/features/[feature-name]/epics/[epic-name]/stories/X.Y.md`
- ❌ **Wrong**: `features/[feature-name]/stories/X.Y.md`
- ❌ **Wrong**: `docs/development/features/[feature-name]/stories/X.Y.md`

**The story file MUST live inside the epic's stories/ folder, NOT in the feature root.**

## Story File Structure

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

## Important Notes

- Story numbering follows [epic].[story] format (e.g., 1.1, 1.2, 2.1, 2.2)
- Each story lives in its epic's stories/ folder
- Story file contains complete task breakdown
- TDD workflow is mandatory (Red-Green-Refactor)
- status.xml tracks current story globally
- Epic TASKS.md provides context for story creation

## When to Use

- Ready to start next story in current epic
- Completed current story and need next one
- Planning work breakdown for epic

## When NOT to Use

- Need to create new feature (use `/create-feature`)
- Need to change feature direction (use `/correct-course`)
- Working on existing story (use `/dev`)

## Example Workflow

```bash
# User completes story 1.1
/dev  # Finish remaining tasks in 1.1

# Review completed work
/review

# Commit story 1.1
/commit

# Create next story
/create-story
# Output: Created story 1.2 at docs/development/features/user-auth/epics/epic-1-foundation/stories/1.2.md

# Start working on new story
/dev
```

## Story Lifecycle

1. **Created**: Story file created via `/create-story`
2. **In Progress**: Developer working on tasks via `/dev`
3. **Waiting For Review**: All tasks complete, awaiting code review
4. **In Progress** (again): Issues found in review, fixing Review Tasks
5. **Done**: Code review approved, story complete
6. **Next Story**: Run `/create-story` to create next story

## Status Tracking

The story file maintains its own status that syncs with status.xml:

- **Status field**: Current story state
- **Last Updated**: Timestamp of last change
- **Task checkboxes**: Track completion (`[ ]` → `[x]`)
- **Review Tasks section**: Added by `/review` if issues found

## Common Issues

**Issue**: Story file not found when running `/dev`
- **Cause**: Story created in wrong location
- **Fix**: Verify file is in `docs/development/features/[feature]/epics/[epic]/stories/`

**Issue**: status.xml not updated after story creation
- **Cause**: Forgot to update `<current-story>`
- **Fix**: Manually update status.xml with new story number

**Issue**: Story number conflicts with existing story
- **Cause**: Didn't check existing stories before creating
- **Fix**: Check stories/ folder first, use next available number
