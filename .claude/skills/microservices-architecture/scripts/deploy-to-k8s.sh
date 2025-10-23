#!/bin/bash

# deploy-to-k8s.sh: Automates the deployment of a microservice to Kubernetes.
#
# This script streamlines the process of building a Docker image, pushing it to
# a container registry, and applying Kubernetes manifests to deploy or update
# a microservice in a Kubernetes cluster.
#
# Prerequisites:
# - Docker installed and configured.
# - kubectl configured to connect to your target Kubernetes cluster.
# - Access to a container registry (e.g., Docker Hub, GCR, ECR).
#
# Usage:
#   ./deploy-to-k8s.sh [OPTIONS]
#
# Options:
#   --service-name <name>     Required: The name of the microservice (e.g., 'user-service').
#   --image-tag <tag>         Required: The Docker image tag (e.g., 'latest', 'v1.0.0').
#   --registry <url>          Required: Your container registry URL (e.g., 'myregistry.com/myorg').
#   --k8s-manifest <path>     Required: Path to the Kubernetes manifest file (e.g., 'k8s/deployment.yaml').
#   --dockerfile <path>       Optional: Path to the Dockerfile. Defaults to './Dockerfile'.
#   --build-context <path>    Optional: Path to the Docker build context. Defaults to '.'.
#   --namespace <namespace>   Optional: Kubernetes namespace to deploy to. Defaults to 'default'.
#   --dry-run                 Print the actions that would be taken without
#                             actually executing commands.
#   --help                    Show this help message and exit.
#
# Example:
#   ./deploy-to-k8s.sh \
#     --service-name user-service \
#     --image-tag v1.0.0 \
#     --registry myregistry.com/myorg \
#     --k8s-manifest k8s/user-service.yaml
#
#   ./deploy-to-k8s.sh --service-name product-service --image-tag latest --registry gcr.io/my-project --k8s-manifest k8s/product-service.yaml --dry-run

# --- Color Constants ---
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# --- Helper Functions ---
print_success() { echo -e "${GREEN}✓ $1${NC}"; }
print_info() { echo -e "${CYAN}ℹ $1${NC}"; }
print_warning() { echo -e "${YELLOW}▲ $1${NC}"; }
print_error() { echo -e "${RED}✗ $1${NC}"; }

show_help() {
  grep "^#" "$0" | grep -v "^#!" | sed -e 's/^# //g' -e 's/^#$//g'
}

# --- Main Logic ---

SERVICE_NAME=""
IMAGE_TAG=""
REGISTRY=""
K8S_MANIFEST=""
DOCKERFILE="./Dockerfile"
BUILD_CONTEXT="."
NAMESPACE="default"
DRY_RUN=false

# Parse arguments
while (( "$#" )); do
  case "$1" in
    --service-name)
      SERVICE_NAME="$2"
      shift 2
      ;;
    --image-tag)
      IMAGE_TAG="$2"
      shift 2
      ;;
    --registry)
      REGISTRY="$2"
      shift 2
      ;;
    --k8s-manifest)
      K8S_MANIFEST="$2"
      shift 2
      ;;
    --dockerfile)
      DOCKERFILE="$2"
      shift 2
      ;;
    --build-context)
      BUILD_CONTEXT="$2"
      shift 2
      ;;
    --namespace)
      NAMESPACE="$2"
      shift 2
      ;;
    --dry-run)
      DRY_RUN=true
      shift
      ;;
    --help)
      show_help
      exit 0
      ;;
    -*|--*=)
      print_error "Unsupported flag $1"
      show_help
      exit 1
      ;;
    *)
      print_error "Unsupported argument $1"
      show_help
      exit 1
      ;;
  esac
done

# Validate required arguments
if [ -z "$SERVICE_NAME" ] || [ -z "$IMAGE_TAG" ] || [ -z "$REGISTRY" ] || [ -z "$K8S_MANIFEST" ]; then
  print_error "Error: --service-name, --image-tag, --registry, and --k8s-manifest are required."
  show_help
  exit 1
fi

# Construct full image name
FULL_IMAGE_NAME="${REGISTRY}/${SERVICE_NAME}:${IMAGE_TAG}"

print_info "Starting deployment for service: ${SERVICE_NAME} (Image: ${FULL_IMAGE_NAME})"
if [ "$DRY_RUN" = true ]; then
  print_warning "Running in DRY-RUN mode. No commands will be executed."
fi

# --- Step 1: Build Docker Image ---
print_info "Building Docker image..."
BUILD_COMMAND="docker build -f ${DOCKERFILE} -t ${FULL_IMAGE_NAME} ${BUILD_CONTEXT}"
if [ "$DRY_RUN" = true ]; then
  print_info "Would execute: ${BUILD_COMMAND}"
else
  ${BUILD_COMMAND}
  if [ $? -ne 0 ]; then
    print_error "Docker image build failed."
    exit 1
  fi
  print_success "Docker image built successfully."
fi

# --- Step 2: Push Docker Image to Registry ---
print_info "Pushing Docker image to registry..."
PUSH_COMMAND="docker push ${FULL_IMAGE_NAME}"
if [ "$DRY_RUN" = true ]; then
  print_info "Would execute: ${PUSH_COMMAND}"
else
  ${PUSH_COMMAND}
  if [ $? -ne 0 ]; then
    print_error "Docker image push failed."
    exit 1
  fi
  print_success "Docker image pushed successfully."
fi

# --- Step 3: Deploy to Kubernetes ---
print_info "Deploying to Kubernetes namespace '${NAMESPACE}'..."
DEPLOY_COMMAND="kubectl apply -f ${K8S_MANIFEST} -n ${NAMESPACE}"
if [ "$DRY_RUN" = true ]; then
  print_info "Would execute: ${DEPLOY_COMMAND}"
else
  ${DEPLOY_COMMAND}
  if [ $? -ne 0 ]; then
    print_error "Kubernetes deployment failed."
    exit 1
  fi
  print_success "Kubernetes manifests applied successfully."
fi

print_success "Deployment process completed for ${SERVICE_NAME}."
print_info "You can check the deployment status with: kubectl get deployments -n ${NAMESPACE}"
print_info "And logs with: kubectl logs -f deployment/${SERVICE_NAME} -n ${NAMESPACE}"
