#!/bin/bash

# blue-green-traffic-switch.sh
#
# Purpose: Automates the traffic switch for a Kubernetes Blue-Green deployment
# by updating the service selector. This script ensures a quick, consistent,
# and auditable cutover between the blue and green environments.
#
# Usage:
#   ./blue-green-traffic-switch.sh --service <service-name> --version <new-version-label> [--namespace <namespace>] [--dry-run]
#
# Examples:
#   ./blue-green-traffic-switch.sh --service my-app-service --version v2
#   ./blue-green-traffic-switch.sh --service api-gateway --version green --namespace production --dry-run
#
# Requirements:
#   - kubectl installed and configured to access the Kubernetes cluster.
#   - Permissions to patch Kubernetes Services.

# --- Configuration ---
SERVICE_NAME=""
NEW_VERSION_LABEL=""
NAMESPACE="default"
DRY_RUN=false

# --- Functions ---

# Function to display script usage
usage() {
    echo "Usage: $0 --service <service-name> --version <new-version-label> [--namespace <namespace>] [--dry-run]"
    echo ""
    echo "  --service <service-name>      : (Required) The name of the Kubernetes Service to update."
    echo "  --version <new-version-label> : (Required) The new version label (e.g., 'v2', 'green') to set in the service selector."
    echo "  --namespace <namespace>       : (Optional) The Kubernetes namespace where the service is located. Defaults to 'default'."
    echo "  --dry-run                     : (Optional) If set, the script will only show what would be done without making actual changes."
    echo "  --help                        : Display this help message."
    exit 1
}

# Function to parse command-line arguments
parse_args() {
    while [[ "$#" -gt 0 ]]; do
        case "$1" in
            --service)
                SERVICE_NAME="$2"
                shift
                ;;
            --version)
                NEW_VERSION_LABEL="$2"
                shift
                ;;
            --namespace)
                NAMESPACE="$2"
                shift
                ;;
            --dry-run)
                DRY_RUN=true
                ;;
            --help)
                usage
                ;;
            *)
                echo "Error: Unknown parameter: $1"
                usage
                ;;
        esac
        shift
    done

    if [[ -z "$SERVICE_NAME" || -z "$NEW_VERSION_LABEL" ]]; then
        echo "Error: --service and --version are required parameters."
        usage
    fi
}

# --- Main Script Logic ---

parse_args "$@"

echo "--- Blue-Green Traffic Switch Script ---"
echo "Service Name:        $SERVICE_NAME"
echo "New Version Label:   $NEW_VERSION_LABEL"
echo "Namespace:           $NAMESPACE"
echo "Dry Run:             $DRY_RUN"
echo "----------------------------------------"

# Check if kubectl is installed
if ! command -v kubectl &> /dev/null; then
    echo "Error: kubectl is not installed or not in PATH. Please install it."
    exit 1
fi

# Construct the patch command
PATCH_COMMAND="kubectl patch service $SERVICE_NAME -n $NAMESPACE -p '{"spec":{"selector":{"version":"$NEW_VERSION_LABEL"}}}'"

if $DRY_RUN; then
    echo "Dry run enabled. The following command would be executed:"
    echo "$PATCH_COMMAND"
    echo "No changes were made."
    exit 0
fi

echo "Attempting to switch traffic for service '$SERVICE_NAME' in namespace '$NAMESPACE' to version '$NEW_VERSION_LABEL'..."
eval "$PATCH_COMMAND"

if [ $? -eq 0 ]; then
    echo "Success: Traffic for service '$SERVICE_NAME' successfully switched to version '$NEW_VERSION_LABEL'."
    echo "Verification: Run 'kubectl get service $SERVICE_NAME -n $NAMESPACE -o yaml' to confirm the selector change."
else
    echo "Error: Failed to switch traffic for service '$SERVICE_NAME'."
    echo "Please check kubectl configuration, service name, namespace, and permissions."
    exit 1
fi
