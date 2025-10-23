---
description: Create a new feature with proper setup and documentation
model: claude-sonnet-4-5
argument-hint: [feature name]
---

# /create-feature - Create New Feature

**Purpose**: Set up complete feature structure with epics, documentation, and status tracking

## Process

1. **Clarify Feature Details**
   - Name
   - Description
   - Priority
   - Complexity

2. **Read Meta Prompt for Setup Requirements**
   - Review `prompts/project-setup-meta-prompt.md` for authoritative instructions

3. **Review Existing Project Setup**
   - Agents and commands are shared across features (don't recreate)

4. **Divide Feature into Epics**
   - Break down feature into logical groupings of related tasks
   - Examples: epic-1-foundation, epic-2-core, epic-3-polish

5. **Create Feature Directory Structure**

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

6. **Update status.xml**
   - Add new feature section in `docs/development/status.xml`
   - Configure epics tracking
   - Set up current-story tracking

7. **CRITICAL: Create Feature Documentation**
   - **Correct location**: `docs/development/features/[feature-name]/`
   - **NOT**: `features/[feature-name]/docs/`
   - Create: FEATURE_SPEC.md, TASKS.md, TECHNICAL_DESIGN.md, etc.
   - This is separate from the features/ directory

8. **CRITICAL: Create Epic Folders**
   - **Correct location**: `docs/development/features/[feature-name]/epics/[epic-name]/`
   - **NOT**: `features/[feature-name]/epics/`
   - Create for each epic: DESCRIPTION.md, TASKS.md, NOTES.md

9. **CRITICAL: Create Stories Folder**
   - **Correct location**: `docs/development/features/[feature-name]/epics/[epic-name]/stories/`
   - **NOT**: `features/[feature-name]/stories/`
   - **NOT**: `docs/development/features/[feature-name]/stories/`
   - ONLY in the epic-specific stories/ folder

10. **Handle Active Feature Switching**
    - Only ONE feature can be active at a time
    - Set `<is-active-feature>true/false</is-active-feature>`
    - Set `<current-epic>` to track which epic is being worked on

11. **Populate Pending Tasks**
    - Read TASKS.md
    - Distribute tasks into appropriate epics

12. **Show Summary and Next Steps**
    - Report what was created
    - Mention using `/create-story` to create first story

## Important Notes

- Reads `prompts/project-setup-meta-prompt.md` for authoritative instructions
- **Divide all feature tasks into epics** (e.g., epic-1-foundation, epic-2-core, epic-3-polish)
- Each epic has its own folder in `docs/development/features/[feature-name]/epics/[epic-name]/`
- Each epic contains a stories/ subfolder for user stories
- Agents and commands are SHARED across features (don't recreate)
- Sets `<is-active-feature>true/false</is-active-feature>` appropriately
- Sets `<current-epic>` to track which epic is being worked on
- User chooses "now" (develop immediately) or "later" (setup only)

## When to Use

- Starting a new major feature in the project
- Need to organize complex work into epics
- Setting up structure before development begins

## When NOT to Use

- Adding small improvements to existing feature (use `/create-story`)
- One-off tasks (use `/one-off`)
- Bug fixes (use `/fix`)
