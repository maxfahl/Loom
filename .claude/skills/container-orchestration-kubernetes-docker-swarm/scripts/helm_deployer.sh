
#!/bin/bash

# helm_deployer.sh
# Description: Automates the deployment or upgrade of Helm charts to a Kubernetes cluster.
#              Supports custom values files, dry-run, and namespace specification.

# --- Configuration Variables (can be overridden by environment variables or arguments) ---
HELM_BIN=${HELM_BIN:-"helm"}

# --- Helper Functions ---
print_help() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Automates the deployment or upgrade of Helm charts."
    echo ""
    echo "Options:"
    echo "  -c, --chart <CHART_PATH>    Path to the Helm chart (e.g., ./my-chart or stable/nginx-ingress)"
    echo "  -r, --release <RELEASE_NAME>  Name of the Helm release (e.g., my-app-release)"
    echo "  -n, --namespace <NAMESPACE>   Kubernetes namespace to deploy to (default: default)"
    echo "  -f, --values <VALUES_FILE>    Path to a YAML values file (optional)"
    echo "  -u, --upgrade                 Perform a Helm upgrade instead of install (creates if not exists)"
    echo "  -d, --dry-run                 Simulate a release without installing or upgrading"
    echo "  -w, --wait                    Wait until all Pods, PVCs, Services, and minimum number of Pods of a Deployment are in a ready state before marking the release as successful. It will wait for as long as --timeout"
    echo "  -t, --timeout <DURATION>      Time to wait for any individual Kubernetes operation (default: 5m0s)"
    echo "  -h, --help                    Display this help message"
    echo ""
    echo "Examples:"
    echo "  $0 -c ./my-chart -r my-release -n dev"
    echo "  $0 -c stable/nginx-ingress -r nginx -n ingress -f values.yaml --upgrade --dry-run"
    echo "  $0 -c my-repo/my-app -r prod-app -n production --upgrade --wait --timeout 10m"
    echo ""
    echo "Requires: Helm CLI to be installed and kubectl configured to the target cluster."
}

log_error() {
    echo -e "\033[0;31m[ERROR]\033[0m $1" >&2
}

log_info() {
    echo -e "\033[0;34m[INFO]\033[0m $1"
}

log_success() {
    echo -e "\033[0;32m[SUCCESS]\033[0m $1"
}

# --- Argument Parsing ---
CHART_PATH=""
RELEASE_NAME=""
NAMESPACE="default"
VALUES_FILE=""
UPGRADE_FLAG=""
DRY_RUN_FLAG=""
WAIT_FLAG=""
TIMEOUT="5m0s"

while [[ $# -gt 0 ]]; do
    key="$1"
    case $key in
        -c|--chart)
        CHART_PATH="$2"
        shift # past argument
        shift # past value
        ;;
        -r|--release)
        RELEASE_NAME="$2"
        shift # past argument
        shift # past value
        ;;
        -n|--namespace)
        NAMESPACE="$2"
        shift # past argument
        shift # past value
        ;;
        -f|--values)
        VALUES_FILE="$2"
        shift # past argument
        shift # past value
        ;;
        -u|--upgrade)
        UPGRADE_FLAG="--upgrade"
        shift # past argument
        ;;
        -d|--dry-run)
        DRY_RUN_FLAG="--dry-run"
        shift # past argument
        ;;
        -w|--wait)
        WAIT_FLAG="--wait"
        shift # past argument
        ;;
        -t|--timeout)
        TIMEOUT="$2"
        shift # past argument
        shift # past value
        ;;
        -h|--help)
        print_help
        exit 0
        ;;
        *)
        log_error "Unknown option: $1"
        print_help
        exit 1
        ;;
    esac
done

# --- Input Validation ---
if [ -z "$CHART_PATH" ]; then
    log_error "Chart path is required. Use -c or --chart."
    print_help
    exit 1
fi

if [ -z "$RELEASE_NAME" ]; then
    log_error "Release name is required. Use -r or --release."
    print_help
    exit 1
fi

if [ -n "$VALUES_FILE" ] && [ ! -f "$VALUES_FILE" ]; then
    log_error "Values file not found: $VALUES_FILE"
    exit 1
fi

# --- Main Logic ---
log_info "Starting Helm deployment for release '$RELEASE_NAME' in namespace '$NAMESPACE'..."

HELM_COMMAND="${HELM_BIN} upgrade ${UPGRADE_FLAG} ${DRY_RUN_FLAG} ${WAIT_FLAG} --install ${RELEASE_NAME} ${CHART_PATH} --namespace ${NAMESPACE} --timeout ${TIMEOUT}"

if [ -n "$VALUES_FILE" ]; then
    HELM_COMMAND+=" -f ${VALUES_FILE}"
fi

log_info "Executing command: ${HELM_COMMAND}"

# Execute the Helm command
if eval "$HELM_COMMAND"; then
    log_success "Helm deployment for '$RELEASE_NAME' completed successfully."
    exit 0
else
    log_error "Helm deployment for '$RELEASE_NAME' failed."
    exit 1
fi
