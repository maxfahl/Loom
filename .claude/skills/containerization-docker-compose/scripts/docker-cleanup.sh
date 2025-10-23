#!/bin/bash
# docker-cleanup.sh: A script to clean up old Docker images, containers, and volumes.
#
# This script helps free up disk space and maintain a tidy Docker environment
# by removing unused or dangling Docker resources. It provides options for
# interactive confirmation and dry runs.
#
# Usage:
#    ./docker-cleanup.sh [--containers] [--images] [--volumes] [--networks] [--all] [--force] [--dry-run] [--verbose]
#
# Examples:
#    # Clean up all dangling images and stopped containers interactively
#    ./docker-cleanup.sh --images --containers

#    # Clean up all unused Docker resources without confirmation
#    ./docker-cleanup.sh --all --force

#    # Dry run: show what would be removed without actually deleting anything
#    ./docker-cleanup.sh --all --dry-run
#
# Configuration:
#    - Requires Docker to be installed and running.
#
# Error Handling:
#    - Exits if Docker is not running.
#    - Provides informative messages about what is being removed.
#
# Dependencies:
#    - Docker CLI
#

# --- Configuration --- START
# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color
# --- Configuration --- END

# --- Helper Functions --- START
log_error() {
    echo -e "${RED}ERROR: $1${NC}" >&2
    exit 1
}

log_warning() {
    echo -e "${YELLOW}WARNING: $1${NC}" >&2
}

log_info() {
    if [[ "$VERBOSE" == "true" ]]; then
        echo -e "${GREEN}INFO: $1${NC}"
    fi
}

check_docker() {
    if ! command -v docker &> /dev/null; then
        log_error "Docker CLI not found. Please install Docker."
    fi
    if ! docker info &> /dev/null; then
        log_error "Docker daemon is not running. Please start Docker."
    fi
}

confirm_action() {
    if [[ "$FORCE" == "true" ]]; then
        return 0 # Auto-confirm if --force is used
    fi
    read -r -p "${YELLOW}Are you sure you want to proceed? (y/N): ${NC}" response
    if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
        return 0
    else
        return 1
    fi
}

run_command() {
    local cmd="$@"
    log_info "Executing: $cmd"
    if [[ "$DRY_RUN" == "true" ]]; then
        echo -e "${YELLOW}DRY RUN: Would execute: $cmd${NC}"
    else
        eval "$cmd"
        if [[ $? -ne 0 ]]; then
            log_warning "Command failed: $cmd"
        fi
    fi
}
# --- Helper Functions --- END

# --- Main Logic --- START

CLEAN_CONTAINERS="false"
CLEAN_IMAGES="false"
CLEAN_VOLUMES="false"
CLEAN_NETWORKS="false"
CLEAN_ALL="false"
FORCE="false"
DRY_RUN="false"
VERBOSE="false"

# Parse command-line arguments
while [[ $# -gt 0 ]]; do
    key="$1"
    case $key in
        --containers)
        CLEAN_CONTAINERS="true"
        shift # past argument
        ;;
        --images)
        CLEAN_IMAGES="true"
        shift # past argument
        ;;
        --volumes)
        CLEAN_VOLUMES="true"
        shift # past argument
        ;;
        --networks)
        CLEAN_NETWORKS="true"
        shift # past argument
        ;;
        --all)
        CLEAN_ALL="true"
        shift # past argument
        ;;
        --force)
        FORCE="true"
        shift # past argument
        ;;
        --dry-run)
        DRY_RUN="true"
        shift # past argument
        ;;
        --verbose)
        VERBOSE="true"
        shift # past argument
        ;;
        -h|--help)
        echo "Usage: $0 [--containers] [--images] [--volumes] [--networks] [--all] [--force] [--dry-run] [--verbose]"
        echo ""
        echo "Options:"
        echo "  --containers   Remove all stopped containers."
        echo "  --images       Remove all dangling images (images not associated with any container)."
        echo "  --volumes      Remove all unused local volumes."
        echo "  --networks     Remove all unused networks."
        echo "  --all          Remove all stopped containers, dangling images, unused volumes, and unused networks."
        echo "  --force        Do not ask for confirmation before removing resources."
        echo "  --dry-run      Show what would be removed without actually deleting anything."
        echo "  --verbose      Enable verbose output."
        echo "  -h, --help     Display this help message."
        exit 0
        ;;
        *)
        log_error "Unknown option: $1"
        ;;
    esac
