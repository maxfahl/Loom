#!/bin/bash

# ci-cd-security-check.sh
#
# Purpose:
#   Integrates basic security checks into a CI/CD pipeline. This script performs
#   secret detection, runs linters with security-focused rules, and includes a
#   placeholder for static application security testing (SAST).
#   It's designed to be generic and adaptable to various CI/CD environments.
#
# Usage:
#   ./ci-cd-security-check.sh [OPTIONS]
#
# Options:
#   -p, --path <path>     Specify the project root directory (default: current directory)
#   -s, --skip <check>    Skip a specific check (e.g., 'secrets', 'lint', 'sast'). Can be used multiple times.
#   -d, --dry-run         Show commands that would be executed without running them
#   -h, --help            Display this help message
#
# Examples:
#   ./ci-cd-security-check.sh
#   ./ci-cd-security-check.sh --skip secrets --skip sast
#   ./ci-cd-security-check.sh -p ./my-app -d
#
# Requirements:
#   - `grep` (for basic secret detection)
#   - `eslint` (for JavaScript/TypeScript linting, if applicable)
#   - `flake8` (for Python linting, if applicable)
#   - Other linters/SAST tools as configured in the project.
#
# Exit Codes:
#   0 - All enabled security checks passed or dry run.
#   1 - One or more security checks failed.
#
# Configuration (Environment Variables):
#   - SECRETS_SCAN_PATTERNS: Comma-separated regex patterns for secret detection (default: common API keys, passwords)
#   - LINT_COMMAND: Command to run the linter (e.g., "npm run lint", "flake8 ./\n")
#   - SAST_COMMAND: Command to run the SAST tool (e.g., "semgrep --config=auto .\n")

# --- Configuration Variables ---
PROJECT_PATH="."
SKIP_SECRETS=false
SKIP_LINT=false
SKIP_SAST=false
DRY_RUN=false

# Default secret patterns (can be overridden by SECRETS_SCAN_PATTERNS env var)
DEFAULT_SECRETS_SCAN_PATTERNS="API_KEY|PASSWORD|SECRET_KEY|AWS_ACCESS_KEY_ID|AWS_SECRET_ACCESS_KEY|GH_TOKEN"
SECRETS_SCAN_PATTERNS="${SECRETS_SCAN_PATTERNS:-$DEFAULT_SECRETS_SCAN_PATTERNS}"

# Default lint and SAST commands (can be overridden by env vars)
LINT_COMMAND="${LINT_COMMAND:-}" # e.g., "npm run lint -- --format compact" or "flake8 ."
SAST_COMMAND="${SAST_COMMAND:-}" # e.g., "semgrep --config=auto ."

# --- Helper Functions ---

# Function to print messages in color
print_color() {
    COLOR=$1
    MESSAGE=$2
    NC='\033[0m' # No Color
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
        return 0
    else
        print_color "blue" "Executing: $COMMAND"
        eval "$COMMAND"
        return $?
    fi
}

# --- Main Logic ---

# Parse command-line arguments
while [[ "$#" -gt 0 ]]; do
    case "$1" in
        -p|--path) PROJECT_PATH="$2"; shift ;; 
        -s|--skip) 
            case "$2" in
                secrets) SKIP_SECRETS=true ;; 
                lint) SKIP_LINT=true ;; 
                sast) SKIP_SAST=true ;; 
                *) print_color "red" "Unknown check to skip: $2"; display_help ;; 
            esac
            shift ;; 
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

print_color "yellow" "Starting CI/CD security checks in '$PROJECT_PATH'..."

ALL_CHECKS_PASSED=true

# --- 1. Secret Detection ---
if [ "$SKIP_SECRETS" = false ]; then
    print_color "yellow" "\n--- Running Secret Detection ---"
    # Exclude common binary/dependency directories
    SECRET_SCAN_CMD="grep -r -E \"$SECRETS_SCAN_PATTERNS\" . --exclude-dir={.git,node_modules,vendor,build,dist,coverage}"
    if run_command "$SECRET_SCAN_CMD"; then
        print_color "green" "Secret detection completed: No obvious secrets found."
    else
        print_color "red" "Secret detection found potential secrets. Please review the output."
        ALL_CHECKS_PASSED=false
    fi
else
    print_color "yellow" "\n--- Skipping Secret Detection ---"
fi

# --- 2. Linting with Security Rules ---
if [ "$SKIP_LINT" = false ]; then
    print_color "yellow" "\n--- Running Linter with Security Rules ---"
    if [ -n "$LINT_COMMAND" ]; then
        if run_command "$LINT_COMMAND"; then
            print_color "green" "Linter with security rules passed."
        else
            print_color "red" "Linter with security rules failed. Please fix reported issues."
            ALL_CHECKS_PASSED=false
        fi
    else
        print_color "yellow" "LINT_COMMAND not set. Skipping linting with security rules."
    fi
else
    print_color "yellow" "\n--- Skipping Linting with Security Rules ---"
fi

# --- 3. Basic SAST Scan ---
if [ "$SKIP_SAST" = false ]; then
    print_color "yellow" "\n--- Running Basic SAST Scan ---"
    if [ -n "$SAST_COMMAND" ]; then
        if run_command "$SAST_COMMAND"; then
            print_color "green" "Basic SAST scan passed."
        else
            print_color "red" "Basic SAST scan found issues. Please review and fix."
            ALL_CHECKS_PASSED=false
        fi
    else
        print_color "yellow" "SAST_COMMAND not set. Skipping basic SAST scan."
    fi
else
    print_color "yellow" "\n--- Skipping Basic SAST Scan ---
"
fi

if [ "$DRY_RUN" = true ]; then
    print_color "yellow" "Dry run completed. No actual checks were performed."
    exit 0
elif [ "$ALL_CHECKS_PASSED" = true ]; then
    print_color "green" "\nAll CI/CD security checks passed successfully."
    exit 0
else
    print_color "red" "\nOne or more CI/CD security checks failed. Please review the output and address the issues."
    exit 1
fi
