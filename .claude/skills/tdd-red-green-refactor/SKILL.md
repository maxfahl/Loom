---
name: tdd-red-green-refactor
version: 1.0.0
category: Software Development / Testing
tags: TDD, Test-Driven Development, Red Green Refactor, unit testing, refactoring, clean code
description: The core cycle of Test-Driven Development (TDD) for building robust and maintainable software.
---

# TDD: Red-Green-Refactor Skill

## 1. Skill Purpose

This skill enables Claude to effectively apply the Red-Green-Refactor cycle of Test-Driven Development (TDD) to build high-quality, robust, and maintainable software. It focuses on guiding the development process through small, iterative steps, ensuring code correctness, improving design, and reducing technical debt.

## 2. When to Activate This Skill

Activate this skill when:
- Developing new features or functionalities.
- Fixing bugs (write a test that reproduces the bug first).
- Refactoring existing code to improve its structure or readability.
- Designing new modules or components.
- Collaborating on a codebase where high quality and maintainability are critical.
- Discussing best practices for software development and testing.

## 3. Core Knowledge

The fundamental concepts, phases, and tools Claude needs to know regarding the TDD Red-Green-Refactor cycle:

### The Three Phases:

-   **Red Phase (Write a failing test)**:
    -   **Goal**: Define a new, small piece of desired functionality by writing a single, failing automated test.
    -   **Characteristics**: The test should fail for the expected reason (e.g., method not found, assertion failure). It should be concise, focused on a single behavior, and clearly express the requirement.
    -   **Key Actions**: Understand the requirement, write a test that fails, verify it fails.

-   **Green Phase (Make the test pass)**:
    -   **Goal**: Write the *minimal* amount of production code necessary to make the failing test pass.
    -   **Characteristics**: Focus on getting the test to pass quickly. Do not worry about perfect design, elegance, or efficiency at this stage. It's about functionality.
    -   **Key Actions**: Implement just enough code, run tests, verify all tests pass.

-   **Refactor Phase (Improve the code)**:
    -   **Goal**: Improve the structure, readability, and maintainability of the code without changing its external behavior.
    -   **Characteristics**: This is where design emerges. Remove duplication, improve naming, simplify complex logic, optimize (if necessary and safe). The comprehensive test suite acts as a safety net.
    -   **Key Actions**: Identify code smells, apply refactoring techniques, run all tests, verify all tests still pass.

### Supporting Concepts:

-   **Unit Testing**: Testing individual, isolated units of code (functions, methods, classes).
-   **Test Doubles (Mocks, Stubs, Fakes, Spies)**: Objects that stand in for real dependencies to isolate the unit under test and control its behavior.
-   **Assertion Libraries**: Frameworks or tools used to verify expected outcomes in tests (e.g., `assert` in Python, `expect` in Jest).
-   **Test Runner**: Software that executes tests and reports results (e.g., Jest, Pytest, JUnit).
-   **Arrange-Act-Assert (AAA) Pattern**: A common structure for unit tests: setup (Arrange), execute (Act), verify (Assert).
-   **Small, Incremental Steps**: The essence of TDD; each cycle should be very short.
-   **Fast Feedback Loop**: Tests should run quickly to provide immediate feedback.
-   **Executable Documentation**: Well-written tests serve as clear examples of how the code is intended to be used.

### Modern Tooling & Trends:

-   **AI-Powered Test Generation**: Tools that can suggest or generate initial test cases.
-   **Integrated Development Environments (IDEs)**: Features for running tests, debugging, and refactoring.
-   **Continuous Integration (CI)**: Automated testing as part of the build process to catch regressions early.
-   **Static Analysis Tools**: Linters and code quality checkers that complement TDD by enforcing coding standards.

## 4. Key Guidance for Claude

### Always Recommend (✅ best practices)

