#!/bin/bash
#
# Script: db-reset-and-seed.sh
# Description: Resets the local development database, applies all pending migrations,
#              and optionally runs a seeding script to populate it with test data.
#
# Usage: ./db-reset-and-seed.sh [--seed <seed_script_path>] [--no-confirm]
#
# Example:
#   ./db-reset-and-seed.sh
#   ./db-reset-and-seed.sh --seed ./scripts/seed-dev-data.ts
#   ./db-reset-and-seed.sh --no-confirm
#
# Requirements:
#   - PostgreSQL database accessible via DATABASE_URL environment variable.
#   - node-pg-migrate installed globally or locally (via npx).
#   - psql command-line client installed.
#
# Configuration:
#   - DATABASE_URL: Connection string for the PostgreSQL database (e.g., postgres://user:password@host:port/database).
#                   Must be set as an environment variable.
#   - MIGRATIONS_DIR: Directory containing migration files. Defaults to 'src/migrations'.
#
# Error Handling:
#   - Exits if DATABASE_URL is not set.
#   - Exits if psql or node-pg-migrate commands fail.

# --- Configuration ---
MIGRATIONS_DIR="${MIGRATIONS_DIR:-src/migrations}"
# ---------------------

# --- Helper Functions ---
print_help() {
  echo "Usage: $0 [--seed <seed_script_path>] [--no-confirm]"
  echo ""
  echo "Description: Resets the local development database, applies all pending migrations,"
  echo "             and optionally runs a seeding script to populate it with test data."
  echo ""
  echo "Options:"
  echo "  --seed <path>     Path to a TypeScript or JavaScript seeding script to run after migrations."
  echo "                    (e.g., ./scripts/seed-dev-data.ts)"
  echo "  --no-confirm      Skip the confirmation prompt before resetting the database."
  echo "  -h, --help        Display this help message."
  echo ""
  echo "Configuration:"
  echo "  DATABASE_URL      PostgreSQL connection string (required)."
  echo "  MIGRATIONS_DIR    Directory for migration files (default: src/migrations)."
  echo ""
  echo "Examples:"
  echo "  $0"
  echo "  $0 --seed ./scripts/seed-dev-data.ts"
  echo "  DATABASE_URL=postgres://user:pass@host:5432/mydb $0 --no-confirm"
  exit 0
}

# --- Main Logic ---

SEED_SCRIPT=""
NO_CONFIRM=false

# Parse arguments
while [[ $# -gt 0 ]]; do
  case "$1" in
    --seed)
      SEED_SCRIPT="$2"
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

# Validate DATABASE_URL
if [ -z "$DATABASE_URL" ]; then
  echo "Error: DATABASE_URL environment variable is not set." >&2
  echo "Please set it to your PostgreSQL connection string (e.g., postgres://user:password@host:port/database)." >&2
  exit 1
fi

DB_NAME=$(echo "$DATABASE_URL" | sed -n 's/.*\/\([^?]*\).*/\1/p')
DB_HOST=$(echo "$DATABASE_URL" | sed -n 's/.*@\([^:]*\).*/\1/p')
DB_USER=$(echo "$DATABASE_URL" | sed -n 's/.*\/\([^:]*\).*/\1/p')

if [ -z "$DB_NAME" ] || [ -z "$DB_HOST" ] || [ -z "$DB_USER" ]; then
  echo "Error: Could not parse database name, host, or user from DATABASE_URL." >&2
  echo "Please ensure DATABASE_URL is in the format: postgres://user:password@host:port/database" >&2
  exit 1
fi

echo ""
echo "--- Database Reset and Seed ---"
echo "Target Database: $DB_NAME on $DB_HOST"
echo "Migrations Directory: $MIGRATIONS_DIR"
[ -n "$SEED_SCRIPT" ] && echo "Seed Script: $SEED_SCRIPT"
echo ""

if [ "$NO_CONFIRM" = false ]; then
  read -r -p "WARNING: This will PERMANENTLY DELETE and recreate the database '$DB_NAME'. Are you sure? (y/N) " response
  if [[ ! "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
    echo "Operation cancelled."
    exit 0
  fi
fi

# 1. Drop and Recreate Database
echo "1. Dropping and recreating database '$DB_NAME' நான"
# Connect to postgres database to drop the target database
PGDATABASE="postgres" psql -h "$DB_HOST" -U "$DB_USER" -c "DROP DATABASE IF EXISTS \"$DB_NAME\";" || {
  echo "Error: Failed to drop database '$DB_NAME'. Ensure no active connections." >&2
  exit 1
}
PGDATABASE="postgres" psql -h "$DB_HOST" -U "$DB_USER" -c "CREATE DATABASE \"$DB_NAME\";" || {
  echo "Error: Failed to create database '$DB_NAME'." >&2
  exit 1
}
echo "Database '$DB_NAME' recreated successfully."

# 2. Apply Migrations
echo "2. Applying all pending migrations..."
npx node-pg-migrate up --migrations-dir "$MIGRATIONS_DIR" || {
  echo "Error: Failed to apply migrations." >&2
  exit 1
}
echo "All migrations applied successfully."

# 3. Run Seed Script (if provided)
if [ -n "$SEED_SCRIPT" ]; then
  echo "3. Running seed script '$SEED_SCRIPT' நான"
  if [[ "$SEED_SCRIPT" == *.ts ]]; then
    # Use ts-node for TypeScript seed scripts
    npx ts-node "$SEED_SCRIPT" || {
      echo "Error: Failed to run TypeScript seed script '$SEED_SCRIPT'." >&2
      exit 1
    }
  elif [[ "$SEED_SCRIPT" == *.js ]]; then
    node "$SEED_SCRIPT" || {
      echo "Error: Failed to run JavaScript seed script '$SEED_SCRIPT'." >&2
      exit 1
    }
  else
    echo "Error: Unsupported seed script file type. Must be .ts or .js." >&2
    exit 1
  fi
  echo "Seed script '$SEED_SCRIPT' executed successfully."
fi

echo "\n--- Database reset and seed complete! ---"
