#!/bin/bash
#
# check-format.sh: Checks for unformatted files using Prettier.
#
# This script is designed for CI/CD pipelines. It will:
# 1. Run `prettier --check` on the entire project.
# 2. Provide clear output on success or failure.
# 3. Exit with a non-zero status code if unformatted files are found.

set -e

# --- Color Codes ---
COLOR_GREEN="\033[0;32m"
COLOR_RED="\033[0;31m"
COLOR_RESET="\033[0m"

# --- Helper Functions ---
function print_success() {
  echo -e "${COLOR_GREEN}✅ $1${COLOR_RESET}"
}

function print_error() {
  echo -e "${COLOR_RED}❌ $1${COLOR_RESET}"
}

# --- Main Logic ---

echo "Checking for unformatted files with Prettier..."

# The `--check` flag makes Prettier output a human-friendly summary
# and exit with a non-zero status code if any files are not formatted.
if npx prettier --check .; then
  print_success "All files are correctly formatted."
  exit 0
else
  print_error "Unformatted files found. Please run 'npm run format' to fix them."
  exit 1
fi
