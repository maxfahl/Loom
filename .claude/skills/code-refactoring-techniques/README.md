# Code Refactoring Techniques Skill

This directory contains the Claude skill package for **Code Refactoring Techniques**.

## Overview

This skill provides Claude with the knowledge and tools to assist developers in improving code quality, maintainability, and readability through various refactoring practices. It covers fundamental principles, common techniques, and guidance on when and how to apply them effectively.

## Contents

-   `SKILL.md`: The main instruction file for Claude, detailing the purpose, core knowledge, guidance, anti-patterns, and a code review checklist for refactoring.
-   `examples/`: A collection of TypeScript code examples demonstrating "bad" code patterns and their "good" refactored counterparts.
-   `patterns/`: (Currently empty, reserved for future common refactoring patterns or templates).
-   `scripts/`: Automation scripts designed to streamline common refactoring-related tasks.

## How to Use This Skill (for Developers)

Refer to `SKILL.md` for detailed guidance on code refactoring. The `examples/` directory provides practical illustrations of refactoring techniques. The `scripts/` directory contains utility scripts that can help automate parts of your refactoring workflow.

## Automation Scripts

This skill includes the following automation scripts:

1.  `smell-detector.py`: Scans TypeScript files for common code smells.
2.  `extract-function-helper.py`: An interactive helper for "Extract Method/Function" refactoring.
3.  `ref-updater.sh`: Updates references after file moves or symbol renames.
4.  `format-and-lint.sh`: Automates code formatting and linting.

For detailed usage instructions for each script, please refer to the script files themselves within the `scripts/` directory.
