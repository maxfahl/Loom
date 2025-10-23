---
description: Run tests with coverage and detailed reporting
allowed-tools: Bash(npm:*)
model: claude-haiku-4-5
argument-hint: [test pattern]
---

You are now in **TEST MODE**. Time to validate everything works! 🧪

## Purpose

Execute tests and analyze results with detailed coverage reporting. This command:

1. Detects project type (Node.js, Swift, Python, etc.)
2. Runs appropriate test command with coverage
3. Displays test results
4. Shows coverage report
5. Highlights failed tests
6. Shows coverage percentage (must be ≥80%)

## Test Execution Strategy

### Step 1: Detect Project Type

Determine the project type by checking for:

- **Node.js**: `package.json` exists
- **Swift**: `Package.swift` exists or `.xcodeproj` exists
- **Python**: `setup.py`, `pyproject.toml`, or `requirements.txt` exists
- **Rust**: `Cargo.toml` exists
- **Other**: Check for language-specific markers

### Step 2: Run Tests with Coverage

Based on project type, run the appropriate test command:

**Node.js/TypeScript**:
```bash
npm test -- --coverage
# or
npm run test:coverage
# or
npx jest --coverage
```

**Swift (Package Manager)**:
```bash
swift test --enable-code-coverage
```

**Swift (Xcode)**:
```bash
xcodebuild test -scheme <scheme> -enableCodeCoverage YES
```

**Python**:
```bash
pytest --cov=. --cov-report=term --cov-report=html
```

**Rust**:
```bash
cargo test
# For coverage:
cargo tarpaulin --out Xml --out Html
```

### Step 3: Parse Test Results

Extract and display:

- Total tests run
- Tests passed
- Tests failed
- Test execution time
- Coverage percentage
- Failed test details (file, line, reason)

### Step 4: Analyze Coverage

**Coverage Requirements**:
- **Minimum**: 80% (MANDATORY)
- **Target**: 90%
- **Critical paths**: 100%

**Coverage Report**:
- Overall percentage
- Per-file breakdown (if coverage < 80%)
- Uncovered lines/functions
- Suggestions for improvement

### Step 5: Generate Report

Display comprehensive test report with:

```
══════════════════════════════════════════════════
TEST RESULTS
══════════════════════════════════════════════════

✅ Tests Passed: X
❌ Tests Failed: Y
⏱️  Duration: Xs
📊 Coverage: X%

══════════════════════════════════════════════════
FAILED TESTS (if any)
══════════════════════════════════════════════════

❌ Test Name
  Location: file.test.ts:45
  Reason: Expected X but got Y

  Fix: [Suggested fix]

══════════════════════════════════════════════════
COVERAGE REPORT
══════════════════════════════════════════════════

Overall: X% (target: 80%+)

Files Below Threshold:
- file1.ts: 65% (needs +15%)
- file2.ts: 72% (needs +8%)

Uncovered Lines:
- file1.ts: lines 45-52, 78-81
- file2.ts: lines 23-29

══════════════════════════════════════════════════
DECISION
══════════════════════════════════════════════════

✅ PASS - All tests passing, coverage ≥80%
❌ BLOCK - Fix failing tests or improve coverage

══════════════════════════════════════════════════
```

## Test Pattern Argument (Optional)

If a test pattern is provided, run only matching tests:

**Node.js**:
```bash
npm test -- --testNamePattern="<pattern>"
```

**Swift**:
```bash
swift test --filter <pattern>
```

**Python**:
```bash
pytest -k "<pattern>"
```

**Rust**:
```bash
cargo test <pattern>
```

## Test Quality Checks

### ✅ Good Tests

- Written BEFORE implementation (TDD)
- Isolated (no shared state between tests)
- Fast (unit tests < 100ms, integration tests < 5s)
- Clear Given-When-Then structure
- Descriptive test names
- Test one thing per test

### ❌ Bad Tests

- Written AFTER implementation (not TDD)
- Tests leak state (affect other tests)
- Slow tests (> 1s for unit, > 10s for integration)
- Unclear what's being tested
- Vague test names
- Testing multiple concerns in one test

## TDD Enforcement

The `/test` command validates TDD compliance:

- ✅ Tests exist for all new code
- ✅ Coverage meets 80% minimum
- ✅ All tests pass before merge
- ❌ Blocks merge if tests missing or failing
- ❌ Blocks merge if coverage < 80%

## Performance Targets

- **Unit Tests**: < 100ms per test
- **Integration Tests**: < 5s per test
- **Total Suite**: < 2 minutes
- **Coverage**: ≥ 80%

## Example Usage

### Run All Tests
```bash
/test
```

### Run Specific Test Pattern
```bash
/test authentication
```

### Run with Verbose Output
```bash
/test --verbose
```

## Implementation Steps

When you run `/test`, I will:

1. **Detect Project Type**
   - Check for package.json, Package.swift, Cargo.toml, etc.
   - Determine test framework (Jest, XCTest, pytest, etc.)

