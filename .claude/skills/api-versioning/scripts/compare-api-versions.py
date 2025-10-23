#!/usr/bin/env python3

# compare-api-versions.py
#
# Purpose:
#   Compares two versions of an API definition (e.g., OpenAPI/Swagger spec files)
#   to identify breaking changes, new features, and deprecated elements. This helps
#   in generating migration guides and ensuring proper semantic versioning.
#
# Usage:
#   ./compare-api-versions.py --old-spec <path_to_old_spec> --new-spec <path_to_new_spec> [--output <report_file>]
#
# Examples:
#   ./compare-api-versions.py --old-spec ./openapi-v1.yaml --new-spec ./openapi-v2.yaml --output api_diff_report.md
#   ./compare-api-versions.py -o ./specs/v1/openapi.json -n ./specs/v2/openapi.json
#
# Configuration:
#   - Supports OpenAPI (YAML/JSON) specification files.
#
# Error Handling:
#   - Exits if required arguments are missing or files are not found.
#   - Provides clear messages for parsing errors.
#   - Uses colored output for console readability.

import argparse
import os
import yaml
import json
from typing import Dict, Any, List, Optional

# --- Constants and Colors ---

COLOR_RED = '\033[91m'
COLOR_YELLOW = '\033[93m'
COLOR_GREEN = '\033[92m'
COLOR_BLUE = '\033[94m'
COLOR_RESET = '\033[0m'

# --- Helper Functions ---

def print_colored(text: str, color: str):
    print(f"{color}{text}{COLOR_RESET}")

def load_spec(file_path: str) -> Optional[Dict[str, Any]]:
    """Loads an OpenAPI spec from a YAML or JSON file."""
    try:
        with open(file_path, 'r') as f:
            if file_path.endswith(('.yaml', '.yml')):
                return yaml.safe_load(f)
            elif file_path.endswith('.json'):
                return json.load(f)
            else:
                print_colored(f"Error: Unsupported file format for spec: {file_path}", COLOR_RED)
                return None
    except FileNotFoundError:
        print_colored(f"Error: Spec file not found at {file_path}", COLOR_RED)
        return None
    except (yaml.YAMLError, json.JSONDecodeError) as e:
        print_colored(f"Error parsing spec {file_path}: {e}", COLOR_RED)
        return None

def get_endpoint_signature(path: str, method: str, details: Dict[str, Any]) -> str:
    """Generates a unique signature for an endpoint."""
    params = sorted([p.get('name') for p in details.get('parameters', []) if p.get('in') == 'path'])
    return f"{method.upper()} {path} ({params})".strip()

def compare_openapi_specs(old_spec: Dict[str, Any], new_spec: Dict[str, Any]) -> Dict[str, Any]:
    """Compares two OpenAPI specifications and identifies changes."""
    report = {
        'breaking_changes': [],
        'new_features': [],
        'deprecated_elements': [],
        'modified_elements': []
    }

    old_paths = old_spec.get('paths', {})
    new_paths = new_spec.get('paths', {})

    # Compare paths and methods
    for path, old_methods in old_paths.items():
        for method, old_details in old_methods.items():
            endpoint_id = f"{method.upper()} {path}"
            new_details = new_paths.get(path, {}).get(method)

            if not new_details:
                # Endpoint removed - breaking change
                report['breaking_changes'].append(f"Removed endpoint: {endpoint_id}")
            else:
                # Check for deprecation
                if old_details.get('deprecated') and not new_details.get('deprecated'):
                    report['modified_elements'].append(f"Endpoint {endpoint_id} is no longer deprecated.")
                elif not old_details.get('deprecated') and new_details.get('deprecated'):
                    report['deprecated_elements'].append(f"Endpoint {endpoint_id} is now deprecated.")

                # Compare parameters
                old_params = {p['name']: p for p in old_details.get('parameters', [])}
                new_params = {p['name']: p for p in new_details.get('parameters', [])}

                for param_name, old_param in old_params.items():
                    new_param = new_params.get(param_name)
                    if not new_param:
                        if old_param.get('required'):
                            report['breaking_changes'].append(f"Removed required parameter '{param_name}' from {endpoint_id}")
                        else:
                            report['modified_elements'].append(f"Removed optional parameter '{param_name}' from {endpoint_id}")
                    elif old_param.get('required') and not new_param.get('required'):
                        report['breaking_changes'].append(f"Parameter '{param_name}' in {endpoint_id} changed from required to optional (potential breaking change for some clients).")
                    elif not old_param.get('required') and new_param.get('required'):
                        report['breaking_changes'].append(f"Parameter '{param_name}' in {endpoint_id} changed from optional to required.")
                    # More detailed comparison for type, format, etc. could go here

                for param_name, new_param in new_params.items():
                    if param_name not in old_params:
                        if new_param.get('required'):
                            report['breaking_changes'].append(f"Added required parameter '{param_name}' to {endpoint_id}")
                        else:
                            report['new_features'].append(f"Added optional parameter '{param_name}' to {endpoint_id}")

                # Compare request bodies (simplistic check for existence/schema changes)
                old_request_body = old_details.get('requestBody', {})
                new_request_body = new_details.get('requestBody', {})
                if old_request_body and not new_request_body:
                    report['breaking_changes'].append(f"Removed request body from {endpoint_id}")
                elif not old_request_body and new_request_body:
                    report['new_features'].append(f"Added request body to {endpoint_id}")
                # Deeper comparison of requestBody schema would be complex

                # Compare responses (simplistic check for status codes/schema changes)
                old_responses = old_details.get('responses', {})
                new_responses = new_details.get('responses', {})
                for status_code, old_response in old_responses.items():
                    if status_code not in new_responses:
                        report['breaking_changes'].append(f"Removed response for status code {status_code} from {endpoint_id}")
                for status_code, new_response in new_responses.items():
                    if status_code not in old_responses:
                        report['new_features'].append(f"Added response for status code {status_code} to {endpoint_id}")

    # Find new endpoints
    for path, new_methods in new_paths.items():
        for method, new_details in new_methods.items():
            if method not in old_paths.get(path, {}):
                report['new_features'].append(f"Added new endpoint: {method.upper()} {path}")

    return report

