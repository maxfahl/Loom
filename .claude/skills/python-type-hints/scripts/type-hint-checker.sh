#!/bin/bash

# type-hint-checker.sh
# Description: Runs a specified static type checker (Mypy or Pyright) on the project,
#              providing a clear report of type errors.
# Usage: ./type-hint-checker.sh [OPTIONS]
#
# Options:
#   --project <path>    Specify the path to the project root directory.
#                       Defaults to the current directory.
#   --checker <name>    Specify the type checker to use: 'mypy' (default) or 'pyright'.
#   --strict            Run the type checker in strict mode (e.g., mypy --strict).
#   --help              Display this help message.

set -euo pipefail

# --- Configuration Variables ---
DEFAULT_PROJECT_PATH="."
DEFAULT_CHECKER="mypy"

# --- Helper Functions ---
log_info() {
  echo -e "\033[0;34m[INFO]\033[0m $1"
}

log_success() {
  echo -e "\033[0;32m[SUCCESS]\033[0m $1"
}

log_warning() {
  echo -e "\033[0;33m[WARNING]\033[0m $1"
}

log_error() {
  echo -e "\033[0;31m[ERROR]\033[0m $1" >&2
  exit 1
}

show_help() {
  grep "^# Usage:" "$0" | sed -e 's/^# //' -e 's/^Usage: //'
  grep "^#   --" "$0" | sed -e 's/^#   //'
  exit 0
}

# --- Main Logic ---
main() {
  local project_path="$DEFAULT_PROJECT_PATH"
  local checker="$DEFAULT_CHECKER"
  local strict_mode=false

  # Parse arguments
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --project)
        project_path="$2"
        shift 2
        ;;
      --checker)
        checker="$2"
        shift 2
        ;;
      --strict)
        strict_mode=true
        shift
        ;;
      --help)
        show_help
        ;;
      -*)
        log_error "Unknown option: $1. Use --help for usage."
        ;;
      *)
        # Positional argument, assume it's project path if not already set
        if [[ "$project_path" == "$DEFAULT_PROJECT_PATH" ]]; then
          project_path="$1"
        else
          log_error "Unexpected argument: $1. Use --help for usage."
        fi
        shift
        ;;
    esac
  done

  log_info "Starting type checking for project: $project_path using $checker"

  local checker_command=("python3" "-m")
  local checker_args=()

  case "$checker" in
    mypy)
      checker_command+=("mypy")
      checker_args+=("$project_path")
      if [[ "$strict_mode" == true ]]; then
        checker_args+=("--strict")
      fi
      # Check if mypy is installed
      if ! command -v mypy &> /dev/null; then
        log_error "Mypy not found. Please install it: pip install mypy"
      fi
      ;;
    pyright)
      checker_command+=("pyright")
      checker_args+=("$project_path")
      if [[ "$strict_mode" == true ]]; then
        log_warning "Pyright is strict by default. --strict flag has no additional effect."
      fi
      # Check if pyright is installed
      if ! command -v pyright &> /dev/null; then
        log_error "Pyright not found. Please install it: npm install -g pyright or pip install pyright"
      fi
      ;;
    *)
      log_error "Unsupported type checker: $checker. Choose 'mypy' or 'pyright'."
      ;;
  esac

  log_info "Executing command: ${checker_command[@]} ${checker_args[@]}"

  # Execute type checker and capture output/status
  if "${checker_command[@]}" "${checker_args[@]}"; then
    log_success "Type check passed! No errors found using $checker."
    exit 0
  else
    log_error "Type check failed! Errors found using $checker. See above for details."
    exit 1
  fi
}

# --- Script Entry Point ---
main "$@"