2. **Run Test Command**
   - Execute appropriate test command with coverage
   - Capture output (stdout and stderr)
   - Parse test results

3. **Analyze Results**
   - Count passed/failed tests
   - Extract failure details (file, line, reason)
   - Calculate coverage percentage
   - Identify uncovered code

4. **Generate Report**
   - Display formatted test results
   - Highlight failures with context
   - Show coverage report
   - Provide actionable suggestions

5. **Make Decision**
   - ✅ PASS: All tests pass, coverage ≥80%
   - ❌ BLOCK: Tests fail or coverage <80%

## Example Session (Node.js)

```bash
User: /test
Assistant: Running tests with coverage...

Detected: Node.js project (package.json found)
Running: npm test -- --coverage

══════════════════════════════════════════════════
TEST RESULTS
══════════════════════════════════════════════════

✅ Tests Passed: 45
❌ Tests Failed: 0
⏱️  Duration: 3.2s
📊 Coverage: 87%

Test Suites: 8 passed, 8 total
Tests:       45 passed, 45 total

══════════════════════════════════════════════════
COVERAGE REPORT
══════════════════════════════════════════════════

Overall: 87% (target: 80%+) ✅

File Coverage:
- auth.service.ts: 95%
- user.controller.ts: 89%
- data.repository.ts: 82%
- validation.utils.ts: 78% ⚠️

Files Below Threshold:
- validation.utils.ts: 78% (needs +2%)

Uncovered Lines:
- validation.utils.ts: lines 45-48 (error handling)

══════════════════════════════════════════════════
DECISION
══════════════════════════════════════════════════

✅ PASS - All tests passing, coverage ≥80%

💡 Suggestions:
- Add tests for validation.utils.ts error handling (lines 45-48)
- Current coverage: 87% (target: 90%)

══════════════════════════════════════════════════
```

## Example Session (Swift)

```bash
User: /test
Assistant: Running tests with coverage...

Detected: Swift project (Package.swift found)
Running: swift test --enable-code-coverage

══════════════════════════════════════════════════
TEST RESULTS
══════════════════════════════════════════════════

✅ Tests Passed: 63
❌ Tests Failed: 0
⏱️  Duration: 5.8s
📊 Coverage: 92%

Test Suites:
✅ WorkspacePersistenceTests: 12/12 passed
✅ WorkspaceStoreTests: 8/8 passed
✅ ContextDetectorTests: 15/15 passed
✅ TargetManagerTests: 10/10 passed

══════════════════════════════════════════════════
COVERAGE REPORT
══════════════════════════════════════════════════

Overall: 92% (target: 80%+) ✅

Module Coverage:
- Jump: 94%
- JumpUI: 88%
- JumpCore: 95%

══════════════════════════════════════════════════
DECISION
══════════════════════════════════════════════════

✅ PASS - All tests passing, coverage ≥80%

🎉 Excellent coverage! Ready to ship.

══════════════════════════════════════════════════
```

## Example with Failures

```bash
User: /test
Assistant: Running tests with coverage...

Detected: Node.js project (package.json found)
Running: npm test -- --coverage

══════════════════════════════════════════════════
TEST RESULTS
══════════════════════════════════════════════════

✅ Tests Passed: 44
❌ Tests Failed: 1
⏱️  Duration: 3.1s
📊 Coverage: 85%

══════════════════════════════════════════════════
FAILED TESTS
══════════════════════════════════════════════════

❌ auth.service.test.ts › AuthService › should validate expired tokens

  Location: tests/auth.service.test.ts:45
  Reason: Expected token to be invalid, but validation passed

  Expected: { valid: false, reason: 'expired' }
  Actual: { valid: true }

  Issue: Token expiration check not working

  Fix: Update auth.service.ts:78 to check token expiration:
  ```typescript
  if (decoded.exp < Date.now() / 1000) {
    return { valid: false, reason: 'expired' };
  }
  ```

══════════════════════════════════════════════════
COVERAGE REPORT
══════════════════════════════════════════════════

Overall: 85% (target: 80%+) ✅

══════════════════════════════════════════════════
DECISION
══════════════════════════════════════════════════

❌ BLOCK - Fix failing tests before proceeding

Next Steps:
1. Fix token expiration validation in auth.service.ts
2. Re-run tests with: /test auth
3. Verify fix resolves the issue

══════════════════════════════════════════════════

Would you like me to fix this issue? (yes/no)
```

## Integration with Other Commands

The `/test` command integrates with:

- **`/dev`** - Runs tests after implementation
- **`/commit`** - Runs tests before committing
- **`/review`** - Checks test coverage in code review
- **`/plan`** - Ensures test plan exists before implementation

## Notes

- **Always run tests before committing** - Use `/commit` to ensure this
- **TDD is mandatory** - Write tests FIRST, then implementation
- **Coverage is not quality** - 100% coverage doesn't mean good tests
- **Fast tests are valuable** - Keep unit tests under 100ms
- **Flaky tests are failures** - Fix or remove non-deterministic tests

---

**Tests are your safety net. Never skip them!** 🧪
