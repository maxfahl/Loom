#!/bin/bash

# audit_and_update_deps.sh
# Description: Audits Node.js project dependencies for vulnerabilities using npm audit
#              and provides options to fix them or list for manual review.
# Usage: ./audit_and_update_deps.sh [--fix] [--dry-run] [--project-path <path>]

# --- Configuration ---
DEFAULT_PROJECT_PATH="."

# --- Functions ---

# Function to display help message
show_help() {
  echo "Usage: $0 [--fix] [--dry-run] [--project-path <path>]"
  echo ""
  echo "Audits Node.js project dependencies for vulnerabilities using npm audit."
  echo "Provides options to automatically fix vulnerabilities or list them for manual review."
  echo ""
  echo "Options:"
  echo "  --fix             Attempt to automatically fix vulnerabilities using 'npm audit fix'."
  echo "  --dry-run         Show what 'npm audit fix' would do without actually making changes."
  echo "  --project-path    Specify the root path of the Node.js project (default: current directory)."
  echo "  -h, --help        Display this help message."
  echo ""
  echo "Example:"
  echo "  $0 --fix --project-path /path/to/my/node-app"
  echo "  $0 --dry-run"
  echo "  $0"
  exit 0
}

# Function to print messages in color
print_info() { echo -e "\033[0;34m[INFO]\033[0m $1"; }
print_success() { echo -e "\033[0;32m[SUCCESS]\033[0m $1"; }
print_warning() { echo -e "\033[0;33m[WARNING]\033[0m $1"; }
print_error() { echo -e "\033[0;31m[ERROR]\033[0m $1"; exit 1; }

# --- Main Script ---

# Parse arguments
FIX=false
DRY_RUN=false
PROJECT_PATH="$DEFAULT_PROJECT_PATH"

while [[ "$#" -gt 0 ]]; do
  key="$1"
  case $key in
    --fix)
      FIX=true
      shift
      ;;
    --dry-run)
      DRY_RUN=true
      shift
      ;;
    --project-path)
      PROJECT_PATH="$2"
      shift # past argument
      shift # past value
      ;;
    -h|--help)
      show_help
      ;;
    *)
      print_error "Unknown option: $1. Use --help for usage."
      ;;
  esac
done

# Resolve project path to absolute path
PROJECT_PATH=$(realpath "$PROJECT_PATH")

# Check if package.json exists
if [ ! -f "$PROJECT_PATH/package.json" ]; then
  print_error "package.json not found in '$PROJECT_PATH'. Please ensure this is a Node.js project root."
fi

print_info "Navigating to project directory: $PROJECT_PATH"
cd "$PROJECT_PATH" || print_error "Failed to change to project directory '$PROJECT_PATH'."

print_info "Running npm audit to check for vulnerabilities..."

# Run npm audit
AUDIT_OUTPUT=$(npm audit --json)
AUDIT_EXIT_CODE=$?

if [ $AUDIT_EXIT_CODE -eq 0 ]; then
  print_success "No known vulnerabilities found."
  exit 0
fi

# Parse audit output for summary
TOTAL_VULNERABILITIES=$(echo "$AUDIT_OUTPUT" | jq '.metadata.vulnerabilities.total')
FIXABLE_VULNERABILITIES=$(echo "$AUDIT_OUTPUT" | jq '.metadata.vulnerabilities.fixable.total')

print_warning "Found $TOTAL_VULNERABILITIES total vulnerabilities, $FIXABLE_VULNERABILITIES of which are fixable."

if [ "$FIX" = true ]; then
  if [ "$DRY_RUN" = true ]; then
    print_info "Performing a dry run of 'npm audit fix'..."
    npm audit fix --dry-run
    print_info "Dry run complete. No changes were made."
  else
    print_info "Attempting to fix vulnerabilities with 'npm audit fix'..."
    npm audit fix
    FIX_EXIT_CODE=$?
    if [ $FIX_EXIT_CODE -eq 0 ]; then
      print_success "'npm audit fix' completed successfully. Re-running audit to confirm."
      # Re-run audit to confirm fixes
      npm audit
    else
      print_error "'npm audit fix' failed or could not fix all vulnerabilities. Please review the output above."
    fi
  fi
elif [ "$DRY_RUN" = true ]; then
  print_info "Running 'npm audit' in detail (no fix attempt, dry-run for fix not requested)."
  npm audit
else
  print_info "To attempt automatic fixes, run with the --fix option."
  print_info "Listing all vulnerabilities for manual review:"
  npm audit
fi

print_info "Audit process complete."

exit 0
