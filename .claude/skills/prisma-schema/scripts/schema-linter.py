#!/usr/bin/env python3

# schema-linter.py
#
# Purpose:
#   Lints the `schema.prisma` file for common anti-patterns and best practice violations.
#   This script helps maintain schema quality, consistency, and prevents common issues
#   like missing `onDelete` actions, incorrect naming conventions, and missing timestamps.
#
# Usage:
#   python scripts/schema-linter.py [--path <path_to_schema.prisma>] [--no-color]
#
# Arguments:
#   --path <path> : Optional. Specifies the path to the `schema.prisma` file.
#                   Defaults to './prisma/schema.prisma'.
#   --no-color    : Optional. Disables colored output.
#
# Examples:
#   python scripts/schema-linter.py
#   python scripts/schema-linter.py --path ./src/prisma/schema.prisma
#   python scripts/schema-linter.py --no-color
#
# Requirements:
#   - Python 3.6+.
#
# Error Handling:
#   - Exits if the specified `schema.prisma` file is not found.
#   - Provides detailed warnings/errors for each identified issue.

import argparse
import re
import os

# --- Configuration ---
DEFAULT_SCHEMA_PATH = "./prisma/schema.prisma"

# --- Colors for terminal output ---
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# --- Helper Functions ---

def print_colored(text, color, no_color):
    if no_color:
        print(text)
    else:
        print(f"{color}{text}{Colors.ENDC}")

def is_pascal_case(name):
    return re.fullmatch(r'[A-Z][a-zA-Z0-9]*', name) is not None

def is_camel_case(name):
    return re.fullmatch(r'[a-z][a-zA-Z0-9]*', name) is not None

# --- Main Linter Logic ---

def lint_schema(schema_path, no_color):
    warnings = 0
    errors = 0

    if not os.path.exists(schema_path):
        print_colored(f"Error: schema.prisma not found at '{schema_path}'", Colors.FAIL, no_color)
        return 1, 0 # Return errors, warnings

    print_colored(f"\nLinting Prisma schema: {schema_path}", Colors.HEADER, no_color)
    print_colored("-------------------------------------", Colors.HEADER, no_color)

    with open(schema_path, 'r') as f:
        content = f.readlines()

    in_model = False
    current_model = ""
    model_line_num = 0
    model_has_updated_at = False

    for i, line in enumerate(content):
        line_num = i + 1
        stripped_line = line.strip()

        # Detect model start
        model_match = re.match(r'^model\s+(\w+)\s*\{', stripped_line)
        if model_match:
            in_model = True
            current_model = model_match.group(1)
            model_line_num = line_num
            model_has_updated_at = False

            # Check model naming convention
            if not is_pascal_case(current_model):
                print_colored(f"  {Colors.WARNING}Warning (L{line_num}): Model '{current_model}' should be PascalCase.", Colors.WARNING, no_color)
                warnings += 1
            continue

        # Detect model end
        if in_model and stripped_line == '}':
            in_model = False
            # Check for missing updatedAt field after model definition ends
            if not model_has_updated_at and current_model not in ["_Migration", "_RelationalMigration"]:
                print_colored(f"  {Colors.WARNING}Warning (L{model_line_num}): Model '{current_model}' is missing an 'updatedAt' field with `@updatedAt` attribute.", Colors.WARNING, no_color)
                warnings += 1
            current_model = ""
            model_line_num = 0
            continue

        if in_model:
            # Check field naming convention
            field_match = re.match(r'^(\w+)\s+.*?', stripped_line)
            if field_match:
                field_name = field_match.group(1)
                if not is_camel_case(field_name) and not field_name.startswith("@@") and field_name not in ["id", "createdAt", "updatedAt", "deletedAt"]:
                    print_colored(f"  {Colors.WARNING}Warning (L{line_num}): Field '{field_name}' in model '{current_model}' should be camelCase.", Colors.WARNING, no_color)
                    warnings += 1

            # Check for missing onDelete on @relation fields
            if "@relation" in stripped_line and "onDelete:" not in stripped_line:
                # Exclude self-relations where onDelete might be intentionally omitted or handled differently
                if f"@relation(fields: [{field_name}Id], references: [id])" not in stripped_line:
                    print_colored(f"  {Colors.WARNING}Warning (L{line_num}): Missing 'onDelete' action for relation in model '{current_model}'. Consider adding `onDelete: Cascade | SetNull | Restrict`.", Colors.WARNING, no_color)
                    warnings += 1

            # Check for updatedAt field
            if "@updatedAt" in stripped_line:
                model_has_updated_at = True

    print_colored("-------------------------------------", Colors.HEADER, no_color)
    if errors == 0 and warnings == 0:
        print_colored("  No issues found. Schema looks good!", Colors.OKGREEN, no_color)
    else:
        if errors > 0:
            print_colored(f"  {Colors.FAIL}{errors} error(s) found.{Colors.ENDC}", Colors.FAIL, no_color)
        if warnings > 0:
            print_colored(f"  {Colors.WARNING}{warnings} warning(s) found.{Colors.ENDC}", Colors.WARNING, no_color)

    return errors, warnings

# --- Main Execution ---
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Lints a Prisma schema.prisma file for common anti-patterns and best practices."
    )
    parser.add_argument(
        "--path",
        type=str,
        default=DEFAULT_SCHEMA_PATH,
        help=f"Path to the schema.prisma file (default: {DEFAULT_SCHEMA_PATH})"
    )
    parser.add_argument(
        "--no-color",
        action="store_true",
        help="Disable colored output"
    )
    args = parser.parse_args()

    total_errors, total_warnings = lint_schema(args.path, args.no_color)

    if total_errors > 0:
        exit(1)
    elif total_warnings > 0:
        exit(0) # Exit with 0 for warnings, 1 for errors
    else:
        exit(0)
