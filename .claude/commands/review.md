---
description: Comprehensive review of uncommitted changes with automatic status updates
model: sonnet
---

# /review - Comprehensive Code Review

## What This Command Does

Full code review using 7-phase hierarchical framework with automatic Review Tasks creation and story status updates.

## Process

1. **Read Current Context**:
   - Read `status.xml` for active feature
   - Read `<current-story>` value
   - Read story file at `docs/development/features/[feature]/epics/[epic]/stories/[current-story].md`
   - Read acceptance criteria and requirements from story

**Step 1.5: Query AML for Review Patterns** (NEW - Agent Memory & Learning):

Before executing the review, query AML to load common review patterns and avoid missing known issues:

```typescript
// Query for common review findings in this code type
const reviewPatterns = await aml.queryPatterns('code-reviewer-pro', {
  type: 'review-finding',
  context: {
    fileTypes: changedFiles.map(f => f.extension),
    framework: project.framework,
    componentType: storyContext.componentType
  },
  minConfidence: 0.7,
  limit: 10,
  sortBy: 'frequency'
});

// Query for security patterns relevant to changed code
const securityPatterns = await aml.querySolutions('security-reviewer', {
  errorType: 'security-vulnerability',
  context: {
    framework: project.framework,
    changeTypes: diffStats.changeTypes
  },
  limit: 5
});

// Query for false positive patterns to avoid
const falsePositives = await aml.queryPatterns('code-reviewer-pro', {
  type: 'false-positive',
  context: {
    framework: project.framework,
    reviewPhase: 'automated'
  },
  limit: 5
});
```

**Apply Learned Intelligence**:
- Prioritize review areas based on historical finding frequency
- Apply known security patterns for this framework (e.g., 98% accuracy for "SQL injection in ORM")
- Skip false positive checks that wasted time in past reviews
- Use proven review checklists for this component type
- Predict review time based on similar code change sizes

2. **Embed Git Diff for Full Context**:

   Gather ALL changes upfront:

   ```bash
   # Git status
   git status

   # Files modified
   git diff --name-only origin/HEAD...

   # Commits
   git log --no-decorate origin/HEAD...

   # Full diff content
   git diff --merge-base origin/HEAD
   ```

   **Why**: Embedding full context upfront prevents repeated file reads and improves review quality.

3. **Review Code Using 7-Phase Framework**:

   Spawn `code-reviewer` agent with 7-phase hierarchical framework:

   ```markdown
   Task(
     subagent_type="code-reviewer",
     description="Review uncommitted changes using 7-phase framework",
     prompt="Execute comprehensive code review using the 7-phase hierarchical framework. Review all uncommitted changes and check against story acceptance criteria."
   )
   ```

   **Phases**:
   1. **Architectural Design & Integrity** (Critical)
   2. **Functionality & Correctness** (Critical)
   3. **Security** (Non-Negotiable)
   4. **Maintainability & Readability** (High Priority)
   5. **Testing Strategy & Robustness** (High Priority)
   6. **Performance & Scalability** (Important)
   7. **Dependencies & Documentation** (Important)

   **Also check**:
   - Story acceptance criteria are met
   - All tasks are completed
   - TDD requirements followed (tests written first, 80%+ coverage)
   - Component library priority order (Kibo UI → Blocks.so → ReUI → shadcn/ui)

4. **Apply Triage Matrix**:

   Categorize findings:
   - **Blocker**: Must fix before merge (security, architectural regression)
   - **Improvement**: Strong recommendation for better implementation
   - **Nit**: Minor polish, optional

   **Philosophy**: "Net Positive > Perfection" - Merge if it improves code health, even if not perfect

5. **Handle Review Findings**:

   **If Issues Found**:
   - Create/Update "## Review Tasks" section in story file
   - Add tasks with priority prefix:
     - `- [ ] Fix: [Blocking issue description] (file:line)`
     - `- [ ] Improvement: [High priority improvement] (file:line)`
     - `- [ ] Nit: [Low priority polish] (file:line)`
   - Update story **Status** to "In Progress" (back from "Waiting For Review")
   - Update **Last Updated** timestamp
   - Report issues to user with clear actionable feedback

   **If No Issues (Approved)**:
   - Update story **Status** to "Done"
   - Update **Last Updated** timestamp
   - Add completion note to status.xml
   - Congratulate user on completing the story

