# PostgreSQL Advanced Features Skill

This directory contains the Claude Skill Package for advanced PostgreSQL features. This skill enables Claude to provide expert guidance on optimizing PostgreSQL performance, scaling databases, implementing robust security, and managing complex data structures.

For detailed instructions, core knowledge, guidance, anti-patterns, and code review checklists, please refer to [SKILL.md](SKILL.md).

## Directory Structure

*   `SKILL.md`: The main instruction file for Claude, detailing the skill's purpose, knowledge, and guidance.
*   `examples/`: Contains code examples demonstrating advanced PostgreSQL features.
*   `patterns/`: Stores common SQL patterns and best practices.
*   `scripts/`: Houses automation scripts to assist with common PostgreSQL tasks.

## Custom Scripts

The `scripts/` directory includes several automation tools to streamline advanced PostgreSQL development and operations:

*   `pg_config_optimizer.py`: Optimizes `postgresql.conf` parameters based on system resources.
*   `pg_index_analyzer.py`: Analyzes database activity to recommend or identify inefficient indexes.
*   `pg_partition_generator.py`: Generates SQL DDL for declarative table partitioning.
*   `pg_rls_policy_manager.py`: Helps create, view, and audit Row-Level Security policies.
