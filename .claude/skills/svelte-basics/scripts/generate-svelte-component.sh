#!/bin/bash

# generate-svelte-component.sh
# Description: Scaffolds a new Svelte component (.svelte file) with essential <script lang="ts">
#              <template>, and <style> blocks, promoting consistent component structure.

# Usage: ./generate-svelte-component.sh <ComponentName> [directory]
# Example: ./generate-svelte-component.sh Button components
# This will create src/components/Button.svelte

# --- Configuration ---
DEFAULT_COMPONENTS_DIR="src/lib/components"

# --- Functions ---

# Function to display help message
display_help() {
  echo "Usage: $0 <ComponentName> [directory]"
  echo ""
  echo "Scaffolds a new Svelte component file."
  echo "The component name should be in PascalCase (e.g., 'Button')."
  echo "An optional directory can be provided (e.g., 'components', 'layout')."
  echo "If no directory is provided, it defaults to '$DEFAULT_COMPONENTS_DIR'."
  echo ""
  echo "Example: $0 MyHeader layout"
  echo "  Creates: src/lib/layout/MyHeader.svelte"
  echo "Example: $0 PrimaryButton"
  echo "  Creates: src/lib/components/PrimaryButton.svelte"
  exit 0
}

# Function to create the component file
create_component() {
  local name=$1
  local target_dir=$2
  local filepath="${target_dir}/${name}.svelte"

  # Ensure target directory exists
  mkdir -p "${target_dir}"

  if [ -f "${filepath}" ]; then
    echo "Error: Svelte component file '${filepath}' already exists." >&2
    exit 1
  fi

  cat <<EOF > "${filepath}"
<script lang="ts">
  // Define props here
  // export let propName: string = 'defaultValue';

  // Reactive declarations
  // $: doubledCount = count * 2;

  // Lifecycle hooks
  // import { onMount } from 'svelte';
  // onMount(() => {
  //   console.log('Component mounted');
  // });

  // Event dispatcher
  // import { createEventDispatcher } from 'svelte';
  // const dispatch = createEventDispatcher();
  // function handleClick() {
  //   dispatch('click', { value: 'someValue' });
  // }
</script>

<template>
  <div class="${name}">
    <h1>Hello from ${name} Component!</h1>
    <!-- Your component content here -->
  </div>
</template>

<style lang="scss">
  .${name} {
    /* Component-specific styles */
    padding: 1rem;
    border: 1px solid #eee;
    border-radius: 4px;
    background-color: #f9f9f9;
  }
</style>
EOF

  echo "Successfully created Svelte component: ${filepath}"
  echo "Remember to update the props, logic, and styles according to your needs."
}

# --- Main Logic ---

# Check for help flag
if [[ "$1" == "-h" || "$1" == "--help" ]]; then
  display_help
fi

# Check if a component name is provided
if [ -z "$1" ]; then
  echo "Error: Component name not provided." >&2
  display_help
fi

# Validate component name (PascalCase, no spaces/special chars)
if ! [[ "$1" =~ ^[A-Z][a-zA-Z0-9]*$ ]]; then
  echo "Error: Invalid component name. Please use PascalCase (e.g., 'Button')." >&2
  exit 1
fi

COMPONENT_NAME=$1
TARGET_DIRECTORY="$DEFAULT_COMPONENTS_DIR"

if [ -n "$2" ]; then
  # If a directory is provided, append it to src/lib/ (SvelteKit convention)
  TARGET_DIRECTORY="src/lib/$2"
fi

# Call function to create the component
create_component "$COMPONENT_NAME" "$TARGET_DIRECTORY"
