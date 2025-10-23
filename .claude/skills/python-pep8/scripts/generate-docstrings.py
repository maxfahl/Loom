#!/usr/bin/env python3
# .devdev/skills/python-pep8/scripts/generate-docstrings.py

"""
Description:
This script scans a specified Python file or directory for functions and classes
lacking docstrings and generates basic PEP 257 compliant docstring stubs.
This helps developers quickly add documentation.

Usage:
  python3 generate-docstrings.py [OPTIONS] <PATH>

Options:
  -h, --help       Show this help message and exit.
  -d, --dry-run    Perform a dry run; show what would be changed without writing to files.
  -f, --force      Overwrite existing empty docstrings.

Arguments:
  PATH             The path to a Python file or directory to process.

Requirements:
  - Python 3.6+

Example Usage:
  python3 generate-docstrings.py my_module.py
  python3 generate-docstrings.py --dry-run my_project/
  python3 generate-docstrings.py -f src/api.py
"""

import argparse
import ast
import os
import sys

# --- Colors for output ---
GREEN = "\033[0;32m"
YELLOW = "\033[0;33m"
RED = "\033[0;31m"
BLUE = "\033[0;34m"
NC = "\033[0m"  # No Color


class DocstringGenerator(ast.NodeVisitor):
    """AST visitor to find functions/classes and generate docstrings."""

    def __init__(self, content, force_overwrite=False):
        self.content = content.splitlines(keepends=True)
        self.new_content = list(self.content)
        self.changes_made = False
        self.force_overwrite = force_overwrite

    def _insert_docstring(self, node, indent_level, name, node_type):
        # Check if a docstring already exists
        if (isinstance(node.body[0], ast.Expr) and
                isinstance(node.body[0].value, ast.Constant) and
                isinstance(node.body[0].value.value, str)):
            existing_docstring = node.body[0].value.value.strip()
            if existing_docstring and not self.force_overwrite:
                print(f"{YELLOW}Skipping existing docstring for {node_type} '{name}'. Use --force to overwrite empty ones.{NC}")
                return

        # Determine insertion point
        insert_line = node.body[0].lineno if node.body else node.lineno + 1
        indent = " " * indent_level * 4

        docstring_lines = [
            f'{indent}"""Summary of {name}.',  # Single line summary
            f'{indent}'''',  # Blank line
        ]

        if node_type == "function":
            args = []
            if isinstance(node.args, ast.arguments):
                for arg in node.args.posonlyargs:
                    args.append(arg.arg)
                for arg in node.args.args:
                    if arg.arg != 'self' and arg.arg != 'cls':
                        args.append(arg.arg)
                for arg in node.args.kwonlyargs:
                    args.append(arg.arg)

            if args:
                docstring_lines.append(f'{indent}Args:')
                for arg in args:
                    docstring_lines.append(f'{indent}    {arg} (type): Description of {arg}.')

            if node.returns:
                docstring_lines.append(f'{indent}Returns:')
                docstring_lines.append(f'{indent}    type: Description of return value.')

        elif node_type == "class":
            # For classes, we might want to add Attributes section
            docstring_lines.append(f'{indent}Attributes:')
            docstring_lines.append(f'{indent}    attr (type): Description of attr.')

        docstring_lines.append(f'{indent}"""')

        # Insert docstring lines into new_content
        # Adjust line numbers for insertion
        current_line_index = insert_line
        for i, line in enumerate(docstring_lines):
            self.new_content.insert(current_line_index + i, line + "\n")
        self.changes_made = True
        print(f"{GREEN}Generated docstring for {node_type} '{name}' at line {insert_line}.{NC}")

    def visit_FunctionDef(self, node):
        # Calculate indentation level based on the function's column offset
        indent_level = node.col_offset // 4
        self._insert_docstring(node, indent_level, node.name, "function")
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node):
        indent_level = node.col_offset // 4
        self._insert_docstring(node, indent_level, node.name, "function")
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        indent_level = node.col_offset // 4
        self._insert_docstring(node, indent_level, node.name, "class")
        self.generic_visit(node)


def process_file(filepath, dry_run, force_overwrite):
    """Processes a single Python file to generate missing docstrings."""
    print(f"{BLUE}Processing file: {filepath}{NC}")
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        tree = ast.parse(content)

        generator = DocstringGenerator(content, force_overwrite)
        generator.visit(tree)

        if generator.changes_made:
            if dry_run:
                print(f"{YELLOW}Dry run: Changes would be applied to {filepath}{NC}")
                # For dry run, print the diff or new content for review
                # This is a simplified diff, a real diff would be more complex
                print("--- Original ---")
                for line in generator.content:
                    sys.stdout.write(line)
                print("\n--- Proposed ---")
                for line in generator.new_content:
                    sys.stdout.write(line)
                print("----------------\n")
            else:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.writelines(generator.new_content)
                print(f"{GREEN}Docstrings generated and saved to {filepath}{NC}")
        else:
            print(f"{YELLOW}No docstrings generated for {filepath}{NC}")

    except SyntaxError as e:
        print(f"{RED}Error: Syntax error in {filepath}: {e}{NC}", file=sys.stderr)
    except Exception as e:
        print(f"{RED}Error processing {filepath}: {e}{NC}", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(
        description="Generate PEP 257 docstring stubs for Python functions and classes."
    )
    parser.add_argument(
        "path",
        type=str,
        help="The path to a Python file or directory to process."
    )
    parser.add_argument(
        "-d", "--dry-run",
        action="store_true",
        help="Perform a dry run; show what would be changed without writing to files."
    )
    parser.add_argument(
        "-f", "--force",
        action="store_true",
        help="Overwrite existing empty docstrings."
    )

    args = parser.parse_args()

    if os.path.isfile(args.path):
        process_file(args.path, args.dry_run, args.force)
    elif os.path.isdir(args.path):
        for root, _, files in os.walk(args.path):
            for file in files:
                if file.endswith('.py'):
                    filepath = os.path.join(root, file)
                    process_file(filepath, args.dry_run, args.force)
    else:
        print(f"{RED}Error: Path '{args.path}' is not a valid file or directory.{NC}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
