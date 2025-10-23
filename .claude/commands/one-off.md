---
description: Delegate a one-off task to the coordinator agent
allowed-tools: Task
model: claude-sonnet-4-5
argument-hint: [Describe the one-off task you want to accomplish]
---

# /one-off - Delegate One-Off Task

**Purpose**: Delegates a general-purpose task to the coordinator agent for autonomous execution, emphasizing parallelization and the use of Claude Code Skills.

## Process

1. **Analyze the Request**: Break down the user's request into logical sub-tasks.
2. **Identify Sub-Agents**: Determine the best specialized sub-agents to handle each sub-task.
3. **Delegate in Parallel**: Spawn the required sub-agents to work on the sub-tasks simultaneously whenever possible.
4. **Instruct Sub-Agents**: Provide each sub-agent with a clear, detailed prompt that includes all necessary context and instructs them to use Claude Code Skills.
5. **Synthesize Results**: Gather results from sub-agents, ensure integration, and present the final solution.
6. **Context is Key**: Read `docs/development/INDEX.md` and `docs/development/status.xml` to provide relevant context to sub-agents.

## Usage Examples

```bash
# Delegate a complex documentation update
/one-off "Update all API documentation to reflect the new authentication flow"

# Delegate a research task
/one-off "Research best practices for implementing rate limiting in our API"

# Delegate a refactoring task
/one-off "Refactor the authentication module to use the new token service"
```

## When to Use

- One-off tasks that don't fit into current story workflow
- Research and analysis tasks
- Documentation updates across multiple files
- Cross-cutting concerns not tied to specific features
- Experimental work or proof-of-concepts

## When NOT to Use

- Regular feature development (use `/dev` instead)
- Bug fixes that should be tracked (use `/fix` instead)
- Tasks that are part of current story (use `/dev` instead)

## Coordinator Agent Instructions

When this command is invoked, the coordinator agent receives:

```markdown
Task: One-off task delegation

User Request: [user's task description]

Instructions:

You are the coordinator agent executing a one-off task outside the normal story workflow.

**Your Mission**:
1. Analyze the request and break it into logical sub-tasks
2. Identify which specialized agents are best suited for each sub-task
3. Spawn sub-agents in parallel whenever possible (maximize parallelization)
4. Provide each sub-agent with complete context and clear instructions
5. Instruct sub-agents to use Claude Code Skills when appropriate
6. Synthesize results from all sub-agents
7. Ensure all work is integrated and complete
8. Report final results to user

**Context Sources**:
- Read docs/development/INDEX.md for project overview
- Read docs/development/status.xml for current project state
- Read relevant feature documentation if applicable
- Read CLAUDE.md for project-specific conventions

**Parallelization Strategy**:
- Spawn 4-6 agents simultaneously for independent sub-tasks
- Examples:
  - Documentation updates: Spawn agents per doc section
  - Research tasks: Spawn agents per research topic
  - Refactoring: Spawn agents per module/component
  - Analysis: Spawn agents per codebase area

**Claude Code Skills**:
- Encourage sub-agents to create Skills for reusable logic
- Use existing Skills when available
- Package common patterns as Skills for future use

**Success Criteria**:
- All sub-tasks completed
- Results integrated cohesively
- No conflicts or inconsistencies
- Clear report of what was accomplished
- Any new patterns documented

**Report Format**:

When complete, provide:

```
✅ One-Off Task Complete

**Task**: [brief description]

**What Was Done**:
- Sub-task 1: [description] (agent: [name])
- Sub-task 2: [description] (agent: [name])
- Sub-task 3: [description] (agent: [name])

**Agents Used**:
- [agent-1]: [what they did]
- [agent-2]: [what they did]

**Files Modified**:
- [file-1]: [changes]
- [file-2]: [changes]

**Skills Created** (if applicable):
- [skill-name]: [description]

**Next Steps** (if applicable):
- [suggested follow-up actions]
```
```

## Notes

- This command does NOT update status.xml or story files
- Use this for work outside the normal feature/epic/story workflow
- Coordinator will handle all sub-agent spawning and coordination
- Results are reported but not tracked in project status
- Ideal for exploratory work, research, and one-time tasks
