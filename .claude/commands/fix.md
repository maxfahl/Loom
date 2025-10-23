---
description: Address a bug by creating a new, high-priority story
model: sonnet
argument-hint: [Describe the bug]
---

# /fix - Fix Bug

## What This Command Does

Create a high-priority story for a bug fix and optionally start working on it immediately.

## Process

**Step 0: Query AML for Bug Solutions** (NEW - Agent Memory & Learning):

Before creating the bug fix story, query AML for similar bug solutions and patterns:

```typescript
// Query for solutions to similar bug signatures
const similarBugSolutions = await aml.querySolutions('debugger', {
  errorType: extractedErrorType,
  errorMessage: bugDescription,
  context: {
    framework: project.framework,
    component: affectedComponent
  },
  limit: 5
});

// Query for error resolution patterns
const errorPatterns = await aml.queryPatterns('debugger', {
  type: 'bug-resolution',
  context: {
    bugCategory: categorizedBug,
    severity: estimatedSeverity,
    framework: project.framework
  },
  minConfidence: 0.6,
  limit: 5,
  sortBy: 'success_rate'
});

// Query for recurring bug families
const recurringBugs = await aml.queryPatterns('debugger', {
  type: 'bug-family',
  context: {
    errorSignature: extractErrorSignature(bugDescription),
    codeArea: affectedComponent
  },
  limit: 3
});
```

**Apply Learned Intelligence**:
- Check if this bug has been seen before (exact match or similar pattern)
- Use proven fix strategies for this bug category (e.g., 95% success rate)
- Identify root cause faster using historical bug patterns
- Apply preventive measures from similar bugs
- Estimate fix time based on bug complexity and historical data

1. **Gather Bug Details**:
   - Use `$ARGUMENTS` if provided
   - Otherwise, ask user for bug description
   - Understand reproduction steps
   - Clarify impact and severity
   - Check AML for similar bugs and suggested fixes

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

**Final Step: Record Bug Fix to AML** (NEW - Agent Memory & Learning):

After successfully fixing the bug (or creating the story), record the bug and solution for future reference:

```typescript
// Calculate bug metrics
const bugMetrics = {
  timestamp: Date.now(),
  bugId: storyNumber,
  severity: severity,
  timeToIdentify: identificationTime,
  impactedUsers: impactEstimate,
  reproduced: wasReproduced
};

// Record bug solution (after fix is implemented)
await aml.recordSolution('debugger', {
  problem: {
    errorType: extractedErrorType,
    errorMessage: bugDescription,
    stackTraceHash: generateStackTraceHash(errorDetails),
    context: {
      framework: project.framework,
      component: affectedComponent,
      severity: severity,
      reproducible: reproductionSteps.length > 0
    }
  },
  solution: {
    rootCause: rootCauseAnalysis,
    fixApproach: fixStrategy,
    codeFix: implementedFix,
    prevention: preventiveMeasures
  },
  effectiveness: {
    worked: true, // Will be updated after verification
    timeToFixMinutes: 0, // Will be updated during fix
    preventedRecurrence: 0, // Will be updated over time
    relatedErrorsFixed: relatedBugs.length
  }
});

// Record bug family pattern if recurring
if (isRecurringBug) {
  await aml.recordPattern('debugger', {
    type: 'bug-family',
    context: {
      errorSignature: extractErrorSignature(bugDescription),
      codeArea: affectedComponent,
      framework: project.framework
    },
    approach: {
      technique: 'pattern-recognition',
      codeTemplate: bugPattern,
      rationale: 'Recurring bug family with common root cause'
    },
    conditions: {
      whenApplicable: bugFamilyTriggers,
      whenNotApplicable: exceptionalCases
    },
    tags: ['bug-family', severity, affectedComponent]
  });
}

// Record bug resolution strategy
await aml.recordDecision('debugger', {
  type: 'bug-fix-strategy',
  question: `How to fix: ${bugDescription}?`,
  context: {
    bugSeverity: severity,
    bugCategory: categorizedBug,
    impactedUsers: impactEstimate,
    framework: project.framework
  },
  chosenOption: fixStrategy,
  alternativesConsidered: consideredApproaches,
  decisionFactors: {
    primary: ['fix-effectiveness', 'risk-of-regression'],
    secondary: ['fix-complexity', 'time-to-fix']
  },
  outcome: {
    successMetrics: {
      bugFixed: false, // Will be updated after fix verification
      noRegressions: false, // Will be updated after testing
      userSatisfaction: 0 // Will be updated based on feedback
    },
    wouldRepeat: true // Will be updated based on outcome
  }
});

// Record prevention pattern
if (preventiveMeasures.length > 0) {
  await aml.recordPattern('debugger', {
    type: 'bug-prevention',
    context: {
      bugCategory: categorizedBug,
      framework: project.framework,
      component: affectedComponent
    },
    approach: {
      technique: 'preventive-measure',
      codeTemplate: preventiveMeasureCode,
      rationale: 'Prevent recurrence of this bug family'
    },
    conditions: {
      whenApplicable: ['similar-components', 'new-features'],
      whenNotApplicable: ['legacy-code', 'deprecated-features']
    },
    tags: ['prevention', 'proactive', bugCategory]
  });
}
```

**Learning Outcomes Tracked**:
- Bug solutions by error type and framework
- Bug family patterns (recurring bugs with common root cause)
- Effective fix strategies by bug category
- Time to fix by bug severity and complexity
- Prevention patterns to avoid similar bugs
- Bug recurrence rates after fixes

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
