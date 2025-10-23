#!/usr/bin/env python3
"""
sync-schema-migrator.py: Automates the generation of database migration scripts for local databases.

This script compares an old schema definition (e.g., in JSON format) with a new one
and generates a migration script (e.g., SQL ALTER TABLE statements) to transform
the database from the old schema to the new one.

It's designed to be a flexible starting point that can be adapted for various
local database solutions (SQLite, Realm, Core Data, etc.) and ORMs.

Usage:
    python3 sync-schema-migrator.py --old-schema <path/to/old_schema.json> \
                                    --new-schema <path/to/new_schema.json> \
                                    --output <path/to/migration_script.sql>

Example Schema JSON (old_schema.json):
{
    "version": 1,
    "tables": {
        "users": {
            "columns": {
                "id": "INTEGER PRIMARY KEY",
                "name": "TEXT NOT NULL",
                "email": "TEXT UNIQUE"
            }
        }
    }
}

Example Schema JSON (new_schema.json):
{
    "version": 2,
    "tables": {
        "users": {
            "columns": {
                "id": "INTEGER PRIMARY KEY",
                "name": "TEXT NOT NULL",
                "email": "TEXT UNIQUE",
                "age": "INTEGER"
            }
        },
        "products": {
            "columns": {
                "product_id": "TEXT PRIMARY KEY",
                "name": "TEXT NOT NULL",
                "price": "REAL"
            }
        }
    }
}
"""

import argparse
import json
import sys
from typing import Dict, Any

def load_schema(file_path: str) -> Dict[str, Any]:
    """Loads a schema definition from a JSON file."""
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: Schema file not found at '{file_path}'", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in schema file at '{file_path}'", file=sys.stderr)
        sys.exit(1)

def generate_sql_migration(old_schema: Dict[str, Any], new_schema: Dict[str, Any]) -> str:
    """
    Generates SQL migration statements based on schema differences.
    This is a simplified example and might not cover all edge cases (e.g., column type changes, renames).
    """
    migrations = []

    # Handle table additions and removals
    old_tables = set(old_schema.get('tables', {}).keys())
    new_tables = set(new_schema.get('tables', {}).keys())

    added_tables = new_tables - old_tables
    removed_tables = old_tables - new_tables

    for table_name in sorted(added_tables):
        table_def = new_schema['tables'][table_name]
        columns_def = ', '.join([f"{col_name} {col_type}" for col_name, col_type in table_def['columns'].items()])
        migrations.append(f"CREATE TABLE {table_name} ({columns_def});")

    for table_name in sorted(removed_tables):
        migrations.append(f"DROP TABLE {table_name};")

    # Handle column additions and removals within existing tables
    common_tables = old_tables.intersection(new_tables)
    for table_name in sorted(common_tables):
        old_cols = set(old_schema['tables'][table_name]['columns'].keys())
        new_cols = set(new_schema['tables'][table_name]['columns'].keys())

        added_cols = new_cols - old_cols
        removed_cols = old_cols - new_cols

        for col_name in sorted(added_cols):
            col_type = new_schema['tables'][table_name]['columns'][col_name]
            migrations.append(f"ALTER TABLE {table_name} ADD COLUMN {col_name} {col_type};")

        # Note: SQLite does not directly support DROP COLUMN before version 3.35.0 (2021-03-12)
        # For broader compatibility, dropping columns often involves recreating the table.
        # This example assumes a database that supports direct DROP COLUMN or is for conceptual understanding.
        for col_name in sorted(removed_cols):
            migrations.append(f"ALTER TABLE {table_name} DROP COLUMN {col_name};")

    return "\n".join(migrations)

def main():
    parser = argparse.ArgumentParser(
        description="Generate database migration scripts by comparing old and new schema definitions.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        '--old-schema',
        required=True,
        help="Path to the old schema definition file (JSON)."
    )
    parser.add_argument(
        '--new-schema',
        required=True,
        help="Path to the new schema definition file (JSON)."
    )
    parser.add_argument(
        '--output',
        required=True,
        help="Path to the output migration script file (e.g., .sql or .py)."
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help="Print the migration script to stdout instead of writing to a file."
    )

    args = parser.parse_args()

    old_schema = load_schema(args.old_schema)
    new_schema = load_schema(args.new_schema)

    if new_schema.get('version', 0) <= old_schema.get('version', 0):
        print("Warning: New schema version is not greater than old schema version. No migration generated.", file=sys.stderr)
        sys.exit(0)

    migration_script_content = generate_sql_migration(old_schema, new_schema)

    if not migration_script_content:
        print("No schema changes detected. No migration script generated.")
        sys.exit(0)

    if args.dry_run:
        print("\n--- Generated Migration Script (Dry Run) ---\\n")
        print(migration_script_content)
        print("\n--------------------------------------------\\n")
    else:
        try:
            with open(args.output, 'w') as f:
                f.write(migration_script_content)
            print(f"Migration script successfully generated to '{args.output}'")
        except IOError:
            print(f"Error: Could not write migration script to '{args.output}'", file=sys.stderr)
            sys.exit(1)

if __name__ == '__main__':
    main()
