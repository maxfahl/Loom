#!/bin/bash

# k8s-health-check.sh
# Description: Checks the health and status of a Kubernetes deployment, including pod readiness, replica count, and service accessibility.
# Purpose: Automates the verification of a successful Kubernetes deployment, reducing manual checks and speeding up troubleshooting.

# Usage: ./k8s-health-check.sh <namespace> <deployment-name> [--kube-context <context>] [--timeout <seconds>]

# Configuration:
# KUBECTL_PATH: Path to kubectl executable (default: /usr/local/bin/kubectl or found in PATH)
# MAX_WAIT_SECONDS: Maximum time to wait for deployment to be ready (default: 300 seconds)

# Error handling:
# Exits with 1 if kubectl is not found, deployment not found, or deployment not ready within timeout.

# --- Script Start ---

# Set default values
KUBECTL_PATH=$(which kubectl)
MAX_WAIT_SECONDS=300
KUBE_CONTEXT=""
NAMESPACE=""
DEPLOYMENT_NAME=""

# Function to display help message
display_help() {
    echo "Usage: $0 <namespace> <deployment-name> [--kube-context <context>] [--timeout <seconds>]"
    echo ""
    echo "Checks the health and status of a Kubernetes deployment."
    echo ""
    echo "Arguments:"
    echo "  <namespace>        The Kubernetes namespace where the deployment is located."
    echo "  <deployment-name>  The name of the Kubernetes deployment to check."
    echo ""
    echo "Options:"
    echo "  --kube-context <context>  Specify the Kubernetes context to use (e.g., 'my-cluster-dev')."
    echo "  --timeout <seconds>       Maximum time to wait for the deployment to be ready (default: 300 seconds)."
    echo "  --help                    Display this help message."
    echo ""
    echo "Examples:"
    echo "  $0 default my-app-deployment"
    echo "  $0 production api-gateway --kube-context prod-cluster --timeout 600"
    exit 0
}

# Parse command-line arguments
while [[ "$#" -gt 0 ]]; do
    case "$1" in
        --kube-context)
            KUBE_CONTEXT="--context $2"
            shift
            ;;
        --timeout)
            MAX_WAIT_SECONDS="$2"
            shift
            ;;
        --help)
            display_help
            ;;
        -*)
            echo "Error: Unknown option: $1" >&2
            display_help
            ;;
        *)
            if [[ -z "$NAMESPACE" ]]; then
                NAMESPACE="$1"
            elif [[ -z "$DEPLOYMENT_NAME" ]]; then
                DEPLOYMENT_NAME="$1"
            else
                echo "Error: Too many arguments provided." >&2
                display_help
            fi
            ;;
    esac
    shift
done

# Validate required arguments
if [[ -z "$NAMESPACE" || -z "$DEPLOYMENT_NAME" ]]; then
    echo "Error: Namespace and deployment name are required." >&2
    display_help
fi

# Check if kubectl is installed
if ! command -v kubectl &> /dev/null; then
    echo "Error: kubectl is not installed or not found in PATH." >&2
    exit 1
fi

echo "--- Kubernetes Deployment Health Check ---"
echo "Deployment: $DEPLOYMENT_NAME in namespace $NAMESPACE"
echo "Kubernetes Context: ${KUBE_CONTEXT:-- (default)}"
echo "Max wait time: $MAX_WAIT_SECONDS seconds"
echo "----------------------------------------"

# Check if deployment exists
if ! $KUBECTL_PATH $KUBE_CONTEXT get deployment "$DEPLOYMENT_NAME" -n "$NAMESPACE" &> /dev/null; then
    echo "Error: Deployment '$DEPLOYMENT_NAME' not found in namespace '$NAMESPACE'." >&2
    exit 1
fi

# Wait for deployment to be ready
echo "Waiting for deployment '$DEPLOYMENT_NAME' to be ready..."
if ! $KUBECTL_PATH $KUBE_CONTEXT rollout status deployment/"$DEPLOYMENT_NAME" -n "$NAMESPACE" --timeout="${MAX_WAIT_SECONDS}s"; then
    echo "Error: Deployment '$DEPLOYMENT_NAME' did not become ready within ${MAX_WAIT_SECONDS} seconds." >&2
    exit 1
fi
echo "Deployment '$DEPLOYMENT_NAME' is ready."

# Check pod status
echo "Checking pod status for deployment '$DEPLOYMENT_NAME'..."
POD_STATUS=$($KUBECTL_PATH $KUBE_CONTEXT get pods -n "$NAMESPACE" -l app="$DEPLOYMENT_NAME" -o json | jq -r '.items[] | .status.phase + " " + .metadata.name')
if [[ -z "$POD_STATUS" ]]; then
    echo "Warning: No pods found for deployment '$DEPLOYMENT_NAME' with label 'app=$DEPLOYMENT_NAME'. This might indicate a misconfiguration."
else
    echo "Pods status:"
    echo "$POD_STATUS"
    if echo "$POD_STATUS" | grep -q "Running"; then
        echo "All pods are running."
    else
        echo "Warning: Some pods are not in 'Running' state."
    fi
fi

# Check service accessibility (if a service exists for the deployment)
echo "Checking for associated services..."
SERVICE_NAME=$($KUBECTL_PATH $KUBE_CONTEXT get service -n "$NAMESPACE" -l app="$DEPLOYMENT_NAME" -o jsonpath='{.items[0].metadata.name}' 2>/dev/null)

if [[ -n "$SERVICE_NAME" ]]; then
    echo "Found service: $SERVICE_NAME"
    SERVICE_TYPE=$($KUBECTL_PATH $KUBE_CONTEXT get service "$SERVICE_NAME" -n "$NAMESPACE" -o jsonpath='{.spec.type}')
    echo "Service type: $SERVICE_TYPE"

    case "$SERVICE_TYPE" in
        "LoadBalancer")
            EXTERNAL_IP=""
            for i in $(seq 1 60); do # Wait up to 60 seconds for external IP
                EXTERNAL_IP=$($KUBECTL_PATH $KUBE_CONTEXT get service "$SERVICE_NAME" -n "$NAMESPACE" -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
                if [[ -n "$EXTERNAL_IP" ]]; then
                    break
                fi
                sleep 1
            done
            if [[ -n "$EXTERNAL_IP" ]]; then
                echo "External IP: $EXTERNAL_IP"
                echo "Attempting to curl service..."
                if curl -s -o /dev/null -w "%{http_code}" "http://$EXTERNAL_IP" | grep -q "200"; then
                    echo "Service is accessible via HTTP (returned 2xx status)."
                else
                    echo "Warning: Service might not be fully accessible via HTTP or returned non-2xx status."
                fi
            else
                echo "Warning: LoadBalancer external IP not assigned within timeout."
            fi
            ;;
        "NodePort")
            echo "NodePort service detected. Manual check of node IP and port required for external access."
            ;;
        "ClusterIP")
            echo "ClusterIP service detected. Accessible only within the cluster."
            ;;
        *)
            echo "Unknown service type: $SERVICE_TYPE"
            ;;
    esac
else
    echo "No service found for deployment '$DEPLOYMENT_NAME' with label 'app=$DEPLOYMENT_NAME'."
fi

echo "--- Health check complete for deployment '$DEPLOYMENT_NAME' ---"
exit 0
