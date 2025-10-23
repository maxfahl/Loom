#!/bin/bash

# update-api-gateway-routes.sh
#
# Purpose:
#   Automates the update of API Gateway routing configurations (e.g., Nginx).
#   It helps to manage the lifecycle of API versions by adding new routes or
#   marking old ones for deprecation/removal in the gateway configuration.
#
# Usage:
#   ./update-api-gateway-routes.sh --gateway <nginx> --config <path_to_config> --action <add|deprecate|remove> --version <vX> --target <target_path> [--upstream <upstream_server>]
#
# Examples:
#   ./update-api-gateway-routes.sh --gateway nginx --config /etc/nginx/conf.d/api.conf --action add --version v2 --target /api/v2 --upstream http://localhost:3002
#   ./update-api-api-gateway-routes.sh --gateway nginx --config /etc/nginx/conf.d/api.conf --action deprecate --version v1 --target /api/v1
#   ./update-api-gateway-routes.sh --gateway nginx --config /etc/nginx/conf.d/api.conf --action remove --version v1 --target /api/v1
#
# Configuration:
#   - Currently supports Nginx configuration files as an example.
#   - For other gateways (Kong, AWS API Gateway), this script would serve as a wrapper
#     to their respective CLI tools or APIs (not implemented in this example).
#
# Error Handling:
#   - Exits if required arguments are missing or invalid.
#   - Exits if the configuration file is not found or cannot be written to.
#   - Provides clear messages for actions taken.

set -euo pipefail

# --- Configuration ---
GATEWAY_TYPE=""
CONFIG_FILE=""
ACTION=""
VERSION=""
TARGET_PATH=""
UPSTREAM_SERVER=""

# --- Functions ---

# Displays help message
show_help() {
  echo "Usage: $0 --gateway <nginx> --config <path> --action <add|deprecate|remove> --version <vX> --target <target_path> [--upstream <upstream_server>]"
  echo ""
  echo "Purpose: Automates the update of API Gateway routing configurations."
  echo ""
  echo "Options:"
  echo "  --gateway         API Gateway type (e.g., 'nginx')."
  echo "  --config          Path to the gateway configuration file."
  echo "  --action          Action to perform: 'add', 'deprecate', or 'remove'."
  echo "  --version         API version (e.g., 'v1', 'v2')."
  echo "  --target          The base path for the API version (e.g., '/api/v2')."
  echo "  --upstream        Required for 'add' action: The upstream server URL (e.g., 'http://localhost:3002')."
  echo "  -h, --help        Display this help message."
  echo ""
  echo "Examples:"
  echo "  $0 --gateway nginx --config /etc/nginx/conf.d/api.conf --action add --version v2 --target /api/v2 --upstream http://localhost:3002"
  echo "  $0 --gateway nginx --config /etc/nginx/conf.d/api.conf --action deprecate --version v1 --target /api/v1"
  exit 0
}

# Parses command-line arguments
parse_args() {
  while [[ "$#" -gt 0 ]]; do
    case "$1" in
      --gateway) GATEWAY_TYPE="$2"; shift ;;
      --config) CONFIG_FILE="$2"; shift ;;
      --action) ACTION="$2"; shift ;;
      --version) VERSION="$2"; shift ;;
      --target) TARGET_PATH="$2"; shift ;;
      --upstream) UPSTREAM_SERVER="$2"; shift ;;
      -h|--help) show_help ;;
      *) echo "Unknown parameter: $1"; show_help ;;
    esac
    shift
  done
}

# Validates arguments
validate_args() {
  if [[ -z "$GATEWAY_TYPE" || -z "$CONFIG_FILE" || -z "$ACTION" || -z "$VERSION" || -z "$TARGET_PATH" ]]; then
    echo "Error: Missing required arguments." >&2
    show_help
  fi

  if [[ "$GATEWAY_TYPE" != "nginx" ]]; then
    echo "Error: Unsupported gateway type: $GATEWAY_TYPE. Currently only 'nginx' is supported as an example." >&2
    exit 1
  fi

  if [[ ! -f "$CONFIG_FILE" ]]; then
    echo "Error: Configuration file not found: $CONFIG_FILE" >&2
    exit 1
  fi

  if [[ "$ACTION" == "add" && -z "$UPSTREAM_SERVER" ]]; then
    echo "Error: --upstream is required for 'add' action." >&2
    show_help
  fi

  if [[ "$ACTION" != "add" && "$ACTION" != "deprecate" && "$ACTION" != "remove" ]]; then
    echo "Error: Invalid action. Must be 'add', 'deprecate', or 'remove'." >&2
    exit 1
  fi
}

