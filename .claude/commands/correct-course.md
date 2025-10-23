---
description: Correct course on a feature based on new requirements or direction changes
model: claude-sonnet-4-5
argument-hint: [feature name or current]
---

# /correct-course - Correct Feature Direction

**Purpose**: Adjust feature direction based on changing requirements, mistakes, or new insights

## Process

1. **Identify Feature**
   - Use "current" for active feature
   - Or specify feature name explicitly

2. **Read Current Feature State**
   - Read `status.xml` for feature tracking
   - Read epic documentation (DESCRIPTION.md, TASKS.md, NOTES.md)
   - Read feature documentation (FEATURE_SPEC.md, TECHNICAL_DESIGN.md, etc.)
   - Review committed code
   - Review commit history

3. **Show User Current State Summary**
   - Feature overview
   - Epic breakdown and status
   - Completed work
   - Current progress
   - Pending tasks

4. **Understand Desired Changes**
   - Ask user what needs to change
   - Clarify new requirements
   - Understand why correction is needed
   - Identify scope of changes

5. **Analyze Impact**
   - Code to keep
   - Code to modify
   - Code to remove
   - Tests to update
   - Documentation to revise
   - Epics to reorganize

6. **Update Epic Documentation**
   - Update DESCRIPTION.md with changes
   - Update TASKS.md with new/modified/removed tasks
   - Add notes to NOTES.md explaining changes
   - Update story files if needed

7. **Update Feature Documentation**
   - Update FEATURE_SPEC.md with new requirements
   - Update TECHNICAL_DESIGN.md with architectural changes
   - Add entry to CHANGELOG.md documenting the correction
   - Update INDEX.md if structure changed

8. **Update status.xml**
   - Add course correction notes
   - Update epic status if changed
   - Mark tasks as cancelled if appropriate
   - Update `<current-epic>` if switching epics
   - Add `<cancelled-tasks>` section if needed

9. **Create Action Plan**
   - **Cleanup**: Remove obsolete code/tests/docs
   - **Modify**: Update existing implementations
   - **Add**: Create new functionality
   - **Update Docs**: Revise all affected documentation
   - **Verify**: Run tests and ensure nothing broke

10. **Execute Corrections**
    - Present plan to user
    - Offer options:
      - Automatic: Execute all changes autonomously
      - Step-by-step: Confirm each major change
      - Manual: Provide plan, user executes

11. **Handle Git History**
    - Revert commits if needed
    - Create new branch if significant changes
    - Document reasoning in commit messages

12. **Verify Corrections**
    - Run tests
    - Check documentation accuracy
    - Verify status.xml reflects new state
    - Ensure epic task lists are correct

13. **Update Epic Task Lists**
    - Reflect new direction in TASKS.md
    - Mark completed tasks
    - Add new tasks from corrections

14. **Update status.xml Final State**
    - Confirm all changes are tracked
    - Set correct `<current-epic>` and `<current-story>`
    - Update `<last-updated>` timestamp

## Important Notes

- Reads `prompts/project-setup-meta-prompt.md` for guidance
- Reviews ALL existing work before making changes (including all epic folders)
- Documents WHY correction was needed in:
  - Feature docs (CHANGELOG.md)
  - Epic NOTES.md
- Updates status.xml to reflect new direction (including epic status)
- Handles cancelled tasks appropriately (mark epic as cancelled if needed)
- May reorganize epics if direction changes significantly
- Updates `<current-epic>` if switching to different epic
- May add `<cancelled-tasks>` section to status.xml

## When to Use

- Requirements changed after starting development
- Discovered better approach mid-implementation
- Need to pivot feature direction
- Major bugs require architectural changes
- Epics need reorganization

## When NOT to Use

- Small bug fixes (use `/fix`)
- Minor code improvements (use `/dev`)
- Adding new story to existing epic (use `/create-story`)

## Example Scenarios

**Scenario 1: Changed Requirements**
- User: "We need to support OAuth2 instead of basic auth"
- Command analyzes current auth implementation
- Updates epic-1-authentication tasks
- Marks basic auth code for removal
- Adds OAuth2 implementation tasks
- Updates documentation

**Scenario 2: Epic Reorganization**
- User: "Epic 2 is too large, split into epic 2 and 3"
- Command analyzes epic-2 tasks
- Creates new epic-3 folder
- Redistributes tasks logically
- Updates status.xml epic tracking
- Moves stories to correct epics

**Scenario 3: Architectural Change**
- User: "Switch from REST API to GraphQL"
- Command analyzes current API code
- Updates TECHNICAL_DESIGN.md
- Reorganizes epic tasks
- Plans migration strategy
- Documents reasoning
