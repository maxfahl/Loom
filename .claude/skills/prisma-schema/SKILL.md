---
name: prisma-schema
version: 1.0.0
category: Database / ORM
tags: Prisma, Schema, Database, ORM, TypeScript, Migration
description: Designing and managing database schemas with Prisma ORM.
---

# Prisma Schema Design

## Skill Purpose

This skill enables Claude to effectively design, evolve, and maintain database schemas using Prisma ORM's declarative schema language. It covers data modeling, defining relationships, managing migrations, and adhering to best practices for building robust and scalable applications. Claude will be able to assist with creating new models, modifying existing ones, generating and applying migrations, troubleshooting schema-related issues, and optimizing database interactions.

## When to Activate This Skill

Activate this skill when the task involves:
- Defining new database models or entities.
- Modifying existing database schemas (adding/removing fields, changing types).
- Establishing or altering relationships between models.
- Generating, reviewing, or applying database migrations.
- Troubleshooting Prisma schema validation errors or migration failures.
- Optimizing database queries or schema performance with Prisma.
- Discussing data modeling strategies for a new feature or application.

**Keywords:** `Prisma schema`, `database model`, `data migration`, `define relationship`, `Prisma ORM`, `schema.prisma`, `model definition`, `database design`.

## Core Knowledge

Claude should possess a deep understanding of the following Prisma concepts:

### Prisma Schema Language (SDL)
-   **`model`**: Defines a database table and its fields.
-   **`enum`**: Defines a set of allowed values for a field.
-   **`type`**: Defines a composite type for reusing field sets.
-   **`datasource`**: Configures the database connection.
-   **`generator`**: Configures Prisma Client and other generated assets.

### Data Types
-   `String`, `Int`, `Boolean`, `DateTime`, `Json`, `Bytes`, `Decimal`, `BigInt`.
-   Understanding of native database types mapping.

### Field Attributes
-   `@id`: Defines the primary key.
-   `@unique`: Ensures unique values for a field.
-   `@default`: Sets a default value for a field.
-   `@map("column_name")`: Maps a field to a different column name in the database.
-   `@relation`: Defines relationships between models.
-   `@updatedAt`: Automatically updates a `DateTime` field on record updates.
-   `@db.NativeType`: Specifies a native database type.

### Model Attributes
-   `@@id([field1, field2])`: Defines a composite primary key.
-   `@@unique([field1, field2])`: Defines a composite unique constraint.
-   `@@index([field1, field2])`: Defines a composite index.
-   `@@map("table_name")`: Maps a model to a different table name in the database.

### Relationships
-   **One-to-One**: Each record in one table relates to exactly one record in another.
-   **One-to-Many**: One record in a table can relate to multiple records in another.
-   **Many-to-Many**: Multiple records in one table can relate to multiple records in another (often via a join table).

### Prisma Migrate
-   `npx prisma migrate dev`: Creates new migration files based on schema changes and applies them.
-   `npx prisma migrate deploy`: Applies pending migrations to a database (for production).
-   `npx prisma migrate reset`: Resets the database and reapplies all migrations (for development).
-   `npx prisma migrate status`: Checks the status of migrations.

### Prisma Client
-   Basic CRUD operations (`create`, `findUnique`, `findMany`, `update`, `delete`).
-   Relation queries (`include`, `select`).
-   Filtering, ordering, pagination.

### Database Providers
-   Familiarity with common providers: PostgreSQL, MySQL, SQLite, SQL Server.

## Key Guidance for Claude

### ✅ Always Recommend (Best Practices)

