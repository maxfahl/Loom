#!/bin/bash

# generate-composable.sh
#
# Purpose:
#   Automates the creation of a new Vue 3 composable function with TypeScript,
#   including a basic structure and an optional test file.
#   This script helps maintain consistency and speeds up development of reusable logic.
#
# Usage:
#   ./generate-composable.sh <ComposableName> [options]
#
# Options:
#   -p, --path <path>     Specify the directory to create the composable in.
#                         Defaults to 'src/composables'.
#   -t, --with-test       Generate an accompanying Vitest test file.
#   -h, --help            Display this help message.
#
# Examples:
#   ./generate-composable.sh useCounter
#   ./generate-composable.sh useAuth -p src/features/auth
#   ./generate-composable.sh useLocalStorage --with-test
#
# Requirements:
#   - Bash shell
#
# Output:
#   - Creates use<ComposableName>.ts and optionally use<ComposableName>.test.ts files.
#   - Prints messages indicating success or failure.

# --- Configuration ---
DEFAULT_COMPOSABLE_PATH="src/composables"
DEFAULT_TEST_PATH="src/composables" # Can be adjusted if tests are in a separate top-level directory

# --- Helper Functions ---

# Function to display help message
show_help() {
  grep '^#' "$0" | cut -c 2-
}

# Function to convert kebab-case to PascalCase
kebab_to_pascal() {
  echo "$1" | sed -r 's/(^|-)([a-z])/​\U\2/g'
}

# --- Main Script Logic ---

COMPOSABLE_NAME=""
COMPOSABLE_PATH=""
WITH_TEST=false

# Parse arguments
while [[ "$#" -gt 0 ]]; do
  case "$1" in
    -p|--path)
      COMPOSABLE_PATH="$2"
      shift
      ;;
    -t|--with-test)
      WITH_TEST=true
      ;;
    -h|--help)
      show_help
      exit 0
      ;;
    -*)
      echo "Error: Unknown option '$1'" >&2
      show_help
      exit 1
      ;;
    *)
      if [[ -z "$COMPOSABLE_NAME" ]]; then
        COMPOSABLE_NAME="$1"
      else
        echo "Error: Too many arguments. Composable name already set to '$COMPOSABLE_NAME'." >&2
        show_help
        exit 1
      fi
      ;;
  esac
  shift
done

# Validate composable name
if [[ -z "$COMPOSABLE_NAME" ]]; then
  echo "Error: Composable name is required." >&2
  show_help
  exit 1
fi

# Ensure composable name starts with 'use'
if [[ ! "$COMPOSABLE_NAME" =~ ^use[A-Z] ]]; then
  echo "Warning: It is a convention for composable names to start with 'use'. Consider renaming '$COMPOSABLE_NAME' to 'use$(kebab_to_pascal "$COMPOSABLE_NAME")'."
fi

# Determine final paths
if [[ -z "$COMPOSABLE_PATH" ]]; then
  COMPOSABLE_DIR="${DEFAULT_COMPOSABLE_PATH}"
else
  COMPOSABLE_DIR="${COMPOSABLE_PATH}"
fi

# Convert composable name to PascalCase for file and function naming
PASCAL_COMPOSABLE_NAME=$(kebab_to_pascal "$COMPOSABLE_NAME")

COMPOSABLE_FILE="${COMPOSABLE_DIR}/${COMPOSABLE_NAME}.ts"
TEST_FILE="${COMPOSABLE_DIR}/${COMPOSABLE_NAME}.test.ts"

# Create directory if it doesn't exist
mkdir -p "$(dirname "$COMPOSABLE_FILE")" || { echo "Error: Could not create directory $(dirname "$COMPOSABLE_FILE")" >&2; exit 1; }

# Generate .ts file content
COMPOSABLE_CONTENT=''
import { ref, computed } from 'vue';

export function ${COMPOSABLE_NAME}() {
  const count = ref(0);
  const doubleCount = computed(() => count.value * 2);

  function increment() {
    count.value++;
  }

  return {
    count,
    doubleCount,
    increment,
  };
}
''

# Write .ts file
echo "Creating ${COMPOSABLE_FILE}..."
echo "$COMPOSABLE_CONTENT" > "$COMPOSABLE_FILE" || { echo "Error: Could not write to ${COMPOSABLE_FILE}" >&2; exit 1; }
echo "Successfully created ${COMPOSABLE_FILE}"

# Generate .test.ts file if requested
if "$WITH_TEST"; then
  # Create directory for test file if different from composable directory
  mkdir -p "$(dirname "$TEST_FILE")" || { echo "Error: Could not create directory $(dirname "$TEST_FILE")" >&2; exit 1; }

  TEST_CONTENT=''
import { describe, it, expect } from 'vitest';
import { ref } from 'vue';
import { ${COMPOSABLE_NAME} } from './${COMPOSABLE_NAME}';

describe('${COMPOSABLE_NAME}', () => {
  it('should return a count of 0 initially', () => {
    const { count } = ${COMPOSABLE_NAME}();
    expect(count.value).toBe(0);
  });

  it('should increment the count', () => {
    const { count, increment } = ${COMPOSABLE_NAME}();
    increment();
    expect(count.value).toBe(1);
  });

  it('should return double the count', () => {
    const { count, doubleCount, increment } = ${COMPOSABLE_NAME}();
    increment();
    increment();
    expect(count.value).toBe(2);
    expect(doubleCount.value).toBe(4);
  });
});
''

  echo "Creating ${TEST_FILE}..."
echo "$TEST_CONTENT" > "$TEST_FILE" || { echo "Error: Could not write to ${TEST_FILE}" >&2; exit 1; }
echo "Successfully created ${TEST_FILE}"
fi

echo "Composable generation complete."
