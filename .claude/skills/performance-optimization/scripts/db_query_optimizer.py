#!/usr/bin/env python3

"""
db_query_optimizer.py

Analyzes a given SQL query and provides suggestions for performance optimization,
focusing on common anti-patterns like SELECT * and identifying potential indexing
opportunities based on WHERE, JOIN, ORDER BY, and GROUP BY clauses.

Usage:
  python3 db_query_optimizer.py -q "SELECT * FROM users WHERE age > 30 ORDER BY name"
  python3 db_query_optimizer.py -f my_query.sql
  python3 db_query_optimizer.py -q "SELECT id, name FROM products WHERE category_id = 5 GROUP BY name"

"""

import argparse
import re
import sys

# --- Configuration / Constants ---
COLOR_RED = "\033[91m"
COLOR_GREEN = "\033[92m"
COLOR_YELLOW = "\033[93m"
COLOR_BLUE = "\033[94m"
COLOR_RESET = "\033[0m"

# --- Helper Functions ---

def analyze_query(query: str) -> list[str]:
    """Analyzes the SQL query and returns a list of optimization suggestions."""
    suggestions = []
    query_lower = query.lower()

    # Suggestion 1: Avoid SELECT *
    if re.search(r"select\s+\*\s+from", query_lower):
        suggestions.append(
            f"{COLOR_YELLOW}Suggestion: Avoid using SELECT *.{COLOR_RESET} "
            "Explicitly list the columns you need to retrieve. This reduces data transfer "
            "and processing overhead, especially for tables with many columns."
        )

    # Suggestion 2: Identify columns for WHERE clause indexing
    where_match = re.search(r"where\s+(.*?)(?:order\s+by|group\s+by|limit|offset|;|$)", query_lower, re.DOTALL)
    if where_match:
        where_clause = where_match.group(1)
        # Simple heuristic: find column names that are likely used in conditions
        # This regex is basic and might need refinement for complex WHERE clauses
        potential_indexed_columns = set(re.findall(r"\b(\w+)\s*[=<>!~]+\s*['"\w.]+", where_clause))
        potential_indexed_columns.update(re.findall(r"\b(\w+)\s+(?:is\s+not\s+null|is\s+null)", where_clause))
        potential_indexed_columns.update(re.findall(r"\b(\w+)\s+between\s+.*?\s+and\s+.*?", where_clause))
        potential_indexed_columns.update(re.findall(r"\b(\w+)\s+in\s*\(.*?\)", where_clause))

        if potential_indexed_columns:
            suggestions.append(
                f"{COLOR_BLUE}Consider indexing columns used in WHERE clauses:{COLOR_RESET} "
                f"{COLOR_GREEN}{', '.join(sorted(potential_indexed_columns))}{COLOR_RESET}. "
                "Indexes can significantly speed up data retrieval for filtered results."
            )

    # Suggestion 3: Identify columns for ORDER BY clause indexing
    order_by_match = re.search(r"order\s+by\s+(.*?)(?:limit|offset|;|$)", query_lower)
    if order_by_match:
        order_by_columns = re.findall(r"\b(\w+)(?:\s+asc|\s+desc)?", order_by_match.group(1))
        if order_by_columns:
            suggestions.append(
                f"{COLOR_BLUE}Consider indexing columns used in ORDER BY clauses:{COLOR_RESET} "
                f"{COLOR_GREEN}{', '.join(sorted(set(order_by_columns)))}{COLOR_RESET}. "
                "Indexes can help avoid costly sorts, especially on large datasets."
            )

    # Suggestion 4: Identify columns for GROUP BY clause indexing
    group_by_match = re.search(r"group\s+by\s+(.*?)(?:having|order\s+by|limit|offset|;|$)", query_lower)
    if group_by_match:
        group_by_columns = re.findall(r"\b(\w+)", group_by_match.group(1))
        if group_by_columns:
            suggestions.append(
                f"{COLOR_BLUE}Consider indexing columns used in GROUP BY clauses:{COLOR_RESET} "
                f"{COLOR_GREEN}{', '.join(sorted(set(group_by_columns)))}{COLOR_RESET}. "
                "Indexes can speed up aggregation operations."
            )

    # Suggestion 5: Identify columns for JOIN clauses indexing
    join_matches = re.findall(r"join\s+\w+\s+on\s+.*?\. (\w+)\s*=\s*.*?\.\w+", query_lower)
    if join_matches:
        suggestions.append(
            f"{COLOR_BLUE}Consider indexing columns used in JOIN conditions:{COLOR_RESET} "
            f"{COLOR_GREEN}{', '.join(sorted(set(join_matches)))}{COLOR_RESET}. "
            "Indexing foreign key columns or columns used in JOINs can drastically improve join performance."
        )

    if not suggestions:
        suggestions.append(f"{COLOR_GREEN}No obvious optimization suggestions found for this query. Looks good!{COLOR_RESET}")

    return suggestions

# --- Main Execution ---

def main():
    parser = argparse.ArgumentParser(
        description="Analyze SQL queries for performance optimization suggestions.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "-q", "--query",
        type=str,
        help="The SQL query string to analyze."
    )
    parser.add_argument(
        "-f", "--file",
        type=str,
        help="Path to a file containing the SQL query to analyze."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simulate the analysis without performing any actual database operations (N/A for this script)."
    )

    args = parser.parse_args()

    query_to_analyze = ""
    if args.query:
        query_to_analyze = args.query
    elif args.file:
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                query_to_analyze = f.read()
        except FileNotFoundError:
            print(f"{COLOR_RED}Error: File not found at {args.file}{COLOR_RESET}", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"{COLOR_RED}Error reading file {args.file}: {e}{COLOR_RESET}", file=sys.stderr)
            sys.exit(1)
    else:
        parser.print_help()
        sys.exit(1)

    if not query_to_analyze.strip():
        print(f"{COLOR_YELLOW}Warning: No query provided for analysis.{COLOR_RESET}", file=sys.stderr)
        sys.exit(0)

    print(f"{COLOR_BLUE}Analyzing SQL Query:{COLOR_RESET}\n---\n{query_to_analyze.strip()}\n---\n")

    if args.dry_run:
        print(f"{COLOR_YELLOW}Dry run: Analysis would be performed for the query above.{COLOR_RESET}")
        print(f"{COLOR_YELLOW}No actual database operations are performed by this script in any mode.{COLOR_RESET}")
        sys.exit(0)

    suggestions = analyze_query(query_to_analyze)

    print(f"{COLOR_BLUE}Optimization Suggestions:{COLOR_RESET}")
    if suggestions:
        for i, suggestion in enumerate(suggestions):
            print(f"  {i+1}. {suggestion}")
    else:
        print(f"  {COLOR_GREEN}No specific suggestions found. The query appears well-formed.{COLOR_RESET}")

if __name__ == "__main__":
    main()
