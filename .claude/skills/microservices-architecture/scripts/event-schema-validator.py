#!/usr/bin/env python3
"""
event-schema-validator.py: Validates a JSON event against a JSON schema.

This script ensures that event data conforms to its predefined schema, which is
critical for maintaining data consistency and interoperability in event-driven
microservices architectures. It uses the `jsonschema` library for validation.

Usage:
    python3 event-schema-validator.py [OPTIONS]

Options:
    --event-file <path>     Required: Path to the JSON file containing the event data.
    --schema-file <path>    Required: Path to the JSON schema file for validation.
    --dry-run               Print the actions that would be taken without
                            actually performing validation.
    --help                  Show this help message and exit.

Example:
    python3 event-schema-validator.py --event-file ./events/order_created.json --schema-file ./schemas/order_created_schema.json
    python3 event-schema-validator.py --event-file ./events/user_updated.json --schema-file ./schemas/user_schema.json --dry-run
"""

import argparse
import json
import sys
from pathlib import Path
from colorama import Fore, Style, init
from jsonschema import validate, ValidationError

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

def load_json_file(file_path: Path) -> dict:
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print_error(f"Error: File not found at {file_path}")
        sys.exit(1)
    except json.JSONDecodeError:
        print_error(f"Error: Invalid JSON in file {file_path}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description="Validates a JSON event against a JSON schema."
    )
    parser.add_argument(
        "--event-file",
        type=str,
        required=True,
        help="Path to the JSON file containing the event data."
    )
    parser.add_argument(
        "--schema-file",
        type=str,
        required=True,
        help="Path to the JSON schema file for validation."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the actions that would be taken without actually performing validation."
    )
    args = parser.parse_args()

    event_file_path = Path(args.event_file)
    schema_file_path = Path(args.schema_file)
    dry_run = args.dry_run

    print_info(f"Validating event: {event_file_path} against schema: {schema_file_path}")
    if dry_run:
        print_warning("Running in DRY-RUN mode. No actual validation will be performed.")

    if dry_run:
        print_info("Dry run complete. No validation performed.")
        sys.exit(0)

    # Check for jsonschema library
    try:
        import jsonschema
    except ImportError:
        print_error("The 'jsonschema' library is not installed. Please install it using: pip install jsonschema")
        sys.exit(1)

    event_data = load_json_file(event_file_path)
    schema_data = load_json_file(schema_file_path)

    try:
        validate(instance=event_data, schema=schema_data)
        print_success(f"Event {event_file_path} is VALID against schema {schema_file_path}.")
    except ValidationError as e:
        print_error(f"Event {event_file_path} is INVALID against schema {schema_file_path}.")
        print_error(f"Validation Error: {e.message}")
        if e.path:
            print_error(f"Path: {list(e.path)}")
        if e.validator:
            print_error(f"Validator: {e.validator} (Value: {e.validator_value})")
        sys.exit(1)
    except Exception as e:
        print_error(f"An unexpected error occurred during validation: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
