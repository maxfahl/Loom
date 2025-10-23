#!/bin/bash

# strict-mode-checker.sh
# Description: Runs TypeScript compilation with specific strict flags enabled,
#              providing a focused report on violations. Useful for CI/CD or pre-commit hooks.
# Usage: ./strict-mode-checker.sh [OPTIONS]
#
# Options:
#   --project <path>    Specify the path to the tsconfig.json file or project root.
#                       Defaults to the current directory.
#   --flags <flags>     Comma-separated list of specific strict flags to check (e.g., noImplicitAny,strictNullChecks).
#                       If not provided, checks all flags implied by "strict": true.
#   --no-emit           Do not emit output files (default: true).
#   --help              Display this help message.

set -euo pipefail

# --- Configuration Variables ---
DEFAULT_TSCONFIG_PATH="."
DEFAULT_NO_EMIT=true

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
  local project_path="$DEFAULT_TSCONFIG_PATH"
  local specific_flags=""
  local no_emit="$DEFAULT_NO_EMIT"

  # Parse arguments
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --project)
        project_path="$2"
        shift 2
        ;; 
      --flags)
        specific_flags="$2"
        shift 2
        ;; 
      --no-emit)
        no_emit=true
        shift
        ;; 
      --emit)
        no_emit=false
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
        if [[ "$project_path" == "$DEFAULT_TSCONFIG_PATH" ]]; then
          project_path="$1"
        else
          log_error "Unexpected argument: $1. Use --help for usage."
        fi
        shift
        ;; 
    esac
  done

  log_info "Starting TypeScript strict mode check for project: $project_path"

  # Check for npx and tsc
  if ! command -v npx &> /dev/null; then
    log_error "npx not found. Please ensure Node.js and npm are installed."
  fi
  if ! npx tsc --version &> /dev/null; then
    log_error "TypeScript compiler (tsc) not found. Please install it: npm install -g typescript or npm install --save-dev typescript."
  fi

  local tsc_command="npx tsc --project \"$project_path\""

  if [[ "$no_emit" == true ]]; then
    tsc_command+=" --noEmit"
  fi

  if [[ -n "$specific_flags" ]]; then
    log_info "Checking specific flags: $specific_flags"
    IFS=',' read -ra ADDR <<< "$specific_flags"
    for flag in "${ADDR[@]}"; do
      # Ensure the flag is a valid strict flag, otherwise tsc will error
      case "$flag" in
        strict|noImplicitAny|strictNullChecks|strictFunctionTypes|strictPropertyInitialization|strictBindCallApply|alwaysStrict|noImplicitThis|noUncheckedIndexedAccess|exactOptionalPropertyTypes|noImplicitOverride|noImplicitReturns|useUnknownInCatchVariables)
          tsc_command+=" --$flag"
          ;; 
        *)
          log_warning "Skipping unknown or non-strict flag: $flag"
          ;; 
      esac
    done
  else
    log_info "Checking all flags implied by \"strict\": true (or existing tsconfig.json)"
    # If no specific flags, rely on tsconfig.json's 'strict' setting
    # or add --strict if not explicitly checking other flags
    if [[ ! -f "$project_path/tsconfig.json" ]]; then
      log_warning "No tsconfig.json found at $project_path. Running with --strict flag."
      tsc_command+=" --strict"
    fi
  fi

  log_info "Executing command: $tsc_command"

  # Execute tsc and capture output/status
  if eval "$tsc_command"; then
    log_success "TypeScript strict mode check passed! No errors found."
    exit 0
  else
    log_error "TypeScript strict mode check failed! Errors found. See above for details."
    exit 1
  fi
}

# --- Script Entry Point ---
main "$@"
