#!/usr/bin/env python3

# strict-mode-type-coverage.py
# Description: Analyzes a TypeScript project and reports on its "strictness coverage".
#              This includes checking tsconfig.json for strict flags and identifying files
#              that might be opting out of strict checks.
# Usage: python3 strict-mode-type-coverage.py [project_root_dir]
#        If project_root_dir is not provided, it analyzes the current directory.

import os
import json
import re
import argparse
from typing import Dict, Any, List

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

def find_tsconfig(root_dir: str) -> str | None:
    for dirpath, _, filenames in os.walk(root_dir):
        if "tsconfig.json" in filenames:
            return os.path.join(dirpath, "tsconfig.json")
    return None

def parse_tsconfig(tsconfig_path: str) -> Dict[str, Any]:
    try:
        with open(tsconfig_path, 'r', encoding='utf-8') as f:
            # Remove comments from tsconfig.json before parsing
            content = re.sub(r"//.*", "", f.read())
            return json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        log_error(f"Error parsing tsconfig.json at {tsconfig_path}: {e}")
        return {{}}

def find_ts_files(root_dir: str, exclude_dirs: List[str]) -> List[str]:
    ts_files = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Modify dirnames in-place to skip excluded directories
        dirnames[:] = [d for d in dirnames if d not in exclude_dirs]

        for f in filenames:
            if f.endswith(('.ts', '.tsx')) and not f.endswith(('.d.ts')):
                ts_files.append(os.path.join(dirpath, f))
    return ts_files

def analyze_file_for_suppressions(filepath: str) -> bool:
    with open(filepath, 'r', encoding='utf-8') as f:
        first_lines = [f.readline() for _ in range(5)] # Check first few lines
        for line in first_lines:
            if "// @ts-nocheck" in line or "// @ts-ignore" in line:
                return True
    return False

def main():
    parser = argparse.ArgumentParser(
        description="Analyze TypeScript project for strictness coverage."
    )
    parser.add_argument(
        "project_root_dir",
        nargs="?",
        default=".",
        help="Root directory of the TypeScript project (default: current directory)"
    )
    args = parser.parse_args()

    project_root_dir = os.path.abspath(args.project_root_dir)

    if not os.path.isdir(project_root_dir):
        log_error(f"Project root directory not found: {project_root_dir}")
        return

    log_info(f"Starting strictness coverage analysis for: {project_root_dir}")

    tsconfig_path = find_tsconfig(project_root_dir)
    if not tsconfig_path:
        log_error("No tsconfig.json found in the project. Cannot analyze strictness.")
        return

    log_info(f"Found tsconfig.json at: {os.path.relpath(tsconfig_path, project_root_dir)}")
    tsconfig = parse_tsconfig(tsconfig_path)
    compiler_options = tsconfig.get("compilerOptions", {{}})

    # Report on tsconfig.json strict flags
    print(f"\n{COLOR_CYAN}--- tsconfig.json Strictness Report ---" + COLOR_RESET)
    strict_enabled = compiler_options.get("strict", False)
    print(f"  Strict mode (\"strict\": true): {COLOR_GREEN if strict_enabled else COLOR_RED}{strict_enabled}{COLOR_RESET}")

    strict_flags = [
        "noImplicitAny", "strictNullChecks", "strictFunctionTypes",
        "strictPropertyInitialization", "strictBindCallApply", "alwaysStrict",
        "noImplicitThis", "noUncheckedIndexedAccess", "exactOptionalPropertyTypes",
        "noImplicitOverride", "noImplicitReturns", "useUnknownInCatchVariables"
    ]

    for flag in strict_flags:
        value = compiler_options.get(flag, False)
        # If 'strict' is true, these are implicitly true unless explicitly set to false
        if strict_enabled and flag not in compiler_options:
            value = True
        print(f"  {flag}: {COLOR_GREEN if value else COLOR_RED}{value}{COLOR_RESET}")

    # Analyze individual files for suppressions
    print(f"\n{COLOR_CYAN}--- File-level Strictness Report ---" + COLOR_RESET)
    exclude_dirs = ["node_modules", "dist", ".git"]
    ts_files = find_ts_files(project_root_dir, exclude_dirs)

    if not ts_files:
        log_warning("No TypeScript source files found for analysis.")
        return

    total_files = len(ts_files)
    suppressed_files = []

    for ts_file in ts_files:
        if analyze_file_for_suppressions(ts_file):
            suppressed_files.append(os.path.relpath(ts_file, project_root_dir))

    num_suppressed = len(suppressed_files)
    num_strict_files = total_files - num_suppressed

    print(f"  Total TypeScript files: {total_files}")
    print(f"  Files with // @ts-nocheck or // @ts-ignore: {num_suppressed}")
    print(f"  Files adhering to strict checks (no suppressions): {num_strict_files}")

    if total_files > 0:
        strict_coverage_percentage = (num_strict_files / total_files) * 100
        print(f"  Strictness Coverage: {COLOR_CYAN}{strict_coverage_percentage:.2f}%{COLOR_RESET}")
    else:
        print(f"  Strictness Coverage: {COLOR_CYAN}0.00%{COLOR_RESET}")

    if num_suppressed > 0:
        log_warning("The following files contain type suppression comments:")
        for f in suppressed_files:
            print(f"    - {f}")
        log_info("Consider refactoring these files to remove suppressions and enable full strictness.")

    log_success("Strictness coverage analysis complete.")

if __name__ == "__main__":
    main()
