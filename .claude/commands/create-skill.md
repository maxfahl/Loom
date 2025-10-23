---
description: Create new Claude Code skill (uses skill-creator agent)
model: sonnet
argument-hint: [skill-name]
---

# /create-skill - Create New Skill

## What This Command Does

Create a new Claude Code skill package following official guidelines and best practices.

## Process

1. **Validate Skill Name**:
   - Check that `$ARGUMENTS` follows naming convention:
     - Lowercase letters, numbers, and hyphens only
     - Max 64 characters
     - No uppercase, no underscores, no special characters
   - Examples: `my-skill`, `api-helper-2024`, `data-processor`

2. **Delegate to Skill Creator Agent**:

   ```markdown
   Task(
     subagent_type="skill-creator",
     description="Create new skill: $ARGUMENTS",
     prompt="Create a new Claude Code skill named '$ARGUMENTS'.

     Follow these steps:
     1. Validate the skill name follows official guidelines
     2. Ask user for skill purpose and functionality
     3. Create complete skill package structure
     4. Generate SKILL.md with proper YAML frontmatter
     5. Create any necessary scripts or templates
     6. Add comprehensive documentation
     7. Create examples and usage guides

     Ensure compliance with all official Claude Code skill creation guidelines."
   )
   ```

3. **Skill Creator Agent Will**:
   - Validate skill name format
   - Gather requirements from user
   - Create `.claude/skills/[skill-name]/` directory
   - Generate SKILL.md with valid YAML
   - Create scripts directory if needed
   - Add templates if needed
   - Create comprehensive README
   - Add examples
   - Validate final structure

4. **Output**:
   ```markdown
   ✅ Skill created successfully!

   Location: .claude/skills/[skill-name]/
   Files created:
   - SKILL.md (main skill definition)
   - README.md (documentation)
   - scripts/ (if applicable)
   - templates/ (if applicable)
   - examples/ (usage examples)

   The skill is now available for use in your project.

   To use this skill:
   - Reference it in commands or agent prompts
   - Skills are auto-discovered by Claude Code
   ```

## Agent Delegation

```markdown
Task(
  subagent_type="skill-creator",
  description="Create skill: $ARGUMENTS",
  prompt="Create new Claude Code skill named '$ARGUMENTS'. Follow official skill creation guidelines. Ask user for skill purpose and create complete package structure with SKILL.md, scripts, templates, and documentation."
)
```

## Recommended Skills

<!-- TODO: Add relevant skills from .claude/skills/ -->

The skill-creator agent has built-in knowledge of skill creation guidelines.

**Skill Troubleshooting Authority**: If any referenced skill does not work or any script within the skill does not work, Claude Code has the authority to fix them.

## Arguments

- `$ARGUMENTS`: Skill name (lowercase, hyphens, max 64 chars)

## Examples

```
/create-skill api-validator
```

Creates a new skill for API validation.

```
/create-skill database-migration-helper
```

Creates a skill for database migrations.

```
/create-skill
```

Prompts for skill name interactively.

## Validation Rules

Before delegation, verify:
- [ ] Skill name uses only lowercase letters, numbers, and hyphens
- [ ] Skill name is 64 characters or less
- [ ] No spaces, underscores, or special characters
- [ ] Name is descriptive and follows conventions
