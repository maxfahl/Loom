# TypeScript Strict Mode Skill

This directory contains the Claude Skill package for enforcing strict type-checking in TypeScript. The goal of this skill is to guide Claude (and developers) in writing robust, maintainable, and bug-free TypeScript code by leveraging the full power of TypeScript's strict mode.

## Contents

-   `SKILL.md`: The main instruction file for Claude, detailing the purpose, core knowledge, guidance, anti-patterns, and review checklist for TypeScript strict mode.
-   `examples/`: A directory containing practical code examples demonstrating various aspects of strict mode.
-   `patterns/`: A directory for common TypeScript type patterns that align with strict mode principles.
-   `scripts/`: A collection of automation scripts to assist with strict mode adoption, migration, and analysis.
-   `README.md`: This human-readable documentation.

## Getting Started

To understand how Claude utilizes this skill, refer to the `SKILL.md` file. For practical demonstrations, explore the `examples/` directory. The `scripts/` directory provides tools to automate common tasks related to TypeScript strict mode.

## Automation Scripts

The `scripts/` directory contains the following utilities:

1.  **`strict-mode-initializer.sh`**: Sets up a new TypeScript project with a strict `tsconfig.json`.
2.  **`strict-mode-migrator.py`**: Helps migrate existing projects to strict mode by identifying and suggesting fixes for type violations.
3.  **`strict-mode-checker.sh`**: Runs focused TypeScript strictness checks, ideal for CI/CD pipelines.
4.  **`strict-mode-type-coverage.py`**: Analyzes and reports on the strictness coverage of your codebase.

Refer to the individual script files for detailed usage instructions and examples.