done

# If no specific cleanup option is provided, default to --all
if [[ "$CLEAN_CONTAINERS" == "false" && \
      "$CLEAN_IMAGES" == "false" && \
      "$CLEAN_VOLUMES" == "false" && \
      "$CLEAN_NETWORKS" == "false" && \
      "$CLEAN_ALL" == "false" ]]; then
    CLEAN_ALL="true"
fi

# If --all is specified, enable all specific cleanup options
if [[ "$CLEAN_ALL" == "true" ]]; then
    CLEAN_CONTAINERS="true"
    CLEAN_IMAGES="true"
    CLEAN_VOLUMES="true"
    CLEAN_NETWORKS="true"
fi

# Check Docker installation and status
check_docker

log_info "Starting Docker cleanup process..."

# Cleanup containers
if [[ "$CLEAN_CONTAINERS" == "true" ]]; then
    echo -e "\n${GREEN}--- Cleaning up stopped containers ---${NC}"
    STOPPED_CONTAINERS=$(docker ps -aq --filter status=exited)
    if [[ -n "$STOPPED_CONTAINERS" ]]; then
        echo "The following stopped containers will be removed:"
        echo "$STOPPED_CONTAINERS"
        if confirm_action; then
            run_command "docker rm $STOPPED_CONTAINERS"
        else
            log_info "Skipping stopped containers removal."
        fi
    else
        log_info "No stopped containers to remove."
    fi
fi

# Cleanup dangling images
if [[ "$CLEAN_IMAGES" == "true" ]]; then
    echo -e "\n${GREEN}--- Cleaning up dangling images ---${NC}"
    DANGLING_IMAGES=$(docker images -q --filter dangling=true)
    if [[ -n "$DANGLING_IMAGES" ]]; then
        echo "The following dangling images will be removed:"
        docker images --filter dangling=true
        if confirm_action; then
            run_command "docker rmi $DANGLING_IMAGES"
        else
            log_info "Skipping dangling images removal."
        fi
    else
        log_info "No dangling images to remove."
    fi
fi

# Cleanup unused volumes
if [[ "$CLEAN_VOLUMES" == "true" ]]; then
    echo -e "\n${GREEN}--- Cleaning up unused volumes ---${NC}"
    UNUSED_VOLUMES=$(docker volume ls -q --filter dangling=true)
    if [[ -n "$UNUSED_VOLUMES" ]]; then
        echo "The following unused volumes will be removed:"
        docker volume ls --filter dangling=true
        if confirm_action; then
            run_command "docker volume rm $UNUSED_VOLUMES"
        else
            log_info "Skipping unused volumes removal."
        fi
    else
        log_info "No unused volumes to remove."
    fi
fi

# Cleanup unused networks
if [[ "$CLEAN_NETWORKS" == "true" ]]; then
    echo -e "\n${GREEN}--- Cleaning up unused networks ---${NC}"
    UNUSED_NETWORKS=$(docker network ls -q --filter dangling=true)
    if [[ -n "$UNUSED_NETWORKS" ]]; then
        echo "The following unused networks will be removed:"
        docker network ls --filter dangling=true
        if confirm_action; then
            run_command "docker network rm $UNUSED_NETWORKS"
        else
            log_info "Skipping unused networks removal."
        fi
    else
        log_info "No unused networks to remove."
    fi
fi

log_info "Docker cleanup process finished."

# --- Main Logic --- END
