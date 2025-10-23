#!/bin/bash

# GitHub Actions Workflow Validator
#
# This script uses 'act' to locally validate GitHub Actions workflows for syntax
# and basic structural correctness. It helps catch errors before pushing to GitHub.
#
# Usage:
#   ./validate_workflow.sh --file .github/workflows/ci.yaml
#   ./validate_workflow.sh --dir .github/workflows
#   ./validate_workflow.sh -h # For help
#
# Requirements:
#   - act: https://github.com/nektos/act#installation
#     Install with: brew install act (macOS) or refer to documentation for other OS.
#
# Features:
# - Checks for 'act' installation.
# - Validates a specific workflow file or all workflows in a directory.
# - Provides clear output for validation results.

set -e

# --- Configuration ---
ACT_COMMAND="act"

# --- Functions ---

print_help() {
  echo "Usage: $(basename "$0") [OPTIONS]"
  echo "Validate GitHub Actions workflows locally using 'act'."
  echo ""
  echo "Options:"
  echo "  -f, --file <PATH>      Path to a specific workflow file (e.g., .github/workflows/ci.yaml)"
  echo "  -d, --dir <PATH>       Path to a directory containing workflow files (e.g., .github/workflows)"
  echo "  -h, --help             Display this help message."
  echo ""
  echo "Requirements:"
  echo "  - 'act' must be installed and available in your PATH."
  echo "    Installation: https://github.com/nektos/act#installation"
  echo "    Example (macOS): brew install act"
  echo ""
  echo "Example:"
  echo "  $(basename "$0") --file .github/workflows/main.yaml"
  echo "  $(basename "$0") --dir .github/workflows"
}

check_act_installed() {
  if ! command -v "$ACT_COMMAND" &> /dev/null;
  then
    echo "Error: 'act' is not installed or not found in your PATH." >&2
    echo "Please install 'act' to use this script. Refer to: https://github.com/nektos/act#installation" >&2
    exit 1
  fi
}

validate_file() {
  local file_path="$1"
  if [[ ! -f "$file_path" ]]; then
    echo "Error: Workflow file not found at '$file_path'." >&2
    exit 1
  fi

  echo "Validating workflow file: '$file_path'..."
  # Using --dry-run to validate syntax without actually executing jobs
  # --workflows to specify the file to validate
  if "$ACT_COMMAND" --dry-run --workflows "$file_path" &> /dev/null;
  then
    echo "✅ Validation successful for '$file_path'."
  else
    echo "❌ Validation failed for '$file_path'. See output above for details." >&2
    # Rerun without redirecting output to show errors
    "$ACT_COMMAND" --dry-run --workflows "$file_path"
    exit 1
  fi
}

validate_directory() {
  local dir_path="$1"
  if [[ ! -d "$dir_path" ]]; then
    echo "Error: Workflow directory not found at '$dir_path'." >&2
    exit 1
  fi

  echo "Validating all workflow files in directory: '$dir_path'..."
  local workflow_files=($(find "$dir_path" -name "*.yaml" -o -name "*.yml"))

  if [[ ${#workflow_files[@]} -eq 0 ]]; then
    echo "No .yaml or .yml workflow files found in '$dir_path'."
    exit 0
  fi

  local all_valid=true
  for file in "${workflow_files[@]}"; do
    echo "---"
    if ! "$ACT_COMMAND" --dry-run --workflows "$file" &> /dev/null;
    then
      echo "❌ Validation failed for '$file'. See output above for details." >&2
      "$ACT_COMMAND" --dry-run --workflows "$file"
      all_valid=false
    else
      echo "✅ Validation successful for '$file'."
    fi
  done

  if ! "$all_valid"; then
    echo "\nSummary: Some workflow files failed validation." >&2
    exit 1
  else
    echo "\nSummary: All workflow files validated successfully."
  fi
}

# --- Main Logic ---

check_act_installed

FILE_TO_VALIDATE=""
DIR_TO_VALIDATE=""

while [[ "$#" -gt 0 ]]; do
  key="$1"
  case $key in
    -f|--file)
      FILE_TO_VALIDATE="$2"
      shift # past argument
      shift # past value
      ;; 
    -d|--dir)
      DIR_TO_VALIDATE="$2"
      shift # past argument
      shift # past value
      ;; 
    -h|--help)
      print_help
      exit 0
      ;; 
    *)
      echo "Unknown option: $1" >&2
      print_help
      exit 1
      ;; 
  esac
done

if [[ -n "$FILE_TO_VALIDATE" && -n "$DIR_TO_VALIDATE" ]]; then
  echo "Error: Cannot specify both --file and --dir." >&2
  print_help
  exit 1
elif [[ -n "$FILE_TO_VALIDATE" ]]; then
  validate_file "$FILE_TO_VALIDATE"
elif [[ -n "$DIR_TO_VALIDATE" ]]; then
  validate_directory "$DIR_TO_VALIDATE"
else
  echo "Error: Please specify either --file or --dir." >&2
  print_help
  exit 1
fi
