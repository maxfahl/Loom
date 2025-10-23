#!/usr/bin/env python3
"""
validate-graphql-schema.py: A script to validate a GraphQL schema against best practices.

This script parses a GraphQL Schema Definition Language (SDL) file and performs
various checks to ensure it adheres to common best practices, such as naming conventions,
presence of descriptions, and potential N+1 issues (though full N+1 detection requires runtime analysis).

Usage:
    python3 validate-graphql-schema.py -s <schema_file.graphql> [--verbose]

Examples:
    # Validate a GraphQL schema file
    python3 validate-graphql-schema.py -s ../examples/graphql-schema.graphql

    # Validate with verbose output
    python3 validate-graphql-schema.py -s ../examples/graphql-schema.graphql --verbose

Configuration:
    - Naming conventions can be customized within the script.

Error Handling:
    - Exits with an error if the schema file is not found or is invalid GraphQL SDL.
    - Reports all identified violations of best practices.

Dependencies:
    - `graphql-core` (install with: `pip install graphql-core`)
    - `argparse` (built-in)
    - `json` (built-in)
    - `sys` (built-in)
    - `os` (built-in)
"""

import argparse
import json
import sys
import os
import re
from graphql import build_schema, GraphQLSchema, GraphQLObjectType, GraphQLField, GraphQLArgument, GraphQLInputObjectType, GraphQLEnumType, GraphQLScalarType, GraphQLInterfaceType, GraphQLUnionType

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

def validate_naming_convention(name: str, expected_pattern: str, item_type: str, item_name: str) -> bool:
    """Validates if a name matches the expected naming convention."""
    if not re.fullmatch(expected_pattern, name):
        log_warning(f"  Naming Convention Violation: {item_type} '{item_name}' has a field/argument '{name}' that does not follow {expected_pattern} convention.")
        return False
    return True

