#!/bin/bash

# validate-workflow.sh
#
# Purpose:
#   Validates and lints GitHub Actions workflow files using 'actionlint'.
#   This ensures that workflow syntax is correct, follows best practices,
#   and helps catch common errors before committing.
#
# Usage:
#   ./validate-workflow.sh [<workflow_file_or_dir>] [--dry-run]
#
# Arguments:
#   <workflow_file_or_dir> : Optional. The path to a specific workflow YAML file
#                            or a directory containing workflow files (e.g., ".github/workflows").
#                            Defaults to ".github/workflows" if not provided.
#   --dry-run              : Optional. If present, the script will only print the
#                            'actionlint' command that would be executed without actually running it.
#
# Example:
#   ./validate-workflow.sh .github/workflows/ci.yml
#   ./validate-workflow.sh .github/workflows
#   ./validate-workflow.sh --dry-run
#
# Configuration:
#   - Requires 'actionlint' to be installed and available in the system's PATH.
#     Installation instructions: https://github.com/rhysd/actionlint#installation
#   - TFLint configuration can be managed via a .tflint.hcl file in the module directory.
#
# Error Handling:
#   - Exits if 'actionlint' is not found.
#   - Exits if the specified path does not exist.
#   - Reports failures from 'actionlint' and exits with a non-zero status if issues are found.

set -euo pipefail

# --- Colors for better readability ---
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# --- Functions ---

log_info() {
  echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
  echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
  echo -e "${RED}[ERROR]${NC} $1" >&2
  exit 1
}

# --- Main Script Logic ---

TARGET_PATH=".github/workflows"
DRY_RUN=false

# Parse arguments
for arg in "$@"; do
  case $arg in
    --dry-run)
      DRY_RUN=true
      shift
      ;; 
    *)
      if [[ -z "$TARGET_PATH" || "$TARGET_PATH" == ".github/workflows" ]]; then
        TARGET_PATH="$arg"
      else
        log_error "Unknown argument or multiple paths provided: $arg"
      fi
      shift
      ;; 
  esac
done

# Validate actionlint installation
if ! command -v actionlint &> /dev/null; then
  log_error "actionlint is not installed or not found in PATH. Please install it: https://github.com/rhysd/actionlint#installation"
fi

# Validate target path
if [[ ! -e "$TARGET_PATH" ]]; then
  log_error "Target path '$TARGET_PATH' does not exist. Aborting."
fi

log_info "Starting validation for GitHub Actions workflows at: '$TARGET_PATH'"
if "$DRY_RUN"; then
  log_warn "Dry run enabled. Command will be printed but not executed."
fi

ACTIONLINT_CMD="actionlint $TARGET_PATH"

if "$DRY_RUN"; then
  log_info "Would execute: $ACTIONLINT_CMD"
else
  if eval "$ACTIONLINT_CMD"; then
    log_info "GitHub Actions workflow validation passed for '$TARGET_PATH'."
  else
    log_error "GitHub Actions workflow validation failed for '$TARGET_PATH'. Please review the issues reported by actionlint."
  fi
fi
