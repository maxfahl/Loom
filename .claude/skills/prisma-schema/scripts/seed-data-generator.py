#!/usr/bin/env python3

# seed-data-generator.py
#
# Purpose:
#   Generates basic seed data for specified Prisma models based on their definitions
#   in `schema.prisma`. This script helps automate the creation of realistic-looking
#   test data for development and testing environments, reducing manual effort.
#
# Usage:
#   python scripts/seed-data-generator.py <Model1> [Model2 ...]
#   python scripts/seed-data-generator.py --path ./src/prisma/schema.prisma User Post
#
# Arguments:
#   <Model1> [Model2 ...] : One or more model names (e.g., User, Post) for which
#                           to generate seed data.
#   --path <path>         : Optional. Specifies the path to the `schema.prisma` file.
#                           Defaults to './prisma/schema.prisma'.
#   --count <num>         : Optional. Number of records to generate per model. Defaults to 5.
#
# Examples:
#   python scripts/seed-data-generator.py User Post
#   python scripts/seed-data-generator.py Product --count 10
#
# Requirements:
#   - Python 3.6+.
#   - `schema.prisma` file must exist.
#
# Error Handling:
#   - Exits if no models are specified.
#   - Exits if `schema.prisma` is not found.
#   - Informs the user if a specified model is not found in the schema.

import argparse
import re
import os
import random
from datetime import datetime, timedelta

# --- Configuration ---
DEFAULT_SCHEMA_PATH = "./prisma/schema.prisma"
DEFAULT_RECORD_COUNT = 5

# --- Helper Functions ---

def to_camel_case(snake_str):
    components = snake_str.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])

def generate_random_string(length=10):
    letters = 'abcdefghijklmnopqrstuvwxyz'
    return ''.join(random.choice(letters) for i in range(length))

def generate_random_email():
    return f"{generate_random_string(5)}@{generate_random_string(5)}.com"

def generate_random_int(min_val=1, max_val=100):
    return random.randint(min_val, max_val)

def generate_random_boolean():
    return random.choice([True, False])

def generate_random_datetime():
    now = datetime.now()
    # Generate a date within the last year
    past_date = now - timedelta(days=random.randint(1, 365))
    return past_date.isoformat(timespec='seconds') + 'Z' # ISO 8601 format with Z for UTC

# --- Schema Parsing Logic ---

def parse_prisma_schema(schema_path):
    models = {}
    current_model = None

    with open(schema_path, 'r') as f:
        for line in f:
            stripped_line = line.strip()

            model_match = re.match(r'^model\s+(\w+)\s*\{', stripped_line)
            if model_match:
                current_model = model_match.group(1)
                models[current_model] = {'fields': {}}
                continue

            if current_model and stripped_line == '}':
                current_model = None
                continue

            if current_model:
                field_match = re.match(r'^(\w+)\s+(\w+)(\?|!)?(\s+@.*)?', stripped_line)
                if field_match:
                    field_name = field_match.group(1)
                    field_type = field_match.group(2)
                    is_optional = field_match.group(3) == '?'
                    attributes = field_match.group(4) or ''

                    # Skip @id, @createdAt, @updatedAt, @default(autoincrement()) for seeding
                    if "@id" in attributes or "@default(autoincrement())" in attributes or field_name in ["createdAt", "updatedAt", "deletedAt"]:
                        continue

                    # Handle relations - we'll assume foreign keys are provided manually for simplicity
                    if "@relation" in attributes:
                        # This is a relation field, we need the foreign key field
                        fk_match = re.search(r'fields:\s*\[(\w+)\]', attributes)
                        if fk_match:
                            fk_field_name = fk_match.group(1)
                            models[current_model]['fields'][fk_field_name] = {'type': 'Int', 'optional': is_optional, 'is_fk': True}
                        continue

                    # Handle enums
                    if field_type in models: # If field_type is another model, it's a relation, handled above
                        continue

                    models[current_model]['fields'][field_name] = {'type': field_type, 'optional': is_optional, 'is_fk': False}

    return models

# --- Data Generation Logic ---

def generate_seed_data(model_name, model_fields, count):
    data = []
    for _ in range(count):
        record = {}
        for field_name, field_info in model_fields.items():
            if field_info['optional'] and random.random() < 0.3: # 30% chance to be null if optional
                record[field_name] = 'null'
                continue

            if field_info['is_fk']:
                # For FKs, we'll just put a placeholder or a random int for now.
                # In a real scenario, you'd link to existing IDs.
                record[field_name] = generate_random_int(1, 10) # Assuming FKs are Int and start from 1
                continue

            if field_info['type'] == 'String':
                if "email" in field_name.lower():
                    record[field_name] = f"'{generate_random_email()}'"
                else:
                    record[field_name] = f"'{field_name}_{generate_random_string(5)}'"
            elif field_info['type'] == 'Int':
                record[field_name] = generate_random_int()
            elif field_info['type'] == 'Boolean':
                record[field_name] = str(generate_random_boolean()).lower()
            elif field_info['type'] == 'DateTime':
                record[field_name] = f"new Date('{generate_random_datetime()}')"
            elif field_info['type'] == 'Json':
                record[field_name] = "{ key: 'value' }" # Simple JSON placeholder
            # Add more type handlers as needed
            else:
                record[field_name] = f"'TODO_{field_info['type']}'" # Placeholder for unhandled types
        data.append(record)
    return data

# --- Main Execution ---
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generates seed data for Prisma models based on schema.prisma."
    )
    parser.add_argument(
        "models",
        metavar="ModelName",
        type=str,
        nargs='+',
        help="One or more model names (e.g., User, Post) for which to generate seed data."
    )
    parser.add_argument(
        "--path",
        type=str,
        default=DEFAULT_SCHEMA_PATH,
        help=f"Path to the schema.prisma file (default: {DEFAULT_SCHEMA_PATH})"
    )
    parser.add_argument(
        "--count",
        type=int,
        default=DEFAULT_RECORD_COUNT,
        help=f"Number of records to generate per model (default: {DEFAULT_RECORD_COUNT})"
    )
    args = parser.parse_args()

    if not os.path.exists(args.path):
        print(f"Error: schema.prisma not found at '{args.path}'")
        exit(1)

    print(f"Parsing schema from: {args.path}")
    parsed_models = parse_prisma_schema(args.path)

    if not parsed_models:
        print("No models found in schema.prisma. Exiting.")
        exit(0)

    print("\n--- Generated Seed Data (TypeScript Format) ---")

    for model_to_seed in args.models:
        if model_to_seed not in parsed_models:
            print(f"Warning: Model '{model_to_seed}' not found in schema. Skipping.")
            continue

        print(f"\n// Seed data for {model_to_seed}")
        print(f"const {to_camel_case(model_to_seed)}Data = [")

        seed_data = generate_seed_data(model_to_seed, parsed_models[model_to_seed]['fields'], args.count)

        for record in seed_data:
            fields_str = ', '.join([f'{k}: {v}' for k, v in record.items()])
            print(f"  {{ {fields_str} }},")
        print("];")

    print("\n--- End of Generated Seed Data ---")
    print("\nRemember to integrate this into your Prisma seeding script (e.g., prisma/seed.ts).")
