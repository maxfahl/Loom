#!/bin/bash

# code-quality-checker.sh
#
# Description:
#   Automates running a suite of code quality checks for a .NET solution.
#   It performs code formatting, builds the solution (which includes Roslyn analyzers),
#   and executes unit tests. Designed for local use or CI/CD pipelines.
#
# Usage:
#   ./code-quality-checker.sh [--solution <SolutionFile>] [--dry-run]
#
# Arguments:
#   --solution <SolutionFile> : Optional. Path to the .sln file. If not provided,
#                               the script will search for one in the current directory.
#   --dry-run                 : Optional. If present, commands will only be printed
#                               without executing them.
#
# Example:
#   ./code-quality-checker.sh
#   ./code-quality-checker.sh --solution MyProject.sln
#   ./code-quality-checker.sh --dry-run

# --- Configuration ---
# Define colors for output
GREEN="\033[0;32m"
YELLOW="\033[0;33m"
RED="\033[0;31m"
NC="\033[0m" # No Color

# --- Helper Functions ---

# Function to print messages in green
print_success() {
  echo -e "${GREEN}[SUCCESS] $1${NC}"
}

# Function to print messages in yellow
print_info() {
  echo -e "${YELLOW}[INFO] $1${NC}"
}

# Function to print messages in red
print_error() {
  echo -e "${RED}[ERROR] $1${NC}"
}

# Function to execute a command or print it in dry-run mode
execute_command() {
  local cmd="$@"
  if [ "$DRY_RUN" = true ]; then
    print_info "DRY RUN: $cmd"
    return 0 # Always succeed in dry-run
  else
    print_info "Executing: $cmd"
    eval "$cmd"
    if [ $? -ne 0 ]; then
      print_error "Command failed: $cmd"
      return 1
    fi
  fi
  return 0
}

# --- Main Script Logic ---

SOLUTION_FILE=""
DRY_RUN=false

# Parse arguments
while [[ $# -gt 0 ]]; do
  key="$1"
  case $key in
    --solution)
      SOLUTION_FILE="$2"
      shift # past argument
      shift # past value
      ;;
    --dry-run)
      DRY_RUN=true
      print_info "Dry run mode activated. No commands will be executed."
      shift # past argument
      ;;
    *)
      print_error "Unknown option: $1"
      echo "Usage: $0 [--solution <SolutionFile>] [--dry-run]"
      exit 1
      ;;
  esac
done

# Find solution file if not provided
if [ -z "$SOLUTION_FILE" ]; then
  print_info "Searching for .sln file in current directory..."
  SOLUTION_FILE=$(find . -maxdepth 1 -name "*.sln" | head -n 1)
  if [ -z "$SOLUTION_FILE" ]; then
    print_error "No .sln file found in the current directory. Please specify with --solution."
    exit 1
  fi
  print_info "Found solution file: ${SOLUTION_FILE}"
fi

# --- Run Quality Checks ---

print_info "Starting code quality checks for ${SOLUTION_FILE}"

# 1. Run dotnet format
print_info "Running dotnet format..."
if ! execute_command "dotnet format "${SOLUTION_FILE}" --verify-no-changes"; then
  print_error "Code formatting issues found. Please run 'dotnet format' to fix them."
  exit 1
fi
print_success "Code formatting check passed."

# 2. Run dotnet build (includes Roslyn analyzers)
print_info "Building solution and running Roslyn analyzers..."
if ! execute_command "dotnet build "${SOLUTION_FILE}" --configuration Release"; then
  print_error "Build failed or Roslyn analyzers reported issues."
  exit 1
fi
print_success "Build and Roslyn analyzer checks passed."

# 3. Run dotnet test
print_info "Running unit tests..."
if ! execute_command "dotnet test "${SOLUTION_FILE}" --configuration Release --no-build"; then
  print_error "Unit tests failed."
  exit 1
fi
print_success "All unit tests passed."

print_success "All code quality checks completed successfully!"
exit 0
