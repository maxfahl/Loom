#!/bin/bash

# run-affected-tests.sh
# Identifies and runs tests only for packages affected by recent changes in a pnpm monorepo.
# This script leverages pnpm's --filter-prod and --filter-dev flags to determine affected packages.

# Usage:
#   ./run-affected-tests.sh [git_ref_or_commit]
#   ./run-affected-tests.sh main
#   ./run-affected-tests.sh HEAD~1

# Arguments:
#   [git_ref_or_commit]: Optional. The Git reference (branch name, commit hash) to compare against.
#                        If not provided, it defaults to the merge-base of the current branch and the default branch (e.g., main/master).

# Requirements:
#   - pnpm: Must be installed and configured for the monorepo.
#   - git: Must be installed and the current directory must be a git repository.

set -euo pipefail

# --- Configuration ---
ROOT_DIR=$(git rev-parse --show-toplevel || pwd)
DEFAULT_BRANCH="main" # Or 'master', depending on your repository

# --- Helper Functions ---
print_help() {
  echo "Usage: $0 [git_ref_or_commit]"
  echo ""
  echo "Identifies and runs tests only for packages affected by recent changes in a pnpm monorepo."
  echo "Leverages pnpm's --filter-prod and --filter-dev flags."
  echo ""
  echo "Arguments:"
  echo "  [git_ref_or_commit]  Optional. The Git reference (branch name, commit hash) to compare against."
  echo "                       If not provided, it defaults to the merge-base of the current branch and the default branch (e.g., main/master)."
  echo "  -h, --help           Display this help message."
  echo ""
  echo "Example:"
  echo "  $0 main                 # Compare against the 'main' branch"
  echo "  $0 HEAD~1               # Compare against the previous commit"
  echo "  $0                      # Compare against the merge-base of current and default branch"
  exit 0
}

# Function to check for required commands
check_dependencies() {
  if ! command -v pnpm &> /dev/null;
  then
    echo "Error: 'pnpm' is not installed. Please install it to run this script."
    echo "  Refer to: https://pnpm.io/installation"
    exit 1
  fi
  if ! command -v git &> /dev/null;
  then
    echo "Error: 'git' is not installed. Please install it to run this script."
    exit 1
  fi
  if ! git rev-parse --is-inside-work-tree &> /dev/null;
  then
    echo "Error: Not inside a git repository."
    exit 1
  fi
}

# --- Main Logic ---

# Parse arguments
if [[ "$#" -gt 0 && "$1" == "-h" || "$1" == "--help" ]]; then
  print_help
fi

check_dependencies

COMPARE_REF=""
if [[ -n "$1" ]]; then
  COMPARE_REF="$1"
else
  # Determine the default branch dynamically if possible, or use hardcoded
  if git remote show origin &> /dev/null;
  then
    DEFAULT_BRANCH=$(git remote show origin | grep 'HEAD branch' | awk '{print $NF}' || echo "main")
  fi
  echo "No compare reference provided. Using merge-base with default branch '$DEFAULT_BRANCH'."
  COMPARE_REF=$(git merge-base "HEAD" "origin/$DEFAULT_BRANCH" || git merge-base "HEAD" "$DEFAULT_BRANCH" || echo "")
  if [[ -z "$COMPARE_REF" ]]; then
    echo "Error: Could not determine a suitable Git reference to compare against. Please provide one manually."
    exit 1
  fi
fi

echo "\nRunning affected tests by comparing against: '$COMPARE_REF'"

# Get affected packages that have changed or whose dependencies have changed
# --filter-prod: includes packages that have changed and their direct/indirect dependents
# --filter-dev: includes packages that have changed and their direct/indirect dev dependents
# We use both to be comprehensive for testing.

AFFECTED_PACKAGES=$(pnpm --filter-prod "...[$COMPARE_REF]" --filter-dev "...[$COMPARE_REF]" recursive list --json --depth -1 || true)

if [[ "$AFFECTED_PACKAGES" == "[]" || "$AFFECTED_PACKAGES" == "" ]]; then
  echo "\nNo packages affected by changes since '$COMPARE_REF'. Skipping tests. ✅"
  exit 0
fi

# Extract package names from the JSON output
PACKAGE_NAMES=$(echo "$AFFECTED_PACKAGES" | jq -r '.[] | .name')

if [[ -z "$PACKAGE_NAMES" ]]; then
  echo "\nNo package names found in affected list. This might indicate an issue or no relevant changes. Skipping tests. ✅"
  exit 0
fi

echo "\nDetected affected packages:"
echo "$PACKAGE_NAMES" | sed 's/^/- /'

echo "\nRunning tests for affected packages..."

# Run tests for affected packages using pnpm filter
# We use --stream to see output from each package as it runs
# We use --fail-fast to stop on the first test failure
if pnpm --filter "{$(echo "$PACKAGE_NAMES" | tr '\n' ',')}" test --stream --fail-fast; then
  echo "\nAll affected tests passed successfully! ✅"
  exit 0
else
  echo "\nSome affected tests failed. ❌"
  exit 1
fi
