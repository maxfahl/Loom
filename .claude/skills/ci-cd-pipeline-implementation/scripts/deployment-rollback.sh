#!/bin/bash

# deployment-rollback.sh
#
# Purpose:
#   Automates the rollback of a deployed application to a specified previous version.
#   This script interacts with common deployment tools (e.g., kubectl, cloud provider CLIs)
#   to quickly revert to a stable state, minimizing downtime.
#
# Usage:
#   ./deployment-rollback.sh --type <kubernetes|ecs|gcloud> --name <deployment_name> [--namespace <namespace>] [--revision <revision_number>] [--dry-run]
#
# Requirements:
#   - kubectl: For Kubernetes rollbacks. Install via your package manager or official docs.
#   - aws cli: For AWS ECS rollbacks. Install via official docs.
#   - gcloud cli: For Google Cloud Run rollbacks. Install via official docs.
#
# Configuration:
#   - KUBECONFIG: Path to your Kubernetes configuration file (if not default).
#   - AWS_PROFILE: AWS CLI profile to use.
#   - GCLOUD_PROJECT: Google Cloud project ID.
#
# Exit Codes:
#   0: Rollback initiated successfully or dry-run completed.
#   1: An error occurred during rollback.

set -euo pipefail

# --- Colors for better readability ---
RED="\033[0;31m"
GREEN="\033[0;32m"
YELLOW="\033[0;33m"
BLUE="\033[0;34m"
NC="\033[0m" # No Color

# --- Helper Functions ---

log_info() {
  echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
  echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warn() {
  echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
  echo -e "${RED}[ERROR]${NC} $1" >&2
}

# Function to display help message
show_help() {
  echo "Usage: $0 --type <kubernetes|ecs|gcloud> --name <deployment_name> [OPTIONS]"
  echo ""
  echo "  Automates the rollback of a deployed application to a specified previous version."
  echo ""
  echo "Required Arguments:"
  echo "  --type <kubernetes|ecs|gcloud>  The type of deployment platform."
  echo "  --name <deployment_name>        The name of the deployment or service to rollback."
  echo ""
  echo "Options:"
  echo "  --namespace <namespace>         (Kubernetes only) The Kubernetes namespace. Defaults to 'default'."
  echo "  --revision <revision_number>    (Kubernetes only) The target revision number to rollback to."
  echo "                                  If omitted, rolls back to the previous revision."
  echo "  --cluster <cluster_name>        (ECS only) The ECS cluster name."
  echo "  --service <service_name>        (ECS only) The ECS service name. Defaults to --name."
  echo "  --region <aws_region>           (ECS/GCloud) AWS/GCloud region. Defaults to environment config."
  echo "  --project <gcloud_project>      (GCloud only) Google Cloud project ID."
  echo "  --dry-run                       Perform a dry run without making any actual changes."
  echo "  -h, --help                      Show this help message and exit."
  echo ""
  echo "Examples:"
  echo "  # Kubernetes: Rollback 'my-app' in 'production' namespace to previous revision"
  echo "  $0 --type kubernetes --name my-app --namespace production"
  echo ""
  echo "  # Kubernetes: Rollback 'my-app' to revision 3"
  echo "  $0 --type kubernetes --name my-app --revision 3"
  echo ""
  echo "  # AWS ECS: Rollback 'my-service' in 'my-cluster'"
  echo "  $0 --type ecs --name my-service --cluster my-cluster"
  echo ""
  echo "  # Google Cloud Run: Rollback 'my-service' in 'my-project'"
  echo "  $0 --type gcloud --name my-service --project my-project --region us-central1"
}

# --- Argument Parsing ---
DEPLOYMENT_TYPE=""
DEPLOYMENT_NAME=""
NAMESPACE="default"
REVISION=""
CLUSTER=""
SERVICE_NAME=""
REGION=""
PROJECT=""
DRY_RUN=false

while [[ $# -gt 0 ]]; do
  key="$1"
  case $key in
    --type)
      DEPLOYMENT_TYPE="$2"
      shift # past argument
      shift # past value
      ;;
    --name)
      DEPLOYMENT_NAME="$2"
      shift # past argument
      shift # past value
      ;;
    --namespace)
      NAMESPACE="$2"
      shift # past argument
      shift # past value
      ;;
    --revision)
      REVISION="$2"
      shift # past argument
      shift # past value
      ;;
    --cluster)
      CLUSTER="$2"
      shift # past argument
      shift # past value
      ;;
    --service)
      SERVICE_NAME="$2"
      shift # past argument
      shift # past value
      ;;
    --region)
      REGION="$2"
      shift # past argument
      shift # past value
      ;;
    --project)
      PROJECT="$2"
      shift # past argument
      shift # past value
      ;;
    --dry-run)
      DRY_RUN=true
      shift # past argument
      ;;
    -h|--help)
      show_help
      exit 0
      ;;
    *)
      log_error "Unknown option: $1"
      show_help
      exit 1
      ;;
  esac
