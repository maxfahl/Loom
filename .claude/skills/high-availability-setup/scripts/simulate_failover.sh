#!/bin/bash

# Failover Simulation Script
#
# This script simulates a service failure by stopping a specified systemd service
# on a Linux system. It can be used to test automated failover mechanisms and
# ensure that monitoring and recovery systems react as expected.
#
# Usage:
#   ./simulate_failover.sh --service my-web-app --action stop
#   ./simulate_failover.sh --service my-web-app --action restart
#   ./simulate_failover.sh -h # For help
#
# Requirements:
#   - systemd (Linux init system)
#   - Root privileges (for stopping/starting systemd services)
#
# Features:
# - Stops, starts, or restarts a specified systemd service.
# - Asks for user confirmation before performing actions.
# - Provides clear feedback on success or failure.
#
# Note: For Windows systems, you would typically use 'sc stop <service_name>'
#       and 'sc start <service_name>' in a PowerShell or Command Prompt script.

set -e

# --- Functions ---

print_help() {
  echo "Usage: $(basename "$0") [OPTIONS]"
  echo "Simulate a service failure to test HA failover mechanisms."
  echo ""
  echo "Options:"
  echo "  -s, --service <NAME>   Name of the systemd service to control (e.g., nginx, postgresql)."
  echo "  -a, --action <ACTION>  Action to perform: 'stop', 'start', or 'restart'."
  echo "  -y, --yes              Skip confirmation prompt and proceed with the action."
  echo "  -h, --help             Display this help message."
  echo ""
  echo "Examples:"
  echo "  $(basename "$0") --service my-api --action stop"
  echo "  $(basename "$0") --service my-db --action restart --yes"
  echo ""
  echo "Note: This script requires root privileges to control systemd services."
}

confirm_action() {
  local service_name="$1"
  local action="$2"
  local skip_confirm="$3"

  if [[ "$skip_confirm" == "true" ]]; then
    return 0 # Skip confirmation
  fi

  read -r -p "Are you sure you want to ${action} the service '${service_name}'? (y/N) " response
  case "$response" in
    [yY][eE][sS]|[yY])
      return 0
      ;;
    *)
      echo "Action cancelled."
      exit 0
      ;;
  esac
}

control_service() {
  local service_name="$1"
  local action="$2"

  if [[ $(id -u) -ne 0 ]]; then
    echo "Error: This script requires root privileges. Please run with sudo." >&2
    exit 1
  fi

  if ! systemctl is-active --quiet "$service_name"; then
    if [[ "$action" == "stop" ]]; then
      echo "Service '$service_name' is not running. No need to stop."
      exit 0
    fi
  fi

  echo "Attempting to ${action} service '$service_name'..."
  if sudo systemctl "$action" "$service_name"; then
    echo "✅ Successfully ${action}ed service '$service_name'."
  else
    echo "❌ Failed to ${action} service '$service_name'." >&2
    exit 1
  fi

  # Give it a moment and check status
  sleep 2
  if systemctl is-active --quiet "$service_name"; then
    echo "Service '$service_name' is now active."
  else
    echo "Service '$service_name' is not active (as expected for 'stop' action, or unexpected for 'start'/ 'restart')."
  fi
}

# --- Main Logic ---

SERVICE_NAME=""
ACTION=""
SKIP_CONFIRM="false"

while [[ "$#" -gt 0 ]]; do
  key="$1"
  case $key in
    -s|--service)
      SERVICE_NAME="$2"
      shift # past argument
      shift # past value
      ;;
    -a|--action)
      ACTION="$2"
      shift # past argument
      shift # past value
      ;;
    -y|--yes)
      SKIP_CONFIRM="true"
      shift # past argument
      ;;
    -h|--help)
      print_help
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      print_help
      exit 1
      ;;
  esac
done

if [[ -z "$SERVICE_NAME" || -z "$ACTION" ]]; then
  echo "Error: --service and --action are required." >&2
  print_help
  exit 1
fi

if [[ "$ACTION" != "stop" && "$ACTION" != "start" && "$ACTION" != "restart" ]]; then
  echo "Error: Invalid action '$ACTION'. Must be 'stop', 'start', or 'restart'." >&2
  print_help
  exit 1
fi

confirm_action "$SERVICE_NAME" "$ACTION" "$SKIP_CONFIRM"
control_service "$SERVICE_NAME" "$ACTION"
