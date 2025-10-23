---
name: jest-unit-tests
version: 1.0.0
category: Web Development / Testing
tags: Jest, unit testing, JavaScript, TypeScript, testing framework, mocking, assertions
description: Writing effective unit tests with Jest for JavaScript and TypeScript applications.
---

# Jest Unit Tests Skill

## 1. Skill Purpose

This skill enables Claude to write effective, maintainable, and robust unit tests for JavaScript and TypeScript applications using Jest. It focuses on leveraging Jest's features for fast, isolated, and comprehensive testing, ensuring code quality, enabling safe refactoring, and improving developer confidence.

## 2. When to Activate This Skill

Activate this skill when:
- Writing new features or functionalities in JavaScript/TypeScript.
- Fixing bugs in JavaScript/TypeScript applications.
- Refactoring existing JavaScript/TypeScript code.
- Performing code reviews on test files to ensure adherence to Jest best practices.
- Setting up a testing environment for a new JavaScript/TypeScript project.
- Discussing testing strategies and best practices for front-end or Node.js applications.

## 3. Core Knowledge

The fundamental concepts, features, and best practices Claude needs to know regarding Jest unit testing:

### Jest Fundamentals:

-   **Test Suites (`describe`)**: Grouping related tests together.
-   **Test Cases (`it`, `test`)**: Defining individual test scenarios.
-   **Assertions (`expect`)**: Verifying expected outcomes using various matchers.
-   **Matchers**: Functions like `toBe`, `toEqual`, `toBeTruthy`, `toBeFalsy`, `toContain`, `toThrow`, `toMatchSnapshot`, etc.
-   **Setup and Teardown**: Lifecycle hooks (`beforeAll`, `afterAll`, `beforeEach`, `afterEach`) for managing test state.

### Key Testing Concepts:

-   **AAA Pattern (Arrange, Act, Assert)**: Structuring tests for clarity.
    -   **Arrange**: Set up test data and environment.
    -   **Act**: Execute the code under test.
    -   **Assert**: Verify the results.
-   **Test Isolation**: Each test should run independently without affecting others.
-   **Focus on Behavior**: Test *what* the code does, not *how* it does it.
-   **Descriptive Naming**: Clear test names that explain purpose and expected outcome.
-   **Fast Tests**: Unit tests should execute quickly.

### Advanced Jest Features:

-   **Mocking**: Replacing real dependencies with controlled substitutes.
    -   `jest.mock()`: Mocking modules.
    -   `jest.fn()`: Creating mock functions.
    -   `jest.spyOn()`: Spying on existing functions/methods.
    -   `mockImplementation`, `mockReturnValue`, `mockResolvedValue`, `mockRejectedValue`.
-   **Asynchronous Testing**: Handling Promises and async/await.
    -   `async/await` with `resolves`/`rejects` matchers.
    -   `done()` callback for older async patterns.
-   **Snapshot Testing (`toMatchSnapshot`)**: Capturing UI or data structures and comparing them against a saved snapshot.
-   **Test Coverage**: Generating reports to measure how much of the code is covered by tests.
-   **Parameterized Tests**: Using `test.each` or `describe.each` for running the same test with different data.

### Integration & Workflow:

-   **`jest.config.js`**: Configuration file for Jest.
-   **`package.json` scripts**: Defining `test` scripts for easy execution.
-   **CI/CD Integration**: Running tests automatically in continuous integration pipelines.
-   **Watch Mode**: Running tests automatically on file changes (`jest --watchAll`).

## 4. Key Guidance for Claude

### Always Recommend (✅ best practices)

