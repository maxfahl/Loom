#!/bin/bash

# publish-pact-contract.sh
#
# Publishes a generated consumer contract to a Pact Broker.
# This script is typically run in the consumer's CI/CD pipeline after successful
# consumer-side contract test execution.
#
# Usage:
#   ./publish-pact-contract.sh --consumer-name FrontendApp --provider-name UserService --consumer-version 1.0.0 --contract-file ./pact/interactions/frontendapp-userservice.json
#   ./publish-pact-contract.sh -c MyConsumer -p MyProvider -v 2.1.0 -f ./pact/myconsumer-myprovider.json -b https://broker.example.com -t YOUR_BROKER_TOKEN
#
# Requirements:
#   - Node.js and npm/yarn installed.
#   - `@pact-foundation/pact` installed as a dev dependency in your project.
#   - PACT_BROKER_URL and PACT_BROKER_TOKEN (or equivalent) environment variables
#     should be set or passed as arguments if publishing to a broker.
#
# Options:
#   -c, --consumer-name <name>     : The name of the consumer application (e.g., 'FrontendApp'). (Required)
#   -p, --provider-name <name>     : The name of the provider service (e.g., 'UserService'). (Required)
#   -v, --consumer-version <version>: The version of the consumer application (e.g., '1.0.0'). (Required)
#   -f, --contract-file <file>     : Path to the generated Pact contract JSON file. (Required)
#   -b, --pact-broker-url <url>    : The URL of the Pact Broker.
#   -t, --pact-broker-token <token>: Bearer token for authenticating with the Pact Broker.
#   -h, --help                     : Display this help message.

# --- Configuration ---
# Path to the Pact Publisher script (usually in node_modules/.bin)
PACT_PUBLISHER_BIN="$(npm bin)/pact-broker publish"

# --- Functions ---
function display_help() {
  echo "Usage: $(basename "$0") [OPTIONS]"
  echo ""
  echo "Publishes a generated consumer contract to a Pact Broker."
  echo ""
  echo "Options:"
  echo "  -c, --consumer-name <name>      The name of the consumer application. (Required)"
  echo "  -p, --provider-name <name>      The name of the provider service. (Required)"
  echo "  -v, --consumer-version <version> The version of the consumer application. (Required)"
  echo "  -f, --contract-file <file>      Path to the generated Pact contract JSON file. (Required)"
  echo "  -b, --pact-broker-url <url>     The URL of the Pact Broker."
  echo "  -t, --pact-broker-token <token> Bearer token for authenticating with the Pact Broker."
  echo "  -h, --help                      Display this help message."
  echo ""
  echo "Example:"
  echo "  $(basename "$0") -c FrontendApp -p UserService -v 1.0.0 -f ./pact/interactions/frontendapp-userservice.json -b https://broker.example.com -t YOUR_TOKEN"
  exit 0
}

function error_exit() {
  echo -e "\033[0;31mError: $1\033[0m" >&2
  exit 1
}

# --- Main Script ---

CONSUMER_NAME=""
PROVIDER_NAME=""
CONSUMER_VERSION=""
CONTRACT_FILE=""
PACT_BROKER_URL=""
PACT_BROKER_TOKEN=""

# Parse command-line arguments
while (( "$#" )); do
  case "$1" in
    -c|--consumer-name)
      if [ -n "$2" ] && [ "${2:0:1}" != "-" ]; then
        CONSUMER_NAME="$2"
        shift 2
      else
        error_exit "Argument for $1 is missing or invalid."
      fi
      ;;
    -p|--provider-name)
      if [ -n "$2" ] && [ "${2:0:1}" != "-" ]; then
        PROVIDER_NAME="$2"
        shift 2
      else
        error_exit "Argument for $1 is missing or invalid."
      fi
      ;;
    -v|--consumer-version)
      if [ -n "$2" ] && [ "${2:0:1}" != "-" ]; then
        CONSUMER_VERSION="$2"
        shift 2
      else
        error_exit "Argument for $1 is missing or invalid."
      fi
      ;;
    -f|--contract-file)
      if [ -n "$2" ] && [ "${2:0:1}" != "-" ]; then
        CONTRACT_FILE="$2"
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
if [ -z "$CONSUMER_NAME" ]; then
  error_exit "Consumer name (--consumer-name) is required."
fi

if [ -z "$PROVIDER_NAME" ]; then
  error_exit "Provider name (--provider-name) is required."
fi

if [ -z "$CONSUMER_VERSION" ]; then
  error_exit "Consumer version (--consumer-version) is required."
fi

if [ -z "$CONTRACT_FILE" ]; then
  error_exit "Contract file path (--contract-file) is required."
fi

if [ ! -f "$CONTRACT_FILE" ]; then
  error_exit "Contract file not found: $CONTRACT_FILE"
fi

if [ -z "$PACT_BROKER_URL" ]; then
  error_exit "Pact Broker URL (--pact-broker-url) is required to publish contracts."
fi

# Check if pact-broker is available
if ! command -v "$PACT_PUBLISHER_BIN" &> /dev/null; then
  error_exit "'pact-broker' command not found. Please ensure @pact-foundation/pact is installed and in your PATH."
fi

PUBLISH_COMMAND=("$PACT_PUBLISHER_BIN")
PUBLISH_COMMAND+=("$CONTRACT_FILE")
PUBLISH_COMMAND+=("--consumer-app-version" "$CONSUMER_VERSION")
PUBLISH_COMMAND+=("--broker-base-url" "$PACT_BROKER_URL")

if [ -n "$PACT_BROKER_TOKEN" ]; then
  PUBLISH_COMMAND+=("--broker-token" "$PACT_BROKER_TOKEN")
fi

echo "Publishing Pact contract to broker..."
echo "Command: ${PUBLISH_COMMAND[*]}"

# Execute the publish command
"${PUBLISH_COMMAND[@]}" || error_exit "Failed to publish Pact contract."

echo -e "\033[0;32mPact contract published successfully!\033[0m"
