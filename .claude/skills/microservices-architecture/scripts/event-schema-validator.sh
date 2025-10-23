#!/bin/bash

# event-schema-validator.sh
# Wrapper script to validate a JSON event against a JSON schema
# using the Python script event-schema-validator.py.

# Usage:
#   ./event-schema-validator.sh --event-file <path> --schema-file <path> [OPTIONS]
#
# Options:
#   --event-file <path>     Required: Path to the JSON file containing the event data.
#   --schema-file <path>    Required: Path to the JSON schema file for validation.
#   --dry-run               Print the actions that would be taken without
#                           actually performing validation.
#   --help                  Show this help message and exit.
#
# Example:
#   ./event-schema-validator.sh --event-file ./events/order_created.json --schema-file ./schemas/order_created_schema.json
#   ./event-schema-validator.sh --event-file ./events/user_updated.json --schema-file ./schemas/user_schema.json --dry-run

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PYTHON_SCRIPT="${SCRIPT_DIR}/event-schema-validator.py"

# Check if Python script exists
if [ ! -f "$PYTHON_SCRIPT" ]; then
  echo "Error: Python script '${PYTHON_SCRIPT}' not found." >&2
  exit 1
fi

# Execute the Python script with all arguments passed to this shell script
python3 "$PYTHON_SCRIPT" "$@"

# Check the exit status of the Python script
if [ $? -eq 0 ]; then
  echo "\nEvent schema validation script finished successfully."
else
  echo "\nEvent schema validation script encountered an error." >&2
  exit 1
fi
