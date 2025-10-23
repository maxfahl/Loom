#!/usr/bin/env python3

# check_n_plus_1_queries.py
#
# Description:
#   Analyzes Rails log files to detect potential N+1 query issues.
#   N+1 queries occur when an application executes N additional database queries
#   for each result of an initial query, leading to significant performance degradation.
#   This script identifies repeated, similar queries within a short time window,
#   which is a strong indicator of an N+1 problem.
#
# Usage:
#   python3 check_n_plus_1_queries.py [OPTIONS] <LOG_FILE_PATH>
#
# Arguments:
#   <LOG_FILE_PATH>  Path to the Rails log file (e.g., log/development.log, log/production.log).
#
# Options:
#   -h, --help           Display this help message.
#   -t, --threshold      Time threshold in seconds to group similar queries (default: 0.1).
#   -c, --count          Minimum number of repeated queries to flag as N+1 (default: 5).
#   -o, --output         Output format (text, json). Default: text.
#   -d, --dry-run        Process the log file but do not output anything, just show summary.
#
# Example Usage:
#   python3 check_n_plus_1_queries.py log/development.log
#   python3 check_n_plus_1_queries.py log/production.log -t 0.05 -c 10 -o json
#   python3 check_n_plus_1_queries.py /var/log/rails/production.log --dry-run
#
# Production-ready features:
#   - Argument parsing with `argparse`.
#   - Configurable threshold and count for detection.
#   - Multiple output formats (text, JSON).
#   - Dry-run mode.
#   - Basic error handling for file operations.
#   - Colored output for better readability (requires `colorama` or similar, but kept simple for core Python).
#
import argparse
import re
import json
from collections import defaultdict
import datetime

def colorize(text, color_code):
    """Applies ANSI color codes to text."""
    return f"\033[{color_code}m{text}\033[0m"

def red(text):
    return colorize(text, "31")

def yellow(text):
    return colorize(text, "33")

def green(text):
    return colorize(text, "32")

def blue(text):
    return colorize(text, "34")

def parse_log_entry(line):
    """Parses a log line for SQL queries and timestamps."""
    # Example log format:
    # I, [2025-10-19T10:30:00.123456 #12345]  INFO -- :   User Load (0.5ms)  SELECT "users".* FROM "users" WHERE "users"."id" = $1 LIMIT $2
    # D, [2025-10-19T10:30:00.123456 #12345] DEBUG -- :   Post Load (0.8ms)  SELECT "posts".* FROM "posts" WHERE "posts"."user_id" = $1
    
    # Regex to capture timestamp and SQL query
    match = re.match(r'.*\[(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{6}) #\d+\]\s+\w+\s+--\s+:\s+.*?\s+\(\d+\.\d+ms\)\s+(SELECT|INSERT|UPDATE|DELETE|BEGIN|COMMIT|ROLLBACK)\s+.*', line)
    if match:
        timestamp_str = match.group(1)
        try:
            timestamp = datetime.datetime.strptime(timestamp_str, "%Y-%m-%dT%H:%M:%S.%f")
            # Extract the SQL query part, simplifying it by removing specific values
            sql_query = re.sub(r'(\'|\")["\w\s\-\.]+(\'|\" )', "'?'", line) # Replace string literals
            sql_query = re.sub(r'\b\d+\b', '?', sql_query) # Replace numbers
            sql_query = re.sub(r'\$\d+', '$?', sql_query) # Replace parameterized values
            sql_query = re.sub(r'LIMIT \?', 'LIMIT $?', sql_query) # Specific for LIMIT
            sql_query = re.sub(r'OFFSET \?', 'OFFSET $?', sql_query) # Specific for OFFSET
            # Further simplify by removing specific table/column names if needed, but keep general structure
            return timestamp, sql_query.strip()
        except ValueError:
            pass
    return None, None

