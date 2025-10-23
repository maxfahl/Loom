#!/bin/bash

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"

show_help() {
  echo "Usage: $0 <resource-name> [path/to/services]"
  echo "Generates a boilerplate Angular API client service and interface."
}

kebab_case() {
  echo "$1" | sed -e 's/\([A-Z]\)/-\1/g' -e 's/^-//' | tr '[:upper:]' '[:lower:]'
}

pascal_case() {
  echo "$1" | perl -pe 's/(^|-)(\w)/\U$2/g; s/-//g'
}

if ! command -v ng &> /dev/null; then
    echo "Error: Angular CLI (ng) is not installed or not in your PATH." >&2
    exit 1
fi

if [ -z "$1" ]; then
  echo "Error: Resource name is required." >&2
  show_help
  exit 1
fi

RESOURCE_NAME_RAW="$1"
RESOURCE_NAME_KEBAB=$(kebab_case "$RESOURCE_NAME_RAW")
RESOURCE_NAME_PASCAL=$(pascal_case "$RESOURCE_NAME_KEBAB")
SERVICE_PATH="${2:-src/app/core/services}"

FULL_SERVICE_DIR="$SERVICE_PATH"
SERVICE_FILE_NAME="$RESOURCE_NAME_KEBAB.service"

echo "Generating Angular API client for resource: '$RESOURCE_NAME_RAW' in '$FULL_SERVICE_DIR'..."

ng generate service "$FULL_SERVICE_DIR/$SERVICE_FILE_NAME" --flat --skip-tests=true

SERVICE_FILE="$FULL_SERVICE_DIR/$SERVICE_FILE_NAME.ts"
INTERFACE_FILE="$FULL_SERVICE_DIR/$RESOURCE_NAME_KEBAB.interface.ts"

# Create interface file
INTERFACE_CONTENT="export interface I${RESOURCE_NAME_PASCAL} {\n  id: string;\n  name: string;\n}\n\nexport interface ICreate${RESOURCE_NAME_PASCAL} extends Omit<I${RESOURCE_NAME_PASCAL}, 'id'> {}\nexport interface IUpdate${RESOURCE_NAME_PASCAL} extends Partial<ICreate${RESOURCE_NAME_PASCAL}> {}\n"
echo -e "$INTERFACE_CONTENT" > "$INTERFACE_FILE"
echo "Created interface file: $INTERFACE_FILE"

# Create service file from template
if [ -f "$SERVICE_FILE" ]; then
  TEMPLATE_FILE="$SCRIPT_DIR/ng-api-client-gen.service.template"
  
  if [ ! -f "$TEMPLATE_FILE" ]; then
    echo "Error: Template file not found at $TEMPLATE_FILE" >&2
    exit 1
  fi

  cat "$TEMPLATE_FILE" | \
    sed "s/__RESOURCE_PASCAL_CASE__/${RESOURCE_NAME_PASCAL}/g" | \
    sed "s/__RESOURCE_KEBAB_CASE__/${RESOURCE_NAME_KEBAB}/g" > "$SERVICE_FILE"

  echo "Updated service '$SERVICE_FILE' from template."
else
  echo "Warning: Service file '$SERVICE_FILE' not found after ng generate. Skipping modifications." >&2
fi

echo "API client for '$RESOURCE_NAME_RAW' generated successfully."