#!/bin/bash

# generate-vue-component.sh
#
# Purpose:
#   Automates the creation of a new Vue 3 component with Composition API,
#   <script setup>, TypeScript, and an optional test file.
#   This script saves significant time by generating boilerplate code,
#   ensuring consistency and adherence to best practices.
#
# Usage:
#   ./generate-vue-component.sh <ComponentName> [options]
#
# Options:
#   -p, --path <path>     Specify the directory to create the component in.
#                         Defaults to 'src/components'.
#   -t, --with-test       Generate an accompanying Vitest test file.
#   -h, --help            Display this help message.
#
# Examples:
#   ./generate-vue-component.sh MyButton
#   ./generate-vue-component.sh UserProfile -p src/views/user
#   ./generate-vue-component.sh ProductCard --with-test
#   ./generate-vue-component.sh BaseInput -p src/components/base --with-test
#
# Requirements:
#   - Bash shell
#   - Basic understanding of Vue 3, Composition API, and TypeScript.
#
# Output:
#   - Creates <ComponentName>.vue and optionally <ComponentName>.test.ts files.
#   - Prints messages indicating success or failure.

# --- Configuration ---
DEFAULT_COMPONENT_PATH="src/components"
DEFAULT_TEST_PATH="src/components" # Can be adjusted if tests are in a separate top-level directory

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

COMPONENT_NAME=""
COMPONENT_PATH=""
WITH_TEST=false

# Parse arguments
while [[ "$#" -gt 0 ]]; do
  case "$1" in
    -p|--path)
      COMPONENT_PATH="$2"
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
      if [[ -z "$COMPONENT_NAME" ]]; then
        COMPONENT_NAME="$1"
      else
        echo "Error: Too many arguments. Component name already set to '$COMPONENT_NAME'." >&2
        show_help
        exit 1
      fi
      ;;
  esac
  shift
done

# Validate component name
if [[ -z "$COMPONENT_NAME" ]]; then
  echo "Error: Component name is required." >&2
  show_help
  exit 1
fi

# Determine final paths
if [[ -z "$COMPONENT_PATH" ]]; then
  COMPONENT_DIR="${DEFAULT_COMPONENT_PATH}"
else
  COMPONENT_DIR="${COMPONENT_PATH}"
fi

# Convert component name to PascalCase for file and component naming
PASCAL_COMPONENT_NAME=$(kebab_to_pascal "$COMPONENT_NAME")
VUE_FILE="${COMPONENT_DIR}/${PASCAL_COMPONENT_NAME}.vue"
TEST_FILE="${COMPONENT_DIR}/${PASCAL_COMPONENT_NAME}.test.ts"

# Create directory if it doesn't exist
mkdir -p "$(dirname "$VUE_FILE")" || { echo "Error: Could not create directory $(dirname "$VUE_FILE")" >&2; exit 1; }

# Generate .vue file content
VUE_CONTENT='<script setup lang="ts">
import { defineProps } from "vue";

interface Props {
  msg?: string;
}

const props = defineProps<Props>();
</script>

<template>
  <div class="${COMPONENT_NAME}">
    <h1>{{ msg || "${PASCAL_COMPONENT_NAME} Component" }}</h1>
    <p>This is the ${PASCAL_COMPONENT_NAME} component.</p>
  </div>
</template>

<style scoped>
.${COMPONENT_NAME} {
  /* Add component-specific styles here */
}
</style>'

# Write .vue file
echo "Creating ${VUE_FILE}..."
echo "$VUE_CONTENT" > "$VUE_FILE" || { echo "Error: Could not write to ${VUE_FILE}" >&2; exit 1; }
echo "Successfully created ${VUE_FILE}"

# Generate .test.ts file if requested
if "$WITH_TEST"; then
  # Create directory for test file if different from component directory
  mkdir -p "$(dirname "$TEST_FILE")" || { echo "Error: Could not create directory $(dirname "$TEST_FILE")" >&2; exit 1; }

  TEST_CONTENT='import { mount } from "@vue/test-utils";
import { describe, it, expect } from "vitest";
import ${PASCAL_COMPONENT_NAME} from "./${PASCAL_COMPONENT_NAME}.vue";

describe("${PASCAL_COMPONENT_NAME}", () => {
  it('renders properly', () => {
    const wrapper = mount(${PASCAL_COMPONENT_NAME}, { props: { msg: 'Hello Vitest' } });
    expect(wrapper.text()).toContain('Hello Vitest');
  });

  it('renders default message when no prop is passed', () => {
    const wrapper = mount(${PASCAL_COMPONENT_NAME});
    expect(wrapper.text()).toContain("${PASCAL_COMPONENT_NAME} Component");
  });
});'

  echo "Creating ${TEST_FILE}..."
echo "$TEST_CONTENT" > "$TEST_FILE" || { echo "Error: Could not write to ${TEST_FILE}" >&2; exit 1; }
echo "Successfully created ${TEST_FILE}"
fi

echo "Component generation complete."
