---
name: database-performance-tuning
version: 0.1.0
category: Database / Performance
tags: database, performance, tuning, optimization, sql, indexing, query, schema, maintenance
description: Optimizing database operations for improved speed, efficiency, and scalability.
---

# Database Performance Tuning

## 1. Skill Purpose

This skill enables Claude to identify, analyze, and resolve performance bottlenecks in database systems. It covers strategies for optimizing SQL queries, designing efficient database schemas, implementing effective indexing, and performing regular maintenance to ensure optimal database health and responsiveness. The goal is to improve application speed, reduce resource consumption, and enhance overall system scalability.

## 2. When to Activate This Skill

Activate this skill when:
- A user reports slow application response times related to data retrieval or storage.
- Database queries are executing slowly or timing out.
- Database server CPU, memory, or I/O utilization is consistently high.
- New features or data models are being designed, requiring performance considerations.
- Performing routine database maintenance or health checks.
- Migrating data or upgrading database systems.
- Identifying and resolving N+1 query problems.

Keywords/Patterns: "database slow", "optimize query", "performance bottleneck", "indexing strategy", "schema design", "database tuning", "slow SQL", "high database load", "N+1 query", "database optimization".

## 3. Core Knowledge

The fundamental concepts, patterns, and APIs Claude needs to know for database performance tuning include:

### 3.1. Indexing Strategies
- **Types of Indexes**: B-tree, Hash, Bitmap, Full-text, Clustered vs. Non-clustered.
- **When to Index**: Columns in `WHERE`, `JOIN`, `ORDER BY`, `GROUP BY` clauses. Foreign keys.
- **When NOT to Index**: Low cardinality columns, frequently updated columns (consider trade-offs).
- **Composite Indexes**: Order of columns in composite indexes.
- **Covering Indexes**: Indexes that include all columns needed for a query, avoiding table lookups.
- **Index Maintenance**: Rebuilding, reorganizing, monitoring usage.

### 3.2. SQL Query Optimization
- **`EXPLAIN` / Query Plan Analysis**: Understanding how the database executes a query.
- **Avoiding `SELECT *`**: Always specify columns.
- **Optimizing `WHERE` Clauses**: Avoid functions on indexed columns, use appropriate operators.
- **Efficient `JOIN`s**: Choosing correct `JOIN` types, join order, indexing join columns.
- **Subquery Optimization**: `EXISTS` vs. `IN`, `JOIN` vs. subquery.
- **Limiting Results**: `LIMIT`, `OFFSET`, `TOP`.
- **Minimizing `DISTINCT` and `ORDER BY`**: Use only when necessary.
- **Common Table Expressions (CTEs)**: Simplifying complex queries.
- **Avoiding N+1 Queries**: Eager loading, batching.
- **Batch Operations**: `INSERT ... VALUES (...), (...)`, `UPDATE ... WHERE IN (...)`.

### 3.3. Database Design and Configuration
- **Schema Design**:
    - **Normalization**: Reducing data redundancy (1NF, 2NF, 3NF, BCNF).
    - **Denormalization**: Introducing controlled redundancy for read performance.
    - **Data Types**: Using the most efficient data types (e.g., `INT` vs. `BIGINT`, `VARCHAR(50)` vs. `TEXT`).
- **Caching**: Database-level caching (buffer pool), application-level caching.
- **Hardware Resources**: CPU, RAM, Disk I/O (SSD vs. HDD), Network.
- **Database Configuration Parameters**: Memory allocation, connection limits, buffer sizes, transaction isolation levels.

### 3.4. Regular Maintenance
- **Monitoring**: Key metrics (latency, throughput, connections, locks, deadlocks, resource utilization).
- **Statistics Updates**: Ensuring the query optimizer has up-to-date information.
- **Archiving/Purging Data**: Managing data lifecycle.
- **Vacuuming/Analyze (PostgreSQL)**, **DBCC UPDATESTATISTICS (SQL Server)**.

