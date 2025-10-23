#!/bin/bash

# create_migration_with_index.sh
#
# Description:
#   Generates a new Rails migration file and automatically adds an `add_index` statement
#   for a specified table and column. This helps ensure database performance best practices
#   are followed from the start, especially for frequently queried columns or foreign keys.
#
# Usage:
#   ./create_migration_with_index.sh <TableName> <ColumnName> [OPTIONS]
#
# Arguments:
#   <TableName>   The name of the database table (e.g., users, products).
#   <ColumnName>  The name of the column to add an index to (e.g., email, category_id).
#
# Options:
#   -u, --unique         Create a unique index.
#   -h, --help           Display this help message.
#   -d, --dry-run        Show what would be created without actually running `rails generate`.
#
# Example Usage:
#   ./create_migration_with_index.sh users email --unique
#   ./create_migration_with_index.sh products category_id
#   ./create_migration_with_index.sh orders user_id --dry-run
#
# Production-ready features:
#   - Argument parsing with help text.
#   - Dry-run mode.
#   - Error handling for missing arguments.
#   - Integration with `rails generate migration`.
#   - Automatic insertion of `add_index` statement.
#

# --- Configuration ---
# No specific configuration needed, relies on Rails conventions.
# ---------------------

# Function to display help message
display_help() {
  echo "Usage: $0 <TableName> <ColumnName> [OPTIONS]"
  echo ""
  echo "Arguments:"
  echo "  <TableName>   The name of the database table (e.g., users, products)."
  echo "  <ColumnName>  The name of the column to add an index to (e.g., email, category_id)."
  echo ""
  echo "Options:"
  echo "  -u, --unique         Create a unique index."
  echo "  -h, --help           Display this help message."
  echo "  -d, --dry-run        Show what would be created without actually running 
    echo "Example Usage:"
  echo "  $0 users email --unique"
  echo "  $0 products category_id"
  echo "  $0 orders user_id --dry-run"
  exit 0
}

# Parse arguments
TABLE_NAME=""
COLUMN_NAME=""
UNIQUE_INDEX=false
DRY_RUN=false

while [[ "$#" -gt 0 ]]; do
  case "$1" in
    -u|--unique)
      UNIQUE_INDEX=true
      ;;
    -h|--help)
      display_help
      ;;
    -d|--dry-run)
      DRY_RUN=true
      ;;
    *)
      if [[ -z "$TABLE_NAME" ]]; then
        TABLE_NAME="$1"
      elif [[ -z "$COLUMN_NAME" ]]; then
        COLUMN_NAME="$1"
      else
        echo "Error: Unknown argument or too many arguments: $1" >&2
        display_help
      fi
      ;;
  esac
  shift
done

# Validate arguments
if [[ -z "$TABLE_NAME" || -z "$COLUMN_NAME" ]]; then
  echo "Error: Table name and column name are required." >&2
  display_help
fi

# Construct migration name
MIGRATION_NAME="add_${COLUMN_NAME}_to_${TABLE_NAME}"

# Construct index options
INDEX_OPTIONS=""
if $UNIQUE_INDEX;
  INDEX_OPTIONS=", unique: true"
fi

# Migration content to insert
INSERT_CONTENT="    add_index :${TABLE_NAME}, :${COLUMN_NAME}${INDEX_OPTIONS}"

# Dry run logic
if $DRY_RUN;
  echo "--- Dry Run: Would generate migration and insert index statement ---"
  echo "Rails command: rails generate migration ${MIGRATION_NAME}"
  echo "Would insert the following line into the generated migration's \`change\` method:"
  echo "${INSERT_CONTENT}"
  echo "--------------------------------------------------------------------"
  exit 0
fi

# Check if `rails` command is available
if ! command -v rails &> /dev/null
then
    echo "Error: 'rails' command not found. Please ensure you are in a Rails project directory and Rails is installed." >&2
    exit 1
fi

echo "Generating migration: ${MIGRATION_NAME}"

# Run rails generate migration
RAILS_GENERATE_OUTPUT=$(rails generate migration "${MIGRATION_NAME}" 2>&1)
if [[ $? -ne 0 ]]
  echo "Error generating migration:" >&2
  echo "$RAILS_GENERATE_OUTPUT" >&2
  exit 1
fi

# Extract the path to the newly created migration file
MIGRATION_FILE=$(echo "$RAILS_GENERATE_OUTPUT" | grep "create" | awk '{print $2}')

if [[ -z "$MIGRATION_FILE" ]]
  echo "Error: Could not determine the generated migration file path." >&2
  echo "$RAILS_GENERATE_OUTPUT" >&2
  exit 1
fi

# Insert the add_index line into the migration file
# Find the 'def change' line and insert after it
if [[ -f "$MIGRATION_FILE" ]]
  # Using awk for in-place editing to insert after 'def change'
  awk -v insert="${INSERT_CONTENT}" '/def change/
  {
    print
    print insert
    next
  }
  { print }' "$MIGRATION_FILE" > "${MIGRATION_FILE}.tmp" && mv "${MIGRATION_FILE}.tmp" "$MIGRATION_FILE"

  echo "Successfully added index to migration file: ${MIGRATION_FILE}"
  echo "Remember to run \`rails db:migrate\` to apply the changes."
else
  echo "Error: Generated migration file not found at '$MIGRATION_FILE'." >&2
  exit 1
fi

exit 0
