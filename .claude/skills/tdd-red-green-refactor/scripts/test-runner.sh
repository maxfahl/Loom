#!/bin/bash

# test-runner.sh
# Description: A versatile shell script to run tests efficiently, supporting watch mode
#              and specific test filters to speed up the Red-Green cycle.
# Usage: ./test-runner.sh [--lang <language>] [--watch] [--filter <pattern>] [-- <extra_args>]
#
# Options:
#   --lang <language>   Specify the primary language: 'js', 'ts' (TypeScript), 'py' (Python).
#                       Defaults to 'ts'.
#   --watch             Run tests in watch mode (if supported by the test runner).
#   --filter <pattern>  Filter tests by name or path (e.g., 'add', 'user.test.ts').
#   -- <extra_args>     Pass additional arguments directly to the underlying test runner.
#   --help              Display this help message.

set -euo pipefail

# --- Configuration Variables ---
COLOR_RESET="\033[0m"
COLOR_RED="\033[0;31m"
COLOR_GREEN="\033[0;32m"
COLOR_YELLOW="\033[0;33m"
COLOR_BLUE="\033[0;34m"

DEFAULT_LANG="ts"

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
  local lang="$DEFAULT_LANG"
  local watch_mode=false
  local filter_pattern=""
  local extra_args=()

  # Parse arguments
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --lang)
        lang="$2"
        shift 2
        ;;
      --watch)
        watch_mode=true
        shift
        ;;
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

  log_info "Running tests for language: $lang"

  local test_command=()

  case "$lang" in
    js|ts)
      if ! command -v jest &> /dev/null; then
        log_error "Jest not found. Please install it (e.g., npm install -g jest or npm install --save-dev jest)."
      fi
      test_command=("jest")
      if [[ "$watch_mode" == true ]]; then
        test_command+=("--watchAll")
      fi
      if [[ -n "$filter_pattern" ]]; then
        test_command+=("--testNamePattern" "$filter_pattern")
      fi
      test_command+=("${extra_args[@]}")
      ;;
    py)
      if ! command -v pytest &> /dev/null; then
        # Check if pytest is available in a local venv
        if [[ -f "venv/bin/pytest" ]]; then
          test_command=("venv/bin/pytest")
        else
          log_error "Pytest not found. Please install it (e.g., pip install pytest) or ensure your virtual environment is activated."
        fi
      else
        test_command=("pytest")
      fi

      if [[ "$watch_mode" == true ]]; then
        log_warning "Pytest does not have a built-in watch mode. Consider using `pytest-watch` (pip install pytest-watch) and running `ptw` directly."
        # For simplicity, we'll just run it once if watch mode is requested for pytest
      fi
      if [[ -n "$filter_pattern" ]]; then
        test_command+=("-k" "$filter_pattern") # Pytest uses -k for expression matching
      fi
      test_command+=("${extra_args[@]}")
      ;;
    *)
      log_error "Unsupported language: $lang. Choose 'js', 'ts', or 'py'."
      ;;
  esac

  log_info "Executing test command: ${test_command[@]}"

  # Execute the test command
  if "${test_command[@]}"; then
    log_success "All tests passed!"
    exit 0
  else
    log_error "Tests failed!"
    exit 1
  fi
}

# --- Script Entry Point ---
main "$@"
