# Django REST Framework (DRF) Skill

This directory contains the Claude Skill package for building robust, scalable, and secure REST APIs with Django REST Framework. The goal of this skill is to guide Claude (and developers) in effectively designing, implementing, and optimizing DRF-based APIs.

## Contents

-   `SKILL.md`: The main instruction file for Claude, detailing the purpose, core knowledge, guidance, anti-patterns, and review checklist for DRF development.
-   `examples/`: A directory containing practical code examples demonstrating various aspects of DRF, such as basic CRUD, custom permissions, and nested serializers.
-   `patterns/`: A directory for common DRF patterns, including service layer abstraction and custom throttling.
-   `scripts/`: A collection of automation scripts to assist with DRF workflow, including project initialization, app generation, permission generation, and serializer validation.
-   `README.md`: This human-readable documentation.

## Getting Started

To understand how Claude utilizes this skill, refer to the `SKILL.md` file. For practical demonstrations, explore the `examples/` directory. The `scripts/` directory provides tools to automate common tasks related to Django REST Framework.

## Automation Scripts

The `scripts/` directory contains the following utilities:

1.  **`drf-project-init.sh`**: Initializes a new Django project with DRF setup.
2.  **`drf-app-generator.py`**: Generates boilerplate for a new DRF app.
3.  **`drf-permission-generator.py`**: Generates templates for custom DRF permission classes.
4.  **`drf-serializer-validator.py`**: Analyzes DRF serializers for common issues.

Refer to the individual script files for detailed usage instructions and examples.
