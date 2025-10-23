#!/usr/bin/env python3

# check-api-deprecation.py
#
# Purpose:
#   Scans API codebase (e.g., OpenAPI spec, route files) for deprecated endpoints
#   and flags them based on a defined deprecation policy. It helps ensure that
#   deprecated APIs are properly managed and eventually removed.
#
# Usage:
#   ./check-api-deprecation.py --api-spec <path_to_openapi_spec> [--policy <months>] [--output <report_file>]
#   ./check-api-deprecation.py --api-dir <path_to_api_routes> [--policy <months>] [--output <report_file>]
#
# Examples:
#   ./check-api-deprecation.py --api-spec ./openapi.yaml --policy 6
#   ./check-api-deprecation.py --api-dir ./src/api --policy 12 --output deprecation_report.md
#
# Configuration:
#   - Default deprecation policy is 6 months.
#   - Supports OpenAPI YAML/JSON files.
#   - Can scan Python/TypeScript files for '@deprecated' annotations (basic).
#
# Error Handling:
#   - Exits if required arguments are missing or invalid.
#   - Provides clear messages for file parsing errors.
#   - Uses colored output for better readability.

import argparse
import os
import yaml
import json
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional

# --- Constants and Colors ---

COLOR_RED = '\033[91m'
COLOR_YELLOW = '\033[93m'
COLOR_GREEN = '\033[92m'
COLOR_BLUE = '\033[94m'
COLOR_RESET = '\033[0m'

# --- Helper Functions ---

def print_colored(text: str, color: str):
    print(f"{color}{text}{COLOR_RESET}")

def parse_openapi_spec(file_path: str) -> Optional[Dict[str, Any]]:
    """Parses an OpenAPI (YAML/JSON) specification file."""
    try:
        with open(file_path, 'r') as f:
            if file_path.endswith(('.yaml', '.yml')):
                return yaml.safe_load(f)
            elif file_path.endswith('.json'):
                return json.load(f)
            else:
                print_colored(f"Error: Unsupported file format for OpenAPI spec: {file_path}", COLOR_RED)
                return None
    except FileNotFoundError:
        print_colored(f"Error: OpenAPI spec file not found at {file_path}", COLOR_RED)
        return None
    except (yaml.YAMLError, json.JSONDecodeError) as e:
        print_colored(f"Error parsing OpenAPI spec {file_path}: {e}", COLOR_RED)
        return None

def find_deprecated_in_openapi(spec: Dict[str, Any], policy_months: int) -> List[Dict[str, Any]]:
    """Finds deprecated endpoints in an OpenAPI spec and checks their deprecation status."""
    deprecated_endpoints = []
    paths = spec.get('paths', {})
    for path, methods in paths.items():
        for method, details in methods.items():
            if isinstance(details, dict) and details.get('deprecated', False):
                description = details.get('description', '')
                # Look for a deprecation date in the description or a custom extension
                deprecation_date_str = None
                if 'x-deprecated-date' in details:
                    deprecation_date_str = details['x-deprecated-date']
                elif 'deprecated since' in description.lower():
                    # Basic regex to find a date like YYYY-MM-DD or YYYY/MM/DD
                    import re
                    match = re.search(r'deprecated since\s*(\d{4}[-/]\d{2}[-/]\d{2})', description.lower())
                    if match:
                        deprecation_date_str = match.group(1).replace('/', '-')

                status = "Active Deprecation"
                if deprecation_date_str:
                    try:
                        deprecation_date = datetime.strptime(deprecation_date_str, '%Y-%m-%d')
                        sunset_date = deprecation_date + timedelta(days=policy_months * 30)
                        if datetime.now() > sunset_date:
                            status = f"Past Sunset Date (Sunset: {sunset_date.strftime('%Y-%m-%d')})"
                        else:
                            status = f"Deprecating (Sunset: {sunset_date.strftime('%Y-%m-%d')})"
                    except ValueError:
                        status = f"Active Deprecation (Invalid Date: {deprecation_date_str})"

                deprecated_endpoints.append({
                    'path': path,
                    'method': method.upper(),
                    'status': status,
                    'description': description.split('\n')[0] # First line of description
                })
    return deprecated_endpoints

