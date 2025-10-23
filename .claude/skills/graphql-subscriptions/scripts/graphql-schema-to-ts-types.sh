#!/bin/bash

# graphql-schema-to-ts-types.sh
#
# Description:
#   Generates TypeScript types from a GraphQL schema file using `graphql-codegen`.
#   This ensures type safety across client and server for GraphQL operations,
#   including queries, mutations, and subscriptions.
#
# Usage:
#   ./graphql-schema-to-ts-types.sh --schema ./common/schema.graphql --output ./common/graphql-types.ts
#   ./graphql-schema-to-ts-types.sh --help
#
# Arguments:
#   --schema, -s : Required. Path to the GraphQL schema file (e.g., schema.graphql).
#   --output, -o : Required. Path for the generated TypeScript types file (e.g., graphql-types.ts).
#
# Prerequisites:
#   - Node.js and npm/yarn
#   - graphql-codegen: Must be installed in your project (npm install @graphql-codegen/cli @graphql-codegen/typescript @graphql-codegen/typescript-operations)
#
# Example:
#   # Generate types from a schema file
#   ./graphql-schema-to-ts-types.sh -s ./common/schema.graphql -o ./common/graphql-types.ts
#
#   # Ensure graphql-codegen is installed in your project:
#   # npm install --save-dev @graphql-codegen/cli @graphql-codegen/typescript @graphql-codegen/typescript-operations

set -euo pipefail

# --- Configuration Defaults ---
SCHEMA_FILE=""
OUTPUT_FILE=""

# --- Helper Functions ---

print_help() {
    echo "Usage: $0 --schema <SCHEMA_FILE> --output <OUTPUT_FILE>"
    echo "       $0 --help"
    echo ""
    echo "Arguments:"
    echo "  --schema, -s : Required. Path to the GraphQL schema file (e.g., schema.graphql)."
    echo "  --output, -o : Required. Path for the generated TypeScript types file (e.g., graphql-types.ts)."
    echo ""
    echo "Description:"
    echo "  Generates TypeScript types from a GraphQL schema file using `graphql-codegen`."
    echo "  This ensures type safety across client and server for GraphQL operations,"
    echo "  including queries, mutations, and subscriptions."
    echo ""
    echo "Prerequisites:"
    echo "  - Node.js and npm/yarn"
    echo "  - graphql-codegen: Must be installed in your project (npm install @graphql-codegen/cli @graphql-codegen/typescript @graphql-codegen/typescript-operations)"
    echo ""
    echo "Example:"
    echo "  ./graphql-schema-to-ts-types.sh -s ./common/schema.graphql -o ./common/graphql-types.ts"
}

log_info() {
    echo -e "\033[0;34m[INFO]\033[0m $1"
}

log_success() {
    echo -e "\033[0;32m[SUCCESS]\033[0m $1"
}

log_error() {
    echo -e "\033[0;31m[ERROR]\033[0m $1" >&2
}

# --- Argument Parsing ---

while [[ $# -gt 0 ]]; do
    key="$1"
    case $key in
        -s|--schema)
        SCHEMA_FILE="$2"
        shift # past argument
        shift # past value
        ;;
        -o|--output)
        OUTPUT_FILE="$2"
        shift # past argument
        shift # past value
        ;;
        --help)
        print_help
        exit 0
        ;;
        *)
        log_error "Unknown option: $1"
        print_help
        exit 1
        ;;
    esac
done

# --- Validation ---

if [[ -z "$SCHEMA_FILE" ]]; then
    log_error "Error: --schema is required."
    print_help
    exit 1
fi

if [[ -z "$OUTPUT_FILE" ]]; then
    log_error "Error: --output is required."
    print_help
    exit 1
fi

if [[ ! -f "$SCHEMA_FILE" ]]; then
    log_error "Error: Schema file not found at '$SCHEMA_FILE'."
    exit 1
fi

if ! command -v graphql-codegen &> /dev/null; then
    log_error "Error: graphql-codegen is not installed or not in PATH."
    log_error "Please install it in your project: npm install --save-dev @graphql-codegen/cli @graphql-codegen/typescript @graphql-codegen/typescript-operations"
    exit 1
fi

# --- Main Logic ---

log_info "Generating codegen.yml configuration file..."
cat << EOF > codegen.yml
overwrite: true
schema: "${SCHEMA_FILE}"
documents: "./**/*.graphql" # Adjust if you have client-side GraphQL documents
generates:
  "${OUTPUT_FILE}":
    plugins:
      - "typescript"
      - "typescript-operations"
    config:
      skipTypename: true
      enumsAsTypes: true
      scalars:
        DateTime: string
        JSON: any
EOF

log_info "Running graphql-codegen to generate TypeScript types..."
# Ensure the output directory exists
mkdir -p "$(dirname "${OUTPUT_FILE}")"

graphql-codegen --config codegen.yml || { log_error "Failed to generate GraphQL types."; exit 1; }

log_success "TypeScript types generated successfully to ${OUTPUT_FILE}"
log_info "You can now remove the temporary codegen.yml file if desired."
rm codegen.yml || true # Clean up codegen.yml, ignore error if it doesn't exist
