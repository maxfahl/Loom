---
description: Run test suite and analyze results
---

You are now in **TEST MODE** for Jump workspace manager. Time to validate everything works! 🧪

## Test Suites Available

### 1. Unit Tests (Swift Package Manager)

Fast isolated tests for business logic, models, services.

```bash
swift test
```

### 2. E2E Tests (XCUIApplication in TestTools/)

Real UI automation tests with XCUIApplication.

```bash
cd TestTools && ./launch-ui-tests.sh
```

### 3. Specific Test Class

Run one test class:

```bash
swift test --filter WorkspacePersistenceTests
```

### 4. Specific Test Method

Run one test method:

```bash
swift test --filter WorkspacePersistenceTests/testSaveWorkspace
```

## What I'll Do

When you run `/test`, I will:

1. **Run Both Test Suites**
   - Unit tests via `swift test`
   - E2E tests via `cd TestTools && ./launch-ui-tests.sh`

2. **Analyze Results**
   - Total tests: passed/failed counts
   - Failed tests: detailed analysis
   - Test coverage: percentage of code covered
   - Performance: slow tests identified

3. **Validate E2E Integrity**
   - Verify E2E tests use XCUIApplication (no fakes!)
   - Check for "Automation running..." dialog (proves real UI)
   - Ensure tests don't mock UI components

4. **Generate Report**
   - Summary of test health
   - Failures with file:line references
   - Suggestions for fixing failures
   - Coverage gaps if any

## Test Quality Checks

### ✅ Good Tests

- Written BEFORE implementation (TDD)
- Isolated (no shared state between tests)
- Fast (unit tests < 100ms, E2E tests < 5s)
- Clear Given-When-Then structure
- E2E tests use XCUIApplication for real UI automation

### ❌ Bad Tests

- Written AFTER implementation (not TDD)
- Tests leak state (affect other tests)
- Slow tests (> 1s for unit, > 10s for E2E)
- Unclear what's being tested
- Fake "E2E" tests that don't use XCUIApplication

## Example Session

```bash
User: /test
Assistant: Running test suites...

══════════════════════════════════════════════════
UNIT TESTS (Swift Package Manager)
══════════════════════════════════════════════════
Running: swift test

✅ WorkspacePersistenceTests: 12/12 passed
✅ WorkspaceStoreTests: 8/8 passed
✅ ContextDetectorTests: 15/15 passed
✅ TargetManagerTests: 10/10 passed

Total: 45 tests, 45 passed, 0 failed ✅
Duration: 2.3s
Coverage: 87%

══════════════════════════════════════════════════
E2E TESTS (XCUIApplication)
══════════════════════════════════════════════════
Running: cd TestTools && ./launch-ui-tests.sh

Generating Xcode project with XcodeGen...
Building JumpRunnerApp...
Launching UI tests...

✅ "Automation running..." dialog detected (real UI automation confirmed!)

✅ PopoverE2ETests: 25/25 passed
✅ WorkspaceNavigationE2ETests: 18/18 passed
✅ ShortcutRecordingE2ETests: 12/12 passed
✅ SettingsE2ETests: 8/8 passed

Total: 63 tests, 63 passed, 0 failed ✅
Duration: 45s
Results: TestResults/UI.xcresult

══════════════════════════════════════════════════
OVERALL TEST REPORT
══════════════════════════════════════════════════

✅ Unit Tests: 45 passed
✅ E2E Tests: 63 passed
✅ Total: 108 tests passed
✅ Coverage: 87% (target: 80%+)
✅ E2E Integrity: CONFIRMED (real XCUIApplication automation)

🎉 ALL TESTS PASSING! Ready to ship.

💡 Suggestions:
- No issues detected
- Coverage above target
- All E2E tests using real UI automation

══════════════════════════════════════════════════
```

## Example with Failures

````bash
User: /test
Assistant: Running test suites...

══════════════════════════════════════════════════
UNIT TESTS
══════════════════════════════════════════════════

❌ WorkspacePersistenceTests: 11/12 passed, 1 FAILED

FAILED: testSaveWorkspaceWithInvalidPermissions
  Location: Tests/Jump/WorkspacePersistenceTests.swift:45
  Reason: XCTAssertEqual failed: ("0644") is not equal to ("0600")

  Issue: File permissions not set correctly
  Expected: 0600 (read/write owner only)
  Actual: 0644 (read for group/others)

  Fix: Update WorkspacePersistence.swift:78 to set correct permissions:
  ```swift
  try FileManager.default.setAttributes(
      [.posixPermissions: 0o600],
      ofItemAtPath: fileURL.path
  )
````

Total: 45 tests, 44 passed, 1 failed ❌

══════════════════════════════════════════════════
DECISION: BLOCK MERGE ❌
══════════════════════════════════════════════════

Fix failing test before proceeding.

Would you like me to fix this? (yes/no)

````

## Test Options

### Run Specific Suite
```bash
/test unit       # Unit tests only
/test e2e        # E2E tests only
/test all        # Both (default)
````

### Run with Coverage

```bash
/test --coverage
```

### Run Specific Story Tests

```bash
/test story-2.1
```

### Watch Mode (Continuous Testing)

```bash
/test --watch
```

## Performance Targets

- **Unit Tests**: < 100ms per test
- **E2E Tests**: < 5s per test
- **Total Unit Suite**: < 10s
- **Total E2E Suite**: < 2 minutes
- **Coverage**: > 80%

## TDD Enforcement

The `/test` command validates TDD compliance:

- ✅ Tests exist for all new code
- ✅ Tests were committed BEFORE implementation (git log check)
- ✅ E2E tests use XCUIApplication (no fakes)
- ❌ Blocks merge if tests missing or fake

---

**Tests are your safety net. Never skip them!** 🧪
