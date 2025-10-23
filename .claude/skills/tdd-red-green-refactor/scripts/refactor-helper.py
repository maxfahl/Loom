#!/usr/bin/env python3

# refactor-helper.py
# Description: Analyzes Python code for common refactoring opportunities,
#              such as functions exceeding a specified line count.
# Usage: python3 refactor-helper.py [project_root_dir] [--max-lines <count>]
#        If project_root_dir is not provided, it analyzes the current directory.

import os
import argparse
import ast
from typing import List, Tuple

# --- Configuration Variables ---
COLOR_RESET = "\033[0m"
COLOR_RED = "\033[0;31m"
COLOR_GREEN = "\033[0;32m"
COLOR_YELLOW = "\033[0;33m"
COLOR_BLUE = "\033[0;34m"
COLOR_CYAN = "\033[0;36m"

DEFAULT_MAX_FUNCTION_LINES = 30

# --- Helper Functions ---
def log_info(message: str):
    print(f"{COLOR_BLUE}[INFO]{COLOR_RESET} {message}")

def log_warning(message: str):
    print(f"{COLOR_YELLOW}[WARNING]{COLOR_RESET} {message}")

def log_error(message: str):
    print(f"{COLOR_RED}[ERROR]{COLOR_RESET} {message}")

def log_success(message: str):
    print(f"{COLOR_GREEN}[SUCCESS]{COLOR_RESET} {message}")

def find_py_files(root_dir: str, exclude_dirs: List[str]) -> List[str]:
    py_files = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Modify dirnames in-place to skip excluded directories
        dirnames[:] = [d for d in dirnames if d not in exclude_dirs]

        for f in filenames:
            if f.endswith('.py'):
                py_files.append(os.path.join(dirpath, f))
    return py_files

class FunctionLengthAnalyzer(ast.NodeVisitor):
    def __init__(self, max_lines: int):
        self.max_lines = max_lines
        self.long_functions: List[Tuple[str, int, int]] = [] # (function_name, start_line, line_count)

    def visit_FunctionDef(self, node: ast.FunctionDef):
        self._check_function_length(node)
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        self._check_function_length(node)
        self.generic_visit(node)

    def _check_function_length(self, node: Any):
        # Calculate the number of lines in the function body
        # This is a simplified approach; it counts lines from the start of the function
        # to the end of its last statement.
        # A more robust solution might involve parsing the source code lines directly.
        start_line = node.lineno
        end_line = node.body[-1].lineno if node.body else start_line
        line_count = end_line - start_line + 1

        if line_count > self.max_lines:
            self.long_functions.append((node.name, start_line, line_count))

def main():
    parser = argparse.ArgumentParser(
        description="Analyze Python project for refactoring opportunities (e.g., long functions)."
    )
    parser.add_argument(
        "project_root_dir",
        nargs="?",
        default=".",
        help="Root directory of the Python project (default: current directory)"
    )
    parser.add_argument(
        "--max-lines",
        type=int,
        default=DEFAULT_MAX_FUNCTION_LINES,
        help=f"Maximum allowed lines for a function (default: {DEFAULT_MAX_FUNCTION_LINES})"
    )
    args = parser.parse_args()

    project_root_dir = os.path.abspath(args.project_root_dir)
    max_lines = args.max_lines

    if not os.path.isdir(project_root_dir):
        log_error(f"Project root directory not found: {project_root_dir}")
        return

    log_info(f"Starting refactoring analysis for: {project_root_dir}")
    log_info(f"Flagging functions longer than {max_lines} lines.")

    exclude_dirs = ["venv", ".venv", "node_modules", "dist", ".git", "__pycache__"]
    py_files = find_py_files(project_root_dir, exclude_dirs)

    if not py_files:
        log_warning("No Python files found for analysis.")
        return

    total_long_functions = 0
    for py_file in py_files:
        try:
            with open(py_file, 'r', encoding='utf-8') as f:
                tree = ast.parse(f.read(), filename=py_file)
            analyzer = FunctionLengthAnalyzer(max_lines)
            analyzer.visit(tree)

            if analyzer.long_functions:
                log_warning(f"Found long functions in {os.path.relpath(py_file, project_root_dir)}:")
                for func_name, start_line, line_count in analyzer.long_functions:
                    print(f"  {COLOR_CYAN}Line {start_line}:{COLOR_RESET} Function '{func_name}' has {line_count} lines (>{max_lines}).")
                    total_long_functions += 1
        except SyntaxError as e:
            log_error(f"Syntax error in {py_file} at line {e.lineno}: {e.msg}")
        except Exception as e:
            log_error(f"Error processing {py_file}: {e}")

    if total_long_functions == 0:
        log_success("No functions exceeding the line limit found. Good job!")
    else:
        log_warning(f"Analysis complete. Found {total_long_functions} functions that could be refactored.")
        log_info("Consider breaking down these functions into smaller, more focused units.")

    log_success("Refactoring analysis complete.")

if __name__ == "__main__":
    main()
