#!/usr/bin/env python3
"""
service-dependency-analyzer.py: Analyzes microservice dependencies by scanning codebases.

This script scans specified files or directories for patterns indicating inter-service
communication (e.g., HTTP/HTTPS calls to other services). It helps visualize
and understand the dependency graph within a microservices architecture.

Usage:
    python3 service-dependency-analyzer.py [OPTIONS] <files_or_dirs...>

Options:
    --exclude <glob_pattern>  Glob pattern for files/directories to exclude.
                              Can be specified multiple times.
    --service-prefix <prefix> Prefix used for internal service hostnames (e.g., 'http://user-service').
                              This helps identify internal service calls.
                              Can be specified multiple times.
    --output-format <format>  Output format: 'text' (default) or 'json'.
    --dry-run                 Print the actions that would be taken without
                              actually creating or modifying files.
    --help                    Show this help message and exit.

Arguments:
    <files_or_dirs...>        One or more file paths or directories to scan.
                              Supports glob patterns (e.g., 'src/**/*.ts').

Example:
    python3 service-dependency-analyzer.py ./services --service-prefix 'http://user-service' --service-prefix 'http://product-service'
    python3 service-dependency-analyzer.py . --exclude 'node_modules/*' --output-format json
"""

import argparse
import os
import re
import sys
from pathlib import Path
from typing import List, Dict, Any, Set
from colorama import Fore, Style, init
import fnmatch
import json

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

# Regex to find HTTP/HTTPS URLs in code
# This is a simplified regex and might need adjustment for specific patterns
URL_REGEX = re.compile(r"(http|https)://([a-zA-Z0-9.-]+)(:[0-9]+)?(/[^"]*)?", re.IGNORECASE)

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
                    if file_path.suffix in [".js", ".ts", ".jsx", ".tsx", ".py", ".java", ".go"]:
                        if not any(fnmatch.fnmatch(str(file_path), pattern) for pattern in exclude_patterns):
                            found_files.append(file_path)
    return found_files

def extract_dependencies(
    file_path: Path,
    service_prefixes: List[str],
    current_service_name: str = "unknown-service"
) -> Set[str]:
    dependencies = set()
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
            for match in URL_REGEX.finditer(content):
                full_url = match.group(0)
                hostname = match.group(2)

                # Check if the URL matches any known service prefix
                for prefix in service_prefixes:
                    if hostname in prefix or full_url.startswith(prefix):
                        # Extract service name from prefix (e.g., http://user-service -> user-service)
                        dep_service = prefix.split('//')[-1].split('/')[0].split(':')[0]
                        if dep_service and dep_service != current_service_name:
                            dependencies.add(dep_service)
                        break
    except Exception as e:
        print_error(f"Error processing file {file_path}: {e}")
    return dependencies

def get_service_name_from_path(file_path: Path, base_paths: List[Path]) -> str:
    for bp in base_paths:
        try:
            relative_path = file_path.relative_to(bp)
            # Assuming service name is the first directory after the base path
            return str(relative_path).split(os.sep)[0]
        except ValueError:
            continue
    return "unknown-service"

def main():
    parser = argparse.ArgumentParser(
        description="Analyzes microservice dependencies by scanning codebases."
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
        "--service-prefix",
        action="append",
        default=[],
        help="Prefix used for internal service hostnames (e.g., 'http://user-service'). Can be specified multiple times."
    )
    parser.add_argument(
        "--output-format",
        type=str,
        choices=["text", "json"],
        default="text",
        help="Output format: 'text' (default) or 'json'."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the actions that would be taken without actually creating or modifying files."
    )
    args = parser.parse_args()

    dry_run = args.dry_run
    exclude_patterns = args.exclude
    service_prefixes = [p.rstrip('/') for p in args.service_prefix] # Remove trailing slashes
    output_format = args.output_format

    print_info("Starting service dependency analysis...")
    if dry_run:
        print_warning("Running in DRY-RUN mode. No files will be modified.")

    files_to_scan = find_files(args.files_or_dirs, exclude_patterns)

    if not files_to_scan:
        print_warning("No files found to scan based on provided paths and exclusions.")
        sys.exit(0)

    # Determine base paths for service names (e.g., if services are in ./services/user-service)
    base_paths = [Path(p) for p in args.files_or_dirs if Path(p).is_dir()]
    if not base_paths:
        base_paths = [Path(os.getcwd())] # Default to current working directory

    service_dependencies: Dict[str, Set[str]] = {}

    for file_path in files_to_scan:
        current_service_name = get_service_name_from_path(file_path, base_paths)
        if current_service_name not in service_dependencies:
            service_dependencies[current_service_name] = set()

        deps = extract_dependencies(file_path, service_prefixes, current_service_name)
        service_dependencies[current_service_name].update(deps)

    # Convert sets to lists for JSON output
    final_dependencies = {s: sorted(list(deps)) for s, deps in service_dependencies.items()}

    if dry_run:
        print_info("Analysis results (dry-run):")
        if output_format == "json":
            print(json.dumps(final_dependencies, indent=2))
        else:
            for service, deps in final_dependencies.items():
                print(f"{Fore.CYAN}Service: {service}{Style.RESET_ALL}")
                if deps:
                    for dep in deps:
                        print(f"  -> Depends on: {dep}")
                else:
                    print("  (No explicit internal dependencies found)")
    else:
        if output_format == "json":
            print(json.dumps(final_dependencies, indent=2))
        else:
            print_success("\nService dependency analysis complete.")
            for service, deps in final_dependencies.items():
                print(f"{Fore.CYAN}Service: {service}{Style.RESET_ALL}")
                if deps:
                    for dep in deps:
                        print(f"  -> Depends on: {dep}")
                else:
                    print("  (No explicit internal dependencies found)")

if __name__ == "__main__":
    main()
