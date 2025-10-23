---
description: Plan next feature or task with detailed breakdown
model: sonnet
argument-hint: [feature name or task]
---

# /plan - Plan Feature or Task

## What This Command Does

Create detailed implementation plan with TDD breakdown and task organization.

## Process

**Step 0: Query AML for Planning Patterns** (Optional - Only if AML is Enabled):

First, check if AML is enabled by reading `docs/development/status.xml` and looking for `<aml enabled="true">`.

**If AML is enabled**:

Before creating the plan, query AML for successful planning patterns and estimation data:

```typescript
// Query for planning patterns for similar features
const planningPatterns = await aml.queryPatterns('coordinator', {
  type: 'feature-planning',
  context: {
    featureType: inferredFeatureType,
    framework: project.framework,
    complexity: estimatedComplexity
  },
  minConfidence: 0.7,
  limit: 5,
  sortBy: 'success_rate'
});

// Query for estimation accuracy from past epics
const estimationPatterns = await aml.queryPatterns('coordinator', {
  type: 'story-estimation',
  context: {
    featureType: inferredFeatureType,
    teamSize: team.size,
    framework: project.framework
  },
  limit: 10,
  sortBy: 'confidence'
});

// Query for task decomposition strategies
const decompositionPatterns = await aml.queryDecisions('coordinator', {
  type: 'task-breakdown',
  context: {
    featureComplexity: estimatedComplexity,
    featureType: inferredFeatureType
  },
  limit: 3
});

// Query for risks encountered in similar features
const knownRisks = await aml.querySolutions('coordinator', {
  context: {
    featureType: inferredFeatureType,
    framework: project.framework
  },
  limit: 5
});
```

**Apply Learned Intelligence**:
- Use proven task breakdown structures for this feature type (e.g., 92% success rate)
- Apply accurate time estimates based on historical data (avg: actual vs planned = 1.2x)
- Identify known risks from similar features completed previously
- Optimize phase ordering based on successful past plans
- Predict story count and epic duration

**If AML is disabled**:
- Skip this step and proceed to Step 1

1. **Read Agent Directory** (CRITICAL):
   - Read `.claude/AGENTS.md` to understand all available agents
   - Identify which agents are needed for this plan

2. **Understand Requirements**:
   - If feature name provided in `$ARGUMENTS`, use that
   - Otherwise, ask user for feature/task description
   - Clarify scope, goals, and constraints

3. **Research & Analysis**:
   - Use researcher agent if needed for best practices
   - Review existing codebase structure
   - Identify dependencies and integration points

4. **Create Implementation Plan**:
   - Break down into logical phases
   - For each phase, create TDD breakdown:
     - 🔴 RED: Write failing tests first
     - 🟢 GREEN: Implement minimum to pass tests
     - 🔵 REFACTOR: Clean up and optimize
     - ✅ REVIEW: Code review checklist
     - 📊 TEST: Verify coverage and quality
     - 📝 COMMIT: Atomic commits

5. **Identify Tasks & Agent Assignments**:
   - Reference `.claude/AGENTS.md` to assign appropriate agents to each task
   - Create specific, actionable tasks
   - Estimate complexity (S/M/L/XL)
   - Identify dependencies between tasks
   - Suggest task order

5. **Output Plan**:
   ```markdown
   # Implementation Plan: [Feature/Task Name]

   ## Overview
   [Brief description and goals]

   ## Phases

   ### Phase 1: [Phase Name]
   **Goal**: [What this phase accomplishes]

   **Tasks**:
   1. 🔴 RED: Write tests for [X]
   2. 🟢 GREEN: Implement [X]
   3. 🔵 REFACTOR: Optimize [X]
   4. ✅ REVIEW: Review against [criteria]
   5. 📊 TEST: Verify [coverage/quality]
   6. 📝 COMMIT: Atomic commit for [X]

   **Complexity**: [S/M/L/XL]
   **Dependencies**: [List dependencies]

   ### Phase 2: [Phase Name]
   ...

   ## Risks & Mitigation
   - Risk: [Description]
     Mitigation: [How to address]

   ## Next Steps
   [Immediate actions to take]
   ```

**Final Step: Record Planning to AML** (Optional - Only if AML is Enabled):

First, check if AML is enabled by reading `docs/development/status.xml` and looking for `<aml enabled="true">`.

**If AML is enabled**:

After creating the plan, record the planning decisions and estimations for future learning:

