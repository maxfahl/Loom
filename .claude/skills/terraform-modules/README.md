# Terraform Modules Skill Package

This package provides Claude with the knowledge and tools to effectively work with Terraform modules, promoting best practices for reusability, maintainability, and consistency in Infrastructure as Code (IaC).

## Overview

Terraform modules are a fundamental concept for organizing, encapsulating, and reusing infrastructure configurations. This skill package equips Claude with the understanding of how to design, implement, consume, and validate Terraform modules according to industry standards.

## Contents

- **`SKILL.md`**: The core instruction file for Claude, detailing best practices, anti-patterns, and guidance for Terraform module development.
- **`examples/`**: Contains example Terraform configurations demonstrating how to use and structure modules.
- **`patterns/`**: Stores common Terraform module design patterns.
- **`scripts/`**: A collection of automation scripts to streamline common tasks related to Terraform modules.
- **`README.md` (this file)**: Human-readable documentation for the skill package.

## Custom Scripts

The `scripts/` directory contains the following automation tools:

### 1. `generate-module-boilerplate.sh`

- **Description**: Scaffolds a new Terraform module with the recommended directory structure (`main.tf`, `variables.tf`, `outputs.tf`, `versions.tf`, `README.md`, `examples/`, `patterns/`, `scripts/`).
- **Usage**:
    ```bash
    ./scripts/generate-module-boilerplate.sh <module_name> [--dry-run]
    ```
- **Example**:
    ```bash
    ./scripts/generate-module-boilerplate.sh aws-ec2-instance
    ./scripts/generate-module-boilerplate.sh vpc-network --dry-run
    ```

### 2. `update-module-docs.sh`

- **Description**: Automates the generation or update of `README.md` documentation for a Terraform module using `terraform-docs`. Ensures documentation (inputs, outputs, requirements, providers) is always accurate.
- **Usage**:
    ```bash
    ./scripts/update-module-docs.sh <module_path> [--check] [--dry-run]
    ```
- **Example**:
    ```bash
    ./scripts/update-module-docs.sh ./my-module
    ./scripts/update-module-docs.sh . --check
    ```
- **Prerequisite**: Requires `terraform-docs` to be installed.

### 3. `validate-terraform-module.sh`

- **Description**: Runs `terraform fmt -check`, `terraform validate`, and `tflint` across a specified Terraform module to ensure code quality, adherence to best practices, and correctness.
- **Usage**:
    ```bash
    ./scripts/validate-terraform-module.sh <module_path> [--dry-run]
    ```
- **Example**:
    ```bash
    ./scripts/validate-terraform-module.sh ./my-module
    ./scripts/validate-terraform-module.sh . --dry-run
    ```
- **Prerequisites**: Requires `terraform` and `tflint` to be installed.

### 4. `tf-module-version-updater.py`

- **Description**: A Python script to find and update the version constraint of a specified Terraform module within a root Terraform configuration file.
- **Usage**:
    ```bash
    python3 ./scripts/tf-module-version-updater.py <config_file> <module_name> <new_version> [--dry-run]
    ```
- **Example**:
    ```bash
    python3 ./scripts/tf-module-version-updater.py main.tf my-vpc-module "~> 2.0.0"
    python3 ./scripts/tf-module-version-updater.py prod/main.tf aws-s3-bucket "1.0.5" --dry-run
    ```

## Installation

To use this skill package, ensure you have the necessary tools installed:
- Terraform CLI
- `terraform-docs` (for `update-module-docs.sh`)
- `tflint` (for `validate-terraform-module.sh`)
- Python 3 (for `tf-module-version-updater.py`)

Place the `terraform-modules` directory within your Claude skills directory (e.g., `.devdev/skills/`).