-   ✅ Structure tests using the Arrange-Act-Assert (AAA) pattern.
-   ✅ Write small, focused tests that verify a single behavior or unit of code.
-   ✅ Use descriptive `describe` and `it`/`test` blocks to clearly articulate the test's purpose.
-   ✅ Employ Jest's powerful matchers (`expect().toBe()`, `expect().toEqual()`, etc.) for precise assertions.
-   ✅ Use `beforeEach` and `afterEach` for setting up and tearing down test-specific state to ensure test isolation.
-   ✅ Mock external dependencies (APIs, databases, complex modules) using `jest.mock()` or `jest.fn()` to isolate the unit under test.
-   ✅ Use `jest.spyOn()` to verify interactions with existing functions or methods without altering their behavior.
-   ✅ Always use `async/await` with `expect().resolves` or `expect().rejects` for testing asynchronous code.
-   ✅ Integrate Jest into the CI/CD pipeline to ensure tests run on every commit.
-   ✅ Aim for high code coverage, but prioritize testing critical paths and complex logic over 100% line coverage.

### Never Recommend (❌ anti-patterns)

-   ❌ Never write tests that are tightly coupled to implementation details; focus on public behavior.
-   ❌ Avoid shared state between tests; ensure each test runs in a clean, isolated environment.
-   ❌ Do not use `any` type in TypeScript test files unless absolutely necessary and justified.
-   ❌ Avoid overly complex or long test files; break them down into smaller, more manageable suites.
-   ❌ Do not ignore failing tests; a failing test indicates a bug or a broken expectation.
-   ❌ Avoid excessive or unnecessary mocking that makes tests hard to understand or maintain.
-   ❌ Do not rely on `setTimeout` or manual delays for asynchronous testing; use `async/await` or `done()`.
-   ❌ Avoid snapshot testing for every component or data structure; use it judiciously for large, stable outputs.

### Common Questions & Responses (FAQ format)

**Q: How do I test a function that makes an API call?**
A: Use `jest.mock('axios')` (or your HTTP client) to mock the entire module. Then, use `mockResolvedValue` or `mockRejectedValue` on the mocked HTTP method (e.g., `axios.get.mockResolvedValue({ data: ... })`) to control the API response. This isolates your component from the actual network request.

**Q: My tests are slow. How can I speed them up?**
A: Ensure tests are isolated and don't share state. Avoid heavy I/O operations (database calls, file system access) by mocking them. Use `jest --runInBand` to debug serial execution, but generally Jest runs tests in parallel. Consider breaking down large test files. Ensure your Jest configuration is optimized (e.g., `testMatch` is specific).

**Q: When should I use `toBe` vs `toEqual`?**
A: Use `toBe` for primitive values (numbers, strings, booleans) and to check if two objects are the *exact same instance* in memory. Use `toEqual` for deep equality checks of objects or arrays, where you want to compare the values of their properties rather than their memory addresses.

**Q: How do I test a component that uses `localStorage` or `sessionStorage`?**
A: Jest provides a mock for `localStorage` and `sessionStorage` by default in a browser environment. You can directly interact with `localStorage.setItem()`, `localStorage.getItem()`, etc., in your tests, and Jest will manage a mock in-memory version. Remember to clear it with `beforeEach(() => localStorage.clear())`.

## 5. Anti-Patterns to Flag

### Example 1: Testing Implementation Details

**BAD:**
```typescript
// utils.ts
export function _privateHelper(value: number): number {
  return value * 2;
}

export function publicFunction(input: number): number {
  return _privateHelper(input) + 1;
}

// utils.test.ts
describe('publicFunction', () => {
  it('should call _privateHelper internally', () => {
    const spy = jest.spyOn(require('./utils'), '_privateHelper');
    publicFunction(5);
    expect(spy).toHaveBeenCalledWith(5);
  });
});
```
*Problem*: The test is coupled to the private `_privateHelper` function. If `_privateHelper` is refactored or removed, the test breaks even if `publicFunction`'s behavior remains correct.

**GOOD:**
```typescript
// utils.ts (same as above)

// utils.test.ts
describe('publicFunction', () => {
  it('should return the correct result', () => {
    expect(publicFunction(5)).toBe(11); // (5 * 2) + 1
  });

  it('should handle zero input', () => {
    expect(publicFunction(0)).toBe(1);
  });
});
```
*Solution*: Test the public behavior of `publicFunction` directly. This makes tests more resilient to internal changes.

