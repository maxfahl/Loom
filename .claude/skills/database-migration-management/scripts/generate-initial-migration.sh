#!/bin/bash
#
# Script: generate-initial-migration.sh
# Description: Generates an initial node-pg-migrate TypeScript migration file from an existing
#              PostgreSQL database schema using pg_dump. This is useful when onboarding
#              node-pg-migrate to an existing project with an established database.
#
# Usage: ./generate-initial-migration.sh [--output <output_file_path>] [--db-url <database_url>] [--no-confirm]
#
# Example:
#   ./generate-initial-migration.sh
#   ./generate-initial-migration.sh --output src/migrations/001_initial_schema.ts
#   ./generate-initial-migration.sh --db-url postgres://user:pass@host:5432/mydb
#
# Requirements:
#   - PostgreSQL database accessible.
#   - pg_dump command-line client installed.
#   - node-pg-migrate installed globally or locally (via npx).
#
# Configuration:
#   - DATABASE_URL: Connection string for the PostgreSQL database. Defaults to environment variable.
#   - MIGRATIONS_DIR: Directory for migration files. Defaults to 'src/migrations'.
#
# Error Handling:
#   - Exits if pg_dump or node-pg-migrate commands fail.

# --- Configuration ---
MIGRATIONS_DIR="${MIGRATIONS_DIR:-src/migrations}"
# ---------------------

# --- Helper Functions ---
print_help() {
  echo "Usage: $0 [--output <output_file_path>] [--db-url <database_url>] [--no-confirm]"
  echo ""
  echo "Description: Generates an initial node-pg-migrate TypeScript migration file from an existing"
  echo "             PostgreSQL database schema using pg_dump. This is useful when onboarding"
  echo "             node-pg-migrate to an existing project with an established database."
  echo ""
  echo "Options:"
  echo "  --output <path>   Specify the full path for the output migration file (e.g., src/migrations/initial_schema.ts)."
  echo "                    If not provided, a timestamped file will be created in MIGRATIONS_DIR."
  echo "  --db-url <url>    Specify the PostgreSQL database connection URL. Overrides DATABASE_URL env var."
  echo "  --no-confirm      Skip the confirmation prompt before proceeding."
  echo "  -h, --help        Display this help message."
  echo ""
  echo "Configuration:"
  echo "  DATABASE_URL      PostgreSQL connection string (can be overridden by --db-url)."
  echo "  MIGRATIONS_DIR    Directory for migration files (default: src/migrations)."
  echo ""
  echo "Examples:"
  echo "  $0"
  echo "  $0 --output db/migrations/001_baseline.ts --db-url postgres://user:pass@host:5432/mydb"
  echo "  DATABASE_URL=postgres://localhost/my_db $0 --no-confirm"
  exit 0
}

# --- Main Logic ---

OUTPUT_FILE=""
DB_URL="${DATABASE_URL}"
NO_CONFIRM=false

# Parse arguments
while [[ $# -gt 0 ]]; do
  case "$1" in
    --output)
      OUTPUT_FILE="$2"
      shift # past argument
      shift # past value
      ;;
    --db-url)
      DB_URL="$2"
      shift # past argument
      shift # past value
      ;;
    --no-confirm)
      NO_CONFIRM=true
      shift # past argument
      ;;
    -h|--help)
      print_help
      ;;
    *)
      echo "Unknown option: $1" >&2
      print_help
      ;;
  esac
done

# Validate DB_URL
if [ -z "$DB_URL" ]; then
  echo "Error: Database connection URL (DATABASE_URL or --db-url) is not set." >&2
  echo "Please provide a PostgreSQL connection string." >&2
  exit 1
fi

# Ensure migrations directory exists if output file is not fully specified
if [ -z "$OUTPUT_FILE" ]; then
  mkdir -p "$MIGRATIONS_DIR" || { echo "Error: Could not create directory '$MIGRATIONS_DIR'." >&2; exit 1; }
  TIMESTAMP=$(date +%Y%m%d%H%M%S)
  OUTPUT_FILE="${MIGRATIONS_DIR}/${TIMESTAMP}_initial_schema.ts"
fi

echo ""
echo "--- Generating Initial Migration ---"
echo "Source Database URL: ${DB_URL}"
echo "Output File: ${OUTPUT_FILE}"
echo ""

if [ "$NO_CONFIRM" = false ]; then
  read -r -p "This will dump the schema from the specified database and create a new migration file. Continue? (y/N) " response
  if [[ ! "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
    echo "Operation cancelled."
    exit 0
  fi
fi

# 1. Dump schema using pg_dump
echo "1. Dumping database schema..."
SCHEMA_SQL=$(PGPASSWORD=$(echo "$DB_URL" | sed -n 's/.*:\(.*\)@.*/\1/p') pg_dump --schema-only --no-owner --no-privileges --no-comments --clean --if-exists -d "$DB_URL" 2>&1)

if [ $? -ne 0 ]; then
  echo "Error: pg_dump failed." >&2
  echo "pg_dump output:" >&2
  echo "$SCHEMA_SQL" >&2
  exit 1
fi

# 2. Create migration file content
echo "2. Creating migration file content..."
cat << EOF > "$OUTPUT_FILE"
import { MigrationBuilder, ColumnDefinitions } from 'node-pg-migrate';

export async function up(pgm: MigrationBuilder): Promise<void> {
  pgm.sql(`
${SCHEMA_SQL}
  `);
}

export async function down(pgm: MigrationBuilder): Promise<void> {
  // This down function is intentionally left empty or minimal for an initial schema dump.
  // Reverting an initial schema dump typically means dropping the entire database,
  // which is usually not desired for a single migration rollback.
  // If you need to revert, consider dropping and recreating the database.
  console.warn('Reverting initial schema migration is not recommended. Consider dropping and recreating the database if necessary.');
}
EOF

if [ $? -ne 0 ]; then
  echo "Error: Failed to write migration file '$OUTPUT_FILE'." >&2
  exit 1
fi

echo "\n--- Initial migration generated successfully! ---"
echo "File: '$OUTPUT_FILE'"
echo ""
echo "Next steps:"
echo "1. Review the generated migration file for any sensitive data or unwanted statements."
echo "2. Apply this migration to your database using: npx node-pg-migrate up --fake --migrations-dir ${MIGRATIONS_DIR}"
echo "   The --fake flag is crucial here to mark the existing schema as applied without re-executing DDL."

exit 0