```typescript
// Calculate planning metrics
const planningMetrics = {
  timestamp: Date.now(),
  featureName: featureName,
  phaseCount: phases.length,
  totalTaskCount: tasks.length,
  estimatedComplexity: complexity,
  estimatedDuration: estimatedHours,
  risksIdentified: risks.length
};

// Record feature planning pattern
await aml.recordPattern('coordinator', {
  type: 'feature-planning',
  context: {
    featureType: inferredFeatureType,
    framework: project.framework,
    complexity: complexity,
    phaseCount: phases.length
  },
  approach: {
    technique: 'tdd-phase-breakdown',
    codeTemplate: planTemplate,
    rationale: 'Proven TDD workflow with parallel execution opportunities'
  },
  conditions: {
    whenApplicable: ['greenfield-features', 'refactoring', 'enhancements'],
    whenNotApplicable: ['hotfixes', 'trivial-changes']
  },
  tags: ['planning', 'tdd', inferredFeatureType, complexity]
});

// Record task breakdown decision
await aml.recordDecision('coordinator', {
  type: 'task-breakdown',
  question: `How to decompose ${featureName} feature?`,
  context: {
    featureComplexity: complexity,
    featureType: inferredFeatureType,
    framework: project.framework
  },
  chosenOption: `${phases.length} phases, ${tasks.length} tasks`,
  alternativesConsidered: alternativeBreakdowns,
  decisionFactors: {
    primary: ['testability', 'parallelization', 'dependencies'],
    secondary: ['team-capacity', 'risk-mitigation']
  },
  outcome: {
    successMetrics: {
      planClarity: 1.0, // Will be updated based on execution
      estimationAccuracy: 0.0 // Will be updated when feature completes
    },
    wouldRepeat: true // Will be updated based on outcome
  }
});

// Record initial estimation (to be updated with actual data)
await aml.recordPattern('coordinator', {
  type: 'story-estimation',
  context: {
    featureType: inferredFeatureType,
    taskCount: tasks.length,
    complexity: complexity,
    framework: project.framework
  },
  approach: {
    technique: 'historical-data-estimation',
    metrics: {
      estimatedHours: estimatedHours,
      estimatedStories: Math.ceil(tasks.length / 3),
      confidenceLevel: 0.7
    }
  },
  tags: ['estimation', 'planning', complexity]
});

// Record identified risks for future reference
for (const risk of identifiedRisks) {
  await aml.recordSolution('coordinator', {
    problem: {
      errorType: 'planning-risk',
      errorMessage: risk.description,
      context: {
        featureType: inferredFeatureType,
        riskCategory: risk.category
      }
    },
    solution: {
      rootCause: risk.source,
      fixApproach: 'proactive-mitigation',
      codeFix: risk.mitigation,
      prevention: risk.preventionStrategy
    },
    effectiveness: {
      worked: false, // Will be updated during execution
      severity: risk.severity
    }
  });
}
```

**Learning Outcomes Tracked**:
- Effective task breakdown patterns by feature type
- Estimation accuracy (planned vs actual) by complexity
- Risk prediction accuracy for different feature types
- Optimal phase ordering and parallelization strategies
- Agent assignment success rates by task type
- Planning time vs feature completion time correlation

**If AML is disabled**:
- Skip this step entirely

## Agent Delegation

**CRITICAL**: Always read `.claude/AGENTS.md` first to choose the right agent!

Example delegations based on task type:

```markdown
# For research
Task(
  subagent_type="<choose from AGENTS.md>",
  description="Research best practices for $ARGUMENTS",
  prompt="Research current best practices..."
)

# For architecture
Task(
  subagent_type="cloud-architect",
  description="Review architecture for $ARGUMENTS",
  prompt="Review proposed architecture..."
)

# For technology-specific planning
Task(
  subagent_type="nextjs-pro",  # or react-pro, python-pro, etc from AGENTS.md
  description="Plan Next.js implementation for $ARGUMENTS",
  prompt="Plan Next.js-specific implementation..."
)
```

## Recommended Skills

<!-- TODO: Add relevant skills from .claude/skills/ -->

- `tdd-red-green-refactor` - For TDD planning
- `clean-architecture` - For architecture planning
- `requirements-engineering` - For requirements analysis

Use these skills heavily throughout execution to ensure best practices.

**Skill Troubleshooting Authority**: If any referenced skill does not work or any script within the skill does not work, Claude Code has the authority to fix them.

## Arguments

- `$ARGUMENTS`: Feature name or task description to plan

## Examples

```
/plan user authentication
```

Creates implementation plan for user authentication feature.

```
/plan
```

Asks user for feature/task description interactively.
