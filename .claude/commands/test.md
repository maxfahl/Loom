---
description: Run tests with coverage and detailed reporting
model: haiku
argument-hint: [test pattern]
---

# /test - Run Tests

## What This Command Does

Execute tests and analyze results with optional pattern filtering.

## Process

1. **Determine Test Command**:
   - Check package.json for test scripts
   - Detect test framework (Jest, Vitest, Mocha, etc.)

2. **Run Tests**:
   ```bash
   # With pattern if provided
   npm test -- $ARGUMENTS --coverage --verbose

   # Without pattern
   npm test -- --coverage --verbose
   ```

3. **Analyze Results**:
   - Parse test output for pass/fail counts
   - Extract coverage percentages
   - Identify failing tests with details
   - Show coverage report summary

4. **Report Findings**:
   ```markdown
   # Test Results

   ## Summary
   - Tests Run: [X]
   - Passed: [X]
   - Failed: [X]
   - Skipped: [X]

   ## Coverage
   - Statements: [X]%
   - Branches: [X]%
   - Functions: [X]%
   - Lines: [X]%

   ## Failing Tests (if any)
   - [Test name]: [Error message]
     File: [file:line]

   ## Next Steps
   [Recommendations for fixing failures or improving coverage]
   ```

## Recommended Skills

<!-- TODO: Add relevant skills from .claude/skills/ -->

- `jest-unit-tests` - For Jest test execution
- `tdd-red-green-refactor` - For TDD methodology
- `playwright-e2e` - For E2E tests

Use these skills heavily throughout execution to ensure best practices.

**Skill Troubleshooting Authority**: If any referenced skill does not work or any script within the skill does not work, Claude Code has the authority to fix them.

## Arguments

- `$ARGUMENTS`: Optional test pattern to filter which tests to run

## Examples

```
/test
```

Runs all tests with coverage.

```
/test auth
```

Runs only tests matching "auth" pattern.

```
/test src/components/Button.test.ts
```

Runs specific test file.
