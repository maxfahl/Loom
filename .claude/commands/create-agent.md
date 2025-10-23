---
description: Create new specialized agent (uses agent-creator agent)
model: sonnet
argument-hint: [agent-name]
---

# /create-agent - Create New Agent

## What This Command Does

Create a new specialized Claude Code agent following official guidelines and framework conventions.

## Process

1. **Validate Agent Name**:
   - Check that `$ARGUMENTS` follows naming convention:
     - Lowercase letters and hyphens only
     - Filename must match agent name
     - No uppercase, no underscores, no special characters
   - Examples: `api-specialist`, `database-optimizer`, `ui-designer`

2. **Delegate to Agent Creator Agent**:

   ```markdown
   Task(
     subagent_type="agent-creator",
     description="Create new agent: $ARGUMENTS",
     prompt="Create a new Claude Code agent named '$ARGUMENTS'.

     Follow these steps:
     1. Validate the agent name follows official guidelines
     2. Ask user for agent purpose, responsibilities, and capabilities
     3. Create agent template in .claude/agents/$ARGUMENTS.md
     4. Include proper YAML frontmatter (name, description, tools, model)
     5. Add standard sections (Start by Reading, YOLO Mode, Update status.xml, Responsibilities)
     6. Include MCP Server Integration section if agent needs MCP tools
     7. Add agent-specific workflow instructions
     8. Update AGENTS.md to include new agent in appropriate category
     9. Update all framework references to include new agent
     10. Update agent counts in CLAUDE.md (currently 44 agents)

     Ensure compliance with all official Claude Code agent creation guidelines."
   )
   ```

3. **Agent Creator Will**:
   - Validate agent name format
   - Gather agent requirements from user
   - Create template file in `.claude/agents/[agent-name].md`
   - Include proper YAML frontmatter
   - Add all standard sections
   - Include MCP integration if needed
   - Create agent-specific workflow
   - Update AGENTS.md with new agent
   - Update framework references
   - Update agent counts

4. **Output**:
   ```markdown
   ✅ Agent created successfully!

   Location: .claude/agents/[agent-name].md

   Next steps:
   1. Review the agent template and customize as needed
   2. Agent has been added to AGENTS.md directory
   3. The agent is now available in .claude/agents/

   The agent is immediately available for use.
   ```

## Agent Delegation

```markdown
Task(
  subagent_type="agent-creator",
  description="Create agent: $ARGUMENTS",
  prompt="Create new Claude Code agent named '$ARGUMENTS'. Follow official agent creation guidelines and Loom framework conventions. Ask user for agent purpose, create template, update AGENTS.md, and update all framework references."
)
```

## Recommended Skills

<!-- TODO: Add relevant skills from .claude/skills/ -->

The agent-creator agent has built-in knowledge of agent creation guidelines.

**Skill Troubleshooting Authority**: If any referenced skill does not work or any script within the skill does not work, Claude Code has the authority to fix them.

## Arguments

- `$ARGUMENTS`: Agent name (lowercase with hyphens)

## Examples

```
/create-agent database-specialist
```

Creates a new agent specialized in database operations.

```
/create-agent api-designer
```

Creates a new agent for API design.

```
/create-agent
```

Prompts for agent name interactively.

## Validation Rules

Before delegation, verify:
- [ ] Agent name uses only lowercase letters and hyphens
- [ ] No spaces, underscores, numbers, or special characters
- [ ] Name is descriptive and follows conventions
- [ ] Name doesn't conflict with existing agents

## Important Notes

After creating a new agent:
1. The agent template is created directly in `.claude/agents/`
2. AGENTS.md is updated with the new agent
3. Framework references are updated throughout the codebase
4. Agent counts are updated in CLAUDE.md (remember to update from 44 to new count)
5. The agent is immediately available for use
