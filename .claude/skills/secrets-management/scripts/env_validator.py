#!/usr/bin/env python3

"""
env_validator.py

Purpose:
  Lints and validates .env files against common best practices and an optional
  .env.example template. It checks for missing variables, incorrect formatting,
  and potential security issues.

Pain Point Solved:
  Inconsistent or malformed .env files can lead to runtime errors or accidental
  secret exposure. This script helps maintain .env file quality and consistency,
  especially when multiple developers are working on a project.

Usage Examples:
  # Validate a .env file against a .env.example template
  python scripts/env_validator.py --env-file .env --template .env.example

  # Validate a .env file for basic formatting issues only
  python scripts/env_validator.py --env-file .env

  # Validate and exit with an error code if issues are found
  python scripts/env_validator.py --env-file .env --template .env.example --strict

Configuration:
  - `--env-file`: Path to the .env file to validate (default: .env).
  - `--template`: Optional path to an .env.example file to compare against.
  - `--strict`: If set, the script will exit with a non-zero status code if any issues are found.

Dependencies:
  - python-dotenv: pip install python-dotenv (for robust .env parsing)
"""

import argparse
import os
import sys
from dotenv import dotenv_values

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def load_env_file(file_path: str) -> dict:
    """
    Loads key-value pairs from a .env file.
    """
    if not os.path.exists(file_path):
        return {}
    return dotenv_values(file_path)

def validate_env_file(env_file_path: str, template_file_path: str = None) -> bool:
    """
    Validates a .env file for common issues and against a template.
    Returns True if no issues, False otherwise.
    """
    issues_found = False

    print(f"{bcolors.HEADER}{bcolors.BOLD}--- .env File Validator ---{bcolors.ENDC}")
    print(f"Validating: {bcolors.OKBLUE}{env_file_path}{bcolors.ENDC}")

    if not os.path.exists(env_file_path):
        print(f"{bcolors.FAIL}Error: .env file not found at '{env_file_path}'.{bcolors.ENDC}")
        return False

    env_vars = load_env_file(env_file_path)

    # Basic checks on the .env file itself
    print(f"{bcolors.OKCYAN}Performing basic .env file checks...{bcolors.ENDC}")
    with open(env_file_path, 'r') as f:
        for i, line in enumerate(f, 1):
            stripped_line = line.strip()
            if not stripped_line or stripped_line.startswith('#'):
                continue

            if '=' not in stripped_line:
                print(f"{bcolors.WARNING}Warning (Line {i}): Missing '=' in line: '{stripped_line}'. This might be ignored.{bcolors.ENDC}")
                issues_found = True
            elif stripped_line.count('=') > 1 and not (stripped_line.startswith("'"') or stripped_line.startswith('""')):
                # Check for multiple '=' if not a quoted value
                key, value = stripped_line.split('=', 1)
                if not (value.startswith("'"') and value.endswith("'"')) and \
                   not (value.startswith('""') and value.endswith('""')):
                    print(f"{bcolors.WARNING}Warning (Line {i}): Multiple '=' found in line without proper quoting: '{stripped_line}'. Ensure values are correctly quoted if they contain '='.{bcolors.ENDC}")
                    issues_found = True

    # Check for duplicate keys (dotenv_values handles this by taking the last one, but it's a warning)
    # This requires re-parsing manually to detect duplicates
    seen_keys = set()
    with open(env_file_path, 'r') as f:
        for i, line in enumerate(f, 1):
            stripped_line = line.strip()
            if not stripped_line or stripped_line.startswith('#'):
                continue
            if '=' in stripped_line:
                key = stripped_line.split('=', 1)[0].strip()
                if key in seen_keys:
                    print(f"{bcolors.WARNING}Warning (Line {i}): Duplicate key '{key}' found. The last occurrence will be used.{bcolors.ENDC}")
                    issues_found = True
                seen_keys.add(key)

    # Template comparison
    if template_file_path:
        print(f"{bcolors.OKCYAN}Comparing with template: {template_file_path}...{bcolors.ENDC}")
        if not os.path.exists(template_file_path):
            print(f"{bcolors.WARNING}Warning: Template file not found at '{template_file_path}'. Skipping template comparison.{bcolors.ENDC}")
        else:
            template_vars = load_env_file(template_file_path)

            # Check for missing variables in .env file
            for key in template_vars:
                if key not in env_vars:
                    print(f"{bcolors.FAIL}Error: Missing variable '{key}' from {env_file_path} (present in template).{bcolors.ENDC}")
                    issues_found = True

            # Check for extra variables in .env file (optional, can be noisy)
            # for key in env_vars:
            #     if key not in template_vars:
            #         print(f"{bcolors.WARNING}Warning: Extra variable '{key}' in {env_file_path} (not in template).{bcolors.ENDC}")
            #         issues_found = True

    # Check for sensitive values (heuristic, can be improved)
    print(f"{bcolors.OKCYAN}Checking for potentially sensitive values...{bcolors.ENDC}")
    sensitive_keywords = ["PASSWORD", "SECRET", "KEY", "TOKEN", "CREDENTIALS"]
    for key, value in env_vars.items():
        if any(keyword in key.upper() for keyword in sensitive_keywords):
            if len(value) < 16:
                print(f"{bcolors.WARNING}Warning: Key '{key}' looks sensitive but its value is short ({len(value)} chars). Consider a longer, more complex secret.{bcolors.ENDC}")
                issues_found = True
            if value.lower() in ["password", "secret", "123456", "test", "changeme"]:
                print(f"{bcolors.FAIL}Error: Key '{key}' has a weak/default value: '{value}'. Change immediately!{bcolors.ENDC}")
                issues_found = True

    if not issues_found:
        print(f"{bcolors.OKGREEN}Validation successful: No issues found in {env_file_path}.{bcolors.ENDC}")
        return True
    else:
        print(f"{bcolors.FAIL}Validation failed: Issues found in {env_file_path}.{bcolors.ENDC}")
        return False

def main():
    parser = argparse.ArgumentParser(
        description="Lint and validate .env files for best practices and consistency.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        '--env-file',
        type=str,
        default=".env",
        help="Path to the .env file to validate (default: .env)."
    )
    parser.add_argument(
        '--template',
        type=str,
        help="Optional path to an .env.example file to compare against."
    )
    parser.add_argument(
        '--strict',
        action='store_true',
        help="If set, the script will exit with a non-zero status code if any issues are found."
    )

    args = parser.parse_args()

    if not os.path.exists(args.env_file):
        print(f"{bcolors.FAIL}Error: Specified .env file not found at '{args.env_file}'.{bcolors.ENDC}", file=sys.stderr)
        sys.exit(1)

    validation_passed = validate_env_file(args.env_file, args.template)

    if args.strict and not validation_passed:
        sys.exit(1)
    elif not validation_passed:
        sys.exit(0) # Exit 0 even if warnings, unless --strict is used

if __name__ == "__main__":
    main()