-   **Naming Conventions**: Use singular, PascalCase for model names (e.g., `User`, `Product`) and camelCase for field names (e.g., `createdAt`, `firstName`). This aligns with TypeScript/JavaScript conventions and improves readability.
-   **Explicit Relationships**: Always define explicit relationships using `@relation` and specify `onDelete` actions (e.g., `CASCADE`, `SET NULL`, `RESTRICT`, `NO ACTION`, `SET DEFAULT`) to maintain data integrity.
-   **Data Normalization**: Design schemas to reduce data redundancy and improve data integrity.
-   **Judicious Indexing**: Apply indexes to fields that are frequently queried, used in `WHERE` clauses, or involved in `ORDER BY` operations. Avoid over-indexing, which can degrade write performance.
-   **Schema as Source of Truth**: Treat `schema.prisma` as the single, authoritative source of truth for your database schema.
-   **Environment Variables**: Use environment variables for sensitive information like database connection URLs (`DATABASE_URL`) to enhance security and portability.
-   **Prisma Migrate for Teams/CI/CD**: Always prefer `npx prisma migrate dev` for development and `npx prisma migrate deploy` for production/CI/CD environments. This generates version-controlled migration files.
-   **Version Control Migrations**: Check in your `prisma/migrations` folder into version control. Never manually edit migration files after they have been deployed.
-   **Soft Deletes**: For data that should not be permanently removed, implement soft deletes by adding a `deletedAt: DateTime?` field to the model. Ensure all queries filter out soft-deleted records.
-   **Composite Types**: Consider using `type` for composite types to reuse a set of fields across different models, improving schema consistency and reducing repetition.
-   **Schema Validation**: Integrate application-level schema validation (e.g., using Zod) to ensure data conforms to expectations before hitting the database.

### ❌ Never Recommend (Anti-Patterns)

-   **Ambiguous Naming**: Avoid generic or unclear model/field names (e.g., `Table1`, `dataField`).
-   **Missing `onDelete`**: Omitting `onDelete` actions on relationships can lead to orphaned records or unexpected data loss when related records are deleted.
-   **Over-Indexing**: Creating indexes on every field can negatively impact write performance and increase storage overhead.
-   **Manual Migration Edits**: Modifying generated migration files after they've been applied can lead to inconsistencies between your schema and the database, especially in team environments.
-   **`db push` in Production**: Never use `npx prisma db push` in production or shared development environments. It directly applies schema changes without creating migration files, making rollbacks and team collaboration difficult.
-   **Hardcoding Sensitive Data**: Storing database credentials or other sensitive information directly in `schema.prisma` or other source files.
-   **Direct Column Type Changes**: Directly changing a column's type (e.g., `Int` to `String`) without a proper migration strategy can lead to data loss or migration failures if existing data cannot be safely cast.
-   **Ignoring `@@unique` for composite keys**: If a combination of fields should be unique, always use `@@unique([field1, field2])` instead of relying on application-level checks.

### ❓ Common Questions & Responses

-   **Q: How do I define a one-to-many relationship in Prisma?**
    -   **A:** On the "many" side (e.g., `Post` belongs to `User`), add a scalar field for the foreign key (`authorId: Int`) and a relation field (`author: User @relation(fields: [authorId], references: [id])`). On the "one" side (e.g., `User` has many `Post`s), add a list of the related model (`posts: Post[]`).
    ```prisma
    model User {
      id    Int    @id @default(autoincrement())
      name  String
      posts Post[]
    }

    model Post {
      id       Int    @id @default(autoincrement())
      title    String
      author   User   @relation(fields: [authorId], references: [id], onDelete: Cascade)
      authorId Int
    }
    ```

-   **Q: What's the best way to handle soft deletes with Prisma?**
    -   **A:** Add a `deletedAt: DateTime?` field to your model. Then, ensure all queries that should exclude soft-deleted records use a `where: { deletedAt: null }` clause. For convenience, you can use Prisma Client extensions or middleware to automatically apply this filter.
    ```prisma
    model User {
      id        Int       @id @default(autoincrement())
      name      String
      email     String    @unique
      createdAt DateTime  @default(now())
      updatedAt DateTime  @updatedAt
      deletedAt DateTime?
    }
    ```