-   ✅ Start every new feature or bug fix by writing a failing test (Red phase).
-   ✅ Write the smallest possible test that captures a single, specific behavior.
-   ✅ Ensure the test fails for the right reason before writing any production code.
-   ✅ In the Green phase, write *only* the code needed to make the current failing test pass. Resist the urge to implement more.
-   ✅ Once all tests are green, immediately enter the Refactor phase to improve code quality, remove duplication, and enhance design.
-   ✅ Run all tests frequently, especially after every code change and refactoring step, to ensure no regressions are introduced.
-   ✅ Structure tests using the Arrange-Act-Assert (AAA) pattern for clarity and consistency.
-   ✅ Use descriptive test names that clearly explain what the test is verifying.
-   ✅ Employ test doubles (mocks, stubs) to isolate the unit under test from its dependencies.
-   ✅ Focus on testing behavior, not internal implementation details.

### Never Recommend (❌ anti-patterns)

-   ❌ Never write production code before writing a failing test for that functionality.
-   ❌ Do not write more than one failing test at a time (unless they are very closely related and you can make them pass with a single code change).
-   ❌ Avoid writing complex or large tests that cover multiple behaviors; keep tests small and focused.
-   ❌ Do not skip the Refactor phase. It's crucial for maintaining code health and preventing technical debt.
-   ❌ Never change a test to make it pass if the underlying code is incorrect; fix the production code instead.
-   ❌ Do not test private implementation details that are not part of the public API.
-   ❌ Avoid relying on the order of test execution; tests should be independent.
-   ❌ Do not ignore failing tests; a failing test indicates a bug or a broken expectation that needs immediate attention.

### Common Questions & Responses (FAQ format)

**Q: My test is not failing, even though I haven't written any production code. What's wrong?**
A: This indicates an issue with your test. The test should explicitly assert a condition that cannot be met by the current (non-existent or incorrect) production code. Double-check your assertion and ensure it's expecting a specific failure or an incorrect result. For example, if testing a function that should return `5`, and the function currently returns `0`, your test should assert `assertEqual(my_func(), 5)`, which will fail.

**Q: How do I know when to stop writing tests and start refactoring?**
A: You stop writing *new* failing tests when you have a single failing test (Red phase). You stop writing *production code* when that single test turns green (Green phase). You then immediately move to refactoring. The Refactor phase continues until the code is clean, readable, and all tests still pass. The cycle then repeats for the next small piece of functionality.

**Q: What kind of things should I refactor?**
A: Look for code smells: duplication, long methods, large classes, unclear names, complex conditional logic, poor encapsulation. Refactoring aims to improve design, readability, and maintainability. Examples include extracting methods, renaming variables, introducing design patterns, simplifying conditionals, and improving error handling.

**Q: How do I handle external dependencies (databases, APIs) in my tests?**
A: Use test doubles (mocks, stubs, fakes). For unit tests, you want to isolate the unit under test. Instead of calling a real database, mock the database interaction to return predefined data. This makes tests faster, more reliable, and independent of external systems. For integration tests, you might use real dependencies or lightweight versions (e.g., in-memory databases).

## 5. Anti-Patterns to Flag

### Example 1: Writing Production Code First

**BAD:**
```python
# production_code.py
def add(a, b):
    return a + b

# test_code.py
def test_add():
    assert add(1, 2) == 3
```
*Problem*: The production code was written without a failing test to guide its development. This often leads to untested edge cases or incorrect assumptions.

**GOOD (TDD Cycle):**

1.  **Red:**
    ```python
    # test_code.py
    import pytest
    from production_code import add

    def test_add_two_numbers():
        assert add(1, 2) == 3 # This test will initially fail because 'add' doesn't exist or is incorrect
    ```
    *Run test, confirm failure.*

2.  **Green:**
    ```python
    # production_code.py
    def add(a, b):
        return a + b

    # test_code.py (same as above)
    ```
    *Run test, confirm pass.*

3.  **Refactor:** (In this simple case, not much to refactor, but imagine more complex logic)
    ```python
    # production_code.py
    def add(num1: int, num2: int) -> int: # Add type hints for clarity
        return num1 + num2
    ```
    *Run all tests, confirm pass.*

