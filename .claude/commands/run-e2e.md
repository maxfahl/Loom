---
description: Run E2E tests with XCUIApplication in TestTools/
---

You are now in **E2E TEST MODE** for Jump workspace manager. Let's validate the real UI! 🤖

## Critical E2E Rules

### ✅ REQUIRED

- E2E tests MUST use XCUIApplication
- Tests MUST launch actual app
- Tests MUST control UI with mouse/keyboard simulation
- You'll see "Automation running..." dialog (proves real automation!)

### ❌ FORBIDDEN

- NO fake "E2E" tests that only test data structures
- NO direct component testing in E2E files
- NO mocking of UI in E2E tests
- E2E files must NOT import Jump main app types directly

## What Are E2E Tests?

**End-to-End tests** simulate real user interactions:

- Launch the actual macOS app
- Click buttons with XCUIApplication
- Type text into fields
- Press keyboard shortcuts
- Verify UI state changes

## Test Infrastructure

### Location

```
TestTools/
├── JumpRunnerApp/          # Minimal host app for testing
│   ├── JumpRunnerApp.swift # App entry point
│   └── Info.plist          # macOS app config
├── UITests/                # XCUIApplication tests
│   ├── PopoverE2ETests.swift
│   ├── WorkspaceNavigationE2ETests.swift
│   └── ShortcutRecordingE2ETests.swift
├── project.yml             # XcodeGen configuration
├── launch-ui-tests.sh      # Run script
└── TestResults/            # xcresult files
```

### Why This Structure?

SPM doesn't support XCUIApplication tests, so we:

1. Keep Jump as SPM (clean, simple)
2. Use TestTools/ for UI testing only
3. XcodeGen generates Xcode project on demand
4. Tests run against real app binary

## Running E2E Tests

### Full Suite

```bash
cd TestTools && ./launch-ui-tests.sh
```

### What Happens:

1. XcodeGen generates Xcode project from project.yml
2. Builds JumpRunnerApp (minimal host)
3. Launches XCUIApplication tests
4. You'll see "Automation running..." dialog
5. Tests control app with mouse/keyboard
6. Results saved to TestResults/UI.xcresult

### Specific Test Class

```bash
cd TestTools && xcodebuild test \
  -project JumpRunner.xcodeproj \
  -scheme JumpRunnerApp \
  -testPlan UITests \
  -only-testing:UITests/PopoverE2ETests
```

### Specific Test Method

```bash
cd TestTools && xcodebuild test \
  -project JumpRunner.xcodeproj \
  -scheme JumpRunnerApp \
  -testPlan UITests \
  -only-testing:UITests/PopoverE2ETests/testWorkspaceSelection
```

## What I'll Do

When you run `/run-e2e`, I will:

