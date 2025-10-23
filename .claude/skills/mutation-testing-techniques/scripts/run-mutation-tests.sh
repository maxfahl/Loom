#!/bin/bash

# run-mutation-tests.sh
# Description: Executes mutation tests using Stryker Mutator with optional filtering for changed files.
# This script allows running mutation tests on the entire project or only on files changed since a specific git ref.

# Usage:
#   ./run-mutation-tests.sh
#   ./run-mutation-tests.sh --diff [git_ref] (e.g., --diff main or --diff HEAD~1)
#   ./run-mutation-tests.sh --config [path_to_config.json]
#   ./run-mutation-tests.sh --dry-run

# --- Configuration Options ---
DEFAULT_CONFIG_FILE="stryker.conf.json"

# --- Functions ---
log_info() {
  echo "\033[0;34m[INFO]\033[0m $1"
}

log_success() {
  echo "\033[0;32m[SUCCESS]\033[0m $1"
}

log_warn() {
  echo "\033[0;33m[WARN]\033[0m $1"
}

log_error() {
  echo "\033[0;31m[ERROR]\033[0m $1"
  exit 1
}

show_help() {
  echo "Usage: $0 [OPTIONS]"
  echo "Executes mutation tests using Stryker Mutator."
  echo ""
  echo "Options:"
  echo "  --diff [git_ref]      Run mutation tests only on files changed since the given git reference."
  echo "                        Example: --diff main or --diff HEAD~1"
  echo "  --config [file_path]  Specify a custom Stryker configuration file. Defaults to '$DEFAULT_CONFIG_FILE'."
  echo "  --dry-run             Print the Stryker command without executing it."
  echo "  -h, --help            Show this help message and exit."
  echo ""
  echo "Examples:"
  echo "  $0                                  # Run all mutation tests with default config"
  echo "  $0 --diff main                      # Run mutation tests on files changed since 'main' branch"
  echo "  $0 --config my-stryker-config.json  # Run with a custom config file"
  echo "  $0 --dry-run                        # Show the command that would be executed"
}

# --- Main Script ---

DIFF_MODE=false
GIT_REF=""
CUSTOM_CONFIG=""
DRY_RUN=false

# Parse arguments
while [[ $# -gt 0 ]]; do
  key="$1"
  case $key in
    --diff)
      DIFF_MODE=true
      GIT_REF="$2"
      shift # past argument
      shift # past value
      ;;
    --config)
      CUSTOM_CONFIG="$2"
      shift # past argument
      shift # past value
      ;;
    --dry-run)
      DRY_RUN=true
      shift # past argument
      ;;
    -h|--help)
      show_help
      exit 0
      ;;
    *)
      log_error "Unknown option: $1. Use -h or --help for usage."
      ;;
  esac
done

CONFIG_FILE=${CUSTOM_CONFIG:-$DEFAULT_CONFIG_FILE}

if [ ! -f "$CONFIG_FILE" ]; then
  log_error "Stryker configuration file '$CONFIG_FILE' not found. Please run setup-stryker.sh or provide a valid config."
fi

STRYKER_COMMAND="npx stryker run -f $CONFIG_FILE"

if [ "$DIFF_MODE" = true ]; then
  if [ -z "$GIT_REF" ]; then
    log_error "--diff option requires a git reference (e.g., main, HEAD~1)."
  fi

  log_info "Detecting changed files since '$GIT_REF'..."
  # Get changed files, filter for .ts and .tsx, and format for Stryker's --mutate option
  CHANGED_FILES=$(git diff --name-only --diff-filter=ACMR "$GIT_REF" | grep -E '\.(ts|tsx)$' | tr '\n' ',')

  if [ -z "$CHANGED_FILES" ]; then
    log_warn "No relevant TypeScript/TSX files changed since '$GIT_REF'. Skipping mutation tests."
    exit 0
  fi

  # Remove trailing comma
  CHANGED_FILES=${CHANGED_FILES%}

  log_info "Running mutation tests on changed files: $CHANGED_FILES"
  STRYKER_COMMAND="$STRYKER_COMMAND --mutate $CHANGED_FILES"
else
  log_info "Running mutation tests on all configured files."
fi

if [ "$DRY_RUN" = true ]; then
  log_info "Dry run: The following command would be executed:"
  echo "$STRYKER_COMMAND"
else
  log_info "Executing Stryker Mutator..."
  eval "$STRYKER_COMMAND"
  EXIT_CODE=$?

  if [ $EXIT_CODE -eq 0 ]; then
    log_success "Mutation tests completed successfully. Check the HTML report for details."
  else
    log_error "Mutation tests failed or did not meet thresholds. Exit code: $EXIT_CODE"
  fi
fi
