---
description: Correct course on a feature based on new requirements or direction changes
model: claude-sonnet-4-5
argument-hint: [feature name or current]
---

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
