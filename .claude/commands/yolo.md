---
description: Autonomous mode - Implement complete story from start to finish
---

You are now in **YOLO MODE** 🚀 (You Only Loom Once)

## ⚠️ WARNING: FULLY AUTONOMOUS MODE

In YOLO mode, I will:

1. Read the story and understand ALL acceptance criteria
2. Plan the complete TDD implementation
3. Write ALL tests (RED phase)
4. Implement ALL code (GREEN phase)
5. Refactor for quality (REFACTOR phase)
6. Run full test suite
7. Generate documentation
8. Create conventional commits
9. Request code review
10. Fix any issues found
11. **Ship it** ✅

You will **NOT** be asked for approval at each step.

I will only stop if:

- Tests fail and I can't fix them
- Critical errors occur
- Architecture decision needed
- Ambiguous requirements

## Safety Guarantees

Even in YOLO mode, I WILL NEVER:

- Skip writing tests
- Implement before tests (TDD is sacred)
- Use force unwraps (!)
- Use force casts (as!)
- Create fake E2E tests (must use XCUIApplication)
- Ignore test failures
- Skip code review

## Prerequisites

Before running YOLO mode:

- [ ] Story file exists (docs/stories/story-X.Y.md)
- [ ] Story Context XML exists (docs/stories/story-X.Y-context.xml)
- [ ] All prerequisites complete
- [ ] No blockers
- [ ] Clear acceptance criteria

## Workflow

```
YOLO MODE ACTIVATED 🚀
│
├─ 1. READ STORY
│   └─ Parse acceptance criteria
│   └─ Identify dependencies
│   └─ Estimate complexity
│
├─ 2. PLAN IMPLEMENTATION
│   └─ Break down AC into tasks
│   └─ Design TDD approach
│   └─ Identify test cases
│
├─ 3. RED PHASE (Tests First)
│   └─ Write all failing tests
│   └─ Verify tests fail
│   └─ Commit: "test(scope): add failing tests"
│
├─ 4. GREEN PHASE (Implement)
│   └─ Implement minimum code to pass
│   └─ Verify tests pass
│   └─ Commit: "feat(scope): implement AC#X"
│
├─ 5. REFACTOR PHASE (Clean Up)
│   └─ Improve code quality
│   └─ Verify tests still pass
│   └─ Commit: "refactor(scope): improve implementation"
│
├─ 6. RUN FULL TEST SUITE
│   └─ swift test (unit tests)
│   └─ cd TestTools && ./launch-ui-tests.sh (E2E)
│   └─ Verify 100% pass rate
│
├─ 7. DOCUMENTATION
│   └─ Add /// code comments
│   └─ Update Story Context XML
│   └─ Update ARCHITECTURE.md if needed
│
├─ 8. CODE REVIEW
│   └─ Request reviews from specialists
│   └─ Fix any issues found
│   └─ Verify compliance
│
├─ 9. FINAL VALIDATION
│   └─ All AC met ✅
│   └─ All tests pass ✅
│   └─ Code reviewed ✅
│   └─ Docs updated ✅
│
└─ 10. SHIP IT! 🎉
    └─ Update story status to "Review"
    └─ Report completion
```

## Example Session

