#!/bin/bash

# generate-pinia-store.sh
#
# Purpose:
#   Automates the creation of a new Pinia store with a basic structure
#   including state, getters, and actions, along with an optional test file.
#   This script streamlines the setup of new state management modules.
#
# Usage:
#   ./generate-pinia-store.sh <StoreName> [options]
#
# Options:
#   -p, --path <path>     Specify the directory to create the store in.
#                         Defaults to 'src/stores'.
#   -t, --with-test       Generate an accompanying Vitest test file.
#   -h, --help            Display this help message.
#
# Examples:
#   ./generate-pinia-store.sh Auth
#   ./generate-pinia-store.sh Products -p src/features/shop
#   ./generate-pinia-store.sh UserSettings --with-test
#
# Requirements:
#   - Bash shell
#   - Pinia installed in the project.
#
# Output:
#   - Creates <StoreName>.ts and optionally <StoreName>.test.ts files.
#   - Prints messages indicating success or failure.

# --- Configuration ---
DEFAULT_STORE_PATH="src/stores"
DEFAULT_TEST_PATH="src/stores" # Can be adjusted if tests are in a separate top-level directory

# --- Helper Functions ---

# Function to display help message
show_help() {
  grep '^#' "$0" | cut -c 2-
}

# Function to convert kebab-case to PascalCase
kebab_to_pascal() {
  echo "$1" | sed -r 's/(^|-)([a-z])/​\U\2/g'
}

# Function to convert PascalCase to camelCase
pascal_to_camel() {
  echo "$1" | sed -r 's/^(.)/​\L\1/'
}

# --- Main Script Logic ---

STORE_NAME=""
STORE_PATH=""
WITH_TEST=false

# Parse arguments
while [[ "$#" -gt 0 ]]; do
  case "$1" in
    -p|--path)
      STORE_PATH="$2"
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
      if [[ -z "$STORE_NAME" ]]; then
        STORE_NAME="$1"
      else
        echo "Error: Too many arguments. Store name already set to '$STORE_NAME'." >&2
        show_help
        exit 1
      fi
      ;; 
  esac
  shift
done

# Validate store name
if [[ -z "$STORE_NAME" ]]; then
  echo "Error: Store name is required." >&2
  show_help
  exit 1
fi

# Determine final paths
if [[ -z "$STORE_PATH" ]]; then
  STORE_DIR="${DEFAULT_STORE_PATH}"
else
  STORE_DIR="${STORE_PATH}"
fi

# Convert store name to PascalCase and camelCase
PASCAL_STORE_NAME=$(kebab_to_pascal "$STORE_NAME")
CAMEL_STORE_NAME=$(pascal_to_camel "$PASCAL_STORE_NAME")

STORE_FILE="${STORE_DIR}/${CAMEL_STORE_NAME}.ts"
TEST_FILE="${STORE_DIR}/${CAMEL_STORE_NAME}.test.ts"

# Create directory if it doesn't exist
mkdir -p "$(dirname "$STORE_FILE")" || { echo "Error: Could not create directory $(dirname "$STORE_FILE")" >&2; exit 1; }

# Generate .ts file content
STORE_CONTENT='import { defineStore } from "pinia";

interface ${PASCAL_STORE_NAME}State {
  // Define your state properties here
  count: number;
}

export const use${PASCAL_STORE_NAME}Store = defineStore("${CAMEL_STORE_NAME}", {
  state: (): ${PASCAL_STORE_NAME}State => ({
    count: 0,
  }),
  getters: {
    doubleCount: (state) => state.count * 2,
  },
  actions: {
    increment() {
      this.count++;
    },
    async fetchSomething() {
      // Simulate an async operation
      return new Promise((resolve) => {
        setTimeout(() => {
          console.log("Fetched something!");
          resolve(true);
        }, 1000);
      });
    },
  },
});'

# Write .ts file
echo "Creating ${STORE_FILE}..."
echo "$STORE_CONTENT" > "$STORE_FILE" || { echo "Error: Could not write to ${STORE_FILE}" >&2; exit 1; }
echo "Successfully created ${STORE_FILE}"

# Generate .test.ts file if requested
if "$WITH_TEST"; then
  # Create directory for test file if different from store directory
  mkdir -p "$(dirname "$TEST_FILE")" || { echo "Error: Could not create directory $(dirname "$TEST_FILE")" >&2; exit 1; }

  TEST_CONTENT='import { setActivePinia, createPinia } from "pinia";
import { describe, it, expect, beforeEach } from "vitest";
import { use${PASCAL_STORE_NAME}Store } from "./${CAMEL_STORE_NAME}";

describe("use${PASCAL_STORE_NAME}Store", () => {
  beforeEach(() => {
    setActivePinia(createPinia());
  });

  it("initializes with a count of 0", () => {
    const store = use${PASCAL_STORE_NAME}Store();
    expect(store.count).toBe(0);
  });

  it("increments the count", () => {
    const store = use${PASCAL_STORE_NAME}Store();
    store.increment();
    expect(store.count).toBe(1);
  });

  it("doubles the count via getter", () => {
    const store = use${PASCAL_STORE_NAME}Store();
    store.count = 5;
    expect(store.doubleCount).toBe(10);
  });

  it("fetches something asynchronously", async () => {
    const store = use${PASCAL_STORE_NAME}Store();
    const result = await store.fetchSomething();
    expect(result).toBe(true);
  });
});'

  echo "Creating ${TEST_FILE}..."
  echo "$TEST_CONTENT" > "$TEST_FILE" || { echo "Error: Could not write to ${TEST_FILE}" >&2; exit 1; }
  echo "Successfully created ${TEST_FILE}"
fi

echo "Pinia store generation complete."
