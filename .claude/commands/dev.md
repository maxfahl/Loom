---
description: Continue development on current task with automatic task tracking
model: sonnet
---

# /dev - Continue Development

## What This Command Does

Resume development following configured autonomy level. Behavior adapts based on `/yolo` settings.

## Process

**Step 0: Read YOLO Configuration**:

- Read `docs/development/status.xml` for active feature
- Check `<autonomy-level>` (manual/balanced/story/epic/custom)
- Read breakpoint configuration
- Determine execution mode based on autonomy level

**Step 0.5: Query AML for Context** (Optional - Only if AML is Enabled):

First, check if AML is enabled by reading `docs/development/status.xml` and looking for `<aml enabled="true">`.

**If AML is enabled**:

Before starting development, query AML to load learned patterns and avoid known pitfalls:

```typescript
// Query for similar story patterns
const storyPatterns = await aml.queryPatterns('coordinator', {
  type: 'story-completion',
  context: {
    storyType: currentStory.type,
    framework: project.framework,
    complexity: currentStory.complexity
  },
  minConfidence: 0.7,
  limit: 5,
  sortBy: 'weight'
});

// Query for known issues in this feature area
const knownIssues = await aml.querySolutions('coordinator', {
  context: {
    feature: currentFeature.name,
    framework: project.framework
  },
  limit: 10
});

// Query for optimal delegation patterns
const delegationPatterns = await aml.queryDecisions('coordinator', {
  type: 'agent-delegation',
  context: {
    storyComplexity: currentStory.complexity,
    taskTypes: currentStory.taskTypes
  },
  limit: 3
});
```

**Apply Learned Intelligence**:
- Use proven TDD workflows for this story type (e.g., 95% success rate for "auth-feature" stories)
- Avoid known pitfalls from past similar stories
- Optimize delegation based on historical agent performance
- Predict time estimates based on similar completed stories
- Choose optimal YOLO mode breakpoints based on story complexity

**If AML is disabled**:
- Skip this step entirely and proceed to Step 1

**Step 1: Read Current Context**:

- Read `<current-story>` value (e.g., "1.2")
- Read story file at `docs/development/features/[feature]/epics/[epic]/stories/[current-story].md`
- Load AML-recommended approaches for current story type
- Check AML for estimation accuracy (compare planned vs actual for similar stories)

**Step 2: Determine Execution Mode**:

- **MANUAL Mode**: Interactive work, stop at all breakpoints (A, B, C, D)
- **BALANCED Mode**: Semi-autonomous, stop at B (before commit) and C (between stories)
- **STORY Mode**: Spawn coordinator agent to complete entire story, stop at C
- **EPIC Mode**: Spawn coordinator agent to complete entire epic, stop at D
- **CUSTOM Mode**: Follow user-defined stopping conditions

**Step 3: Execute Based on Mode**:

_For MANUAL Mode (Fully Interactive)_:

1. **Query AML for task-specific patterns**: Before each task, check AML for similar task solutions
2. Check for Review Tasks FIRST (priority: Fix > Improvement > Nit)
3. If review tasks exist, work on those before regular tasks
4. Work on Regular Tasks from "## Tasks and Subtasks"
5. **Apply learned TDD patterns**: Use AML's recommended test-first approaches for this component type
6. Check off subtasks as completed (`[ ]` → `[x]`)
7. **Record task outcomes**: After each task, record what worked/didn't work
8. Update story status to "Waiting For Review" when all tasks done
9. Follow TDD: 🔴 RED → 🟢 GREEN → 🔵 REFACTOR → ✅ REVIEW → 📊 TEST → 📝 COMMIT
10. Stop at all breakpoints (A, B, C, D)

_For BALANCED Mode (Semi-Autonomous)_:

1. **Load AML workflow optimizations**: Query best practices for semi-autonomous story completion
2. Check for Review Tasks FIRST (priority: Fix > Improvement > Nit)
3. Work through tasks interactively with user guidance
4. **Apply learned delegation patterns**: Delegate subtasks to agents based on historical success rates
5. Check off subtasks as completed (`[ ]` → `[x]`)
6. **Track phase timings**: Record how long each phase takes for future estimation
7. Update story status to "Waiting For Review" when all tasks done
8. Follow TDD: 🔴 RED → 🟢 GREEN → 🔵 REFACTOR → ✅ REVIEW → 📊 TEST → 📝 COMMIT
9. Stop at breakpoints B (before commit) and C (between stories)

_For STORY/EPIC/CUSTOM Modes (Autonomous)_:

