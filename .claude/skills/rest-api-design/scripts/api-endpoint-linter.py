#!/usr/bin/env python3
"""
api-endpoint-linter.py: Analyzes API endpoint definitions for RESTful naming convention violations.

This script scans specified files (e.g., JavaScript/TypeScript route definitions)
for common anti-patterns in REST API endpoint naming, such as using verbs in URIs
or inconsistent pluralization of resource names. It helps enforce RESTful design
principles and maintain API consistency.

Usage:
    python3 api-endpoint-linter.py [OPTIONS] <files_or_dirs...>

Options:
    --exclude <glob_pattern>  Glob pattern for files/directories to exclude.
                              Can be specified multiple times.
    --dry-run                 Print the actions that would be taken without
                              actually creating or modifying files.
    --help                    Show this help message and exit.

Arguments:
    <files_or_dirs...>        One or more file paths or directories to scan.
                              Supports glob patterns (e.g., 'src/**/*.ts').

Example:
    python3 api-endpoint-linter.py src/routes/**/*.ts
    python3 api-endpoint-linter.py ./api --exclude './api/v1/legacy/*'
    python3 api-endpoint-linter.py . --exclude 'node_modules/*' --dry-run
"""

import argparse
import os
import re
import sys
from pathlib import Path
from typing import List, Dict, Any
from colorama import Fore, Style, init
import fnmatch

# Initialize colorama for cross-platform colored output
init(autoreset=True)

def print_success(message):
    print(f"{Fore.GREEN}✓ {message}{Style.RESET_ALL}")

def print_info(message):
    print(f"{Fore.CYAN}ℹ {message}{Style.RESET_ALL}")

def print_warning(message):
    print(f"{Fore.YELLOW}▲ {message}{Style.RESET_ALL}")

def print_error(message):
    print(f"{Fore.RED}✗ {message}{Style.RESET_ALL}")

# Common verbs to flag in URIs
VERBS = {
    "get", "create", "add", "post", "update", "put", "patch", "delete", "remove",
    "set", "fetch", "retrieve", "send", "receive", "process", "execute", "do"
}

# Regex to find common route definitions in JS/TS files
# This is a simplified regex and might need adjustment for specific frameworks
ROUTE_REGEX = re.compile(r"(router|app)\.(get|post|put|patch|delete)\(['"](/[^'"]+)['"]", re.IGNORECASE)

def is_plural(word: str) -> bool:
    # Simple pluralization check (can be improved with a proper library)
    if word.endswith("s") or word.endswith("es"):
        return True
    return False

def analyze_uri(uri: str, file_path: Path, line_num: int) -> List[str]:
    issues = []
    path_segments = [segment for segment in uri.split('/') if segment and not re.match(r"^.{$}", segment)] # Exclude path parameters

    for segment in path_segments:
        # Check for verbs
        if segment.lower() in VERBS:
            issues.append(f"  - Verb '{segment}' found in URI segment: {uri} (Line: {line_num})")
        
        # Check for singular nouns (simple check)
        if not is_plural(segment) and segment.lower() not in ["api", "v1", "v2"] and not re.match(r"^\d+$", segment):
            issues.append(f"  - Singular noun '{segment}' found in URI segment. Consider plural: {uri} (Line: {line_num})")

    return issues

def find_files(paths: List[str], exclude_patterns: List[str]) -> List[Path]:
    found_files = []
    for p in paths:
        path = Path(p)
        if path.is_file():
            if not any(fnmatch.fnmatch(str(path), pattern) for pattern in exclude_patterns):
                found_files.append(path)
        elif path.is_dir():
            for root, _, filenames in os.walk(path):
                for filename in filenames:
                    file_path = Path(root) / filename
                    if file_path.suffix in [".js", ".ts", ".jsx", ".tsx"]:
                        if not any(fnmatch.fnmatch(str(file_path), pattern) for pattern in exclude_patterns):
                            found_files.append(file_path)
    return found_files

def main():
    parser = argparse.ArgumentParser(
        description="Analyzes API endpoint definitions for RESTful naming convention violations."
    )
    parser.add_argument(
        "files_or_dirs",
        nargs='+',
        help="One or more file paths or directories to scan. Supports glob patterns (e.g., 'src/**/*.ts')."
    )
    parser.add_argument(
        "--exclude",
        action="append",
        default=[],
        help="Glob pattern for files/directories to exclude. Can be specified multiple times."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the actions that would be taken without actually creating or modifying files."
    )
    args = parser.parse_args()

    dry_run = args.dry_run
    exclude_patterns = args.exclude

    print_info("Starting API endpoint linting...")
    if dry_run:
        print_warning("Running in DRY-RUN mode. No files will be modified.")

    all_issues: Dict[Path, List[str]] = {}
    files_to_scan = find_files(args.files_or_dirs, exclude_patterns)

    if not files_to_scan:
        print_warning("No files found to scan based on provided paths and exclusions.")
        sys.exit(0)

    for file_path in files_to_scan:
        current_file_issues = []
        try:
            with open(file_path, "r") as f:
                for i, line in enumerate(f, 1):
                    match = ROUTE_REGEX.search(line)
                    if match:
                        uri = match.group(3)
                        issues = analyze_uri(uri, file_path, i)
                        if issues:
                            current_file_issues.extend(issues)
            if current_file_issues:
                all_issues[file_path] = current_file_issues
        except Exception as e:
            print_error(f"Error processing file {file_path}: {e}")

    if all_issues:
        print_warning("\nFound potential REST API naming convention violations:")
        for file_path, issues in all_issues.items():
            print(f"{Fore.YELLOW}File: {file_path}{Style.RESET_ALL}")
            for issue in issues:
                print(issue)
        print_error("\nLinting finished with violations.")
        sys.exit(1)
    else:
        print_success("\nAPI endpoint linting finished. No violations found.")

if __name__ == "__main__":
    main()
