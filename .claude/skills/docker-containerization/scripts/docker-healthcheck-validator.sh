#!/bin/bash

# docker-healthcheck-validator.sh
#
# Description:
#   Validates the HEALTHCHECK instruction in a Dockerfile and provides recommendations
#   based on best practices for robustness and efficiency.
#
# Usage:
#   ./docker-healthcheck-validator.sh <Dockerfile_path> [--dry-run]
#
# Arguments:
#   Dockerfile_path: The path to the Dockerfile to analyze.
#   --dry-run:       (Optional) If set, the script will only print recommendations
#                    without attempting any modifications.
#
# Examples:
#   ./docker-healthcheck-validator.sh ./Dockerfile
#   ./docker-healthcheck-validator.sh /app/backend/Dockerfile --dry-run
#
# Configuration:
#   None directly, relies on Dockerfile content.
#
# Error Handling:
#   - Exits if Dockerfile path is not provided or file does not exist.
#   - Provides clear messages for each recommendation.

set -euo pipefail

# --- Colors for better readability ---
GREEN="\033[0;32m"
YELLOW="\033[0;33m"
RED="\033[0;31m"
BLUE="\033[0;34m"
NC="\033[0m" # No Color

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1" >&2
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_help() {
    echo "Usage: $0 <Dockerfile_path> [--dry-run]"
    echo ""
    echo "Arguments:"
    echo "  Dockerfile_path: The path to the Dockerfile to analyze."
    echo "  --dry-run:       (Optional) If set, the script will only print recommendations."
    echo ""
    echo "Description:"
    echo "  Validates the HEALTHCHECK instruction in a Dockerfile and provides recommendations."
    echo ""
    echo "Examples:"
    echo "  $0 ./Dockerfile"
    echo "  $0 /app/backend/Dockerfile --dry-run"
}

# --- Main script logic ---
main() {
    if [[ $# -eq 0 || "$1" == "--help" ]]; then
        print_help
        exit 0
    fi

    DOCKERFILE_PATH="$1"
    DRY_RUN=false

    if [[ $# -gt 1 && "$2" == "--dry-run" ]]; then
        DRY_RUN=true
    fi

    if [[ ! -f "$DOCKERFILE_PATH" ]]; then
        log_error "Dockerfile not found at: $DOCKERFILE_PATH"
        exit 1
    fi

    log_info "Analyzing HEALTHCHECK in Dockerfile: $DOCKERFILE_PATH"
    if $DRY_RUN; then
        log_info "Running in dry-run mode."
    fi

    DOCKERFILE_CONTENT=$(cat "$DOCKERFILE_PATH")
    HEALTHCHECK_FOUND=false
    RECOMMENDATIONS_FOUND=0

    # Check if HEALTHCHECK instruction exists
    if echo "$DOCKERFILE_CONTENT" | grep -qE "^HEALTHCHECK"; then
        HEALTHCHECK_FOUND=true
        log_success "HEALTHCHECK instruction found."

        HEALTHCHECK_LINE=$(echo "$DOCKERFILE_CONTENT" | grep -E "^HEALTHCHECK")

        # Check for recommended parameters
        if ! echo "$HEALTHCHECK_LINE" | grep -qE "--interval="; then
            log_warn "Recommendation: Specify '--interval' for the HEALTHCHECK. Default is 30s, but explicit is better."
            RECOMMENDATIONS_FOUND=$((RECOMMENDATIONS_FOUND + 1))
        fi
        if ! echo "$HEALTHCHECK_LINE" | grep -qE "--timeout="; then
            log_warn "Recommendation: Specify '--timeout' for the HEALTHCHECK. A reasonable timeout prevents hung checks."
            RECOMMENDATIONS_FOUND=$((RECOMMENDATIONS_FOUND + 1))
        fi
        if ! echo "$HEALTHCHECK_LINE" | grep -qE "--start-period="; then
            log_warn "Recommendation: Consider '--start-period' for applications that take time to initialize before responding to health checks."
            RECOMMENDATIONS_FOUND=$((RECOMMENDATIONS_FOUND + 1))
        fi
        if ! echo "$HEALTHCHECK_LINE" | grep -qE "--retries="; then
            log_warn "Recommendation: Specify '--retries' for the HEALTHCHECK. Default is 3, but explicit is better."
            RECOMMENDATIONS_FOUND=$((RECOMMENDATIONS_FOUND + 1))
        fi

        # Check for common healthcheck commands
        if echo "$HEALTHCHECK_LINE" | grep -qE "CMD\s+(curl|wget|/usr/bin/curl|/usr/bin/wget)"; then
            log_info "HEALTHCHECK uses 'curl' or 'wget'. Ensure these utilities are available in the container."
        elif echo "$HEALTHCHECK_LINE" | grep -qE "CMD\s+(node|python|java|go)"; then
            log_info "HEALTHCHECK uses application-specific command. Ensure it's lightweight and reliable."
        else
            log_warn "Recommendation: Ensure the HEALTHCHECK command is robust and accurately reflects application health (e.g., 'curl', 'wget', or a simple script)."
            RECOMMENDATIONS_FOUND=$((RECOMMENDATIONS_FOUND + 1))
        fi

        # Check for exit codes
        if ! echo "$HEALTHCHECK_LINE" | grep -qE "\|\|\s+exit\s+1"; then
            log_warn "Recommendation: Ensure your HEALTHCHECK command explicitly returns an exit code of 0 for success and 1 for failure (e.g., 'CMD curl --fail http://localhost/health || exit 1')."
            RECOMMENDATIONS_FOUND=$((RECOMMENDATIONS_FOUND + 1))
        fi

    else
        log_warn "No HEALTHCHECK instruction found in $DOCKERFILE_PATH."
        log_warn "Recommendation: Add a 'HEALTHCHECK' instruction to your Dockerfile to allow Docker to determine the container's health status. This is crucial for reliable deployments."
        RECOMMENDATIONS_FOUND=$((RECOMMENDATIONS_FOUND + 1))
    fi

    if [[ $RECOMMENDATIONS_FOUND -eq 0 ]]; then
        log_success "HEALTHCHECK in $DOCKERFILE_PATH appears well-configured."
    else
        log_info "Analysis complete. Found $RECOMMENDATIONS_FOUND potential areas for HEALTHCHECK improvement."
    fi
}

main "$@"
