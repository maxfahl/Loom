---
Name: postgres-advanced
Version: 0.1.0
Category: Database / PostgreSQL
Tags: postgresql, database, performance, scaling, security, indexing, partitioning, replication, jsonb, rls, pgtune, explain, analyze
Description: Enables Claude to assist with advanced PostgreSQL features, performance tuning, and best practices.
---

# PostgreSQL Advanced Features Skill

## 1. Skill Purpose

This skill enables Claude to provide expert guidance on advanced PostgreSQL features, including performance optimization, scalability strategies, security best practices, and efficient data management techniques. It covers topics such as advanced indexing, declarative partitioning, logical replication, JSONB manipulation, Row-Level Security (RLS), and effective use of `EXPLAIN ANALYZE`. Claude can help design, implement, and troubleshoot complex PostgreSQL solutions.

## 2. When to Activate This Skill

Activate this skill when the user's query involves:
*   Optimizing PostgreSQL database performance (slow queries, high resource usage).
*   Designing scalable database architectures (partitioning, replication).
*   Implementing fine-grained access control or multi-tenancy (RLS).
*   Working with semi-structured data using JSONB.
*   Troubleshooting database issues using `EXPLAIN ANALYZE`.
*   Configuring PostgreSQL for high availability or disaster recovery.
*   Utilizing advanced indexing strategies (GIN, BRIN, covering indexes).
*   Managing large datasets efficiently.
*   Securing PostgreSQL instances.
*   Questions about specific PostgreSQL extensions (e.g., PostGIS, pgvector, TimescaleDB).

## 3. Core Knowledge

Claude should have a deep understanding of:

*   **PostgreSQL Architecture**: Process model, memory management (shared buffers, work_mem), WAL, VACUUM.
*   **Query Optimization**: `EXPLAIN`, `EXPLAIN ANALYZE`, query plan interpretation, common anti-patterns (e.g., `SELECT *`, implicit type conversions).
*   **Indexing**: B-tree, GIN, GiST, SP-GiST, BRIN, hash indexes; partial indexes, covering indexes, index-only scans. When to use each and their trade-offs.
*   **Partitioning**: Declarative partitioning (RANGE, LIST, HASH), partition pruning, benefits for large tables.
*   **Replication**: Physical (streaming) and Logical replication; synchronous vs. asynchronous; high availability (HA) setups (e.g., Patroni, repmgr).
*   **JSONB**: Operators (`->`, `->>`, `#>`, `#>>`, `?`, `?|`, `?&`), indexing JSONB data (GIN indexes), best practices for storing and querying JSON.
*   **Row-Level Security (RLS)**: `CREATE POLICY`, `ALTER TABLE ... ENABLE ROW LEVEL SECURITY`, `USING` and `WITH CHECK` clauses, multi-tenancy patterns.
*   **Performance Tuning**: `postgresql.conf` parameters (`shared_buffers`, `work_mem`, `maintenance_work_mem`, `effective_cache_size`, `wal_buffers`, `checkpoint_timeout`, `max_wal_size`, `autovacuum` settings), connection pooling.
*   **Security**: Authentication methods (SCRAM-SHA-256), roles and privileges, SSL/TLS, `pg_hba.conf`, `pg_audit`, SQL injection prevention.
*   **Extensions**: Awareness of popular extensions like PostGIS, pgvector, TimescaleDB, pgcrypto, pg_stat_statements, and their use cases.
*   **Transactions & Concurrency**: ACID properties, isolation levels, locking mechanisms.

## 4. Key Guidance for Claude

### ✅ Always Recommend

*   **Use `EXPLAIN ANALYZE`**: Always analyze slow queries with `EXPLAIN ANALYZE` to understand their execution plan, identify bottlenecks, and gather runtime statistics.
*   **Strategic Indexing**: Recommend indexes based on query patterns, focusing on frequently filtered, joined, or ordered columns. Advise on partial and covering indexes where appropriate.
*   **Declarative Partitioning for Large Tables**: For tables exceeding tens of millions of rows, recommend declarative partitioning to improve query performance, maintenance, and data lifecycle management.
*   **Implement RLS for Multi-tenancy/Fine-grained Access**: When dealing with sensitive data or multi-tenant applications, advocate for RLS to enforce access policies directly at the database level.
*   **Leverage JSONB for Semi-structured Data**: Advise using JSONB for flexible schema requirements, ensuring proper GIN indexing for query efficiency.
*   **Automated Backups and Recovery Testing**: Emphasize the importance of regular, automated backups and, crucially, periodic testing of recovery procedures.
*   **Connection Pooling**: Recommend using a connection pooler (e.g., PgBouncer) for applications with many short-lived connections to reduce overhead.
*   **Principle of Least Privilege**: Grant only the necessary permissions to users and roles.
*   **Monitor `pg_stat_statements`**: Regularly review `pg_stat_statements` to identify top-consuming queries and performance regressions.
*   **Keep PostgreSQL Updated**: Advise users to stay on supported PostgreSQL versions and apply security patches promptly.

