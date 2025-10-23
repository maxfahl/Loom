#!/bin/bash

# scan-dependencies.sh
#
# Purpose:
#   Automates running Software Composition Analysis (SCA) tools to identify known vulnerabilities
#   in project dependencies. Supports npm (Node.js), pip (Python), and cargo (Rust) projects.
#   It provides a unified interface to trigger dependency audits and reports findings.
#
# Usage:
#   ./scan-dependencies.sh [OPTIONS]
#
# Options:
#   -p, --path <path>     Specify the project root directory (default: current directory)
#   -t, --type <type>     Specify project type: 'npm', 'pip', 'cargo', or 'all' (default: 'all')
#   -o, --output <file>   Save scan results to a file (default: stdout)
#   -d, --dry-run         Show commands that would be executed without running them
#   -h, --help            Display this help message
#
# Examples:
#   ./scan-dependencies.sh --type npm
#   ./scan-dependencies.sh -p ../my-python-app -t pip -o python_sca_report.txt
#   ./scan-dependencies.sh --dry-run
#
# Requirements:
#   - npm (for Node.js projects)
#   - pip (for Python projects, 'pip-audit' recommended)
#   - cargo (for Rust projects, 'cargo audit' recommended)
#
# Exit Codes:
#   0 - Success, no vulnerabilities found or dry run
#   1 - Vulnerabilities found or an error occurred
#
# Configuration:
#   - PIP_AUDIT_ARGS: Additional arguments for pip-audit (e.g., "--strict")
#   - NPM_AUDIT_ARGS: Additional arguments for npm audit (e.g., "--audit-level=high")
#   - CARGO_AUDIT_ARGS: Additional arguments for cargo audit (e.g., "--deny warnings")

# --- Configuration Variables ---
PROJECT_PATH="."
PROJECT_TYPE="all"
OUTPUT_FILE=""
DRY_RUN=false

# Additional arguments for specific tools (can be overridden by environment variables)
PIP_AUDIT_ARGS="${PIP_AUDIT_ARGS:-}"
NPM_AUDIT_ARGS="${NPM_AUDIT_ARGS:-}"
CARGO_AUDIT_ARGS="${CARGO_AUDIT_ARGS:-}"

# --- Helper Functions ---

# Function to print messages in color
print_color() {
    COLOR=$1
    MESSAGE=$2
    NC='[0m' # No Color
    case "$COLOR" in
        "red")    echo -e "\033[0;31m${MESSAGE}${NC}" ;;
        "green")  echo -e "\033[0;32m${MESSAGE}${NC}" ;;
        "yellow") echo -e "\033[0;33m${MESSAGE}${NC}" ;;
        "blue")   echo -e "\033[0;34m${MESSAGE}${NC}" ;;
        *)        echo -e "${MESSAGE}" ;;
    esac
}

# Function to display help message
display_help() {
    grep "^# Usage:" "$0" | sed -e "s/^# //"
    grep "^# Options:" "$0" | sed -e "s/^# //"
    grep "^# Examples:" "$0" | sed -e "s/^# //"
    grep "^# Requirements:" "$0" | sed -e "s/^# //"
    grep "^# Exit Codes:" "$0" | sed -e "s/^# //"
    grep "^# Configuration:" "$0" | sed -e "s/^# //"
    exit 0
}

# Function to run a command, handling dry-run and output redirection
run_command() {
    COMMAND="$@"
    if [ "$DRY_RUN" = true ]; then
        print_color "blue" "DRY RUN: $COMMAND"
    else
        print_color "blue" "Executing: $COMMAND"
        if [ -n "$OUTPUT_FILE" ]; then
            eval "$COMMAND" >> "$OUTPUT_FILE" 2>&1
        else
            eval "$COMMAND"
        fi
        return $?
    fi
    return 0
}

# --- Main Logic ---

