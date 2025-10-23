---
description: Address a bug by creating a new, high-priority story
model: sonnet
argument-hint: [Describe the bug]
---

# /fix - Fix Bug

## What This Command Does

Create a high-priority story for a bug fix and optionally start working on it immediately.

## Process

1. **Gather Bug Details**:
   - Use `$ARGUMENTS` if provided
   - Otherwise, ask user for bug description
   - Understand reproduction steps
   - Clarify impact and severity

2. **Read Current Context**:
   - Read status.xml for current feature and epic
   - Determine where bug fix story should be created

3. **Create Bug Fix Story**:

   Create new story file with structure:

   ```markdown
   # Story [X.Y]: [BUG FIX] [Description]

   **Status**: To Do
   **Priority**: High
   **Type**: Bug Fix
   **Complexity**: [S/M/L based on impact]
   **Created**: [Date]
   **Last Updated**: [Date]

   ## Bug Description

   [Detailed description from $ARGUMENTS]

   ## Reproduction Steps

   1. [Step 1]
   2. [Step 2]
   3. [Step 3]

   ## Expected Behavior

   [What should happen]

   ## Actual Behavior

   [What actually happens]

   ## Impact

   - Severity: [Critical/High/Medium/Low]
   - Affected Users: [Description]
   - Workaround: [If any]

   ## Root Cause Analysis

   [To be filled during investigation]

   ## Fix Strategy

   [To be filled during planning]

   ## Tasks and Subtasks

   ### Task 1: Investigate Root Cause
   - [ ] Reproduce the bug locally
   - [ ] Identify root cause
   - [ ] Document findings

   ### Task 2: Implement Fix
   - [ ] Write failing test that demonstrates bug
   - [ ] Implement fix
   - [ ] Verify test passes

   ### Task 3: Verify Fix
   - [ ] Test fix manually
   - [ ] Run full test suite
   - [ ] Check for regressions

   ## Test Strategy

   - Regression test: [What to test]
   - Unit tests: [What to test]
   - Integration tests: [What to test]

   ## Definition of Done

   - [ ] Root cause identified and documented
   - [ ] Fix implemented and tested
   - [ ] Regression tests added
   - [ ] Code reviewed and approved
   - [ ] Deployed and verified in staging
   ```

4. **Update Epic TASKS.md**:
   - Add bug fix story with HIGH priority marker

5. **Ask User to Start Now** (optional):
   ```
   Bug fix story created: [X.Y]

   Do you want to start working on this bug fix now?
   - Yes: I'll set it as current story and run /dev
   - No: Story is created and ready when you are
   ```

6. **If Yes, Start Work**:
   - Update status.xml to set as current story
   - Run `/dev` command to begin work

## Agent Delegation

If user wants to start immediately:

```markdown
Task(
  subagent_type="debugger",
  description="Investigate and fix bug: $ARGUMENTS",
  prompt="Investigate the following bug: $ARGUMENTS. Identify root cause, implement fix following TDD, and add regression tests."
)
```

## Recommended Skills

<!-- TODO: Add relevant skills from .claude/skills/ -->

- `tdd-red-green-refactor` - For test-driven bug fixing
- `clean-code-principles` - For quality fixes
- `incident-response-management` - For critical bugs

Use these skills heavily throughout execution to ensure best practices.

**Skill Troubleshooting Authority**: If any referenced skill does not work or any script within the skill does not work, Claude Code has the authority to fix them.

## Arguments

- `$ARGUMENTS`: Bug description

## Examples

```
/fix Login button not working on mobile devices
```

Creates bug fix story for login button issue.

```
/fix
```

Asks user to describe the bug interactively.
