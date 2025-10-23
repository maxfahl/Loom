#!/bin/bash

# ng-gen-feature.sh
#
# Purpose:
#   Automates the creation of a new Angular feature (component, service, routing, and test files)
#   with best practices such as standalone components, OnPush change detection, and lazy loading setup.
#   This script aims to reduce boilerplate and ensure consistency across features.
#
# Usage:
#   ./ng-gen-feature.sh <feature-name> [path/to/feature]
#
# Arguments:
#   <feature-name>    : The name of the feature to generate (e.g., 'user-profile', 'product-details').
#                       Will be converted to kebab-case.
#   [path/to/feature] : Optional. The relative path where the feature should be created.
#                       Defaults to 'src/app/features'.
#
# Examples:
#   ./ng-gen-feature.sh user-profile
#   ./ng-gen-feature.sh product-details modules/shop
#
# Configuration:
#   None directly in script; relies on Angular CLI defaults and project structure.
#
# Error Handling:
#   - Exits if feature name is not provided.
#   - Exits if Angular CLI commands fail.
#
# Cross-platform:
#   Designed for Unix-like environments (Linux, macOS, WSL). Requires `ng` (Angular CLI) to be installed and in PATH.

set -e # Exit immediately if a command exits with a non-zero status.

# --- Helper Functions ---

# Function to display script usage
show_help() {
  echo "Usage: $0 <feature-name> [path/to/feature]"
  echo ""
  echo "Arguments:"
  echo "  <feature-name>    : The name of the feature to generate (e.g., 'user-profile')."
  echo "                      Will be converted to kebab-case."
  echo "  [path/to/feature] : Optional. The relative path where the feature should be created."
  echo "                      Defaults to 'src/app/features'."
  echo ""
  echo "Examples:"
  echo "  $0 user-profile"
  echo "  $0 product-details modules/shop"
  echo ""
  echo "This script automates the creation of a new Angular feature with best practices:"
  echo "  - Standalone component with OnPush change detection."
  echo "  - Associated service."
  echo "  - Routing file for lazy loading."
  echo "  - Basic test file for the component."
}

# Function to convert string to kebab-case
kebab_case() {
  echo "$1" | sed -r 's/([A-Z])/-\1/g' | tr '[:upper:]' '[:lower:]' | sed -r 's/^-//'
}

# --- Main Script Logic ---

# Check if Angular CLI is installed
if ! command -v ng &> /dev/null; then
    echo "Error: Angular CLI (ng) is not installed or not in your PATH." >&2
    echo "Please install it globally: npm install -g @angular/cli" >&2
    exit 1
fi

# Parse arguments
if [ -z "$1" ]; then
  echo "Error: Feature name is required." >&2
  show_help
  exit 1
fi

FEATURE_NAME_RAW="$1"
FEATURE_NAME=$(kebab_case "$FEATURE_NAME_RAW")
FEATURE_PATH="${2:-src/app/features}" # Default path if not provided

FULL_FEATURE_DIR="$FEATURE_PATH/$FEATURE_NAME"

echo "Generating Angular feature: '$FEATURE_NAME' in '$FULL_FEATURE_DIR'..."

# 1. Create the feature directory
mkdir -p "$FULL_FEATURE_DIR"
echo "Created directory: $FULL_FEATURE_DIR"

# 2. Generate Standalone Component with OnPush
echo "Generating standalone component..."
ng generate component "$FULL_FEATURE_DIR/$FEATURE_NAME" --standalone --change-detection OnPush --skip-import --skip-selector --flat --skip-tests=false

# Adjust component content for standalone and OnPush
COMPONENT_FILE="$FULL_FEATURE_DIR/$FEATURE_NAME.component.ts"
if [ -f "$COMPONENT_FILE" ]; then
  # Add imports for CommonModule and ChangeDetectionStrategy
  sed -i '' 's|import { Component } from '\''@angular/core'\'';|import { Component, ChangeDetectionStrategy } from '\''@angular/core'\'';\nimport { CommonModule } from '\''@angular/common'\'';|' "$COMPONENT_FILE"
  # Add CommonModule to imports array and set changeDetection
  sed -i '' "s|  standalone: true,|  standalone: true,\n  imports: [CommonModule],\n  changeDetection: ChangeDetectionStrategy.OnPush,|" "$COMPONENT_FILE"
  # Add selector if --skip-selector was used (ng generate component with --flat doesn't add it)
  if ! grep -q "selector:" "$COMPONENT_FILE"; then
    sed -i '' "s|  standalone: true,|  selector: 'app-$FEATURE_NAME',\n  standalone: true,|" "$COMPONENT_FILE"
  fi
  echo "Updated component '$COMPONENT_FILE' for standalone and OnPush."
else
  echo "Warning: Component file '$COMPONENT_FILE' not found. Skipping modifications." >&2
fi

# 3. Generate Service
echo "Generating service..."
ng generate service "$FULL_FEATURE_DIR/$FEATURE_NAME" --flat --skip-tests=false

# 4. Generate Routing File for Lazy Loading
echo "Generating routing file..."
ROUTING_FILE="$FULL_FEATURE_DIR/$FEATURE_NAME.routes.ts"
cat <<EOF > "$ROUTING_FILE"
import { Routes } from '@angular/router';
import { $FEATURE_NAME_RAW^Component } from './$FEATURE_NAME.component';

export const ${FEATURE_NAME_RAW^}Routes: Routes = [
  {
    path: '',
    component: ${FEATURE_NAME_RAW^}Component,
    // Add any child routes here
    children: [
      // { path: 'sub-feature', component: SubFeatureComponent },
    ],
  },
];
EOF
echo "Created routing file: $ROUTING_FILE"

# 5. Update the component's test file to import CommonModule if it's a standalone component
COMPONENT_SPEC_FILE="$FULL_FEATURE_DIR/$FEATURE_NAME.component.spec.ts"
if [ -f "$COMPONENT_SPEC_FILE" ]; then
  sed -i '' "s|import { ComponentFixture, TestBed } from '@angular/core/testing';|import { ComponentFixture, TestBed } from '@angular/core/testing';\nimport { CommonModule } from '@angular/common';|" "$COMPONENT_SPEC_FILE"
  sed -i '' "s|    declarations: [ $FEATURE_NAME_RAW^Component ]|    imports: [ CommonModule, $FEATURE_NAME_RAW^Component ]|" "$COMPONENT_SPEC_FILE"
  echo "Updated component test file '$COMPONENT_SPEC_FILE' for standalone component."
else
  echo "Warning: Component test file '$COMPONENT_SPEC_FILE' not found. Skipping modifications." >&2
fi

echo ""
echo "Feature '$FEATURE_NAME' generated successfully in '$FULL_FEATURE_DIR'."
echo "To lazy load this feature, add the following to your main routing module (e.g., app.routes.ts):"
echo ""
echo "  { "
echo "    path: '$FEATURE_NAME',
    loadChildren: () => import('./$FULL_FEATURE_DIR/$FEATURE_NAME.routes').then(m => m.${FEATURE_NAME_RAW^}Routes)"
echo "  },"
echo ""
