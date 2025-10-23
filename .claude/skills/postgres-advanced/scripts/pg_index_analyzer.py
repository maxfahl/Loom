
import argparse
import os
import sys

try:
    import psycopg2
    from psycopg2 import sql
except ImportError:
    print("Error: psycopg2 not found. Please install it using: pip install psycopg2-binary")
    sys.exit(1)

def get_db_connection(dbname, user, password, host, port):
    """
    Establishes a connection to the PostgreSQL database.
    """
    try:
        conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
        return conn
    except psycopg2.Error as e:
        print(f"Error connecting to the database: {e}")
        sys.exit(1)

def analyze_missing_indexes(cursor):
    """
    Analyzes pg_stat_statements to find columns frequently used in WHERE/ORDER BY
    clauses that might benefit from new indexes.
    This is a simplified heuristic and may require more sophisticated parsing for real-world scenarios.
    """
    print("\n--- Analyzing for potentially missing indexes ---")
    cursor.execute("SELECT query, calls, total_time FROM pg_stat_statements ORDER BY total_time DESC LIMIT 50;")
    queries = cursor.fetchall()

    potential_indexes = {}

    for query_text, calls, total_time in queries:
        # Simple regex to find columns in WHERE/ORDER BY clauses
        # This is a very basic approach and might miss complex cases or false positives.
        where_match = re.search(r'WHERE\s+([\w\d_\.]+)\s*[<=>!]+', query_text, re.IGNORECASE)
        order_match = re.search(r'ORDER BY\s+([\w\d_\.]+)', query_text, re.IGNORECASE)

        columns_to_check = set()
        if where_match:
            col = where_match.group(1).split('.')[-1] # Get column name, ignore table alias
            columns_to_check.add(col)
        if order_match:
            col = order_match.group(1).split('.')[-1]
            columns_to_check.add(col)

        for col_name in columns_to_check:
            # Further check if this column is already indexed on relevant tables
            # This part would require more advanced schema introspection.
            # For this example, we'll just list potential candidates.
            if col_name not in potential_indexes:
                potential_indexes[col_name] = {'queries': [], 'total_time': 0}
            potential_indexes[col_name]['queries'].append(query_text)
            potential_indexes[col_name]['total_time'] += total_time

    if potential_indexes:
        print("Potential columns for new indexes (based on top 50 queries by total_time):")
        for col, data in sorted(potential_indexes.items(), key=lambda item: item[1]['total_time'], reverse=True):
            print(f"  - Column: {col} (involved in {len(data['queries'])} queries, total time: {data['total_time']:.2f}ms)")
            print(f"    Consider: CREATE INDEX ON <table_name> ({col});")
    else:
        print("No obvious missing index candidates found in top queries.")

def analyze_unused_indexes(cursor):
    """
    Analyzes pg_stat_user_indexes to find indexes that are rarely or never used.
    """
    print("\n--- Analyzing for unused or rarely used indexes ---")
    cursor.execute(
        """SELECT
            s.relname AS table_name,
            s.indexrelname AS index_name,
            pg_size_pretty(pg_relation_size(s.indexrelid)) AS index_size,
            s.idx_scan AS index_scans
        FROM
            pg_stat_user_indexes s
        JOIN
            pg_index i ON s.indexrelid = i.indexrelid
        WHERE
            s.idx_scan = 0 AND NOT i.indisprimary AND NOT i.indisunique
        ORDER BY
            pg_relation_size(s.indexrelid) DESC;"""
    )
    unused_indexes = cursor.fetchall()

    if unused_indexes:
        print("The following non-primary, non-unique indexes have 0 scans (potential candidates for removal):")
        for table_name, index_name, index_size, index_scans in unused_indexes:
            print(f"  - Table: {table_name}, Index: {index_name}, Size: {index_size}, Scans: {index_scans}")
            print(f"    Consider: DROP INDEX {index_name};")
    else:
        print("No unused indexes found (or pg_stat_statements is not enabled/reset).")

def main():
    parser = argparse.ArgumentParser(
        description="Analyzes PostgreSQL database for index optimization opportunities.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "--dbname", required=True,
        help="Database name."
    )
    parser.add_argument(
        "--user", required=True,
        help="Database user."
    )
    parser.add_argument(
        "--password", default=os.getenv("PGPASSWORD"),
        help="Database password. Can be provided via PGPASSWORD environment variable."
    )
    parser.add_argument(
        "--host", default="localhost",
        help="Database host (default: localhost)."
    )
    parser.add_argument(
        "--port", type=int, default=5432,
        help="Database port (default: 5432)."
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Show recommendations without executing any DDL."
    )

    args = parser.parse_args()

    print("Connecting to PostgreSQL database...")
    conn = get_db_connection(args.dbname, args.user, args.password, args.host, args.port)
    conn.autocommit = True # For DDL statements if not in dry-run
    cursor = conn.cursor()

    # Check if pg_stat_statements is enabled
    cursor.execute("SELECT 1 FROM pg_extension WHERE extname = 'pg_stat_statements';")
    if not cursor.fetchone():
        print("Warning: pg_stat_statements extension is not enabled. "
              "Index analysis based on query patterns will be limited.\n"
              "To enable: CREATE EXTENSION pg_stat_statements; (requires superuser)")
    else:
        # Reset pg_stat_statements for fresh analysis if needed (optional, user discretion)
        # cursor.execute("SELECT pg_stat_statements_reset();")
        # print("pg_stat_statements reset for fresh analysis.")
        pass

    analyze_missing_indexes(cursor)
    analyze_unused_indexes(cursor)

    cursor.close()
    conn.close()
    print("\nAnalysis complete.")
    if args.dry_run:
        print("Recommendations were shown in dry-run mode. No changes were applied.")
    else:
        print("Please review recommendations and apply manually if desired.")

if __name__ == "__main__":
    import re # Import re here as it's used in analyze_missing_indexes
    main()
