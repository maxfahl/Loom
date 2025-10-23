#!/bin/bash
#
# Script: validate-migrations.sh
# Description: Performs static analysis and checks on node-pg-migrate TypeScript migration files
#              to ensure they adhere to best practices (e.g., presence of down() function, linting).
#
# Usage: ./validate-migrations.sh [--path <migrations_dir>] [--no-lint]
#
# Example:
#   ./validate-migrations.sh
#   ./validate-migrations.sh --path db/migrations
#   ./validate-migrations.sh --no-lint
#
# Requirements:
#   - Node.js and npm/yarn/pnpm installed.
#   - ESLint configured for TypeScript in the project (if --no-lint is not used).
#
# Configuration:
#   - MIGRATIONS_DIR: Directory containing migration files. Defaults to 'src/migrations'.
#
# Error Handling:
#   - Exits if any validation check fails.

# --- Configuration ---
MIGRATIONS_DIR="${MIGRATIONS_DIR:-src/migrations}"
# ---------------------

# --- Helper Functions ---
print_help() {
  echo "Usage: $0 [--path <migrations_dir>] [--no-lint]"
  echo ""
  echo "Description: Performs static analysis and checks on node-pg-migrate TypeScript migration files"
  echo "             to ensure they adhere to best practices (e.g., presence of down() function, linting)."
  echo ""
  echo "Options:"
  echo "  --path <dir>      Specify the directory containing migration files (default: src/migrations)."
  echo "  --no-lint         Skip ESLint checks."
  echo "  -h, --help        Display this help message."
  echo ""
  echo "Configuration:"
  echo "  MIGRATIONS_DIR    Directory for migration files (default: src/migrations)."
  echo "                    Can be overridden by setting the MIGRATIONS_DIR environment variable or --path option."
  echo ""
  echo "Examples:"
  echo "  $0"
  echo "  $0 --path db/migrations"
  echo "  $0 --no-lint"
  exit 0
}

# --- Main Logic ---

SKIP_LINT=false

# Parse arguments
while [[ $# -gt 0 ]]; do
  case "$1" in
    --path)
      MIGRATIONS_DIR="$2"
      shift # past argument
      shift # past value
      ;;
    --no-lint)
      SKIP_LINT=true
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

echo ""
echo "--- Validating Migrations in '$MIGRATIONS_DIR' ---"

# Check if migrations directory exists
if [ ! -d "$MIGRATIONS_DIR" ]; then
  echo "Error: Migrations directory '$MIGRATIONS_DIR' not found." >&2
  exit 1
fi

# 1. Check for down() function in each migration file
echo "1. Checking for presence of 'down()' function..."
DOWN_FUNCTION_MISSING=0
for file in "$MIGRATIONS_DIR"/*.ts; do
  if [ -f "$file" ]; then
    if ! grep -q "export async function down(pgm: MigrationBuilder): Promise<void>" "$file"; then
      echo "  ❌ Warning: Migration file '$(basename "$file")' is missing a 'down()' function." >&2
      DOWN_FUNCTION_MISSING=1
    fi
  fi
done

if [ "$DOWN_FUNCTION_MISSING" -eq 0 ]; then
  echo "  ✅ All migration files contain a 'down()' function."
else
  echo "  ⚠️ Some migration files are missing 'down()' functions. Please add them for reversibility." >&2
  # Decide if this should be a hard error or just a warning. For now, it's a warning.
fi

# 2. Run ESLint (if not skipped)
if [ "$SKIP_LINT" = false ]; then
  echo "2. Running ESLint on migration files..."
  # Check if eslint is available
  if ! command -v eslint &> /dev/null && ! command -v npx eslint &> /dev/null; then
    echo "  ⚠️ ESLint not found. Skipping linting. Please install ESLint or use --no-lint." >&2
  else
    # Use npx eslint to ensure local eslint is used
    npx eslint "$MIGRATIONS_DIR"/*.ts || {
      echo "  ❌ ESLint found issues in migration files." >&2
      exit 1
    }
    echo "  ✅ ESLint checks passed."
  fi
else
  echo "2. Skipping ESLint checks as requested."
fi

# 3. Check for descriptive naming (basic check: not just timestamp)
echo "3. Checking for descriptive migration names..."
DESCRIPTIVE_NAME_ISSUE=0
for file in "$MIGRATIONS_DIR"/*.ts; do
  if [ -f "$file" ]; then
    FILENAME=$(basename "$file")
    # Regex to check if filename contains more than just the timestamp prefix and .ts extension
    if [[ ! "$FILENAME" =~ ^[0-9]{14}_.+\.ts$ ]]; then
      echo "  ❌ Warning: Migration file '${FILENAME}' might not have a descriptive name (e.g., YYYYMMDDHHmmss_description.ts)." >&2
      DESCRIPTIVE_NAME_ISSUE=1
    fi
  fi
done

if [ "$DESCRIPTIVE_NAME_ISSUE" -eq 0 ]; then
  echo "  ✅ All migration files appear to have descriptive names."
else
  echo "  ⚠️ Some migration files might lack descriptive names. Consider renaming for clarity." >&2
fi

# Add more checks here as needed, e.g., for atomic changes, direct SQL usage, etc.

echo "\n--- Migration validation complete! ---"

# Exit with error if any critical issues were found (e.g., missing down() if we make it critical)
# For now, only ESLint failure causes exit 1.
if [ "$DOWN_FUNCTION_MISSING" -eq 1 ]; then
  echo "\nValidation finished with warnings. Please review the output." >&2
  exit 0 # Exit 0 for warnings, 1 for critical errors like linting
fi

exit 0
