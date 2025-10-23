#!/bin/bash

# init-sveltekit.sh
#
# Purpose:
#   Initializes a new SvelteKit project with common development tools pre-configured.
#   This script automates the setup of TypeScript, ESLint, Prettier, Tailwind CSS,
#   and Vitest, saving significant time and ensuring consistent project setups.
#
# Usage:
#   ./init-sveltekit.sh <project_name> [--tailwind] [--vitest] [--eslint] [--prettier]
#
# Arguments:
#   <project_name>  : The name of the new SvelteKit project.
#   --tailwind      : (Optional) Install and configure Tailwind CSS.
#   --vitest        : (Optional) Install and configure Vitest for unit testing.
#   --eslint        : (Optional) Install and configure ESLint for code linting.
#   --prettier      : (Optional) Install and configure Prettier for code formatting.
#
# Examples:
#   ./init-sveltekit.sh my-svelte-app
#   ./init-sveltekit.sh my-blog --tailwind --vitest
#   ./init-sveltekit.sh portfolio --tailwind --eslint --prettier --vitest
#
# Features:
#   - Creates a new SvelteKit project using 'npm create svelte@latest'.
#   - Installs TypeScript, ESLint, Prettier, Tailwind CSS, and Vitest based on flags.
#   - Configures each tool with sensible defaults for SvelteKit.
#   - Includes basic error handling.
#   - Provides clear command-line arguments and help text.
#
# Dependencies:
#   - Node.js and npm (or yarn/pnpm) must be installed.
#   - Git (for initial commit, if desired, though not handled by this script).

# --- Configuration ---
PROJECT_NAME=""
INSTALL_TAILWIND=false
INSTALL_VITEST=false
INSTALL_ESLINT=false
INSTALL_PRETTIER=false

# --- Functions ---

# Display help message
show_help() {
  echo "Usage: $0 <project_name> [--tailwind] [--vitest] [--eslint] [--prettier]"
  echo ""
  echo "Arguments:"
  echo "  <project_name>  : The name of the new SvelteKit project."
  echo "  --tailwind      : (Optional) Install and configure Tailwind CSS."
  echo "  --vitest        : (Optional) Install and configure Vitest for unit testing."
  echo "  --eslint        : (Optional) Install and configure ESLint for code linting."
  echo "  --prettier      : (Optional) (Optional) Install and configure Prettier for code formatting."
  echo ""
  echo "Examples:"
  echo "  $0 my-svelte-app"
  echo "  $0 my-blog --tailwind --vitest"
  echo "  $0 portfolio --tailwind --eslint --prettier --vitest"
  exit 0
}

# Parse command-line arguments
parse_args() {
  if [ "$#" -eq 0 ]; then
    show_help
  fi

  PROJECT_NAME="$1"
  shift

  while [ "$#" -gt 0 ]; do
    case "$1" in
      --tailwind)
        INSTALL_TAILWIND=true
        ;;
      --vitest)
        INSTALL_VITEST=true
        ;;
      --eslint)
        INSTALL_ESLINT=true
        ;;
      --prettier)
        INSTALL_PRETTIER=true
        ;;
      *)
        echo "Error: Unknown argument '$1'"
        show_help
        ;;
    esac
    shift
  done

  if [ -z "$PROJECT_NAME" ]; then
    echo "Error: Project name is required."
    show_help
  fi
}

# Check if a command exists
command_exists() {
  command -v "$1" >/dev/null 2>&1
}

# Main script logic
main() {
  parse_args "$@"

  echo "--- Initializing SvelteKit Project: $PROJECT_NAME ---"

  # 1. Create SvelteKit project
  if ! command_exists "npm"; then
    echo "Error: npm is not installed. Please install Node.js."
    exit 1
  fi

  echo "Creating SvelteKit project with TypeScript..."
  npm create svelte@latest "$PROJECT_NAME" -- --template skeleton --typescript || { echo "Failed to create SvelteKit project."; exit 1; }
  cd "$PROJECT_NAME" || { echo "Failed to change directory to $PROJECT_NAME."; exit 1; }

  echo "Installing dependencies..."
  npm install || { echo "Failed to install project dependencies."; exit 1; }

  # 2. Configure ESLint (if requested)
  if [ "$INSTALL_ESLINT" = true ]; then
    echo "Configuring ESLint..."
    npx svelte-add eslint || { echo "Failed to add ESLint."; exit 1; }
    npm install || { echo "Failed to install ESLint dependencies."; exit 1; }
    echo "ESLint configured."
  fi

  # 3. Configure Prettier (if requested)
  if [ "$INSTALL_PRETTIER" = true ]; then
    echo "Configuring Prettier..."
    npx svelte-add prettier || { echo "Failed to add Prettier."; exit 1; }
    npm install || { echo "Failed to install Prettier dependencies."; exit 1; }
    echo "Prettier configured."
  fi

  # 4. Configure Tailwind CSS (if requested)
  if [ "$INSTALL_TAILWIND" = true ]; then
    echo "Configuring Tailwind CSS..."
    npx svelte-add tailwindcss || { echo "Failed to add Tailwind CSS."; exit 1; }
    npm install || { echo "Failed to install Tailwind CSS dependencies."; exit 1; }
    echo "Tailwind CSS configured."
  fi

  # 5. Configure Vitest (if requested)
  if [ "$INSTALL_VITEST" = true ]; then
    echo "Configuring Vitest..."
    npm install -D vitest @testing-library/svelte @vitest/ui jsdom || { echo "Failed to install Vitest dependencies."; exit 1; }

    # Add Vitest script to package.json
    jq '.scripts.test = "vitest"
.scripts["test:ui"] = "vitest --ui"' package.json > tmp.json && mv tmp.json package.json || { echo "Failed to update package.json for Vitest."; exit 1; }

    # Create vitest.config.ts
    cat << EOF > vitest.config.ts
import { defineConfig } from 'vitest/config';
import { sveltekit } from '@sveltejs/kit/vite';

export default defineConfig({
  plugins: [sveltekit()],
  test: {
    include: ['src/**/*.{test,spec}.{js,ts}'],
    globals: true,
    environment: 'jsdom',
    setupFiles: ['./setupTests.ts'], // Optional: for global test setup
  },
});
EOF

    # Create setupTests.ts (optional but good practice)
    cat << EOF > setupTests.ts
import '@testing-library/svelte/vitest';
import '@testing-library/jest-dom'; // For extended matchers
EOF

    echo "Vitest configured. Remember to add '/// <reference types="vitest/globals" />' to your tsconfig.json if not already present."
  fi

  echo "--- Project '$PROJECT_NAME' setup complete! ---"
  echo "To start development server: cd $PROJECT_NAME && npm run dev"
  echo "To build for production: cd $PROJECT_NAME && npm run build"
  if [ "$INSTALL_VITEST" = true ]; then
    echo "To run tests: cd $PROJECT_NAME && npm run test"
  fi
}

# Execute main function
main "$@"