def validate_schema(schema: GraphQLSchema, verbose: bool = False) -> bool:
    """Validates a GraphQL schema against best practices."""
    all_passed = True
    log_info("Starting GraphQL schema validation...", verbose)

    # Naming Conventions (example patterns)
    TYPE_NAME_PATTERN = r"^[A-Z][a-zA-Z0-9]*$" # PascalCase
    FIELD_ARG_NAME_PATTERN = r"^[a-z][a-zA-Z0-9]*$" # camelCase
    ENUM_VALUE_PATTERN = r"^[A-Z][A-Z0-9_]*$" # SCREAMING_SNAKE_CASE

    for type_name, type_obj in schema.type_map.items():
        # Skip introspection types and built-in scalars
        if type_name.startswith('__') or type_name in ['String', 'Int', 'Float', 'Boolean', 'ID']:
            continue

        log_info(f"Validating type: {type_name}", verbose)

        # Validate Type Naming Convention
        if not validate_naming_convention(type_name, TYPE_NAME_PATTERN, "Type", type_name):
            all_passed = False

        # Check for descriptions
        if not type_obj.description:
            log_warning(f"  Missing Description: Type '{type_name}' should have a description.")
            all_passed = False

        if isinstance(type_obj, GraphQLObjectType) or isinstance(type_obj, GraphQLInterfaceType):
            for field_name, field_obj in type_obj.fields.items():
                log_info(f"  Validating field: {type_name}.{field_name}", verbose)
                # Validate Field Naming Convention
                if not validate_naming_convention(field_name, FIELD_ARG_NAME_PATTERN, "Field", f"{type_name}.{field_name}"):
                    all_passed = False

                # Check for field descriptions
                if not field_obj.description:
                    log_warning(f"  Missing Description: Field '{type_name}.{field_name}' should have a description.")
                    all_passed = False

                # Check for arguments
                for arg_name, arg_obj in field_obj.args.items():
                    log_info(f"    Validating argument: {type_name}.{field_name}({arg_name})", verbose)
                    # Validate Argument Naming Convention
                    if not validate_naming_convention(arg_name, FIELD_ARG_NAME_PATTERN, "Argument", f"{type_name}.{field_name}({arg_name})"):
                        all_passed = False

                    # Check for argument descriptions
                    if not arg_obj.description:
                        log_warning(f"  Missing Description: Argument '{type_name}.{field_name}({arg_name})' should have a description.")
                        all_passed = False

        elif isinstance(type_obj, GraphQLInputObjectType):
            for field_name, field_obj in type_obj.fields.items():
                log_info(f"  Validating input field: {type_name}.{field_name}", verbose)
                # Validate Input Field Naming Convention
                if not validate_naming_convention(field_name, FIELD_ARG_NAME_PATTERN, "Input Field", f"{type_name}.{field_name}"):
                    all_passed = False

                # Check for input field descriptions
                if not field_obj.description:
                    log_warning(f"  Missing Description: Input field '{type_name}.{field_name}' should have a description.")
                    all_passed = False

        elif isinstance(type_obj, GraphQLEnumType):
            for enum_value in type_obj.values:
                log_info(f"  Validating enum value: {type_name}.{enum_value.name}", verbose)
                # Validate Enum Value Naming Convention
                if not validate_naming_convention(enum_value.name, ENUM_VALUE_PATTERN, "Enum Value", f"{type_name}.{enum_value.name}"):
                    all_passed = False

                # Check for enum value descriptions
                if not enum_value.description:
                    log_warning(f"  Missing Description: Enum value '{type_name}.{enum_value.name}' should have a description.")
                    all_passed = False

        # Add more checks as needed, e.g., for Union types, Scalar types, etc.

    # Additional checks (e.g., N+1 potential - this is hard to do statically, but we can check for patterns)
    # For example, if a field returns a list of objects, and each object has a field that would typically
    # require a separate database query, it might indicate an N+1 problem. This is more of a heuristic.
    # For a more robust check, runtime analysis with tools like Apollo Studio or custom tracing is needed.
    log_info("Performing heuristic checks for potential N+1 issues...", verbose)
    for type_name, type_obj in schema.type_map.items():
        if isinstance(type_obj, GraphQLObjectType):
            for field_name, field_obj in type_obj.fields.items():
                # Heuristic: if a field returns a list of complex objects, it might be prone to N+1
                if hasattr(field_obj.type, 'of_type') and isinstance(field_obj.type.of_type, GraphQLObjectType):
                    if field_obj.type.of_type.name not in ['String', 'Int', 'Float', 'Boolean', 'ID']:
                        log_warning(f"  Potential N+1 Warning: Field '{type_name}.{field_name}' returns a list of complex objects ('{field_obj.type.of_type.name}'). Consider using DataLoader or similar techniques to prevent N+1 query problems.")
                        # This is a warning, not a failure for all_passed

    return all_passed

def main():
    parser = argparse.ArgumentParser(
        description="Validate a GraphQL schema against best practices.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "-s", "--schema",
        required=True,
        help="Path to the GraphQL Schema Definition Language (SDL) file."
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output."
    )

    args = parser.parse_args()

    if not os.path.exists(args.schema):
        log_error(f"Schema file not found at '{args.schema}'")
        sys.exit(1)

    try:
        schema_sdl = read_file(args.schema)
        schema = build_schema(schema_sdl)
    except Exception as e:
        log_error(f"Error parsing GraphQL schema from '{args.schema}': {e}")
        sys.exit(1)

    if validate_schema(schema, args.verbose):
        print(f"\n{GREEN}GraphQL schema validated successfully against best practices.{NC}")
        sys.exit(0)
    else:
        print(f"\n{RED}GraphQL schema validation failed. Please review the warnings/errors above.{NC}")
        sys.exit(1)

def read_file(file_path: str) -> str:
    """Helper function to read file content."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

if __name__ == "__main__":
    main()
