#!/bin/bash

# helm-lint-validate.sh
# Description: Lints a Helm chart for syntax errors and best practices, and optionally validates it against a target Kubernetes cluster's schema.
# Purpose: Ensures Helm charts are well-formed and adhere to Kubernetes API standards before deployment, preventing common configuration errors.

# Usage: ./helm-lint-validate.sh <chart-path> [--kube-context <context>] [--strict] [--dry-run]

# Configuration:
# HELM_PATH: Path to helm executable (default: /usr/local/bin/helm or found in PATH)
# KUBECTL_PATH: Path to kubectl executable (default: /usr/local/bin/kubectl or found in PATH)

# Error handling:
# Exits with 1 if helm or kubectl is not found, chart path is invalid, or lint/validation fails.

# --- Script Start ---

# Set default values
HELM_PATH=$(which helm)
KUBECTL_PATH=$(which kubectl)
CHART_PATH=""
KUBE_CONTEXT_OPT=""
STRICT_LINT=false
DRY_RUN_INSTALL=false

# Function to display help message
display_help() {
    echo "Usage: $0 <chart-path> [--kube-context <context>] [--strict] [--dry-run] [--help]"
    echo ""
    echo "Lints a Helm chart and optionally validates it against a Kubernetes cluster."
    echo ""
    echo "Arguments:"
    echo "  <chart-path>      The path to the Helm chart directory (e.g., './my-chart')."
    echo ""
    echo "Options:"
    echo "  --kube-context <context>  Specify the Kubernetes context for validation (e.g., 'my-cluster-dev')."
    echo "  --strict                  Enable strict linting (fail on warnings)."
    echo "  --dry-run                 Perform a Helm install --dry-run --debug to validate against cluster schema."
    echo "  --help                    Display this help message."
    echo ""
    echo "Examples:"
    echo "  $0 ./charts/my-app"
    echo "  $0 ./charts/my-app --strict --dry-run --kube-context dev-cluster"
    exit 0
}

# Parse command-line arguments
while [[ "$#" -gt 0 ]]; do
    case "$1" in
        --kube-context)
            KUBE_CONTEXT_OPT="--kube-context $2"
            shift
            ;;
        --strict)
            STRICT_LINT=true
            ;;
        --dry-run)
            DRY_RUN_INSTALL=true
            ;;
        --help)
            display_help
            ;;
        -*)
            echo "Error: Unknown option: $1" >&2
            display_help
            ;;
        *)
            if [[ -z "$CHART_PATH" ]]; then
                CHART_PATH="$1"
            else
                echo "Error: Too many arguments provided." >&2
                display_help
            fi
            ;;
    esac
    shift
done

# Validate required arguments
if [[ -z "$CHART_PATH" ]]; then
    echo "Error: Chart path is required." >&2
    display_help
fi

# Check if helm is installed
if ! command -v helm &> /dev/null; then
    echo "Error: helm is not installed or not found in PATH." >&2
    exit 1
fi

# Check if chart path is valid
if [[ ! -d "$CHART_PATH" ]]; then
    echo "Error: Chart path '$CHART_PATH' is not a valid directory." >&2
    exit 1
fi

echo "--- Helm Chart Lint and Validation ---"
echo "Chart Path: $CHART_PATH"
echo "Strict Lint: $STRICT_LINT"
echo "Dry Run Install: $DRY_RUN_INSTALL"
[[ -n "$KUBE_CONTEXT_OPT" ]] && echo "Kubernetes Context: $(echo $KUBE_CONTEXT_OPT | cut -d' ' -f2)"
echo "--------------------------------------"

# Perform Helm lint
echo "Running Helm lint..."
LINT_COMMAND="$HELM_PATH lint $CHART_PATH"
if $STRICT_LINT; then
    LINT_COMMAND="$LINT_COMMAND --strict"
fi

if ! $LINT_COMMAND; then
    echo "Error: Helm lint failed." >&2
    exit 1
fi
echo "Helm lint passed."

# Perform Helm dry-run install for validation against cluster schema
if $DRY_RUN_INSTALL; then
    echo "Running Helm dry-run install for schema validation..."
    if ! command -v kubectl &> /dev/null; then
        echo "Error: kubectl is required for --dry-run validation but not found in PATH." >&2
        exit 1
    fi

    # Use a dummy release name and namespace for dry-run
    if ! $HELM_PATH install my-chart-dry-run $CHART_PATH --dry-run --debug --namespace default $KUBE_CONTEXT_OPT > /dev/null; then
        echo "Error: Helm dry-run install failed. This indicates potential schema validation issues or invalid Kubernetes resources." >&2
        exit 1
    fi
    echo "Helm dry-run install passed. Chart is valid against Kubernetes cluster schema."
else
    echo "Skipping Helm dry-run install. Use --dry-run to validate against cluster schema."
fi

echo "--- Helm chart validation complete for '$CHART_PATH' ---"
exit 0
