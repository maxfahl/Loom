---
description: Create a new feature branch with proper setup
---

You are now in **FEATURE CREATION MODE** for Jump workspace manager. Let's set up a new feature! 🌿

## What I'll Do

When you run `/create-feature`, I will:

1. **Validate Prerequisites**
   - Ensure working directory is clean
   - Verify on main branch
   - Check for uncommitted changes

2. **Create Feature Structure**
   - Create git branch: `epic/X-name` or `story/X.Y-name`
   - Create feature tracking directory (if epic)
   - Set up status tracking

3. **Initialize Documentation**
   - Create feature plan document
   - Set up story templates (if epic)
   - Link to relevant docs

4. **Prepare Environment**
   - Switch to new branch
   - Create initial commit
   - Set up tracking

## Branch Naming Convention

### Epic Branches

```
epic/2-state-persistence
epic/3-settings-ui-theme
epic/4-filtering-browsers
epic/5-performance-reliability
```

### Story Branches

```
story/2.1-workspace-persistence
story/2.2-load-on-launch
story/3.1-settings-window
```

## Feature Directory Structure

For epics, creates:

```
features/epic-X-name/
├── status.xml          # Epic progress tracking
├── plan.md             # Epic implementation plan
├── stories/            # Story templates
│   ├── story-X.1.md
│   ├── story-X.2.md
│   └── ...
└── notes.md            # Development notes
```

## Status XML Format

```xml
<epic-status>
  <epic-id>2</epic-id>
  <name>State Persistence</name>
  <status>In Progress</status>
  <progress>
    <total-stories>10</total-stories>
    <completed-stories>2</completed-stories>
    <percentage>20</percentage>
  </progress>
  <current-story>story-2.3</current-story>
  <blockers>
    <!-- None currently -->
  </blockers>
  <last-updated>2025-01-15</last-updated>
</epic-status>
```

## Example Sessions

### Example 1: Create Epic Feature

```bash
User: /create-feature epic-2
Assistant:
══════════════════════════════════════════════════
FEATURE CREATION: Epic 2 - State Persistence
══════════════════════════════════════════════════

[1/5] VALIDATING PREREQUISITES...
✅ Working directory clean
✅ On main branch
✅ No uncommitted changes

[2/5] CREATING FEATURE BRANCH...
✅ Created branch: epic/2-state-persistence
✅ Switched to new branch

[3/5] INITIALIZING FEATURE STRUCTURE...
✅ Created features/epic-2-state-persistence/
✅ Created status.xml
✅ Created plan.md
✅ Created stories/ directory
✅ Generated 10 story templates

[4/5] LINKING DOCUMENTATION...
✅ Linked to docs/development/TECHNICAL_SPEC.md (Epic 2 section)
✅ Linked to docs/development/TESTING_STRATEGY.md (checkpoints)
✅ Added quick commands to plan.md

[5/5] FINALIZING SETUP...
✅ Initial commit: "feat(epic-2): initialize State Persistence epic"
✅ Feature branch ready

══════════════════════════════════════════════════
EPIC FEATURE READY! 🎉
══════════════════════════════════════════════════

Branch: epic/2-state-persistence
Directory: features/epic-2-state-persistence/
Stories: 10 planned

Next Steps:
1. Review plan: features/epic-2-state-persistence/plan.md
2. Start first story: /create-feature story-2.1
3. Or jump straight in: /dev story-2.1

Ready to build! 🚀
```

### Example 2: Create Story Feature

```bash
User: /create-feature story-2.1
Assistant:
══════════════════════════════════════════════════
FEATURE CREATION: story-2.1 - Persist workspaces to JSON
══════════════════════════════════════════════════

[1/4] VALIDATING PREREQUISITES...
✅ On epic/2-state-persistence branch
✅ Working directory clean
✅ Epic feature initialized

[2/4] CREATING STORY BRANCH...
✅ Created branch: story/2.1-workspace-persistence
✅ Branched from: epic/2-state-persistence

[3/4] PREPARING STORY CONTEXT...
✅ Loaded story file: docs/stories/story-2.1.md
✅ Loaded Story Context XML: docs/stories/story-2.1-context.xml
✅ Validated all AC are clear

[4/4] READY FOR DEVELOPMENT...
✅ Branch ready
✅ TDD workflow initialized

══════════════════════════════════════════════════
STORY FEATURE READY! 🎉
══════════════════════════════════════════════════

Branch: story/2.1-workspace-persistence
Story: docs/stories/story-2.1.md
Context: docs/stories/story-2.1-context.xml

Acceptance Criteria:
1. Workspaces saved to JSON file
2. JSON format matches Codable schema
3. File permissions set to 0600

Next Steps:
1. Review story: cat docs/stories/story-2.1.md
2. Start TDD: /dev story-2.1
3. Or go autonomous: /yolo story-2.1

Let's ship it! 🚀
```

### Example 3: Create Custom Feature

```bash
User: /create-feature spike/performance-investigation
Assistant:
══════════════════════════════════════════════════
FEATURE CREATION: spike/performance-investigation
══════════════════════════════════════════════════

[1/3] VALIDATING PREREQUISITES...
✅ Working directory clean
✅ On main branch

[2/3] CREATING SPIKE BRANCH...
✅ Created branch: spike/performance-investigation
✅ Switched to new branch

[3/3] SETTING UP SPIKE...
✅ Created docs/spikes/performance-investigation.md
✅ Added investigation template
✅ Set time-box: 4 hours

══════════════════════════════════════════════════
SPIKE READY! 🔬
══════════════════════════════════════════════════

Branch: spike/performance-investigation
Document: docs/spikes/performance-investigation.md
Time-box: 4 hours

Investigation Questions:
1. What's the current latency baseline?
2. Where are the bottlenecks?
3. What optimization strategies are viable?

Start investigating! 🔬
```

## Feature Types

### Epic Features

- Long-lived branches
- Multiple stories
- Feature directory created
- Status tracking enabled

### Story Features

- Short-lived branches
- Single story focus
- Branch from epic
- Merge back to epic when done

### Spike Features

- Time-boxed investigation
- No production code
- Merge conclusions to docs
- Delete branch after

### Refactor Features

- Code quality improvements
- Tests must stay green
- No behavior changes
- Merge to main when done

## Options

```bash
/create-feature epic-X              # Create epic feature
/create-feature story-X.Y           # Create story feature
/create-feature spike/name          # Create investigation spike
/create-feature refactor/name       # Create refactoring feature
/create-feature feature/name        # Create custom feature
```

## Git Workflow

```
main
├── epic/2-state-persistence
│   ├── story/2.1-workspace-persistence  (merge to epic when done)
│   ├── story/2.2-load-on-launch         (merge to epic when done)
│   └── ... (merge epic to main when all stories done)
│
├── epic/3-settings-ui-theme
│   └── ...
│
└── spike/performance-investigation  (merge conclusions, delete branch)
```

## Cleanup After Completion

```bash
# After story merged to epic
git branch -d story/2.1-workspace-persistence

# After epic merged to main
git branch -d epic/2-state-persistence

# After spike conclusions documented
git branch -D spike/performance-investigation
```

---

**Start every feature with a clean slate!** 🌿
