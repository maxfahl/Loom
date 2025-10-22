---
description: Create a new story file with proper structure
---

You are now in **STORY CREATION MODE** for Jump workspace manager. Let's define some work! 📄

## What I'll Do

When you run `/create-story`, I will:

1. **Gather Story Information**
   - Epic number and story number
   - Story title
   - Story description
   - Acceptance criteria
   - Estimate

2. **Create Story File**
   - `docs/stories/story-X.Y.md`
   - Proper markdown structure
   - All required sections

3. **Create Story Context XML**
   - `docs/stories/story-X.Y-context.xml`
   - Link to epic
   - Reference implementation details
   - Map to codebase structure

4. **Update Tracking**
   - Add to epic story list
   - Update epic progress
   - Link to technical spec

## Story File Template

```markdown
# Story X.Y: <Title>

## Epic

**Epic X**: <Epic Name>

## Status

Not Started | In Progress | Testing | Review | Done

## Description

<Clear description of what needs to be built and why>

## Acceptance Criteria

1. **AC#1**: <Specific, testable criterion>
   - Given: <context>
   - When: <action>
   - Then: <expected result>

2. **AC#2**: <Next criterion>
   - Given: <context>
   - When: <action>
   - Then: <expected result>

3. **AC#3**: <Next criterion>
   - Given: <context>
   - When: <action>
   - Then: <expected result>

## Technical Notes

- Implementation approach: <high-level approach>
- Key technologies: <Swift features, frameworks>
- Dependencies: <what must exist first>

## Testing Requirements

- **Unit Tests**: <what to test>
- **E2E Tests**: <UI automation tests if applicable>
- **Test Coverage**: Target 80%+

## Estimate

<X-Y hours>

## Prerequisites

- [ ] story-X.Y-1 complete
- [ ] Component ABC exists
- [ ] Design mockups available

## Definition of Done

- [ ] All AC met and tested
- [ ] Unit tests pass (80%+ coverage)
- [ ] E2E tests pass (if UI changes)
- [ ] Code reviewed and approved
- [ ] Documentation updated
- [ ] Story Context XML updated
```

## Story Context XML Template

```xml
<?xml version="1.0" encoding="UTF-8"?>
<story-context>
  <story-id>story-X.Y</story-id>
  <epic>Epic X - <Epic Name></epic>
  <title><Story Title></title>

  <acceptance-criteria>
    <criterion id="1">
      <description><AC#1 description></description>
      <test-file>Tests/Jump/<ComponentTests>.swift</test-file>
      <test-method>test<Scenario>()</test-method>
    </criterion>
    <criterion id="2">
      <description><AC#2 description></description>
      <test-file>Tests/Jump/<ComponentTests>.swift</test-file>
      <test-method>test<Scenario>()</test-method>
    </criterion>
  </acceptance-criteria>

  <implementation-details>
    <file path="Sources/Jump/<Component>.swift">
      <component name="<ComponentName>" line="<line>">
        <description><What this component does></description>
        <key-methods>
          <method name="<methodName>" line="<line>"><Description></method>
        </key-methods>
        <dependencies>
          <dependency><Protocol or service name></dependency>
        </dependencies>
      </component>
    </file>
  </implementation-details>

  <technical-decisions>
    <decision>
      <question><What was decided?></question>
      <answer><The decision></answer>
      <rationale><Why this decision?></rationale>
    </decision>
  </technical-decisions>

  <related-documentation>
    <doc type="tech-spec">docs/development/TECHNICAL_SPEC.md#epic-X</doc>
    <doc type="architecture">docs/development/ARCHITECTURE.md#<component></doc>
  </related-documentation>
</story-context>
```

## Example Sessions

### Example 1: Interactive Story Creation

```bash
User: /create-story
Assistant:
══════════════════════════════════════════════════
STORY CREATION WIZARD
══════════════════════════════════════════════════

Let's create a new story!

[1/6] Which epic is this story for?
Available epics:
1. Epic 1: Core Workspace Jump (✅ COMPLETE)
2. Epic 2: State Persistence (🚧 IN PROGRESS - 30% complete)
3. Epic 3: Settings UI & Theme (📋 PLANNED)
4. Epic 4: Filtering & Browsers (📋 PLANNED)
5. Epic 5: Performance & Reliability (📋 PLANNED)

Enter epic number (2-5):
```

```
User: 2
Assistant:
Epic 2 selected: State Persistence

Current stories in Epic 2:
- story-2.1: Persist workspaces to JSON (✅ Done)
- story-2.2: Load workspaces on app launch (✅ Done)
- story-2.3: Handle workspace updates (🚧 In Progress)

[2/6] What's the next story number?
Suggested: story-2.4

Enter story number:
```

```
User: 2.4
Assistant:
[3/6] What's the story title?
Format: "<Action> <Subject>"
Examples:
- "Persist workspaces to JSON"
- "Detect active application context"
- "Implement keyboard shortcut recording"

Enter title:
```

