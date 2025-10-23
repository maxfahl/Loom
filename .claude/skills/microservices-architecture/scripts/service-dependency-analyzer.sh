#!/bin/bash

# service-dependency-analyzer.sh
# Wrapper script to analyze microservice dependencies by scanning codebases
# using the Python script service-dependency-analyzer.py.

# Usage:
#   ./service-dependency-analyzer.sh [OPTIONS] <files_or_dirs...>
#
# Options:
#   --exclude <glob_pattern>  Glob pattern for files/directories to exclude.
#                             Can be specified multiple times.
#   --service-prefix <prefix> Prefix used for internal service hostnames (e.g., 'http://user-service').
#                             This helps identify internal service calls.
#                             Can be specified multiple times.
#   --output-format <format>  Output format: 'text' (default) or 'json'.
#   --dry-run                 Print the actions that would be taken without
#                             actually creating or modifying files.
#   --help                    Show this help message and exit.
#
# Arguments:
#   <files_or_dirs...>        One or more file paths or directories to scan.
#                             Supports glob patterns (e.g., 'src/**/*.ts').
#
# Example:
#   ./service-dependency-analyzer.sh ./services --service-prefix 'http://user-service' --service-prefix 'http://product-service'
#   ./service-dependency-analyzer.sh . --exclude 'node_modules/*' --output-format json

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PYTHON_SCRIPT="${SCRIPT_DIR}/service-dependency-analyzer.py"

# Check if Python script exists
if [ ! -f "$PYTHON_SCRIPT" ]; then
  echo "Error: Python script '${PYTHON_SCRIPT}' not found." >&2
  exit 1
fi

# Execute the Python script with all arguments passed to this shell script
python3 "$PYTHON_SCRIPT" "$@"

# Check the exit status of the Python script
if [ $? -eq 0 ]; then
  echo "\nService dependency analysis script finished successfully."
else
  echo "\nService dependency analysis script encountered an error." >&2
  exit 1
fi