def find_deprecated_in_codebase(api_dir: str, policy_months: int) -> List[Dict[str, Any]]:
    """Scans Python/TypeScript files for @deprecated annotations."""
    deprecated_items = []
    for root, _, files in os.walk(api_dir):
        for file in files:
            if file.endswith(('.py', '.ts', '.tsx')):
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    for i, line in enumerate(f, 1):
                        if '@deprecated' in line.lower():
                            # Attempt to extract deprecation date from comments or docstrings
                            deprecation_date_str = None
                            import re
                            match = re.search(r'@deprecated\s*(?:since\s*)?(\d{4}[-/]\d{2}[-/]\d{2})?', line.lower())
                            if match and match.group(1):
                                deprecation_date_str = match.group(1).replace('/', '-')

                            status = "Active Deprecation"
                            if deprecation_date_str:
                                try:
                                    deprecation_date = datetime.strptime(deprecation_date_str, '%Y-%m-%d')
                                    sunset_date = deprecation_date + timedelta(days=policy_months * 30)
                                    if datetime.now() > sunset_date:
                                        status = f"Past Sunset Date (Sunset: {sunset_date.strftime('%Y-%m-%d')})"
                                    else:
                                        status = f"Deprecating (Sunset: {sunset_date.strftime('%Y-%m-%d')})"
                                except ValueError:
                                    status = f"Active Deprecation (Invalid Date: {deprecation_date_str})"

                            deprecated_items.append({
                                'file': file_path,
                                'line': i,
                                'status': status,
                                'context': line.strip()
                            })
    return deprecated_items

def generate_report(deprecated_list: List[Dict[str, Any]], output_file: Optional[str]):
    """Generates a human-readable report."""
    report_content = []
    report_content.append("# API Deprecation Report\n")
    report_content.append(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    report_content.append(f"Deprecation Policy: {args.policy_months} months\n\n")

    if not deprecated_list:
        report_content.append("No deprecated API elements found.\n")
        print_colored("No deprecated API elements found.", COLOR_GREEN)
        return

    report_content.append("| Type | Path/File | Status | Description/Context |\n")
    report_content.append("|---|---|---|---|
")

    for item in deprecated_list:
        item_type = "Endpoint" if 'method' in item else "Code Element"
        identifier = f"{item.get('method', '')} {item.get('path', '')}" if 'method' in item else f"{item.get('file', '')}:{item.get('line', '')}"
        status = item.get('status', 'Unknown')
        context = item.get('description', item.get('context', ''))

        report_content.append(f"| {item_type} | {identifier} | {status} | {context} |\n")

    if output_file:
        with open(output_file, 'w') as f:
            f.writelines(report_content)
        print_colored(f"Report saved to {output_file}", COLOR_BLUE)
    else:
        for line in report_content:
            if "Past Sunset Date" in line:
                print_colored(line.strip(), COLOR_RED)
            elif "Deprecating" in line:
                print_colored(line.strip(), COLOR_YELLOW)
            else:
                print(line.strip())

# --- Main Logic ---

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Check API deprecation status based on OpenAPI spec or codebase annotations."
    )
    parser.add_argument(
        "--api-spec",
        type=str,
        help="Path to the OpenAPI (YAML/JSON) specification file."
    )
    parser.add_argument(
        "--api-dir",
        type=str,
        help="Path to the directory containing API route files (e.g., Python, TypeScript) to scan for @deprecated annotations."
    )
    parser.add_argument(
        "--policy",
        type=int,
        default=6,
        dest="policy_months",
        help="Deprecation policy in months (default: 6)."
    )
    parser.add_argument(
        "--output",
        type=str,
        help="Optional: File path to save the deprecation report (e.g., report.md)."
    )

    args = parser.parse_args()

    if not args.api_spec and not args.api_dir:
        print_colored("Error: Either --api-spec or --api-dir must be provided.", COLOR_RED)
        parser.print_help()
        exit(1)

    deprecated_items: List[Dict[str, Any]] = []

    if args.api_spec:
        print_colored(f"Scanning OpenAPI spec: {args.api_spec}", COLOR_BLUE)
        spec = parse_openapi_spec(args.api_spec)
        if spec:
            deprecated_items.extend(find_deprecated_in_openapi(spec, args.policy_months))

    if args.api_dir:
        print_colored(f"Scanning API directory: {args.api_dir}", COLOR_BLUE)
        deprecated_items.extend(find_deprecated_in_codebase(args.api_dir, args.policy_months))

    generate_report(deprecated_items, args.output)

    if any("Past Sunset Date" in item['status'] for item in deprecated_items):
        print_colored("\nAction Required: Some APIs are past their sunset date!", COLOR_RED)
        exit(1) # Indicate critical issues
    elif any("Deprecating" in item['status'] for item in deprecated_items):
        print_colored("\nWarning: Some APIs are currently in deprecation period.", COLOR_YELLOW)
        exit(0) # Indicate warnings
    else:
        print_colored("\nAll APIs are compliant with the deprecation policy.", COLOR_GREEN)
        exit(0)
