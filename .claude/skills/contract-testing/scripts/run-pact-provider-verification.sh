#!/bin/bash

# run-pact-provider-verification.sh
#
# Executes the Pact provider verification process against a running provider service.
# This script fetches contracts from a Pact Broker (or uses local files) and runs
# them against the actual provider implementation to ensure compatibility.
#
# Usage:
#   ./run-pact-provider-verification.sh --provider-name UserService --provider-base-url http://localhost:3000
#   ./run-pact-provider-verification.sh -p ProductService -u http://localhost:8080 -b https://broker.example.com -t YOUR_BROKER_TOKEN -v 1.0.0 --publish
#
# Requirements:
#   - Node.js and npm/yarn installed.
#   - `@pact-foundation/pact` installed as a dev dependency in your project.
#   - Your provider service must be running and accessible at the specified URL.
#   - If using a Pact Broker, PACT_BROKER_URL and PACT_BROKER_TOKEN (or equivalent)
#     environment variables should be set or passed as arguments.
#
# Options:
#   -p, --provider-name <name>     : The name of the provider service (e.g., 'UserService'). (Required)
#   -u, --provider-base-url <url>  : The base URL of the running provider service (e.g., 'http://localhost:3000'). (Required)
#   -b, --pact-broker-url <url>    : The URL of the Pact Broker. If not provided, local pact files must be specified.
#   -t, --pact-broker-token <token>: Bearer token for authenticating with the Pact Broker.
#   -v, --provider-version <version>: The version of the provider being verified (e.g., '1.0.0').
#   --publish                      : Flag to publish verification results to the Pact Broker.
#   --local-pact-file <file>       : Path to a local pact file to verify (can be used multiple times).
#   -h, --help                     : Display this help message.

# --- Configuration ---
# Path to the Pact Verifier script (usually in node_modules/.bin)
PACT_VERIFIER_BIN="$(npm bin)/pact-verifier"

# --- Functions ---
function display_help() {
  echo "Usage: $(basename "$0") [OPTIONS]"
  echo ""
  echo "Executes the Pact provider verification process."
  echo ""
  echo "Options:"
  echo "  -p, --provider-name <name>      The name of the provider service (e.g., 'UserService'). (Required)"
  echo "  -u, --provider-base-url <url>   The base URL of the running provider service. (Required)"
  echo "  -b, --pact-broker-url <url>     The URL of the Pact Broker."
  echo "  -t, --pact-broker-token <token> Bearer token for authenticating with the Pact Broker."
  echo "  -v, --provider-version <version> The version of the provider being verified (e.g., '1.0.0')."
  echo "  --publish                       Flag to publish verification results to the Pact Broker."
  echo "  --local-pact-file <file>        Path to a local pact file to verify (can be used multiple times)."
  echo "  -h, --help                      Display this help message."
  echo ""
  echo "Example:"
  echo "  $(basename "$0") -p UserService -u http://localhost:3000 -b https://broker.example.com -t YOUR_TOKEN -v 1.0.0 --publish"
  exit 0
}

function error_exit() {
  echo -e "\033[0;31mError: $1\033[0m" >&2
  exit 1
}

# --- Main Script ---

PROVIDER_NAME=""
PROVIDER_BASE_URL=""
PACT_BROKER_URL=""
PACT_BROKER_TOKEN=""
PROVIDER_VERSION=""
PUBLISH_RESULTS="false"
LOCAL_PACT_FILES=()