### ❌ Never Recommend

*   **`SELECT *` in Production Queries**: Avoid `SELECT *` as it fetches unnecessary data, increases network traffic, and can prevent index-only scans.
*   **Over-indexing**: Do not create excessive indexes, as they incur overhead on writes (INSERT, UPDATE, DELETE) and consume disk space.
*   **Manual `VACUUM` without understanding**: Discourage manual `VACUUM` or `VACUUM FULL` without a clear understanding of its implications and the `autovacuum` process.
*   **Storing Passwords in Plain Text**: Always use strong hashing algorithms (e.g., bcrypt) for passwords, never store them directly.
*   **Disabling `autovacuum`**: `autovacuum` is crucial for maintaining database health and preventing transaction ID wraparound.
*   **Ignoring `pg_hba.conf` security**: Never leave `pg_hba.conf` open to wide access (e.g., `host all all 0.0.0.0/0 trust`).
*   **Using `OFFSET` for deep pagination**: For very deep pagination, `OFFSET` becomes inefficient. Recommend cursor-based pagination instead.

### ❓ Common Questions & Responses

*   **Q: My queries are slow, what should I do?**
    *   **A:** Start by running `EXPLAIN ANALYZE` on your slowest queries. This will show you the execution plan and where time is being spent. Check for missing indexes, sequential scans on large tables, or inefficient joins.
*   **Q: How can I handle a very large table (e.g., billions of rows)?**
    *   **A:** Consider implementing declarative partitioning. This breaks the large table into smaller, more manageable pieces, improving query performance and maintenance operations.
*   **Q: How do I secure my PostgreSQL database?**
    *   **A:** Implement strong authentication (SCRAM-SHA-256), configure `pg_hba.conf` to restrict access, use SSL/TLS for all connections, apply the principle of least privilege for roles, and consider Row-Level Security for sensitive data.
*   **Q: When should I use JSONB instead of a normalized table?**
    *   **A:** Use JSONB when you have semi-structured data, a rapidly evolving schema, or need to store document-like data. For structured, relational data, stick to normalized tables. Remember to index JSONB fields you query frequently.
*   **Q: What's the difference between physical and logical replication?**
    *   **A:** Physical replication (e.g., streaming replication) copies the entire data directory at the block level, ideal for high availability and disaster recovery. Logical replication allows more granular control, replicating specific tables or databases, and can be used for selective data distribution or upgrades.

## 5. Anti-Patterns to Flag

### Anti-Pattern 1: `SELECT *` in application code

```typescript
// BAD: Fetches all columns, even if not needed
const getUser = async (id: number) => {
  const result = await pool.query('SELECT * FROM users WHERE id = $1', [id]);
  return result.rows[0];
};

// GOOD: Selects only necessary columns
const getUserOptimized = async (id: number) => {
  const result = await pool.query('SELECT id, name, email FROM users WHERE id = $1', [id]);
  return result.rows[0];
};
```

### Anti-Pattern 2: Missing Index on frequently queried columns

```sql
-- BAD: Query will likely perform a sequential scan on a large table
SELECT * FROM orders WHERE customer_id = 123 AND order_date > '2025-01-01';

-- GOOD: Add a composite index for efficient lookup
CREATE INDEX idx_orders_customer_date ON orders (customer_id, order_date);
SELECT * FROM orders WHERE customer_id = 123 AND order_date > '2025-01-01';
```

### Anti-Pattern 3: Inefficient JSONB querying without GIN index

```sql
-- BAD: Querying JSONB without a proper index can be slow on large datasets
SELECT * FROM products WHERE data->>'category' = 'electronics';

-- GOOD: Create a GIN index on the JSONB path for faster lookups
CREATE INDEX idx_products_category ON products USING GIN ((data->>'category'));
SELECT * FROM products WHERE data->>'category' = 'electronics';
```

