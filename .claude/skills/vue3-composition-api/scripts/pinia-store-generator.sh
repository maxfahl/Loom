#!/bin/bash

# pinia-store-generator.sh
# Description: Scaffolds a new Pinia store module with a predefined structure (state, getters, actions).
#              Ensures adherence to best practices for Pinia store organization.

# Usage: ./pinia-store-generator.sh <StoreName>
# Example: ./pinia-store-generator.sh User
# This will create src/stores/user.ts

# --- Configuration ---
STORES_DIR="src/stores"

# --- Functions ---

# Function to display help message
display_help() {
  echo "Usage: $0 <StoreName>"
  echo ""
  echo "Scaffolds a new Pinia store module."
  echo "The store name should be in PascalCase (e.g., 'User')."
  echo "The script will create a file named '<storeName>.ts' (lowercase) in '$STORES_DIR'."
  echo ""
  echo "Example: $0 Auth"
  echo "  Creates: $STORES_DIR/auth.ts"
  exit 0
}

# Function to create the store file
create_store() {
  local name=$1
  local lowercase_name=$(echo "$name" | tr '[:upper:]' '[:lower:]')
  local filename="${lowercase_name}.ts"
  local filepath="${STORES_DIR}/${filename}"

  # Ensure stores directory exists
  mkdir -p "${STORES_DIR}"

  if [ -f "${filepath}" ]; then
    echo "Error: Pinia store file '${filepath}' already exists." >&2
    exit 1
  fi

  cat <<EOF > "${filepath}"
import { defineStore } from 'pinia';

interface ${name}State {
  // Define your state properties here
  count: number;
  // user: { id: number; name: string } | null;
}

export const use${name}Store = defineStore('${lowercase_name}', {
  state: (): ${name}State => ({
    count: 0,
    // user: null,
  }),

  getters: {
    // Define your getters here
    doubleCount(state): number {
      return state.count * 2;
    },
    // isAuthenticated: (state) => !!state.user,
  },

  actions: {
    // Define your actions here
    increment() {
      this.count++;
    },
    // async login(credentials: { username: string; password: string }) {
    //   // Simulate API call
    //   this.user = { id: 1, name: credentials.username };
    // },
    // logout() {
    //   this.user = null;
    // },
  },
});
EOF

  echo "Successfully created Pinia store: ${filepath}"
  echo "Remember to update the state, getters, and actions according to your needs."
}

# --- Main Logic ---

# Check for help flag
if [[ "$1" == "-h" || "$1" == "--help" ]]; then
  display_help
fi

# Check if a store name is provided
if [ -z "$1" ]; then
  echo "Error: Pinia store name not provided." >&2
  display_help
fi

# Validate store name (PascalCase, no spaces/special chars)
if ! [[ "$1" =~ ^[A-Z][a-zA-Z0-9]*$ ]]; then
  echo "Error: Invalid store name. Please use PascalCase (e.g., 'User')." >&2
  exit 1
fi

# Call function to create the store
create_store "$1"
