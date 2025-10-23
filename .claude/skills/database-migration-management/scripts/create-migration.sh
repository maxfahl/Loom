#!/bin/bash
#
# Script: create-migration.sh
# Description: Automates the creation of a new node-pg-migrate TypeScript migration file.
#              It generates a file with a proper timestamp and boilerplate for up() and down() functions.
#
# Usage: ./create-migration.sh <migration_name>
#
# Example:
#   ./create-migration.sh add_users_table
#   ./create-migration.sh create_products_and_orders
#
# Requirements:
#   - node-pg-migrate installed globally or locally (via npx)
#   - TypeScript configured in the project
#
# Configuration:
#   - MIGRATIONS_DIR: Directory where migration files should be created. Defaults to 'src/migrations'.
#
# Error Handling:
#   - Exits if migration name is not provided.
#   - Exits if node-pg-migrate command fails.

# --- Configuration ---
MIGRATIONS_DIR="${MIGRATIONS_DIR:-src/migrations}"
# ---------------------

# --- Helper Functions ---
print_help() {
  echo "Usage: $0 <migration_name>"
  echo ""
  echo "Description: Automates the creation of a new node-pg-migrate TypeScript migration file."
  echo "             It generates a file with a proper timestamp and boilerplate for up() and down() functions."
  echo ""
  echo "Arguments:"
  echo "  <migration_name>  The descriptive name for the migration (e.g., add_users_table)."
  echo ""
  echo "Configuration:"
  echo "  MIGRATIONS_DIR    Directory where migration files should be created. Defaults to 'src/migrations'."
  echo "                    Can be overridden by setting the MIGRATIONS_DIR environment variable."
  echo ""
  echo "Examples:"
  echo "  $0 add_users_table"
  echo "  MIGRATIONS_DIR=db/migrations $0 create_products_and_orders"
  exit 0
}

# --- Main Logic ---

# Check for help flag
if [[ "$1" == "--help" || "$1" == "-h" ]]; then
  print_help
fi

# Validate input
if [ -z "$1" ]; then
  echo "Error: Migration name not provided." >&2
  print_help
fi

MIGRATION_NAME="$1"
MIGRATION_PATH="${MIGRATIONS_DIR}"

echo "Creating migration '$MIGRATION_NAME' in '$MIGRATION_PATH'..."

# Ensure migrations directory exists
mkdir -p "$MIGRATION_PATH" || { echo "Error: Could not create directory '$MIGRATION_PATH'." >&2; exit 1; }

# Use npx to run node-pg-migrate to ensure it's found, even if not globally installed
# The -j ts flag ensures TypeScript output
npx node-pg-migrate create "$MIGRATION_NAME" --language ts --migrations-dir "$MIGRATION_PATH" || {
  echo "Error: Failed to create migration file using node-pg-migrate." >&2
  exit 1
}

echo "Migration '$MIGRATION_NAME' created successfully."
echo "Remember to fill in the up() and down() functions in the generated file."