### Anti-Pattern 4: Deep pagination with `OFFSET`

```sql
-- BAD: 'OFFSET' becomes very slow for large offsets as it still scans preceding rows
SELECT * FROM articles ORDER BY created_at DESC OFFSET 100000 LIMIT 10;

-- GOOD: Use cursor-based pagination (e.g., WHERE clause with last seen value)
-- Assuming 'last_created_at' and 'last_id' are from the previous page's last item
SELECT * FROM articles
WHERE (created_at < $1) OR (created_at = $1 AND id < $2)
ORDER BY created_at DESC
LIMIT 10;
```

## 6. Code Review Checklist

*   [ ] Are all `SELECT` statements explicit about the columns they retrieve?
*   [ ] Are appropriate indexes in place for `WHERE`, `JOIN`, `ORDER BY`, and `GROUP BY` clauses? (Verify with `EXPLAIN ANALYZE`)
*   [ ] Is declarative partitioning used for tables exceeding tens of millions of rows?
*   [ ] Are JSONB fields that are frequently queried indexed with GIN?
*   [ ] Is Row-Level Security (RLS) implemented for sensitive data or multi-tenant scenarios?
*   [ ] Are transactions used correctly, and are isolation levels appropriate for the use case?
*   [ ] Is input sanitized and parameterized queries used to prevent SQL injection?
*   [ ] Are database connection parameters (e.g., `statement_timeout`) configured to prevent long-running queries?
*   [ ] Is a connection pooler being utilized if the application has many connections?
*   [ ] Are there any `VACUUM FULL` commands in application code or frequent manual `VACUUM` calls? (Should generally be avoided)

## 7. Related Skills

*   `database-migration-management`: For managing schema changes and versioning.
*   `rest-api-design`: For designing efficient APIs that interact with PostgreSQL.
*   `secrets-management`: For securely handling database credentials.
*   `containerization-docker-compose`: For deploying PostgreSQL in Docker environments.
*   `observability-stack-implementation`: For monitoring PostgreSQL performance and health.

## 8. Examples Directory Structure

```
examples/
├── partitioning/
│   ├── range_partitioning.sql
│   └── list_partitioning.sql
├── rls/
│   ├── multi_tenant_policy.sql
│   └── user_specific_data_policy.sql
├── jsonb/
│   ├── jsonb_indexing.sql
│   └── jsonb_querying.sql
├── indexing/
│   ├── partial_index.sql
│   └── covering_index.sql
└── performance/
    └── explain_analyze_example.sql
```

## 9. Custom Scripts Section

This section outlines automation scripts designed to streamline common, repetitive, and often complex tasks associated with advanced PostgreSQL usage. Each script aims to save significant developer time by automating setup, analysis, or maintenance.

### Script 1: `pg_config_optimizer.py` (Python)

*   **Description**: Analyzes the system's hardware resources (RAM, CPU) and the current PostgreSQL configuration to suggest optimized `postgresql.conf` parameters. It can also apply these changes or generate a diff.
*   **Pain Point**: Manually tuning `postgresql.conf` is complex, requires deep knowledge, and is prone to errors. This script automates the process based on best practices.

### Script 2: `pg_index_analyzer.py` (Python)

*   **Description**: Connects to a PostgreSQL database, analyzes query patterns from `pg_stat_statements` and existing index usage, and recommends new indexes or identifies underutilized/redundant ones.
*   **Pain Point**: Identifying optimal indexing strategies is crucial for performance but often requires manual analysis of query logs and index statistics.

### Script 3: `pg_partition_generator.py` (Python)

*   **Description**: Generates SQL DDL statements for declarative partitioning (RANGE, LIST, HASH) based on user-defined table structure, partition key, and strategy.
*   **Pain Point**: Setting up declarative partitioning involves writing repetitive DDL for parent tables, child tables, and potentially default partitions, which can be error-prone.

### Script 4: `pg_rls_policy_manager.py` (Python)

*   **Description**: Helps create, view, and audit Row-Level Security (RLS) policies for specified tables and roles. It can generate `CREATE POLICY` statements and check for potential RLS misconfigurations.
*   **Pain Point**: Managing RLS policies can be complex, especially in multi-tenant environments, requiring careful definition and auditing to prevent data leaks.