1. **Navigate to TestTools/**

   ```bash
   cd TestTools
   ```

2. **Run Launch Script**

   ```bash
   ./launch-ui-tests.sh
   ```

3. **Capture Output**
   - Test results (pass/fail)
   - Performance metrics
   - Screenshots (if failures)
   - xcresult file path

4. **Analyze Results**
   - Total tests: passed/failed counts
   - Failed tests: detailed analysis with screenshots
   - Slow tests: > 5s per test
   - Flaky tests: intermittent failures

5. **Generate Report**

   ```
   ══════════════════════════════════════════════════
   E2E TEST RESULTS (XCUIApplication)
   ══════════════════════════════════════════════════

   ✅ PopoverE2ETests: 25/25 passed
   ✅ WorkspaceNavigationE2ETests: 18/18 passed
   ✅ ShortcutRecordingE2ETests: 12/12 passed

   Total: 55 tests, 55 passed, 0 failed ✅
   Duration: 45 seconds
   Automation: CONFIRMED (real UI automation detected)

   Results: TestTools/TestResults/UI.xcresult
   ══════════════════════════════════════════════════
   ```

## E2E Test Anatomy

### Good E2E Test Example

```swift
import XCTest

class PopoverE2ETests: XCTestCase {
    var app: XCUIApplication!

    override func setUp() {
        super.setUp()
        continueAfterFailure = false

        // Launch the actual app
        app = XCUIApplication()
        app.launch()
    }

    override func tearDown() {
        app.terminate()
        super.tearDown()
    }

    func testSelectWorkspaceWithMouse() {
        // Given: App is launched with test data
        XCTAssertTrue(app.wait(for: .runningForeground, timeout: 5))

        // When: User clicks first workspace
        let workspaceList = app.tables["workspace-list"]
        XCTAssertTrue(workspaceList.waitForExistence(timeout: 2))

        let firstWorkspace = workspaceList.cells.element(boundBy: 0)
        XCTAssertTrue(firstWorkspace.exists)
        firstWorkspace.click()

        // Then: Workspace is selected
        XCTAssertTrue(firstWorkspace.isSelected)
    }

    func testSelectWorkspaceWithKeyboard() {
        // Given: App is launched
        XCTAssertTrue(app.wait(for: .runningForeground, timeout: 5))

        // When: User presses down arrow key
        app.typeKey(.downArrow, modifierFlags: [])

        // Then: Next workspace is selected
        let workspaceList = app.tables["workspace-list"]
        let secondWorkspace = workspaceList.cells.element(boundBy: 1)
        XCTAssertTrue(secondWorkspace.isSelected)
    }
}
```

### Bad "E2E" Test Example (FORBIDDEN!)

```swift
import XCTest
@testable import Jump // ❌ FORBIDDEN! Importing main app

class FakeE2ETests: XCTestCase {
    func testWorkspaceStore() { // ❌ NOT AN E2E TEST!
        // This is a UNIT test pretending to be E2E
        let store = WorkspaceStore() // ❌ Direct component testing
        let workspace = Workspace(name: "Test")
        store.add(workspace) // ❌ No UI automation!

        XCTAssertEqual(store.workspaces.count, 1) // ❌ Testing data, not UI
    }
}
```

## E2E Test Validation

I will check for E2E test integrity:

### ✅ Real E2E Test Indicators

- Uses XCUIApplication
- app.launch() called
- Uses app.buttons, app.tables, app.textFields
- Uses .click(), .typeKey(), .typeText()
- "Automation running..." dialog appears

### ❌ Fake E2E Test Indicators

- Imports @testable import Jump
- Creates components directly (WorkspaceStore(), etc.)
- No XCUIApplication usage
- No UI element queries
- No automation dialog

## Debugging E2E Failures

When tests fail, I'll help debug:

1. **Check Screenshots**

   ```bash
   open TestTools/TestResults/UI.xcresult
   ```

2. **Run Single Test**

   ```bash
   /run-e2e --test PopoverE2ETests/testWorkspaceSelection
   ```

3. **Enable Verbose Logging**

   ```bash
   /run-e2e --verbose
   ```

4. **Record Test Run**
   ```bash
   /run-e2e --record
   ```

## Performance Targets

- **Single E2E Test**: < 5 seconds
- **Full E2E Suite**: < 2 minutes
- **App Launch Time**: < 1 second
- **UI Response**: < 100ms

## Example Sessions

### Example 1: All Tests Pass

```bash
User: /run-e2e
Assistant:
══════════════════════════════════════════════════
RUNNING E2E TESTS (XCUIApplication)
══════════════════════════════════════════════════

Navigating to TestTools/...
Running: ./launch-ui-tests.sh

[1/4] Generating Xcode project with XcodeGen...
✅ JumpRunner.xcodeproj created

[2/4] Building JumpRunnerApp...
✅ Build succeeded

[3/4] Launching UI tests...
⚡ "Automation running..." dialog detected (real UI automation!)

Running PopoverE2ETests...
✅ testWorkspaceSelectionWithMouse (0.8s)
✅ testWorkspaceSelectionWithKeyboard (0.6s)
✅ testSearchFiltering (1.2s)
✅ testQuickActionExecution (0.9s)
... 21 more tests

Running WorkspaceNavigationE2ETests...
✅ testNavigateWithArrowKeys (0.7s)
✅ testNavigateWithMouse (0.5s)
... 16 more tests

Running ShortcutRecordingE2ETests...
✅ testRecordShortcut (1.4s)
✅ testClearShortcut (0.6s)
... 10 more tests

[4/4] Analyzing results...

══════════════════════════════════════════════════
E2E TEST RESULTS
══════════════════════════════════════════════════

✅ PopoverE2ETests: 25/25 passed (avg: 0.9s/test)
✅ WorkspaceNavigationE2ETests: 18/18 passed (avg: 0.7s/test)
✅ ShortcutRecordingE2ETests: 12/12 passed (avg: 0.8s/test)

Total: 55 tests, 55 passed, 0 failed ✅
Duration: 48 seconds
Results: TestTools/TestResults/UI-2025-01-15-14-23-45.xcresult

🎉 ALL E2E TESTS PASSING!

E2E Integrity: CONFIRMED ✅
- Real XCUIApplication automation detected
- No fake E2E tests found
- All tests use proper UI automation

Ready to ship! 🚀
```

### Example 2: Test Failure

```bash
User: /run-e2e
Assistant:
══════════════════════════════════════════════════
RUNNING E2E TESTS
══════════════════════════════════════════════════

Running tests...

❌ PopoverE2ETests: 24/25 passed, 1 FAILED

FAILED: testWorkspaceSelectionWithMouse
  Duration: 2.3s
  Error: Element not found: table["workspace-list"]

  Screenshot: TestResults/UI.xcresult/testWorkspaceSelectionWithMouse-failure.png

  Likely cause: Workspace list not rendering

  Debug steps:
  1. Check if app launched: ✅ Yes
  2. Check if table exists: ❌ No (timeout after 2s)
  3. Check accessibility ID: "workspace-list" not found

  Possible fixes:
  - Add accessibilityIdentifier to List in PopoverView.swift
  - Increase wait timeout if table loads slowly
  - Check if test data is loaded correctly

══════════════════════════════════════════════════

Total: 55 tests, 54 passed, 1 failed ❌

BLOCKED: Fix failing test before merge

Would you like me to:
1. Open screenshot? (yes/no)
2. Show relevant code? (yes/no)
3. Suggest fix? (yes/no)
```

## Commands

```bash
/run-e2e                    # Run full E2E suite
/run-e2e --verbose          # Verbose output
/run-e2e --test ClassName   # Run specific test class
/run-e2e --record           # Record test execution video
/run-e2e --debug            # Pause on failure for debugging
```

---

**E2E tests are the ultimate truth. Real UI, real interactions, real confidence!** 🤖
