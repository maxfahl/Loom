# Ruby on Rails Development Skill Package

This package provides Claude with comprehensive knowledge and tools for developing modern Ruby on Rails applications. It covers best practices, architectural patterns, performance optimization, security considerations, and includes automation scripts to streamline common development tasks.

## Contents

- `SKILL.md`: The main instruction file detailing core knowledge, guidance, anti-patterns, and a code review checklist for Ruby on Rails development.
- `examples/`: Directory containing practical code examples demonstrating modern Rails patterns (e.g., Hotwire, Service Objects, ViewComponents).
- `patterns/`: Directory with detailed explanations of common Rails architectural and coding patterns.
- `scripts/`: Automation scripts to assist with various development workflows.
- `README.md`: This documentation.

## Getting Started

Refer to `SKILL.md` for detailed guidance on leveraging this skill for Ruby on Rails projects.

## Automation Scripts

The `scripts/` directory contains the following utilities:

- `generate_service_object.sh`: Scaffolds a new Service Object.
- `check_n_plus_1_queries.py`: Analyzes Rails logs to detect N+1 query issues.
- `create_migration_with_index.sh`: Generates a migration with an index for a specified column.
- `setup_rspec.sh`: Sets up RSpec in a Rails project or generates basic spec files.

Each script includes detailed usage instructions and error handling. Please refer to the individual script files for more information.
