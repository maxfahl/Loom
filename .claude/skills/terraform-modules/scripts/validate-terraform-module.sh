#!/bin/bash

# validate-terraform-module.sh
#
# Purpose:
#   Automates the validation and linting of a Terraform module.
#   It runs 'terraform fmt -check', 'terraform validate', and 'tflint'
#   to ensure code quality, adherence to best practices, and correctness.
#
# Usage:
#   ./validate-terraform-module.sh <module_path> [--dry-run]
#
# Arguments:
#   <module_path> : The path to the Terraform module directory (e.g., "./my-module").
#                   Defaults to the current directory if not provided.
#   --dry-run     : Optional. If present, the script will only print the commands
#                   that would be executed without actually running them.
#
# Example:
#   ./validate-terraform-module.sh ./modules/aws-ec2
#   ./validate-terraform-module.sh .
#   ./validate-terraform-module.sh ./my-module --dry-run
#
# Configuration:
#   - Requires 'terraform' and 'tflint' to be installed and available in the system's PATH.
#     - Terraform installation: https://learn.hashicorp.com/tutorials/terraform/install-cli
#     - TFLint installation: https://github.com/terraform-linters/tflint#installation
#   - TFLint configuration can be managed via a .tflint.hcl file in the module directory.
#
# Error Handling:
#   - Exits if 'terraform' or 'tflint' are not found.
#   - Exits if the specified module path is not a valid directory.
#   - Reports failures for each validation step and exits with a non-zero status if any fail.

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

log_step() {
  echo -e "\n${BLUE}--- $1 ---${NC}"
}

# --- Main Script Logic ---

MODULE_PATH="."
DRY_RUN=false

# Parse arguments
for arg in "$@"; do
  case $arg in
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

# Validate tool installations
if ! command -v terraform &> /dev/null; then
  log_error "Terraform CLI is not installed or not found in PATH. Please install it: https://learn.hashicorp.com/tutorials/terraform/install-cli"
fi
if ! command -v tflint &> /dev/null; then
  log_warn "TFLint is not installed or not found in PATH. Skipping linting. Install it for full validation: https://github.com/terraform-linters/tflint#installation"
  TFLINT_INSTALLED=false
else
  TFLINT_INSTALLED=true
fi

# Validate module path
if [[ ! -d "$MODULE_PATH" ]]; then
  log_error "Module path '$MODULE_PATH' is not a valid directory. Aborting."
fi

log_info "Starting validation for Terraform module at: '$MODULE_PATH'"
if "$DRY_RUN"; then
  log_warn "Dry run enabled. Commands will be printed but not executed."
fi

# Change to module directory
pushd "$MODULE_PATH" > /dev/null || log_error "Failed to change directory to '$MODULE_PATH'."

# Initialize Terraform (required for validate)
log_step "Running 'terraform init'..."
if "$DRY_RUN"; then
  echo "Would execute: terraform init"
else
  if ! terraform init -backend=false -upgrade; then
    log_error "Terraform initialization failed. Please resolve the issues."
  fi
fi

# 1. Terraform Format Check
log_step "Running 'terraform fmt -check -recursive'..."
if "$DRY_RUN"; then
  echo "Would execute: terraform fmt -check -recursive ."
else
  if ! terraform fmt -check -recursive .; then
    log_error "Terraform formatting issues found. Run 'terraform fmt -recursive .' to fix."
  fi
  log_info "Terraform formatting check passed."
fi

# 2. Terraform Validate
log_step "Running 'terraform validate'..."
if "$DRY_RUN"; then
  echo "Would execute: terraform validate"
else
  if ! terraform validate; then
    log_error "Terraform validation failed. Please check your HCL syntax and configuration."
  fi
  log_info "Terraform validation passed."
fi

# 3. TFLint (if installed)
if "$TFLINT_INSTALLED"; then
  log_step "Running 'tflint'..."
  if "$DRY_RUN"; then
    echo "Would execute: tflint --recursive"
  else
    if ! tflint --recursive; then
      log_error "TFLint found issues. Please review and fix them."
    fi
    log_info "TFLint check passed."
  fi
else
  log_warn "TFLint not installed. Skipping linting step."
fi

# Return to original directory
popd > /dev/null || log_error "Failed to return to original directory."

log_info "Terraform module validation and linting completed successfully for '$MODULE_PATH'."