**Final Step: Record Review Patterns to AML** (NEW - Agent Memory & Learning):

After completing the review, record outcomes to improve future reviews:

```typescript
// Calculate review metrics
const reviewMetrics = {
  startTime: reviewStartTime,
  endTime: Date.now(),
  reviewTimeMs: Date.now() - reviewStartTime,
  findingsCount: {
    blocker: blockerCount,
    improvement: improvementCount,
    nit: nitCount
  },
  linesReviewed: diffStats.totalLines,
  filesReviewed: changedFiles.length,
  approved: noIssuesFound
};

// Record new review patterns discovered
for (const finding of uniqueFindings) {
  await aml.recordPattern('code-reviewer-pro', {
    type: 'review-finding',
    context: {
      fileType: finding.fileType,
      framework: project.framework,
      componentType: finding.componentType,
      reviewPhase: finding.phase
    },
    approach: {
      technique: finding.issuePattern,
      checkMethod: finding.detectionMethod,
      rationale: finding.whyItMatters
    },
    conditions: {
      whenApplicable: finding.applicableContexts,
      whenNotApplicable: finding.falsePositiveContexts
    },
    tags: ['code-review', finding.severity, finding.category]
  });
}

// Record false positives to avoid future noise
for (const falsePositive of identifiedFalsePositives) {
  await aml.recordPattern('code-reviewer-pro', {
    type: 'false-positive',
    context: {
      framework: project.framework,
      tool: falsePositive.tool,
      pattern: falsePositive.pattern
    },
    approach: {
      technique: 'skip-check',
      rationale: falsePositive.reason
    },
    tags: ['false-positive', 'review-optimization']
  });
}

// Record security findings with high priority
for (const securityFinding of securityFindings) {
  await aml.recordSolution('security-reviewer', {
    problem: {
      errorType: 'security-vulnerability',
      errorMessage: securityFinding.vulnerability,
      context: {
        framework: project.framework,
        category: securityFinding.owaspCategory
      }
    },
    solution: {
      rootCause: securityFinding.cause,
      fixApproach: securityFinding.remediation,
      codeFix: securityFinding.exampleFix,
      prevention: securityFinding.preventionGuidance
    },
    effectiveness: {
      worked: true,
      severity: securityFinding.severity
    }
  });
}

// Record review performance for estimation
await aml.recordPattern('code-reviewer-pro', {
  type: 'review-estimation',
  context: {
    linesChanged: diffStats.totalLines,
    filesChanged: changedFiles.length,
    complexity: estimatedComplexity,
    storyType: currentStory.type
  },
  approach: {
    technique: 'actual-timing-data',
    metrics: reviewMetrics
  },
  tags: ['estimation', 'performance']
});
```

**Learning Outcomes Tracked**:
- Common review findings by file type and framework
- Security patterns and vulnerabilities specific to this codebase
- False positive patterns to skip in future reviews
- Review time estimates by code change size
- Most effective review techniques per component type
- Review quality metrics (findings per 100 lines of code)

## Agent Delegation

```markdown
Task(
  subagent_type="code-reviewer",
  description="Review uncommitted changes",
  prompt="Execute comprehensive code review using the 7-phase hierarchical framework. Apply triage matrix (Blocker/Improvement/Nit). Check story acceptance criteria. Report findings with file:line references."
)
```

## Recommended Skills

<!-- TODO: Add relevant skills from .claude/skills/ -->

- `code-refactoring-techniques` - For code quality assessment
- `clean-code-principles` - For maintainability review
- `owasp-top-10` - For security review
- `solid-principles` - For architectural review

Use these skills heavily throughout execution to ensure best practices.

**Skill Troubleshooting Authority**: If any referenced skill does not work or any script within the skill does not work, Claude Code has the authority to fix them.

## Arguments

This command takes no arguments. Reviews all uncommitted changes.

## Examples

```
/review
```

Executes comprehensive code review and updates story status based on findings.
