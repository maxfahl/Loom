#!/bin/bash

# run-visual-regression-tests.sh
#
# Purpose:
#   Executes Playwright tests that are specifically designed for visual regression testing.
#   This script can either run tests to compare against existing baselines or update
#   baselines if a legitimate UI change has occurred.
#
# Usage:
#   ./run-visual-regression-tests.sh [--update-baselines] [test_file_pattern]
#
# Arguments:
#   --update-baselines: Optional. If present, Playwright will update the visual
#                       baselines instead of comparing against them. Use this when
#                       UI changes are intentional and approved.
#   [test_file_pattern]: Optional. A glob pattern to filter which test files to run.
#                        Defaults to all tests if not provided. Useful for running
#                        visual tests for a specific component or page.
#
# Examples:
#   ./run-visual-regression-tests.sh
#   ./run-visual-regression-tests.sh --update-baselines
#   ./run-visual-regression-tests.sh components/Button.spec.ts
#   ./run-visual-regression-tests.sh --update-baselines "pages/**/*.spec.ts"
#
# Features:
#   - Runs Playwright tests with visual comparison assertions.
#   - Supports updating baselines with a flag.
#   - Allows filtering tests by file pattern.
#   - Provides clear console output with color.
#
# Prerequisites:
#   - Playwright must be installed and configured in the project.
#   - Visual regression tests (e.g., using `expect(page).toHaveScreenshot()`) must exist.

set -euo pipefail

# --- Configuration ---
PLAYWRIGHT_COMMAND="npx playwright test"
VISUAL_TEST_TAG="@visual" # Assuming visual tests are tagged with @visual

# --- Helper Functions ---

# Function to display script usage
usage() {
  echo "Usage: $0 [--update-baselines] [test_file_pattern]"
  echo ""
  echo "Arguments:"
  echo "  --update-baselines: Optional. If present, Playwright will update the visual"
  echo "                      baselines instead of comparing against them."
  echo "  [test_file_pattern]: Optional. A glob pattern to filter which test files to run."
  echo "                       Defaults to all tests if not provided."
  echo ""
  echo "Examples:"
  echo "  $0"
  echo "  $0 --update-baselines"
  echo "  $0 components/Button.spec.ts"
  echo "  $0 --update-baselines \"pages/**/*.spec.ts\""
  exit 1
}

# Function to print messages in color
print_color() {
  local color="$1"
  local message="$2"
  case "$color" in
    "red")    echo -e "\033[0;31m${message}\033[0m" ;;
    "green")  echo -e "\033[0;32m${message}\033[0m" ;;
    "yellow") echo -e "\033[0;33m${message}\033[0m" ;;
    "blue")   echo -e "\033[0;34m${message}\033[0m" ;;
    *)        echo "${message}" ;;
  esac
}

# --- Main Script Logic ---

UPDATE_BASELINES=false
TEST_FILE_PATTERN=""

# Parse arguments
for arg in "$@"
do
  case "$arg" in
    --update-baselines)
      UPDATE_BASELINES=true
      shift
      ;;
    -*)
      print_color "red" "Unknown option: $arg"
      usage
      ;;
    *)
      TEST_FILE_PATTERN="$arg"
      shift
      ;;
  esac
done

PLAYWRIGHT_ARGS=""
if [[ -n "${TEST_FILE_PATTERN}" ]]; then
  PLAYWRIGHT_ARGS="${TEST_FILE_PATTERN}"
fi

if "${UPDATE_BASELINES}"; then
  print_color "yellow" "Running Playwright visual regression tests to UPDATE baselines..."
  PLAYWRIGHT_FULL_COMMAND="${PLAYWRIGHT_COMMAND} --update-snapshots ${PLAYWRIGHT_ARGS}"
else
  print_color "blue" "Running Playwright visual regression tests to COMPARE against baselines..."
  PLAYWRIGHT_FULL_COMMAND="${PLAYWRIGHT_COMMAND} ${PLAYWRIGHT_ARGS}"
fi

print_color "blue" "Executing: ${PLAYWRIGHT_FULL_COMMAND}"

# Execute Playwright command
if ${PLAYWRIGHT_FULL_COMMAND}; then
  print_color "green" "\nPlaywright visual regression tests completed successfully!"
else
  print_color "red" "\nError: Playwright visual regression tests failed. Review the report for details."
  exit 1
fi

print_color "blue" "To view the Playwright HTML report, run: npx playwright show-report"
