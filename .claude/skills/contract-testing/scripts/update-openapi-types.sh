#!/bin/bash

# update-openapi-types.sh
#
# Automates the generation/update of TypeScript types from an OpenAPI specification
# using the `openapi-typescript` tool. This helps keep your frontend types in sync
# with your backend API definitions.
#
# Usage:
#   ./update-openapi-types.sh -s ./path/to/your/openapi.yaml -o ./src/api-types.ts
#   ./update-openapi-types.sh --spec-file ../backend/openapi.json --output-file ./src/generated/api.d.ts
#
# Requirements:
#   - Node.js and npm/yarn installed.
#   - `openapi-typescript` package installed globally (`npm install -g openapi-typescript`)
#     or as a dev dependency in your project (`npm install --save-dev openapi-typescript`).
#
# Options:
#   -s, --spec-file    : Path to the OpenAPI specification file (YAML or JSON).
#   -o, --output-file  : Path for the generated TypeScript output file.
#   -h, --help         : Display this help message.

# --- Configuration ---
# You can set a default path to openapi-typescript if it's not in your PATH
# OPENAPI_TYPESCRIPT_BIN="$(npm bin)/openapi-typescript"
OPENAPI_TYPESCRIPT_BIN="openapi-typescript"

# --- Functions ---
function display_help() {
  echo "Usage: $(basename "$0") [OPTIONS]"
  echo ""
  echo "Automates the generation/update of TypeScript types from an OpenAPI specification."
  echo ""
  echo "Options:"
  echo "  -s, --spec-file <file>   Path to the OpenAPI specification file (YAML or JSON). (Required)"
  echo "  -o, --output-file <file> Path for the generated TypeScript output file. (Required)"
  echo "  -h, --help               Display this help message."
  echo ""
  echo "Example:"
  echo "  $(basename "$0") -s ../backend/openapi.yaml -o ./src/generated/api.d.ts"
  exit 0
}

function error_exit() {
  echo -e "\033[0;31mError: $1\033[0m" >&2
  exit 1
}

# --- Main Script ---

SPEC_FILE=""
OUTPUT_FILE=""

# Parse command-line arguments
while (( "$#" )); do
  case "$1" in
    -s|--spec-file)
      if [ -n "$2" ] && [ "${2:0:1}" != "-" ]; then
        SPEC_FILE="$2"
        shift 2
      else
        error_exit "Argument for $1 is missing or invalid."
      fi
      ;;
    -o|--output-file)
      if [ -n "$2" ] && [ "${2:0:1}" != "-" ]; then
        OUTPUT_FILE="$2"
        shift 2
      else
        error_exit "Argument for $1 is missing or invalid."
      fi
      ;;
    -h|--help)
      display_help
      ;;
    -*|--*=)
      error_exit "Unsupported option $1"
      ;;
    *)
      break
      ;;
  esac
done

# Validate required arguments
if [ -z "$SPEC_FILE" ]; then
  error_exit "OpenAPI specification file (--spec-file) is required."
fi

if [ -z "$OUTPUT_FILE" ]; then
  error_exit "Output TypeScript file (--output-file) is required."
fi

# Check if spec file exists
if [ ! -f "$SPEC_FILE" ]; then
  error_exit "OpenAPI specification file not found: $SPEC_FILE"
fi

# Create output directory if it doesn't exist
OUTPUT_DIR=$(dirname "$OUTPUT_FILE")
if [ ! -d "$OUTPUT_DIR" ]; then
  echo "Creating output directory: $OUTPUT_DIR"
  mkdir -p "$OUTPUT_DIR" || error_exit "Failed to create output directory: $OUTPUT_DIR"
fi

echo "Generating TypeScript types from $SPEC_FILE to $OUTPUT_FILE..."

# Execute openapi-typescript command
# Add any common flags you use, e.g., --prettier, --immutable-types
"$OPENAPI_TYPESCRIPT_BIN" "$SPEC_FILE" --output "$OUTPUT_FILE" \
  || error_exit "Failed to generate TypeScript types. Is 'openapi-typescript' installed and in your PATH?"

echo -e "\033[0;32mSuccessfully generated TypeScript types.\033[0m"
