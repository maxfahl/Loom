#!/bin/bash

# check-modern-js-usage.sh
#
# Purpose:
#   Scans a JavaScript/TypeScript codebase for common modern JavaScript feature
#   usage (e.g., `var`, old function syntax, missing optional chaining opportunities)
#   and reports potential areas for modernization.
#
# Usage:
#   ./check-modern-js-usage.sh [OPTIONS] [PATH]
#
# Options:
#   -h, --help        Display this help message.
#   -v, --verbose     Show more detailed output.
#   -i, --ignore-dir  Comma-separated list of directories to ignore (e.g., node_modules,dist).
#
# Arguments:
#   PATH              The directory to scan (default: current directory).
#
# Examples:
#   ./check-modern-js-usage.sh
#   ./check-modern-js-usage.sh src/
#   ./check-modern-js-usage.sh --verbose ./components
#   ./check-modern-js-usage.sh -i node_modules,build
#
# Requirements:
#   - `grep` command-line utility.

# --- Configuration ---
TARGET_PATH="."
VERBOSE=false
IGNORE_DIRS="node_modules,dist,build,coverage"

# --- Colors for output ---
GREEN="\033[0;32m"
YELLOW="\033[0;33m"
RED="\033[0;31m"
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

display_help() {
    grep 	'^#' "$0" | cut -c 3-
    exit 0
}

# --- Argument Parsing ---
while (( "$#" )); do
    case "$1" in
        -h|--help)
            display_help
            ;;
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        -i|--ignore-dir)
            if [ -n "$2" ] && [ "${2:0:1}" != "-" ]; then
                IGNORE_DIRS="$IGNORE_DIRS,$2"
                shift 2
            else
                log_error "Error: Argument for $1 is missing."
                exit 1
            fi
            ;;
        -*)
            log_warn "Unknown option: $1. Ignoring."
            shift
            ;;
        *)
            TARGET_PATH="$1"
            shift
            ;;
    esac
done

# Construct grep exclude patterns
GREP_EXCLUDE_PATTERN=""
IFS="," read -ra ADDR <<< "$IGNORE_DIRS"
for i in "${ADDR[@]}"; do
    GREP_EXCLUDE_PATTERN+=" --exclude-dir=$i"
done

log_info "Scanning directory: $TARGET_PATH"
log_info "Ignoring directories: $IGNORE_DIRS"

# --- Modernization Checks ---

# 1. Check for `var` keyword
log_info "Checking for 'var' keyword..."
VAR_USAGE=$(grep -r -n -E "\bvar\b" "$TARGET_PATH" --include=\*.{js,ts,jsx,tsx} $GREP_EXCLUDE_PATTERN)
if [ -n "$VAR_USAGE" ]; then
    log_warn "Found 'var' keyword usage. Consider replacing with 'let' or 'const'."
    if [ "$VERBOSE" = true ]; then
        echo "$VAR_USAGE"
    fi
else
    log_success "No 'var' keyword usage found."
fi

# 2. Check for traditional function declarations that could be arrow functions
log_info "Checking for traditional function declarations..."
FUNCTION_DECLARATION_USAGE=$(grep -r -n -E "^\s*function\s+[a-zA-Z_][a-zA-Z0-9_]*\s*\([^)]*\)\s*\{" "$TARGET_PATH" --include=\*.{js,ts,jsx,tsx} $GREP_EXCLUDE_PATTERN)
if [ -n "$FUNCTION_DECLARATION_USAGE" ]; then
    log_warn "Found traditional function declarations. Consider arrow functions for conciseness and lexical 'this'."
    if [ "$VERBOSE" = true ]; then
        echo "$FUNCTION_DECLARATION_USAGE"
    fi
else
    log_success "No traditional function declarations found."
fi

# 3. Check for string concatenation that could be template literals
log_info "Checking for string concatenations..."
STRING_CONCAT_USAGE=$(grep -r -n -E "\+\s*(\'\".*?\'\"|\b[a-zA-Z_][a-zA-Z0-9_]*\b)" "$TARGET_PATH" --include=\*.{js,ts,jsx,tsx} $GREP_EXCLUDE_PATTERN | grep -v -E "^\s*import|^\s*export")
if [ -n "$STRING_CONCAT_USAGE" ]; then
    log_warn "Found string concatenations. Consider using template literals (\\\`\\\`).
    (Note: This check can have false positives for valid arithmetic operations or import/export statements.)"
    if [ "$VERBOSE" = true ]; then
        echo "$STRING_CONCAT_USAGE"
    fi
else
    log_success "No obvious string concatenations found."
fi

# 4. Check for object property access without optional chaining (potential for null/undefined errors)
log_info "Checking for potential optional chaining opportunities..."
OPTIONAL_CHAINING_USAGE=$(grep -r -n -E "\b[a-zA-Z_][a-zA-Z0-9_]*\.[a-zA-Z_][a-zA-Z0-9_]*" "$TARGET_PATH" --include=\*.{js,ts,jsx,tsx} $GREP_EXCLUDE_PATTERN | grep -v -E "^\s*import|^\s*export")
# This is a very broad check and will have many false positives. It's meant to highlight areas for manual review.
if [ -n "$OPTIONAL_CHAINING_USAGE" ]; then
    log_warn "Found direct object property access. Consider using optional chaining (?. ) for potentially null/undefined properties.
    (Note: This check is very broad and will have many false positives. Review manually.)"
    if [ "$VERBOSE" = true ]; then
        echo "$OPTIONAL_CHAINING_USAGE"
    fi
else
    log_success "No obvious direct object property access found that could benefit from optional chaining."
fi

log_success "Modern JavaScript usage check complete."
log_info "Review the warnings and consider refactoring for better code quality."