### 3.5. Advanced Techniques
- **Partitioning**: Horizontal partitioning (range, list, hash), vertical partitioning.
- **Sharding**: Distributing data across multiple database instances.
- **Replication**: Read replicas for scaling read operations.
- **Connection Pooling**: Managing database connections efficiently.

## 4. Key Guidance for Claude

### Always Recommend (✅ Best Practices)
- ✅ **Analyze Query Plans**: Always start by examining the `EXPLAIN` output or query plan for problematic queries to understand their execution path and identify bottlenecks.
- ✅ **Index Strategically**: Create indexes on columns frequently used in `WHERE`, `JOIN`, `ORDER BY`, and `GROUP BY` clauses. Prioritize high-cardinality columns.
- ✅ **Specify Columns in `SELECT`**: Always list specific columns instead of `SELECT *` to reduce data transfer and memory usage.
- ✅ **Use Appropriate Data Types**: Choose the most precise and smallest data types that fit the data to minimize storage and improve processing speed.
- ✅ **Monitor Continuously**: Implement robust monitoring for key database metrics (CPU, memory, I/O, query latency, active connections, locks) to detect issues early.
- ✅ **Update Statistics Regularly**: Ensure database statistics are up-to-date for the query optimizer to make informed decisions.
- ✅ **Test Changes**: Always test performance changes in a staging environment before deploying to production.
- ✅ **Consider Application-Level Caching**: For frequently accessed, slowly changing data, implement caching at the application layer.

### Never Recommend (❌ Anti-Patterns)
- ❌ **Blindly Add Indexes**: Avoid adding indexes without understanding their impact on write performance and storage. Over-indexing can be detrimental.
- ❌ **Using `SELECT *` in Production**: Never use `SELECT *` in production code, especially for large tables or frequently executed queries.
- ❌ **Functions on Indexed Columns in `WHERE`**: Avoid applying functions (e.g., `YEAR(date_column)`) to indexed columns in `WHERE` clauses, as this often prevents index usage.
- ❌ **Ignoring N+1 Query Problems**: Do not allow N+1 queries to persist; they are a major source of performance degradation.
- ❌ **Hardcoding Configuration Values**: Avoid hardcoding database configuration parameters; use environment variables or configuration management.
- ❌ **Running Heavy Queries During Peak Hours**: Do not schedule large data imports, complex reports, or index rebuilds during peak application usage times.

### Common Questions & Responses (FAQ Format)

