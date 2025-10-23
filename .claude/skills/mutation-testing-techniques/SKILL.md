---
name: mutation-testing-techniques
version: 1.0.0
category: Software Quality / Testing
tags: mutation testing, testing, quality, stryker, typescript, javascript, jest, mocha
description: Applying mutation testing to assess test suite effectiveness and identify weak tests.
---

## Skill Purpose

Mutation testing is a powerful technique used to evaluate the quality of a test suite. Unlike traditional code coverage, which only tells you *what* code is executed, mutation testing tells you *how well* your tests can detect changes in the code's behavior. It works by introducing small, syntactic changes (mutations) into your source code, creating "mutants." If your test suite fails when a mutant is introduced, the mutant is "killed," indicating an effective test. If the test suite passes, the mutant "survives," revealing a weakness in your tests that could allow a bug to slip through. This skill enables Claude to understand, apply, and guide developers in leveraging mutation testing to build more robust and reliable software.

## When to Activate This Skill

Activate this skill when:
- **High Code Coverage, Low Confidence**: Your project has high code coverage metrics, but you still encounter bugs in production, suggesting your tests aren't catching behavioral issues.
- **Critical Code Refactoring**: Before or after refactoring critical business logic, to ensure that changes don't introduce regressions and that existing tests are sufficient.
- **Quality Gate Enforcement**: As part of a Continuous Integration/Continuous Delivery (CI/CD) pipeline to enforce a minimum standard of test suite effectiveness.
- **Onboarding New Team Members**: To help new developers understand the importance of writing effective tests, not just covering lines of code.
- **Identifying Test Gaps**: When you suspect certain parts of your application lack sufficient behavioral tests.

## Core Knowledge

### Concepts
- **Mutant**: A slightly modified version of the original source code, created by applying a mutation operator.
- **Mutation Operator**: A rule that defines how to introduce a small, syntactic change to the code (e.g., changing `+` to `-`, `>` to `>=`).
- **Mutation Score**: The percentage of killed mutants. A higher score indicates a more effective test suite.
- **Killed Mutant**: A mutant that causes at least one test to fail. This is the desired outcome.
- **Survived Mutant**: A mutant that does not cause any test to fail. This indicates a weakness in the test suite.
- **Equivalent Mutant**: A mutant that produces the exact same behavior as the original code, making it impossible for any test to kill it. These are rare and often ignored.

### Tools
- **Stryker Mutator**: The leading mutation testing framework for JavaScript and TypeScript projects. It integrates with popular test runners like Jest, Mocha, and Karma.

### Integration
- Stryker Mutator can be integrated into your project as a development dependency.
- Configuration files (`stryker.conf.json` or `stryker.conf.js`) define how mutation tests are run, which files to mutate, which test runner to use, and reporting options.

### Configuration
Key configuration options for Stryker Mutator:
- `mutate`: Glob patterns for files to mutate.
- `testRunner`: The test runner to use (e.g., `jest`, `mocha`).
- `mutator`: Which mutation operators to apply (e.g., `typescript`, `javascript`).
- `reporters`: How to report results (e.g., `html`, `json`, `clear-text`).
- `thresholds`: Define minimum acceptable mutation scores (e.g., `break`, `high`, `low`).
- `ignorePatterns`: Files or patterns to exclude from mutation.
- `excludedMutations`: Specific mutation types to exclude.

## Key Guidance for Claude

### ✅ Always Recommend
- **Start Small**: Begin by applying mutation testing to a small, critical module or a newly developed feature. This helps manage the initial overhead and provides quick wins.
- **Set Realistic Thresholds**: Configure a `thresholds.break` value in Stryker to fail the build if the mutation score drops below an acceptable level. Start with a conservative value and increase it over time.
- **Integrate into CI/CD**: Make mutation testing a mandatory step in your CI/CD pipeline for critical code paths. This ensures continuous quality enforcement.
- **Investigate Survived Mutants**: Treat every survived mutant as a potential bug or a gap in your test suite. Analyze why the mutant survived and enhance your tests accordingly.
- **Focus on Behavioral Tests**: Encourage writing tests that assert specific behaviors and outcomes, rather than just checking if a function was called.

### ❌ Never Recommend
- **Blindly Run on Entire Codebase**: Do not run mutation tests on an entire large codebase without prior configuration and scoping. This can be extremely slow and resource-intensive.
- **Ignore Survived Mutants**: Never ignore survived mutants without understanding why they survived. This defeats the purpose of mutation testing.
- **Replace Other Testing**: Mutation testing complements, but does not replace, other forms of testing (unit, integration, E2E). It's a tool for assessing test quality, not a primary testing method.
- **Over-optimize for 100% Score**: While a high mutation score is good, striving for 100% can lead to writing overly specific or brittle tests for equivalent mutants. Focus on meaningful mutations.

### Common Questions & Responses

- **Q: How can I speed up mutation tests in a large project?**
  - **A:**
    1.  **Scope**: Focus mutation testing on critical or frequently changing modules using `mutate` patterns.
    2.  **Incremental Testing**: Use Stryker's `diff` mode to only mutate changed files.
    3.  **Parallelization**: Configure Stryker to run tests in parallel using `concurrency`.
    4.  **Optimize Test Setup**: Ensure your unit tests are fast and isolated.
    5.  **Disable Bail**: For initial runs, consider setting `disableBail` to `true` in Stryker to allow all mutants to be tested even if some tests fail early.

