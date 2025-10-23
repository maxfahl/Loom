#!/bin/bash

# vue-lint-fix.sh
#
# Purpose:
#   A utility script to run ESLint and Prettier with auto-fix across Vue,
#   TypeScript, and JavaScript files in the project, ensuring code quality
#   and consistent formatting. This helps maintain a clean and standardized
#   codebase, reducing manual effort during code reviews and pre-commit checks.
#
# Usage:
#   ./vue-lint-fix.sh [options] [<path>...]
#
# Options:
#   -h, --help            Display this help message.
#
# Arguments:
#   <path>...             Optional. One or more paths (files or directories)
#                         to lint and fix. If no paths are provided, the script
#                         will lint and fix the entire 'src' directory.
#
# Examples:
#   ./vue-lint-fix.sh
#   ./vue-lint-fix.sh src/components/MyComponent.vue
#   ./vue-lint-fix.sh src/views src/stores/user.ts
#
# Requirements:
#   - Node.js and npm/yarn/pnpm installed.
#   - ESLint and Prettier configured in the project (e.g., via package.json scripts).
#   - Assumes 'eslint --fix' and 'prettier --write' commands are available.
#
# Output:
#   - Displays ESLint and Prettier output.
#   - Reports any errors encountered during the process.

# --- Configuration ---
DEFAULT_LINT_PATH="src"

# --- Helper Functions ---

# Function to display help message
show_help() {
  grep '^#' "$0" | cut -c 2-
}

# --- Main Script Logic ---

# Determine paths to lint/fix
if [ "$#" -eq 0 ] || [[ "$1" == "-h" ]] || [[ "$1" == "--help" ]]; then
  if [[ "$1" == "-h" ]] || [[ "$1" == "--help" ]]; then
    show_help
    exit 0
  fi
  TARGET_PATHS="${DEFAULT_LINT_PATH}"
else
  TARGET_PATHS="$@"
fi

echo "Running ESLint --fix on: ${TARGET_PATHS}"
# Check if eslint command exists
if ! command -v eslint &> /dev/null
then
    echo "Error: eslint command not found. Please ensure ESLint is installed and configured." >&2
    exit 1
fi

# Run ESLint with --fix
eslint --fix ${TARGET_PATHS} || {
  echo "ESLint encountered errors. Please review the output above." >&2
  # Do not exit here, continue to prettier to fix formatting issues even if linting failed
}

echo "\nRunning Prettier --write on: ${TARGET_PATHS}"
# Check if prettier command exists
if ! command -v prettier &> /dev/null
then
    echo "Error: prettier command not found. Please ensure Prettier is installed and configured." >&2
    exit 1
fi

# Run Prettier with --write
prettier --write ${TARGET_PATHS} || {
  echo "Prettier encountered errors. Please review the output above." >&2
  exit 1
}

echo "\nLinting and formatting complete."
