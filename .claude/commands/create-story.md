---
description: Create the next user story for the current epic
model: claude-sonnet-4-5
---

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
