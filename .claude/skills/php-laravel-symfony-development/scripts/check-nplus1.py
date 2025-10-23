import argparse
import re
import os
from collections import defaultdict

# check-nplus1.py
#
# Description:
#   Analyzes application logs or query debug output to detect potential N+1 query problems.
#   This script looks for repetitive query patterns that often indicate N+1 issues.
#   Note: For precise N+1 detection, consider using framework-specific tools like
#   Laravel Telescope, Symfony Profiler, or enabling detailed database query logging.
#   This script provides a generic pattern-matching approach.
#
# Usage:
#   python check-nplus1.py --log-file=path/to/app.log [--threshold=5] [--output=report.txt]
#   python check-nplus1.py --log-dir=path/to/logs [--threshold=10]
#
# Arguments:
#   --log-file      Path to a single log file to analyze.
#   --log-dir       Path to a directory containing log files to analyze.
#   --threshold     (Optional) Minimum number of times a similar query pattern must occur
#                   within a short window to be flagged as potential N+1. Default is 5.
#   --output        (Optional) Path to save the N+1 report. If not provided, prints to console.
#
# Examples:
#   python check-nplus1.py --log-file=storage/logs/laravel.log
#   python check-nplus1.py --log-dir=var/log --threshold=10 --output=nplus1_report.md
#
# Requirements:
#   - Log files should contain database query statements.
#
# Exit Codes:
#   0 - Success
#   1 - Invalid arguments or file/directory not found

class Color:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def color_echo(color, message):
    print(f"{color}{message}{Color.END}")

def extract_query_pattern(query):
    # Simple regex to generalize queries by removing specific values
    # This is a basic approach; more sophisticated parsing might be needed for complex queries
    query = re.sub(r"'[^']*'", "'?'", query) # Replace strings
    query = re.sub(r"\b\d+\b", "?", query) # Replace numbers
    query = re.sub(r"IN \([^)]*\)", "IN (?) ", query) # Replace IN clause values
    return query.strip()

def analyze_log_file(file_path, threshold):
    potential_nplus1 = defaultdict(lambda: {'count': 0, 'lines': []})
    query_patterns = defaultdict(list)

    color_echo(Color.BLUE, f"Analyzing file: {file_path}")

    try:
        with open(file_path, 'r') as f:
            for i, line in enumerate(f):
                # Look for common SQL keywords (SELECT, INSERT, UPDATE, DELETE)
                # This regex is a starting point and might need refinement based on actual log formats
                match = re.search(r'(SELECT|INSERT|UPDATE|DELETE)\s+.*(?:FROM|INTO|UPDATE)\s+`?(\w+)?`?.*(?:WHERE|SET|VALUES|LIMIT|ORDER BY)?.*\s*;', line, re.IGNORECASE)
                if match:
                    full_query = match.group(0).strip()
                    table_name = match.group(2)
                    generalized_query = extract_query_pattern(full_query)

                    query_patterns[generalized_query].append({'line': i + 1, 'table': table_name, 'full_query': full_query})

    except FileNotFoundError:
        color_echo(Color.RED, f"Error: Log file not found: {file_path}")
        return {}
    except Exception as e:
        color_echo(Color.RED, f"Error reading file {file_path}: {e}")
        return {}

    report = {}
    for pattern, occurrences in query_patterns.items():
        if len(occurrences) >= threshold:
            report[pattern] = {
                'count': len(occurrences),
                'table': occurrences[0]['table'],
                'example_query': occurrences[0]['full_query'],
                'lines': [o['line'] for o in occurrences]
            }
    return report

def main():
    parser = argparse.ArgumentParser(
        description="Detects potential N+1 query problems in application logs."
    )
    parser.add_argument(
        "--log-file",
        help="Path to a single log file to analyze."
    )
    parser.add_argument(
        "--log-dir",
        help="Path to a directory containing log files to analyze."
    )
    parser.add_argument(
        "--threshold",
        type=int,
        default=5,
        help="Minimum number of times a similar query pattern must occur to be flagged. Default is 5."
    )
    parser.add_argument(
        "--output",
        help="Path to save the N+1 report. If not provided, prints to console."
    )

    args = parser.parse_args()

    if not args.log_file and not args.log_dir:
        color_echo(Color.RED, "Error: Either --log-file or --log-dir must be provided.")
        parser.print_help()
        sys.exit(1)

    all_reports = {}
    if args.log_file:
        if not os.path.exists(args.log_file):
            color_echo(Color.RED, f"Error: Log file not found: {args.log_file}")
            sys.exit(1)
        all_reports[args.log_file] = analyze_log_file(args.log_file, args.threshold)
    elif args.log_dir:
        if not os.path.isdir(args.log_dir):
            color_echo(Color.RED, f"Error: Log directory not found: {args.log_dir}")
            sys.exit(1)
        for root, _, files in os.walk(args.log_dir):
            for file in files:
                if file.endswith(".log") or file.endswith(".txt"):
                    file_path = os.path.join(root, file)
                    report = analyze_log_file(file_path, args.threshold)
                    if report:
                        all_reports[file_path] = report

    output_content = []
    has_issues = False

    for file_path, report in all_reports.items():
        if report:
            has_issues = True
            output_content.append(f"## Potential N+1 Issues in {file_path}\n")
            output_content.append(f"Threshold for flagging: {args.threshold} similar queries.\n\n")
            for pattern, data in report.items():
                output_content.append(f"### Table: {data['table']}\n")
                output_content.append(f"- **Repeated Query Pattern**: `{pattern}`\n")
                output_content.append(f"- **Occurrences**: {data['count']}\n")
                output_content.append(f"- **Example Query**: `{data['example_query']}`\n")
                output_content.append(f"- **Lines**: {', '.join(map(str, data['lines']))}\n\n")
        else:
            output_content.append(f"No potential N+1 issues found in {file_path} above threshold {args.threshold}.\n\n")

    if not has_issues:
        output_content.append("No potential N+1 issues found across analyzed logs.\n")

    if args.output:
        try:
            with open(args.output, 'w') as f:
                f.write("\n".join(output_content))
            color_echo(Color.GREEN, f"N+1 report saved to {args.output}")
        except Exception as e:
            color_echo(Color.RED, f"Error saving report to {args.output}: {e}")
    else:
        for line in output_content:
            print(line, end='')

    if has_issues:
        color_echo(Color.YELLOW, "\nConsider reviewing the identified query patterns for potential N+1 optimizations.")
    else:
        color_echo(Color.GREEN, "\nNo N+1 issues detected based on the current analysis criteria.")

if __name__ == "__main__":
    main()
