#!/bin/bash

set -e

show_help() {
  echo "Usage: $0 <feature-name> [path/to/feature]"
  echo "Automates the creation of a new Angular feature module."
}

kebab_case() {
  echo "$1" | sed -e 's/ /-/g' -e 's/\([A-Z]\)/-\1/g' -e 's/^-//' | tr '[:upper:]' '[:lower:]'
}

pascal_case() {
  echo "$1" | perl -pe 's/(^|-)(\w)/\U$2/g; s/-//g'
}

if ! command -v ng &> /dev/null; then
    echo "Error: Angular CLI (ng) is not installed or not in your PATH." >&2
    exit 1
fi

if [ -z "$1" ]; then
  echo "Error: Feature name is required." >&2
  show_help
  exit 1
fi

FEATURE_NAME_RAW="$1"
FEATURE_NAME_KEBAB=$(kebab_case "$FEATURE_NAME_RAW")
FEATURE_NAME_PASCAL=$(pascal_case "$FEATURE_NAME_KEBAB")
FEATURE_PATH="${2:-src/app/features}"

FULL_FEATURE_DIR="$FEATURE_PATH/$FEATURE_NAME_KEBAB"

echo "Generating Angular feature: '$FEATURE_NAME_KEBAB' in '$FULL_FEATURE_DIR'..."

mkdir -p "$FULL_FEATURE_DIR"
echo "Created directory: $FULL_FEATURE_DIR"

COMPONENT_PATH="$FULL_FEATURE_DIR/$FEATURE_NAME_KEBAB"
ng generate component "$COMPONENT_PATH" --standalone --change-detection OnPush --skip-import --flat

COMPONENT_FILE="${COMPONENT_PATH}.component.ts"
if [ -f "$COMPONENT_FILE" ]; then
  sed -i.bak "s|import { Component } from '@angular/core';|import { Component, ChangeDetectionStrategy } from '@angular/core';\nimport { CommonModule } from '@angular/common';|" "$COMPONENT_FILE"
  sed -i.bak "s|standalone: true,|standalone: true,\n  imports: [CommonModule],\n  selector: 'app-${FEATURE_NAME_KEBAB}',\n  changeDetection: ChangeDetectionStrategy.OnPush,|" "$COMPONENT_FILE"
  rm "${COMPONENT_FILE}.bak"
  echo "Updated component '$COMPONENT_FILE' for standalone and OnPush."
fi

ng generate service "$FULL_FEATURE_DIR/$FEATURE_NAME_KEBAB" --flat

ROUTING_FILE="$FULL_FEATURE_DIR/$FEATURE_NAME_KEBAB.routes.ts"
ROUTES_CLASS_NAME="${FEATURE_NAME_PASCAL}Routes"
COMPONENT_CLASS_NAME="${FEATURE_NAME_PASCAL}Component"

ROUTING_CONTENT="import { Routes } from '@angular/router';\nimport { ${COMPONENT_CLASS_NAME} } from './${FEATURE_NAME_KEBAB}.component';\n\nexport const ${ROUTES_CLASS_NAME}: Routes = [\n  {\n    path: '',\n    component: ${COMPONENT_CLASS_NAME},\n    children: [],\n  },\n];\n"
echo -e "$ROUTING_CONTENT" > "$ROUTING_FILE"
echo "Created routing file: $ROUTING_FILE"



echo ""
echo "Feature '$FEATURE_NAME_KEBAB' generated successfully."