# Adds a new Nginx location block
add_nginx_route() {
  local route_block=""
  route_block+="
    # API Version: ${VERSION} - Added by script on $(date)
"
  route_block+="    location ${TARGET_PATH}/ {
"
  route_block+="        proxy_pass ${UPSTREAM_SERVER}/;
"
  route_block+="        proxy_set_header Host $host;
"
  route_block+="        proxy_set_header X-Real-IP $remote_addr;
"
  route_block+="        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
"
  route_block+="        proxy_set_header X-Forwarded-Proto $scheme;
"
  route_block+="    }
"

  if grep -q "location ${TARGET_PATH}/" "$CONFIG_FILE"; then
    echo "Warning: Route for ${TARGET_PATH} already exists in ${CONFIG_FILE}. Skipping add action." >&2
  else
    # Find a good place to insert, e.g., before the last '}' of an http or server block
    # This is a simplistic approach; for complex configs, manual review is best.
    if sed -i "/server {/a ${route_block}" "$CONFIG_FILE"; then
      echo "Successfully added route for ${TARGET_PATH} to ${CONFIG_FILE}"
    else
      echo "Error: Failed to add route to ${CONFIG_FILE}. Manual intervention may be required." >&2
      exit 1
    fi
  fi
}

# Deprecates an Nginx location block (e.g., by adding a comment and a warning header)
deprecate_nginx_route() {
  local deprecation_comment="# DEPRECATED API Version: ${VERSION} - Deprecated by script on $(date)"
  local deprecation_header="add_header X-API-Deprecation-Info \"This API version (${VERSION}) is deprecated. Please migrate to a newer version.\";"

  # Check if the route exists
  if ! grep -q "location ${TARGET_PATH}/" "$CONFIG_FILE"; then
    echo "Warning: Route for ${TARGET_PATH} not found in ${CONFIG_FILE}. Cannot deprecate." >&2
    return 0
  fi

  # Add deprecation comment and header
  if sed -i "/location ${TARGET_PATH}\//i ${deprecation_comment}" "$CONFIG_FILE" && \
     sed -i "/location ${TARGET_PATH}\//a 	${deprecation_header}" "$CONFIG_FILE"; then
    echo "Successfully marked route for ${TARGET_PATH} as deprecated in ${CONFIG_FILE}"
  else
    echo "Error: Failed to deprecate route in ${CONFIG_FILE}. Manual intervention may be required." >&2
    exit 1
  fi
}

# Removes an Nginx location block
remove_nginx_route() {
  # This is a very aggressive removal. Use with caution.
  # It removes the location block and any preceding deprecation comments.
  if sed -i "/location ${TARGET_PATH}\//,/^\s*}/d" "$CONFIG_FILE" && \
     sed -i "/DEPRECATED API Version: ${VERSION}/d" "$CONFIG_FILE"; then
    echo "Successfully removed route for ${TARGET_PATH} from ${CONFIG_FILE}"
  else
    echo "Error: Failed to remove route from ${CONFIG_FILE}. Manual intervention may be required." >&2
    exit 1
  fi
}

# --- Main Logic ---
parse_args "$@"
validate_args

echo "Updating API Gateway routes..."
echo "Gateway Type: ${GATEWAY_TYPE}"
echo "Config File: ${CONFIG_FILE}"
echo "Action: ${ACTION}"
echo "Version: ${VERSION}"
echo "Target Path: ${TARGET_PATH}"

case "$GATEWAY_TYPE" in
  nginx)
    case "$ACTION" in
      add) add_nginx_route ;;
      deprecate) deprecate_nginx_route ;;
      remove) remove_nginx_route ;;
    esac
    echo "Remember to reload/restart your Nginx server for changes to take effect (e.g., sudo nginx -s reload)."
    ;;
  *)
    echo "Error: Unhandled gateway type or action for $GATEWAY_TYPE. This script is an example and may require customization for your specific gateway." >&2
    exit 1
    ;;
esac

echo "API Gateway route update complete."
