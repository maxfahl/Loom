# Phase 4: Command Creation

**Part of**: [Project Setup Meta Prompt](../project-setup-meta-prompt.md)

## Purpose

Create 11+ custom slash commands including /dev, /commit, /review, /status, /test, /plan, /docs, /yolo, /create-feature, /correct-course, /create-agent, /create-skill. Includes command templates and creation workflow.

## Related Files

- [../templates/command-template.md](../templates/command-template.md) - Generic command structure
- [../reference/core-agents.md](../reference/core-agents.md) - Agents used by commands
- [phase-5-claude-md.md](phase-5-claude-md.md) - Commands documented in CLAUDE.md

## Usage

Read this file:
- In Phase 4 after agents are created
- To understand all 11+ core commands
- For command creation workflow and templates
- To see which commands use which agents

---

## 🎯 Custom Slash Commands to Create

### Core Commands (Always Include)

**1. /dev** - Continue Development

```yaml
---
description: Continue development on current task with [methodology]
allowed-tools: Bash(npm:*), Bash(git:*), Read, Write, Edit, Glob, Grep
model: claude-sonnet-4-5
---
```

**Purpose**: Resume coding with context of current task, following project conventions

**TDD Variations**:

- **Fully Enforced**: "Follow TDD Red-Green-Refactor strictly. Write failing test FIRST, then implement."
- **Recommended**: "Follow TDD Red-Green-Refactor when possible. Consider writing tests first."
- **No TDD**: "Continue implementation. Add tests for critical functionality."

**2. /commit [message]** - Smart Commit

```yaml
---
description: Smart commit with tests, linting, and conventional commits
allowed-tools: Bash(npm:*), Bash(git:*)
model: claude-sonnet-4-5
argument-hint: [commit message]
---
```

**Purpose**: Run all checks, review changes, create conventional commit

**3. /review** - Comprehensive Review

```yaml
---
description: Comprehensive review of uncommitted changes
allowed-tools: Bash(git:*), Read, Grep
model: claude-sonnet-4-5
---
```

**Purpose**: Full code review checklist before committing

**4. /project-status** - Project Status

```yaml
---
description: Show comprehensive project status
allowed-tools: Bash(git:*), Bash(npm:*), Read
model: claude-haiku-4-5
---
```

**Purpose**: Quick status report (git, tasks, tests, coverage)

**5. /test [pattern]** - Run Tests

```yaml
---
description: Run tests with coverage and detailed reporting
allowed-tools: Bash(npm:*)
model: claude-haiku-4-5
argument-hint: [test pattern]
---
```

**Purpose**: Execute tests and analyze results

**6. /plan [feature]** - Plan Feature

```yaml
---
description: Plan next feature or task with detailed breakdown
model: claude-sonnet-4-5
argument-hint: [feature name or task]
---
```

**Purpose**: Create detailed implementation plan with TDD breakdown

**7. /docs [type]** - Update Documentation

```yaml
---
description: Update documentation after changes
allowed-tools: Read, Write, Edit, Bash(git:*)
model: claude-haiku-4-5
argument-hint: [doc type: code|api|user|all]
---
```

**Purpose**: Update relevant docs based on code changes

**8. /yolo** - Configure YOLO Mode

```yaml
---
description: Configure YOLO mode breakpoints interactively
allowed-tools: Read, Write, Edit
model: claude-haiku-4-5
---
```

**Purpose**: Configure YOLO mode and breakpoints where agents should stop

**Process**:

1. Read current status.xml for active feature
2. Show current YOLO mode status and breakpoints
3. Present numbered list of common breakpoints:

   ```
   Select breakpoints where agents should STOP and ask for confirmation:

   1. After completing development, before code review
   2. After code review, before running tests
   3. After tests pass, before user testing
   4. After user testing, before committing
   5. After commit, before pushing to remote
   6. Before making any file changes (very cautious)
   7. Before running any tests (very cautious)
   8. Before major refactoring

   Enter numbers separated by commas (e.g., "1, 3, 4, 8")
   Or enter "all" for maximum control (stop at all breakpoints)
   Or enter "none" for maximum speed (YOLO mode ON, skip all breakpoints)
   ```

4. Parse user response (e.g., "1, 3, 4, 8")
5. Update status.xml with selected breakpoints
6. Show confirmation:

   ```
   ✅ YOLO mode configured!

   Mode: [ON/OFF]
   Agents will STOP at these breakpoints:
   - Breakpoint 1: After completing development, before code review
   - Breakpoint 3: After tests pass, before user testing
   - Breakpoint 4: After user testing, before committing
   - Breakpoint 8: Before major refactoring

   Agents will SKIP these breakpoints:
   - Breakpoint 2: After code review, before running tests
   - Breakpoint 5: After commit, before pushing to remote
   - Breakpoint 6: Before making any file changes
   - Breakpoint 7: Before running any tests
   ```

**YOLO Mode Logic**:

- If user selects "none": Set `<yolo-mode enabled="true">`, all breakpoints disabled
- If user selects "all": Set `<yolo-mode enabled="false">`, all breakpoints enabled
- If user selects specific numbers: Configure individual breakpoints

**Important**: This command edits `features/[feature-name]/status.xml`

**9. /create-feature [name]** - Create New Feature

```yaml
---
description: Create a new feature with proper setup and documentation
model: claude-sonnet-4-5
argument-hint: [feature name]
---
```

**Purpose**: Set up complete feature structure with epics, documentation, and status tracking

**Process**:

1. Clarify feature details (name, description, priority, complexity)
2. Read meta prompt for setup requirements
3. Review existing project setup (agents/commands are shared)
4. **Divide feature into epics** (logical groupings of related tasks)
5. Create feature directory structure:
   ```
   features/[feature-name]/
   ├── status.xml
   ├── epics/
   │   ├── epic-1-[name]/
   │   │   ├── DESCRIPTION.md  # Epic overview and goals
   │   │   ├── TASKS.md        # Epic-specific task list
   │   │   └── NOTES.md        # Implementation notes
   │   ├── epic-2-[name]/
   │   │   ├── DESCRIPTION.md
   │   │   ├── TASKS.md
   │   │   └── NOTES.md
   │   └── epic-3-[name]/
   │       ├── DESCRIPTION.md
   │       ├── TASKS.md
   │       └── NOTES.md
   ├── src/ (when development starts)
   └── tests/ (when development starts)

   docs/development/features/[feature-name]/
   ├── INDEX.md
   ├── FEATURE_SPEC.md
   ├── TASKS.md
   ├── TECHNICAL_DESIGN.md
   ├── CHANGELOG.md
   └── stories/          # User stories folder (empty initially)
   ```
6. Create status.xml in features/[feature-name]/ with epics configuration and current-story tracking
7. **CRITICAL**: Create feature documentation in docs/development/features/[feature-name]/ (FEATURE_SPEC, TASKS, TECHNICAL_DESIGN, etc.)
   - Create directory: `docs/development/features/[feature-name]/`
   - NOT in `features/[feature-name]/docs/`
   - This is separate from the features/ directory
8. **CRITICAL**: Create empty stories folder at `docs/development/features/[feature-name]/stories/`
   - NOT in `features/[feature-name]/stories/`
   - NOT in `features/[feature-name]/docs/stories/`
   - ONLY in `docs/development/features/[feature-name]/stories/`
9. **Create epic folders** in `features/[feature-name]/epics/` with DESCRIPTION.md, TASKS.md, and NOTES.md for each
10. Handle active feature switching (only ONE active at a time)
11. Populate pending-tasks from TASKS.md into appropriate epics
12. Show summary and next steps (mention using /create-story to create first story)

**Important**:

- Reads `prompts/project-setup-meta-prompt.md` for authoritative instructions
- **Divide all feature tasks into epics** (e.g., epic-1-foundation, epic-2-core, epic-3-polish)
- Each epic has its own folder with documentation
- Agents and commands are SHARED across features (don't recreate)
- Sets `<is-active-feature>true/false</is-active-feature>` appropriately
- Sets `<current-epic>` to track which epic is being worked on
- User chooses "now" (develop immediately) or "later" (setup only)

**10. /correct-course [feature]** - Correct Feature Direction

```yaml
---
description: Correct course on a feature based on new requirements or direction changes
model: claude-sonnet-4-5
argument-hint: [feature name or current]
---
```

**Purpose**: Adjust feature direction based on changing requirements, mistakes, or new insights

**Process**:

1. Identify feature (use "current" for active feature)
2. Read current feature state (status.xml + epic docs + feature docs + code + commits)
3. Show user current state summary (including epic breakdown)
4. Understand desired changes from user
5. Analyze impact (code to keep/modify/remove, tests to update, docs to revise, epics to reorganize)
6. **Update epic documentation** with changes (DESCRIPTION.md, TASKS.md in affected epics)
7. Update feature documentation with change log
8. Update status.xml with course correction notes and epic status changes
9. Create action plan (Cleanup → Modify → Add → Update Docs → Verify)
10. Execute corrections based on user's choice (automatic/step-by-step/manual)
11. Handle git history (revert commits if needed)
12. Verify corrections (tests, docs, status.xml)
13. **Update epic task lists** to reflect new direction
14. Update status.xml final state

**Important**:

- Reads `prompts/project-setup-meta-prompt.md` for guidance
- Reviews ALL existing work before making changes (including all epic folders)
- Documents WHY correction was needed in feature docs AND epic NOTES.md
- Updates status.xml to reflect new direction (including epic status)
- Handles cancelled tasks appropriately (mark epic as cancelled if needed)
- May reorganize epics if direction changes significantly
- Updates `<current-epic>` if switching to different epic
- May add `<cancelled-tasks>` section to status.xml

**11. /create-story** - Create Next Story

```yaml
---
description: Create the next user story for the current epic
model: claude-sonnet-4-5
---
```

**Purpose**: Analyze completed work, identify next story, and create comprehensive story file

**Process**:

1. Read status.xml to identify active feature and current epic
2. Read epic TASKS.md in `features/[feature]/epics/[current-epic]/`
3. Check existing stories in `docs/development/features/[feature-name]/stories/` to see what's been created
4. Analyze what's been completed vs what's pending in the epic
5. Determine next story number (e.g., if current-story is 2.1, check if 2.1 exists, create 2.2)
6. **CRITICAL**: Create new story file at `docs/development/features/[feature-name]/stories/[epic.story].md`
   - NOT in `features/[feature-name]/`
   - NOT in `features/[feature-name]/docs/stories/`
   - ONLY in `docs/development/features/[feature-name]/stories/`
7. Update status.xml `<current-story>` to the new story number
8. Update `<last-updated>` timestamp

**Story File Location** (CRITICAL - DO NOT CHANGE):
- **Correct**: `docs/development/features/[feature-name]/stories/X.Y.md`
- **Wrong**: `features/[feature-name]/stories/X.Y.md`
- **Wrong**: `features/[feature-name]/docs/stories/X.Y.md`

**Story File Structure**:

```markdown
