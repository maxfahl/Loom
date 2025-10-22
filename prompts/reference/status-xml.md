# status.xml Structure

**Part of**: [Project Setup Meta Prompt](../project-setup-meta-prompt.md)

## Purpose

Complete XML structure for feature tracking including metadata, epics, current task, completed tasks, pending tasks, blockers, and YOLO mode configuration. This is the file that all agents read to understand current project state.

## Related Files

- [yolo-mode.md](yolo-mode.md) - YOLO mode configuration in status.xml
- [phase-6-features-setup.md](../phases/phase-6-features-setup.md) - Creating status.xml files
- [story-template.md](../templates/story-template.md) - Story structure referenced in status.xml

## Usage

Read this file when:
- Creating features/ directory structure (Phase 6)
- Understanding status.xml format
- Creating /yolo command
- Teaching agents how to read status.xml
- Setting up epic and story tracking

---

## 📋 status.xml File (CRITICAL for Feature Tracking)

### Purpose and Location

#### Purpose

The `status.xml` file tracks the current state of work for each feature directory. All agents and commands MUST read this file to understand:

- What task is currently being worked on
- What has been completed
- What's pending
- Whether YOLO mode is enabled

#### Location

Create `status.xml` in each feature directory:

```
features/
├── feature-1/
│   ├── status.xml
│   └── [feature files]
├── feature-2/
│   ├── status.xml
│   └── [feature files]
```

### XML Structure Explained

#### Complete status.xml Template

```xml
<?xml version="1.0" encoding="UTF-8"?>
<feature-status>
  <metadata>
    <feature-name>User Authentication</feature-name>
    <last-updated>2025-10-22T14:30:00Z</last-updated>
    <current-phase>Implementation</current-phase>
    <current-epic>epic-2-core-features</current-epic>
    <current-story>2.1</current-story>
    <!-- current-story format: epic.story (e.g., 2.1 = Epic 2, Story 1) -->
    <!-- Story file location: docs/development/features/[feature-name]/epics/epic-2-core-features/stories/2.1.md -->
    <is-active-feature>true</is-active-feature>
    <!-- Only ONE feature should have is-active-feature="true" at a time -->
  </metadata>

  <epics>
    <!-- Epics are logical groupings of related tasks -->
    <!-- Each epic has its own folder: docs/development/features/[feature]/epics/[epic-name]/ -->
    <epic id="epic-1-foundation" status="completed">
      <name>Foundation</name>
      <description>Set up basic authentication infrastructure</description>
      <folder>docs/development/features/[feature]/epics/epic-1-foundation/</folder>
      <completed>2025-10-21T16:00:00Z</completed>
    </epic>
    <epic id="epic-2-core-features" status="in-progress">
      <name>Core Features</name>
      <description>Implement login, logout, and token refresh</description>
      <folder>docs/development/features/[feature]/epics/epic-2-core-features/</folder>
      <started>2025-10-22T08:00:00Z</started>
    </epic>
    <epic id="epic-3-polish" status="pending">
      <name>Polish & Security</name>
      <description>Add rate limiting, security hardening, and error handling</description>
      <folder>docs/development/features/[feature]/epics/epic-3-polish/</folder>
    </epic>
  </epics>

  <yolo-mode enabled="false">
    <!-- YOLO Mode: When enabled, agents skip confirmations at configured breakpoints -->
    <!-- Configure using /yolo command or messaging: "Enable YOLO mode" -->
    <stopping-granularity>story</stopping-granularity>
    <!-- Options: "story" (default), "epic", "custom" -->
    <!-- story: Stop at configured breakpoints within each story -->
    <!-- epic: Only stop after completing full epics (autonomous per epic) -->
    <!-- custom: User-defined breakpoint configuration -->
    <description>
      YOLO mode OFF: Agents ask for confirmation before major steps like going from dev to review, letting user test manually, etc.
      YOLO mode ON: Agents proceed without confirmation at configured breakpoints
      EPIC-LEVEL: Only stops when switching between epics (highest autonomy)
    </description>
    <breakpoints>
      <!-- Breakpoints where agents will stop and ask for confirmation (when YOLO OFF) -->
      <!-- When YOLO ON, agents skip these and proceed automatically -->
      <breakpoint id="1" enabled="true">After completing development, before code review</breakpoint>
      <breakpoint id="2" enabled="true">After code review, before running tests</breakpoint>
      <breakpoint id="3" enabled="true">After tests pass, before user testing</breakpoint>
      <breakpoint id="4" enabled="true">After user testing, before committing</breakpoint>
      <breakpoint id="5" enabled="true">After commit, before pushing to remote</breakpoint>
      <breakpoint id="6" enabled="false">Before making any file changes</breakpoint>
      <breakpoint id="7" enabled="false">Before running any tests</breakpoint>
      <breakpoint id="8" enabled="true">Before major refactoring</breakpoint>
      <breakpoint id="9" enabled="false">After completing epic, before starting next epic</breakpoint>
    </breakpoints>
  </yolo-mode>

  <current-task>
    <id>AUTH-042</id>
    <epic>epic-2-core-features</epic>
    <title>Implement JWT token refresh flow</title>
    <started>2025-10-22T10:00:00Z</started>
    <assigned-to>Main Agent</assigned-to>
    <priority>high</priority>
    <estimated-hours>4</estimated-hours>
  </current-task>

  <completed-tasks>
    <task id="AUTH-040" epic="epic-1-foundation">
      <title>Set up JWT authentication middleware</title>
      <completed>2025-10-21T16:00:00Z</completed>
      <commit-hash>abc123</commit-hash>
    </task>
    <task id="AUTH-041" epic="epic-2-core-features">
      <title>Add login endpoint</title>
      <completed>2025-10-22T09:30:00Z</completed>
      <commit-hash>def456</commit-hash>
    </task>
  </completed-tasks>

  <pending-tasks>
    <task id="AUTH-043" epic="epic-2-core-features">
      <title>Add logout endpoint</title>
      <priority>medium</priority>
      <depends-on>AUTH-042</depends-on>
    </task>
    <task id="AUTH-044" epic="epic-2-core-features">
      <title>Write integration tests</title>
      <priority>high</priority>
      <depends-on>AUTH-042,AUTH-043</depends-on>
    </task>
  </pending-tasks>

  <whats-next>
    <next-task id="AUTH-043" epic="epic-2-core-features">
      <title>Add logout endpoint</title>
      <description>Implement JWT token invalidation and logout</description>
      <estimated-hours>2</estimated-hours>
      <depends-on>AUTH-042</depends-on>
    </next-task>
    <after-that id="AUTH-044" epic="epic-2-core-features">
      <title>Write integration tests</title>
      <priority>high</priority>
    </after-that>
  </whats-next>

  <blockers>
    <blocker id="BLOCK-001">
      <description>Waiting for design approval on error messages</description>
      <raised>2025-10-22T11:00:00Z</raised>
      <severity>medium</severity>
    </blocker>
  </blockers>

  <notes>
    <note timestamp="2025-10-22T14:00:00Z">
      Decided to use httpOnly cookies instead of localStorage for tokens
    </note>
  </notes>
</feature-status>
```

