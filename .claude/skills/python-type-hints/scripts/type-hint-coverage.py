#!/usr/bin/env python3

# type-hint-coverage.py
# Description: Analyzes a Python project and reports on its "type hint coverage".
#              Counts functions/methods with and without type hints, and provides a percentage.
# Usage: python3 type-hint-coverage.py [project_root_dir]
#        If project_root_dir is not provided, it analyzes the current directory.

import os
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

class CoverageAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.total_functions = 0
        self.hinted_functions = 0
        self.total_parameters = 0
        self.hinted_parameters = 0
        self.unhinted_functions: List[Tuple[str, int]] = []
        self.unhinted_parameters: List[Tuple[str, int, str]] = []

    def visit_FunctionDef(self, node: ast.FunctionDef):
        self.total_functions += 1
        if node.returns is not None:
            self.hinted_functions += 1
        else:
            self.unhinted_functions.append((node.name, node.lineno))

        for arg in node.args.args:
            if arg.arg not in ["self", "cls"]:
                self.total_parameters += 1
                if arg.annotation is not None:
                    self.hinted_parameters += 1
                else:
                    self.unhinted_parameters.append((node.name, arg.lineno, arg.arg))
        
        for arg in node.args.kwonlyargs:
            self.total_parameters += 1
            if arg.annotation is not None:
                self.hinted_parameters += 1
            else:
                self.unhinted_parameters.append((node.name, arg.lineno, arg.arg))

        if node.args.vararg:
            self.total_parameters += 1 # Count *args as one parameter
            if node.args.vararg.annotation is not None:
                self.hinted_parameters += 1
            else:
                self.unhinted_parameters.append((node.name, node.args.vararg.lineno, f"*{node.args.vararg.arg}"))
        
        if node.args.kwarg:
            self.total_parameters += 1 # Count **kwargs as one parameter
            if node.args.kwarg.annotation is not None:
                self.hinted_parameters += 1
            else:
                self.unhinted_parameters.append((node.name, node.args.kwarg.lineno, f"**{node.args.kwarg.arg}"))

        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        self.visit_FunctionDef(node) # Async functions are similar for type hinting purposes

def analyze_file(filepath: str) -> CoverageAnalyzer:
    analyzer = CoverageAnalyzer()
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            tree = ast.parse(f.read(), filename=filepath)
        analyzer.visit(tree)
    except SyntaxError as e:
        log_error(f"Syntax error in {filepath} at line {e.lineno}: {e.msg}")
    except Exception as e:
        log_error(f"Error processing {filepath}: {e}")
    return analyzer

def main():
    parser = argparse.ArgumentParser(
        description="Analyze Python project for type hint coverage."
    )
    parser.add_argument(
        "project_root_dir",
        nargs="?",
        default=".",
        help="Root directory of the Python project (default: current directory)"
    )
    args = parser.parse_args()

    project_root_dir = os.path.abspath(args.project_root_dir)

    if not os.path.isdir(project_root_dir):
        log_error(f"Project root directory not found: {project_root_dir}")
        return

    log_info(f"Starting type hint coverage analysis for: {project_root_dir}")

    exclude_dirs = ["venv", ".venv", "node_modules", "dist", ".git", "__pycache__"]
    py_files = find_py_files(project_root_dir, exclude_dirs)

    if not py_files:
        log_warning("No Python files found for analysis.")
        return

    total_functions = 0
    hinted_functions = 0
    total_parameters = 0
    hinted_parameters = 0
    all_unhinted_functions: List[Tuple[str, int, str]] = [] # (filepath, lineno, func_name)
    all_unhinted_parameters: List[Tuple[str, int, str, str]] = [] # (filepath, lineno, func_name, param_name)

    for py_file in py_files:
        analyzer = analyze_file(py_file)
        total_functions += analyzer.total_functions
        hinted_functions += analyzer.hinted_functions
        total_parameters += analyzer.total_parameters
        hinted_parameters += analyzer.hinted_parameters
        for func_name, lineno in analyzer.unhinted_functions:
            all_unhinted_functions.append((os.path.relpath(py_file, project_root_dir), lineno, func_name))
        for func_name, lineno, param_name in analyzer.unhinted_parameters:
            all_unhinted_parameters.append((os.path.relpath(py_file, project_root_dir), lineno, func_name, param_name))

    print(f"\n{COLOR_CYAN}--- Type Hint Coverage Report ---
{COLOR_RESET}")

    # Function return type coverage
    func_coverage = (hinted_functions / total_functions * 100) if total_functions > 0 else 0
    print(f"  Function Return Type Coverage: {func_coverage:.2f}% ({hinted_functions}/{total_functions} functions hinted)")
    if all_unhinted_functions:
        print(f"    {COLOR_YELLOW}Unhinted functions:{COLOR_RESET}")
        for filepath, lineno, func_name in all_unhinted_functions:
            print(f"      - {filepath}:{lineno} - Function '{func_name}'")

    # Parameter type coverage
    param_coverage = (hinted_parameters / total_parameters * 100) if total_parameters > 0 else 0
    print(f"  Parameter Type Coverage: {param_coverage:.2f}% ({hinted_parameters}/{total_parameters} parameters hinted)")
    if all_unhinted_parameters:
        print(f"    {COLOR_YELLOW}Unhinted parameters:{COLOR_RESET}")
        for filepath, lineno, func_name, param_name in all_unhinted_parameters:
            print(f"      - {filepath}:{lineno} - Function '{func_name}', Parameter '{param_name}'")

    if total_functions == 0 and total_parameters == 0:
        log_warning("No functions or parameters found for analysis.")
    elif func_coverage < 100 or param_coverage < 100:
        log_warning("Type hint coverage is not 100%. Consider adding more type hints.")
    else:
        log_success("Excellent! 100% type hint coverage for functions and parameters.")

    log_success("Type hint coverage analysis complete.")

if __name__ == "__main__":
    main()