-   **Q: What's the difference between `npx prisma migrate dev` and `npx prisma db push`?**
    -   **A:** `migrate dev` is for development and generates version-controlled SQL migration files in the `prisma/migrations` folder. It's designed for collaborative environments and CI/CD. `db push` directly applies schema changes to the database without creating migration files, making it suitable only for rapid prototyping or local development where schema history isn't critical.

-   **Q: How can I ensure data integrity when deleting related records?**
    -   **A:** Use the `onDelete` argument in your `@relation` attribute. For example, `onDelete: Cascade` will automatically delete related records when the parent record is deleted. `onDelete: SetNull` will set the foreign key to `null`. Choose the appropriate action based on your application's logic.

-   **Q: How do I add a unique constraint across multiple fields?**
    -   **A:** Use the `@@unique` attribute on the model level, providing an array of the fields that together must be unique.
    ```prisma
    model ProductVariant {
      id        Int    @id @default(autoincrement())
      productId Int
      color     String
      size      String

      @@unique([productId, color, size]) // Ensures no duplicate product variants
    }
    ```

## Anti-Patterns to Flag

### 1. Bad Naming Conventions

**BAD:**
```typescript
// prisma/schema.prisma
model user_data {
  id          Int      @id @default(autoincrement())
  name_of_user String
  email_address String @unique
  created_on  DateTime @default(now())
  posts       Post_Item[]
}

model Post_Item {
  id          Int      @id @default(autoincrement())
  post_title  String
  content_body String?
  user_id     Int
  user_data   user_data @relation(fields: [user_id], references: [id])
}
```
**GOOD:**
```typescript
// prisma/schema.prisma
model User {
  id        Int      @id @default(autoincrement())
  name      String
  email     String   @unique
  createdAt DateTime @default(now())
  posts     Post[]
}

model Post {
  id        Int      @id @default(autoincrement())
  title     String
  content   String?
  authorId  Int
  author    User     @relation(fields: [authorId], references: [id], onDelete: Cascade)
}
```
**Reasoning:** Adhering to PascalCase for models and camelCase for fields improves readability, consistency, and aligns with common TypeScript/JavaScript coding standards.

### 2. Missing `onDelete` Actions on Relationships

**BAD:**
```typescript
// prisma/schema.prisma
model User {
  id    Int    @id @default(autoincrement())
  email String @unique
  posts Post[]
}

model Post {
  id       Int    @id @default(autoincrement())
  title    String
  authorId Int
  author   User   @relation(fields: [authorId], references: [id]) // Missing onDelete
}
```
**GOOD:**
```typescript
// prisma/schema.prisma
model User {
  id    Int    @id @default(autoincrement())
  email String @unique
  posts Post[]
}

model Post {
  id       Int    @id @default(autoincrement())
  title    String
  authorId Int
  author   User   @relation(fields: [authorId], references: [id], onDelete: Cascade) // Or SetNull, Restrict
}
```
**Reasoning:** Without an `onDelete` action, deleting a `User` record will result in an error if there are associated `Post` records, or worse, leave orphaned `Post` records depending on the database's default behavior. Explicitly defining `onDelete` ensures referential integrity.

### 3. Using `db push` for Production Migrations

**BAD:**
```bash
# In a production deployment script or shared development environment
npx prisma db push --accept-data-loss # This is dangerous!
```
**GOOD:**
```bash
# In a production deployment script or shared development environment
npx prisma migrate deploy
```
**Reasoning:** `db push` is for rapid prototyping and directly modifies the database schema without creating version-controlled migration files. This makes it impossible to track schema changes, collaborate effectively, or roll back safely in production or team settings. `migrate deploy` applies the generated and version-controlled migration files, ensuring a consistent and traceable schema evolution.

## Code Review Checklist