### YOLO Mode Configuration

**For complete YOLO mode documentation, see YOLO_MODE.md template (Section 14 above).**

**Quick Reference:**

- Configure: Use `/yolo` command or message "Enable YOLO mode"
- YOLO OFF: Agents stop at enabled breakpoints for user confirmation
- YOLO ON: Agents proceed automatically, skip all breakpoints
- Configuration stored in `features/[feature-name]/status.xml`

### Reading status.xml (For Agents)

#### How Agents Should Read status.xml

**ALL agents and commands MUST read status.xml to understand current feature state.**

**status.xml contains**: Current task, completed tasks, pending tasks, blockers, YOLO mode, current epic, current story.

**For complete status.xml usage instructions**: See CLAUDE.md "status.xml Management" section created during Phase 5.

#### Phase 0 Enhancement: Agent Workflow with Story Files

**Story Status Lifecycle**:

1. **In Progress**: Story is actively being worked on
2. **Waiting For Review**: All tasks completed, awaiting code review
3. **Done**: Code review passed, story complete

**How `/dev` Command Uses status.xml**:

1. Read `<current-story>` value (e.g., "2.1")
2. Read story file at `docs/development/features/[feature]/epics/[epic]/stories/2.1.md`
3. Check for "## Review Tasks" section (if exists, prioritize FIRST)
4. Work on tasks and check them off (`[ ]` → `[x]`)
5. When ALL tasks complete:
   - Update story **Status** to "Waiting For Review"
   - Update story **Last Updated** timestamp
   - Add note to status.xml

