#!/bin/bash
#
# format-staged.sh: Formats staged files using Prettier.
#
# This script is designed to be used with a pre-commit hook (e.g., with husky).
# It ensures that only the files being committed are formatted.
#
# This is more efficient than running Prettier on the whole project.
# It uses `lint-staged` which is the recommended way to do this.

set -e

# --- Color Codes ---
COLOR_GREEN="\033[0;32m"
COLOR_YELLOW="\033[0;33m"
COLOR_RED="\033[0;31m"
COLOR_RESET="\033[0m"

# --- Helper Functions ---
function print_success() {
  echo -e "${COLOR_GREEN}✅ $1${COLOR_RESET}"
}

function print_warning() {
  echo -e "${COLOR_YELLOW}⚠️ $1${COLOR_RESET}"
}

function print_error() {
  echo -e "${COLOR_RED}❌ $1${COLOR_RESET}"
  exit 1
}

# --- Main Logic ---

print_warning "Checking for lint-staged..."
if ! command -v lint-staged &> /dev/null
then
    print_warning "lint-staged could not be found. It is the recommended tool for this job."
    print_warning "Please install it with: npm install --save-dev lint-staged husky"
    print_warning "And configure it in your package.json:"
    echo "{
  \"lint-staged\": {
    \"**/*.{js,jsx,ts,tsx,json,css,scss,md}\": \"prettier --write\"
  }
}"
    print_error "Aborting."
fi

print_success "Found lint-staged. Running it now..."

# lint-staged will automatically find the staged files, run prettier on them,
# and re-stage the changes.
lint-staged

print_success "All staged files have been formatted."
