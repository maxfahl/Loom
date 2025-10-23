#!/bin/bash

# gcp-pipeline-status.sh
#
# This script checks the status of recent Google Cloud Build and Cloud Deploy runs
# for a specified GCP project. It provides a quick overview of pipeline health
# and direct links to logs for failed runs.
#
# Usage:
#    ./gcp-pipeline-status.sh --project <YOUR_GCP_PROJECT_ID>
#    ./gcp-pipeline-status.sh # Uses currently configured gcloud project
#
# Example:
#    ./gcp-pipeline-status.sh --project my-cicd-project-789
#    # Output will be a summary of recent Cloud Build and Cloud Deploy statuses.
#
#    # To get help:
#    ./gcp-pipeline-status.sh --help

set -euo pipefail

# --- Configuration ---
NUM_BUILDS=5 # Number of recent Cloud Builds to display
NUM_DELIVERIES=3 # Number of recent Cloud Deploy deliveries to display

# --- Colors ---
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# --- Helper Functions ---
log_info() { echo -e "${BLUE}INFO:${NC} $1"; }
log_success() { echo -e "${GREEN}SUCCESS:${NC} $1"; }
log_warn() { echo -e "${YELLOW}WARN:${NC} $1" >&2; }
log_error() { echo -e "${RED}ERROR:${NC} $1" >&2; }

show_help() {
    echo "Usage: $0 [OPTIONS]"
    echo "Checks the status of recent Google Cloud Build and Cloud Deploy runs."
    echo ""
    echo "Options:"
    echo "  --project PROJECT_ID  The GCP project ID to scan. If not provided, uses the currently configured gcloud project."
    echo "  --help                Display this help message."
    echo ""
    echo "Examples:"
    echo "  $0 --project my-dev-project-123"
    echo "  $0"
}

get_project_id_from_config() {
    local project_id
    project_id=$(gcloud config get-value project 2>/dev/null || true)
    if [[ -z "$project_id" ]]; then
        log_error "No GCP project configured in gcloud CLI. Please run 'gcloud config set project PROJECT_ID' or provide --project argument."
        exit 1
    fi
    echo "$project_id"
}

check_cloud_build_status() {
    local project_id="$1"
    log_info "Checking recent Cloud Build statuses for project '${project_id}' (last ${NUM_BUILDS} builds)..."

    local builds
    builds=$(gcloud builds list --project "${project_id}" --limit "${NUM_BUILDS}" --sort-by=\"~createTime\" --format=json 2>/dev/null || true)

    if [[ -z "$builds" || "$builds" == "[]" ]]; then
        log_warn "No recent Cloud Builds found for project '${project_id}'."
        return
    fi

    echo ""
    echo "--- Cloud Build Status ---"
    echo ""

    echo "$(echo "$builds" | jq -r '.[] | "Build ID: \(.id)\n  Status: \(.status)\n  Trigger: \(.buildTriggerId // \"N/A\")\n  Create Time: \(.createTime)\n  Log URL: \(.logUrl)\n" ')"

    local failed_builds
    failed_builds=$(echo "$builds" | jq -r '.[] | select(.status == "FAILURE" or .status == "TIMEOUT" or .status == "CANCELLED") | "- Build ID: \(.id), Status: \(.status), Log URL: \(.logUrl)"')

    if [[ -n "$failed_builds" ]]; then
        log_error "\nDetected Failed/Timed Out/Cancelled Cloud Builds:"
        echo "$failed_builds"
    else
        log_success "\nAll recent Cloud Builds are successful!"
    fi
}

check_cloud_deploy_status() {
    local project_id="$1"
    log_info "Checking recent Cloud Deploy statuses for project '${project_id}' (last ${NUM_DELIVERIES} deliveries)...
"

    local deliveries
    deliveries=$(gcloud deploy deliveries list --project "${project_id}" --limit "${NUM_DELIVERIES}" --sort-by=\"~createTime\" --format=json 2>/dev/null || true)

    if [[ -z "$deliveries" || "$deliveries" == "[]" ]]; then
        log_warn "No recent Cloud Deploy deliveries found for project '${project_id}'."
        return
    fi

    echo ""
    echo "--- Cloud Deploy Status ---"
    echo ""

    echo "$(echo "$deliveries" | jq -r '.[] | "Delivery Pipeline: \(.name | split(\" / \")[-1])\n  Last Release: \(.lastAttemptedRelease.id // \"N/A\")\n  Last Release Status: \(.lastAttemptedRelease.state // \"N/A\")\n  Last Release URL: https://console.cloud.google.com/deploy/deliveryPipelines/\(.name | split(\" / \")[-1])/releases/\(.lastAttemptedRelease.id // \"N/A\")?project=\(.project)" ')"

    local failed_deliveries
    failed_deliveries=$(echo "$deliveries" | jq -r '.[] | select(.lastAttemptedRelease.state == "FAILED" or .lastAttemptedRelease.state == "TERMINATED") | "- Delivery Pipeline: \(.name | split(\" / \")[-1]), Last Release Status: \(.lastAttemptedRelease.state), URL: https://console.cloud.google.com/deploy/deliveryPipelines/\(.name | split(\" / \")[-1])/releases/\(.lastAttemptedRelease.id // \"N/A\")?project=\(.project)"')

    if [[ -n "$failed_deliveries" ]]; then
        log_error "\nDetected Failed/Terminated Cloud Deploy Deliveries:"
        echo "$failed_deliveries"
    else
        log_success "\nAll recent Cloud Deploy deliveries are successful!"
    fi
}

# --- Main Logic ---
main() {
    local project_id=""

    while [[ $# -gt 0 ]]; do
        case "$1" in
            --project)
                project_id="$2"
                shift
                shift
                ;;            --help)
                show_help
                exit 0
                ;;            *)
                log_error "Unknown option: $1"
                show_help
                exit 1
                ;;        esac
    done

    if [[ -z "$project_id" ]]; then
        project_id=$(get_project_id_from_config)
    fi

    log_info "\n🚀 Starting GCP Pipeline Status Check for Project: ${project_id} 🚀\n"

    check_cloud_build_status "${project_id}"
    echo "\n"
    check_cloud_deploy_status "${project_id}"

    log_success "\nGCP Pipeline Status Check Complete."
}

main "$@"
