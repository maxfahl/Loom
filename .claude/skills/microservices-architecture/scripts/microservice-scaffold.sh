#!/bin/bash

# microservice-scaffold.sh
# Wrapper script to scaffold a new microservice project
# using the Python script microservice-scaffold.py.

# Usage:
#   ./microservice-scaffold.sh --name <name> --type <type> [OPTIONS]
#
# Options:
#   --name <name>           Required: The name of the microservice (e.g., 'user-service').
#   --type <type>           Required: The type of microservice to scaffold ('python-flask' or 'node-express').
#   --output-dir <path>     Specify the output directory for the new microservice.
#                           Defaults to './<name>'.
#   --port <number>         Specify the port the service will run on. Defaults to 8080.
#   --dry-run               Print the actions that would be taken without
#                           actually creating or modifying files.
#   --help                  Show this help message and exit.
#
# Example:
#   ./microservice-scaffold.sh --name product-catalog --type python-flask --port 5000
#   ./microservice-scaffold.sh --name order-processor --type node-express --output-dir ./services
#   ./microservice-scaffold.sh --name test-service --type python-flask --dry-run

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PYTHON_SCRIPT="${SCRIPT_DIR}/microservice-scaffold.py"

# Check if Python script exists
if [ ! -f "$PYTHON_SCRIPT" ]; then
  echo "Error: Python script '${PYTHON_SCRIPT}' not found." >&2
  exit 1
fi

# Execute the Python script with all arguments passed to this shell script
python3 "$PYTHON_SCRIPT" "$@"

# Check the exit status of the Python script
if [ $? -eq 0 ]; then
  echo "\nMicroservice scaffolding script finished successfully."
else
  echo "\nMicroservice scaffolding script encountered an error." >&2
  exit 1
fi
