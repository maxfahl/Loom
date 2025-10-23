#!/usr/bin/env python3
"""
Database Migration Generator

This script automates the creation of new migration files for database schema changes.
It generates a Python file with a timestamped name and a basic template for 'up' and 'down'
migration functions, promoting a structured approach to database evolution.

Usage:
    python3 generate_migration.py <migration_name> [--migrations-dir <path>]

Example:
    python3 generate_migration.py create_users_table
    python3 generate_migration.py add_email_to_users --migrations-dir ./db/migrations

Configuration:
    - MIGRATIONS_DIR_DEFAULT: Default directory for migration files. Can be overridden by --migrations-dir.
"""

import argparse
import os
import sys
from datetime import datetime

# --- Configuration ---
MIGRATIONS_DIR_DEFAULT = "migrations"
MIGRATION_TEMPLATE = """
"""
Migration: {migration_name}
Date: {timestamp}

This migration handles:
- Applying schema changes in the 'up' function.
- Reverting schema changes in the 'down' function.
"""

def up(cursor):
    """
    Apply the migration changes.
    Example:
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    """
    print(f"Applying migration: {__name__}")
    # Add your SQL/NoSQL schema changes here
    pass

def down(cursor):
    """
    Revert the migration changes.
    Example:
    cursor.execute("""
        DROP TABLE IF EXISTS users;
    """)
    """
    print(f"Reverting migration: {__name__}")
    # Add your SQL/NoSQL schema rollback here
    pass

# Note: The 'cursor' object passed to up/down functions should be a database cursor
# that allows executing SQL commands or NoSQL operations.
# The exact implementation will depend on your database driver and ORM/ODM.
"""

def create_migration_file(migration_name: str, migrations_dir: str):
    """
    Creates a new migration file with the given name and template.

    Args:
        migration_name: The descriptive name of the migration.
        migrations_dir: The directory where migration files should be created.
    """
    try:
        os.makedirs(migrations_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        file_name = f"{timestamp}_{migration_name}.py"
        file_path = os.path.join(migrations_dir, file_name)

        content = MIGRATION_TEMPLATE.format(
            migration_name=migration_name,
            timestamp=datetime.now().isoformat()
        )

        with open(file_path, "w") as f:
            f.write(content)

        print(f"\033[92mSuccessfully created migration file:\033[0m {file_path}")
        print("\033[94mRemember to fill in the 'up' and 'down' functions with your schema changes.\033[0m")

    except OSError as e:
        print(f"\033[91mError creating directory or file: {e}\033[0m", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"\033[91mAn unexpected error occurred: {e}\033[0m", file=sys.stderr)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description="Generate a new database migration file.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "migration_name",
        help="A descriptive name for the migration (e.g., 'create_users_table', 'add_email_to_users')."
    )
    parser.add_argument(
        "--migrations-dir",
        default=MIGRATIONS_DIR_DEFAULT,
        help=f"The directory where migration files will be created. Defaults to '{MIGRATIONS_DIR_DEFAULT}'."
    )

    args = parser.parse_args()

    create_migration_file(args.migration_name, args.migrations_dir)

if __name__ == "__main__":
    main()