- **Spawn coordinator agent** using Task tool
- Coordinator executes **9-phase autonomous workflow**:
  - **Phase 0**: Initialization - Read project state, analyze story readiness
  - **Phase 1**: Pre-Development - Research, docs, architecture (parallel)
  - **Phase 2**: TDD Red - Write failing tests (parallel by type: unit/integration/E2E)
  - **Phase 3**: TDD Green - Implement code (parallel by layer: frontend/backend/mobile)
  - **Phase 4**: TDD Refactor - Clean up code while tests stay green
  - **Phase 5**: Review - Run all reviews in parallel (code/security/design)
  - **Phase 6**: Review Loop - Fix issues if found, loop until "Done"
  - **Phase 7**: Final Verification - Tests, coverage, documentation
  - **Phase 8**: Commit - Conventional commits (if breakpoint B allows)
  - **Phase 9**: Story Loop - Continue to next story/epic (if breakpoints allow)
- Coordinator **maximizes parallelization** (60-80% time savings)
- Coordinator **updates story file** after each phase
- Coordinator **stops at configured breakpoints**

**Step 4: Record Learning Outcomes** (Optional - Only if AML is Enabled):

First, check if AML is enabled by reading `docs/development/status.xml` and looking for `<aml enabled="true">`.

**If AML is enabled**:

After completing work (story/task/phase), record outcomes to improve future executions:

```typescript
// Calculate execution metrics
const executionMetrics = {
  startTime: taskStartTime,
  endTime: Date.now(),
  timeTakenMs: Date.now() - taskStartTime,
  tasksCompleted: completedTaskCount,
  testsAdded: testCount,
  testCoverage: coveragePercent,
  reviewFindings: reviewFindingCount,
  linesChanged: diffStats.total
};

// Record pattern usage outcome
if (appliedPatterns.length > 0) {
  for (const pattern of appliedPatterns) {
    await aml.recordPatternUsage('coordinator', {
      patternId: pattern.id,
      success: allTestsPassed && reviewPassed,
      timeSavedMs: pattern.estimatedTimeSaving,
      errorsPrevented: pattern.issuesAvoided,
      context: {
        storyType: currentStory.type,
        complexity: currentStory.complexity
      }
    });
  }
}

// Record new pattern if discovered
if (discoveredNovelApproach) {
  await aml.recordPattern('coordinator', {
    type: 'workflow-optimization',
    context: {
      storyType: currentStory.type,
      framework: project.framework,
      yoloMode: autonomyLevel
    },
    approach: {
      technique: novelApproach.name,
      codeTemplate: novelApproach.template,
      rationale: novelApproach.reason
    },
    conditions: {
      whenApplicable: novelApproach.applicability,
      whenNotApplicable: novelApproach.limitations
    },
    tags: ['workflow', 'tdd', currentStory.type]
  });
}

// Record delegation decisions (CRITICAL for learning)
if (delegatedToAgents.length > 0) {
  await aml.recordDecision('coordinator', {
    type: 'agent-delegation',
    question: `Which agents for ${currentStory.type} story?`,
    context: {
      storyComplexity: currentStory.complexity,
      taskTypes: currentStory.taskTypes,
      framework: project.framework
    },
    chosenOption: delegatedToAgents.map(a => a.name).join(', '),
    alternativesConsidered: consideredAgents.map(a => a.name),
    decisionFactors: {
      primary: ['agent-expertise', 'historical-success-rate'],
      secondary: ['availability', 'specialization-match']
    },
    outcome: {
      successMetrics: {
        taskCompletionRate: completedCount / totalCount,
        averageQuality: avgQualityScore,
        timeEfficiency: actualTime / estimatedTime
      },
      wouldRepeat: allTasksSucceeded
    }
  });
}

// Record story completion metrics for future estimation
await aml.recordPattern('coordinator', {
  type: 'story-estimation',
  context: {
    storyType: currentStory.type,
    estimatedComplexity: currentStory.estimatedComplexity,
    taskCount: currentStory.tasks.length
  },
  approach: {
    technique: 'actual-timing-data',
    metrics: executionMetrics
  },
  tags: ['estimation', 'metrics']
});
```

**Learning Outcomes Tracked**:
- Which TDD patterns worked best for component types
- Optimal agent delegation by story type
- Accurate time estimates based on historical data
- Common pitfalls and their solutions
- Workflow optimizations discovered during execution

**If AML is disabled**:
- Skip this step entirely and proceed to next task

**TDD Variations**:

- **Fully Enforced**: "Follow TDD Red-Green-Refactor strictly. Write failing test FIRST, then implement."
- **Recommended**: "Follow TDD Red-Green-Refactor when possible. Consider writing tests first."
- **No TDD**: "Continue implementation. Add tests for critical functionality."

## Agent Delegation

