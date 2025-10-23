#!/bin/bash

# perf-budget-check.sh: Performance Budget Checker
#
# This script runs a Lighthouse CI audit against a specified URL and enforces
# predefined performance budgets. It's designed to be used in CI/CD pipelines
# to prevent performance regressions.
#
# Dependencies:
#   - Node.js and npm/yarn
#   - Lighthouse CI: `npm install -g @lhci/cli` or `yarn global add @lhci/cli`
#
# Configuration:
#   This script expects a `.lighthouserc.json` file in the project root or
#   specified by --config. A basic example:
#   ```json
#   {
#     "ci": {
#       "collect": {
#         "url": ["http://localhost:3000"]
#       },
#       "assert": {
#         "assertions": {
#           "performance-score": ["error", {"minScore": 0.90}],
#           "accessibility-score": ["error", {"minScore": 0.95}],
#           "first-contentful-paint": ["error", {"maxNumericValue": 2000}],
#           "total-blocking-time": ["error", {"maxNumericValue": 300}]
#         }
#       }
#     }
#   }
#   ```
#
# Usage:
#   ./perf-budget-check.sh --url <URL> [--config <PATH_TO_LIGHTHOUSERC_JSON>]
#
# Examples:
#   # Run audit on a staging URL with default config
#   ./perf-budget-check.sh --url https://staging.example.com
#
#   # Run audit on a local development server with a custom config file
#   ./perf-budget-check.sh --url http://localhost:3000 --config ./lighthouserc.ci.json
#
#   # Run audit and only collect, without asserting (useful for debugging)
#   ./perf-budget-check.sh --url http://localhost:3000 --no-assert

set -euo pipefail

URL=""
CONFIG_FILE=".lighthouserc.json"
NO_ASSERT="false"

# Function to display help message
help_message() {
  echo "Usage: $0 --url <URL> [--config <PATH>] [--no-assert]"
  echo ""
  echo "Arguments:"
  echo "  --url <URL>             The URL to audit (e.g., https://example.com)."
  echo "  --config <PATH>         Optional: Path to a custom .lighthouserc.json file. Defaults to .lighthouserc.json in current directory."
  echo "  --no-assert             Optional: Run Lighthouse CI in collect mode only, skipping assertions."
  echo "  --help                  Display this help message."
  echo ""
  echo "This script requires Lighthouse CI to be installed globally or locally."
  echo "Install with: npm install -g @lhci/cli"
  exit 1
}

# Parse command-line arguments
while [[ $# -gt 0 ]]; do
  key="$1"
  case $key in
    --url)
      URL="$2"
      shift # past argument
      shift # past value
      ;;
    --config)
      CONFIG_FILE="$2"
      shift # past argument
      shift # past value
      ;;
    --no-assert)
      NO_ASSERT="true"
      shift # past argument
      ;;
    --help)
      help_message
      ;;
    *)
      echo "Unknown option: $1"
      help_message
      ;;
  esac
done

# Validate URL
if [[ -z "$URL" ]]; then
  echo "Error: --url is required." >&2
  help_message
fi

# Check if Lighthouse CI is installed
if ! command -v lhci &> /dev/null;
then
    echo "Error: Lighthouse CI (lhci) is not installed or not in PATH." >&2
    echo "Please install it globally: npm install -g @lhci/cli" >&2
    exit 1
fi

# Check if config file exists
if [[ ! -f "$CONFIG_FILE" ]]; then
  echo "Error: Lighthouse CI config file not found at \"$CONFIG_FILE\"." >&2
  echo "Please create one or specify a different path with --config." >&2
  exit 1
fi

echo "Running Lighthouse CI audit for: $URL"
echo "Using config file: $CONFIG_FILE"

# Run Lighthouse CI
if [[ "$NO_ASSERT" == "true" ]]; then
  echo "Running in collect-only mode (assertions skipped)."
  lhci collect --url "$URL" --config="$CONFIG_FILE"
else
  lhci collect --url "$URL" --config="$CONFIG_FILE" && lhci assert --config="$CONFIG_FILE"
fi

# Capture exit code of lhci command
LHCI_EXIT_CODE=$?

if [[ $LHCI_EXIT_CODE -ne 0 ]]; then
  echo "\nLighthouse CI audit failed due to budget violations or other errors." >&2
  exit $LHCI_EXIT_CODE
else
  echo "\nLighthouse CI audit passed. All performance budgets met!"
  exit 0
fi
