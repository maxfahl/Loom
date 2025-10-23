#!/bin/bash

# api-endpoint-linter.sh
# Wrapper script to analyze API endpoint definitions for RESTful naming convention violations
# using the Python script api-endpoint-linter.py.

# Usage:
#   ./api-endpoint-linter.sh [OPTIONS] <files_or_dirs...>
#
# Options:
#   --exclude <glob_pattern>  Glob pattern for files/directories to exclude.
#                             Can be specified multiple times.
#   --dry-run                 Print the actions that would be taken without
#                             actually creating or modifying files.
#   --help                    Show this help message and exit.
#
# Arguments:
#   <files_or_dirs...>        One or more file paths or directories to scan.
#                             Supports glob patterns (e.g., 'src/**/*.ts').
#
# Example:
#   ./api-endpoint-linter.sh src/routes/**/*.ts
#   ./api-endpoint-linter.sh ./api --exclude './api/v1/legacy/*'
#   ./api-endpoint-linter.sh . --exclude 'node_modules/*' --dry-run

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PYTHON_SCRIPT="${SCRIPT_DIR}/api-endpoint-linter.py"

# Check if Python script exists
if [ ! -f "$PYTHON_SCRIPT" ]; then
  echo "Error: Python script '${PYTHON_SCRIPT}' not found." >&2
  exit 1
fi

# Execute the Python script with all arguments passed to this shell script
python3 "$PYTHON_SCRIPT" "$@"

# Check the exit status of the Python script
if [ $? -eq 0 ]; then
  echo "\nAPI endpoint linting script finished successfully."
else
  echo "\nAPI endpoint linting script encountered an error." >&2
  exit 1
fi
