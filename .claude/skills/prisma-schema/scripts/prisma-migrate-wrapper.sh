#!/bin/bash

# prisma-migrate-wrapper.sh
#
# Purpose:
#   A safer, guided wrapper around Prisma migration commands (`npx prisma migrate dev`
#   and `npx prisma migrate deploy`). It includes pre-checks, post-checks, and
#   reminders to ensure a robust migration workflow.
#
# Usage:
#   bash scripts/prisma-migrate-wrapper.sh dev <migration-name>
#   bash scripts/prisma-migrate-wrapper.sh deploy [--dry-run]
#   bash scripts/prisma-migrate-wrapper.sh status
#
# Arguments:
#   dev <migration-name> : Runs `npx prisma migrate dev` to create and apply a new
#                          migration. Requires a descriptive migration name.
#   deploy [--dry-run]   : Runs `npx prisma migrate deploy` to apply pending migrations.
#                          The `--dry-run` flag will show what would be deployed without
#                          actually applying changes.
#   status               : Runs `npx prisma migrate status` to check the current
#                          migration status.
#
# Examples:
#   bash scripts/prisma-migrate-wrapper.sh dev "add-users-table"
#   bash scripts/prisma-migrate-wrapper.sh deploy
#   bash scripts/prisma-migrate-wrapper.sh deploy --dry-run
#   bash scripts/prisma-migrate-wrapper.sh status
#
# Requirements:
#   - 'schema.prisma' file must exist in the 'prisma/' directory relative to the script's execution.
#   - 'npx' (Node.js package runner) must be available in the PATH.
#
# Error Handling:
#   - Exits if invalid commands or arguments are provided.
#   - Exits if 'schema.prisma' is not found.
#   - Provides clear messages for each step.

set -euo pipefail

# --- Configuration ---
PRISMA_SCHEMA_PATH="./prisma/schema.prisma" # Adjust if your schema.prisma is elsewhere

# --- Functions ---

# Function to display help message
display_help() {
  echo "Usage: bash $(basename "$0") <command> [arguments]"
  echo ""
  echo "Commands:"
  echo "  dev <migration-name> : Create and apply a new migration (e.g., \"add-users-table\")."
  echo "  deploy [--dry-run]   : Apply pending migrations. Use --dry-run to preview changes."
  echo "  status               : Check the current migration status."
  echo ""
  echo "Examples:"
  echo "  bash $(basename "$0") dev \"add-posts-table\""
  echo "  bash $(basename "$0") deploy"
  echo "  bash $(basename "$0") deploy --dry-run"
  echo "  bash $(basename "$0") status"
  echo ""
  echo "This script wraps Prisma migration commands for safer and more guided usage."
  exit 0
}

# Check for help flag
if [[ "$#" -gt 0 && "$1" == "--help" ]]; then
  display_help
fi

# Validate arguments
if [[ "$#" -lt 1 ]]; then
  echo "Error: No command provided." >&2
  display_help
fi

COMMAND="$1"

# Check if schema.prisma exists
if [[ ! -f "$PRISMA_SCHEMA_PATH" ]]; then
  echo "Error: '$PRISMA_SCHEMA_PATH' not found. Please ensure it exists." >&2
  exit 1
fi

case "$COMMAND" in
  dev)
    if [[ "$#" -lt 2 ]]; then
      echo "Error: Migration name required for 'dev' command." >&2
      display_help
    fi
    MIGRATION_NAME="$2"
    echo "Running Prisma migrate dev with name: $MIGRATION_NAME"
    npx prisma migrate dev --name "$MIGRATION_NAME"
    echo "\n--- IMPORTANT ---"
    echo "Migration created and applied. Remember to run 'npx prisma generate' to update Prisma Client."
    echo "-----------------"
    ;;

  deploy)
    DRY_RUN=""
    if [[ "$#" -gt 1 && "$2" == "--dry-run" ]]; then
      DRY_RUN="--dry-run"
      echo "Running Prisma migrate deploy in DRY-RUN mode..."
    else
      echo "Running Prisma migrate deploy..."
    fi
    npx prisma migrate deploy $DRY_RUN
    if [[ -n "$DRY_RUN" ]]; then
      echo "\n--- DRY-RUN COMPLETE ---"
      echo "No changes were applied. Review the output above."
      echo "------------------------"
    else
      echo "\n--- DEPLOYMENT COMPLETE ---"
      echo "Migrations applied successfully."
      echo "---------------------------"
    fi
    ;;

  status)
    echo "Checking Prisma migration status..."
    npx prisma migrate status
    ;;

  *)
    echo "Error: Invalid command '$COMMAND'." >&2
    display_help
    ;;
esac
