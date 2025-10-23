#!/usr/bin/env python3

"""
ocp-analyzer.py

Description:
  A Python script that scans TypeScript/JavaScript files for patterns indicative
  of Open/Closed Principle (OCP) violations, such as long `if/else if` chains
  or `switch` statements that dispatch logic based on type. These often suggest
  that new functionality requires modifying existing code.

Usage:
  python3 ocp-analyzer.py <path_to_directory_or_file> [--min-branches N] [--output-format json|text]

Examples:
  python3 scripts/ocp-analyzer.py src/
  python3 scripts/ocp-analyzer.py src/utils/Processor.ts --min-branches 3
  python3 scripts/ocp-analyzer.py . --output-format json

Configuration Options:
  --min-branches N: Minimum number of branches in an if/else if chain or switch statement
                    to be flagged as a potential OCP violation. Default: 3.
  --output-format: 'text' (default) or 'json'.

Exit Codes:
  0: No potential OCP violations found or analysis completed successfully.
  1: One or more potential OCP violations found.
"""

import argparse
import os
import re
import json
import sys

class Color:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[0;33m'
    BLUE = '\033[0;34m'
    NC = '\033[0m' # No Color

def print_color(color, message):
    print(f"{color}{message}{Color.NC}")

def analyze_file(filepath: str, min_branches: int) -> list:
    results = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Regex to find if/else if chains
        # This looks for 'if (...) {' followed by 'else if (...) {' multiple times
        if_else_if_pattern = re.compile(r'if\s*\([^)]*\)\s*\{[^}]*\}(?:\s*else\s+if\s*\([^)]*\)\s*\{[^}]*\}){\s*' + str(min_branches - 1) + r',}', re.DOTALL)

        # Regex to find switch statements with multiple cases
        switch_pattern = re.compile(r'switch\s*\([^)]*\)\s*\{[^}]*(?:case\s+[^:]*:\s*[^}]*){' + str(min_branches) + r'}[^}]*\}', re.DOTALL)

        # Find if/else if chains
        for match in if_else_if_pattern.finditer(content):
            start_line = content.count('\n', 0, match.start()) + 1
            results.append({
                "file": filepath,
                "type": "if/else if chain",
                "line": start_line,
                "snippet": match.group(0).splitlines()[0] + "...",
                "reason": f"Potential OCP violation: long if/else if chain with >= {min_branches} branches."
            })

        # Find switch statements
        for match in switch_pattern.finditer(content):
            start_line = content.count('\n', 0, match.start()) + 1
            results.append({
                "file": filepath,
                "type": "switch statement",
                "line": start_line,
                "snippet": match.group(0).splitlines()[0] + "...",
                "reason": f"Potential OCP violation: switch statement with >= {min_branches} cases."
            })

    except Exception as e:
        print_color(Color.RED, f"Error processing file {filepath}: {e}")
    return results

def main():
    parser = argparse.ArgumentParser(
        description="Detect potential OCP violations in TypeScript/JavaScript files."
    )
    parser.add_argument(
        "path",
        help="Path to the directory or file to analyze."
    )
    parser.add_argument(
        "--min-branches",
        type=int,
        default=3,
        help="Minimum number of branches in an if/else if chain or switch statement to be flagged. Default: 3."
    )
    parser.add_argument(
        "--output-format",
        choices=['text', 'json'],
        default='text',
        help="Output format: 'text' (default) or 'json'."
    )

    args = parser.parse_args()

    all_results = []
    target_path = args.path

    if os.path.isfile(target_path):
        if target_path.endswith(('.ts', '.js', '.tsx', '.jsx')):
            all_results.extend(analyze_file(target_path, args.min_branches))
    elif os.path.isdir(target_path):
        for root, _, files in os.walk(target_path):
            for file in files:
                if file.endswith(('.ts', '.js', '.tsx', '.jsx')):
                    filepath = os.path.join(root, file)
                    all_results.extend(analyze_file(filepath, args.min_branches))
    else:
        print_color(Color.RED, f"Error: Path '{target_path}' is not a valid file or directory.")
        sys.exit(1)

    if args.output_format == 'json':
        print(json.dumps(all_results, indent=2))
    else:
        if all_results:
            print_color(Color.YELLOW, "\n--- Potential OCP Violations Detected ---")
            for res in all_results:
                print_color(Color.YELLOW, f"File: {res['file']}:L{res['line']}")
                print_color(Color.YELLOW, f"  Type: {res['type']}")
                print_color(Color.YELLOW, f"  Reason: {res['reason']}")
                print_color(Color.YELLOW, f"  Snippet: {res['snippet']}")
            print_color(Color.RED, "\nConsider refactoring these constructs to adhere to the Open/Closed Principle (e.g., using polymorphism).")
            sys.exit(1)
        else:
            print_color(Color.GREEN, "\n--- OCP Analysis ---")
            print_color(Color.GREEN, "No potential OCP violations found based on if/switch statements.")

    sys.exit(0)

if __name__ == "__main__":
    main()
