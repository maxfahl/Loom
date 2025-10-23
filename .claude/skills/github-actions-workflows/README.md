# GitHub Actions Workflows Skill Package

This package provides Claude with the knowledge and tools to effectively design, implement, and manage GitHub Actions workflows, promoting best practices for security, performance, and maintainability in CI/CD pipelines.

## Overview

GitHub Actions enable powerful automation directly within your GitHub repositories. This skill package equips Claude with the understanding of how to leverage GitHub Actions for continuous integration, continuous delivery, and other automation tasks, adhering to modern development standards.

## Contents

- **`SKILL.md`**: The core instruction file for Claude, detailing best practices, anti-patterns, and guidance for GitHub Actions workflow development.
- **`examples/`**: Contains example GitHub Actions workflow YAML files demonstrating various use cases and configurations.
- **`patterns/`**: Stores common GitHub Actions workflow patterns and reusable components.
- **`scripts/`**: A collection of automation scripts to streamline common tasks related to GitHub Actions.
- **`README.md` (this file)**: Human-readable documentation for the skill package.

## Custom Scripts

The `scripts/` directory contains the following automation tools:

### 1. `generate-workflow-boilerplate.sh`

- **Description**: Scaffolds a new GitHub Actions workflow file (`.yml`) with a basic structure, including common jobs (build, test, deploy) and incorporating best practices like action version pinning and caching.
- **Usage**:
    ```bash
    ./scripts/generate-workflow-boilerplate.sh <workflow_name> [--type <ci|cd|full>] [--dry-run]
    ```
- **Example**:
    ```bash
    ./scripts/generate-workflow-boilerplate.sh my-app-ci
    ./scripts/generate-workflow-boilerplate.sh deploy-prod --type cd
    ```

### 2. `pin-action-versions.py`

- **Description**: Automatically updates GitHub Actions references in a workflow file to use specific commit SHAs instead of floating tags or branches. This enhances security and workflow stability.
- **Usage**:
    ```bash
    python3 ./scripts/pin-action-versions.py <workflow_file> [--dry-run]
    ```
- **Example**:
    ```bash
    python3 ./scripts/pin-action-versions.py .github/workflows/ci.yml
    python3 ./scripts/pin-action-versions.py .github/workflows/deploy.yml --dry-run
    ```
- **Prerequisites**: Requires `PyYAML` and `requests` Python packages (`pip install PyYAML requests`) and a GitHub Personal Access Token (PAT) with `repo` scope set as `GITHUB_TOKEN` environment variable.

### 3. `validate-workflow.sh`

- **Description**: Validates and lints GitHub Actions workflow files using `actionlint`. Ensures workflow syntax is correct, follows best practices, and helps catch common errors.
- **Usage**: 
    ```bash
    ./scripts/validate-workflow.sh [<workflow_file_or_dir>] [--dry-run]
    ```
- **Example**:
    ```bash
    ./scripts/validate-workflow.sh .github/workflows/ci.yml
    ./scripts/validate-workflow.sh .github/workflows
    ```
- **Prerequisite**: Requires `actionlint` to be installed.

### 4. `list-workflow-secrets.sh`

- **Description**: Lists GitHub repository secrets for a given repository using the GitHub CLI (`gh`). Useful for reviewing available secrets without navigating the GitHub UI.
- **Usage**:
    ```bash
    ./scripts/list-workflow-secrets.sh <owner/repo> [--dry-run]
    ```
- **Example**:
    ```bash
    ./scripts/list-workflow-secrets.sh myorg/my-repo
    ./scripts/list-workflow-secrets.sh octocat/Spoon-Knife --dry-run
    ```
- **Prerequisite**: Requires the GitHub CLI (`gh`) to be installed and authenticated (`gh auth login`).

## Installation

To use this skill package, ensure you have the necessary tools installed:
- GitHub CLI (`gh`)
- `actionlint` (for `validate-workflow.sh`)
- Python 3 with `PyYAML` and `requests` (for `pin-action-versions.py`)

Place the `github-actions-workflows` directory within your Claude skills directory (e.g., `.devdev/skills/`).
