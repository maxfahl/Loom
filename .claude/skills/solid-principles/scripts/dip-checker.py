#!/usr/bin/env python3

"""
dip-checker.py

Description:
  A Python script that identifies potential Dependency Inversion Principle (DIP)
  violations in TypeScript/JavaScript code. It looks for direct instantiations
  of concrete classes within high-level modules, suggesting a dependency on
  details rather than abstractions.

Usage:
  python3 dip-checker.py <path_to_directory_or_file> [--exclude-patterns "new RegExp,new Map"] [--output-format json|text]

Examples:
  python3 scripts/dip-checker.py src/
  python3 scripts/dip-checker.py src/services/ --exclude-patterns "new Date,new Error"
  python3 scripts/dip-checker.py . --output-format json

Configuration Options:
  --exclude-patterns "pattern1,pattern2": Comma-separated list of patterns to ignore
                                         when detecting 'new' instantiations (e.g., "new Date", "new Map").
  --output-format: 'text' (default) or 'json'.

Exit Codes:
  0: No potential DIP violations found or analysis completed successfully.
  1: One or more potential DIP violations found.
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

def analyze_file(filepath: str, exclude_patterns: list) -> list:
    results = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Regex to find 'new ClassName()' instantiations
        # This is a heuristic and might have false positives (e.g., new Date(), new Error()).
        # It tries to capture the class name being instantiated.
        new_instantiation_pattern = re.compile(r'new\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*
')

        for line_num, line in enumerate(content.splitlines(), 1):
            for match in new_instantiation_pattern.finditer(line):
                class_name = match.group(1)
                full_match = match.group(0)

                # Check against exclude patterns
                is_excluded = False
                for pattern in exclude_patterns:
                    if pattern in full_match:
                        is_excluded = True
                        break
                
                if not is_excluded:
                    results.append({
                        "file": filepath,
                        "line": line_num,
                        "instantiation": full_match.strip(),
                        "class_name": class_name,
                        "reason": "Direct instantiation of a concrete class. Consider depending on an abstraction instead."
                    })
    except Exception as e:
        print_color(Color.RED, f"Error processing file {filepath}: {e}")
    return results

def main():
    parser = argparse.ArgumentParser(
        description="Detect potential DIP violations in TypeScript/JavaScript files."
    )
    parser.add_argument(
        "path",
        help="Path to the directory or file to analyze."
    )
    parser.add_argument(
        "--exclude-patterns",
        type=str,
        default="new Date,new Error,new RegExp,new Map,new Set,new Promise",
        help="Comma-separated list of patterns to ignore (e.g., \"new Date,new Error\"). Default: new Date,new Error,new RegExp,new Map,new Set,new Promise"
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
    exclude_patterns_list = [p.strip() for p in args.exclude_patterns.split(',') if p.strip()]

    if os.path.isfile(target_path):
        if target_path.endswith(('.ts', '.js', '.tsx', '.jsx')):
            all_results.extend(analyze_file(target_path, exclude_patterns_list))
    elif os.path.isdir(target_path):
        for root, _, files in os.walk(target_path):
            for file in files:
                if file.endswith(('.ts', '.js', '.tsx', '.jsx')):
                    filepath = os.path.join(root, file)
                    all_results.extend(analyze_file(filepath, exclude_patterns_list))
    else:
        print_color(Color.RED, f"Error: Path '{target_path}' is not a valid file or directory.")
        sys.exit(1)

    if all_results:
        print_color(Color.YELLOW, "\n--- Potential DIP Violations Detected ---")
        for res in all_results:
            print_color(Color.YELLOW, f"File: {res['file']}:L{res['line']}")
            print_color(Color.YELLOW, f"  Instantiation: {res['instantiation']}")
            print_color(Color.YELLOW, f"  Reason: {res['reason']}")
        print_color(Color.RED, "\nConsider using dependency injection or factories to depend on abstractions.")
        sys.exit(1)
    else:
        print_color(Color.GREEN, "\n--- DIP Analysis ---")
        print_color(Color.GREEN, "No potential DIP violations found based on direct instantiations.")

    sys.exit(0)

if __name__ == "__main__":
    main()