def generate_report_markdown(report: Dict[str, Any], old_spec_path: str, new_spec_path: str) -> str:
    """Generates a Markdown report from the comparison results."""
    md = []
    md.append(f"# API Version Comparison Report\n")
    md.append(f"\nGenerated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    md.append(f"Comparing: `{old_spec_path}` vs `{new_spec_path}`\n\n")

    if not any(report.values()):
        md.append("## No significant changes detected.\n")
        return "\n".join(md)

    if report['breaking_changes']:
        md.append("## ❌ Breaking Changes\n")
        md.append("These changes require clients to update their code.\n\n")
        for change in report['breaking_changes']:
            md.append(f"- {change}\n")
        md.append("\n")

    if report['new_features']:
        md.append("## ✨ New Features / Additions\n")
        md.append("These are backward-compatible additions.\n\n")
        for feature in report['new_features']:
            md.append(f"- {feature}\n")
        md.append("\n")

    if report['deprecated_elements']:
        md.append("## ⚠️ Deprecated Elements\n")
        md.append("These elements are marked for deprecation. Clients should plan to migrate.\n\n")
        for dep in report['deprecated_elements']:
            md.append(f"- {dep}\n")
        md.append("\n")

    if report['modified_elements']:
        md.append("## 🔄 Modified Elements (Non-Breaking)\n")
        md.append("These are changes that are generally backward-compatible.\n\n")
        for mod in report['modified_elements']:
            md.append(f"- {mod}\n")
        md.append("\n")

    return "\n".join(md)

# --- Main Logic ---

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Compare two OpenAPI/Swagger specification files to identify changes."
    )
    parser.add_argument(
        "--old-spec",
        "-o",
        type=str,
        required=True,
        help="Path to the old OpenAPI (YAML/JSON) specification file."
    )
    parser.add_argument(
        "--new-spec",
        "-n",
        type=str,
        required=True,
        help="Path to the new OpenAPI (YAML/JSON) specification file."
    )
    parser.add_argument(
        "--output",
        "-x",
        type=str,
        help="Optional: File path to save the comparison report (e.g., report.md)."
    )

    args = parser.parse_args()

    print_colored(f"Loading old spec: {args.old_spec}", COLOR_BLUE)
    old_spec_content = load_spec(args.old_spec)
    if not old_spec_content:
        exit(1)

    print_colored(f"Loading new spec: {args.new_spec}", COLOR_BLUE)
    new_spec_content = load_spec(args.new_spec)
    if not new_spec_content:
        exit(1)

    print_colored("Comparing API specifications...", COLOR_BLUE)
    comparison_report = compare_openapi_specs(old_spec_content, new_spec_content)

    markdown_report = generate_report_markdown(comparison_report, args.old_spec, args.new_spec)

    if args.output:
        with open(args.output, 'w') as f:
            f.write(markdown_report)
        print_colored(f"Comparison report saved to {args.output}", COLOR_GREEN)
    else:
        print(markdown_report)

    if comparison_report['breaking_changes']:
        print_colored("\nBreaking changes detected! Consider a MAJOR version increment.", COLOR_RED)
        exit(1)
    elif comparison_report['new_features'] or comparison_report['deprecated_elements']:
        print_colored("\nNew features or deprecations detected. Consider a MINOR version increment.", COLOR_YELLOW)
        exit(0)
    elif comparison_report['modified_elements']:
        print_colored("\nNon-breaking modifications detected. Consider a PATCH version increment.", COLOR_GREEN)
        exit(0)
    else:
        print_colored("\nNo significant changes detected.", COLOR_GREEN)
        exit(0)