# Parse command-line arguments
while [[ "$#" -gt 0 ]]; do
    case "$1" in
        -p|--path) PROJECT_PATH="$2"; shift ;;
        -t|--type) PROJECT_TYPE="$2"; shift ;;
        -o|--output) OUTPUT_FILE="$2"; shift ;;
        -d|--dry-run) DRY_RUN=true ;;
        -h|--help) display_help ;;
        *) print_color "red" "Unknown parameter: $1"; display_help ;;
    esac
    shift
done

# Resolve project path
PROJECT_PATH=$(realpath "$PROJECT_PATH")
if [ ! -d "$PROJECT_PATH" ]; then
    print_color "red" "Error: Project path '$PROJECT_PATH' does not exist or is not a directory."
    exit 1
fi
cd "$PROJECT_PATH" || { print_color "red" "Error: Could not change to directory '$PROJECT_PATH'."; exit 1; }

print_color "yellow" "Starting dependency scan in '$PROJECT_PATH' for type(s): '$PROJECT_TYPE'..."

SCAN_SUCCESS=true

# NPM Audit
if [[ "$PROJECT_TYPE" == "npm" || "$PROJECT_TYPE" == "all" ]]; then
    if [ -f "package.json" ]; then
        print_color "yellow" "--- Running npm audit ---"
        if command -v npm &> /dev/null; then
            run_command "npm audit $NPM_AUDIT_ARGS"
            if [ $? -ne 0 ]; then
                print_color "red" "npm audit found vulnerabilities or encountered an error."
                SCAN_SUCCESS=false
            else
                print_color "green" "npm audit completed with no critical vulnerabilities."
            fi
        else
            print_color "red" "npm not found. Skipping npm audit."
            SCAN_SUCCESS=false
        fi
    else
        print_color "yellow" "package.json not found. Skipping npm audit."
    fi
fi

# PIP Audit
if [[ "$PROJECT_TYPE" == "pip" || "$PROJECT_TYPE" == "all" ]]; then
    if [ -f "requirements.txt" ] || [ -f "pyproject.toml" ]; then
        print_color "yellow" "--- Running pip audit ---"
        if command -v pip-audit &> /dev/null; then
            run_command "pip-audit $PIP_AUDIT_ARGS"
            if [ $? -ne 0 ]; then
                print_color "red" "pip-audit found vulnerabilities or encountered an error."
                SCAN_SUCCESS=false
            else
                print_color "green" "pip-audit completed with no critical vulnerabilities."
            fi
        else
            print_color "red" "pip-audit not found. Please install it (e.g., 'pip install pip-audit'). Skipping pip audit."
            SCAN_SUCCESS=false
        fi
    else
        print_color "yellow" "requirements.txt or pyproject.toml not found. Skipping pip audit."
    fi
fi

# Cargo Audit
if [[ "$PROJECT_TYPE" == "cargo" || "$PROJECT_TYPE" == "all" ]]; then
    if [ -f "Cargo.toml" ]; then
        print_color "yellow" "--- Running cargo audit ---"
        if command -v cargo &> /dev/null && command -v cargo-audit &> /dev/null; then
            run_command "cargo audit $CARGO_AUDIT_ARGS"
            if [ $? -ne 0 ]; then
                print_color "red" "cargo audit found vulnerabilities or encountered an error."
                SCAN_SUCCESS=false
            else
                print_color "green" "cargo audit completed with no critical vulnerabilities."
            fi
        else
            print_color "red" "cargo or cargo-audit not found. Please install cargo-audit (e.g., 'cargo install cargo-audit'). Skipping cargo audit."
            SCAN_SUCCESS=false
        fi
    else
        print_color "yellow" "Cargo.toml not found. Skipping cargo audit."
    fi
fi

if [ "$DRY_RUN" = true ]; then
    print_color "yellow" "Dry run completed. No actual scans were performed."
    exit 0
elif [ "$SCAN_SUCCESS" = true ]; then
    print_color "green" "All requested dependency scans completed successfully with no reported vulnerabilities."
    exit 0
else
    print_color "red" "Dependency scan completed with reported vulnerabilities or errors. Please check the output."
    exit 1
fi
