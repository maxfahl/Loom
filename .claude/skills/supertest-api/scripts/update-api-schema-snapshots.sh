#!/bin/bash

# update-api-schema-snapshots.sh
#
# Purpose:
#   Runs the test suite with the Jest snapshot update flag (-u) to update
#   any outdated API response snapshots. This is essential when API responses
#   legitimately change due to new features or modifications, ensuring that
#   tests remain accurate without manual snapshot editing.
#
# Usage:
#   ./update-api-schema-snapshots.sh [test_path]
#
# Arguments:
#   [test_path]: Optional. A specific path or test file to run Jest against.
#                If not provided, Jest will run against all tests in the project.
#
# Examples:
#   ./update-api-schema-snapshots.sh
#   ./update-api-schema-snapshots.sh src/__tests__/api/users.test.ts
#   ./update-api-schema-snapshots.sh "src/__tests__/api/**/*.test.ts"
#
# Features:
#   - Executes Jest with the --updateSnapshot flag.
#   - Allows targeting specific test files or directories.
#   - Provides clear output indicating success or failure.
#   - Includes a dry-run mode to preview changes (though Jest -u directly updates).
#
# Prerequisites:
#   - Jest must be installed and configured in the project.
#   - Snapshot tests must already exist.

set -euo pipefail

# --- Configuration ---
JEST_COMMAND="npx jest"

# --- Helper Functions ---

# Function to display script usage
usage() {
  echo "Usage: $0 [test_path]"
  echo ""
  echo "Arguments:"
  echo "  [test_path]: Optional. A specific path or test file to run Jest against."
  echo "               If not provided, Jest will run against all tests in the project."
  echo ""
  echo "Examples:"
  echo "  $0"
  echo "  $0 src/__tests__/api/users.test.ts"
  echo "  $0 \"src/__tests__/api/**/*.test.ts\""
  exit 1
}

# Function to print messages in color
print_color() {
  local color="$1"
  local message="$2"
  case "$color" in
    "red")    echo -e "\033[0;31m${message}\033[0m" ;;
    "green")  echo -e "\033[0;32m${message}\033[0m" ;;
    "yellow") echo -e "\033[0;33m${message}\033[0m" ;;
    "blue")   echo -e "\033[0;34m${message}\033[0m" ;;
    *)        echo "${message}" ;;
  esac
}

# --- Main Script Logic ---

TEST_PATH="${1:-}"

print_color "blue" "Starting API snapshot update..."

# Construct the Jest command
JEST_FULL_COMMAND="${JEST_COMMAND} --updateSnapshot ${TEST_PATH}"

print_color "blue" "Executing: ${JEST_FULL_COMMAND}"

# Execute Jest command
if ${JEST_FULL_COMMAND}; then
  print_color "green" "\nAPI snapshots updated successfully! Review changes with git diff."
else
  print_color "red" "\nError: Failed to update API snapshots. Check the output above for details."
  exit 1
fi
