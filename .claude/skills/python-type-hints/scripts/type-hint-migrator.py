#!/usr/bin/env python3

# type-hint-migrator.py
# Description: Analyzes a Python project for missing type hints and suggests additions.
# Usage: python3 type-hint-migrator.py [project_root_dir]
#        If project_root_dir is not provided, it analyzes the current directory.

import os
import re
import argparse
import ast
from typing import List, Tuple, Dict, Any

# --- Configuration Variables ---
COLOR_RESET = "\033[0m"
COLOR_RED = "\033[0;31m"
COLOR_GREEN = "\033[0;32m"
COLOR_YELLOW = "\033[0;33m"
COLOR_BLUE = "\033[0;34m"
COLOR_CYAN = "\033[0;36m"

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

class TypeHintAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.violations: List[Tuple[int, str, str]] = []

    def visit_FunctionDef(self, node: ast.FunctionDef):
        # Check return type hint
        if node.returns is None:
            self.violations.append((node.lineno, "Missing return type hint",
                                     f"Suggestion: Add `-> Any` or a more specific type to function `{node.name}`."))

        # Check parameter type hints
        for arg in node.args.args:
            if arg.annotation is None and arg.arg != "self" and arg.arg != "cls": # Ignore self/cls for now
                self.violations.append((arg.lineno, "Missing parameter type hint",
                                         f"Suggestion: Add `: Any` or a more specific type to parameter `{arg.arg}` in function `{node.name}`."))
        
        # Check keyword-only arguments
        for arg in node.args.kwonlyargs:
            if arg.annotation is None:
                self.violations.append((arg.lineno, "Missing parameter type hint",
                                         f"Suggestion: Add `: Any` or a more specific type to keyword-only parameter `{arg.arg}` in function `{node.name}`."))

        # Check varargs and kwargs
        if node.args.vararg and node.args.vararg.annotation is None:
            self.violations.append((node.args.vararg.lineno, "Missing varargs type hint",
                                     f"Suggestion: Add `: tuple[Any, ...]` or a more specific type to `*{node.args.vararg.arg}` in function `{node.name}`."))
        if node.args.kwarg and node.args.kwarg.annotation is None:
            self.violations.append((node.args.kwarg.lineno, "Missing kwargs type hint",
                                     f"Suggestion: Add `: dict[str, Any]` or a more specific type to `**{node.args.kwarg.arg}` in function `{node.name}`."))

        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        # Same checks as FunctionDef
        self.visit_FunctionDef(node)

    # Add more visitors for class attributes, variables, etc., for a more comprehensive tool

def analyze_file(filepath: str) -> List[Tuple[str, int, str, str]]:
    file_violations = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            tree = ast.parse(f.read(), filename=filepath)
        analyzer = TypeHintAnalyzer()
        analyzer.visit(tree)
        for lineno, description, suggestion in analyzer.violations:
            file_violations.append((filepath, lineno, description, suggestion))
    except SyntaxError as e:
        log_error(f"Syntax error in {filepath} at line {e.lineno}: {e.msg}")
    except Exception as e:
        log_error(f"Error processing {filepath}: {e}")
    return file_violations

def main():
    parser = argparse.ArgumentParser(
        description="Analyze Python project for missing type hints and suggest additions."
    )
    parser.add_argument(
        "project_root_dir",
        nargs="?",
        default=".",
        help="Root directory of the Python project (default: current directory)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Only report violations, do not attempt to apply fixes (not implemented yet for this version)"
    )
    args = parser.parse_args()

    project_root_dir = os.path.abspath(args.project_root_dir)

    if not os.path.isdir(project_root_dir):
        log_error(f"Project root directory not found: {project_root_dir}")
        return

    log_info(f"Starting type hint migration analysis for: {project_root_dir}")

    exclude_dirs = ["venv", ".venv", "node_modules", "dist", ".git", "__pycache__"]
    py_files = find_py_files(project_root_dir, exclude_dirs)

    if not py_files:
        log_warning(f"No Python files found in {project_root_dir}. Is the path correct?")
        return

    total_violations = 0
    for py_file in py_files:
        violations = analyze_file(py_file)
        if violations:
            log_warning(f"Found missing type hints in {os.path.relpath(py_file, project_root_dir)}:")
            for filepath, line_num, description, suggestion in violations:
                print(f"  {COLOR_CYAN}Line {line_num}:{COLOR_RESET} {description}")
                print(f"    {COLOR_YELLOW}>> {suggestion}{COLOR_RESET}")
            total_violations += len(violations)

    if total_violations == 0:
        log_success("No obvious missing type hints detected by this basic analysis.")
        log_info("Consider running a full static type checker like Mypy for a comprehensive check.")
    else:
        log_warning(f"Analysis complete. Found {total_violations} potential missing type hints.")
        log_info("Review the suggestions above and consider adding type hints.")
        log_info("For a comprehensive check, run `mypy` or `pyright` on your project.")

if __name__ == "__main__":
    main()