```
User: Handle file corruption gracefully
Assistant:
[4/6] What's the story description?
Describe WHAT needs to be built and WHY.

Enter description (or 'help' for tips):
```

```
User: When the workspace JSON file is corrupted or invalid, Jump should detect this gracefully, create a backup of the corrupted file, and initialize with empty workspace state instead of crashing. This ensures users never lose access to the app even if data corruption occurs.
Assistant:
[5/6] What are the acceptance criteria?
Enter AC one at a time (enter 'done' when finished):

AC#1:
```

```
User: JSON file corruption is detected during load
Assistant: AC#2:
```

```
User: Corrupted file is backed up to .corrupted-TIMESTAMP extension
Assistant: AC#3:
```

```
User: App initializes with empty workspace state
Assistant: AC#4:
```

```
User: User is notified about corruption and backup location
Assistant: AC#5:
```

```
User: done
Assistant:
[6/6] Estimate (in hours)?
Consider: AC analysis + TDD (RED-GREEN-REFACTOR) + testing + docs

Suggested based on 4 AC: 6-8 hours

Enter estimate:
```

```
User: 6-8
Assistant:
══════════════════════════════════════════════════
STORY CREATED! ✅
══════════════════════════════════════════════════

Created files:
- docs/stories/story-2.4.md
- docs/stories/story-2.4-context.xml

Story Details:
- ID: story-2.4
- Epic: 2 - State Persistence
- Title: Handle file corruption gracefully
- AC: 4 criteria
- Estimate: 6-8 hours
- Status: Not Started

Updated:
- docs/development/TECHNICAL_SPEC.md (Epic 2 section)
- features/epic-2-state-persistence/status.xml (added story-2.4)

Next Steps:
1. Review story: cat docs/stories/story-2.4.md
2. Create feature branch: /create-feature story-2.4
3. Start development: /dev story-2.4
4. Or go autonomous: /yolo story-2.4

Ready to ship! 🚀
```

### Example 2: Quick Story Creation

```bash
User: /create-story 2.5 "Implement workspace migration on load" --quick
Assistant:
══════════════════════════════════════════════════
QUICK STORY CREATION
══════════════════════════════════════════════════

Creating story-2.5 with defaults...

✅ Created docs/stories/story-2.5.md
✅ Created docs/stories/story-2.5-context.xml
✅ Added to Epic 2 tracking
✅ Linked to technical spec

Story ready! Edit manually or start development.

/dev story-2.5
```

### Example 3: Story from Template

```bash
User: /create-story --from-epic-plan 2
Assistant:
══════════════════════════════════════════════════
CREATING STORIES FROM EPIC PLAN
══════════════════════════════════════════════════

Reading Epic 2 plan from docs/development/TECHNICAL_SPEC.md...

Found 10 planned stories. Current: 3 exist, 7 to create.

Creating story-2.4...
✅ Handle file corruption gracefully

Creating story-2.5...
✅ Implement workspace migration

Creating story-2.6...
✅ Add file write retry logic

Creating story-2.7...
✅ Optimize JSON serialization

Creating story-2.8...
✅ Add workspace export feature

Creating story-2.9...
✅ Add workspace import feature

Creating story-2.10...
✅ Handle concurrent file access

══════════════════════════════════════════════════
EPIC 2 STORIES COMPLETE! ✅
══════════════════════════════════════════════════

Created: 7 story files (2.4 - 2.10)
Total Epic 2 Stories: 10
Ready for development!

Start with: /dev story-2.4
```

## Story Quality Guidelines

### ✅ Good Stories

- **Clear AC**: Specific, testable criteria
- **Right-sized**: 4-8 hours of work
- **Independent**: Minimal dependencies
- **Testable**: Clear pass/fail conditions
- **Valuable**: Delivers user/business value

### ❌ Bad Stories

- **Vague AC**: "Should work well"
- **Too big**: > 16 hours of work
- **Dependent**: Blocked by many others
- **Untestable**: No clear validation
- **Technical tasks**: "Refactor X" (not user value)

## Story Types

### Feature Stories

User-facing functionality:

- "Persist workspaces to JSON"
- "Detect active application context"
- "Record keyboard shortcuts"

### Bug Stories

Fix defects:

- "Fix crash on invalid JSON"
- "Correct permission handling"

### Tech Debt Stories

Improve codebase:

- "Extract persistence protocol"
- "Refactor context detection"

### Spike Stories

Time-boxed investigation:

- "Research CoreData vs JSON"
- "Evaluate accessibility APIs"

## Integration with TDD

Every story is designed for TDD:

- AC map to test cases (RED phase)
- Implementation follows tests (GREEN phase)
- Refactoring improves quality (REFACTOR phase)
- Story Context XML links tests to code

---

**Every great feature starts with a well-defined story!** 📄

```

```
