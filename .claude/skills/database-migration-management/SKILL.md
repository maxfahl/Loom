---
Name: database-migration-management
Version: 1.0.0
Category: Database / DevOps
Tags: PostgreSQL, migrations, node-pg-migrate, TypeScript, database, schema evolution, DevOps
Description: Manages PostgreSQL database schema evolution using node-pg-migrate with TypeScript.
---

# Database Migration Management with node-pg-migrate

This skill enables Claude to effectively manage PostgreSQL database schema changes using `node-pg-migrate` in TypeScript projects. It covers best practices for creating, applying, and reverting migrations, ensuring database integrity and smooth deployments.

## Skill Purpose

This skill empowers Claude to guide developers through the process of defining, applying, and managing database schema changes in a version-controlled, reproducible, and safe manner. It focuses on leveraging `node-pg-migrate`'s capabilities within a TypeScript ecosystem to maintain database consistency across different environments and facilitate collaborative development.

## When to Activate This Skill

Activate this skill when the user's task involves:

*   **Schema Modification**: Any changes to the database structure (e.g., adding/altering/dropping tables, columns, indexes, constraints, views, functions).
*   **Project Setup**: Initializing a new project that requires a PostgreSQL database with a defined schema.
*   **Deployment**: Integrating database schema updates into CI/CD pipelines for application deployments.
*   **Troubleshooting**: Diagnosing and resolving database schema inconsistencies or errors.
*   **Rollbacks**: Reverting database changes to a previous state.
*   **Code Review**: Reviewing migration files for best practices and potential issues.

## Core Knowledge

To effectively utilize this skill, Claude should understand:

*   **`node-pg-migrate` Fundamentals**:
    *   **`up()` and `down()` functions**: The core of each migration, defining how to apply and revert changes.
    *   **`pgm` object**: The API provided by `node-pg-migrate` for performing DDL operations (e.g., `createTable`, `addColumns`, `dropTable`).
    *   **Migration file structure**: How migration files are organized and named.
    *   **CLI commands**: `create`, `up`, `down`, `redo`, `reset`, `status`.
*   **PostgreSQL DDL (Data Definition Language)**:
    *   `CREATE TABLE`, `ALTER TABLE`, `DROP TABLE`
    *   `CREATE INDEX`, `DROP INDEX`
    *   `ALTER COLUMN`, `ADD COLUMN`, `DROP COLUMN`
    *   `ADD CONSTRAINT`, `DROP CONSTRAINT`
    *   `CREATE TYPE`, `DROP TYPE`
*   **TypeScript**:
    *   Type safety in migration files, ensuring correct schema definitions.
    *   `tsconfig.json` configuration for migration files.
*   **Database Best Practices**:
    *   **Atomic Changes**: Each migration should focus on a single, logical change.
    *   **Idempotency**: Migrations should be runnable multiple times without unintended side effects (though `node-pg-migrate` handles much of this).
    *   **Version Control**: Migrations are code and should be treated as such.
    *   **Testing**: Thoroughly testing migrations in non-production environments.
    *   **Environment Variables**: Securely managing database connection strings.
*   **CI/CD Integration**: Strategies for automating migration execution in deployment pipelines (e.g., running `node-pg-migrate up` before application deployment).

## Key Guidance for Claude

### Always Recommend (✅ best practices)

