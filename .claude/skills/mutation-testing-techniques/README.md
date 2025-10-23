# Mutation Testing Techniques Skill

This skill package provides guidance, examples, and automation scripts for applying mutation testing to assess the effectiveness of your test suites.

## What is Mutation Testing?

Mutation testing is a powerful technique to evaluate the quality of your tests. It works by introducing small, deliberate changes (mutations) into your source code. If your tests fail when these changes are introduced, it means your tests are effective at catching behavioral differences. If your tests still pass, it indicates a gap in your test suite that could allow real bugs to slip through.

## Why Use This Skill?

- **Identify Weak Tests**: Discover tests that pass even when the underlying code's behavior has changed.
- **Improve Test Quality**: Learn to write more robust and meaningful tests that truly assert behavior.
- **Enhance Code Confidence**: Gain higher confidence in your codebase, especially during refactoring or feature development.
- **Automate Quality Gates**: Integrate mutation testing into your CI/CD pipeline to enforce high standards of test effectiveness.

## Contents

- `SKILL.md`: The main instruction file for Claude, detailing the purpose, core knowledge, guidance, anti-patterns, and more.
- `examples/`: Practical code examples demonstrating mutation testing setup and usage in TypeScript projects.
- `patterns/`: Common patterns and best practices for effective mutation testing.
- `scripts/`: Automation scripts to streamline mutation testing workflows.

## Getting Started

Refer to the `SKILL.md` for detailed guidance on how to leverage mutation testing. Explore the `examples/` directory to see practical implementations, and utilize the `scripts/` to automate common tasks.

## Automation Scripts

This package includes the following scripts to help you with mutation testing:

- `setup-stryker.sh`: Initializes Stryker Mutator in a TypeScript project.
- `run-mutation-tests.sh`: Executes mutation tests and generates reports.
- `analyze-mutation-report.py`: Parses Stryker reports to provide actionable insights.

For detailed usage of each script, refer to their respective files in the `scripts/` directory.