### Example 2: Testing Implementation Details

**BAD:**
```typescript
// calculator.ts
class Calculator {
  private _result: number = 0;

  private _addInternal(a: number, b: number): number {
    return a + b;
  }

  public add(a: number, b: number): number {
    this._result = this._addInternal(a, b);
    return this._result;
  }
}

// calculator.test.ts
describe('Calculator', () => {
  it('should call _addInternal when add is called', () => {
    const calculator = new Calculator();
    const spy = jest.spyOn(calculator as any, '_addInternal'); // Spying on private method
    calculator.add(1, 2);
    expect(spy).toHaveBeenCalledWith(1, 2);
  });
});
```
*Problem*: The test is coupled to the private implementation detail `_addInternal`. If `_addInternal` is renamed or removed, the test breaks even if the public `add` behavior remains the same.

**GOOD:**
```typescript
// calculator.ts (same as above)

// calculator.test.ts
describe('Calculator', () => {
  it('should correctly add two numbers', () => {
    const calculator = new Calculator();
    const result = calculator.add(1, 2);
    expect(result).toBe(3);
  });

  it('should return the sum of two negative numbers', () => {
    const calculator = new Calculator();
    const result = calculator.add(-1, -2);
    expect(result).toBe(-3);
  });
});
```
*Solution*: Test the public behavior (`add` returns the correct sum) rather than the internal mechanism. This makes tests more resilient to refactoring.

## 6. Code Review Checklist

-   [ ] Does each new feature or bug fix start with a failing test?
-   [ ] Is the test small, focused, and testing a single behavior?
-   [ ] Does the test fail for the right reason before production code is written?
-   [ ] Is only the minimal necessary production code written to make the test pass?
-   [ ] Has the code been refactored after the test passed, without breaking existing functionality?
-   [ ] Are all tests passing after refactoring?
-   [ ] Are tests structured using the Arrange-Act-Assert (AAA) pattern?
-   [ ] Are test names descriptive and clear about what they are testing?
-   [ ] Are test doubles used appropriately to isolate units from dependencies?
-   [ ] Do tests focus on public behavior rather than private implementation details?
-   [ ] Are tests fast and reliable?

## 7. Related Skills

-   `jest-unit-tests`: Practical application of TDD principles using Jest.
-   `python-type-hints`: Type hints improve code quality and can be refactored during the TDD cycle.
-   `clean-code-principles`: TDD naturally encourages many clean code practices.
-   `solid-principles`: TDD can help drive designs that adhere to SOLID principles.

## 8. Examples Directory Structure

```
tdd-red-green-refactor/
├── examples/
│   ├── simple_calculator_tdd.py    # Python TDD example (Red-Green-Refactor cycle)
│   └── string_utils_tdd.ts         # TypeScript TDD example
├── patterns/
│   ├── test_doubles.py             # Demonstrates mocks, stubs, fakes
│   └── assertion_patterns.ts       # Common assertion patterns
├── scripts/
│   ├── tdd-init.sh                 # Shell script to initialize project with test setup
│   ├── test-runner.sh              # Shell script to run tests efficiently
│   ├── refactor-helper.py          # Python script to identify refactoring opportunities
│   └── test-template-generator.py  # Python script to generate boilerplate test files
└── README.md
```

## 9. Custom Scripts Section

Here are 4 automation scripts designed to save significant time when practicing TDD:

1.  **`tdd-init.sh`**: Initializes a new project with a basic testing framework setup (e.g., Jest for JS/TS, pytest for Python), creating a ready-to-use TDD environment.
2.  **`test-runner.sh`**: A versatile shell script to run tests efficiently, supporting watch mode and specific test filters to speed up the Red-Green cycle.
3.  **`refactor-helper.py`**: A Python script that analyzes code for common refactoring opportunities (e.g., long functions, duplicate code) after the Green phase, guiding the Refactor step.
4.  **`test-template-generator.py`**: A Python script to generate boilerplate test files for a given source file, encouraging test-first development and reducing manual setup.
