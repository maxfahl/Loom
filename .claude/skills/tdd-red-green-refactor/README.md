# TDD: Red-Green-Refactor Skill

This directory contains the Claude Skill package for practicing Test-Driven Development (TDD) using the Red-Green-Refactor cycle. The goal of this skill is to guide Claude (and developers) in building high-quality, robust, and maintainable software through a disciplined, iterative development process.

## Contents

-   `SKILL.md`: The main instruction file for Claude, detailing the purpose, core knowledge, guidance, anti-patterns, and review checklist for TDD.
-   `examples/`: A directory containing practical code examples demonstrating the Red-Green-Refactor cycle in action.
-   `patterns/`: A directory for common testing patterns, such as test doubles and assertion techniques.
-   `scripts/`: A collection of automation scripts to assist with TDD workflow, including project initialization, test running, refactoring guidance, and test file generation.
-   `README.md`: This human-readable documentation.

## Getting Started

To understand how Claude utilizes this skill, refer to the `SKILL.md` file. For practical demonstrations, explore the `examples/` directory. The `scripts/` directory provides tools to automate common tasks related to TDD.

## Automation Scripts

The `scripts/` directory contains the following utilities:

1.  **`tdd-init.sh`**: Initializes a new project with a basic testing framework setup.
2.  **`test-runner.sh`**: Runs tests efficiently, supporting watch mode and specific test filters.
3.  **`refactor-helper.py`**: Analyzes code for common refactoring opportunities.
4.  **`test-template-generator.py`**: Generates boilerplate test files for a given source file.

Refer to the individual script files for detailed usage instructions and examples.
