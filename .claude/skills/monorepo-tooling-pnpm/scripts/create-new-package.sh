#!/bin/bash

# create-new-package.sh
# Scaffolds a new package within the pnpm monorepo.
# It creates the necessary directory structure, package.json, tsconfig.json, and a basic src/index.ts.
# It also automatically adds the new package to pnpm-workspace.yaml.

# Usage:
#   ./create-new-package.sh <package_type> <package_name>
#   ./create-new-package.sh app my-new-app
#   ./create-new-package.sh package my-new-lib

# Arguments:
#   <package_type>: 'app' for an application (e.g., in apps/ directory) or 'package' for a library (e.g., in packages/ directory).
#   <package_name>: The kebab-case name of the new package (e.g., my-new-app, my-new-lib).

set -euo pipefail

# --- Configuration ---
ROOT_DIR=$(git rev-parse --show-toplevel || pwd)
PNPM_WORKSPACE_FILE="$ROOT_DIR/pnpm-workspace.yaml"

# --- Helper Functions ---
print_help() {
  echo "Usage: $0 <package_type> <package_name>"
  echo ""
  echo "Scaffolds a new package within the pnpm monorepo."
  echo ""
  echo "Arguments:"
  echo "  <package_type>  Type of package: 'app' (for apps/) or 'package' (for packages/)."
  echo "  <package_name>  Kebab-case name of the new package (e.g., my-new-app, my-new-lib)."
  echo ""
  echo "Example:"
  echo "  $0 app my-dashboard"
  echo "  $0 package shared-components"
  exit 0
}

# --- Main Logic ---

if [[ $# -ne 2 ]]; then
  echo "Error: Incorrect number of arguments."
  print_help
fi

PACKAGE_TYPE="$1"
PACKAGE_NAME="$2"

if [[ "$PACKAGE_TYPE" != "app" && "$PACKAGE_TYPE" != "package" ]]; then
  echo "Error: Invalid package type '$PACKAGE_TYPE'. Must be 'app' or 'package'."
  print_help
fi

TARGET_DIR=""
if [[ "$PACKAGE_TYPE" == "app" ]]; then
  TARGET_DIR="$ROOT_DIR/apps/$PACKAGE_NAME"
else
  TARGET_DIR="$ROOT_DIR/packages/$PACKAGE_NAME"
fi

if [[ -d "$TARGET_DIR" ]]; then
  echo "Error: Package directory '$TARGET_DIR' already exists. Aborting."
  exit 1
fi

echo "Creating new $PACKAGE_TYPE '$PACKAGE_NAME' at '$TARGET_DIR'..."

mkdir -p "$TARGET_DIR/src"

# Create package.json
cat << EOF > "$TARGET_DIR/package.json"
{
  "name": "$PACKAGE_NAME",
  "version": "1.0.0",
  "description": "$PACKAGE_NAME package",
  "main": "src/index.ts",
  "types": "src/index.ts",
  "scripts": {
    "build": "tsc",
    "lint": "eslint . --ext .ts,.tsx",
    "test": "jest"
  },
  "keywords": [],
  "author": "",
  "license": "MIT",
  "dependencies": {},
  "devDependencies": {
    "typescript": "workspace:*",
    "@types/node": "^20.x.x",
    "eslint": "workspace:*",
    "jest": "workspace:*",
    "@types/jest": "^29.x.x"
  }
}
EOF

# Create tsconfig.json
cat << EOF > "$TARGET_DIR/tsconfig.json"
{
  "extends": "../../tsconfig.base.json",
  "compilerOptions": {
    "outDir": "./dist",
    "rootDir": "./src",
    "declaration": true,
    "tsBuildInfoFile": "./node_modules/.tsbuildinfo"
  },
  "include": ["src/**/*.ts", "src/**/*.tsx"],
  "exclude": ["node_modules", "dist"]
}
EOF

# Create a basic src/index.ts
cat << EOF > "$TARGET_DIR/src/index.ts"
export function hello$PACKAGE_NAME() {
  console.log("Hello from $PACKAGE_NAME!");
}
EOF

echo "Adding '$PACKAGE_TYPE/$PACKAGE_NAME' to $PNPM_WORKSPACE_FILE..."
# Add to pnpm-workspace.yaml if not already present
if ! grep -q "- '$PACKAGE_TYPE/$PACKAGE_NAME'" "$PNPM_WORKSPACE_FILE"; then
  echo "  - '$PACKAGE_TYPE/$PACKAGE_NAME'" >> "$PNPM_WORKSPACE_FILE"
  echo "Added to pnpm-workspace.yaml."
else
  echo "Already present in pnpm-workspace.yaml. Skipping."
fi

echo "\nNew package '$PACKAGE_NAME' created successfully!"
echo "Run 'pnpm install' at the monorepo root to link dependencies."
