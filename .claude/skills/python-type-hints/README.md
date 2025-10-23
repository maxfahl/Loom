# Python Type Hints Skill

This directory contains the Claude Skill package for effectively using type hints in Python. The goal of this skill is to guide Claude (and developers) in writing more robust, readable, and maintainable Python code by leveraging type hints for static analysis, improved IDE support, and enhanced documentation.

## Contents

-   `SKILL.md`: The main instruction file for Claude, detailing the purpose, core knowledge, guidance, anti-patterns, and review checklist for Python type hints.
-   `examples/`: A directory containing practical code examples demonstrating various aspects of type hinting.
-   `patterns/`: A directory for common Python type hinting patterns, such as Pydantic integration or runtime type checking.
-   `scripts/`: A collection of automation scripts to assist with type hint adoption, migration, checking, and coverage analysis.
-   `README.md`: This human-readable documentation.

## Getting Started

To understand how Claude utilizes this skill, refer to the `SKILL.md` file. For practical demonstrations, explore the `examples/` directory. The `scripts/` directory provides tools to automate common tasks related to Python type hints.

## Automation Scripts

The `scripts/` directory contains the following utilities:

1.  **`type-hint-initializer.py`**: Sets up a new Python project with a basic structure and type checking configuration.
2.  **`type-hint-migrator.py`**: Helps migrate existing Python projects by identifying and suggesting type hint additions.
3.  **`type-hint-checker.sh`**: Runs a static type checker (e.g., Mypy, Pyright) on the project.
4.  **`type-hint-coverage.py`**: Analyzes and reports on the type hint coverage of your codebase.

Refer to the individual script files for detailed usage instructions and examples.
