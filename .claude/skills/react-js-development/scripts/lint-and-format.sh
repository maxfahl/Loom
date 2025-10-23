#!/bin/bash

# lint-and-format.sh
#
# Description:
#   Runs common linting (ESLint) and formatting (Prettier) tools for a React/TypeScript project.
#   It helps maintain code quality and consistency across the codebase.
#
# Usage:
#   ./lint-and-format.sh [--fix] [--path <path/to/project>] [--help]
#
# Examples:
#   ./lint-and-format.sh
#   ./lint-and-format.sh --fix
#   ./lint-and-format.sh --path src/components
#
# Configuration:
#   Assumes ESLint and Prettier are installed and configured in the project's devDependencies.
#   (e.g., via `npm install eslint prettier --save-dev`)
#
# Error Handling:
#   Reports errors from ESLint and Prettier commands.
#
# Dry-run:
#   Not directly supported, but running without --fix acts as a check.
#
# Colored Output:
#   Uses ANSI escape codes for better readability.

# --- Colors ---
GREEN="\033[0;32m"
YELLOW="\033[0;33m"
RED="\033[0;31m"
BLUE="\033[0;34m"
NC="\033[0m" # No Color

# --- Variables ---
FIX_MODE=false
TARGET_PATH="." # Default to current directory

# --- Functions ---

show_help() {
  echo -e "${BLUE}Usage:${NC} ./lint-and-format.sh [--fix] [--path <path/to/project>] [--help]"
  echo ""
  echo -e "${BLUE}Description:${NC}"
  echo "  Runs common linting (ESLint) and formatting (Prettier) tools for a React/TypeScript project."
  echo "  It helps maintain code quality and consistency across the codebase."
  echo ""
  echo -e "${BLUE}Options:${NC}"
  echo "  --fix                 (Optional) Automatically fix linting and formatting issues."
  echo "  --path <path>         (Optional) Specify the path to the project or a specific directory/file to process."
  echo "                        Defaults to the current directory ('.')."
  echo "  -h, --help            Display this help message."
  echo ""
  echo -e "${BLUE}Examples:${NC}"
  echo "  ./lint-and-format.sh"
  echo "  ./lint-and-format.sh --fix"
  echo "  ./lint-and-format.sh --path src/components"
  echo ""
  echo -e "${YELLOW}Note:${NC} Ensure ESLint and Prettier are installed as devDependencies in your project."
  exit 0
}

# --- Parse Arguments ---
while [[ "$#" -gt 0 ]]; do
  case "$1" in
    --fix)
      FIX_MODE=true
      shift
      ;;
    --path)
      if [ -n "$2" ] && [[ "$2" != -* ]]; then
        TARGET_PATH="$2"
        shift 2
      else
        echo -e "${RED}Error:${NC} --path requires a directory or file argument." >&2
        exit 1
      fi
      ;;
    -h|--help)
      show_help
      ;;
    *)
      echo -e "${RED}Error:${NC} Unknown argument: $1" >&2
      show_help
      ;;
  esac
done

# --- Check for Node.js and npm/yarn/pnpm ---
if ! command -v node &> /dev/null; then
    echo -e "${RED}Error:${NC} Node.js is not installed. Please install Node.js to run ESLint and Prettier."
    exit 1
fi

PACKAGE_MANAGER=""
if command -v pnpm &> /dev/null; then
    PACKAGE_MANAGER="pnpm"
elif command -v yarn &> /dev/null; then
    PACKAGE_MANAGER="yarn"
elif command -v npm &> /dev/null; then
    PACKAGE_MANAGER="npm"
else
    echo -e "${RED}Error:${NC} No package manager (npm, yarn, or pnpm) found. Please install one."
    exit 1
fi

# --- Run Prettier ---
PRETTIER_CMD="${PACKAGE_MANAGER} prettier ${TARGET_PATH} --write"
if [ "$FIX_MODE" = false ]; then
  PRETTIER_CMD="${PACKAGE_MANAGER} prettier ${TARGET_PATH} --check"
  echo -e "${BLUE}Running Prettier (check mode):${NC}"
else
  echo -e "${BLUE}Running Prettier (fix mode):${NC}"
fi

if ! ${PRETTIER_CMD}; then
  echo -e "${RED}Prettier issues found or command failed!${NC}" >&2
  if [ "$FIX_MODE" = false ]; then
    echo -e "${YELLOW}Run with --fix to attempt to resolve formatting issues.${NC}"
  fi
  PRETTIER_EXIT_CODE=1
else
  echo -e "${GREEN}Prettier check passed.${NC}"
  PRETTIER_EXIT_CODE=0
fi

# --- Run ESLint ---
ESLINT_CMD="${PACKAGE_MANAGER} eslint ${TARGET_PATH} --ext .ts,.tsx,.js,.jsx"
if [ "$FIX_MODE" = true ]; then
  ESLINT_CMD="${ESLINT_CMD} --fix"
  echo -e "${BLUE}Running ESLint (fix mode):${NC}"
else
  echo -e "${BLUE}Running ESLint (check mode):${NC}"
fi

if ! ${ESLINT_CMD}; then
  echo -e "${RED}ESLint issues found or command failed!${NC}" >&2
  if [ "$FIX_MODE" = false ]; then
    echo -e "${YELLOW}Run with --fix to attempt to resolve linting issues.${NC}"
  fi
  ESLINT_EXIT_CODE=1
else
  echo -e "${GREEN}ESLint check passed.${NC}"
  ESLINT_EXIT_CODE=0
fi

# --- Final Summary ---
echo -e "\n${BLUE}--- Linting and Formatting Summary ---${NC}"
if [ "$PRETTIER_EXIT_CODE" -eq 0 ] && [ "$ESLINT_EXIT_CODE" -eq 0 ]; then
  echo -e "${GREEN}All linting and formatting checks passed successfully!${NC}"
  exit 0
else
  echo -e "${RED}Some linting or formatting issues were found. Please review the output above.${NC}"
  exit 1
fi
