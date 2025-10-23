#!/bin/bash

# api-resource-generator.sh
# Wrapper script to generate boilerplate code for a new API resource
# using the Python script api-resource-generator.py.

# Usage:
#   ./api-resource-generator.sh --resource <name> --fields <json_string> [OPTIONS]
#
# Options:
#   --resource <name>       Required: The name of the API resource (e.g., 'User', 'Product').
#   --fields <json_string>  Required: JSON string of fields for the resource.
#                           Example: '[{"name":"id","type":"string","format":"uuid"},{"name":"name","type":"string"}]'.
#   --output-dir <path>     Specify the output directory for the generated files.
#                           Defaults to './src/resources'.
#   --dry-run               Print the actions that would be taken without
#                           actually creating or modifying files.
#   --help                  Show this help message and exit.
#
# Example:
#   ./api-resource-generator.sh --resource Product --fields '[{"name":"id","type":"string","format":"uuid"},{"name":"name","type":"string"},{"name":"price","type":"number","format":"float"}]' --output-dir ./src/api/v1/resources
#   ./api-resource-generator.sh --resource User --fields '[{"name":"id","type":"string","format":"uuid"},{"name":"email","type":"string"},{"name":"password","type":"string"}]'

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PYTHON_SCRIPT="${SCRIPT_DIR}/api-resource-generator.py"

# Check if Python script exists
if [ ! -f "$PYTHON_SCRIPT" ]; then
  echo "Error: Python script '${PYTHON_SCRIPT}' not found." >&2
  exit 1
fi

# Execute the Python script with all arguments passed to this shell script
python3 "$PYTHON_SCRIPT" "$@"

# Check the exit status of the Python script
if [ $? -eq 0 ]; then
  echo "\nAPI resource generation script finished successfully."
else
  echo "\nAPI resource generation script encountered an error." >&2
  exit 1
fi
