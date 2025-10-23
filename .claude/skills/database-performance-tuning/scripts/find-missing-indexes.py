#!/usr/bin/env python3

# find-missing-indexes.py
#
# Description:
#   Scans a PostgreSQL database schema and, based on a provided list of frequently queried columns,
#   suggests potentially missing indexes. This script is a conceptual outline; in a real-world
#   scenario, it would integrate with database drivers (e.g., psycopg2) and potentially parse
#   slow query logs for more accurate suggestions.
#
# Usage:
#   python3 find-missing-indexes.py --host localhost --port 5432 --user postgres --dbname mydb \
#     --columns users.email,orders.product_id,orders.created_at
#
# Requirements:
#   - Python 3
#   - (In a real scenario) A PostgreSQL database driver like `psycopg2` or `SQLAlchemy`.
#
# Features:
#   - Connects to a PostgreSQL database (placeholder).
#   - Fetches existing indexes and table/column information.
#   - Compares frequently queried columns against existing indexes.
#   - Suggests `CREATE INDEX` statements for missing indexes.
#   - Supports dry-run mode.
#
# Configuration:
#   Database connection details are passed via command-line arguments.
#   Frequently queried columns are passed as a comma-separated list.

import argparse
import sys

# Placeholder for database interaction. In a real application, you'd use a library like psycopg2.
class DatabaseConnector:
    def __init__(self, host, port, user, password, dbname):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.dbname = dbname
        self.conn = None

    def connect(self):
        print(f"\033[0;34mAttempting to connect to PostgreSQL database: {self.user}@{self.host}:{self.port}/{self.dbname}\033[0m")
        # In a real scenario:
        # import psycopg2
        # try:
        #     self.conn = psycopg2.connect(
        #         host=self.host, port=self.port, user=self.user,
        #         password=self.password, dbname=self.dbname
        #     )
        #     print("\033[0;32mSuccessfully connected to the database.\033[0m")
        # except Exception as e:
        #     print(f"\033[0;31mError connecting to database: {e}\033[0m")
        #     sys.exit(1)
        print("\033[0;33m(Database connection is simulated. Please integrate a real DB driver like psycopg2.)\033[0m")
        self.conn = True # Simulate connection

    def close(self):
        if self.conn:
            # In a real scenario: self.conn.close()
            print("\033[0;32mDatabase connection closed (simulated).\033[0m")

    def fetch_existing_indexes(self):
        # This query fetches index information for PostgreSQL
        query = """
        SELECT
            t.relname AS table_name,
            a.attname AS column_name,
            idx.relname AS index_name
        FROM
            pg_class t
        JOIN
            pg_attribute a ON a.attrelid = t.oid
        JOIN
            pg_index i ON i.indrelid = t.oid AND a.attnum = ANY(i.indkey)
        JOIN
            pg_class idx ON idx.oid = i.indexrelid
        WHERE
            t.relkind = 'r' -- Only tables
            AND t.relnamespace = (SELECT oid FROM pg_namespace WHERE nspname = 'public') -- Public schema
        ORDER BY
            t.relname, idx.relname, a.attnum;
        """
        print("\033[0;34mFetching existing indexes (simulated)...")
        # In a real scenario:
        # with self.conn.cursor() as cur:
        #     cur.execute(query)
        #     return cur.fetchall()
        
        # Simulate some existing indexes for demonstration
        return [
            ('users', 'id', 'users_pkey'),
            ('users', 'email', 'idx_users_email'),
            ('products', 'id', 'products_pkey'),
            ('orders', 'id', 'orders_pkey'),
            ('orders', 'customer_id', 'idx_orders_customer_id'),
        ]

    def fetch_table_columns(self):
        query = """
        SELECT
            table_name,
            column_name
        FROM
            information_schema.columns
        WHERE
            table_schema = 'public'
        ORDER BY
            table_name, column_name;
        """
        print("\033[0;34mFetching table columns (simulated)...")
        # In a real scenario:
        # with self.conn.cursor() as cur:
        #     cur.execute(query)
        #     return cur.fetchall()

        # Simulate some table columns
        return [
            ('users', 'id'), ('users', 'name'), ('users', 'email'), ('users', 'status'),
            ('products', 'id'), ('products', 'name'), ('products', 'price'),
            ('orders', 'id'), ('orders', 'customer_id'), ('orders', 'product_id'), ('orders', 'created_at'),
        ]

