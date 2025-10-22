# Phase 6: Root Files & Features Setup

**Part of**: [Project Setup Meta Prompt](../project-setup-meta-prompt.md)

## Overview

Create root-level files (.gitignore, README.md) and set up features/ directory structure.

## Root Files

### 1. .gitignore
Create appropriate exclusions for tech stack:
- .env files (never commit secrets)
- node_modules/, venv/, target/ (dependencies)
- Build artifacts (.next/, dist/, build/)
- IDE files (.vscode/, .idea/)
- OS files (.DS_Store, Thumbs.db)

### 2. README.md
Minimal getting started guide:
- Project overview (1-2 sentences)
- Quick start steps (install, run, test)
- Link to full documentation: `docs/development/INDEX.md`

## Features Directory Setup

### For Greenfield Projects

1. **Create features/ directory and docs/development/features/ directory**
2. **Create initial feature folders** (if any planned from PRD):
   ```
   Project Root:

   features/
   ├── feature-name/
   │   ├── status.xml
   │   ├── epics/
   │   │   ├── epic-1-foundation/
   │   │   │   ├── DESCRIPTION.md
   │   │   │   ├── TASKS.md
   │   │   │   └── NOTES.md
   │   │   ├── epic-2-core/
   │   │   │   ├── DESCRIPTION.md
   │   │   │   ├── TASKS.md
   │   │   │   └── NOTES.md
   │   │   └── epic-3-polish/
   │   │       ├── DESCRIPTION.md
   │   │       ├── TASKS.md
   │   │       └── NOTES.md
   │   ├── src/ (created when development starts)
   │   └── tests/ (created when development starts)

   docs/
   └── development/
       └── features/
           └── feature-name/
               ├── INDEX.md
               ├── FEATURE_SPEC.md
               ├── TECHNICAL_DESIGN.md
               ├── TASKS.md
               ├── CHANGELOG.md
               └── stories/ (empty, for /create-story)
   ```

3. **Create status.xml** in features/[name]/ for each feature (see [status-xml.md](../reference/status-xml.md))
4. **Create feature documentation directory** at docs/development/features/[name]/ with all doc files and stories/ subfolder
5. **Populate epics** with DESCRIPTION.md, TASKS.md, NOTES.md in features/[name]/epics/
6. **Set ONE feature** as active: `<is-active-feature>true</is-active-feature>`

### For Brownfield Projects (FIXED)

**Brownfield projects need feature tracking setup too!**

1. **Ask user if they want feature tracking**:
   ```
   I notice this is an existing project. Would you like to adopt the
   features/ + status.xml tracking system for managing development?
   
   Benefits:
   - Track current epic and story being worked on
   - Manage YOLO mode for autonomous development
   - Organize work into logical feature directories
   - Enable /dev, /review, /plan commands to track progress
   
   Options:
   a) Yes, set up feature tracking for existing work
   b) No, skip features/ directory (agents will work without it)
   ```

2. **If user chooses (a), analyze existing codebase**:
   - Read PROJECT_OVERVIEW.md for current features
   - Identify logical feature groupings
   - Propose initial feature directories

3. **Create features/ structure based on analysis**:
   ```
   Example for existing e-commerce project:

   features/
   ├── user-authentication/ (existing code)
   │   ├── status.xml (added)
   │   ├── epics/ (added)
   │   ├── src/ (existing)
   │   └── tests/ (existing)
   ├── product-catalog/ (existing code)
   │   ├── status.xml (added)
   │   ├── epics/ (added)
   │   ├── src/ (existing)
   │   └── tests/ (existing)
   └── shopping-cart/ (in progress - ACTIVE)
       ├── status.xml (added - set as active)
       ├── epics/ (added with current tasks)
       ├── src/ (existing)
       └── tests/ (existing)

   docs/development/features/
   ├── user-authentication/ (added)
   │   ├── INDEX.md
   │   ├── FEATURE_SPEC.md
   │   ├── TECHNICAL_DESIGN.md
   │   ├── TASKS.md
   │   ├── CHANGELOG.md
   │   └── stories/
   ├── product-catalog/ (added)
   │   ├── INDEX.md
   │   ├── FEATURE_SPEC.md
   │   ├── TECHNICAL_DESIGN.md
   │   ├── TASKS.md
   │   ├── CHANGELOG.md
   │   └── stories/
   └── shopping-cart/ (added - ACTIVE)
       ├── INDEX.md
       ├── FEATURE_SPEC.md
       ├── TECHNICAL_DESIGN.md
       ├── TASKS.md
       ├── CHANGELOG.md
       └── stories/ (for /create-story)
   ```

4. **For active feature (work in progress)**:
   - Set `<is-active-feature>true</is-active-feature>`
   - Create epics based on remaining work
   - Populate `<pending-tasks>` from PROJECT_OVERVIEW.md
   - Set `<current-epic>` and `<current-story>` if applicable

5. **For completed features**:
   - Set `<current-phase>Completed</current-phase>`
   - Set `<is-active-feature>false</is-active-feature>`
   - Minimal epic structure (can document what was done)

6. **If user chooses (b)**:
   - Skip features/ directory creation
   - Note in CLAUDE.md that features/ is not used
   - Agents will still function (just without status.xml tracking)

### Epic Structure

Each epic folder contains:

**DESCRIPTION.md**:
```markdown
# Epic: [Epic Name]

## Overview
[What this epic accomplishes]

## Goals
- Goal 1
- Goal 2

## Success Criteria
- [ ] Criterion 1
- [ ] Criterion 2
```

**TASKS.md**:
```markdown
# Tasks for [Epic Name]

## Story 1: [Story title]
- [ ] Task 1
- [ ] Task 2

## Story 2: [Story title]
- [ ] Task 1
- [ ] Task 2
```

**NOTES.md**:
```markdown
# Implementation Notes for [Epic Name]

## Technical Decisions
- Decision 1: Rationale

## Blockers
- [Any blockers encountered]

## Learnings
- [What we learned during this epic]
```

## Related Files
- [status-xml.md](../reference/status-xml.md) - Complete status.xml structure
- [phase-1-discovery.md](phase-1-discovery.md) - Brownfield analysis
- [story-template.md](../templates/story-template.md) - Story file structure

## Next Steps

After Phase 6:
- features/ directory structure created
- status.xml files initialized
- Epic folders populated
- Active feature identified
- Ready for Phase 7 (Verification)
