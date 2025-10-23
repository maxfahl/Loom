---
description: Create a new feature with proper setup and documentation
model: sonnet
argument-hint: [feature name]
---

# /create-feature - Create New Feature

## What This Command Does

Set up complete feature structure with epics, documentation, and status tracking.

## Process

1. **Clarify Feature Details**:
   - Feature name (from `$ARGUMENTS` or ask user)
   - Description and goals
   - Priority (High/Medium/Low)
   - Complexity estimate

2. **Read Meta Prompt**:
   - Review setup requirements
   - Verify project structure exists
   - Note that agents/commands are shared across features

3. **Divide Feature into Epics**:
   - Break down feature into logical groupings
   - Create epic structure (Epic 1, Epic 2, etc.)
   - Define goals for each epic

4. **Create Feature Directory Structure**:

   ```
   docs/development/
   └── status.xml        # Update with new feature
   └── features/[feature-name]/
       ├── INDEX.md
       ├── FEATURE_SPEC.md
       ├── TASKS.md
       ├── TECHNICAL_DESIGN.md
       ├── CHANGELOG.md
       └── epics/
           ├── epic-1-[name]/
           │   ├── DESCRIPTION.md
           │   ├── TASKS.md
           │   ├── NOTES.md
           │   └── stories/
           │       ├── 1.1.md
           │       ├── 1.2.md
           │       └── 1.3.md
           ├── epic-2-[name]/
           │   └── ...
           └── epic-3-[name]/
               └── ...
   ```

5. **Create Documentation Files**:
   - **INDEX.md**: Project overview, tech stack, key references
   - **FEATURE_SPEC.md**: Feature requirements and acceptance criteria
   - **TASKS.md**: High-level task list
   - **TECHNICAL_DESIGN.md**: Architecture and design decisions
   - **CHANGELOG.md**: Track feature evolution

6. **Update status.xml**:
   - Add new feature to tracking
   - Set current feature if it's the first
   - Initialize YOLO configuration
   - Set status to "Planning"

7. **Create First Story** (optional):
   - Ask if user wants to create first story now
   - If yes, run `/create-story` command

## Recommended Skills

<!-- TODO: Add relevant skills from .claude/skills/ -->

- `agile-methodologies` - For epic/story structure
- `requirements-engineering` - For feature specifications
- `clean-architecture` - For technical design

Use these skills heavily throughout execution to ensure best practices.

**Skill Troubleshooting Authority**: If any referenced skill does not work or any script within the skill does not work, Claude Code has the authority to fix them.

## Arguments

- `$ARGUMENTS`: Feature name

## Examples

```
/create-feature user-authentication
```

Creates complete feature structure for user authentication.

```
/create-feature
```

Asks for feature name interactively.
