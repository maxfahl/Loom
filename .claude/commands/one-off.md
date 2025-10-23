---
description: Delegate a one-off task to the coordinator agent
model: sonnet
argument-hint: [Describe the one-off task]
---

# /one-off - One-Off Task

## What This Command Does

Delegate a one-off task to the coordinator agent for tasks outside the normal feature development workflow.

## Process

1. **Gather Task Description**:
   - Use `$ARGUMENTS` if provided
   - Otherwise, ask user for task description
   - Clarify scope and expectations

2. **Delegate to Coordinator**:

   **CRITICAL**: The coordinator will automatically read `.claude/AGENTS.md` to access the full agent directory before delegating.

   ```markdown
   Task(
     subagent_type="coordinator",
     description="Complete one-off task: [brief description]",
     prompt="Execute the following one-off task: $ARGUMENTS

     IMPORTANT: Read .claude/AGENTS.md first to understand all 44 available agents.

     This is outside the normal feature development workflow. Complete the task efficiently and report results.

     If the task requires multiple steps or specialized expertise, spawn appropriate sub-agents in parallel based on the agent directory."
   )
   ```

3. **Report Results**:
   - Coordinator completes task
   - Reports back with results
   - User can review and provide feedback

## Use Cases

- Quick code refactoring not tied to a story
- Research tasks
- Fixing a build issue
- Updating dependencies
- Creating a utility script
- Generating reports
- Ad-hoc analysis

## Agent Delegation

```markdown
Task(
  subagent_type="coordinator",
  description="One-off task: $ARGUMENTS",
  prompt="Complete this one-off task: $ARGUMENTS. Use specialized sub-agents if needed. Report results when complete."
)
```

## Recommended Skills

<!-- TODO: Add relevant skills from .claude/skills/ -->

Skills depend on the task type. Coordinator will select appropriate skills.

**Skill Troubleshooting Authority**: If any referenced skill does not work or any script within the skill does not work, Claude Code has the authority to fix them.

## Arguments

- `$ARGUMENTS`: Description of the one-off task

## Examples

```
/one-off Update all npm dependencies
```

Delegates dependency update task to coordinator.

```
/one-off Refactor the authentication module to use async/await
```

Delegates refactoring task.

```
/one-off Generate a performance report for the API
```

Delegates report generation.

```
/one-off
```

Asks user to describe the task interactively.