**Q: My query is slow, where should I start?**
A: Start by running `EXPLAIN` (or your database's equivalent) on the query. This will show you the execution plan and highlight where the time is being spent (e.g., full table scans, inefficient joins).

**Q: How do I know if I need an index?**
A: If a query frequently filters, sorts, or joins on a particular column, and that column has high cardinality (many unique values), an index is likely beneficial. Check the query plan to see if a full table scan is occurring.

**Q: What's the difference between normalization and denormalization?**
A: **Normalization** aims to reduce data redundancy and improve data integrity by organizing tables and columns. **Denormalization** intentionally introduces redundancy to improve read performance, often by pre-joining data or storing derived values, at the cost of increased storage and potential update anomalies.

**Q: How can I prevent N+1 queries in my ORM?**
A: Use your ORM's eager loading features (e.g., `include`, `join fetch`, `select_related`, `prefetch_related`) to load related data in a single query instead of making N additional queries.

**Q: My database server is running out of memory. What should I check?**
A: Investigate the database's memory configuration (e.g., buffer pool size, sort buffer size), active connections, and currently running queries. Large, unoptimized queries or too many concurrent connections can consume excessive memory.

## 5. Anti-Patterns to Flag

### Anti-Pattern: `SELECT *`
**BAD:**
```typescript
// Inefficient: Fetches all columns, even if only 'name' and 'email' are needed.
const users = await db.query("SELECT * FROM users WHERE status = 'active'");
```

**GOOD:**
```typescript
// Efficient: Fetches only necessary columns.
const users = await db.query("SELECT id, name, email FROM users WHERE status = 'active'");
```

### Anti-Pattern: Function on Indexed Column in `WHERE` Clause
**BAD:**
```typescript
// Prevents index usage on 'created_at' column.
const orders = await db.query("SELECT * FROM orders WHERE DATE(created_at) = '2023-10-26'");
```

**GOOD:**
```typescript
// Allows index usage on 'created_at' column.
const orders = await db.query("SELECT * FROM orders WHERE created_at >= '2023-10-26 00:00:00' AND created_at < '2023-10-27 00:00:00'");
```

### Anti-Pattern: N+1 Query Problem (Example with a hypothetical ORM)
**BAD:**
```typescript
// Fetches all posts, then makes N additional queries to fetch each post's author.
const posts = await Post.findAll();
for (const post of posts) {
  const author = await post.getAuthor(); // N+1 query
  console.log(`${post.title} by ${author.name}`);
}
```

**GOOD:**
```typescript
// Eager loading: Fetches posts and their authors in a single (or fewer) optimized queries.
const postsWithAuthors = await Post.findAll({ include: [Author] });
for (const post of postsWithAuthors) {
  console.log(`${post.title} by ${post.Author.name}`);
}
```

## 6. Code Review Checklist

- [ ] Are `SELECT *` statements avoided in performance-critical queries?
- [ ] Are appropriate indexes present on columns used in `WHERE`, `JOIN`, `ORDER BY`, and `GROUP BY` clauses?
- [ ] Are functions or calculations avoided on indexed columns within `WHERE` clauses?
- [ ] Is eager loading or batching used to prevent N+1 query problems?
- [ ] Are data types chosen optimally for storage and performance?
- [ ] Are `LIMIT` and `OFFSET` (or equivalent) used for pagination?
- [ ] Is there a plan for regular database maintenance (statistics, archiving)?
- [ ] Are transaction isolation levels set appropriately for the application's needs?
- [ ] Is connection pooling configured and utilized?
- [ ] For complex queries, has the query plan been analyzed and optimized?

## 7. Related Skills

- `sql-nosql-database-management`: For general database administration and operations.
- `prisma-schema`: For optimizing database interactions within Prisma ORM.
- `django-rest-framework`: For optimizing database access patterns in Django applications.
- `nodejs-express-nestjs-development`: For implementing application-level caching and connection pooling in Node.js.

## 8. Examples Directory Structure

- `examples/sql/slow_query.sql`: Example of a slow SQL query.
- `examples/sql/optimized_query.sql`: Example of an optimized SQL query.
- `examples/typescript/n_plus_1_problem.ts`: TypeScript example demonstrating the N+1 query problem.
- `examples/typescript/eager_loading_solution.ts`: TypeScript example demonstrating eager loading to solve N+1.
- `examples/config/db_config_tuning.json`: Example of database configuration parameters for tuning.

## 9. Custom Scripts Section

For database performance tuning, the following 3-5 automation scripts would save significant time:

1.  **`analyze-query-plan.sh`**: Automates running `EXPLAIN` (or equivalent) for a given SQL query and provides a formatted, human-readable output, highlighting potential issues.
2.  **`find-missing-indexes.py`**: Scans a database schema and common query patterns (from a log or configuration) to suggest potentially missing indexes.
3.  **`db-health-check.sh`**: Performs a series of checks on database metrics (connections, locks, buffer hit ratio, disk I/O) and provides a summary report.
4.  **`generate-schema-diff.py`**: Compares two database schemas (e.g., development vs. production) and generates a diff report, useful for identifying unintended schema changes that could impact performance.
5.  **`nplus1-detector.ts`**: (TypeScript) A utility to integrate into an application's test suite or development environment to detect and report N+1 query patterns.
