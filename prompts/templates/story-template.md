# Story File Template

**Part of**: [Project Setup Meta Prompt](../project-setup-meta-prompt.md)

## Purpose

Template for story files (epic.story format like 1.1, 2.3) used in the docs/development/features/[feature]/epics/[epic]/stories/ directory. Includes story description, acceptance criteria, tasks/subtasks, technical details, and notes sections.

## Related Files

- [../reference/status-xml.md](../reference/status-xml.md) - Stories referenced in status.xml
- [../phases/phase-6-features-setup.md](../phases/phase-6-features-setup.md) - Features and stories setup

## Usage

Read this file:
- When creating stories with /create-story command
- To understand story file structure
- For epic.story numbering format (e.g., 2.3 = Epic 2, Story 3)

---

# Story X.Y: [Story Title]

**Epic**: [Epic X - Epic Name]
**Created**: [ISO 8601 timestamp]
**Status**: In Progress

## Story Description

[1-2 paragraph description of what this story accomplishes]

## Acceptance Criteria

- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

## Tasks and Subtasks

### Task 1: [Task Name]

- [ ] Subtask 1.1: [Description]
- [ ] Subtask 1.2: [Description]
- [ ] Subtask 1.3: [Description]

### Task 2: [Task Name]

- [ ] Subtask 2.1: [Description]
- [ ] Subtask 2.2: [Description]

### Task 3: [Task Name]

- [ ] Subtask 3.1: [Description]

## Technical Details

### Files to Create/Modify

- `[file path]` - [What to do]
- `[file path]` - [What to do]

### Dependencies

- Depends on: [Previous story or external dependency]
- Blocks: [Future stories that depend on this]

### Testing Requirements

- [ ] Unit tests for [component]
- [ ] Integration tests for [flow]
- [ ] E2E tests for [user journey]

## Notes

[Any important context, decisions, or considerations]

---

**Last Updated**: [ISO 8601 timestamp]
```

**Important**:

- Story file is THE source of truth for what to implement
- Agents read this story file to understand requirements
- Checklist items are checked off as work progresses
- Story location: `docs/development/features/[feature]/epics/[epic]/stories/[story].md`
- Epic folder: `docs/development/features/[feature]/epics/[epic]/`
- Feature tracking: `features/[feature]/status.xml` (not in docs/)
- Format is always `[epic-number].[story-number].md` (e.g., 2.1.md, 2.2.md)
