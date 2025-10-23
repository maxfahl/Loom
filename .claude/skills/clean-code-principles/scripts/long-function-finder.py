#!/usr/bin/env python3

"""
long-function-finder.py

Description:
  A Python script that identifies functions in TypeScript/JavaScript files
  that exceed a configurable line limit. Long functions often violate the
  Single Responsibility Principle and are harder to read and test.

Usage:
  python3 long-function-finder.py <path_to_directory_or_file> [--max-lines N]

Examples:
  python3 scripts/long-function-finder.py src/
  python3 scripts/long-function-finder.py src/components/MyComponent.tsx --max-lines 50
  python3 scripts/long-function-finder.py . --max-lines 30

Configuration Options:
  --max-lines N: Maximum allowed lines for a function. Functions exceeding this will be reported. Default: 40.

Exit Codes:
  0: No functions found exceeding the line limit or analysis completed successfully.
  1: One or more functions exceed the line limit.
"""

import argparse
import os
import re
import sys

class Color:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[0;33m'
    BLUE = '\033[0;34m'
    NC = '\033[0m' # No Color

def print_color(color, message):
    print(f"{color}{message}{Color.NC}")

def analyze_file(filepath: str, max_lines: int) -> list:
    results = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Regex to find functions/methods in TypeScript/JavaScript
        # This regex attempts to capture the function name and its body.
        # It's a simplified approach and might not be perfect for all edge cases.
        function_pattern = re.compile(
            r'(?:(?:export|public|private|protected|static|async)\s+)*'  # Modifiers
            r'(?:function\s+([a-zA-Z_][a-zA-Z0-9_]*)|([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*(?:function|\()|([a-zA-Z_][a-zA-Z0-9_]*):\s*(?:function|\()|([a-zA-Z_][a-zA-Z0-9_]*)\s*\()' # Function declarations, arrow functions, object methods
            r'(?:[^;{{]*)' # Arguments and return types
            r'{{([^{{}}]* (?:{{[^{{}}]*}} [^{{}}]*)*)}}', # Function body (basic brace matching)
            re.DOTALL
        )

        for match in function_pattern.finditer(content):
            function_name = match.group(1) or match.group(2) or match.group(3) or match.group(4)
            function_body = match.group(5)

            if function_name and function_body:
                # Count non-empty lines in the function body
                lines_in_function = len([line for line in function_body.splitlines() if line.strip()])
                if lines_in_function > max_lines:
                    results.append({
                        "file": filepath,
                        "function": function_name,
                        "lines": lines_in_function,
                        "max_lines": max_lines
                    })
    except Exception as e:
        print_color(Color.RED, f"Error processing file {filepath}: {e}")
    return results

def main():
    parser = argparse.ArgumentParser(
        description="Find functions exceeding a specified line limit in TypeScript/JavaScript files."
    )
    parser.add_argument(
        "path",
        help="Path to the directory or file to analyze."
    )
    parser.add_argument(
        "--max-lines",
        type=int,
        default=40,
        help="Maximum allowed lines for a function. Default: 40."
    )

    args = parser.parse_args()

    all_results = []
    target_path = args.path

    if os.path.isfile(target_path):
        if target_path.endswith(('.ts', '.js', '.tsx', '.jsx')):
            all_results.extend(analyze_file(target_path, args.max_lines))
    elif os.path.isdir(target_path):
        for root, _, files in os.walk(target_path):
            for file in files:
                if file.endswith(('.ts', '.js', '.tsx', '.jsx')):
                    filepath = os.path.join(root, file)
                    all_results.extend(analyze_file(filepath, args.max_lines))
    else:
        print_color(Color.RED, f"Error: Path '{target_path}' is not a valid file or directory.")
        sys.exit(1)

    if all_results:
        print_color(Color.YELLOW, "\n--- Long Function Report ---")
        for res in all_results:
            print_color(Color.YELLOW, f"File: {res['file']}")
            print_color(Color.YELLOW, f"  Function: {res['function']}")
            print_color(Color.YELLOW, f"  Lines: {res['lines']} (Max: {res['max_lines']})")
        print_color(Color.RED, "\nOne or more functions exceed the maximum allowed line limit.")
        sys.exit(1)
    else:
        print_color(Color.GREEN, "\n--- Long Function Report ---")
        print_color(Color.GREEN, "No functions found exceeding the line limit.")

    sys.exit(0)

if __name__ == "__main__":
    main()
