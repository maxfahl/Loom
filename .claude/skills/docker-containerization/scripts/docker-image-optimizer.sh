#!/bin/bash

# docker-image-optimizer.sh
#
# Description:
#   Analyzes a Dockerfile for common anti-patterns and suggests optimizations
#   to reduce image size, improve build speed, and enhance security.
#   It provides actionable recommendations based on best practices.
#
# Usage:
#   ./docker-image-optimizer.sh <Dockerfile_path> [--dry-run]
#
# Arguments:
#   Dockerfile_path: The path to the Dockerfile to analyze.
#   --dry-run:       (Optional) If set, the script will only print recommendations
#                    without attempting any modifications (though this script
#                    doesn't modify files, it's good practice for future expansion).
#
# Examples:
#   ./docker-image-optimizer.sh ./Dockerfile
#   ./docker-image-optimizer.sh /app/backend/Dockerfile --dry-run
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
    echo "  Analyzes a Dockerfile for common anti-patterns and suggests optimizations"
    echo "  to reduce image size, improve build speed, and enhance security."
    echo "  It provides actionable recommendations based on best practices."
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

    log_info "Analyzing Dockerfile: $DOCKERFILE_PATH"
    if $DRY_RUN; then
        log_info "Running in dry-run mode. No modifications will be attempted."
    fi

    DOCKERFILE_CONTENT=$(cat "$DOCKERFILE_PATH")
    RECOMMENDATIONS_FOUND=0

    # --- Optimization Checks ---

    # 1. Check for 'latest' tag
    if grep -q "FROM .*latest" "$DOCKERFILE_PATH"; then
        log_warn "Recommendation: Avoid using 'latest' tag for base images. Pin to a specific version (e.g., 'node:20-alpine') for reproducibility."
        RECOMMENDATIONS_FOUND=$((RECOMMENDATIONS_FOUND + 1))
    fi

    # 2. Check for non-minimal base images (basic check)
    if echo "$DOCKERFILE_CONTENT" | grep -Eiq "FROM (ubuntu|debian|centos|fedora|node:[0-9]+$|python:[0-9.]+$|ruby:[0-9.]+$)" && ! echo "$DOCKERFILE_CONTENT" | grep -Eiq "FROM (alpine|slim)"; then
        log_warn "Recommendation: Consider using a minimal base image (e.g., Alpine, -slim variants) to reduce image size."
        RECOMMENDATIONS_FOUND=$((RECOMMENDATIONS_FOUND + 1))
    fi

    # 3. Check for missing .dockerignore
    if [[ ! -f "$(dirname "$DOCKERFILE_PATH")/.dockerignore" ]]; then
        log_warn "Recommendation: Create a '.dockerignore' file in the same directory as your Dockerfile to exclude unnecessary files from the build context (e.g., .git, node_modules, .env)."
        RECOMMENDATIONS_FOUND=$((RECOMMENDATIONS_FOUND + 1))
    fi

    # 4. Check for multiple consecutive RUN commands without chaining
    if echo "$DOCKERFILE_CONTENT" | awk '/^RUN/{count++} !/^RUN/{if(count>1) print NR-count; count=0}' | grep -q .; then
        log_warn "Recommendation: Combine multiple consecutive 'RUN' commands using '&&' to reduce the number of image layers and improve caching."
        RECOMMENDATIONS_FOUND=$((RECOMMENDATIONS_FOUND + 1))
    fi

    # 5. Check for multi-stage build potential (simple heuristic: multiple FROM statements)
    if [[ $(grep -c "^FROM" "$DOCKERFILE_PATH") -eq 1 ]]; then
        log_warn "Recommendation: Consider implementing multi-stage builds to separate build-time dependencies from runtime, significantly reducing final image size."
        RECOMMENDATIONS_FOUND=$((RECOMMENDATIONS_FOUND + 1))
    fi

    # --- Security Checks ---

    # 6. Check for running as root (no USER instruction or USER root)
    if ! echo "$DOCKERFILE_CONTENT" | grep -qE "^USER" || echo "$DOCKERFILE_CONTENT" | grep -qE "^USER\s+root"; then
        log_warn "Recommendation: Run containers as a non-root user. Add a 'USER' instruction with a non-root user after installing dependencies."
        RECOMMENDATIONS_FOUND=$((RECOMMENDATIONS_FOUND + 1))
    fi

    # 7. Check for hardcoded secrets (simple ENV check for common secret names)
    if echo "$DOCKERFILE_CONTENT" | grep -qE "ENV\s+(API_KEY|SECRET|PASSWORD|TOKEN)="; then
        log_warn "Recommendation: Avoid hardcoding sensitive information (e.g., API keys, passwords) in Dockerfiles. Use Docker Secrets or external secret management solutions."
        RECOMMENDATIONS_FOUND=$((RECOMMENDATIONS_FOUND + 1))
    fi

    # --- Reliability Checks ---

    # 8. Check for missing HEALTHCHECK
    if ! echo "$DOCKERFILE_CONTENT" | grep -qE "^HEALTHCHECK"; then
        log_warn "Recommendation: Add a 'HEALTHCHECK' instruction to your Dockerfile to allow Docker to determine the container's health status."
        RECOMMENDATIONS_FOUND=$((RECOMMENDATIONS_FOUND + 1))
    fi

    if [[ $RECOMMENDATIONS_FOUND -eq 0 ]]; then
        log_success "No major optimization or security issues found in $DOCKERFILE_PATH based on current checks."
    else
        log_info "Analysis complete. Found $RECOMMENDATIONS_FOUND potential areas for improvement."
    fi
}

main "$@"
