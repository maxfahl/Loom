#!/usr/bin/env python3
"""
check_docstring_coverage.py

This script scans Python files in a given directory and reports on the percentage
of functions and classes that have docstrings, adhering to PEP 257.

Usage Examples:
    # Check docstring coverage in the current directory
    python check_docstring_coverage.py .

    # Check docstring coverage in 'src/' directory with verbose output
    python check_docstring_coverage.py src/ -v

    # Check docstring coverage and exclude a specific file
    python check_docstring_coverage.py . --exclude my_script.py
"""

import argparse
import ast
import os
import sys

try:
    from colorama import Fore, Style, init
    init(autoreset=True)
except ImportError:
    class Color:
        def __getattr__(self, name):
            return ''
    Fore = Color()
    Style = Color()

class DocstringAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.total_entities = 0
        self.documented_entities = 0
        self.undocumented_details = []
        self.current_file = None

    def _check_docstring(self, node):
        self.total_entities += 1
        if ast.get_docstring(node):
            self.documented_entities += 1
        else:
            self.undocumented_details.append(
                f"  - {node.name} (Line: {node.lineno}) in {self.current_file}"
            )

    def visit_FunctionDef(self, node):
        self._check_docstring(node)
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node):
        self._check_docstring(node)
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        self._check_docstring(node)
        self.generic_visit(node)

def main():
    parser = argparse.ArgumentParser(
        description="Check Python docstring coverage.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "path",
        help="The path to the directory to scan."
    )
    parser.add_argument(
        "--exclude",
        nargs='*',
        default=[],
        help="List of file or directory names to exclude from the scan."
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Show details of undocumented functions/classes."
    )

    args = parser.parse_args()
    target_path = args.path
    exclude_names = set(args.exclude)

    if not os.path.isdir(target_path):
        print(f"{Fore.RED}Error: Provided path '{target_path}' is not a valid directory.{Style.RESET_ALL}", file=sys.stderr)
        sys.exit(1)

    analyzer = DocstringAnalyzer()
    python_files = []

    for root, dirs, files in os.walk(target_path):
        # Filter out excluded directories
        dirs[:] = [d for d in dirs if d not in exclude_names]
        for file in files:
            if file.endswith(".py") and file not in exclude_names:
                python_files.append(os.path.join(root, file))

    if not python_files:
        print(f"{Fore.YELLOW}No Python files found in '{target_path}'.{Style.RESET_ALL}")
        sys.exit(0)

    print(f"{Fore.CYAN}Scanning {len(python_files)} Python files for docstrings...{Style.RESET_ALL}")

    for py_file in python_files:
        analyzer.current_file = py_file
        try:
            with open(py_file, "r", encoding="utf-8") as f:
                tree = ast.parse(f.read(), filename=py_file)
            analyzer.visit(tree)
        except Exception as e:
            print(f"{Fore.RED}Error parsing file '{py_file}': {e}{Style.RESET_ALL}", file=sys.stderr)

    total_found = analyzer.total_entities
    total_documented = analyzer.documented_entities
    undocumented_details = analyzer.undocumented_details

    if total_found == 0:
        print(f"{Fore.YELLOW}No functions or classes found to document in the scanned files.{Style.RESET_ALL}")
        sys.exit(0)

    coverage_percentage = (total_documented / total_found) * 100 if total_found > 0 else 0

    print(f"\n{Fore.CYAN}--- Docstring Coverage Report ---")
    print(f"Scanned files: {len(python_files)}")
    print(f"Total functions/classes found: {total_found}")
    print(f"Documented functions/classes: {total_documented}")
    print(f"Coverage: {coverage_percentage:.2f}%")

    if undocumented_details:
        print(f"{Fore.RED}Undocumented Entities:{Style.RESET_ALL}")
        if args.verbose:
            for detail in undocumented_details:
                print(detail)
        else:
            print(f"{Fore.YELLOW}  (Run with -v or --verbose to see details){Style.RESET_ALL}")
        sys.exit(1) # Indicate that undocumented entities were found
    else:
        print(f"{Fore.GREEN}All found functions and classes are documented!{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
