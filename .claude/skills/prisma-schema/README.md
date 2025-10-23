# Prisma Schema Design Skill

This skill provides comprehensive guidance and automation for designing and managing database schemas using Prisma ORM. It's designed to help developers and AI agents (like Claude) adhere to best practices, avoid common pitfalls, and efficiently evolve their database structures.

## What this Skill Covers

-   **Prisma Schema Language (SDL)**: Understanding models, enums, types, datasources, and generators.
-   **Data Modeling**: Best practices for defining fields, data types, and attributes (`@id`, `@unique`, `@default`, `@relation`, etc.).
-   **Relationships**: How to correctly define one-to-one, one-to-many, and many-to-many relationships with referential actions (`onDelete`).
-   **Database Migrations**: Using `prisma migrate` for version-controlled schema evolution in development and production environments.
-   **Common Pitfalls**: Identifying and avoiding issues like bad naming conventions, missing `onDelete` actions, and incorrect migration workflows.
-   **Performance & Integrity**: Guidance on indexing, data normalization, and ensuring data integrity.

## When to Use This Skill

Refer to this skill when you are:
-   Starting a new project with Prisma and need to define your initial database schema.
-   Adding new models or fields to an existing Prisma project.
-   Modifying relationships between your database entities.
-   Generating or applying database migrations.
-   Troubleshooting schema-related errors or migration failures.
-   Looking to optimize your Prisma schema for performance or maintainability.
-   Performing code reviews on `schema.prisma` files.

## Key Features

-   **Best Practices**: Clear recommendations for naming, relationships, and migration strategies.
-   **Anti-Patterns**: Examples of common mistakes and how to correct them.
-   **Code Review Checklist**: A handy list to ensure schema quality.
-   **Automation Scripts**: Time-saving scripts for scaffolding models, managing migrations, linting schemas, and generating seed data.

## Automation Scripts

This skill includes the following utility scripts in the `scripts/` directory:

-   `generate-model.sh`: Quickly scaffolds a new Prisma model with standard fields.
-   `prisma-migrate-wrapper.sh`: A safer wrapper for Prisma migrations (`dev` and `deploy`).
-   `schema-linter.py`: Lints your `schema.prisma` for best practice violations.
-   `seed-data-generator.py`: Generates basic seed data for specified models.

For detailed usage of each script, refer to their respective files in the `scripts/` directory.
