#!/bin/bash

# pipeline-config-validator.sh
#
# Purpose:
#   Validates CI/CD configuration files (e.g., GitHub Actions YAML, GitLab CI YAML)
#   for syntax errors and adherence to basic best practices *before* committing.
#   This prevents pipeline failures due to simple typos or structural issues.
#
# Usage:
#   ./pipeline-config-validator.sh [FILE_OR_DIR...]
#   If no arguments are provided, it defaults to checking common CI/CD file paths.
#
# Requirements:
#   - yamllint: For general YAML syntax validation.
#     Install: pip install yamllint (or brew install yamllint on macOS)
#   - (Optional) actionlint: For GitHub Actions specific validation.
#     Install: https://github.com/rhysd/actionlint#installation
#
# Configuration:
#   - YAMLLINT_CONFIG: Path to a custom yamllint configuration file.
#     Defaults to a basic configuration if not set.
#
# Exit Codes:
#   0: All files passed validation.
#   1: One or more files failed validation or a required tool is missing.

set -euo pipefail

# --- Configuration ---
YAMLLINT_CONFIG="${YAMLLINT_CONFIG:-}" # Can be overridden by environment variable

# --- Colors for better readability ---
RED="\033[0;31m"
GREEN="\033[0;32m"
YELLOW="\033[0;33m"
BLUE="\033[0;34m"
NC="\033[0m" # No Color

# --- Helper Functions ---

log_info() {
  echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
  echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warn() {
  echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
  echo -e "${RED}[ERROR]${NC} $1" >&2
}

# Function to display help message
show_help() {
  echo "Usage: $0 [FILE_OR_DIR...]"
  echo ""
  echo "  Validates CI/CD configuration files for syntax and basic best practices."
  echo "  If no arguments are provided, it checks common CI/CD file paths."
  echo ""
  echo "Arguments:"
  echo "  FILE_OR_DIR  One or more file paths or directories to validate."
  echo "               Directories will be searched for common CI/CD YAML files."
  echo ""
  echo "Environment Variables:"
  echo "  YAMLLINT_CONFIG  Path to a custom yamllint configuration file."
  echo "                   (e.g., YAMLLINT_CONFIG=./.yamllint.yml $0)"
  echo ""
  echo "Examples:"
  echo "  $0"
  echo "  $0 .github/workflows/ci.yml"
  echo "  $0 .github/workflows/ .gitlab-ci.yml"
  echo "  YAMLLINT_CONFIG=./my-yamllint.yml $0"
  echo ""
  echo "Requirements:"
  echo "  - yamllint: Install via 'pip install yamllint' or 'brew install yamllint'."
  echo "  - (Optional) actionlint: For GitHub Actions specific validation."
  echo "    See https://github.com/rhysd/actionlint#installation for installation."
}

# Check for yamllint
check_yamllint() {
  if ! command -v yamllint &> /dev/null;
  then
    log_error "yamllint is not installed."
    log_error "Please install it: 'pip install yamllint' or 'brew install yamllint'."
    exit 1
  fi
}

# Find CI/CD YAML files in a given path
find_ci_files() {
  local path="$1"
  find "$path" -type f \( -name "*.yml" -o -name "*.yaml" \) \
    -and \( -path "*/.github/workflows/*" -o -name ".gitlab-ci.yml" -o -name "Jenkinsfile" -o -path "*/.circleci/*" \)
}

# Validate a single YAML file using yamllint
validate_yaml_file() {
  local file="$1"
  log_info "Validating YAML syntax for: ${file}"
  if [ -n "$YAMLLINT_CONFIG" ] && [ -f "$YAMLLINT_CONFIG" ]; then
    yamllint -c "$YAMLLINT_CONFIG" "$file"
  else
    yamllint "$file"
  fi
}

# Main validation logic
main() {
  check_yamllint

  local files_to_validate=()
  local default_paths=(".github/workflows" ".gitlab-ci.yml" "Jenkinsfile" ".circleci")

  if [ "$#" -eq 0 ]; then
    log_info "No specific files/directories provided. Searching default CI/CD paths..."
    for p in "${default_paths[@]}"; do
      if [ -e "$p" ]; then
        if [ -f "$p" ]; then
          files_to_validate+=("$p")
        elif [ -d "$p" ]; then
          while IFS= read -r -d $'' file; do
            files_to_validate+=("$file")
          done < <(find_ci_files "$p" -print0)
        fi
      fi
    done
  else
    for arg in "$@"; do
      if [ -f "$arg" ]; then
        files_to_validate+=("$arg")
      elif [ -d "$arg" ]; then
        while IFS= read -r -d $'' file; do
          files_to_validate+=("$file")
        done < <(find_ci_files "$arg" -print0)
      else
        log_warn "Skipping '$arg': Not a valid file or directory."
      fi
    done
  fi

  if [ "${#files_to_validate[@]}" -eq 0 ]; then
    log_warn "No CI/CD configuration files found to validate."
    exit 0
  fi

  log_info "Found ${#files_to_validate[@]} files for validation."
  local validation_failed=0

  for file in "${files_to_validate[@]}"; do
    if validate_yaml_file "$file"; then
      log_success "  ✔ Passed: ${file}"
    else
      log_error "  ✖ Failed: ${file}"
      validation_failed=1
    fi

    # Optional: Add actionlint for GitHub Actions specific files
    if [[ "$file" == *.github/workflows/* ]] && command -v actionlint &> /dev/null; then
      log_info "  Running actionlint for GitHub Actions workflow: ${file}"
      if actionlint -color "$file"; then
        log_success "    ✔ actionlint passed for: ${file}"
      else
        log_error "    ✖ actionlint failed for: ${file}"
        validation_failed=1
      fi
    elif [[ "$file" == *.github/workflows/* ]]; then
      log_warn "  actionlint not found. Skipping GitHub Actions specific validation for: ${file}"
      log_warn "  Consider installing actionlint for more thorough GitHub Actions validation."
    fi
  done

  if [ "$validation_failed" -eq 0 ]; then
    log_success "All CI/CD configuration files passed validation!"
    exit 0
  else
    log_error "One or more CI/CD configuration files failed validation."
    exit 1
  fi
}

# Check for help argument
if [[ "$#" -gt 0 && ( "$1" == "--help" || "$1" == "-h" ) ]]; then
  show_help
  exit 0
fi

main "$@"
