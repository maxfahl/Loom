#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
api-security-audit.py: A script to perform a basic security audit of an API
defined by an OpenAPI (Swagger) specification.

This script checks for common misconfigurations such as:
1. Missing authentication schemes for protected endpoints.
2. Use of insecure HTTP instead of HTTPS.
3. Potential exposure of sensitive data in example responses.

It helps developers "shift-left" by identifying security issues early in the
design or development phase.

Usage:
    python3 api-security-audit.py <path_to_openapi_spec.yaml/json> [--verbose]

Example:
    python3 api-security-audit.py ./openapi.yaml --verbose
    python3 api-security-audit.py https://petstore.swagger.io/v2/swagger.json
"""

import argparse
import json
import re
import sys
import yaml
from urllib.parse import urlparse
import requests

# --- Configuration ---
# Patterns to detect sensitive data in example responses
SENSITIVE_DATA_PATTERNS = {
    "credit_card": r"(\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4})",
    "email": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
    "password": r"(password|secret|token|api_key|credential)([\s"':=]+)([a-zA-Z0-9!@#$%^&*()_+-=]{8,})",
    "jwt": r"eyJ[A-Za-z0-9-_]+\.eyJ[A-Za-z0-9-_]+\.[A-Za-z0-9-_]+",
    "private_key": r"-----BEGIN (RSA|EC|PGP) PRIVATE KEY-----",
}

# --- Helper Functions ---
def print_color(text, color):
    """Prints text in a specified color."""
    colors = {
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "magenta": "\033[95m",
        "cyan": "\033[96m",
        "white": "\033[97m",
        "reset": "\033[0m",
    }
    sys.stdout.write(f"{colors.get(color, colors['reset'])}{text}{colors['reset']}\n")

def load_openapi_spec(spec_path):
    """Loads an OpenAPI specification from a local file or URL."""
    try:
        if spec_path.startswith(("http://", "https://")):
            print_color(f"Fetching OpenAPI spec from URL: {spec_path}", "blue")
            response = requests.get(spec_path, timeout=10)
            response.raise_for_status()
            content = response.text
        else:
            print_color(f"Loading OpenAPI spec from file: {spec_path}", "blue")
            with open(spec_path, "r", encoding="utf-8") as f:
                content = f.read()

        if spec_path.endswith((".yaml", ".yml")):
            return yaml.safe_load(content)
        elif spec_path.endswith(".json"):
            return json.loads(content)
        else:
            print_color("Error: Unsupported file extension. Please use .yaml, .yml, or .json.", "red")
            sys.exit(1)
    except FileNotFoundError:
        print_color(f"Error: File not found at {spec_path}", "red")
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        print_color(f"Error fetching URL {spec_path}: {e}", "red")
        sys.exit(1)
    except (yaml.YAMLError, json.JSONDecodeError) as e:
        print_color(f"Error parsing OpenAPI spec: {e}", "red")
        sys.exit(1)
    except Exception as e:
        print_color(f"An unexpected error occurred: {e}", "red")
        sys.exit(1)

def check_security_schemes(spec, verbose):
    """Checks for defined security schemes."""
    print_color("\n--- Security Scheme Check ---", "cyan")
    security_schemes = spec.get("components", {}).get("securitySchemes", {})
    if not security_schemes:
        print_color("  [WARNING] No security schemes defined in components.securitySchemes.", "yellow")
        print_color("  Recommendation: Define authentication methods like OAuth2, API Key, or HTTP Bearer.", "yellow")
        return False
    else:
        print_color("  [INFO] Security schemes defined:", "green")
        for name, scheme in security_schemes.items():
            print_color(f"    - {name}: Type={scheme.get('type')}, Scheme={scheme.get('scheme', 'N/A')}", "green")
        return True

def audit_endpoints(spec, verbose):
    """Audits each endpoint for security best practices."""
    print_color("\n--- Endpoint Audit ---", "cyan")
    issues_found = 0
    paths = spec.get("paths", {})

    for path, path_item in paths.items():
        for method, operation in path_item.items():
            if method.lower() not in ["get", "post", "put", "delete", "patch"]:
                continue

            endpoint_id = f"{method.upper()} {path}"
            print_color(f"  Auditing: {endpoint_id}", "blue")

            # 1. Check for authentication/authorization
            security = operation.get("security")
            if not security:
                print_color(f"    [WARNING] No security defined for {endpoint_id}.", "yellow")
                print_color("    Recommendation: All sensitive endpoints should have authentication and authorization.", "yellow")
                issues_found += 1
            elif verbose:
                print_color(f"    [INFO] Security defined: {security}", "green")

            # 2. Check for HTTPS enforcement (if servers are defined)
            servers = spec.get("servers", [])
            if servers:
                insecure_server_found = False
                for server in servers:
                    url = server.get("url")
                    if url and urlparse(url).scheme == "http":
                        print_color(f"    [WARNING] Insecure HTTP server URL found: {url}", "yellow")
                        print_color("    Recommendation: Always use HTTPS for API communication.", "yellow")
                        insecure_server_found = True
                        issues_found += 1
                        break
                if not insecure_server_found and verbose:
                    print_color("    [INFO] No insecure HTTP server URLs found.", "green")
            elif verbose:
                print_color("    [INFO] No 'servers' defined in spec, cannot check HTTPS enforcement.", "blue")

            # 3. Check example responses for sensitive data
            responses = operation.get("responses", {})
            for status_code, response_obj in responses.items():
                content = response_obj.get("content", {})
                for media_type, media_type_obj in content.items():
                    example = media_type_obj.get("example")
                    if example:
                        example_str = json.dumps(example) if isinstance(example, (dict, list)) else str(example)
                        for data_type, pattern in SENSITIVE_DATA_PATTERNS.items():
                            if re.search(pattern, example_str, re.IGNORECASE):
                                print_color(f"      [WARNING] Potential {data_type.replace('_', ' ')} found in example response for {endpoint_id} (Status: {status_code}, Media Type: {media_type}).", "yellow")
                                print_color("      Recommendation: Example responses should use dummy data and avoid real sensitive information.", "yellow")
                                issues_found += 1
                                break # Only report one sensitive data type per example

    if issues_found == 0:
        print_color("\n  [SUCCESS] No major security issues detected in endpoint audit.", "green")
    else:
        print_color(f"\n  [SUMMARY] Found {issues_found} potential security issues during endpoint audit.", "yellow")
    return issues_found

def main():
    parser = argparse.ArgumentParser(
        description="Perform a basic security audit of an OpenAPI specification.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "spec_path",
        help="Path to the OpenAPI spec file (YAML/JSON) or a URL."
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output for more details."
    )
    args = parser.parse_args()

    print_color("Starting API Security Audit...", "magenta")

    spec = load_openapi_spec(args.spec_path)
    if not spec:
        sys.exit(1)

    total_issues = 0
    total_issues += check_security_schemes(spec, args.verbose)
    total_issues += audit_endpoints(spec, args.verbose)

    print_color("\n--- Audit Summary ---", "magenta")
    if total_issues == 0:
        print_color("  [AUDIT PASSED] No security warnings found. Good job!", "green")
    else:
        print_color(f"  [AUDIT FAILED] Found {total_issues} potential security issues. Please review the warnings above.", "red")
        sys.exit(1)

if __name__ == "__main__":
    main()
