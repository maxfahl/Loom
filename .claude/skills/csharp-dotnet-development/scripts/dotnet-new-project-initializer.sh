#!/bin/bash

# dotnet-new-project-initializer.sh
#
# Description:
#   Automates the setup of a new .NET solution with a Web API project,
#   a class library for core logic, and an xUnit test project.
#   It also configures EditorConfig for consistent coding styles.
#
# Usage:
#   ./dotnet-new-project-initializer.sh <ProjectName> [--dry-run]
#
# Arguments:
#   <ProjectName> : The base name for the new solution and projects (e.g., "MyAwesomeApp").
#   --dry-run     : Optional. If present, the script will only print commands
#                   without executing them.
#
# Example:
#   ./dotnet-new-project-initializer.sh MyWebApp
#   ./dotnet-new-project-initializer.sh MyService --dry-run

# --- Configuration ---
WEBAPI_SUFFIX=".Api"
CORE_SUFFIX=".Core"
TEST_SUFFIX=".Tests"
TEST_FRAMEWORK="xunit" # Can be xunit, nunit, or mstest

# --- Helper Functions ---

# Function to print messages in green
print_success() {
  echo -e "\033[0;32m[SUCCESS] $1\033[0m"
}

# Function to print messages in yellow
print_info() {
  echo -e "\033[0;33m[INFO] $1\033[0m"
}

# Function to print messages in red
print_error() {
  echo -e "\033[0;31m[ERROR] $1\033[0m"
}

# Function to execute a command or print it in dry-run mode
execute_command() {
  if [ "$DRY_RUN" = true ]; then
    print_info "DRY RUN: $1"
  else
    print_info "Executing: $1"
    eval "$1"
    if [ $? -ne 0 ]; then
      print_error "Command failed: $1"
      exit 1
    fi
  fi
}

# --- Main Script Logic ---

# Check for required arguments
if [ -z "$1" ]; then
  print_error "Missing ProjectName argument."
  echo "Usage: $0 <ProjectName> [--dry-run]"
  exit 1
fi

PROJECT_BASE_NAME="$1"
DRY_RUN=false

# Parse optional arguments
for arg in "$@"; do
  case $arg in
    --dry-run)
      DRY_RUN=true
      print_info "Dry run mode activated. No commands will be executed."
      shift # Remove --dry-run from processing
      ;;
  esac
done

SOLUTION_NAME="${PROJECT_BASE_NAME}.sln"
WEBAPI_PROJECT_NAME="${PROJECT_BASE_NAME}${WEBAPI_SUFFIX}"
CORE_PROJECT_NAME="${PROJECT_BASE_NAME}${CORE_SUFFIX}"
TEST_PROJECT_NAME="${PROJECT_BASE_NAME}${TEST_SUFFIX}"

print_info "Initializing .NET solution: ${PROJECT_BASE_NAME}"

# 1. Create new solution
execute_command "dotnet new sln -n "${PROJECT_BASE_NAME}""

# 2. Create Web API project
execute_command "dotnet new webapi -n "${WEBAPI_PROJECT_NAME}" -o "${WEBAPI_PROJECT_NAME}""
execute_command "dotnet sln "${SOLUTION_NAME}" add "${WEBAPI_PROJECT_NAME}/${WEBAPI_PROJECT_NAME}.csproj""

# 3. Create Class Library project (Core)
execute_command "dotnet new classlib -n "${CORE_PROJECT_NAME}" -o "${CORE_PROJECT_NAME}""
execute_command "dotnet sln "${SOLUTION_NAME}" add "${CORE_PROJECT_NAME}/${CORE_PROJECT_NAME}.csproj""

# 4. Create xUnit Test project
execute_command "dotnet new ${TEST_FRAMEWORK} -n "${TEST_PROJECT_NAME}" -o "${TEST_PROJECT_NAME}""
execute_command "dotnet sln "${SOLUTION_NAME}" add "${TEST_PROJECT_NAME}/${TEST_PROJECT_NAME}.csproj""

# 5. Add project references
execute_command "dotnet add "${WEBAPI_PROJECT_NAME}/${WEBAPI_PROJECT_NAME}.csproj" reference "${CORE_PROJECT_NAME}/${CORE_PROJECT_NAME}.csproj""
execute_command "dotnet add "${TEST_PROJECT_NAME}/${TEST_PROJECT_NAME}.csproj" reference "${CORE_PROJECT_NAME}/${CORE_PROJECT_NAME}.csproj""
execute_command "dotnet add "${TEST_PROJECT_NAME}/${TEST_PROJECT_NAME}.csproj" reference "${WEBAPI_PROJECT_NAME}/${WEBAPI_PROJECT_NAME}.csproj""

# 6. Add EditorConfig (basic example)
EDITORCONFIG_CONTENT="""root = true

[*]
indent_style = space
indent_size = 4
end_of_line = lf
charset = utf-8
trim_trailing_whitespace = true
insert_final_newline = true

[*.cs]
csharp_indent_braces = false
csharp_new_line_before_open_brace = all
csharp_space_between_parentheses = false
csharp_preserve_single_line_blocks = true
csharp_preserve_single_line_statements = true
"""
execute_command "echo "${EDITORCONFIG_CONTENT}" > ".editorconfig""

# 7. Restore NuGet packages
execute_command "dotnet restore "${SOLUTION_NAME}""

print_success "Solution '${PROJECT_BASE_NAME}' initialized successfully!"
print_info "To run the Web API: cd ${WEBAPI_PROJECT_NAME} && dotnet run"
print_info "To run tests: cd ${TEST_PROJECT_NAME} && dotnet test"
