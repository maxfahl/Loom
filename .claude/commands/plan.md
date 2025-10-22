---
description: Plan implementation for a story or epic
---

You are now in **PLANNING MODE** for Jump workspace manager. Let's break down the work! 📋

## What I'll Help You Plan

### 1. Story Implementation Plan

Break a story into concrete tasks following TDD:

- Acceptance criteria analysis
- Test cases to write (RED phase)
- Implementation steps (GREEN phase)
- Refactoring opportunities (REFACTOR phase)
- Time estimates
- Dependencies

### 2. Epic Implementation Plan

Break an epic into story sequence:

- Story prioritization
- Dependencies between stories
- Parallel work opportunities
- Checkpoint criteria validation points
- Epic timeline estimate

### 3. Technical Spike Plan

Investigate unknown technical areas:

- Research questions to answer
- Prototypes to build
- Technologies to evaluate
- Decision criteria
- Time-boxed investigation

## Story Planning Template

When you run `/plan story-X.Y`, I'll create:

````markdown
# Story Implementation Plan: story-X.Y

## Overview

- **Epic**: X - <Epic Name>
- **Story**: <Story Title>
- **Estimate**: X-Y hours
- **Status**: Not Started

## Acceptance Criteria

1. <AC #1>
2. <AC #2>
3. <AC #3>

## Dependencies

- ✅ story-X.Y-1 complete
- ✅ Component ABC exists
- ⏸️ Design mockups (waiting)

## TDD Implementation Plan

### AC#1: <Acceptance Criterion>

#### RED Phase (Write Failing Test)

**Test File**: `Tests/Jump/<Component>Tests.swift`
**Test Method**: `test<Scenario>()`

```swift
func test<Scenario>() {
    // Given: <setup>
    // When: <action>
    // Then: <assertion that will fail>
}
```
````

**Estimated**: 30 minutes

#### GREEN Phase (Implement)

**File**: `Sources/Jump/<Component>.swift`
**Changes**:

1. Add <property/method>
2. Implement <logic>
3. Handle <edge cases>

**Estimated**: 1 hour

#### REFACTOR Phase (Clean Up)

**Improvements**:

1. Extract <repeated code>
2. Improve <readability>
3. Optimize <performance>

**Estimated**: 30 minutes

---

### AC#2: <Next Criterion>

[Repeat structure]

---

## Total Estimate

- RED phases: 1.5 hours
- GREEN phases: 3 hours
- REFACTOR phases: 1.5 hours
- **Total**: 6 hours

## Technical Notes

- Uses Result<T, JumpError> for error handling
- Codable for JSON serialization
- @Published for reactive state
- MainActor for UI updates

## Risks & Mitigation

- **Risk**: File I/O might fail
  **Mitigation**: Comprehensive error handling with Result pattern

- **Risk**: JSON schema might change
  **Mitigation**: Version field in JSON for migration

## Success Criteria

- [ ] All AC tests pass
- [ ] Unit test coverage > 80%
- [ ] E2E tests use XCUIApplication (if UI changes)
- [ ] Code reviewed and approved
- [ ] Documentation updated

````

## Epic Planning Template

When you run `/plan epic-X`, I'll create:

```markdown
# Epic Implementation Plan: Epic X - <Epic Name>

## Overview
- **Epic**: X - <Epic Name>
- **Stories**: Y total
- **Estimate**: Z weeks
- **Status**: Planned

## Story Sequencing

### Phase 1: Foundation (Week 1-2)
1. **story-X.1** - <Title> (4 hours)
   - Prerequisites: None
   - Deliverable: <Core component>

2. **story-X.2** - <Title> (6 hours)
   - Prerequisites: story-X.1
   - Deliverable: <Integration>

### Phase 2: Features (Week 3-4)
3. **story-X.3** - <Title> (8 hours)
   - Prerequisites: story-X.2
   - Deliverable: <Feature A>

4. **story-X.4** - <Title> (8 hours)
   - Prerequisites: story-X.2 (can run parallel with X.3!)
   - Deliverable: <Feature B>

### Phase 3: Polish (Week 5)
5. **story-X.5** - <Title> (6 hours)
   - Prerequisites: story-X.3, story-X.4
   - Deliverable: <Integration + UX polish>

## Parallel Work Opportunities
- story-X.3 and story-X.4 can run in parallel (different components)
- story-X.7 and story-X.8 can run in parallel (isolated features)

## Checkpoint Criteria
After this epic, validate:
- [ ] <Checkpoint criterion 1>
- [ ] <Checkpoint criterion 2>
- [ ] Performance: <target>
- [ ] Test coverage: > 80%

## Timeline
- **Start**: Week 1
- **Foundation Complete**: End of Week 2
- **Features Complete**: End of Week 4
- **Epic Complete**: End of Week 5
- **Checkpoint Validation**: Week 6

## Risks
- <Risk>: <Mitigation>
````

## Example Sessions

### Example 1: Plan a Story

```bash
User: /plan story-2.1
Assistant: Reading story-2.1 details...

Story: Persist workspaces to JSON
Epic: 2 - State Persistence
Status: Not Started

Creating detailed implementation plan...

[Generates complete plan with TDD breakdown]

Plan saved to: docs/plans/story-2.1-plan.md

Would you like to start implementation? (/dev story-2.1)
```

### Example 2: Plan an Epic

```bash
User: /plan epic-2
Assistant: Analyzing Epic 2: State Persistence...

Stories: 10 total
Estimated: 4-6 weeks
Dependencies: Epic 1 complete ✅

Creating epic roadmap with story sequencing...

[Generates complete epic plan]

Plan saved to: docs/plans/epic-2-plan.md

Ready to start? (/dev story-2.1)
```

### Example 3: Plan Technical Spike

```bash
User: /plan spike "Evaluate CoreData vs JSON persistence"
Assistant: Creating technical spike plan...

Research Questions:
1. What's the performance difference?
2. What's the migration complexity?
3. What's the testing complexity?

Time-boxed: 4 hours

[Generates spike plan with research tasks]

Plan saved to: docs/spikes/persistence-evaluation.md
```

## Planning Best Practices

### ✅ Good Plans

- Break work into < 8 hour chunks
- Identify dependencies explicitly
- Estimate time realistically
- Include testing time
- Consider refactoring time
- Document technical decisions

### ❌ Bad Plans

- Massive stories (> 16 hours)
- Ignore dependencies
- Underestimate testing time
- Skip refactoring phase
- Assume everything works first try

## Integration with TDD

Every plan enforces TDD:

- RED phase comes first (tests)
- GREEN phase implements minimum code
- REFACTOR phase improves quality
- Each phase has time estimate
- Each phase has clear deliverable

## Planning Tools

I can help with:

- **/plan story-X.Y** - Detailed story plan
- **/plan epic-X** - Epic roadmap
- **/plan spike "topic"** - Technical investigation
- **/plan refactor <component>** - Refactoring plan
- **/plan performance <target>** - Performance optimization plan

---

**Proper planning prevents poor performance!** 📋
