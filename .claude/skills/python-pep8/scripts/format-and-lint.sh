#!/bin/bash
# .devdev/skills/python-pep8/scripts/format-and-lint.sh

# Description:
# This script automates the process of formatting Python files with Black and then
# linting them with Ruff, ensuring both style consistency and adherence to best practices.
# It supports dry-run and fix modes for both tools.
#
# Usage:
#   ./format-and-lint.sh [OPTIONS] [PATH]
#
# Options:
#   -d, --dry-run    Perform a dry run (show changes without applying them).
#   -f, --fix        Automatically fix linting issues (Ruff only).
#   -h, --help       Display this help message.
#
# Arguments:
#   PATH             Optional. The path to a file or directory to process.
#                    Defaults to the current directory if not provided.
#
# Requirements:
#   - black: Python code formatter (pip install black)
#   - ruff: Python linter and formatter (pip install ruff)
#
# Example Usage:
#   ./format-and-lint.sh
#   ./format-and-lint.sh --dry-run src/my_module.py
#   ./format-and-lint.sh -f my_project/
#   ./format-and-lint.sh --help

# --- Configuration ---
DEFAULT_PATH="."
BLACK_COMMAND="black"
RUFF_COMMAND="ruff"

# --- Colors for output ---
GREEN="\033[0;32m"
YELLOW="\033[0;33m"
RED="\033[0;31m"
BLUE="\033[0;34m"
NC="\033[0m" # No Color

# --- Functions ---

# Function to display help message
show_help() {
    echo -e "${BLUE}Usage: $(basename "$0") [OPTIONS] [PATH]${NC}"
    echo ""
    echo "Description:"
    echo "  Automates formatting with Black and linting with Ruff for Python files."
    echo "  Ensures style consistency and adherence to best practices."
    echo ""
    echo "Options:"
    echo "  -d, --dry-run    Perform a dry run (show changes without applying them)."
    echo "  -f, --fix        Automatically fix linting issues (Ruff only)."
    echo "  -h, --help       Display this help message."
    echo ""
    echo "Arguments:"
    echo "  PATH             Optional. The path to a file or directory to process."
    echo "                   Defaults to the current directory if not provided."
    echo ""
    echo "Requirements:"
    echo "  - black: Python code formatter (pip install black)"
    echo "  - ruff: Python linter and formatter (pip install ruff)"
    echo ""
    echo "Example Usage:"
    echo "  $(basename "$0")"
    echo "  $(basename "$0") --dry-run src/my_module.py"
    echo "  $(basename "$0") -f my_project/"
    echo "  $(basename "$0") --help"
    exit 0
}

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# --- Main Script Logic ---

# Parse command-line arguments
DRY_RUN=false
FIX_MODE=false
TARGET_PATH=""

while [[ "$#" -gt 0 ]]; do
    case "$1" in
        -d|--dry-run)
            DRY_RUN=true
            shift
            ;;
        -f|--fix)
            FIX_MODE=true
            shift
            ;;
        -h|--help)
            show_help
            ;;
        -*)
            echo -e "${RED}Error: Unknown option '$1'${NC}"
            show_help
            ;;
        *)
            TARGET_PATH="$1"
            shift
            ;;
    esac
done

# Set target path to default if not provided
if [ -z "$TARGET_PATH" ]; then
    TARGET_PATH="$DEFAULT_PATH"
fi

echo -e "${BLUE}--- Starting Python Formatting and Linting ---${NC}"
echo -e "${YELLOW}Target Path: ${TARGET_PATH}${NC}"
echo -e "${YELLOW}Dry Run: ${DRY_RUN}${NC}"
echo -e "${YELLOW}Fix Mode: ${FIX_MODE}${NC}"
echo ""

# 1. Check for Black
if ! command_exists "$BLACK_COMMAND"; then
    echo -e "${RED}Error: Black is not installed. Please install it using 'pip install black'.${NC}"
    exit 1
fi

# 2. Check for Ruff
if ! command_exists "$RUFF_COMMAND"; then
    echo -e "${RED}Error: Ruff is not installed. Please install it using 'pip install ruff'.${NC}"
    exit 1
fi

# 3. Run Black (Formatter)
echo -e "${BLUE}Running Black formatter...${NC}"
BLACK_ARGS=()
if [ "$DRY_RUN" = true ]; then
    BLACK_ARGS+=("--check" "--diff")
else
    BLACK_ARGS+=("") # No specific args for in-place formatting
fi

if "$BLACK_COMMAND" "${BLACK_ARGS[@]}" "$TARGET_PATH"; then
    echo -e "${GREEN}Black formatting completed successfully.${NC}"
else
    echo -e "${YELLOW}Black found issues or made changes. Please review.${NC}"
    if [ "$DRY_RUN" = true ]; then
        echo -e "${YELLOW}Run without --dry-run to apply changes.${NC}"
    fi
fi
echo ""

# 4. Run Ruff (Linter)
echo -e "${BLUE}Running Ruff linter...${NC}"
RUFF_ARGS=()
if [ "$DRY_RUN" = true ]; then
    RUFF_ARGS+=("--check" "--diff")
fi
if [ "$FIX_MODE" = true ]; then
    RUFF_ARGS+=("--fix")
fi

if "$RUFF_COMMAND" "${RUFF_ARGS[@]}" "$TARGET_PATH"; then
    echo -e "${GREEN}Ruff linting completed successfully. No issues found.${NC}"
else
    echo -e "${RED}Ruff found linting issues.${NC}"
    if [ "$DRY_RUN" = true ]; then
        echo -e "${YELLOW}Run without --dry-run to apply changes, or with --fix to attempt automatic fixes.${NC}"
    elif [ "$FIX_MODE" = true ]; then
        echo -e "${YELLOW}Ruff attempted to fix issues. Please review remaining warnings/errors.${NC}"
    else
        echo -e "${YELLOW}Please address the reported linting issues.${NC}"
    fi
    exit 1 # Exit with error code if linting issues are found
fi

echo ""
echo -e "${GREEN}--- Python Formatting and Linting Finished ---${NC}"
exit 0
