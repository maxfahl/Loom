#!/bin/bash

# jest-coverage-reporter.sh
# Description: Runs Jest and generates a detailed test coverage report.
#              Supports setting coverage thresholds.
# Usage: ./jest-coverage-reporter.sh [--threshold <percentage>] [-- <extra_args>]
#
# Options:
#   --threshold <percentage> Set a global coverage threshold (e.g., 80 for 80%).
#                            If coverage falls below this, the script will exit with an error.
#   -- <extra_args>          Pass additional arguments directly to the Jest command.
#   --help                   Display this help message.

set -euo pipefail

# --- Configuration Variables ---
COLOR_RESET="\033[0m"
COLOR_RED="\033[0;31m"
COLOR_GREEN="\033[0;32m"
COLOR_YELLOW="\033[0;33m"
COLOR_BLUE="\033[0;34m"

DEFAULT_COVERAGE_THRESHOLD=""

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
  local coverage_threshold="$DEFAULT_COVERAGE_THRESHOLD"
  local extra_args=()

  # Parse arguments
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --threshold)
        coverage_threshold="$2"
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

  log_info "Generating Jest test coverage report..."

  if ! command -v jest &> /dev/null; then
    log_error "Jest not found. Please install it (e.g., npm install --save-dev jest)."
  fi

  local jest_command=("jest" "--coverage")

  if [[ -n "$coverage_threshold" ]]; then
    log_info "Setting global coverage threshold to ${coverage_threshold}%."
    jest_command+=("--coverageThreshold.global.branches=${coverage_threshold}")
    jest_command+=("--coverageThreshold.global.functions=${coverage_threshold}")
    jest_command+=("--coverageThreshold.global.lines=${coverage_threshold}")
    jest_command+=("--coverageThreshold.global.statements=${coverage_threshold}")
  fi

  jest_command+=("${extra_args[@]}")

  log_info "Executing command: ${jest_command[@]}"

  # Execute Jest
  if "${jest_command[@]}"; then
    log_success "Jest test coverage report generated successfully."
    exit 0
  else
    log_error "Jest test coverage check failed. See report above for details."
    exit 1
  fi
}

# --- Script Entry Point ---
main "$@"
