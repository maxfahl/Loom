# Jest Unit Tests Skill

This directory contains the Claude Skill package for writing effective unit tests with Jest for JavaScript and TypeScript applications. The goal of this skill is to guide Claude (and developers) in leveraging Jest's powerful features to ensure code quality, enable safe refactoring, and improve developer confidence.

## Contents

-   `SKILL.md`: The main instruction file for Claude, detailing the purpose, core knowledge, guidance, anti-patterns, and review checklist for Jest unit testing.
-   `examples/`: A directory containing practical code examples demonstrating various aspects of Jest testing.
-   `patterns/`: A directory for common Jest testing patterns, such as custom matchers and parameterized tests.
-   `scripts/`: A collection of automation scripts to assist with Jest workflow, including project initialization, test running, coverage reporting, and mock generation.
-   `README.md`: This human-readable documentation.

## Getting Started

To understand how Claude utilizes this skill, refer to the `SKILL.md` file. For practical demonstrations, explore the `examples/` directory. The `scripts/` directory provides tools to automate common tasks related to Jest unit testing.

## Automation Scripts

The `scripts/` directory contains the following utilities:

1.  **`jest-init.sh`**: Initializes a new project with Jest configured.
2.  **`jest-test-watcher.sh`**: Runs Jest in watch mode for rapid feedback.
3.  **`jest-coverage-reporter.sh`**: Generates detailed test coverage reports.
4.  **`jest-mock-generator.js`**: Generates boilerplate mock files for modules/classes.

Refer to the individual script files for detailed usage instructions and examples.