# Parse command-line arguments
while (( "$#" )); do
  case "$1" in
    -p|--provider-name)
      if [ -n "$2" ] && [ "${2:0:1}" != "-" ]; then
        PROVIDER_NAME="$2"
        shift 2
      else
        error_exit "Argument for $1 is missing or invalid."
      fi
      ;;
    -u|--provider-base-url)
      if [ -n "$2" ] && [ "${2:0:1}" != "-" ]; then
        PROVIDER_BASE_URL="$2"
        shift 2
      else
        error_exit "Argument for $1 is missing or invalid."
      fi
      ;;
    -b|--pact-broker-url)
      if [ -n "$2" ] && [ "${2:0:1}" != "-" ]; then
        PACT_BROKER_URL="$2"
        shift 2
      else
        error_exit "Argument for $1 is missing or invalid."
      fi
      ;;
    -t|--pact-broker-token)
      if [ -n "$2" ] && [ "${2:0:1}" != "-" ]; then
        PACT_BROKER_TOKEN="$2"
        shift 2
      else
        error_exit "Argument for $1 is missing or invalid."
      fi
      ;;
    -v|--provider-version)
      if [ -n "$2" ] && [ "${2:0:1}" != "-" ]; then
        PROVIDER_VERSION="$2"
        shift 2
      else
        error_exit "Argument for $1 is missing or invalid."
      fi
      ;;
    --publish)
      PUBLISH_RESULTS="true"
      shift
      ;;
    --local-pact-file)
      if [ -n "$2" ] && [ "${2:0:1}" != "-" ]; then
        LOCAL_PACT_FILES+=("$2")
        shift 2
      else
        error_exit "Argument for $1 is missing or invalid."
      fi
      ;;
    -h|--help)
      display_help
      ;;
    -*|--*=)
      error_exit "Unsupported option $1"
      ;;
    *)
      break
      ;;
  esac
done

# Validate required arguments
if [ -z "$PROVIDER_NAME" ]; then
  error_exit "Provider name (--provider-name) is required."
fi

if [ -z "$PROVIDER_BASE_URL" ]; then
  error_exit "Provider base URL (--provider-base-url) is required."
fi

# Check if pact-verifier is available
if ! command -v "$PACT_VERIFIER_BIN" &> /dev/null; then
  error_exit "'pact-verifier' command not found. Please ensure @pact-foundation/pact is installed and in your PATH."
fi

VERIFIER_COMMAND=("$PACT_VERIFIER_BIN")
VERIFIER_COMMAND+=("--provider" "$PROVIDER_NAME")
VERIFIER_COMMAND+=("--provider-base-url" "$PROVIDER_BASE_URL")
VERIFIER_COMMAND+=("--verbose")

if [ -n "$PACT_BROKER_URL" ]; then
  VERIFIER_COMMAND+=("--pact-broker-url" "$PACT_BROKER_URL")
  if [ -n "$PACT_BROKER_TOKEN" ]; then
    VERIFIER_COMMAND+=("--pact-broker-token" "$PACT_BROKER_TOKEN")
  fi
  if [ -n "$PROVIDER_VERSION" ]; then
    VERIFIER_COMMAND+=("--provider-app-version" "$PROVIDER_VERSION")
  fi
  if [ "$PUBLISH_RESULTS" == "true" ]; then
    VERIFIER_COMMAND+=("--publish-verification-results")
  fi
  # Example: Fetch pacts with specific tags or from specific consumers
  # VERIFIER_COMMAND+=("--consumer-version-selectors= \"{\"tag\": \"master\", \"latest\": true}\" ")
  # VERIFIER_COMMAND+=("--consumer-version-selectors= \"{\"branch\": \"main\", \"latest\": true}\" ")
else
  if [ ${#LOCAL_PACT_FILES[@]} -eq 0 ]; then
    error_exit "No Pact Broker URL provided and no local pact files specified. Cannot perform verification."
  fi
  for file in "${LOCAL_PACT_FILES[@]}"; do
    if [ ! -f "$file" ]; then
      error_exit "Local pact file not found: $file"
    fi
    VERIFIER_COMMAND+=("--pact-urls" "$file")
  done
fi

echo "Running Pact provider verification..."
echo "Command: ${VERIFIER_COMMAND[*]}"

# Execute the verifier command
"${VERIFIER_COMMAND[@]}" || error_exit "Pact provider verification failed!"

echo -e "\033[0;32mPact provider verification successful!\033[0m"
