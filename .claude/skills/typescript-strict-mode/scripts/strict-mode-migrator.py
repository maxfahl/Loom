#!/usr/bin/env python3

# strict-mode-migrator.py
# Description: Analyzes a TypeScript project for common strict mode violations
#              (e.g., implicit any, unhandled nulls) and suggests fixes.
# Usage: python3 strict-mode-migrator.py [project_root_dir]
#        If project_root_dir is not provided, it analyzes the current directory.

import os
import re
import argparse
from typing import List, Tuple

# --- Configuration Variables ---
# Colors for terminal output
COLOR_RESET = "\033[0m"
COLOR_RED = "\033[0;31m"
COLOR_GREEN = "\033[0;32m"
COLOR_YELLOW = "\033[0;33m"
COLOR_BLUE = "\033[0;34m"
COLOR_CYAN = "\033[0;36m"

# Regex patterns for common strict mode violations
# This is a simplified set for demonstration. A real-world tool would use AST parsing.
IMPLICIT_ANY_PATTERN = re.compile(r"\b(function|const|let|var)\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(([^)]*)\)", re.MULTILINE)
IMPLICIT_ANY_PARAM_PATTERN = re.compile(r"\b([a-zA-Z_][a-zA-Z0-9_]*)(?!\s*:\s*[a-zA-Z_][a-zA-Z0-9_<>,[\]\s]*)")

# Pattern to find potential null/undefined issues (simplified, needs context for accuracy)
# This will broadly flag assignments/usages without null checks.
NULL_UNDEFINED_PATTERN = re.compile(r"\b([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*(null|undefined)\b")

# --- Helper Functions ---
def log_info(message: str):
    print(f"{COLOR_BLUE}[INFO]{COLOR_RESET} {message}")

def log_warning(message: str):
    print(f"{COLOR_YELLOW}[WARNING]{COLOR_RESET} {message}")

def log_error(message: str):
    print(f"{COLOR_RED}[ERROR]{COLOR_RESET} {message}")

def log_success(message: str):
    print(f"{COLOR_GREEN}[SUCCESS]{COLOR_RESET} {message}")

def find_ts_files(root_dir: str) -> List[str]:
    ts_files = []
    for dirpath, _, filenames in os.walk(root_dir):
        for f in filenames:
            if f.endswith(('.ts', '.tsx')) and not f.endswith(('.d.ts')):
                ts_files.append(os.path.join(dirpath, f))
    return ts_files

def analyze_file(filepath: str) -> List[Tuple[str, int, str, str]]:
    violations = []
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        line_num = i + 1

        # Check for implicit any in function parameters
        for match in IMPLICIT_ANY_PATTERN.finditer(line):
            params_str = match.group(3)
            for param_match in IMPLICIT_ANY_PARAM_PATTERN.finditer(params_str):
                param_name = param_match.group(1)
                violations.append((
                    filepath,
                    line_num,
                    f"Implicit 'any' for parameter '{param_name}' in function/variable declaration.",
                    f"Suggestion: Add explicit type annotation, e.g., '{param_name}: string'."
                ))
        
        # Check for direct null/undefined assignments (simplified)
        for match in NULL_UNDEFINED_PATTERN.finditer(line):
            var_name = match.group(1)
            violations.append((
                filepath,
                line_num,
                f"Potential null/undefined assignment to '{var_name}'.",
                f"Suggestion: Ensure '{var_name}' type allows null/undefined (e.g., 'Type | null') and handle with optional chaining or nullish coalescing."
            ))

    return violations

def main():
    parser = argparse.ArgumentParser(
        description="Analyze TypeScript project for strict mode violations and suggest fixes."
    )
    parser.add_argument(
        "project_root_dir",
        nargs="?",
        default=".",
        help="Root directory of the TypeScript project (default: current directory)"
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

    log_info(f"Starting strict mode migration analysis for: {project_root_dir}")

    ts_files = find_ts_files(project_root_dir)
    if not ts_files:
        log_warning(f"No TypeScript files found in {project_root_dir}. Is the path correct?")
        return

    total_violations = 0
    for ts_file in ts_files:
        violations = analyze_file(ts_file)
        if violations:
            log_warning(f"Found violations in {os.path.relpath(ts_file, project_root_dir)}:")
            for filepath, line_num, description, suggestion in violations:
                print(f"  {COLOR_CYAN}Line {line_num}:{COLOR_RESET} {description}")
                print(f"    {COLOR_YELLOW}>> {suggestion}{COLOR_RESET}")
            total_violations += len(violations)

    if total_violations == 0:
        log_success("No common strict mode violations detected by this basic analysis.")
        log_info("Consider enabling strict mode in tsconfig.json and running `tsc --noEmit` for a full check.")
    else:
        log_warning(f"Analysis complete. Found {total_violations} potential strict mode violations.")
        log_info("Review the suggestions above and consider enabling strict mode in your tsconfig.json.")
        log_info("For a comprehensive check, enable `\"strict\": true` in `tsconfig.json` and run `npx tsc --noEmit`.")

if __name__ == "__main__":
    main()
