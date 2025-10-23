#!/usr/bin/env python3

# invalidate-query-cli.py
#
# Purpose: A command-line interface (CLI) tool to simulate invalidating TanStack Query caches.
#          This is useful for demonstrating how cache invalidation works or for integrating
#          with external systems (e.g., CI/CD, backend webhooks) that need to signal
#          a frontend to refetch data (though actual invalidation would happen via a
#          websocket or similar mechanism in a real application).
#
# Usage:
#   python3 invalidate-query-cli.py <query_key_pattern> [--exact] [--dry-run]
#
# Examples:
#   python3 invalidate-query-cli.py todos
#   python3 invalidate-query-cli.py "['todos', '123']" --exact
#   python3 invalidate-query-cli.py users --dry-run
#
# Options:
#   <query_key_pattern>  The query key or pattern to invalidate (e.g., "todos", "['todos', '123']")
#                        For array keys, use JSON string format.
#   --exact              If set, invalidates only queries that exactly match the pattern.
#                        Otherwise, invalidates queries that start with the pattern.
#   --dry-run            Simulate the invalidation without performing any action.
#   --verbose            Enable verbose output.
#   --help               Display this help message.

import argparse
import json
import sys

def colored_print(text, color):
    """Prints text in a specified color."""
    colors = {
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "magenta": "\033[95m",
        "cyan": "\033[96m",
        "white": "\033[97m",
        "reset": "\033[0m",
    }
    print(f"{colors.get(color, colors['reset'])}{text}{colors['reset']}")

def main():
    parser = argparse.ArgumentParser(
        description="Simulate TanStack Query cache invalidation.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "query_key_pattern",
        help="The query key or pattern to invalidate (e.g., \"todos\", \"[\'todos\', \'123\']\").\n"
             "For array keys, use JSON string format."
    )
    parser.add_argument(
        "--exact",
        action="store_true",
        help="If set, invalidates only queries that exactly match the pattern.\n"
             "Otherwise, invalidates queries that start with the pattern."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simulate the invalidation without performing any action."
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose output."
    )

    args = parser.parse_args()

    query_key_pattern = args.query_key_pattern
    is_exact = args.exact
    is_dry_run = args.dry_run
    is_verbose = args.verbose

    colored_print(f"\n--- TanStack Query Invalidation CLI ---", "blue")
    colored_print(f"Pattern: {query_key_pattern}", "cyan")
    colored_print(f"Exact Match: {is_exact}", "cyan")
    colored_print(f"Dry Run: {is_dry_run}", "cyan")

    try:
        # Attempt to parse as JSON array for hierarchical keys
        parsed_pattern = json.loads(query_key_pattern)
        if not isinstance(parsed_pattern, list):
            raise ValueError("Query key pattern as JSON must be a list.")
        display_pattern = json.dumps(parsed_pattern)
    except json.JSONDecodeError:
        # Treat as a simple string key
        parsed_pattern = query_key_pattern
        display_pattern = f"'{{query_key_pattern}}"'
    except ValueError as e:
        colored_print(f"Error parsing query key pattern: {e}", "red")
        sys.exit(1)

    colored_print(f"Interpreted pattern: {display_pattern}", "cyan")

    if is_dry_run:
        colored_print("\n(Dry Run Mode) No actual invalidation will occur.", "yellow")

    # In a real application, this is where you'd interact with a QueryClient
    # or send a signal to the frontend. For this simulation, we just log.
    if is_exact:
        message = f"Simulating invalidation for exact query key: {display_pattern}"
    else:
        message = f"Simulating invalidation for query keys starting with: {display_pattern}"

    if is_dry_run:
        colored_print(f"DRY RUN: {message}", "yellow")
    else:
        colored_print(f"ACTION: {message}", "green")

    if is_verbose:
        colored_print("\nVerbose output enabled. Details of simulated action:", "blue")
        colored_print("  - This script simulates the `queryClient.invalidateQueries()` call.", "white")
        colored_print("  - In a real-world scenario, this script would trigger a mechanism (e.g., a websocket event, a serverless function call) that informs the frontend application to execute `queryClient.invalidateQueries()`.", "white")
        colored_print("  - Ensure your frontend application is configured to listen for such signals and perform the actual invalidation.", "white")

    colored_print("\n--- Simulation Complete ---", "blue")

if __name__ == "__main__":
    main()
