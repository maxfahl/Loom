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

**Step 1: Read Current Context**:
- Read `<current-story>` value (e.g., "1.2")
- Read story file at `docs/development/features/[feature]/epics/[epic]/stories/[current-story].md`

**Step 2: Determine Execution Mode**:

- **MANUAL Mode**: Interactive work, stop at all breakpoints (A, B, C, D)
- **BALANCED Mode**: Semi-autonomous, stop at B (before commit) and C (between stories)
- **STORY Mode**: Spawn coordinator agent to complete entire story, stop at C
- **EPIC Mode**: Spawn coordinator agent to complete entire epic, stop at D
- **CUSTOM Mode**: Follow user-defined stopping conditions

**Step 3: Execute Based on Mode**:

*For MANUAL/BALANCED (Interactive/Semi-Autonomous)*:
1. Check for Review Tasks (PRIORITY - Fix > Improvement > Nit)
2. Work on Regular Tasks from "## Tasks and Subtasks"
3. Check off subtasks as completed (`[ ]` → `[x]`)
4. Update story status when complete
5. Follow TDD: 🔴 RED → 🟢 GREEN → 🔵 REFACTOR → ✅ REVIEW → 📊 TEST → 📝 COMMIT
6. Stop at enabled breakpoints

*For STORY/EPIC/CUSTOM (Autonomous)*:
- Spawn coordinator agent (Task tool)
- Agent executes complete TDD cycle with parallel sub-agents
- Agent checks off tasks in story file
- Agent updates story status
- Agent stops at configured breakpoints

**TDD Variations**:
- **Fully Enforced**: "Follow TDD Red-Green-Refactor strictly. Write failing test FIRST, then implement."
- **Recommended**: "Follow TDD Red-Green-Refactor when possible. Consider writing tests first."
- **No TDD**: "Continue implementation. Add tests for critical functionality."

## Agent Delegation

**For STORY/EPIC/CUSTOM modes**:

```markdown
Use the Task tool to spawn coordinator agent:

Task(
  subagent_type="coordinator",
  description="Complete [story/epic] following TDD and YOLO configuration",
  prompt="Execute development workflow for [story/epic details]. Follow configured autonomy level and stop at enabled breakpoints. Execute complete TDD cycle with parallel sub-agents."
)
```

## Recommended Skills

<!-- TODO: Add relevant skills from .claude/skills/ -->

- `tdd-red-green-refactor` - For test-driven development
- `atomic-commits` - For commit best practices
- `clean-code-principles` - For code quality

Use these skills heavily throughout execution to ensure best practices.

**Skill Troubleshooting Authority**: If any referenced skill does not work or any script within the skill does not work, Claude Code has the authority to fix them.

## Arguments

This command takes no arguments. Behavior is determined by YOLO configuration in status.xml.

## Examples

```
/dev
```

Reads status.xml, determines mode, and continues development accordingly.
