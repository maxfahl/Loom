# Custom Scripts for PostgreSQL Advanced Skill

This directory contains a collection of automation scripts designed to streamline common, repetitive, and often complex tasks associated with advanced PostgreSQL usage. Each script aims to save significant developer time by automating setup, analysis, or maintenance.

## Scripts Overview

### 1. `pg_config_optimizer.py`

*   **Description**: Analyzes the system's hardware resources (RAM, CPU) and the current PostgreSQL configuration (`postgresql.conf`) to suggest optimized parameters. It can also apply these changes or generate a diff.
*   **Usage Examples**:
    ```bash
    # Dry run with default RAM detection
    python pg_config_optimizer.py /path/to/your/postgresql.conf --dry-run

    # Apply changes to a new output file, specifying RAM
    python pg_config_optimizer.py /path/to/your/postgresql.conf --ram 16 --output /tmp/optimized_postgresql.conf

    # Apply changes directly to the original file (creates a .bak backup)
    python pg_config_optimizer.py /path/to/your/postgresql.conf --ram 32
    ```

### 2. `pg_index_analyzer.py`

*   **Description**: Connects to a PostgreSQL database, analyzes query patterns from `pg_stat_statements` and existing index usage, and recommends new indexes or identifies underutilized/redundant ones.
*   **Prerequisites**: `psycopg2-binary` (install via `pip install psycopg2-binary`). The `pg_stat_statements` extension must be enabled in your PostgreSQL database.
*   **Usage Examples**:
    ```bash
    # Analyze indexes in dry-run mode
    python pg_index_analyzer.py --dbname mydatabase --user myuser --password mypassword --host localhost --port 5432 --dry-run

    # Analyze indexes, using PGPASSWORD environment variable
    PGPASSWORD=mypassword python pg_index_analyzer.py --dbname mydatabase --user myuser

    # Analyze indexes on a remote host
    python pg_index_analyzer.py --dbname mydatabase --user myuser --password mypassword --host my.remote.host --port 5432
    ```

### 3. `pg_partition_generator.py`

*   **Description**: Generates SQL DDL statements for declarative partitioning (RANGE, LIST, HASH) based on user-defined table structure, partition key, and strategy.
*   **Usage Examples**:
    ```bash
    # Generate SQL for RANGE partitioning by date
    python pg_partition_generator.py my_events event_date --type range \
      --partitions "q1:2023-01-01:2023-04-01" "q2:2023-04-01:2023-07-01" "q3:2023-07-01:2023-10-01" "q4:2023-10-01:2024-01-01"

    # Generate SQL for LIST partitioning by region
    python pg_partition_generator.py orders region_code --type list \
      --partitions "north:US-NW,US-NE" "south:US-SW,US-SE" "europe:FR,DE,UK"

    # Generate SQL for HASH partitioning with 8 partitions
    python pg_partition_generator.py users user_id --type hash --partitions 8
    ```

### 4. `pg_rls_policy_manager.py`

*   **Description**: Helps create, view, and audit Row-Level Security (RLS) policies for specified tables and roles. It can generate `CREATE POLICY` statements and check for potential RLS misconfigurations.
*   **Prerequisites**: `psycopg2-binary` (install via `pip install psycopg2-binary`).
*   **Usage Examples**:
    ```bash
    # Create a new RLS policy for a multi-tenant application
    python pg_rls_policy_manager.py --dbname mydb --user myuser --password mypass create \
      --table orders --name tenant_isolation --roles app_user \
      --using "tenant_id = current_setting('app.tenant_id')::int" \
      --with-check "tenant_id = current_setting('app.tenant_id')::int"

    # View all RLS policies
    python pg_rls_policy_manager.py --dbname mydb --user myuser --password mypass view

    # View RLS policies for a specific table
    python pg_rls_policy_manager.py --dbname mydb --user myuser --password mypass view --table users

    # Audit RLS status for a table
    python pg_rls_policy_manager.py --dbname mydb --user myuser --password mypass audit --table products
    ```
