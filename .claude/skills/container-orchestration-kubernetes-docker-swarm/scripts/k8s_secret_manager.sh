#!/bin/bash

# k8s_secret_manager.sh
# Description: Manages Kubernetes Secrets (create or update) from a file or a direct value.
#              Supports opaque secrets.

# --- Configuration Variables (can be overridden by environment variables or arguments) ---
KUBECTL_BIN=${KUBECTL_BIN:-"kubectl"}

# --- Helper Functions ---
print_help() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Manages Kubernetes Secrets (create or update)."
    echo ""
    echo "Options:"
    echo "  -n, --namespace <NAMESPACE>   Kubernetes namespace for the secret (default: default)"
    echo "  -s, --secret-name <NAME>      Name of the Kubernetes Secret (e.g., my-api-key)"
    echo "  -k, --key <KEY>               Key name within the secret (e.g., api-key)"
    echo "  -f, --from-file <FILE_PATH>   Path to a file whose content will be used as the secret value"
    echo "  -v, --from-value <VALUE>      Direct string value for the secret (use with caution for sensitive data)"
    echo "  -t, --type <TYPE>             Type of the secret (default: Opaque). Other common types: generic, docker-registry, tls"
    echo "  -o, --overwrite               Overwrite the secret if it already exists (default: false)"
    echo "  -d, --dry-run                 Simulate the command without applying changes to the cluster"
    echo "  -h, --help                    Display this help message"
    echo ""
    echo "Examples:"
    echo "  # Create a secret from a file"
    echo "  $0 -n default -s my-app-secret -k api-key -f ./secrets/api_key.txt"
    echo ""
    echo "  # Create a secret from a direct value (use with caution)"
    echo "  $0 -n dev -s db-pass -k password -v \"supersecurepassword\""
    echo ""
    echo "  # Update an existing secret, overwriting its value"
    echo "  $0 -n prod -s my-app-secret -k api-key -f ./secrets/new_api_key.txt --overwrite"
    echo ""
    echo "  # Dry-run creation of a secret"
    echo "  $0 -n test -s test-secret -k test-data -v \"testvalue\" --dry-run"
    echo ""
    echo "Requires: kubectl to be installed and configured to the target cluster."
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
NAMESPACE="default"
SECRET_NAME=""
SECRET_KEY=""
FROM_FILE=""
FROM_VALUE=""
SECRET_TYPE="Opaque"
OVERWRITE_FLAG=""
DRY_RUN_FLAG=""

while [[ $# -gt 0 ]]; do
    key="$1"
    case $key in
        -n|--namespace)
        NAMESPACE="$2"
        shift # past argument
        shift # past value
        ;;
        -s|--secret-name)
        SECRET_NAME="$2"
        shift # past argument
        shift # past value
        ;;
        -k|--key)
        SECRET_KEY="$2"
        shift # past argument
        shift # past value
        ;;
        -f|--from-file)
        FROM_FILE="$2"
        shift # past argument
        shift # past value
        ;;
        -v|--from-value)
        FROM_VALUE="$2"
        shift # past argument
        shift # past value
        ;;
        -t|--type)
        SECRET_TYPE="$2"
        shift # past argument
        shift # past value
        ;;
        -o|--overwrite)
        OVERWRITE_FLAG="--overwrite"
        shift # past argument
        ;;
        -d|--dry-run)
        DRY_RUN_FLAG="--dry-run=client"
        shift # past argument
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
if [ -z "$SECRET_NAME" ]; then
    log_error "Secret name is required. Use -s or --secret-name."
    print_help
    exit 1
fi

if [ -z "$SECRET_KEY" ]; then
    log_error "Secret key is required. Use -k or --key."
    print_help
    exit 1
fi

if [ -z "$FROM_FILE" ] && [ -z "$FROM_VALUE" ]; then
    log_error "Either --from-file or --from-value must be provided."
    print_help
    exit 1
fi

if [ -n "$FROM_FILE" ] && [ -n "$FROM_VALUE" ]; then
    log_error "Cannot use both --from-file and --from-value simultaneously."
    print_help
    exit 1
fi

if [ -n "$FROM_FILE" ] && [ ! -f "$FROM_FILE" ]; then
    log_error "File not found: $FROM_FILE"
    exit 1
fi

# --- Main Logic ---
log_info "Preparing Kubernetes Secret '$SECRET_NAME' in namespace '$NAMESPACE'..."

# Check if secret exists
SECRET_EXISTS=$(${KUBECTL_BIN} get secret "$SECRET_NAME" -n "$NAMESPACE" &> /dev/null; echo $?)

CREATE_OR_REPLACE="create"
if [ "$SECRET_EXISTS" -eq 0 ]; then
    log_info "Secret '$SECRET_NAME' already exists."
    if [ -z "$OVERWRITE_FLAG" ]; then
        log_error "Secret '$SECRET_NAME' already exists. Use --overwrite to update it."
        exit 1
    else
        CREATE_OR_REPLACE="replace"
        log_info "Using 'replace' command due to --overwrite flag."
    fi
fi

COMMAND_ARGS=(
    "$CREATE_OR_REPLACE"
    "secret"
    "$SECRET_TYPE"
    "$SECRET_NAME"
    "--namespace"
    "$NAMESPACE"
)

if [ -n "$FROM_FILE" ]; then
    COMMAND_ARGS+=("--from-file=${SECRET_KEY}=${FROM_FILE}")
elif [ -n "$FROM_VALUE" ]; then
    COMMAND_ARGS+=("--from-literal=${SECRET_KEY}=${FROM_VALUE}")
fi

if [ -n "$DRY_RUN_FLAG" ]; then
    COMMAND_ARGS+=("$DRY_RUN_FLAG" "-o" "yaml")
fi

log_info "Executing command: ${KUBECTL_BIN} ${COMMAND_ARGS[*]}"

if ${KUBECTL_BIN} "${COMMAND_ARGS[@]}"; then
    if [ -n "$DRY_RUN_FLAG" ]; then
        log_success "Dry-run for secret '$SECRET_NAME' successful."
    else
        log_success "Kubernetes Secret '$SECRET_NAME' ${CREATE_OR_REPLACE}d successfully."
    fi
    exit 0
else
    log_error "Failed to ${CREATE_OR_REPLACE} Kubernetes Secret '$SECRET_NAME'."
    exit 1
fi