done

# Validate required arguments
if [ -z "$DEPLOYMENT_TYPE" ] || [ -z "$DEPLOYMENT_NAME" ]; then
  log_error "Missing required arguments: --type and --name."
  show_help
  exit 1
fi

# --- Rollback Functions ---

rollback_kubernetes() {
  log_info "Initiating Kubernetes rollback for deployment '$DEPLOYMENT_NAME' in namespace '$NAMESPACE'..."
  local cmd="kubectl rollout undo deployment/$DEPLOYMENT_NAME -n $NAMESPACE"
  if [ -n "$REVISION" ]; then
    cmd="$cmd --to-revision=$REVISION"
    log_info "  Targeting revision: $REVISION"
  else
    log_info "  Rolling back to previous revision."
  fi

  if $DRY_RUN; then
    log_warn "(Dry-run) Kubernetes rollback command: $cmd"
    log_success "(Dry-run) Kubernetes rollback would be initiated."
  else
    log_info "Executing: $cmd"
    if eval "$cmd"; then
      log_success "Kubernetes deployment '$DEPLOYMENT_NAME' rollback initiated successfully."
      log_info "You can check the status with: kubectl rollout status deployment/$DEPLOYMENT_NAME -n $NAMESPACE"
    else
      log_error "Failed to initiate Kubernetes deployment rollback."
      exit 1
    fi
  fi
}

rollback_ecs() {
  SERVICE_NAME="${SERVICE_NAME:-$DEPLOYMENT_NAME}"
  if [ -z "$CLUSTER" ]; then
    log_error "For ECS rollback, --cluster is required."
    exit 1
  fi
  log_info "Initiating AWS ECS rollback for service '$SERVICE_NAME' in cluster '$CLUSTER'..."
  local cmd="aws ecs update-service --cluster $CLUSTER --service $SERVICE_NAME --force-new-deployment"
  if [ -n "$REGION" ]; then
    cmd="$cmd --region $REGION"
  fi

  if $DRY_RUN; then
    log_warn "(Dry-run) AWS ECS rollback command: $cmd"
    log_success "(Dry-run) AWS ECS rollback would be initiated."
  else
    log_info "Executing: $cmd"
    if eval "$cmd"; then
      log_success "AWS ECS service '$SERVICE_NAME' rollback initiated successfully."
      log_info "This will force a new deployment of the currently deployed task definition."
      log_info "To revert to a specific previous task definition, you would need to update the service with --task-definition."
    else
      log_error "Failed to initiate AWS ECS service rollback."
      exit 1
    fi
  fi
}

rollback_gcloud() {
  if [ -z "$PROJECT" ]; then
    log_error "For Google Cloud Run rollback, --project is required."
    exit 1
  fi
  if [ -z "$REGION" ]; then
    log_error "For Google Cloud Run rollback, --region is required."
    exit 1
  fi
  log_info "Initiating Google Cloud Run rollback for service '$DEPLOYMENT_NAME' in project '$PROJECT' and region '$REGION'..."
  
  # Get current revisions
  local revisions_json
  revisions_json=$(gcloud run revisions list --service "$DEPLOYMENT_NAME" --project "$PROJECT" --region "$REGION" --format=json)
  
  local latest_revision
  latest_revision=$(echo "$revisions_json" | jq -r '.[0].metadata.name')
  
  local previous_revision
  previous_revision=$(echo "$revisions_json" | jq -r '.[1].metadata.name')

  if [ -z "$previous_revision" ]; then
    log_error "No previous revision found for service '$DEPLOYMENT_NAME'. Cannot rollback."
    exit 1
  fi

  log_info "Latest revision: $latest_revision"
  log_info "Previous revision: $previous_revision"

  local cmd="gcloud run services update $DEPLOYMENT_NAME --project $PROJECT --region $REGION --no-traffic --to-revisions=$previous_revision"

  if $DRY_RUN; then
    log_warn "(Dry-run) Google Cloud Run rollback command: $cmd"
    log_success "(Dry-run) Google Cloud Run rollback would be initiated to revision '$previous_revision'."
  else
    log_info "Executing: $cmd"
    if eval "$cmd"; then
      log_success "Google Cloud Run service '$DEPLOYMENT_NAME' rollback initiated successfully to revision '$previous_revision'."
      log_info "Traffic is now directed to the previous revision. You may need to adjust traffic splitting if you want to fully revert."
    else
      log_error "Failed to initiate Google Cloud Run service rollback."
      exit 1
    fi
  fi
}

# --- Main Logic ---

case "$DEPLOYMENT_TYPE" in
  kubernetes)
    rollback_kubernetes
    ;;
  ecs)
    rollback_ecs
    ;;
  gcloud)
    rollback_gcloud
    ;;
  *)
    log_error "Invalid deployment type: '$DEPLOYMENT_TYPE'. Supported types: kubernetes, ecs, gcloud."
    show_help
    exit 1
    ;;
esac