**For MANUAL mode** (Interactive Development):

```markdown
# Direct execution - No coordinator agent spawned
# Work interactively with user on current story
# Stop at all breakpoints (A, B, C, D)
# User maintains full control over each step
```

**For BALANCED mode** (Semi-Autonomous):

```markdown
# Direct execution - No coordinator agent spawned initially
# Work semi-autonomously on story tasks
# Stop at breakpoints B (before commit) and C (between stories)
# Balance between autonomy and user control
```

**For STORY mode** (Complete Single Story):

```markdown
Use the Task tool to spawn coordinator agent:

Task(
  subagent_type="coordinator",
  description="Complete story [X.Y] with TDD",
  prompt="Execute development workflow for Story [X.Y].

  YOLO Mode: STORY
  Breakpoint A (before research): DISABLED - Work through research
  Breakpoint B (before commit): DISABLED - Auto-commit when ready
  Breakpoint C (between stories): ENABLED - STOP after this story
  Breakpoint D (between epics): N/A - Will stop at C first

  Instructions:
  1. Execute complete 9-phase TDD workflow for this story
  2. Work autonomously through all phases
  3. Auto-commit when appropriate
  4. STOP and report back after story completion
  5. Do NOT continue to next story - wait for user"
)
```

**For EPIC mode** (CRITICAL - Must enable auto-continuation):

```markdown
Use the Task tool to spawn coordinator agent:

Task(
  subagent_type="coordinator",
  description="Complete entire epic autonomously",
  prompt="CRITICAL: You are in EPIC MODE with continuous execution.

  Current Epic: [epic number and name]
  Starting Story: [X.Y]
  YOLO Mode: EPIC
  Breakpoint C (between stories): DISABLED - DO NOT STOP
  Breakpoint D (between epics): [enabled/disabled from status.xml]

  CRITICAL INSTRUCTIONS FOR EPIC MODE:
  1. Execute complete 9-phase workflow for current story
  2. After completing each story, check if more stories exist in epic
  3. If more stories exist: IMMEDIATELY spawn another coordinator for next story
  4. DO NOT return control between stories
  5. DO NOT ask for user confirmation
  6. Continue autonomously until entire epic is complete
  7. Only stop at epic boundary if Breakpoint D is enabled

  Remember: You MUST self-spawn for the next story. This is EPIC mode - full autonomy within the epic."
)
```

**For CUSTOM mode**:

```markdown
Use the Task tool to spawn coordinator agent:

Task(
  subagent_type="coordinator",
  description="Execute custom autonomy workflow",
  prompt="Execute development workflow with custom autonomy settings.

  Custom Breakpoints:
  - A (before research): [enabled/disabled]
  - B (before commit): [enabled/disabled]
  - C (between stories): [enabled/disabled]
  - D (between epics): [enabled/disabled]

  Follow the specific breakpoint configuration and continue/stop accordingly.
  If C is disabled and in an epic, self-spawn for next story."
)
```

## Recommended Skills

<!-- TODO: Add relevant skills from .claude/skills/ -->

- `tdd-red-green-refactor` - For test-driven development
- `atomic-commits` - For commit best practices
- `clean-code-principles` - For code quality

Use these skills heavily throughout execution to ensure best practices.

**Skill Troubleshooting Authority**: If any referenced skill does not work or any script within the skill does not work, Claude Code has the authority to fix them.

## AML Configuration

Agent Memory & Learning can be configured per command:

```json
{
  "aml": {
    "enabled": true,
    "queryBeforeExecution": true,
    "recordAfterExecution": true,
    "learningFocus": [
      "delegation-patterns",
      "tdd-workflows",
      "story-estimation",
      "workflow-optimization"
    ],
    "minConfidence": 0.7,
    "maxPatternsToQuery": 5
  }
}
```

**Disable AML for this command**:
Set `aml.enabled: false` in `.loom/memory/config.json` under `commandOverrides.dev`

**What /dev Learns Over Time**:
1. **Delegation Intelligence**: Which agents excel at which story types
2. **Workflow Optimization**: Fastest paths through TDD cycles
3. **Estimation Accuracy**: Actual vs estimated time by story complexity
4. **YOLO Mode Tuning**: Optimal breakpoint configurations
5. **Error Prevention**: Common pitfalls and how to avoid them
6. **Task Decomposition**: Best ways to break down stories
7. **Phase Timing**: Realistic time allocations per TDD phase
8. **Review Readiness**: Patterns that pass review first time

## Arguments

This command takes no arguments. Behavior is determined by YOLO configuration in status.xml.

## Examples

```
/dev
```

Reads status.xml, determines mode, and continues development accordingly.
