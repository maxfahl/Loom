#!/usr/bin/env python3

"""
cyclomatic-complexity-analyzer.py

Description:
  A Python script that analyzes TypeScript/JavaScript files to calculate the cyclomatic
  complexity of functions. It helps identify overly complex functions that might be hard
  to understand, test, and maintain.

Usage:
  python3 cyclomatic-complexity-analyzer.py <path_to_directory_or_file> [--threshold N] [--output-format json|text]

Examples:
  python3 scripts/cyclomatic-complexity-analyzer.py src/
  python3 scripts/cyclomatic-complexity-analyzer.py src/utils/my_module.ts --threshold 10
  python3 scripts/cyclomatic-complexity-analyzer.py . --output-format json

Configuration Options:
  --threshold N: Report functions with complexity equal to or above this threshold. Default: 10.
  --output-format: 'text' (default) or 'json'.

Exit Codes:
  0: No functions exceed the complexity threshold or analysis completed successfully.
  1: One or more functions exceed the complexity threshold.
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

def calculate_cyclomatic_complexity(function_code: str) -> int:
    # Basic calculation: 1 + number of decision points
    complexity = 1
    # Keywords that indicate decision points
    keywords = ['if', 'for', 'while', 'case', 'catch', '&& ', '|| ', '?:']

    for keyword in keywords:
        complexity += len(re.findall(r'\b' + re.escape(keyword) + r'\b', function_code))

    return complexity

def analyze_file(filepath: str, threshold: int) -> list:
    results = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Regex to find functions/methods in TypeScript/JavaScript
        # This is a simplified regex and might not catch all cases, but covers common ones.
        # It tries to capture function name and its body.
        function_pattern = re.compile(
            r'(?:(?:export|public|private|protected|static|async)\s+)*'  # Modifiers
            r'(?:function\s+([a-zA-Z_][a-zA-Z0-9_]*)|([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*(?:function|\()|([a-zA-Z_][a-zA-Z0-9_]*):\s*(?:function|\()|([a-zA-Z_][a-zA-Z0-9_]*)\s*\()' # Function declarations, arrow functions, object methods
            r'(?:[^;{{]*)' # Arguments and return types
            r'\{([^{{}}]*(?:\{{[^{{}}]*\}}[^\{{}}]*)*)\}', # Function body (basic brace matching)
            re.DOTALL
        )

        for match in function_pattern.finditer(content):
            # Prioritize named function, then arrow function name, then object method name
            function_name = match.group(1) or match.group(2) or match.group(3) or match.group(4)
            function_body = match.group(5)

            if function_name and function_body:
                complexity = calculate_cyclomatic_complexity(function_body)
                if complexity >= threshold:
                    results.append({
                        "file": filepath,
                        "function": function_name,
                        "complexity": complexity,
                        "threshold": threshold
                    })
    except Exception as e:
        print_color(Color.RED, f"Error processing file {filepath}: {e}")
    return results

def main():
    parser = argparse.ArgumentParser(
        description="Analyze cyclomatic complexity of functions in TypeScript/JavaScript files."
    )
    parser.add_argument(
        "path",
        help="Path to the directory or file to analyze."
    )
    parser.add_argument(
        "--threshold",
        type=int,
        default=10,
        help="Report functions with complexity equal to or above this threshold. Default: 10."
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
            all_results.extend(analyze_file(target_path, args.threshold))
    elif os.path.isdir(target_path):
        for root, _, files in os.walk(target_path):
            for file in files:
                if file.endswith(('.ts', '.js', '.tsx', '.jsx')):
                    filepath = os.path.join(root, file)
                    all_results.extend(analyze_file(filepath, args.threshold))
    else:
        print_color(Color.RED, f"Error: Path '{target_path}' is not a valid file or directory.")
        sys.exit(1)

    if args.output_format == 'json':
        print(json.dumps(all_results, indent=2))
    else:
        if all_results:
            print_color(Color.YELLOW, "\n--- Cyclomatic Complexity Analysis Results ---")
            for res in all_results:
                print_color(Color.YELLOW, f"File: {res['file']}")
                print_color(Color.YELLOW, f"  Function: {res['function']}")
                print_color(Color.YELLOW, f"  Complexity: {res['complexity']} (Threshold: {res['threshold']})")
            print_color(Color.RED, "\nOne or more functions exceed the cyclomatic complexity threshold.")
            sys.exit(1)
        else:
            print_color(Color.GREEN, "\n--- Cyclomatic Complexity Analysis Results ---")
            print_color(Color.GREEN, "No functions found exceeding the complexity threshold.")

    sys.exit(0)

if __name__ == "__main__":
    main()
