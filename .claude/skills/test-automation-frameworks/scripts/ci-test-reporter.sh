#!/bin/bash

# ci-test-reporter.sh
#
# Description:
#   This script processes test results (primarily Playwright's JSON reporter output)
#   and generates a concise summary report suitable for CI/CD pipelines.
#   It can extract total tests, passed, failed, skipped counts, and provide a quick overview
#   of test execution status.
#
# Usage:
#   ./ci-test-reporter.sh <path_to_json_report> [options]
#
# Arguments:
#   <path_to_json_report> : The path to the Playwright JSON test report file.
#
# Options:
#   -o, --output <file>   : Output the summary report to a file instead of stdout.
#   -h, --help            : Show this help message and exit.
#
# Examples:
#   ./ci-test-reporter.sh ./test-results/report.json
#   ./ci-test-reporter.sh ./playwright-report/results.json -o ci_summary.txt
#
# Dependencies:
#   - `jq` (command-line JSON processor) must be installed.
#
# Note:
#   This script is specifically tailored for Playwright's JSON report format.
#   For Selenium, you would typically use a different reporter (e.g., Allure) and a corresponding
#   script to process its output.

set -euo pipefail

# --- Functions ---

# Displays help message
show_help() {
  echo "Usage: $0 <path_to_json_report> [options]"
  echo ""
  echo "Arguments:"
  echo "  <path_to_json_report> : The path to the Playwright JSON test report file."
  echo ""
  echo "Options:"
  echo "  -o, --output <file>   : Output the summary report to a file instead of stdout."
  echo "  -h, --help            : Show this help message and exit."
  echo ""
  echo "Description:"
  echo "  Processes Playwright JSON test reports and generates a concise summary for CI/CD."
  echo ""
  echo "Dependencies:"
  echo "  - jq (command-line JSON processor)"
}

# --- Main Logic ---

# Check for help flag
if [[ "$#" -gt 0 && ("$1" == "-h" || "$1" == "--help") ]]; then
  show_help
  exit 0
fi

# Validate arguments
if [ "$#" -lt 1 ]; then
  echo "Error: Missing path to JSON report."
  show_help
  exit 1
fi

JSON_REPORT_PATH="$1"
OUTPUT_FILE=""

# Parse options
shift # past the report path
while [[ $# -gt 0 ]]; do
  key="$1"
  case $key in
    -o|--output)
      OUTPUT_FILE="$2"
      shift # past argument
      shift # past value
      ;;
    *)
      echo "Unknown option: $1"
      show_help
      exit 1
      ;;
  esac
done

# Check if jq is installed
if ! command -v jq &> /dev/null
then
    echo "Error: 'jq' is not installed. Please install it to use this script."
    echo "  On macOS: brew install jq"
    echo "  On Debian/Ubuntu: sudo apt-get install jq"
    echo "  On CentOS/RHEL: sudo yum install jq"
    exit 1
fi

# Check if report file exists
if [ ! -f "$JSON_REPORT_PATH" ]; then
  echo "Error: JSON report file not found at '$JSON_REPORT_PATH'."
  exit 1
fi

echo "Processing test report: ${JSON_REPORT_PATH}"

# Extract data using jq
TOTAL_TESTS=$(jq '.stats.tests' "$JSON_REPORT_PATH")
PASSED_TESTS=$(jq '.stats.passes' "$JSON_REPORT_PATH")
FAILED_TESTS=$(jq '.stats.failures' "$JSON_REPORT_PATH")
SKIPPED_TESTS=$(jq '.stats.skipped' "$JSON_REPORT_PATH")
DURATION=$(jq '.stats.duration' "$JSON_REPORT_PATH") # Duration in milliseconds

# Convert duration to seconds
DURATION_SECONDS=$(echo "scale=2; $DURATION / 1000" | bc)

# Determine overall status
STATUS="SUCCESS"
if [ "$FAILED_TESTS" -gt 0 ]; then
  STATUS="FAILURE"
fi

# Generate summary report
REPORT_SUMMARY=""
REPORT_SUMMARY+="--- E2E Test Summary ---\n"
REPORT_SUMMARY+="Overall Status: ${STATUS}\n"
REPORT_SUMMARY+="Total Tests: ${TOTAL_TESTS}\n"
REPORT_SUMMARY+="Passed: ${PASSED_TESTS}\n"
REPORT_SUMMARY+="Failed: ${FAILED_TESTS}\n"
REPORT_SUMMARY+="Skipped: ${SKIPPED_TESTS}\n"
REPORT_SUMMARY+="Duration: ${DURATION_SECONDS} seconds\n"
REPORT_SUMMARY+="-----------------------\n"

if [ "$FAILED_TESTS" -gt 0 ]; then
  REPORT_SUMMARY+="\nFailed Tests Details:\n"
  # Extract details of failed tests
  FAILED_DETAILS=$(jq -r '.suites[] | .tests[] | select(.status == "failed") | "  - \(.fullTitle) (Error: \(.errors[0].message | split("\\n") | .[0]))"' "$JSON_REPORT_PATH")
  REPORT_SUMMARY+="${FAILED_DETAILS}\n"
fi

# Output the report
if [ -n "$OUTPUT_FILE" ]; then
  echo -e "${REPORT_SUMMARY}" > "$OUTPUT_FILE"
  echo "Summary report saved to '$OUTPUT_FILE'"
else
  echo -e "${REPORT_SUMMARY}"
fi

# Exit with non-zero status if tests failed
if [ "$FAILED_TESTS" -gt 0 ]; then
  exit 1
fi
