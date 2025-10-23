---
description: Create the next user story for the current epic
model: sonnet
---

# /create-story - Create User Story

## What This Command Does

Create the next user story within the current epic with proper structure and tasks.

## Process

**Step 0: Query AML for Story Patterns** (NEW - Agent Memory & Learning):

Before creating the story, query AML for successful story structure patterns:

```typescript
// Query for story structure patterns
const storyPatterns = await aml.queryPatterns('coordinator', {
  type: 'story-structure',
  context: {
    epicType: currentEpic.type,
    framework: project.framework,
    complexity: estimatedComplexity
  },
  minConfidence: 0.7,
  limit: 5,
  sortBy: 'success_rate'
});

// Query for acceptance criteria patterns
const acceptanceCriteriaPatterns = await aml.queryPatterns('coordinator', {
  type: 'acceptance-criteria',
  context: {
    storyType: inferredStoryType,
    framework: project.framework
  },
  limit: 5
});

// Query for story quality metrics
const qualityMetrics = await aml.queryPatterns('coordinator', {
  type: 'story-quality',
  context: {
    epicType: currentEpic.type
  },
  limit: 10,
  sortBy: 'completion_rate'
});
```

**Apply Learned Intelligence**:
- Use proven story structures for this epic type (e.g., 94% completion rate)
- Apply effective acceptance criteria templates
- Predict story completion time based on similar stories
- Optimize task breakdown based on historical data
- Identify common story quality issues to avoid

1. **Read Current Context**:
   - Read status.xml for current feature and epic
   - Read epic DESCRIPTION.md for goals and context
   - Read existing stories to understand numbering
   - Load AML-recommended story structures

2. **Determine Story Number**:
   - Find highest story number in current epic
   - Increment by 1 (e.g., if 1.2 exists, next is 1.3)

3. **Gather Story Details**:
   - Ask user for story description
   - Clarify acceptance criteria
   - Understand dependencies
   - Estimate complexity (S/M/L/XL)

4. **Create Story File** (e.g., `1.3.md`):

   ```markdown
   # Story 1.3: [Story Title]

   **Status**: To Do
   **Priority**: [High/Medium/Low]
   **Complexity**: [S/M/L/XL]
   **Created**: [Date]
   **Last Updated**: [Date]

   ## Description

   As a [user type], I want [goal] so that [benefit].

   ## Acceptance Criteria

   - [ ] Criterion 1
   - [ ] Criterion 2
   - [ ] Criterion 3

   ## Technical Notes

   [Any technical considerations or constraints]

   ## Tasks and Subtasks

   ### Task 1: [Task Name]
   - [ ] Subtask 1.1
   - [ ] Subtask 1.2

   ### Task 2: [Task Name]
   - [ ] Subtask 2.1
   - [ ] Subtask 2.2

   ## Dependencies

   - Story 1.2: [Description]

   ## Test Strategy

   - Unit tests: [What to test]
   - Integration tests: [What to test]
   - E2E tests: [What to test]

   ## Definition of Done

   - [ ] All acceptance criteria met
   - [ ] Tests written and passing (80%+ coverage)
   - [ ] Code reviewed and approved
   - [ ] Documentation updated
   - [ ] Deployed to staging
   ```

5. **Update Epic TASKS.md**:
   - Add new story to epic task list

6. **Update status.xml** (optional):
   - If user wants to start immediately, set as current story

**Final Step: Record Story Creation to AML** (NEW - Agent Memory & Learning):

After creating the story, record the story structure and quality for future improvement:

```typescript
// Calculate story creation metrics
const storyMetrics = {
  timestamp: Date.now(),
  storyNumber: storyNumber,
  complexity: complexity,
  taskCount: tasks.length,
  acceptanceCriteriaCount: acceptanceCriteria.length,
  dependencyCount: dependencies.length,
  estimatedHours: estimatedHours
};

// Record story structure pattern
await aml.recordPattern('coordinator', {
  type: 'story-structure',
  context: {
    epicType: currentEpic.type,
    storyType: inferredStoryType,
    framework: project.framework,
    complexity: complexity
  },
  approach: {
    technique: 'user-story-format',
    codeTemplate: storyTemplate,
    rationale: 'Proven story structure with clear AC and tasks'
  },
  conditions: {
    whenApplicable: ['feature-work', 'enhancements', 'new-capabilities'],
    whenNotApplicable: ['hotfixes', 'technical-debt']
  },
  tags: ['story-creation', inferredStoryType, complexity]
});

// Record acceptance criteria pattern
await aml.recordPattern('coordinator', {
  type: 'acceptance-criteria',
  context: {
    storyType: inferredStoryType,
    framework: project.framework,
    featureArea: currentFeature.name
  },
  approach: {
    technique: 'testable-criteria',
    codeTemplate: acceptanceCriteriaTemplate,
    rationale: 'Clear, testable acceptance criteria'
  },
  conditions: {
    whenApplicable: [inferredStoryType, 'user-facing-features'],
    whenNotApplicable: ['internal-refactoring']
  },
  tags: ['acceptance-criteria', inferredStoryType]
});

// Record story quality baseline (to be updated upon completion)
await aml.recordPattern('coordinator', {
  type: 'story-quality',
  context: {
    epicType: currentEpic.type,
    storyType: inferredStoryType,
    complexity: complexity,
    taskCount: tasks.length
  },
  approach: {
    technique: 'quality-metrics-tracking',
    metrics: {
      completionRate: 0, // Will be updated when story completes
      timeToComplete: 0, // Will be updated when story completes
      reviewIterations: 0, // Will be updated during review
      testCoverage: 0, // Will be updated when tests written
      qualityScore: 0 // Will be calculated at completion
    }
  },
  tags: ['story-quality', 'tracking', complexity]
});

// Record task breakdown decision
await aml.recordDecision('coordinator', {
  type: 'story-task-breakdown',
  question: `How to break down story ${storyNumber}?`,
  context: {
    storyComplexity: complexity,
    storyType: inferredStoryType,
    epicGoal: currentEpic.goal
  },
  chosenOption: `${tasks.length} tasks with ${subtaskCount} subtasks`,
  alternativesConsidered: alternativeBreakdowns,
  decisionFactors: {
    primary: ['testability', 'clear-ownership', 'incremental-value'],
    secondary: ['parallelization', 'dependencies']
  },
  outcome: {
    successMetrics: {
      taskClarity: 1.0, // Will be updated based on execution feedback
      completionRate: 0, // Will be updated when story completes
      estimationAccuracy: 0 // Actual time / estimated time
    },
    wouldRepeat: true // Will be updated based on outcome
  }
});
```

**Learning Outcomes Tracked**:
- Effective story structure patterns by epic type
- High-quality acceptance criteria templates
- Optimal task breakdown strategies
- Story completion rates by complexity
- Estimation accuracy (planned vs actual) by story type
- Common story quality issues and how to avoid them

## Recommended Skills

<!-- TODO: Add relevant skills from .claude/skills/ -->

- `agile-methodologies` - For story structure
- `requirements-engineering` - For acceptance criteria
- `tdd-red-green-refactor` - For test strategy

Use these skills heavily throughout execution to ensure best practices.

**Skill Troubleshooting Authority**: If any referenced skill does not work or any script within the skill does not work, Claude Code has the authority to fix them.

## Arguments

This command takes no arguments. Creates next story in current epic.

## Examples

```
/create-story
```

Creates next user story in current epic.
