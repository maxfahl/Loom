# Phase 3: Agent Creation

**Part of**: [Project Setup Meta Prompt](../project-setup-meta-prompt.md)

## Overview

Create 13 core agents + 2-4 technology-specific agents (or skip if using template).

## Core Agents

All 13 core agent definitions with complete workflows, MCP integration, and usage patterns are in:
- **[core-agents.md](../reference/core-agents.md)** - Complete agent definitions

Agent list:
1. coordinator
2. senior-developer
3. test-writer
4. documentation-writer
5. bug-finder
6. refactor-specialist
7. qa-tester
8. git-helper
9. architecture-advisor
10. performance-optimizer
11. agent-creator
12. skill-creator

## MCP Integration

MCP server assignments for each agent are documented in:
- **[mcp-integration.md](../reference/mcp-integration.md)**

11/13 agents have optional MCP server access.

## Creation Process

**If using template project**:
- Copy agents from template
- Optionally validate with 3 parallel agents (see template-system.md)
- Skip to tech-specific agents

**If creating from scratch**:
1. Create all 13 core agents using definitions from core-agents.md
2. Ensure each agent includes:
   - YAML frontmatter (name, description, tools, model)
   - INDEX.md reading requirement
   - status.xml reading requirement
   - MCP integration (if applicable)
   - Project-specific instructions

## Technology-Specific Agents

Based on tech stack, create 2-4 specialized agents:
- **React/Next.js**: react-component-builder
- **API Development**: api-endpoint-builder
- **Database**: database-schema-manager
- **DevOps**: deployment-specialist

## Parallel Creation

Launch 4 parallel agent-creation agents (see parallelization-patterns.md):
- Agent 1: coordinator, senior-developer, test-writer
- Agent 2: documentation-writer, bug-finder, refactor-specialist
- Agent 3: qa-tester, git-helper, architecture-advisor
- Agent 4: performance-optimizer, agent-creator, skill-creator

## Related Files
- [core-agents.md](../reference/core-agents.md) - All agent definitions
- [mcp-integration.md](../reference/mcp-integration.md) - MCP assignments
- [coordinator-workflow.md](../reference/coordinator-workflow.md) - Coordinator details
- [agent-template.md](../templates/agent-template.md) - Generic template
- [template-system.md](../reference/template-system.md) - Template copying
