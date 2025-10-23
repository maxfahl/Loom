# Reference: CLAUDE.md Template

**Purpose**: This file documents the CLAUDE.md template structure for reference purposes only. The actual deployment is handled by `scripts/deploy-claude-md.sh` which is called directly from `setup.md` and `update-setup.md`.

## Template Location

**Source**: `prompts/reference/claude-md-template.md`

## Template Philosophy

**CLAUDE.md is NOT documentation—it's an instruction manual.**

It provides:
1. **What Loom is** (concise overview)
2. **Core components** (agents, commands, epics/stories, YOLO)
3. **How to work in this project** (workflows, rules, guardrails)
4. **Folder structure** (with descriptions of where to find things)
5. **Critical guardrails** (NEVER/ALWAYS rules for agents and commands)

## Marker System

The template uses HTML markers to identify framework-managed sections:

```markdown
<!-- LOOM_FRAMEWORK_START -->
[Framework sections - auto-updated on script re-runs]
<!-- LOOM_FRAMEWORK_END -->

## 📊 Project-Specific Details
[User customizations - preserved on script re-runs]
```

**Framework Sections** (between markers):
- What is Loom?
- Loom Framework Components (agents, commands, epics/stories, YOLO)
- Project Structure (complete folder tree with descriptions)
- How to Work in This Project (pre-task checklist, execution rules, workflows)
- Critical Guardrails (NEVER/ALWAYS lists)
- Quick Reference (command lookup table)
- status.xml Structure

**User Sections** (outside markers):
- Project-Specific Details (tech stack, TDD level, commands)
- Custom workflows
- Project-specific conventions
- Additional notes

## Placeholders

The template contains these placeholders (replaced by deployment script):

- `[PROJECT_NAME]` - Project name from discovery
- `[YYYY-MM-DD]` - Current date
- `[TECH_STACK]` - Full tech stack description
- `[TDD_LEVEL]` - One of: STRICT, RECOMMENDED, OPTIONAL
- `[PREVIEW_COMMAND]` - Command to start dev server
- `[TEST_COMMAND]` - Command to run tests
- `[BUILD_COMMAND]` - Command to build project

## Conditional Sections

The template includes conditional TDD sections:

```markdown
[IF STRICT]
- **MANDATORY**: Red-Green-Refactor cycle enforced
- Write failing tests FIRST (RED)
...

[IF RECOMMENDED]
- **RECOMMENDED**: Tests should be written before or alongside implementation
...

[IF OPTIONAL]
- **OPTIONAL**: Add tests for critical functionality
...
```

The deployment script selects the appropriate section based on `TDD_LEVEL` parameter.

## Deployment

**Script**: `scripts/deploy-claude-md.sh`

**Called from**:
- `setup.md` - Phase 4 (new projects)
- `update-setup.md` - Step 2.5 (existing projects)

**Script handles**:
- Creating new CLAUDE.md from template
- Updating existing CLAUDE.md (marker-based replacement)
- Preserving user customizations
- Replacing all placeholders
- Handling conditional TDD sections
- Creating LOOM_FRAMEWORK.md if custom CLAUDE.md exists

See `setup.md` and `update-setup.md` for actual deployment instructions.
