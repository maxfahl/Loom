#!/usr/bin/env python3

# query-key-linter.py
#
# Purpose: A linter for TanStack Query keys in TypeScript files. It scans for common
#          anti-patterns and enforces best practices such as using `as const` for
#          type inference, hierarchical structuring, and adherence to naming conventions.
#          This helps prevent common invalidation bugs and improves type safety.
#
# Usage:
#   python3 query-key-linter.py [--path <directory>] [--fix] [--verbose]
#
# Examples:
#   python3 query-key-linter.py
#   python3 query-key-linter.py --path src/features --fix
#   python3 query-key-linter.py --verbose
#
# Options:
#   --path       Optional: Directory to scan (default: current working directory).
#   --fix        Optional: Attempt to automatically fix some issues (e.g., add `as const`).
#   --verbose    Optional: Enable verbose output.
#   --help       Display this help message.

import argparse
import os
import re
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

def lint_file(filepath, fix_mode, verbose_mode):
    """Lints a single TypeScript file for TanStack Query key best practices."""
    violations = []
    fixed_content = []
    file_changed = False

    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        original_line = line
        # Rule 1: Ensure query keys defined as arrays use 'as const'
        # Matches patterns like: `['todos']`, `['todos', id]`
        match_array_key = re.search(r'(\[.*?\])(?!\s*as\s+const)', line)
        if match_array_key:
            array_key_str = match_array_key.group(1)
            if "queryKey" in line or "queryKeys" in line: # Only flag if it's likely a query key definition
                violation_msg = f"L{i+1}: Query key array '{array_key_str}' should use 'as const' for type inference."
                violations.append(violation_msg)
                if fix_mode:
                    new_line = line.replace(array_key_str, f"{array_key_str} as const", 1)
                    if new_line != line:
                        line = new_line
                        file_changed = True
                        if verbose_mode:
                            colored_print(f"  FIXED: {violation_msg}", "green")

        # Rule 2: Encourage hierarchical keys (simple string keys are often less flexible)
        # This is more of a suggestion, harder to auto-fix without context.
        # We'll look for `queryKey: 'someString'`
        match_simple_string_key = re.search(r'queryKey:\s*(\'|\\").*?(\'|\\")', line)
        if match_simple_string_key:
            key_str = match_simple_string_key.group(0)
            violation_msg = f"L{i+1}: Consider using hierarchical array for query key '{key_str}' for better invalidation control."
            violations.append(violation_msg)


        fixed_content.append(line)

    if file_changed and fix_mode:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(fixed_content)
        if verbose_mode:
            colored_print(f"File '{filepath}' was modified.", "yellow")

    return violations

def main():
    parser = argparse.ArgumentParser(
        description="Linter for TanStack Query keys in TypeScript files.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "--path",
        default=".",
        help="Directory to scan (default: current working directory)."
    )
    parser.add_argument(
        "--fix",
        action="store_true",
        help="Attempt to automatically fix some issues (e.g., add `as const`)."
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose output."
    )

    args = parser.parse_args()

    scan_path = args.path
    fix_mode = args.fix
    verbose_mode = args.verbose

    colored_print(f"\n--- TanStack Query Key Linter ---", "blue")
    colored_print(f"Scanning path: {os.path.abspath(scan_path)}", "cyan")
    colored_print(f"Fix mode: {fix_mode}", "cyan")

    total_violations = 0
    scanned_files = 0

    for root, _, files in os.walk(scan_path):
        for file in files:
            if file.endswith((".ts", ".tsx")):
                filepath = os.path.join(root, file)
                scanned_files += 1
                if verbose_mode:
                    colored_print(f"  Scanning: {filepath}", "white")
                file_violations = lint_file(filepath, fix_mode, verbose_mode)
                if file_violations:
                    colored_print(f"Violations found in {filepath}:", "red")
                    for violation in file_violations:
                        colored_print(f"  - {violation}", "red")
                    total_violations += len(file_violations)

    colored_print(f"\n--- Linter Summary ---", "blue")
    colored_print(f"Scanned {scanned_files} TypeScript files.", "cyan")

    if total_violations > 0:
        colored_print(f"Found {total_violations} total violations.", "red")
        if fix_mode:
            colored_print("Some violations might have been automatically fixed.", "yellow")
        sys.exit(1)
    else:
        colored_print("No TanStack Query key violations found. Good job!", "green")
        sys.exit(0)

if __name__ == "__main__":
    main()
