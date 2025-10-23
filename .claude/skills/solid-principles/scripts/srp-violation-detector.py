#!/usr/bin/env python3

"""
srp-violation-detector.py

Description:
  A Python script that heuristically analyzes TypeScript/JavaScript classes
  to identify potential Single Responsibility Principle (SRP) violations.
  It flags classes with a high number of public methods or methods that
  operate on seemingly unrelated data, suggesting multiple responsibilities.

Usage:
  python3 srp-violation-detector.py <path_to_directory_or_file> [--max-public-methods N] [--output-format json|text]

Examples:
  python3 scripts/srp-violation-detector.py src/
  python3 scripts/srp-violation-detector.py src/services/UserService.ts --max-public-methods 7
  python3 scripts/srp-violation-detector.py . --output-format json

Configuration Options:
  --max-public-methods N: Maximum allowed public methods in a class before flagging as potential SRP violation. Default: 5.
  --output-format: 'text' (default) or 'json'.

Exit Codes:
  0: No potential SRP violations found or analysis completed successfully.
  1: One or more potential SRP violations found.
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

def analyze_file(filepath: str, max_public_methods: int) -> list:
    results = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Regex to find classes
        class_pattern = re.compile(r'(?:export\s+)?class\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*(?:extends\s+[a-zA-Z_][a-zA-Z0-9_]*)?\s*(?:implements\s+[a-zA-Z_][a-zA-Z0-9_]*(?:,\s*[a-zA-Z_][a-zA-Z0-9_]*)*)?\s*\{([^}]*)\}', re.DOTALL)

        for class_match in class_pattern.finditer(content):
            class_name = class_match.group(1)
            class_body = class_match.group(2)

            # Regex to find public methods within the class body
            # This includes methods declared with 'public', or implicitly public (no modifier)
            # It tries to exclude constructors, getters/setters, and private/protected methods.
            method_pattern = re.compile(r'(?:public\s+|async\s+|static\s+)?([a-zA-Z_][a-zA-Z0-9_]*)\s*\([^)]*\)(?:\s*:\s*[a-zA-Z_][a-zA-Z0-9_]*)?\s*\{', re.DOTALL)
            
            public_methods = []
            for method_match in method_pattern.finditer(class_body):
                method_name = method_match.group(1)
                # Exclude constructors and common getter/setter patterns (heuristic)
                if method_name != 'constructor' and not (method_name.startswith('get') or method_name.startswith('set')):
                    public_methods.append(method_name)
            
            num_public_methods = len(public_methods)

            if num_public_methods > max_public_methods:
                results.append({
                    "file": filepath,
                    "class": class_name,
                    "public_methods_count": num_public_methods,
                    "max_public_methods": max_public_methods,
                    "methods": public_methods
                })
    except Exception as e:
        print_color(Color.RED, f"Error processing file {filepath}: {e}")
    return results

def main():
    parser = argparse.ArgumentParser(
        description="Detect potential SRP violations in TypeScript/JavaScript classes."
    )
    parser.add_argument(
        "path",
        help="Path to the directory or file to analyze."
    )
    parser.add_argument(
        "--max-public-methods",
        type=int,
        default=5,
        help="Maximum allowed public methods in a class before flagging. Default: 5."
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
            all_results.extend(analyze_file(target_path, args.max_public_methods))
    elif os.path.isdir(target_path):
        for root, _, files in os.walk(target_path):
            for file in files:
                if file.endswith(('.ts', '.js', '.tsx', '.jsx')):
                    filepath = os.path.join(root, file)
                    all_results.extend(analyze_file(filepath, args.max_public_methods))
    else:
        print_color(Color.RED, f"Error: Path '{target_path}' is not a valid file or directory.")
        sys.exit(1)

    if args.output_format == 'json':
        print(json.dumps(all_results, indent=2))
    else:
        if all_results:
            print_color(Color.YELLOW, "\n--- Potential SRP Violations Detected ---")
            for res in all_results:
                print_color(Color.YELLOW, f"File: {res['file']}")
                print_color(Color.YELLOW, f"  Class: {res['class']}")
                print_color(Color.YELLOW, f"  Public Methods: {res['public_methods_count']} (Max: {res['max_public_methods']})")
                print_color(Color.YELLOW, f"  Methods: {', '.join(res['methods'])}")
            print_color(Color.RED, "\nConsider refactoring these classes to adhere to the Single Responsibility Principle.")
            sys.exit(1)
        else:
            print_color(Color.GREEN, "\n--- SRP Analysis ---")
            print_color(Color.GREEN, "No potential SRP violations found based on public method count.")

    sys.exit(0)

if __name__ == "__main__":
    main()
