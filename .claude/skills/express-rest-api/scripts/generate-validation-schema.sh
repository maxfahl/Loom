#!/bin/bash

# generate-validation-schema.sh
#
# Purpose: Generates a basic Zod validation schema for a given resource.
#          This script helps developers quickly scaffold validation logic for API requests.
#
# Usage: ./generate-validation-schema.sh <SchemaName>
#   <SchemaName>: The name of the schema (e.g., User, Product, Post).
#                 The script will convert this to kebab-case for filenames and PascalCase for the schema object.
#
# Example:
#   ./generate-validation-schema.sh User
#   This will create:
#     - src/validation/userValidation.ts
#
# Configuration:
#   - BASE_DIR: The base directory of the Express.js project (e.g., where src/ is located). Defaults to current directory.
#
# Error Handling:
#   - Checks if a schema name is provided.
#   - Checks if the schema file already exists to prevent accidental overwrites.
#   - Provides informative messages for success or failure.

# --- Configuration ---
BASE_DIR="."
# --- End Configuration ---

# --- Utility Functions ---

# Function to convert PascalCase to kebab-case
pascal_to_kebab() {
  echo "$1" | sed -r 's/([A-Z])/-\\L\\1/g' | sed -r 's/^-//'
}

# Function to convert kebab-case to PascalCase
kebab_to_pascal() {
  echo "$1" | sed -r 's/(^|-)([a-z])/\\U\\1\\2/g'
}

# --- Main Script Logic ---

# Check if schema name is provided
if [ -z "$1" ]; then
  echo "❌ Error: Please provide a name for your validation schema."
  echo "Usage: ./generate-validation-schema.sh <SchemaName>"
  exit 1
fi

SCHEMA_NAME_PASCAL=$(kebab_to_pascal "$1")
SCHEMA_NAME_KEBAB=$(pascal_to_kebab "$SCHEMA_NAME_PASCAL")

VALIDATION_FILE="$BASE_DIR/src/validation/${SCHEMA_NAME_KEBAB}Validation.ts"

# Check if validation file already exists
if [ -f "$VALIDATION_FILE" ]; then
  echo "⚠️ Warning: Validation schema '$SCHEMA_NAME_PASCAL' already exists at '$VALIDATION_FILE'."
  read -p "Do you want to overwrite it? (y/N): " OVERWRITE
  if [[ ! "$OVERWRITE" =~ ^[yY]$ ]]; then
    echo "Aborting schema generation."
    exit 0
  fi
  echo "Overwriting existing schema..."
fi

# Create validation directory if it doesn't exist
mkdir -p "$BASE_DIR/src/validation" || { echo "❌ Error: Failed to create directory '$BASE_DIR/src/validation'."; exit 1; }

# Create validation schema file content
cat << EOF > "$VALIDATION_FILE"
import { Request, Response, NextFunction } from 'express';
import { z } from 'zod';

// Define Zod schema for ${SCHEMA_NAME_PASCAL} creation and update
export const ${SCHEMA_NAME_KEBAB}Schema = z.object({
  // Example fields: Customize these based on your resource
  name: z.string().min(3, 'Name must be at least 3 characters'),
  email: z.string().email('Invalid email address').optional(),
  age: z.number().int().positive('Age must be a positive integer').optional(),
  isActive: z.boolean().default(true),
});

// Infer the TypeScript type from the schema
export type ${SCHEMA_NAME_PASCAL}Input = z.infer<typeof ${SCHEMA_NAME_KEBAB}Schema>;

export const validate${SCHEMA_NAME_PASCAL} = (req: Request, res: Response, next: NextFunction) => {
  try {
    ${SCHEMA_NAME_KEBAB}Schema.parse(req.body);
    next();
  } catch (error: any) {
    res.status(400).json({
      status: 'error',
      statusCode: 400,
      message: 'Validation failed',
      errors: error.errors,
    });
  }
};
EOF

echo "✅ Successfully created validation schema '$SCHEMA_NAME_PASCAL' at '$VALIDATION_FILE'."
echo "Remember to import and use this validation middleware in your routes."
