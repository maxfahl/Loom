#!/bin/bash

# jest-test-watcher.sh
# Description: Runs Jest in watch mode with common options, allowing for rapid feedback during development.
# Usage: ./jest-test-watcher.sh [--filter <pattern>] [-- <extra_args>]
#
# Options:
#   --filter <pattern>  Filter tests by name or path (e.g., 'add', 'user.test.ts').
#   -- <extra_args>     Pass additional arguments directly to the Jest command.
#   --help              Display this help message.

set -euo pipefail

# --- Configuration Variables ---
COLOR_RESET="\033[0m"
COLOR_RED="\033[0;31m"
COLOR_GREEN="\033[0;32m"
COLOR_YELLOW="\033[0;33m"
COLOR_BLUE="\033[0;34m"

# --- Helper Functions ---
log_info() {
  echo -e "${COLOR_BLUE}[INFO]${COLOR_RESET} $1"
}

log_success() {
  echo -e "${COLOR_GREEN}[SUCCESS]${COLOR_RESET} $1"
}

log_warning() {
  echo -e "${COLOR_YELLOW}[WARNING]${COLOR_RESET} $1"
}

log_error() {
  echo -e "${COLOR_RED}[ERROR]${COLOR_RESET} $1" >&2
  exit 1
}

show_help() {
  grep "^# Usage:" "$0" | sed -e 's/^# //' -e 's/^Usage: //'
  grep "^#   --" "$0" | sed -e 's/^#   //'
  exit 0
}

# --- Main Logic ---
main() {
  local filter_pattern=""
  local extra_args=()

  # Parse arguments
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --filter)
        filter_pattern="$2"
        shift 2
        ;;
      --)
        shift
        extra_args=("$@")
        break
        ;;
      --help)
        show_help
        ;;
      -*)
        log_error "Unknown option: $1. Use --help for usage."
        ;;
      *)
        log_error "Unexpected argument: $1. Use --help for usage."
        ;;
    esac
  done

  log_info "Starting Jest in watch mode..."

  if ! command -v jest &> /dev/null; then
    log_error "Jest not found. Please install it (e.g., npm install --save-dev jest)."
  fi

  local jest_command=("jest" "--watchAll")

  if [[ -n "$filter_pattern" ]]; then
    jest_command+=("--testNamePattern" "$filter_pattern")
  fi

  jest_command+=("${extra_args[@]}")

  log_info "Executing command: ${jest_command[@]}"

  # Execute Jest
  if "${jest_command[@]}"; then
    log_success "Jest watcher exited successfully."
    exit 0
  else
    log_error "Jest watcher exited with errors."
    exit 1
  fi
}

# --- Script Entry Point ---
main "$@"
