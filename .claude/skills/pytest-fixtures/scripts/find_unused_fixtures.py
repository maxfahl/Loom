#!/usr/bin/env python3
"""
find_unused_fixtures.py

This script scans a specified test directory to identify and list pytest fixtures
that are defined but never used within the test suite.

Usage Examples:
    # Find unused fixtures in the current directory
    python find_unused_fixtures.py .

    # Find unused fixtures in a specific test directory
    python find_unused_fixtures.py tests/

    # Find unused fixtures and output to a file
    python find_unused_fixtures.py tests/ > unused_fixtures.txt
"""

import argparse
import os
import ast
import sys
from collections import defaultdict

try:
    from colorama import Fore, Style, init
    init(autoreset=True)
except ImportError:
    class Color:
        def __getattr__(self, name):
            return ''
    Fore = Color()
    Style = Color()

class FixtureAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.defined_fixtures = defaultdict(list)  # {fixture_name: [(file_path, line_num)]}
        self.used_fixtures = defaultdict(list)     # {fixture_name: [(file_path, line_num)]}
        self.current_file = None

    def visit_FunctionDef(self, node):
        # Check for @pytest.fixture decorator
        for decorator in node.decorator_list:
            if isinstance(decorator, ast.Call) and isinstance(decorator.func, ast.Attribute):
                if decorator.func.attr == 'fixture' and getattr(decorator.func.value, 'id', '') == 'pytest':
                    self.defined_fixtures[node.name].append((self.current_file, node.lineno))
            elif isinstance(decorator, ast.Name) and decorator.id == 'fixture': # Handles `from pytest import fixture`
                 self.defined_fixtures[node.name].append((self.current_file, node.lineno))

        # Check for fixture usage in function arguments
        for arg in node.args.args:
            self.used_fixtures[arg.arg].append((self.current_file, node.lineno))

        self.generic_visit(node)

    def analyze_file(self, file_path):
        self.current_file = file_path
        with open(file_path, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read(), filename=file_path)
        self.visit(tree)

    def get_unused_fixtures(self):
        unused = {}
        for fixture_name, definitions in self.defined_fixtures.items():
            if fixture_name not in self.used_fixtures:
                unused[fixture_name] = definitions
        return unused

def main():
    parser = argparse.ArgumentParser(
        description="Find unused pytest fixtures in a test directory."
    )
    parser.add_argument(
        "path",
        help="The path to the test directory to scan (e.g., './tests' or '.')."
    )

    args = parser.parse_args()
    target_path = args.path

    if not os.path.isdir(target_path):
        print(f"{Fore.RED}Error: Provided path '{target_path}' is not a valid directory.{Style.RESET_ALL}", file=sys.stderr)
        sys.exit(1)

    analyzer = FixtureAnalyzer()
    python_files = []

    for root, _, files in os.walk(target_path):
        for file in files:
            if file.endswith(".py") and (file.startswith("test_") or file == "conftest.py"):
                python_files.append(os.path.join(root, file))

    if not python_files:
        print(f"{Fore.YELLOW}No Python test files found in '{target_path}'.{Style.RESET_ALL}")
        sys.exit(0)

    print(f"{Fore.CYAN}Scanning {len(python_files)} Python files for fixtures...{Style.RESET_ALL}")

    for py_file in python_files:
        try:
            analyzer.analyze_file(py_file)
        except Exception as e:
            print(f"{Fore.RED}Error parsing file '{py_file}': {e}{Style.RESET_ALL}", file=sys.stderr)

    unused_fixtures = analyzer.get_unused_fixtures()

    if unused_fixtures:
        print(f"\n{Fore.RED}--- UNUSED PYTEST FIXTURES FOUND ---")
        for fixture_name, definitions in unused_fixtures.items():
            print(f"{Fore.YELLOW}Fixture: {fixture_name}{Style.RESET_ALL}")
            for file_path, line_num in definitions:
                print(f"  Defined in: {file_path}:{line_num}")
        print(f"{Fore.RED}------------------------------------{Style.RESET_ALL}")
        sys.exit(1) # Indicate that unused fixtures were found
    else:
        print(f"\n{Fore.GREEN}No unused pytest fixtures found in '{target_path}'.{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