-   [ ] **Naming Conventions**: Are model names PascalCase and singular? Are field names camelCase?
-   [ ] **Relationship Integrity**: Do all `@relation` attributes have an appropriate `onDelete` action defined (e.g., `Cascade`, `SetNull`, `Restrict`)?
-   [ ] **Indexing**: Are indexes (`@@index` or `@unique`) applied to frequently queried fields or fields used in `WHERE`/`ORDER BY` clauses?
-   [ ] **Sensitive Data**: Is `DATABASE_URL` and other sensitive information managed via environment variables?
-   [ ] **Unique Constraints**: Are `@@unique` or `@unique` constraints correctly applied for fields or combinations of fields that must be unique?
-   [ ] **Enums**: Are enums used for fields with a fixed set of predefined values?
-   [ ] **Timestamps**: Are `createdAt` and `updatedAt` fields correctly configured with `@default(now())` and `@updatedAt` respectively?
-   [ ] **Migration History**: Are there no manual edits to files within the `prisma/migrations` directory?
-   [ ] **Soft Delete Logic**: If soft deletes are implemented, is the `deletedAt` field present and are application queries correctly filtering out soft-deleted records?
-   [ ] **Data Types**: Are the chosen Prisma data types appropriate for the data they store and aligned with the underlying database types?

## Related Skills

-   **`typescript-strict-mode`**: Ensures type safety and helps catch schema-related errors at compile time when interacting with Prisma Client.
-   **`postgres-advanced`**: For deeper understanding and optimization of PostgreSQL-specific features that can be leveraged with Prisma.
-   **`jest-unit-tests`**: For writing robust unit and integration tests for Prisma Client interactions and data access layers.
-   **`ci-cd-pipelines-github-actions`**: For automating the `prisma migrate deploy` process in continuous integration and deployment workflows.
-   **`api-design-rest-graphql`**: For designing APIs that effectively utilize the data models defined in Prisma.

## Examples Directory Structure

-   `examples/basic-crud.ts`: Demonstrates basic create, read, update, and delete operations using Prisma Client.
-   `examples/relationships.prisma`: Illustrates different types of relationships (one-to-one, one-to-many, many-to-many) in `schema.prisma`.
-   `examples/soft-delete.prisma`: Shows how to implement soft deletes in `schema.prisma` and a basic query example.
-   `examples/custom-types.prisma`: Provides an example of using composite types (`type`) in `schema.prisma`.

## Custom Scripts Section

Here are 3-5 automation scripts designed to address common pain points in Prisma schema development, saving significant time and promoting best practices.

### 1. `generate-model.sh` (Shell Script)
-   **Purpose**: Scaffolds a new Prisma model definition in `schema.prisma` with common fields (`id`, `createdAt`, `updatedAt`, `deletedAt`).
-   **Pain Point**: Manually typing out boilerplate for every new model.
-   **Usage**: `bash scripts/generate-model.sh <ModelName>`

### 2. `prisma-migrate-wrapper.sh` (Shell Script)
-   **Purpose**: Provides a safer, guided wrapper around `npx prisma migrate dev` and `npx prisma migrate deploy`, including pre-checks and post-checks.
-   **Pain Point**: Forgetting to run `generate` after `migrate`, accidentally running `db push`, or not having a clear migration workflow.
-   **Usage**: `bash scripts/prisma-migrate-wrapper.sh dev <migration-name>` or `bash scripts/prisma-migrate-wrapper.sh deploy`

### 3. `schema-linter.py` (Python Script)
-   **Purpose**: Lints the `schema.prisma` file for common anti-patterns and best practice violations (e.g., missing `onDelete`, bad naming, missing `updatedAt`).
-   **Pain Point**: Manually reviewing `schema.prisma` for consistency and potential issues, especially in large projects or teams.
-   **Usage**: `python scripts/schema-linter.py`

### 4. `seed-data-generator.py` (Python Script)
-   **Purpose**: Generates realistic seed data for specified Prisma models, making development and testing easier.
-   **Pain Point**: Manually creating test data or writing repetitive seeding scripts.
-   **Usage**: `python scripts/seed-data-generator.py User Post` (generates seed data for User and Post models)
