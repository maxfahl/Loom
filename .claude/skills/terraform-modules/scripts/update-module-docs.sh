#!/bin/bash

# update-module-docs.sh
#
# Purpose:
#   Automates the generation or update of README.md documentation for a Terraform module
#   using 'terraform-docs'. This ensures that module documentation (inputs, outputs,
#   requirements, providers) is always accurate and up-to-date.
#
# Usage:
#   ./update-module-docs.sh <module_path> [--check] [--dry-run]
#
# Arguments:
#   <module_path> : The path to the Terraform module directory (e.g., "./my-module").
#                   Defaults to the current directory if not provided.
#   --check       : Optional. If present, the script will only check if the README.md
#                   is up-to-date without modifying it. Exits with 0 if up-to-date,
#                   1 otherwise.
#   --dry-run     : Optional. If present, the script will only print the 'terraform-docs'
#                   command that would be executed without actually running it.
#
# Example:
#   ./update-module-docs.sh ./modules/aws-vpc
#   ./update-module-docs.sh . --check
#   ./update-module-docs.sh ./my-module --dry-run
#
# Configuration:
#   - Requires 'terraform-docs' to be installed and available in the system's PATH.
#     Installation instructions: https://terraform-docs.io/user-guide/installation/
#
# Error Handling:
#   - Exits if 'terraform-docs' is not found.
#   - Exits if the specified module path is not a valid directory.
#   - Provides informative messages for all actions.

set -euo pipefail

# --- Colors for better readability ---
GREEN=\'\033[0;32m\'
YELLOW=\'\033[0;33m\'
RED=\'\033[0;31m\'
NC=\'\033[0m\' # No Color

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

MODULE_PATH="."
CHECK_MODE=false
DRY_RUN=false

# Parse arguments
for arg in "$@"; do
  case $arg in
    --check)
      CHECK_MODE=true
      shift
      ;;
    --dry-run)
      DRY_RUN=true
      shift
      ;;
    *)
      if [[ -z "$MODULE_PATH" || "$MODULE_PATH" == "." ]]; then
        MODULE_PATH="$arg"
      else
        log_error "Unknown argument or multiple module paths provided: $arg"
      fi
      shift
      ;;
  esac
done

# Validate terraform-docs installation
if ! command -v terraform-docs &> /dev/null; then
  log_error "terraform-docs is not installed or not found in PATH. Please install it: https://terraform-docs.io/user-guide/installation/"
fi

# Validate module path
if [[ ! -d "$MODULE_PATH" ]]; then
  log_error "Module path '$MODULE_PATH' is not a valid directory. Aborting."
fi

log_info "Processing Terraform module at: '$MODULE_PATH'"

TERRAFORM_DOCS_CMD="terraform-docs markdown table --output-file README.md --output-mode inject $MODULE_PATH"

if "$CHECK_MODE"; then
  log_info "Running in check mode: Verifying if README.md is up-to-date."
  TERRAFORM_DOCS_CMD="terraform-docs markdown table --check --output-file README.md --output-mode inject $MODULE_PATH"
  if "$DRY_RUN"; then
    log_warn "Dry run enabled. Would execute: $TERRAFORM_DOCS_CMD"
    exit 0
  fi
  if eval "$TERRAFORM_DOCS_CMD"; then
    log_info "README.md is up-to-date for module '$MODULE_PATH'."
    exit 0
  else
    log_error "README.md is OUTDATED for module '$MODULE_PATH'. Please run without --check to update."
  fi
else
  log_info "Generating/Updating README.md for module '$MODULE_PATH'."
  if "$DRY_RUN"; then
    log_warn "Dry run enabled. Would execute: $TERRAFORM_DOCS_CMD"
    exit 0
  fi
  if eval "$TERRAFORM_DOCS_CMD"; then
    log_info "Successfully generated/updated README.md for module '$MODULE_PATH'."
  else
    log_error "Failed to generate/update README.md for module '$MODULE_PATH'. Check terraform-docs output above."
  fi
fi