*   ✅ **TypeScript First**: Always write migration files using TypeScript (`.ts` extension) to leverage type checking and improve code quality.
*   ✅ **Version Control**: Store all migration files in your project's version control system (e.g., Git) alongside your application code.
*   ✅ **Dedicated Directory**: Organize migration files in a clearly defined directory, typically `src/migrations`, `db/migrations`, or `migrations` at the project root.
*   ✅ **Descriptive Naming**: Use a consistent, timestamped, and descriptive naming convention for migration files (e.g., `YYYYMMDDHHmmss_add_users_table.ts`). `node-pg-migrate` relies on this for ordering.
*   ✅ **Bidirectional Migrations**: Always implement both `up()` and `down()` functions in each migration file. The `down()` function should precisely reverse the changes made by `up()`. This is crucial for rollbacks and development flexibility.
*   ✅ **Atomic Changes**: Design each migration to perform a single, logical change to the database schema. This makes migrations easier to understand, debug, and revert.
*   ✅ **Thorough Testing**: Test migrations extensively in development and staging environments. This includes testing both `up()` and `down()` operations.
*   ✅ **Automated Execution**: Integrate migration execution into your CI/CD pipeline. Migrations should run automatically as part of your deployment process before the application starts.
*   ✅ **Environment Variables**: Use environment variables (e.g., `DATABASE_URL`) for all sensitive database connection details. Never hardcode credentials.
*   ✅ **Database Backups**: Emphasize the importance of creating a full database backup before applying any migrations in a production environment.
*   ✅ **Zero-Downtime Migrations**: For high-availability applications, plan migrations to be non-blocking and avoid long-running locks to minimize downtime. This often involves a multi-step approach (e.g., add new column, deploy code using both, migrate data, remove old column).

### Never Recommend (❌ anti-patterns)

*   ❌ **Modifying Applied Migrations**: Never alter a migration file after it has been applied to a shared environment (e.g., staging, production). If a change is needed, create a new migration.
*   ❌ **Complex, Multi-Purpose Migrations**: Avoid creating migration files that perform many unrelated schema changes. This makes them difficult to understand, test, and revert.
*   ❌ **Hardcoding Credentials**: Do not embed database usernames, passwords, or connection strings directly in migration files or configuration.
*   ❌ **Missing `down()` Functions**: Never omit the `down()` function. This severely hinders the ability to rollback changes and can lead to irreversible schema states.
*   ❌ **Manual Production Migrations**: Avoid manually running migrations in production. Always automate this process through CI/CD.
*   ❌ **Ignoring Backups**: Do not proceed with production deployments involving migrations without a recent, verified database backup.
*   ❌ **Direct SQL Injection**: Be vigilant about constructing SQL queries safely within migrations, avoiding direct concatenation of untrusted input.

### Common Questions & Responses (FAQ format)

*   **Q: How do I create a new migration file?**
    *   **A**: Use the `node-pg-migrate create <migration_name> --language ts` command. For example: `node-pg-migrate create add_users_table --language ts`.
*   **Q: What's the command to apply all pending migrations?**
    *   **A**: Run `node-pg-migrate up`. This will apply all migrations that haven't been run yet, in chronological order.
*   **Q: How can I revert the last applied migration?**
    *   **A**: Use `node-pg-migrate down`. To revert multiple migrations, you can specify a count, e.g., `node-pg-migrate down 2`.
*   **Q: My project already has an existing database schema. How do I start using `node-pg-migrate` without running all migrations from scratch?**
    *   **A**: You can create an initial "fake" migration. First, dump your existing schema using `pg_dump --schema-only > initial_schema.sql`. Then, create a new migration file (e.g., `YYYYMMDDHHmmss_initial_schema.ts`) that represents this schema. Finally, apply this migration with `node-pg-migrate up --fake`. This marks the initial schema as applied in the `pgmigrations` table without actually executing the DDL.
*   **Q: How do I configure `node-pg-migrate` to connect to my database?**
    *   **A**: `node-pg-migrate` primarily uses environment variables. Set `DATABASE_URL` (e.g., `postgres://user:password@host:port/database`) or individual variables like `PGHOST`, `PGUSER`, `PGPASSWORD`, `PGDATABASE`, `PGPORT`. You can also use a `.env` file with tools like `dotenv`.