**How `/review` Command Uses status.xml**:

1. Read `<current-story>` value
2. Read story file for acceptance criteria
3. Review code against requirements
4. **If issues found**:
   - Add/Update "## Review Tasks" section in story file
   - Add tasks with priority: Fix/Improvement/Nit
   - Update story **Status** to "In Progress"
   - Update story **Last Updated** timestamp
5. **If no issues**:
   - Update story **Status** to "Done"
   - Update story **Last Updated** timestamp
   - Add completion note to status.xml

**Review Tasks Format**:

```markdown
## Review Tasks

- [ ] Fix: Blocking issue description (`file:line`)
- [ ] Improvement: High priority improvement (`file:line`)
- [ ] Nit: Low priority polish (`file:line`)
```

**Example Workflow**:

```
User: /dev
Agent: Reads story 2.1, works on tasks, completes all
Agent: Updates story Status to "Waiting For Review"

User: /review
Agent: Finds 3 issues
Agent: Adds Review Tasks section to story
Agent: Updates story Status back to "In Progress"

User: /dev
Agent: Prioritizes Review Tasks first
Agent: Fixes all review issues
Agent: Updates story Status to "Waiting For Review"

User: /review
Agent: No issues found
Agent: Updates story Status to "Done"
```

### Template for New Features

#### File Creation

**During project setup:**

- **⚠️ IMPORTANT**: Create `features/` directory
- Create subdirectory for each major feature
- Create `status.xml` in each feature directory
- Initialize with empty tasks

**Template status.xml for new features:**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<feature-status>
  <metadata>
    <feature-name>[Feature Name]</feature-name>
    <last-updated>[ISO 8601 timestamp]</last-updated>
    <current-phase>Planning</current-phase>
    <current-epic>[epic-id or empty]</current-epic>
    <current-story>[epic.story or empty]</current-story>
    <!-- current-story format: epic.story (e.g., 1.1, 2.3) -->
    <!-- Story file location: docs/development/features/[feature-name]/epics/[epic-id]/stories/[epic.story].md -->
    <is-active-feature>true</is-active-feature>
    <!-- Set to true for the feature currently being developed -->
  </metadata>

  <epics>
    <!-- Divide feature into logical epics (groupings of related tasks) -->
    <!-- Each epic has folder: docs/development/features/[feature]/epics/[epic-name]/ -->
    <!-- Each epic folder contains: DESCRIPTION.md, TASKS.md, NOTES.md, stories/ subdirectory -->
    <epic id="epic-1-[name]" status="pending">
      <name>[Epic Name]</name>
      <description>[What this epic accomplishes]</description>
      <folder>docs/development/features/[feature]/epics/epic-1-[name]/</folder>
    </epic>
    <epic id="epic-2-[name]" status="pending">
      <name>[Epic Name]</name>
      <description>[What this epic accomplishes]</description>
      <folder>docs/development/features/[feature]/epics/epic-2-[name]/</folder>
    </epic>
    <!-- Add more epics as needed -->
  </epics>

  <yolo-mode enabled="false">
    <description>YOLO mode OFF: Agents will ask for confirmation before major steps.</description>
    <breakpoints>
      <breakpoint id="1" enabled="true">After completing development, before code review</breakpoint>
      <breakpoint id="2" enabled="true">After code review, before running tests</breakpoint>
      <breakpoint id="3" enabled="true">After tests pass, before user testing</breakpoint>
      <breakpoint id="4" enabled="true">After user testing, before committing</breakpoint>
      <breakpoint id="5" enabled="true">After commit, before pushing to remote</breakpoint>
      <breakpoint id="6" enabled="false">Before making any file changes</breakpoint>
      <breakpoint id="7" enabled="false">Before running any tests</breakpoint>
      <breakpoint id="8" enabled="true">Before major refactoring</breakpoint>
    </breakpoints>
  </yolo-mode>

  <current-task>
    <id>NONE</id>
    <epic>[epic-id]</epic>
    <title>No task currently assigned</title>
  </current-task>

  <completed-tasks></completed-tasks>
  <pending-tasks></pending-tasks>

  <whats-next>
    <next-task id="" epic="[epic-id]">
      <title>[What to work on after current task completes]</title>
      <description>[Brief description]</description>
    </next-task>
  </whats-next>

  <blockers></blockers>
  <notes></notes>
</feature-status>
```

---
