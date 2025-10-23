#!/bin/bash

# generate-svelte-store.sh
# Description: Scaffolds a new Svelte writable store (.ts file) with TypeScript types,
#              including `writable` import and basic `set`, `update` functions.

# Usage: ./generate-svelte-store.sh <StoreName>
# Example: ./generate-svelte-store.sh Auth
# This will create src/lib/stores/authStore.ts

# --- Configuration ---
DEFAULT_STORES_DIR="src/lib/stores"

# --- Functions ---

# Function to display help message
display_help() {
  echo "Usage: $0 <StoreName>"
  echo ""
  echo "Scaffolds a new Svelte writable store file."
  echo "The store name should be in PascalCase (e.g., 'Auth')."
  echo "The script will create a file named '<storeName>Store.ts' in '$DEFAULT_STORES_DIR'."
  echo ""
  echo "Example: $0 User"
  echo "  Creates: $DEFAULT_STORES_DIR/userStore.ts"
  exit 0
}

# Function to create the store file
create_store() {
  local name=$1
  local filename="${name}Store.ts"
  local filepath="${DEFAULT_STORES_DIR}/${filename}"

  # Ensure stores directory exists
  mkdir -p "${DEFAULT_STORES_DIR}"

  if [ -f "${filepath}" ]; then
    echo "Error: Svelte store file '${filepath}' already exists." >&2
    exit 1
  fi

  cat <<EOF > "${filepath}"
import { writable } from 'svelte/store';

// Define the interface for your store's state
interface ${name}State {
  // Example properties
  value: string;
  count: number;
  // isAuthenticated: boolean;
  // user: { id: string; name: string } | null;
}

const initialState: ${name}State = {
  value: 'initial value',
  count: 0,
  // isAuthenticated: false,
  // user: null,
};

export const ${name.toLowerCase()}Store = writable<${name}State>(initialState);

// Example custom functions to interact with the store
export const update${name}Value = (newValue: string) => {
  ${name.toLowerCase()}Store.update(state => ({ ...state, value: newValue }));
};

export const increment${name}Count = () => {
  ${name.toLowerCase()}Store.update(state => ({ ...state, count: state.count + 1 }));
};

// You can also export a custom store with more methods
/*
function create${name}Store() {
  const { subscribe, set, update } = writable<${name}State>(initialState);

  return {
    subscribe,
    set,
    update,
    reset: () => set(initialState),
    // add custom methods here
    toggleAuth: () => update(state => ({ ...state, isAuthenticated: !state.isAuthenticated }))
  };
}
export const ${name.toLowerCase()}CustomStore = create${name}Store();
*/
EOF

  echo "Successfully created Svelte store: ${filepath}"
  echo "Remember to update the interface, initial state, and functions according to your needs."
}

# --- Main Logic ---

# Check for help flag
if [[ "$1" == "-h" || "$1" == "--help" ]]; then
  display_help
fi

# Check if a store name is provided
if [ -z "$1" ]; then
  echo "Error: Store name not provided." >&2
  display_help
fi

# Validate store name (PascalCase, no spaces/special chars)
if ! [[ "$1" =~ ^[A-Z][a-zA-Z0-9]*$ ]]; then
  echo "Error: Invalid store name. Please use PascalCase (e.g., 'Auth')." >&2
  exit 1
fi

# Call function to create the store
create_store "$1"
