---
description: Address a bug by creating a new, high-priority story
allowed-tools: Read, Write, Edit, Glob, Grep, Task
model: claude-sonnet-4-5
argument-hint: [Describe the bug you want to fix]
---

# /fix - Fix an Issue

**Purpose**: Intelligently handle a request to fix a bug by researching existing stories and, if necessary, creating a new high-priority story for the fix.

## Process

### Step 1: Research Existing Stories

Scan all story files (`*.md`) within the active feature's `epics` directory to see if the bug is already covered.

```bash
# Read status.xml to identify active feature
# Search for existing stories that might cover this bug
# Check story titles, descriptions, and tasks
```

### Step 2: Report Findings and Ask User

**If the fix is already planned**:
```
🔍 Bug Fix Research Results

**Your Request**: [user's bug description]

**Finding**: This issue is already covered in existing story:
- Story [X.Y]: [title]
- Location: docs/development/features/[feature]/epics/[epic]/stories/[X.Y].md
- Status: [In Progress / Waiting For Review / Done]

**Recommendation**: Use `/dev` to continue work on Story [X.Y] instead of creating a duplicate.

Would you like to proceed with Story [X.Y] or create a new story anyway?
```

**If not found in existing stories**:
```
🔍 Bug Fix Research Results

**Your Request**: [user's bug description]

**Finding**: No existing story covers this bug.

**Recommendation**: Create a new high-priority fix story.

Would you like to create a new story for this fix? (yes/no)
```

### Step 3: Create New Story (If User Approved)

If user approves creating a new story:

1. **Determine Story Number**:
   - Read current epic and existing stories
   - Calculate next story number (e.g., if current epic has stories 3.1, 3.2, create 3.3-fix)
   - Use `-fix` suffix to indicate this is a bug fix story

2. **Create Story File**:

   **Location**: `docs/development/features/[feature-name]/epics/[epic-name]/stories/[epic.story]-fix.md`

   **Story File Structure**:
   ```markdown
   # Story [epic].[story]-fix: Fix - [Bug Title]

   **Status**: In Progress
   **Epic**: [epic-id]
   **Priority**: HIGH (Bug Fix)
   **Created**: [YYYY-MM-DD]
   **Last Updated**: [YYYY-MM-DD]

   ## Bug Description

   [User's bug description]

   ## Expected Behavior

   [What should happen]

   ## Actual Behavior

   [What currently happens]

   ## Steps to Reproduce

   1. [Step 1]
   2. [Step 2]
   3. [Step 3]

   ## Acceptance Criteria

   - [ ] Bug is fixed and no longer reproducible
   - [ ] Tests added to prevent regression
   - [ ] No new bugs introduced
   - [ ] Code review approved

   ## Tasks and Subtasks

   ### Task 1: Investigate Root Cause
   - [ ] Reproduce the bug locally
   - [ ] Identify the problematic code
   - [ ] Understand why the bug occurs

   ### Task 2: 🔴🟢🔵 TDD Workflow (MANDATORY)
   - [ ] 🔴 RED: Write failing test that reproduces the bug
   - [ ] 🟢 GREEN: Implement fix to make test pass
   - [ ] 🔵 REFACTOR: Clean up code while keeping tests green
   - [ ] ✅ VERIFY: Coverage ≥80%

   ### Task 3: Verify Fix
   - [ ] Confirm original steps to reproduce no longer trigger bug
   - [ ] Run full test suite
   - [ ] Check for any side effects

   ### Task 4: Code Review
   - [ ] Run `/review` command
   - [ ] Address any review findings

   ## Technical Details

   [Implementation notes, affected files, related code]

   ## Testing Requirements

   - Regression test: [description of test that catches this bug]
   - Unit tests: [affected units]
   - Integration tests: [if needed]

   ---

   _Last updated: [YYYY-MM-DD]_
   ```

### Step 4: "Shoe Horn" the Story In

Update `docs/development/status.xml` to prioritize the fix:

```xml
<!-- Save the current story to resume later -->
<whats-next>
  <item>Resume Story [X.Y]: [original story title] (was in progress before fix)</item>
</whats-next>

<!-- Set the fix story as current -->
<current-story>[epic].[story]-fix</current-story>

<!-- Add note about the fix -->
<notes>
  <note timestamp="[YYYY-MM-DD HH:MM:SS]">
    Created high-priority fix story [epic].[story]-fix for: [bug description]
    Original story [X.Y] paused and will resume after fix is complete.
  </note>
</notes>
```

### Step 5: Confirm to User

```
✅ Fix Story Created

**Story**: [epic].[story]-fix - Fix - [Bug Title]
**Location**: docs/development/features/[feature]/epics/[epic]/stories/[epic.story]-fix.md
**Priority**: HIGH (Bug Fix)

**What Happened**:
- Created new story for the bug fix
- Set as current story in status.xml
- Original story [X.Y] paused and saved to resume later

**Next Steps**:
1. Run `/dev` to start working on the fix
2. Follow TDD workflow (write failing test first)
3. Run `/review` when fix is complete
4. Run `/commit` to commit the fix
5. Original story [X.Y] will automatically resume after this fix

**Story Tasks**:
- Investigate root cause
- Write regression test (TDD RED phase)
- Implement fix (TDD GREEN phase)
- Refactor if needed (TDD REFACTOR phase)
- Verify fix and run full test suite
```

## Usage Examples

```bash
# Fix a specific bug
/fix "Users can't log out when session expires"

# Fix a UI bug
/fix "Button overlaps text on mobile devices at 375px width"

# Fix a data bug
/fix "User profile data not saving correctly for premium accounts"

# Fix a performance bug
/fix "API endpoint times out when fetching large datasets"
```

## When to Use

- Discovered a bug not covered by existing stories
- Need to create a high-priority fix story
- Want to track bug fix as a separate story
- Bug requires investigation and proper TDD workflow

## When NOT to Use

- Bug is already covered in existing story (just use `/dev`)
- Minor typo or quick fix (just fix it directly)
- Bug is in story currently in progress (work on that story)

## Research Strategy

When scanning for existing stories, check for:

1. **Exact matches**: Story title/description mentions the exact bug
2. **Related features**: Stories working on the same component/area
3. **Similar symptoms**: Stories addressing similar issues
4. **Recent fixes**: Stories recently completed that might have fixed it

**Search locations**:
- `docs/development/features/[feature]/epics/*/stories/*.md`
- Story titles and descriptions
- Task lists and acceptance criteria
- Technical details sections

## Notes

- Story numbering follows pattern: `[epic].[next-story]-fix`
- The `-fix` suffix indicates this is a bug fix story
- Fix stories have HIGH priority by default
- Original story is paused, not cancelled
- Fix story updates status.xml as current story
- After fix is complete and committed, original story can resume
- TDD is MANDATORY for fix stories (regression test required)

## Philosophy

**"Stop the Line" Approach**:
- When a bug is found, address it immediately
- Create proper story for tracking and accountability
- Follow TDD to ensure regression test exists
- Resume original work only after fix is complete and verified

This ensures bugs don't accumulate and all fixes are properly tested and documented.