*   **Q: What if a migration fails during `up()`?**
    *   **A**: `node-pg-migrate` typically wraps migrations in transactions, so a failure should roll back the changes. Inspect the error logs, fix the issue in the migration file (if it hasn't been applied to shared environments), or create a new migration to correct the problem. If it's a shared environment, you might need to `down` the failed migration (if partially applied) and then `up` again after fixing.

## Anti-Patterns to Flag

Here are common anti-patterns and how to correct them:

### Anti-pattern: Modifying an already applied migration

**BAD:**
```typescript
// migrations/20230101000000_create_users_table.ts (already applied to production)
import { MigrationBuilder } from 'node-pg-migrate';

export async function up(pgm: MigrationBuilder): Promise<void> {
  pgm.createTable('users', {
    id: 'id',
    name: { type: 'varchar(255)', notNull: true },
    // Oops, forgot email! Adding it here directly.
    email: { type: 'varchar(255)', notNull: true, unique: true },
    createdAt: {
      type: 'timestamp',
      notNull: true,
      default: pgm.func('current_timestamp'),
    },
  });
}

export async function down(pgm: MigrationBuilder): Promise<void> {
  pgm.dropTable('users');
}
```
**Why it's bad**: Modifying an already applied migration can lead to inconsistencies between environments, especially if the change is applied to some but not all instances of the database. It breaks the immutability of migration history.

**GOOD:**
```typescript
// migrations/20230101000000_create_users_table.ts (unchanged)
import { MigrationBuilder } from 'node-pg-migrate';

export async function up(pgm: MigrationBuilder): Promise<void> {
  pgm.createTable('users', {
    id: 'id',
    name: { type: 'varchar(255)', notNull: true },
    createdAt: {
      type: 'timestamp',
      notNull: true,
      default: pgm.func('current_timestamp'),
    },
  });
}

export async function down(pgm: MigrationBuilder): Promise<void> {
  pgm.dropTable('users');
}

// migrations/20230102000000_add_email_to_users.ts (new migration)
import { MigrationBuilder } from 'node-pg-migrate';

export async function up(pgm: MigrationBuilder): Promise<void> {
  pgm.addColumns('users', {
    email: {
      type: 'varchar(255)',
      notNull: true,
      unique: true,
    },
  });
}

export async function down(pgm: MigrationBuilder): Promise<void> {
  pgm.dropColumns('users', ['email']);
}
```
**Explanation**: Create a new migration to introduce the `email` column. This preserves the history and ensures all environments evolve consistently.

### Anti-pattern: Non-atomic migrations

**BAD:**
```typescript
// migrations/20230103000000_initial_setup.ts
import { MigrationBuilder } from 'node-pg-migrate';

export async function up(pgm: MigrationBuilder): Promise<void> {
  pgm.createTable('users', { /* ... */ });
  pgm.createTable('products', { /* ... */ });
  pgm.addColumns('users', { /* ... */ });
  pgm.createIndex('products', ['name']);
  pgm.sql(`INSERT INTO settings (key, value) VALUES ('app_version', '1.0.0');`);
}

export async function down(pgm: MigrationBuilder): Promise<void> {
  // This down function would be very complex and error-prone to reverse everything
  pgm.dropTable('products');
  pgm.dropTable('users');
  // ... and so on
}
```
**Why it's bad**: This migration does too many things. If one step fails, it's hard to recover. Reverting it is also very complex and prone to errors.

**GOOD:**
```typescript
// migrations/20230103000000_create_users_table.ts
import { MigrationBuilder } from 'node-pg-migrate';
export async function up(pgm: MigrationBuilder): Promise<void> { pgm.createTable('users', { /* ... */ }); }
export async function down(pgm: MigrationBuilder): Promise<void> { pgm.dropTable('users'); }

// migrations/20230103000001_create_products_table.ts
import { MigrationBuilder } from 'node-pg-migrate';
export async function up(pgm: MigrationBuilder): Promise<void> { pgm.createTable('products', { /* ... */ }); }
export async function down(pgm: MigrationBuilder): Promise<void> { pgm.dropTable('products'); }

// migrations/20230103000002_add_product_name_index.ts
import { MigrationBuilder } from 'node-pg-migrate';
export async function up(pgm: MigrationBuilder): Promise<void> { pgm.createIndex('products', ['name']); }
export async function down(pgm: MigrationBuilder): Promise<void> { pgm.dropIndex('products', ['name']); }

// migrations/20230103000003_insert_initial_settings.ts
import { MigrationBuilder } from 'node-pg-migrate';
export async function up(pgm: MigrationBuilder): Promise<void> { pgm.sql(`INSERT INTO settings (key, value) VALUES ('app_version', '1.0.0');`); }
export async function down(pgm: MigrationBuilder): Promise<void> { pgm.sql(`DELETE FROM settings WHERE key = 'app_version';`); }
```
**Explanation**: Each migration handles a single, logical change. This makes them easier to manage, test, and revert.

## Code Review Checklist

*   [ ] **TypeScript Usage**: Are migration files written in TypeScript (`.ts`)?
*   [ ] **Bidirectional**: Does each migration file export both an `up()` and a `down()` function?
*   [ ] **Reversibility**: Is the `down()` function a true and safe inverse of the `up()` function?
*   [ ] **Naming Convention**: Is the migration file named descriptively and with a correct timestamp (e.g., `YYYYMMDDHHmmss_description.ts`)?
*   [ ] **Atomicity**: Does each migration perform a single, logical schema change?
*   [ ] **Idempotency (where applicable)**: Are DDL statements written to be idempotent where possible (e.g., `CREATE TABLE IF NOT EXISTS`)?
*   [ ] **Environment Variables**: Are all sensitive database connection details sourced from environment variables?
*   [ ] **No Hardcoded Values**: Are there no hardcoded credentials or environment-specific configurations?
*   [ ] **SQL Safety**: Are raw SQL queries safe from injection vulnerabilities?
*   [ ] **Performance Considerations**: For large tables, are indexes added concurrently? Are long-running locks avoided?
*   [ ] **Data Integrity**: Are there any potential data loss scenarios, and if so, are they mitigated or clearly documented?
*   [ ] **Foreign Keys**: Are foreign key constraints handled correctly (e.g., `ON DELETE CASCADE`, `ON UPDATE RESTRICT`)?

## Related Skills

*   [`typescript-strict-mode`](./typescript-strict-mode/SKILL.md): For ensuring high-quality, type-safe TypeScript code in migrations.
*   [`ci-cd-pipelines-github-actions`](./ci-cd-pipelines-github-actions/SKILL.md): For automating the execution of migrations in continuous integration and deployment workflows.
*   [`docker-best-practices`](./docker-best-practices/SKILL.md): For setting up and managing local PostgreSQL databases for development and testing environments.

## Examples Directory Structure

*   `examples/simple-table-creation.ts`
*   `examples/add-column-with-default.ts`
*   `examples/create-index.ts`
*   `examples/alter-column-type.ts`
*   `examples/add-foreign-key.ts`

## Custom Scripts Section

This section outlines automation scripts designed to streamline common `node-pg-migrate` workflows, saving significant developer time and reducing manual errors.

### 1. `create-migration.sh`

**Purpose**: Automates the creation of a new `node-pg-migrate` TypeScript migration file with a proper timestamp and boilerplate.

**Usage**:
```bash
./scripts/create-migration.sh <migration_name>
```

**Example**:
```bash
./scripts/create-migration.sh add_users_table
```

### 2. `db-reset-and-seed.sh`

**Purpose**: Resets the local development database, applies all pending migrations, and optionally runs a seeding script to populate it with test data.

**Usage**:
```bash
./scripts/db-reset-and-seed.sh [--seed <seed_script_path>] [--no-confirm]
```

**Example**:
```bash
./scripts/db-reset-and-seed.sh --seed ./scripts/seed-dev-data.ts
```

### 3. `validate-migrations.sh`

**Purpose**: Performs static analysis and checks on migration files to ensure they adhere to best practices (e.g., presence of `down()` function, proper naming, linting).

**Usage**:
```bash
./scripts/validate-migrations.sh [--path <migrations_dir>]
```

**Example**:
```bash
./scripts/validate-migrations.sh --path src/migrations
```

### 4. `generate-initial-migration.sh`

**Purpose**: Generates an initial `node-pg-migrate` migration file from an existing PostgreSQL database schema using `pg_dump`. This is useful when onboarding `node-pg-migrate` to an existing project.

**Usage**:
```bash
./scripts/generate-initial-migration.sh [--output <output_file_path>] [--db-url <database_url>]
```

**Example**:
```bash
./scripts/generate-initial-migration.sh --output src/migrations/initial_schema.ts
```
