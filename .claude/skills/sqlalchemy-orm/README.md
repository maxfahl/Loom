# SQLAlchemy ORM Skill Package

This package provides a comprehensive skill set for working with SQLAlchemy ORM, focusing on modern best practices, performance optimization, and maintainable code. It includes detailed guidance, anti-pattern examples, a code review checklist, and automation scripts to streamline development with SQLAlchemy.

## Contents

*   `SKILL.md`: The main instruction file for Claude, detailing core knowledge, best practices, and common pitfalls.
*   `examples/`: Directory containing example code snippets demonstrating various SQLAlchemy ORM features and patterns.
*   `patterns/`: Directory for common design patterns related to SQLAlchemy ORM (e.g., Repository Pattern).
*   `scripts/`: Automation scripts to assist with common SQLAlchemy ORM development tasks.
*   `README.md`: This documentation.

## Getting Started

Refer to `SKILL.md` for detailed guidance on using SQLAlchemy ORM effectively.

## Automation Scripts

Explore the `scripts/` directory for useful automation tools:

*   `alembic_setup.sh`: Automates Alembic initialization and initial migration generation.
*   `generate_model.py`: Generates basic SQLAlchemy 2.0 declarative models.
*   `n_plus_1_detector.py`: Helps detect potential N+1 query issues.
*   `session_factory_template.py`: Generates a best-practice session factory with dependency injection.
