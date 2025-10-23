#!/bin/bash

# generate-model.sh
#
# Purpose:
#   Scaffolds a new Prisma model definition in 'schema.prisma' with common fields.
#   This script helps automate the creation of boilerplate model structures,
#   including 'id', 'createdAt', 'updatedAt', and an optional 'deletedAt' field
#   for soft deletes.
#
# Usage:
#   bash scripts/generate-model.sh <ModelName> [--soft-delete]
#
# Arguments:
#   <ModelName>    : The name of the model to create (e.g., User, Product, OrderItem).
#                    Will be converted to PascalCase.
#   --soft-delete  : Optional. If present, adds a 'deletedAt' field to the model
#                    for soft deletion functionality.
#
# Examples:
#   bash scripts/generate-model.sh Post
#   bash scripts/generate-model.sh Comment --soft-delete
#
# Requirements:
#   - 'schema.prisma' file must exist in the 'prisma/' directory relative to the script's execution.
#   - 'sed' command-line utility (standard on most Unix-like systems).
#
# Error Handling:
#   - Exits if no model name is provided.
#   - Exits if 'schema.prisma' is not found.
#   - Informs the user if the model already exists.

set -euo pipefail

# --- Configuration ---
PRISMA_SCHEMA_PATH="./prisma/schema.prisma" # Adjust if your schema.prisma is elsewhere

# --- Functions ---

# Function to convert string to PascalCase
to_pascal_case() {
  echo "$1" | sed -r 's/(^|_)([a-z])/\U\2/g'
}

# Function to display help message
display_help() {
  echo "Usage: bash $(basename "$0") <ModelName> [--soft-delete]"
  echo ""
  echo "Arguments:"
  echo "  <ModelName>    The name of the model to create (e.g., User, Product)."
  echo "                 Will be converted to PascalCase."
  echo "  --soft-delete  Optional. Adds a 'deletedAt' field for soft deletion."
  echo ""
  echo "Examples:"
  echo "  bash $(basename "$0") Post"
  echo "  bash $(basename "$0") Comment --soft-delete"
  echo ""
  echo "This script scaffolds a new Prisma model definition in '$PRISMA_SCHEMA_PATH'."
  exit 0
}

# --- Main Script Logic ---

# Check for help flag
if [[ "$#" -gt 0 && "$1" == "--help" ]]; then
  display_help
fi

# Validate arguments
if [[ "$#" -lt 1 ]]; then
  echo "Error: No model name provided." >&2
  display_help
fi

MODEL_NAME_RAW="$1"
MODEL_NAME=$(to_pascal_case "$MODEL_NAME_RAW")
SOFT_DELETE=0

if [[ "$#" -gt 1 && "$2" == "--soft-delete" ]]; then
  SOFT_DELETE=1
fi

echo "Attempting to generate Prisma model: $MODEL_NAME"

# Check if schema.prisma exists
if [[ ! -f "$PRISMA_SCHEMA_PATH" ]]; then
  echo "Error: '$PRISMA_SCHEMA_PATH' not found. Please ensure it exists." >&2
  exit 1
fi

# Check if model already exists in schema.prisma
if grep -q "model $MODEL_NAME {" "$PRISMA_SCHEMA_PATH"; then
  echo "Warning: Model '$MODEL_NAME' already exists in '$PRISMA_SCHEMA_PATH'. Skipping creation."
  exit 0
fi

# Construct the model definition
MODEL_DEFINITION="
model $MODEL_NAME {
  id        Int      @id @default(autoincrement())
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt"

if [[ "$SOFT_DELETE" -eq 1 ]]; then
  MODEL_DEFINITION+="
  deletedAt DateTime?"
fi

MODEL_DEFINITION+="
  // Add your fields here
}
"

# Append the new model definition to schema.prisma
echo "$MODEL_DEFINITION" >> "$PRISMA_SCHEMA_PATH"

echo "Successfully added model '$MODEL_NAME' to '$PRISMA_SCHEMA_PATH'."
echo "Remember to run 'npx prisma format' and 'npx prisma migrate dev' to apply changes."
