---
description: Plan next feature or task with detailed breakdown
model: sonnet
argument-hint: [feature name or task]
---

# /plan - Plan Feature or Task

## What This Command Does

Create detailed implementation plan with TDD breakdown and task organization.

## Process

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