- **Q: What is a good mutation score to aim for?**
  - **A:** There's no universal "good" score, as it depends on the project's criticality and maturity. However, for critical business logic, aim for **80% or higher**. For less critical code, **60-70%** might be acceptable. The goal is continuous improvement.

- **Q: My tests are passing, but mutation tests show many survived mutants. What does this mean?**
  - **A:** This is a classic scenario where mutation testing shines! It means your tests are executing the code (high coverage) but are not asserting against the specific behaviors that the mutants are changing. You need to enhance your assertions to cover these mutated behaviors.

- **Q: How do I handle equivalent mutants?**
  - **A:** Equivalent mutants are rare. If you encounter one, and you're certain it's equivalent (i.e., no test can ever distinguish its behavior from the original code), you can add it to `excludedMutations` in your Stryker configuration. However, always double-check to ensure it's truly equivalent.

## Anti-Patterns to Flag

### ❌ BAD: High Code Coverage, Low Mutation Score

```typescript
// src/calculator.ts
export function add(a: number, b: number): number {
  return a + b;
}

// test/calculator.test.ts
import { add } from '../src/calculator';

describe('add', () => {
  it('should call the add function', () => {
    add(1, 2); // Test passes, but doesn't assert the result
  });
});
// Mutation: `return a + b;` -> `return a - b;` would survive because the test doesn't assert the outcome.
```

### ✅ GOOD: High Code Coverage, High Mutation Score

```typescript
// src/calculator.ts
export function add(a: number, b: number): number {
  return a + b;
}

// test/calculator.test.ts
import { add } from '../src/calculator';

describe('add', () => {
  it('should return the sum of two numbers', () => {
    expect(add(1, 2)).toBe(3); // Test asserts the correct behavior
  });

  it('should handle negative numbers', () => {
    expect(add(-1, 1)).toBe(0);
    expect(add(-1, -2)).toBe(-3);
  });
});
// Mutation: `return a + b;` -> `return a - b;` would be killed by the `expect(add(1, 2)).toBe(3);` assertion.
```

### ❌ BAD: Ignoring Irrelevant Mutants

```json
// stryker.conf.json (example snippet)
{
  "mutate": ["src/**/*.ts"],
  "excludedMutations": [] // No exclusions, leading to mutations in auto-generated code or trivial getters/setters
}
// This can lead to many survived mutants that are not indicative of test suite weakness,
// wasting time investigating non-issues.
```

### ✅ GOOD: Thoughtfully Excluding Irrelevant Mutants

```json
// stryker.conf.json (example snippet)
{
  "mutate": ["src/**/*.ts", "!src/generated/**/*.ts"], // Exclude generated code
  "excludedMutations": [
    "StringLiteral", // Often not useful to mutate string literals
    "BooleanLiteral" // Mutating true/false might not always reveal behavioral gaps
  ],
  "ignorePatterns": [
    "**/index.ts", // Often just re-exports, not much logic
    "**/*.d.ts" // Type definition files
  ]
}
// Focuses mutation testing on meaningful code and relevant mutation types.
```

## Code Review Checklist

- [ ] Is mutation testing configured for new or modified critical modules?
- [ ] Does the mutation score for the relevant modules meet the defined threshold?
- [ ] Are there any new survived mutants in the changes? If so, are they justified (e.g., equivalent mutants) or do they indicate a test gap?
- [ ] Have tests been added or improved to kill previously surviving mutants?
- [ ] Is the Stryker configuration up-to-date and optimized for the project (e.g., `ignorePatterns`, `excludedMutations`)?
- [ ] Are the tests asserting specific behaviors rather than just achieving coverage?

## Related Skills

- `test-driven-development`: Mutation testing provides excellent feedback for TDD cycles.
- `code-quality-metrics`: Mutation score is a key metric for overall code quality.
- `quality-gate-enforcement`: Mutation testing can be a critical component of CI/CD quality gates.
- `ci-cd-pipelines-github-actions`: How to integrate mutation testing into automated workflows.

## Examples Directory Structure

- `examples/typescript/simple-function/`
    - `src/calculator.ts`
    - `test/calculator.test.ts`
    - `stryker.conf.json`
- `examples/typescript/react-component/`
    - `src/components/Button.tsx`
    - `test/components/Button.test.ts`
    - `stryker.conf.json`

## Custom Scripts Section

For this skill, the following automation scripts will significantly enhance the developer workflow:

1.  **`setup-stryker.sh`**: A shell script to initialize Stryker Mutator in a TypeScript project, installing dependencies and creating a basic configuration file.
2.  **`run-mutation-tests.sh`**: A shell script to execute mutation tests with a specified configuration and generate a report, optionally filtering by changed files.
3.  **`analyze-mutation-report.py`**: A Python script to parse a Stryker JSON report, identify key areas for improvement (e.g., modules with low mutation scores, specific survived mutants), and provide actionable recommendations.
