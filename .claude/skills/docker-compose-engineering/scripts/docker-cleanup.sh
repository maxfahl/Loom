#!/bin/bash

# docker-cleanup.sh
#
# Purpose:
#   Cleans up unused Docker resources (containers, images, volumes, networks)
#   to free up disk space and maintain a tidy Docker environment.
#
# Usage:
#   ./docker-cleanup.sh [--containers] [--images] [--volumes] [--networks] [--all] [--dry-run]
#
# Arguments:
#   --containers : Remove all stopped containers.
#   --images     : Remove dangling images (those not associated with any container).
#   --volumes    : Remove all unused local volumes.
#   --networks   : Remove all unused networks.
#   --all        : Remove all of the above (containers, images, volumes, networks).
#   --dry-run    : (Optional) Show what would be removed without actually removing it.
#   --help       : Show this help message and exit.
#
# Examples:
#   ./docker-cleanup.sh --all
#   ./docker-cleanup.sh --images --volumes
#   ./docker-cleanup.sh --containers --dry-run
#
# Features:
#   - Selective cleanup of Docker resources.
#   - Dry-run mode to preview changes.
#   - Includes basic error handling.
#   - Provides clear command-line arguments and help text.
#
# Dependencies:
#   - Docker must be installed and running.
#   - Bash shell.

# --- Configuration ---
CLEAN_CONTAINERS=false
CLEAN_IMAGES=false
CLEAN_VOLUMES=false
CLEAN_NETWORKS=false
DRY_RUN=false

# --- Functions ---

# Display help message
show_help() {
  echo "Usage: $0 [--containers] [--images] [--volumes] [--networks] [--all] [--dry-run]"
  echo ""
  echo "Arguments:"
  echo "  --containers : Remove all stopped containers."
  echo "  --images     : Remove dangling images (those not associated with any container)."
  echo "  --volumes    : Remove all unused local volumes."
  echo "  --networks   : Remove all unused networks."
  echo "  --all        : Remove all of the above (containers, images, volumes, networks)."
  echo "  --dry-run    : (Optional) Show what would be removed without actually removing it."
  echo "  --help       : Show this help message and exit."
  echo ""
  echo "Examples:"
  echo "  $0 --all"
  echo "  $0 --images --volumes"
  echo "  $0 --containers --dry-run"
  exit 0
}

# Parse command-line arguments
parse_args() {
  if [ "$#" -eq 0 ]; then
    show_help
  fi

  while [ "$#" -gt 0 ]; do
    case "$1" in
      --containers)
        CLEAN_CONTAINERS=true
        ;;
      --images)
        CLEAN_IMAGES=true
        ;;
      --volumes)
        CLEAN_VOLUMES=true
        ;;
      --networks)
        CLEAN_NETWORKS=true
        ;;
      --all)
        CLEAN_CONTAINERS=true
        CLEAN_IMAGES=true
        CLEAN_VOLUMES=true
        CLEAN_NETWORKS=true
        ;;
      --dry-run)
        DRY_RUN=true
        ;;
      --help)
        show_help
        ;;
      *)
        echo "Error: Unknown argument 
'$1'."
        show_help
        ;;
    esac
    shift
  done

  if ! "$CLEAN_CONTAINERS" && ! "$CLEAN_IMAGES" && ! "$CLEAN_VOLUMES" && ! "$CLEAN_NETWORKS" ; then
    echo "Error: No cleanup option specified. Use --help for options."
    exit 1
  fi
}

# Check if docker command exists
check_docker() {
  if ! command -v docker &> /dev/null; then
    echo "Error: Docker is not installed. Please install Docker to use this script."
    exit 1
  fi
  if ! docker info &> /dev/null; then
    echo "Error: Docker daemon is not running. Please start Docker."
    exit 1
  fi
}

# Main script logic
main() {
  parse_args "$@"
  check_docker

  echo "--- Starting Docker Cleanup ---"
  if "$DRY_RUN"; then
    echo "(DRY RUN MODE: No changes will be made)"
  fi

  local prune_cmd="docker system prune -f"
  local dry_run_flag=""
  if "$DRY_RUN"; then
    prune_cmd="docker system prune --filter 'until=24h'" # A trick to make prune show output without actually removing much
    dry_run_flag=" --format '{{.ID}} {{.Names}}'" # For listing, not pruning
  fi

  if "$CLEAN_CONTAINERS"; then
    echo "
--- Cleaning up stopped containers ---"
    if "$DRY_RUN"; then
      echo "Stopped containers that would be removed:"
      docker ps -a --filter status=exited --format "{{.ID}}	{{.Names}}	{{.Status}}"
    else
      docker container prune -f || echo "No stopped containers to remove."
    fi
  fi

  if "$CLEAN_IMAGES"; then
    echo "
--- Cleaning up dangling images ---"
    if "$DRY_RUN"; then
      echo "Dangling images that would be removed:"
      docker images -f "dangling=true" --format "{{.ID}}	{{.Repository}}	{{.Tag}}"
    else
      docker image prune -f || echo "No dangling images to remove."
    fi
  fi

  if "$CLEAN_VOLUMES"; then
    echo "
--- Cleaning up unused volumes ---"
    if "$DRY_RUN"; then
      echo "Unused volumes that would be removed:"
      docker volume ls -f "dangling=true" --format "{{.Name}}"
    else
      docker volume prune -f || echo "No unused volumes to remove."
    fi
  fi

  if "$CLEAN_NETWORKS"; then
    echo "
--- Cleaning up unused networks ---"
    if "$DRY_RUN"; then
      echo "Unused networks that would be removed:"
      docker network ls -f "dangling=true" --format "{{.Name}}	{{.ID}}"
    else
      docker network prune -f || echo "No unused networks to remove.""
    fi
  fi

  echo "
--- Docker Cleanup Complete ---"
  if "$DRY_RUN"; then
    echo "(DRY RUN MODE: No changes were made)"
  fi
}

# Execute main function
main "$@"
