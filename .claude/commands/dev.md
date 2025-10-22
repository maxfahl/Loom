---
description: Start development on a story with FULLY ENFORCED TDD workflow
---

You are now in **DEV MODE** for Jump workspace manager. 🚀

## Your Mission

Implement a story using **FULLY ENFORCED TDD** workflow:

1. **RED** - Write failing test FIRST
2. **GREEN** - Implement minimum code to pass
3. **REFACTOR** - Clean up while keeping tests green

## Critical Rules

### ❌ FORBIDDEN

- NO implementation before tests
- NO skipping the RED phase
- NO force unwraps (!)
- NO force casts (as!)
- NO fake E2E tests (must use XCUIApplication)

### ✅ REQUIRED

- Tests MUST be written BEFORE implementation
- E2E tests MUST use XCUIApplication in TestTools/
- All code must use Result<T,Error> pattern
- All models must be Codable
- All SwiftUI state management must use proper property wrappers

## Story Context Authority

Story Context XML is your **single source of truth**. Read it FIRST:

```bash
ls docs/stories/*.xml
```

## TDD Workflow

### Phase 1: RED (Write Failing Test)

1. Read Story Context XML for acceptance criteria
2. Choose ONE acceptance criterion to implement
3. Write a failing test that validates this criterion
4. Run tests - verify it FAILS (proves test is valid)
5. Commit: `git commit -m "test(story-X.Y): add failing test for AC#Z"`

### Phase 2: GREEN (Implement)

1. Write MINIMUM code to pass the test
2. Run tests - verify it PASSES
3. Commit: `git commit -m "feat(story-X.Y): implement AC#Z"`

### Phase 3: REFACTOR (Clean Up)

1. Improve code quality while keeping tests green
2. Run tests - verify still PASSES
3. Commit: `git commit -m "refactor(story-X.Y): clean up AC#Z implementation"`

### Repeat

Repeat RED-GREEN-REFACTOR for each acceptance criterion until story is complete.

## Quick Commands

**Check what's next:**

```bash
/status
```

**Run tests:**

```bash
# Unit tests
swift test

# E2E tests (XCUIApplication)
cd TestTools && ./launch-ui-tests.sh
```

**Review code:**

```bash
/review
```

**Create conventional commit:**

```bash
/commit
```

## Story Status Progression

- `Not Started` → `In Progress` (when you start)
- `In Progress` → `Testing` (when implementation done)
- `Testing` → `Review` (when tests pass)
- `Review` → `Done` (when approved)

## Swift Best Practices Reminder

- **No force unwraps**: Use guard, if-let, or ?? instead of !
- **Result pattern**: Return Result<T, JumpError> instead of throwing
- **Codable**: All models must conform to Codable
- **Protocol-oriented**: Design with protocols first
- **Combine**: Use @Published for reactive state
- **Async/await**: Use modern concurrency for async operations
- **MainActor**: Ensure UI updates on main thread

## Example Session

```bash
User: /dev story-2.1
Assistant: Reading Story Context XML for story-2.1...

         Story: Persist workspaces to JSON
         Epic: 2 - State Persistence
         Status: Not Started

         Acceptance Criteria:
         1. Workspaces saved to ~/Library/Application Support/Jump/workspaces.json
         2. JSON format matches Workspace Codable schema
         3. File created with correct permissions (0600)

         Starting TDD cycle for AC#1...

         🔴 RED: Writing failing test...
         [Creates test file]

         ✅ Test fails (as expected). Ready to implement.

         🟢 GREEN: Implementing minimum code to pass...
         [Implements code]

         ✅ Test passes! Ready to refactor.

         🔵 REFACTOR: Cleaning up implementation...
         [Refactors code]

         ✅ Tests still pass! AC#1 complete.

         Moving to AC#2...
```

## Need Help?

- **/status** - Show current epic/story progress
- **/test** - Run test suite and analyze results
- **/review** - Get code review from specialists
- **/docs** - Update documentation for changes

---

**Remember**: Tests FIRST, code SECOND. No exceptions. This is the way. 🧪➡️💻

```

```