### Example 2: Shared State Between Tests

**BAD:**
```typescript
let counter = 0;

describe('Counter', () => {
  it('should increment counter', () => {
    counter++;
    expect(counter).toBe(1);
  });

  it('should reset counter', () => {
    counter = 0;
    expect(counter).toBe(0);
  });
});
```
*Problem*: The order of tests matters. If `should reset counter` runs first, `should increment counter` will fail. Tests are not isolated.

**GOOD:**
```typescript
describe('Counter', () => {
  let counter: number;

  beforeEach(() => {
    counter = 0; // Reset counter before each test
  });

  it('should increment counter', () => {
    counter++;
    expect(counter).toBe(1);
  });

  it('should reset counter (implicitly by beforeEach)', () => {
    expect(counter).toBe(0); // Counter is 0 due to beforeEach
  });
});
```
*Solution*: Use `beforeEach` to set up a fresh state for each test, ensuring isolation.

## 6. Code Review Checklist

-   [ ] Are tests structured using the Arrange-Act-Assert (AAA) pattern?
-   [ ] Is each test focused on a single behavior or unit?
-   [ ] Are `describe` and `it`/`test` names clear and descriptive?
-   [ ] Are appropriate Jest matchers used for assertions (`toBe`, `toEqual`, `toThrow`, `resolves`, etc.)?
-   [ ] Is `beforeEach`/`afterEach` used effectively to manage test state and ensure isolation?
-   [ ] Are external dependencies mocked using `jest.mock()` or `jest.fn()`?
-   [ ] Is `jest.spyOn()` used correctly to observe function calls?
-   [ ] Is asynchronous code tested using `async/await` with `resolves`/`rejects`?
-   [ ] Do tests focus on public behavior rather than private implementation details?
-   [ ] Are there any `any` types that could be replaced with more specific types or type assertions?
-   [ ] Is the test file located appropriately (e.g., alongside the source file or in `__tests__`)?

## 7. Related Skills

-   `tdd-red-green-refactor`: Jest is a primary tool for implementing the TDD cycle.
-   `typescript-strict-mode`: Jest tests should also adhere to strict TypeScript type checking.
-   `clean-code-principles`: Writing clean, readable tests is as important as writing clean production code.

## 8. Examples Directory Structure

```
jest-unit-tests/
├── examples/
│   ├── basic_assertions.test.ts    # Demonstrates common Jest matchers
│   ├── mocking_dependencies.test.ts # Examples of jest.mock, jest.fn, jest.spyOn
│   ├── async_testing.test.ts       # Testing asynchronous code with Jest
│   └── setup_teardown.test.ts      # Usage of beforeEach, afterEach, etc.
├── patterns/
│   ├── custom_matchers.ts          # Creating custom Jest matchers
│   └── parameterized_tests.ts      # Using test.each for data-driven tests
├── scripts/
│   ├── jest-init.sh                # Shell script to initialize Jest in a project
│   ├── jest-test-watcher.sh        # Shell script to run Jest in watch mode
│   ├── jest-coverage-reporter.sh   # Shell script to generate Jest coverage reports
│   └── jest-mock-generator.js      # Node.js script to generate boilerplate mock files
└── README.md
```

## 9. Custom Scripts Section

Here are 4 automation scripts designed to save significant time when working with Jest unit tests:

1.  **`jest-init.sh`**: Initializes a new JavaScript/TypeScript project with Jest configured, including `package.json` scripts and a basic `jest.config.js`.
2.  **`jest-test-watcher.sh`**: A shell script to run Jest in watch mode with common options, allowing for rapid feedback during development.
3.  **`jest-coverage-reporter.sh`**: A shell script to run Jest and generate a detailed test coverage report, with options for setting coverage thresholds.
4.  **`jest-mock-generator.js`**: A Node.js script to generate boilerplate mock files for modules or classes, streamlining the process of creating test doubles.
