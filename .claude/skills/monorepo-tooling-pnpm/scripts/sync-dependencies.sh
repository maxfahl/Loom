#!/bin/bash

# sync-dependencies.sh
# Synchronizes common development dependencies (e.g., typescript, eslint) from the root package.json
# to all workspace packages, ensuring consistency and proper workspace protocol usage.

# Usage:
#   ./sync-dependencies.sh
#   ./sync-dependencies.sh --dry-run

# Requirements:
#   - pnpm: Must be installed and configured for the monorepo.
#   - jq: A lightweight and flexible command-line JSON processor.

set -euo pipefail

# --- Configuration ---
ROOT_DIR=$(git rev-parse --show-toplevel || pwd)
ROOT_PACKAGE_JSON="$ROOT_DIR/package.json"
PNPM_WORKSPACE_FILE="$ROOT_DIR/pnpm-workspace.yaml"
DRY_RUN=false

# List of dev dependencies to synchronize from root to all packages
# These should typically be tools that are used consistently across the monorepo.
DEV_DEPS_TO_SYNC=("typescript" "eslint" "prettier" "jest" "@types/node" "@types/jest" "@types/react")

# --- Helper Functions ---
print_help() {
  echo "Usage: $0 [--dry-run]"
  echo ""
  echo "Synchronizes common development dependencies from the root package.json to all workspace packages."
  echo "Ensures consistency and proper workspace protocol usage for specified dev dependencies."
  echo ""
  echo "Options:"
  echo "  --dry-run  Show what changes would be made without actually modifying files."
  echo "  -h, --help Display this help message."
  echo ""
  echo "Example:"
  echo "  $0"
  echo "  $0 --dry-run"
  exit 0
}

# Function to check for required commands
check_dependencies() {
  if ! command -v pnpm &> /dev/null;
  then
    echo "Error: 'pnpm' is not installed. Please install it to run this script."
    echo "  Refer to: https://pnpm.io/installation"
    exit 1
  fi
  if ! command -v jq &> /dev/null;
  then
    echo "Error: 'jq' is not installed. Please install it to run this script."
    echo "  On macOS: brew install jq"
    echo "  On Debian/Ubuntu: sudo apt-get install jq"
    exit 1
  fi
}

# --- Main Logic ---

# Parse arguments
while [[ $# -gt 0 ]]; do
  key="$1"
  case $key in
    --dry-run)
      DRY_RUN=true
      shift # past argument
      ;;
    -h|--help)
      print_help
      ;;
    *)
      echo "Unknown option: $1"
      print_help
      ;;
  esac
done

check_dependencies

if [[ ! -f "$ROOT_PACKAGE_JSON" ]]; then
  echo "Error: Root package.json not found at '$ROOT_PACKAGE_JSON'."
  exit 1
fi

if [[ ! -f "$PNPM_WORKSPACE_FILE" ]]; then
  echo "Error: pnpm-workspace.yaml not found at '$PNPM_WORKSPACE_FILE'."
  exit 1
fi

if $DRY_RUN; then
  echo "Running in DRY-RUN mode. No files will be modified.\n"
fi

echo "Synchronizing common development dependencies..."

# Get root dev dependencies
ROOT_DEV_DEPS_JSON=$(jq '.devDependencies' "$ROOT_PACKAGE_JSON")

# Get list of workspace packages
WORKSPACE_PACKAGES=()
while IFS= read -r line; do
  # Extract package paths from pnpm-workspace.yaml, handling glob patterns
  # This is a simplified approach; a more robust solution might use 'pnpm recursive ls --json'
  if [[ $line =~ ^[[:space:]]*-['|'](.*)['|'] ]]; then
    GLOB_PATTERN="${BASH_REMATCH[1]}"
    # Expand glob patterns to actual directories
    for dir in $(find "$ROOT_DIR" -type d -path "${ROOT_DIR}/${GLOB_PATTERN//\*/*}" 2>/dev/null);
    do
      if [[ -f "$dir/package.json" ]]; then
        WORKSPACE_PACKAGES+=("$dir")
      fi
    done
  fi
done < "$PNPM_WORKSPACE_FILE"

# Ensure uniqueness and sort
IFS=$'\n' WORKSPACE_PACKAGES=($(sort -u <<<"${WORKSPACE_PACKAGES[*]}"))
unset IFS

if [[ ${#WORKSPACE_PACKAGES[@]} -eq 0 ]]; then
  echo "No workspace packages found. Exiting."
  exit 0
fi

for PACKAGE_PATH in "${WORKSPACE_PACKAGES[@]}"; do
  PACKAGE_NAME=$(basename "$PACKAGE_PATH")
  PACKAGE_PACKAGE_JSON="$PACKAGE_PATH/package.json"

  if [[ ! -f "$PACKAGE_PACKAGE_JSON" ]]; then
    echo "Warning: package.json not found for '$PACKAGE_NAME' at '$PACKAGE_PACKAGE_JSON'. Skipping."
    continue
  fi

  echo "\nProcessing package: '$PACKAGE_NAME'"
  CURRENT_PACKAGE_JSON_CONTENT=$(cat "$PACKAGE_PACKAGE_JSON")
  UPDATED_PACKAGE_JSON_CONTENT="$CURRENT_PACKAGE_JSON_CONTENT"
  CHANGES_MADE=false

  for DEP_NAME in "${DEV_DEPS_TO_SYNC[@]}"; do
    ROOT_DEP_VERSION=$(echo "$ROOT_DEV_DEPS_JSON" | jq -r ".""$DEP_NAME"" // null)

    if [[ "$ROOT_DEP_VERSION" != "null" ]]; then
      CURRENT_DEP_VERSION=$(echo "$CURRENT_PACKAGE_JSON_CONTENT" | jq -r ".devDependencies.""$DEP_NAME"" // null)

      if [[ "$CURRENT_DEP_VERSION" != "workspace:*" ]]; then
        echo "  - Updating '$DEP_NAME' to 'workspace:*' in '$PACKAGE_NAME'"
        UPDATED_PACKAGE_JSON_CONTENT=$(echo "$UPDATED_PACKAGE_JSON_CONTENT" | jq ".devDependencies.""$DEP_NAME"" = "workspace:*"")
        CHANGES_MADE=true
      else
        echo "  - '$DEP_NAME' is already 'workspace:*' in '$PACKAGE_NAME'. Skipping."
      fi
    fi
  done

  if $CHANGES_MADE; then
    if $DRY_RUN; then
      echo "  (Dry Run) Would update '$PACKAGE_PACKAGE_JSON'."
      # echo "--- Proposed changes for $PACKAGE_NAME ---"
      # diff -u <(echo "$CURRENT_PACKAGE_JSON_CONTENT") <(echo "$UPDATED_PACKAGE_JSON_CONTENT") || true
      # echo "---------------------------------------"
    else
      echo "  Updating '$PACKAGE_PACKAGE_JSON'..."
      echo "$UPDATED_PACKAGE_JSON_CONTENT" > "$PACKAGE_PACKAGE_JSON"
    fi
  else
    echo "  No changes needed for '$PACKAGE_NAME'."
  fi
done

if $DRY_RUN; then
  echo "\nSynchronization dry run complete. No files were modified."
else
  echo "\nSynchronization complete. Run 'pnpm install' at the monorepo root to apply changes."
fi