```bash
User: /yolo story-2.1
Assistant:
🚀 YOLO MODE ACTIVATED for story-2.1
══════════════════════════════════════════════════

[1/10] READING STORY...
Story: Persist workspaces to JSON
Epic: 2 - State Persistence
AC: 3 criteria
Estimate: 6 hours

[2/10] PLANNING IMPLEMENTATION...
TDD Plan created: 3 AC × 3 phases = 9 steps
Tests: WorkspacePersistenceTests.swift
Implementation: Sources/Jump/Services/WorkspacePersistence.swift

[3/10] RED PHASE - Writing failing tests...
✅ Created Tests/Jump/WorkspacePersistenceTests.swift
✅ testSaveWorkspaceToJSON - FAILS ✅ (expected)
✅ testJSONFormatMatchesCodeable - FAILS ✅ (expected)
✅ testFilePermissions0600 - FAILS ✅ (expected)
✅ Committed: "test(persistence): add failing tests for workspace save"

[4/10] GREEN PHASE - Implementing...
✅ Created Sources/Jump/Services/WorkspacePersistence.swift
✅ Implemented save() method with Result<Void, JumpError>
✅ Implemented Codable JSON serialization
✅ Set file permissions to 0600
✅ All tests now PASS ✅
✅ Committed: "feat(persistence): implement workspace save to JSON"

[5/10] REFACTOR PHASE - Cleaning up...
✅ Extracted encoder configuration
✅ Improved error messages
✅ Added code comments
✅ Tests still PASS ✅
✅ Committed: "refactor(persistence): improve code quality"

[6/10] RUNNING FULL TEST SUITE...
Unit Tests: 148 → 151 passed ✅
E2E Tests: 148 passed ✅
Coverage: 87% → 89% ✅

[7/10] UPDATING DOCUMENTATION...
✅ Added /// comments to WorkspacePersistence
✅ Updated docs/stories/story-2.1-context.xml
✅ Updated docs/development/ARCHITECTURE.md
✅ Updated docs/development/TECHNICAL_SPEC.md

[8/10] REQUESTING CODE REVIEW...
Coordinating specialist reviews...
[🦅 Swift Specialist: APPROVE ✅]
[🏗️ Architecture Advisor: APPROVE ✅]
[🔍 Code Reviewer: APPROVE ✅]

No issues found!

[9/10] FINAL VALIDATION...
✅ All AC met
✅ All tests pass
✅ Code reviewed and approved
✅ Docs updated
✅ TDD workflow followed

[10/10] SHIPPING! 🎉
✅ Updated story-2.1 status: In Progress → Review
✅ Ready for merge

══════════════════════════════════════════════════
STORY COMPLETE: story-2.1 ✅
══════════════════════════════════════════════════

Duration: 47 minutes
Commits: 3 (test → feat → refactor)
Tests Added: 3
Lines of Code: 156
Coverage Impact: +2%

Epic 2 Progress: 20% → 30%

Next Story: story-2.2 - Load workspaces on app launch

Ready to continue? (/yolo story-2.2)
```

## When to Use YOLO Mode

### ✅ Good Use Cases

- **Clear requirements** - All AC well-defined
- **No blockers** - All prerequisites complete
- **Standard patterns** - Using familiar tech
- **Confidence** - You trust the autonomous workflow

### ❌ Avoid YOLO Mode When

- **Ambiguous requirements** - AC unclear or contradictory
- **Research needed** - Unknown technical territory
- **Architecture decisions** - Need human input on design
- **Critical changes** - High-risk modifications

## YOLO Mode Options

```bash
/yolo story-X.Y              # Implement single story
/yolo epic-X                 # Implement entire epic (brave!)
/yolo story-X.Y --skip-review # Skip code review (not recommended!)
/yolo story-X.Y --dry-run    # Show plan without executing
```

## Monitoring Progress

I'll provide real-time updates:

- ✅ Steps completed
- ⏳ Current step
- ⏸️ Paused (waiting for resolution)
- ❌ Blocked (need human intervention)

## Emergency Stop

At any point, you can:

- Type "stop" to pause
- Review current progress
- Make decisions on blockers
- Resume or abort

## Post-YOLO Report

After completion, you'll get:

```markdown
# YOLO Mode Completion Report

## Story: story-X.Y

Status: ✅ Complete

## Metrics

- Duration: X minutes
- Commits: Y
- Tests Added: Z
- Coverage Impact: +N%

## Changes

- Files Created: [list]
- Files Modified: [list]
- Tests Added: [list]

## Quality Checks

- ✅ All AC met
- ✅ All tests pass
- ✅ Code reviewed
- ✅ Docs updated
- ✅ TDD followed

## Next Steps

- Ready for merge
- Next story: story-X.Y+1
```

---

**YOLO = You Only Loom Once. Make it count!** 🚀

⚠️ **Use responsibly**: YOLO mode is powerful but requires well-defined stories with clear AC. When in doubt, use `/dev` for step-by-step control.

```

```
