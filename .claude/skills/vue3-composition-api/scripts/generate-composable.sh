#!/bin/bash

# generate-composable.sh
# Description: Scaffolds a new Vue 3 Composition API composable file with essential imports and a basic structure.
#              Promotes consistent naming (use* convention) and reduces boilerplate.

# Usage: ./generate-composable.sh <ComposableName>
# Example: ./generate-composable.sh Counter
# This will create src/composables/useCounter.ts

# --- Configuration ---
COMPOSABLES_DIR="src/composables"

# --- Functions ---

# Function to display help message
display_help() {
  echo "Usage: $0 <ComposableName>"
  echo ""
  echo "Scaffolds a new Vue 3 Composition API composable file."
  echo "The composable name should be in PascalCase (e.g., 'Counter')."
  echo "The script will create a file named 'use<ComposableName>.ts' in '$COMPOSABLES_DIR'."
  echo ""
  echo "Example: $0 MyFeature"
  echo "  Creates: $COMPOSABLES_DIR/useMyFeature.ts"
  exit 0
}

# Function to create the composable file
create_composable() {
  local name=$1
  local filename="use${name}.ts"
  local filepath="${COMPOSABLES_DIR}/${filename}"

  # Ensure composables directory exists
  mkdir -p "${COMPOSABLES_DIR}"

  if [ -f "${filepath}" ]; then
    echo "Error: Composable file '${filepath}' already exists." >&2
    exit 1
  fi

  cat <<EOF > "${filepath}"
import { ref, computed, watch, onMounted, onUnmounted } from 'vue';
import type { Ref } from 'vue';

/**
 * @module use${name}
 * @description A Vue 3 Composition API composable for managing ${name.toLowerCase()} related logic.
 *
 * @param {any} initialValue - Optional initial value for the composable's state.
 * @returns {{ /* Define the reactive properties and functions exposed by this composable */ }}
 */
export function use${name}(initialValue?: any) {
  // --- State ---
  const state = ref(initialValue) as Ref<any>; // Example reactive state

  // --- Computed Properties ---
  const doubledState = computed(() => {
    if (typeof state.value === 'number') {
      return state.value * 2;
    }
    return undefined;
  });

  // --- Methods ---
  const updateState = (newValue: any) => {
    state.value = newValue;
  };

  // --- Watchers ---
  watch(state, (newValue, oldValue) => {
    console.log(`State changed from ${oldValue} to ${newValue}`);
  });

  // --- Lifecycle Hooks ---
  onMounted(() => {
    console.log(`Composable use${name} mounted.`);
  });

  onUnmounted(() => {
    console.log(`Composable use${name} unmounted.`);
  });

  // --- Exposed API ---
  return {
    state,
    doubledState,
    updateState,
  };
}
EOF

  echo "Successfully created composable: ${filepath}"
  echo "Remember to update the types and logic according to your needs."
}

# --- Main Logic ---

# Check for help flag
if [[ "$1" == "-h" || "$1" == "--help" ]]; then
  display_help
fi

# Check if a composable name is provided
if [ -z "$1" ]; then
  echo "Error: Composable name not provided." >&2
  display_help
fi

# Validate composable name (PascalCase, no spaces/special chars)
if ! [[ "$1" =~ ^[A-Z][a-zA-Z0-9]*$ ]]; then
  echo "Error: Invalid composable name. Please use PascalCase (e.g., 'Counter')." >&2
  exit 1
fi

# Call function to create the composable
create_composable "$1"
