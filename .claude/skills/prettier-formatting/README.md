# Prettier Formatting Skill

This package contains a Claude skill for understanding and using Prettier, an opinionated code formatter.

## Description

Prettier enforces a consistent code style across your entire codebase by parsing your code and re-printing it with its own rules. This saves time and mental energy by automating the process of formatting code.

This skill enables Claude to:
- Configure Prettier for a new or existing project.
- Integrate Prettier with ESLint to avoid rule conflicts.
- Set up automated formatting workflows using editor integration and pre-commit hooks.
- Troubleshoot common Prettier issues.

## Components

### `SKILL.md`

The core instruction file for Claude. It contains detailed information on when to use the skill, core concepts, best practices, and anti-patterns.

### `scripts/`

This directory contains automation scripts to help with common Prettier-related tasks:

- **`setup-prettier.sh`**: A shell script to initialize a new project with Prettier, a default configuration, and `package.json` scripts.
- **`check-format.sh`**: A shell script to check for unformatted files, suitable for use in CI/CD pipelines.
- **`format-staged.sh`**: A shell script designed to be used with a pre-commit hook (like `husky` and `lint-staged`) to format only the files that are staged for commit.
- **`init-prettierignore.py`**: A Python script that generates a comprehensive `.prettierignore` file with common patterns for various project types.

### `examples/`

This directory will contain sample files to demonstrate how Prettier formats different types of code.

### `patterns/`

This directory will contain common code patterns related to Prettier configuration and usage.

## Usage

To use the scripts, navigate to the `scripts/` directory and execute them directly. For example:

```bash
# To set up Prettier in a project
bash ./setup-prettier.sh

# To check for unformatted files
bash ./check-format.sh
```

The `SKILL.md` file is intended for use by Claude and provides the foundational knowledge for the AI to assist with Prettier-related tasks.