def suggest_missing_indexes(
    db_connector,
    frequently_queried_columns,
    dry_run=True
):
    if not db_connector.conn:
        print("\033[0;31mError: Not connected to database. Exiting.")
        return

    existing_indexes_raw = db_connector.fetch_existing_indexes()
    table_columns_raw = db_connector.fetch_table_columns()

    # Process existing indexes into a more usable format
    # { 'table_name': { 'column_name': 'index_name' } }
    existing_indexes = {}
    for table_name, column_name, index_name in existing_indexes_raw:
        if table_name not in existing_indexes:
            existing_indexes[table_name] = {}
        existing_indexes[table_name][column_name] = index_name

    # Process table columns into a set for quick lookup
    all_table_columns = set()
    for table_name, column_name in table_columns_raw:
        all_table_columns.add(f"{table_name}.{column_name}")

    suggested_indexes = []
    print("\n--- Index Suggestion Report ---")

    for col_spec in frequently_queried_columns:
        if '.' not in col_spec:
            print(f"\033[0;33mWarning: Skipping invalid column specification '{col_spec}'. Expected format: table.column")
            continue

        table_name, column_name = col_spec.split('.', 1)

        if col_spec not in all_table_columns:
            print(f"\033[0;33mWarning: Column '{col_spec}' not found in schema. Skipping.")
            continue

        if table_name in existing_indexes and column_name in existing_indexes[table_name]:
            print(f"\033[0;32mInfo: Column '{col_spec}' already indexed by '{existing_indexes[table_name][column_name]}'.")
        else:
            index_name = f"idx_{table_name}_{column_name}"
            create_index_sql = f"CREATE INDEX {index_name} ON {table_name} ({column_name});"
            suggested_indexes.append(create_index_sql)
            print(f"\033[0;31mSuggestion: Column '{col_spec}' is frequently queried but not indexed.")
            print(f"  Proposed SQL: {create_index_sql}")

    print("\n--- Summary ---")
    if suggested_indexes:
        print(f"\033[0;33mFound {len(suggested_indexes)} potential missing indexes.")
        if dry_run:
            print("\033[0;33mRun without --dry-run to execute these (after careful review!).")
        else:
            print("\033[0;32mExecuting suggested CREATE INDEX statements (simulated).")
            # In a real scenario, execute these SQL statements
            for sql in suggested_indexes:
                print(f"Executing: {sql}")
                # with db_connector.conn.cursor() as cur:
                #     cur.execute(sql)
            # db_connector.conn.commit()
    else:
        print("\033[0;32mNo missing indexes suggested for the provided columns.")

def main():
    parser = argparse.ArgumentParser(
        description="Suggests missing indexes for a PostgreSQL database based on frequently queried columns."
    )
    parser.add_argument('--host', default='localhost', help='Database host')
    parser.add_argument('--port', type=int, default=5432, help='Database port')
    parser.add_argument('--user', default='postgres', help='Database user')
    parser.add_argument('--password', default=None, help='Database password (will prompt if not provided)')
    parser.add_argument('--dbname', required=True, help='Database name')
    parser.add_argument('--columns', required=True,
                        help='Comma-separated list of frequently queried columns (e.g., table1.colA,table2.colB)')
    parser.add_argument('--dry-run', action='store_true', help='Only print suggested indexes, do not execute.')

    args = parser.parse_args()

    frequently_queried_columns = [col.strip() for col in args.columns.split(',')]

    db_connector = DatabaseConnector(
        host=args.host, port=args.port, user=args.user,
        password=args.password, dbname=args.dbname
    )

    db_connector.connect()
    if db_connector.conn:
        suggest_missing_indexes(db_connector, frequently_queried_columns, args.dry_run)
    db_connector.close()

if __name__ == '__main__':
    main()
