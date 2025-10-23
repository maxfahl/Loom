#!/usr/bin/env python3
"""
SQL Query Performance Analyzer

This script connects to a PostgreSQL database, executes a given SQL query with EXPLAIN ANALYZE,
and provides a human-readable summary of its performance characteristics and potential optimization suggestions.

Usage:
    python3 analyze_query.py "SELECT * FROM users WHERE id = 1;" \
        --db-url "postgresql://user:password@host:port/dbname"

Example:
    python3 analyze_query.py "SELECT p.name, c.name FROM products p JOIN categories c ON p.category_id = c.id WHERE p.price > 100;" \
        --db-url "postgresql://app_user:secure_password@localhost:5432/my_app_db"

Configuration:
    - Supports PostgreSQL via psycopg2.
    - Database URL can be provided via --db-url or DB_URL environment variable.
"""

import argparse
import os
import sys
import re
import json

try:
    import psycopg2
    from psycopg2 import sql
except ImportError:
    print("\033[91mError: psycopg2 not found. Please install it using: pip install psycopg2-binary\033[0m", file=sys.stderr)
    sys.exit(1)

def parse_explain_output(explain_output: str) -> dict:
    """
    Parses the EXPLAIN ANALYZE output and extracts key performance metrics and warnings.
    This is a simplified parser and might need to be extended for more complex outputs.
    """
    summary = {
        "total_cost": None,
        "total_rows": None,
        "execution_time_ms": None,
        "planning_time_ms": None,
        "warnings": [],
        "suggestions": []
    }

    # Extract total execution time
    exec_time_match = re.search(r"Execution Time: (\d+\.\d+) ms", explain_output)
    if exec_time_match:
        summary["execution_time_ms"] = float(exec_time_match.group(1))

    # Extract planning time
    plan_time_match = re.search(r"Planning Time: (\d+\.\d+) ms", explain_output)
    if plan_time_match:
        summary["planning_time_ms"] = float(plan_time_match.group(1))

    # Look for sequential scans (full table scans)
    if "Seq Scan" in explain_output:
        summary["warnings"].append("Potential full table scan detected (Seq Scan).")
        summary["suggestions"].append("Consider adding an index on the columns used in the WHERE clause or JOIN conditions.")

    # Look for high costs or large row estimates vs actual
    # This is a very basic heuristic and needs more sophisticated parsing for accuracy
    cost_match = re.search(r"cost=\d+\.\d+\.\.(\d+\.\d+)", explain_output)
    if cost_match:
        summary["total_cost"] = float(cost_match.group(1))
        if summary["total_cost"] > 1000:
            summary["warnings"].append(f"High estimated total cost: {summary['total_cost']}.")
            summary["suggestions"].append("Review query for inefficiencies, especially JOINs and WHERE clauses.")

    # Check for temporary files (indicating sort/hash operations that might spill to disk)
    if "temporary file" in explain_output.lower():
        summary["warnings"].append("Query might be using temporary files (e.g., for large sorts).")
        summary["suggestions"].append("Increase `work_mem` or optimize query to avoid large sorts/hashes.")

    return summary

def analyze_query(db_url: str, query: str, output_format: str):
    """
    Connects to the database, runs EXPLAIN ANALYZE on the query, and prints the analysis.
    """
    conn = None
    try:
        conn = psycopg2.connect(db_url)
        cur = conn.cursor()

        # Use EXPLAIN ANALYZE for actual execution details
        explain_query = sql.SQL("EXPLAIN (ANALYZE, VERBOSE, FORMAT TEXT) {}").format(sql.SQL(query))
        cur.execute(explain_query)
        explain_output = "\n".join([row[0] for row in cur.fetchall()])

        analysis_summary = parse_explain_output(explain_output)

        if output_format == "json":
            print(json.dumps({
                "query": query,
                "explain_output": explain_output,
                "analysis_summary": analysis_summary
            }, indent=2))
        else:
            print("\033[1m--- SQL Query Analysis ---\033[0m")
            print(f"\033[1mQuery:\033[0m {query}")
            print("\n\033[1m--- EXPLAIN ANALYZE Output ---\033[0m")
            print(explain_output)

            print("\n\033[1m--- Analysis Summary ---\033[0m")
            if analysis_summary["execution_time_ms"] is not None:
                print(f"  \033[96mExecution Time:\033[0m {analysis_summary['execution_time_ms']:.2f} ms")
            if analysis_summary["planning_time_ms"] is not None:
                print(f"  \033[96mPlanning Time:\033[0m {analysis_summary['planning_time_ms']:.2f} ms")
            if analysis_summary["total_cost"] is not None:
                print(f"  \033[96mEstimated Total Cost:\033[0m {analysis_summary['total_cost']:.2f}")

            if analysis_summary["warnings"]:
                print("\n\033[93m--- Warnings ---\033[0m")
                for warning in analysis_summary["warnings"]:
                    print(f"  - {warning}")

            if analysis_summary["suggestions"]:
                print("\n\033[94m--- Optimization Suggestions ---\033[0m")
                for suggestion in analysis_summary["suggestions"]:
                    print(f"  - {suggestion}")

            print("\n\033[1m--- End of Analysis ---\033[0m")

    except psycopg2.Error as e:
        print(f"\033[91mDatabase error: {e}\033[0m", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"\033[91mAn unexpected error occurred: {e}\033[0m", file=sys.stderr)
        sys.exit(1)
    finally:
        if conn:
            conn.close()

def main():
    parser = argparse.ArgumentParser(
        description="Analyze SQL query performance using EXPLAIN ANALYZE.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "query",
        help="The SQL query to analyze."
    )
    parser.add_argument(
        "--db-url",
        default=os.environ.get("DB_URL"),
        help="Database connection URL (e.g., 'postgresql://user:password@host:port/dbname'). \ 
              Can also be set via the DB_URL environment variable."
    )
    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format for the analysis. Defaults to 'text'."
    )

    args = parser.parse_args()

    if not args.db_url:
        print("\033[91mError: Database URL not provided. Use --db-url or set DB_URL environment variable.\033[0m", file=sys.stderr)
        sys.exit(1)

analyze_query(args.db_url, args.query, args.format)

if __name__ == "__main__":
    main()
