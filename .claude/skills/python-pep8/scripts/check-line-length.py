#!/usr/bin/env python3
# .devdev/skills/python-pep8/scripts/check-line-length.py

"""
Description:
This script identifies and reports lines exceeding the PEP 8 recommended length
(79 characters for code, 72 for comments/docstrings). It provides detailed
output including file, line number, current length, and the problematic line.

Usage:
  python3 check-line-length.py [OPTIONS] <PATH>

Options:
  -h, --help       Show this help message and exit.
  -c, --code-limit INT  Set custom code line length limit (default: 79).
  -d, --doc-limit INT   Set custom docstring/comment line length limit (default: 72).

Arguments:
  PATH             The path to a Python file or directory to process.

Requirements:
  - Python 3.6+

Example Usage:
  python3 check-line-length.py my_module.py
  python3 check-line-length.py --code-limit 100 src/
  python3 check-line-length.py -d 80 my_project/tests/
"""

import argparse
import os
import sys
import re

# --- Colors for output ---
RED = "\033[0;31m"
YELLOW = "\033[0;33m"
BLUE = "\033[0;34m"
NC = "\033[0m"  # No Color


def is_docstring_or_comment(line):
    """Checks if a line is likely part of a docstring or a comment."""
    # Simple heuristic: starts with # or is inside triple quotes
    # This is not perfect but covers most cases for line length checking
    return line.strip().startswith('#') or re.match(r'^\s*("""|''')', line.strip())


def check_file_line_lengths(filepath, code_limit, doc_limit):
    """Checks line lengths in a single Python file and reports violations."""
    violations = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f, 1):
                line_stripped = line.rstrip('\n')
                current_length = len(line_stripped)

                if is_docstring_or_comment(line_stripped):
                    if current_length > doc_limit:
                        violations.append({
                            'file': filepath,
                            'line_num': i,
                            'length': current_length,
                            'limit': doc_limit,
                            'type': 'docstring/comment',
                            'content': line_stripped
                        })
                else:
                    if current_length > code_limit:
                        violations.append({
                            'file': filepath,
                            'line_num': i,
                            'length': current_length,
                            'limit': code_limit,
                            'type': 'code',
                            'content': line_stripped
                        })
    except Exception as e:
        print(f"{RED}Error processing {filepath}: {e}{NC}", file=sys.stderr)
    return violations


def main():
    parser = argparse.ArgumentParser(
        description="Check Python file line lengths against PEP 8 guidelines."
    )
    parser.add_argument(
        "path",
        type=str,
        help="The path to a Python file or directory to process."
    )
    parser.add_argument(
        "-c", "--code-limit",
        type=int,
        default=79,
        help="Set custom code line length limit (default: 79)."
    )
    parser.add_argument(
        "-d", "--doc-limit",
        type=int,
        default=72,
        help="Set custom docstring/comment line length limit (default: 72)."
    )

    args = parser.parse_args()

    all_violations = []

    if os.path.isfile(args.path):
        all_violations.extend(check_file_line_lengths(args.path, args.code_limit, args.doc_limit))
    elif os.path.isdir(args.path):
        for root, _, files in os.walk(args.path):
            for file in files:
                if file.endswith('.py'):
                    filepath = os.path.join(root, file)
                    all_violations.extend(check_file_line_lengths(filepath, args.code_limit, args.doc_limit))
    else:
        print(f"{RED}Error: Path '{args.path}' is not a valid file or directory.{NC}", file=sys.stderr)
        sys.exit(1)

    if all_violations:
        print(f"{RED}\n--- Line Length Violations Found ({len(all_violations)}) ---"{NC})
        for v in all_violations:
            print(f"{YELLOW}{v['file']}:{v['line_num']}: {v['type'].capitalize()} line length ({v['length']}) exceeds limit ({v['limit']}){NC}")
            print(f"  {v['content']}")
        sys.exit(1)
    else:
        print(f"{BLUE}\n--- No Line Length Violations Found ---"{NC})


if __name__ == "__main__":
    main()
