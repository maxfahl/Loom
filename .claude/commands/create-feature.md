---
description: Create a new feature with proper setup and documentation
model: claude-sonnet-4-5
argument-hint: [feature name]
---

**Purpose**: Set up complete feature structure with epics, documentation, and status tracking

**Process**:

1. Clarify feature details (name, description, priority, complexity)
2. Read meta prompt for setup requirements
3. Review existing project setup (agents/commands are shared)
4. **Divide feature into epics** (logical groupings of related tasks)
5. Create feature directory structure:
   ```
   docs/development/
   └── status.xml        # Feature tracking (SINGLE FILE for ALL features)
   └── features/[feature-name]/
       ├── INDEX.md
       ├── FEATURE_SPEC.md
       ├── TASKS.md
       ├── TECHNICAL_DESIGN.md
       ├── CHANGELOG.md
       └── epics/            # Epic folders with stories
           ├── epic-1-[name]/
           │   ├── DESCRIPTION.md  # Epic overview and goals
           │   ├── TASKS.md        # Epic-specific task list
           │   ├── NOTES.md        # Implementation notes
           │   └── stories/        # Stories for this epic
           │       ├── 1.1.md
           │       ├── 1.2.md
           │       └── 1.3.md
           ├── epic-2-[name]/
           │   ├── DESCRIPTION.md
           │   ├── TASKS.md
           │   ├── NOTES.md
           │   └── stories/
           │       ├── 2.1.md
           │       └── 2.2.md
           └── epic-3-[name]/
               ├── DESCRIPTION.md
               ├── TASKS.md
               ├── NOTES.md
               └── stories/
                   └── 3.1.md
   ```
6. Update status.xml in docs/development/ with new feature section (epics configuration and current-story tracking)
7. **CRITICAL**: Create feature documentation in docs/development/features/[feature-name]/ (FEATURE_SPEC, TASKS, TECHNICAL_DESIGN, etc.)
   - Create directory: `docs/development/features/[feature-name]/`
   - NOT in `features/[feature-name]/docs/`
   - This is separate from the features/ directory
8. **CRITICAL**: Create epic folders in `docs/development/features/[feature-name]/epics/[epic-name]/` with DESCRIPTION.md, TASKS.md, and NOTES.md for each epic
   - NOT in `features/[feature-name]/epics/`
   - ONLY in `docs/development/features/[feature-name]/epics/`
9. **CRITICAL**: Create stories folder inside each epic at `docs/development/features/[feature-name]/epics/[epic-name]/stories/`
   - NOT in `features/[feature-name]/stories/`
   - NOT in `docs/development/features/[feature-name]/stories/`
   - ONLY in `docs/development/features/[feature-name]/epics/[epic-name]/stories/`
10. Handle active feature switching (only ONE active at a time)
11. Populate pending-tasks from TASKS.md into appropriate epics
12. Show summary and next steps (mention using /create-story to create first story)

**Important**:

- Reads `prompts/project-setup-meta-prompt.md` for authoritative instructions
- **Divide all feature tasks into epics** (e.g., epic-1-foundation, epic-2-core, epic-3-polish)
- Each epic has its own folder in `docs/development/features/[feature-name]/epics/[epic-name]/`
- Each epic contains a stories/ subfolder for user stories
- Agents and commands are SHARED across features (don't recreate)
- Active feature tracked in status.xml
- Feature source code goes in features/ directory (created during implementation)
- Feature documentation ALWAYS in docs/development/features/
