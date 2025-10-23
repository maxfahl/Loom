#!/usr/bin/env python3

# drf-serializer-validator.py
# Description: Analyzes Django REST Framework serializer files for common anti-patterns,
#              such as 'fields = '__all__'' or potential N+1 query issues in SerializerMethodField usage.
# Usage: python3 drf-serializer-validator.py [project_root_dir]
#
# Options:
#   --help: Display this help message.

import os
import sys
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

def find_serializer_files(root_dir: str, exclude_dirs: List[str]) -> List[str]:
    serializer_files = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Modify dirnames in-place to skip excluded directories
        dirnames[:] = [d for d in dirnames if d not in exclude_dirs]

        for f in filenames:
            if f.endswith('serializers.py'):
                serializer_files.append(os.path.join(dirpath, f))
    return serializer_files

class SerializerAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.violations: List[Tuple[int, str, str]] = []
        self.current_serializer_name: str | None = None

    def visit_ClassDef(self, node: ast.ClassDef):
        # Check if it's a serializer class (simple check for now)
        if any(base.id.endswith('Serializer') for base in node.bases if isinstance(base, ast.Name)):
            self.current_serializer_name = node.name
            self.generic_visit(node) # Visit children (Meta class, fields)
            self.current_serializer_name = None
        else:
            self.generic_visit(node)

    def visit_Assign(self, node: ast.Assign):
        if self.current_serializer_name and isinstance(node.targets[0], ast.Name) and node.targets[0].id == "fields":
            if isinstance(node.value, ast.Constant) and node.value.value == '__all__':
                self.violations.append((
                    node.lineno,
                    f"Serializer '{self.current_serializer_name}' uses 'fields = '__all__''.",
                    "Suggestion: Explicitly list fields to avoid exposing sensitive data or unnecessary fields."
                ))
        self.generic_visit(node)

    def visit_Call(self, node: ast.Call):
        if self.current_serializer_name and isinstance(node.func, ast.Attribute) and node.func.attr == "SerializerMethodField":
            # Flag SerializerMethodField as a potential N+1 query source
            self.violations.append((
                node.lineno,
                f"Serializer '{self.current_serializer_name}' uses SerializerMethodField.",
                "Suggestion: Ensure the method does not cause N+1 queries. Pre-fetch related data if necessary."
            ))
        self.generic_visit(node)

def analyze_file(filepath: str) -> List[Tuple[str, int, str, str]]:
    file_violations = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            tree = ast.parse(f.read(), filename=filepath)
        analyzer = SerializerAnalyzer()
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
        description="Analyze Django REST Framework serializer files for common anti-patterns."
    )
    parser.add_argument(
        "project_root_dir",
        nargs="?",
        default=".",
        help="Root directory of the Django project (default: current directory)"
    )
    args = parser.parse_args()

    project_root_dir = os.path.abspath(args.project_root_dir)

    if not os.path.isdir(project_root_dir):
        log_error(f"Project root directory not found: {project_root_dir}")
        return

    log_info(f"Starting DRF serializer analysis for: {project_root_dir}")

    exclude_dirs = ["venv", ".venv", "node_modules", "dist", ".git", "__pycache__"]
    serializer_files = find_serializer_files(project_root_dir, exclude_dirs)

    if not serializer_files:
        log_warning("No serializer.py files found for analysis.")
        return

    total_violations = 0
    for ser_file in serializer_files:
        violations = analyze_file(ser_file)
        if violations:
            log_warning(f"Found potential issues in {os.path.relpath(ser_file, project_root_dir)}:")
            for filepath, lineno, description, suggestion in violations:
                print(f"  {COLOR_CYAN}Line {lineno}:{COLOR_RESET} {description}")
                print(f"    {COLOR_YELLOW}>> {suggestion}{COLOR_RESET}")
            total_violations += len(violations)

    if total_violations == 0:
        log_success("No common serializer anti-patterns detected by this basic analysis.")
    else:
        log_warning(f"Analysis complete. Found {total_violations} potential serializer issues.")
        log_info("Review the suggestions above to improve your DRF serializers.")

    log_success("DRF serializer analysis complete.")

if __name__ == "__main__":
    main()
