#!/bin/bash

# api-spec-generator.sh
# Wrapper script to generate a basic OpenAPI (Swagger) specification YAML file
# using the Python script api-spec-generator.py.

# Usage:
#   ./api-spec-generator.sh --resource <name> --fields <json_string> [OPTIONS]
#
# Options:
#   --resource <name>       Required: The name of the API resource (e.g., 'User', 'Product').
#   --fields <json_string>  Required: JSON string of fields for the resource.
#                           Example: '[{"name":"id","type":"string","format":"uuid"},{"name":"name","type":"string"}]'.
#   --output-file <path>    Specify the output YAML file path. Defaults to './openapi.yaml'.
#   --dry-run               Print the actions that would be taken without
#                           actually creating or modifying files.
#   --help                  Show this help message and exit.
#
# Example:
#   ./api-spec-generator.sh --resource Product --fields '[{"name":"id","type":"string","format":"uuid"},{"name":"name","type":"string"},{"name":"price","type":"number","format":"float"},{"name":"description","type":"string","nullable":true}]' --output-file ./product_api.yaml
#   ./api-spec-generator.sh --resource Order --fields '[{"name":"id","type":"string","format":"uuid"},{"name":"userId","type":"string"},{"name":"total","type":"number"}]'

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PYTHON_SCRIPT="${SCRIPT_DIR}/api-spec-generator.py"

# Check if Python script exists
if [ ! -f "$PYTHON_SCRIPT" ]; then
  echo "Error: Python script '${PYTHON_SCRIPT}' not found." >&2
  exit 1
fi

# Execute the Python script with all arguments passed to this shell script
python3 "$PYTHON_SCRIPT" "$@"

# Check the exit status of the Python script
if [ $? -eq 0 ]; then
  echo "\nAPI spec generation script finished successfully."
else
  echo "\nAPI spec generation script encountered an error." >&2
  exit 1
fi
