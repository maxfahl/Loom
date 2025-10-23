# Loom - Framework Development Instructions

**Project**: Loom Meta-Framework Repository
**Version**: 1.0
**Purpose**: Maintain agent templates, command templates, and deployment scripts

---

## 1. What This Is

- Loom meta-framework repository
- Contains entry point prompts that users reference from their projects
- Contains agent templates in `.claude/agents/`, command templates in `.claude/commands/`
- CLAUDE.md instructions are for **framework development**, not user project setup

---

## 2. Entry Points (Users Reference These)

```
loomify.md        -> Unified entry point (auto-detects setup vs update mode)
```

---

## 3. Core Rule: Maintain Cross-References

When you change ANY file:

- Search ALL files for references to it
- Analyze the surrounding instructions/context around each reference
- Update those references AND their surrounding context to reflect the change
- Update counts if adding/removing agents or commands

---

## 4. Source of Truth

- **Agent Templates**: `.claude/agents/*.md` (41 templates - EDIT DIRECTLY)
- **Agent Directory**: `.claude/AGENTS.md` (complete agent list - EDIT DIRECTLY)
- **Command Templates**: `.claude/commands/*.md` (17 templates - EDIT DIRECTLY)
- **Docs**: `prompts/templates/doc-templates.md` -> deployed to user projects

**Key Change**: Templates now live directly in `.claude/` - no copying/generation needed for framework!

---

## 5. File Structure

```
Entry Point:
└── loomify.md -> prompts/setup/* + prompts/update-setup/* (auto-detects mode)

Templates (EDIT DIRECTLY):
├── .claude/agents/*.md (46 agent templates)
├── .claude/commands/*.md (17 command templates)
├── .claude/AGENTS.md (agent directory)
└── .claude/skills/*.md (Claude Skills packages)

Scripts:
├── sync-loom-files.sh (deploy to user projects)
├── deploy-claude-md.sh (deploy CLAUDE.md with markers)
└── migrate-stories.sh (fix story locations)
```

---

## 6. Common Operations

### Add New Agent

1. **Create template**: Create new `.md` file in `.claude/agents/[agent-name].md`
   - Use lowercase and hyphens only (e.g., `my-agent.md`)
   - Copy structure from existing agent template
   - Include valid YAML frontmatter (name, description, tools, model)
   - Add standard sections (Start by Reading, YOLO Mode, Update status.xml, Responsibilities)
   - Include MCP Server Integration section if agent needs MCP tools
   - Document agent-specific workflow

2. **Update agent directory**:
   - Edit `.claude/AGENTS.md`
   - Add new agent to appropriate category
   - Include: expertise, use cases, delegation pattern, model

3. **Update counts everywhere**:
   - Search for "46 agents" and update to new count throughout codebase
   - Update CHANGELOG.md

### Edit Existing Agent

1. **Edit template**: Modify `.claude/agents/[agent-name].md` directly
2. **Changes apply immediately**: No copying/generation needed
3. **Update CHANGELOG.md**: Document changes

### Add New Command

1. **Create template**: Create new `.md` file in `.claude/commands/[command-name].md`
   - Use lowercase and hyphens only (e.g., `my-command.md` → `/my-command`)
   - Copy structure from existing command template
   - Include YAML frontmatter (description, model, argument-hint if needed)
   - Add standard sections:
     - "What This Command Does"
     - "Process" (step-by-step workflow)
     - "Agent Delegation" (if command spawns agents)
     - "Recommended Skills" (from `.claude/skills/`)
     - "Arguments" documentation
     - "Examples" section

2. **Update counts everywhere**:
   - Search for "18 commands" and update to new count
   - Update CHANGELOG.md

### Edit Existing Command

1. **Edit template**: Modify `.claude/commands/[command-name].md` directly
2. **Changes apply immediately**: No copying/generation needed
3. **Update CHANGELOG.md**: Document changes

### Command Naming and Frontmatter Guidelines

**Naming Convention**:

- Filename without `.md` becomes command name: `optimize.md` → `/optimize`
- Use lowercase and hyphens only
- No spaces, underscores, or special characters

**YAML Frontmatter Fields** (all optional):

```yaml
---
description: Brief command summary (required for programmatic access)
model: sonnet|opus|haiku (override default model)
argument-hint: [arg1] [arg2] (guide for auto-completion)
---
```

**Common Patterns**:

- Simple prompt commands: No agent delegation, direct instructions
- Agent delegation commands: Use Task tool with subagent_type
- Multi-step workflow commands: Combine bash execution and file operations

### Change Agent MCP Access

1. Edit `.claude/agents/[agent-name].md`: Update "MCP Server Integration" section
2. Update `.claude/AGENTS.md` if delegation pattern changes
3. Update CHANGELOG.md

### Update Documentation

Edit prompts in `prompts/setup/`, `prompts/update-setup/`, `prompts/templates/` -> find all references -> update

---

## 7. Before Committing

- Verify counts (agents: 46, commands: 18)
- Test that templates work correctly
- Update CHANGELOG.md and version

---

## 8. Never Do

- X Edit files in user projects (only edit framework templates)
- X Change counts without updating all references
- X Break `<!-- LOOM_FRAMEWORK_START/END -->` markers in CLAUDE.md template

---

**That's it. Keep it simple.**
