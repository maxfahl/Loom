#!/usr/bin/env python3
"""
generate-docker-compose-env.py: A script to generate a .env file for Docker Compose.

This script helps manage environment variables for Docker Compose projects.
It can generate a .env file based on a template file or by interactively prompting
the user for values, making it easier to set up development or production environments.

Usage:
    python3 generate-docker-compose-env.py [-t <template_file>] [-o <output_file>] [--interactive] [--force] [--verbose]

Examples:
    # Generate .env interactively, saving to .env (default output)
    python3 generate-docker-compose-env.py --interactive

    # Generate .env from a template file, saving to .env.local
    python3 generate-docker-compose-env.py -t .env.template -o .env.local

    # Force overwrite an existing .env file
    python3 generate-docker-compose-env.py -t .env.template --force

Configuration:
    - Template file: A simple text file where each line is an environment variable
      in the format `KEY=DEFAULT_VALUE` or `KEY=` for variables without a default.
      Comments starting with `#` are ignored.

Error Handling:
    - Warns if the output file already exists and --force is not used.
    - Exits if the template file is not found.

Dependencies:
    - argparse (built-in)
    - os (built-in)
    - sys (built-in)
"""

import argparse
import os
import sys

# Colors for output
RED = '\033[0;31m'
GREEN = '\033[0;32m'
YELLOW = '\033[0;33m'
NC = '\033[0m' # No Color

def log_error(message):
    print(f"{RED}ERROR: {message}{NC}", file=sys.stderr)

def log_warning(message):
    print(f"{YELLOW}WARNING: {message}{NC}", file=sys.stderr)

def log_info(message, verbose):
    if verbose:
        print(f"{GREEN}INFO: {message}{NC}")

def parse_template(template_path: str) -> dict:
    """Parses a template file and returns a dictionary of key-default_value pairs."""
    env_vars = {}
    try:
        with open(template_path, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if '=' in line:
                    key, value = line.split('=', 1)
                    env_vars[key.strip()] = value.strip()
                else:
                    env_vars[line.strip()] = ""
    except FileNotFoundError:
        log_error(f"Template file not found at '{template_path}'")
        sys.exit(1)
    except Exception as e:
        log_error(f"Error reading template file '{template_path}': {e}")
        sys.exit(1)
    return env_vars

def main():
    parser = argparse.ArgumentParser(
        description="Generate a .env file for Docker Compose.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "-t", "--template",
        help="Path to a template file with default environment variables (e.g., .env.example)."
    )
    parser.add_argument(
        "-o", "--output",
        default=".env",
        help="Output path for the .env file (default: .env)."
    )
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Interactively prompt for each environment variable."
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing output file without prompting."
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output."
    )

    args = parser.parse_args()

    env_vars_to_write = {}

    if args.template:
        log_info(f"Loading environment variables from template: {args.template}", args.verbose)
        env_vars_to_write = parse_template(args.template)

    if args.interactive:
        log_info("Starting interactive .env generation...", args.verbose)
        if not env_vars_to_write and not args.template:
            log_warning("No template provided. Starting with an empty set of variables. You can add new ones.")
            # Allow adding new variables interactively if no template is given
            while True:
                key = input(f"{GREEN}Enter new variable name (or leave blank to finish): {NC}").strip()
                if not key:
                    break
                value = input(f"{GREEN}Enter value for {key} (default: empty): {NC}").strip()
                env_vars_to_write[key] = value
        else:
            for key, default_value in env_vars_to_write.items():
                prompt = f"{GREEN}Enter value for {key} (default: '{default_value}'): {NC}"
                user_input = input(prompt).strip()
                env_vars_to_write[key] = user_input if user_input else default_value

    # Check if output file exists
    if os.path.exists(args.output) and not args.force:
        log_warning(f"Output file '{args.output}' already exists.")
        response = input(f"{YELLOW}Overwrite existing file? (y/N): {NC}").strip().lower()
        if response != 'y':
            log_info("Operation cancelled.", args.verbose)
            sys.exit(0)

    try:
        with open(args.output, 'w') as f:
            for key, value in env_vars_to_write.items():
                f.write(f"{key}={value}\n")
        print(f"\n{GREEN}Successfully generated .env file to '{args.output}'{NC}")
    except Exception as e:
        log_error(f"Error writing to output file '{args.output}': {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