def analyze_log(log_file_path, threshold, min_count, dry_run=False):
    """Analyzes the log file for N+1 queries."""
    potential_n_plus_1 = defaultdict(list)
    total_queries = 0
    flagged_issues = 0

    try:
        with open(log_file_path, 'r') as f:
            for line_num, line in enumerate(f, 1):
                timestamp, query = parse_log_entry(line)
                if timestamp and query:
                    total_queries += 1
                    # Group queries by a simplified version of the SQL
                    # This simplification is crucial to catch N+1 where only parameters change
                    simplified_query = re.sub(r'WHERE \"(\w+)\"\."id" = \$\? LIMIT \$\?', 'WHERE "table"."id" = $? LIMIT $?', query)
                    simplified_query = re.sub(r'WHERE \"(\w+)\"\."(\w+)_id" = \$\?', 'WHERE "table"."foreign_id" = $?', simplified_query)
                    
                    potential_n_plus_1[simplified_query].append((timestamp, line_num, line.strip()))
    except FileNotFoundError:
        print(red(f"Error: Log file not found at '{log_file_path}'"))
        return None
    except Exception as e:
        print(red(f"Error reading log file: {e}"))
        return None

    results = []
    for query_pattern, occurrences in potential_n_plus_1.items():
        # Sort occurrences by timestamp to detect sequences
        occurrences.sort(key=lambda x: x[0])

        current_sequence = []
        for i, (timestamp, line_num, original_line) in enumerate(occurrences):
            if not current_sequence:
                current_sequence.append((timestamp, line_num, original_line))
            else:
                prev_timestamp, _, _ = current_sequence[-1]
                if (timestamp - prev_timestamp).total_seconds() <= threshold:
                    current_sequence.append((timestamp, line_num, original_line))
                else:
                    if len(current_sequence) >= min_count:
                        flagged_issues += 1
                        results.append({
                            "pattern": query_pattern,
                            "count": len(current_sequence),
                            "first_occurrence_line": current_sequence[0][1],
                            "last_occurrence_line": current_sequence[-1][1],
                            "occurrences": [
                                {"timestamp": ts.isoformat(), "line_num": ln, "log_line": ol}
                                for ts, ln, ol in current_sequence
                            ]
                        })
                    current_sequence = [(timestamp, line_num, original_line)]
        
        # Check for any remaining sequence after loop
        if len(current_sequence) >= min_count:
            flagged_issues += 1
            results.append({
                "pattern": query_pattern,
                "count": len(current_sequence),
                "first_occurrence_line": current_sequence[0][1],
                "last_occurrence_line": current_sequence[-1][1],
                "occurrences": [
                    {"timestamp": ts.isoformat(), "line_num": ln, "log_line": ol}
                    for ts, ln, ol in current_sequence
                ]
            })
    
    if dry_run:
        print(blue(f"Dry run complete. Total queries processed: {total_queries}. Potential N+1 issues flagged: {flagged_issues}."))
        return [] # Return empty list for dry run

    return results

def main():
    parser = argparse.ArgumentParser(
        description="Analyzes Rails log files to detect potential N+1 query issues.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "log_file_path",
        help="Path to the Rails log file (e.g., log/development.log, log/production.log)."
    )
    parser.add_argument(
        "-t", "--threshold",
        type=float,
        default=0.1,
        help="Time threshold in seconds to group similar queries (default: 0.1)."
    )
    parser.add_argument(
        "-c", "--count",
        type=int,
        default=5,
        help="Minimum number of repeated queries to flag as N+1 (default: 5)."
    )
    parser.add_argument(
        "-o", "--output",
        choices=["text", "json"],
        default="text",
        help="Output format (text, json). Default: text."
    )
    parser.add_argument(
        "-d", "--dry-run",
        action="store_true",
        help="Process the log file but do not output anything, just show summary."
    )

    args = parser.parse_args()

    print(blue(f"Analyzing log file: {args.log_file_path} for N+1 queries..."))
    print(blue(f"Threshold: {args.threshold}s, Min Count: {args.count}"))

    results = analyze_log(args.log_file_path, args.threshold, args.count, args.dry_run)

    if results is None: # Error occurred during analysis
        exit(1)

    if args.dry_run:
        exit(0)

    if not results:
        print(green("No potential N+1 query issues detected within the specified criteria."))
        exit(0)

    if args.output == "json":
        print(json.dumps(results, indent=2))
    else:
        print(yellow("\n--- Detected Potential N+1 Query Issues ({len(results)}) ---"))
        for i, issue in enumerate(results):
            print(f"\n{blue('Issue {i+1}:')}")
            print(f"  {yellow('Pattern:')} {issue['pattern']}")
            print(f"  {yellow('Repeated Count:')} {issue['count']}")
            print(f"  {yellow('First Occurrence Line:')} {issue['first_occurrence_line']}")
            print(f"  {yellow('Last Occurrence Line:')} {issue['last_occurrence_line']}")
            print(yellow("  Sample Occurrences:"))
            for occ in issue['occurrences'][:3]: # Show first 3 occurrences
                print(f"    Line {occ['line_num']}: {occ['log_line']}")
            if issue['count'] > 3:
                print(f"    ... ({issue['count'] - 3} more occurrences)")
        print(yellow("\n--- End of N+1 Query Report ---"))
        print(yellow("Consider using eager loading (e.g., `.includes()`, `.preload()`) to resolve these issues."))

if __name__ == "__main__":
    main()
