#!/bin/bash

# compose-cleanup.sh
#
# Purpose:
#   Provides a convenient way to clean up stopped Docker Compose containers,
#   dangling images, unused volumes, and networks, either for a specific project
#   or globally.
#
# Pain Point Solved:
#   Frees up disk space and prevents resource clutter from old or failed Docker Compose runs.
#
# Usage:
#   ./compose-cleanup.sh [options]
#
# Options:
#   -p, --project       Clean up resources for the current Docker Compose project only.
#                       (Requires a docker-compose.yml in the current directory)
#   -g, --global        Clean up all unused Docker resources globally (containers, images, volumes, networks).
#   -c, --containers    Clean up stopped containers.
#   -i, --images        Clean up dangling images.
#   -v, --volumes       Clean up unused volumes.
#   -n, --networks      Clean up unused networks.
#   -a, --all           Clean up all types of resources (containers, images, volumes, networks).
#   -d, --dry-run       Show what would be cleaned up without actually deleting anything.
#   -h, --help          Display this help message.
#
# Examples:
#   ./compose-cleanup.sh --project --all
#   ./compose-cleanup.sh --global --images --volumes
#   ./compose-cleanup.sh -g -a -d

set -euo pipefail

# --- Configuration ---
DRY_RUN=false
CLEAN_PROJECT=false
CLEAN_GLOBAL=false
CLEAN_CONTAINERS=false
CLEAN_IMAGES=false
CLEAN_VOLUMES=false
CLEAN_NETWORKS=false

# --- Functions ---

log_info() {
  echo -e "\033[0;34m[INFO]\033[0m $1"
}

log_success() {
  echo -e "\033[0;32m[SUCCESS]\033[0m $1"
}

log_warning() {
  echo -e "\033[0;33m[WARNING]\033[0m $1"
}

log_error() {
  echo -e "\033[0;31m[ERROR]\033[0m $1" >&2
}

show_help() {
  grep "^#" "$0" | cut -c 2-
}

# --- Argument Parsing ---

while [[ $# -gt 0 ]]; do
  key="$1"
  case $key in
    -p|--project)
      CLEAN_PROJECT=true
      shift
      ;;
    -g|--global)
      CLEAN_GLOBAL=true
      shift
      ;;
    -c|--containers)
      CLEAN_CONTAINERS=true
      shift
      ;;
    -i|--images)
      CLEAN_IMAGES=true
      shift
      ;;
    -v|--volumes)
      CLEAN_VOLUMES=true
      shift
      ;;
    -n|--networks)
      CLEAN_NETWORKS=true
      shift
      ;;
    -a|--all)
      CLEAN_CONTAINERS=true
      CLEAN_IMAGES=true
      CLEAN_VOLUMES=true
      CLEAN_NETWORKS=true
      shift
      ;;
    -d|--dry-run)
      DRY_RUN=true
      shift
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

# --- Validation ---

if ! command -v docker &> /dev/null; then
  log_error "Docker is not installed. Please install Docker to use this script. Exiting."
  exit 1
fi

if [[ "$CLEAN_PROJECT" = true && "$CLEAN_GLOBAL" = true ]]; then
  log_error "Cannot use --project and --global simultaneously. Please choose one. Exiting."
  exit 1
fi

if [[ "$CLEAN_PROJECT" = false && "$CLEAN_GLOBAL" = false ]]; then
  log_error "No cleanup scope specified. Use --project or --global. Exiting."
  show_help
  exit 1
fi

if [[ "$CLEAN_CONTAINERS" = false && "$CLEAN_IMAGES" = false && \
      "$CLEAN_VOLUMES" = false && "$CLEAN_NETWORKS" = false ]]; then
  log_error "No resource type specified for cleanup. Use --containers, --images, --volumes, --networks, or --all. Exiting."
  show_help
  exit 1
fi

if [[ "$CLEAN_PROJECT" = true && ! -f "docker-compose.yml" ]]; then
  log_error "--project option requires a 'docker-compose.yml' file in the current directory. Exiting."
  exit 1
fi

# --- Main Cleanup Logic ---

if [[ "$DRY_RUN" = true ]]; then
  log_info "Performing DRY RUN. No resources will be deleted."
fi

if [[ "$CLEAN_PROJECT" = true ]]; then
  log_info "Cleaning up resources for the current Docker Compose project..."
  PROJECT_NAME=$(basename "$(pwd)") # Get current directory name as project name
  if docker compose ps -q &> /dev/null; then # Check if any containers are running
    log_warning "Some containers for project '$PROJECT_NAME' might be running. Consider stopping them first with 'docker compose down'."
  fi

  if [[ "$CLEAN_CONTAINERS" = true ]]; then
    log_info "Removing stopped containers for project '$PROJECT_NAME'ப்பான"
    if [[ "$DRY_RUN" = false ]]; then
      docker compose rm -s -f -v
    else
      log_info "(Dry Run) Would run: docker compose rm -s -f -v"
    fi
  fi

  if [[ "$CLEAN_VOLUMES" = true ]]; then
    log_info "Removing unused volumes for project '$PROJECT_NAME'ப்பான"
    if [[ "$DRY_RUN" = false ]]; then
      docker compose down --volumes --rmi local
    else
      log_info "(Dry Run) Would run: docker compose down --volumes --rmi local"
    fi
  fi

  # For project-specific images and networks, `docker compose down` with --rmi local handles images
  # and networks are removed by default with `docker compose down`
  if [[ "$CLEAN_IMAGES" = true ]]; then
    log_warning "Project-specific images are typically removed with 'docker compose down --rmi local'."
    log_warning "To remove dangling images, use the global cleanup option."
  fi
  if [[ "$CLEAN_NETWORKS" = true ]]; then
    log_warning "Project-specific networks are typically removed with 'docker compose down'."
    log_warning "To remove unused global networks, use the global cleanup option."
  fi

  log_success "Project cleanup process completed."

elif [[ "$CLEAN_GLOBAL" = true ]]; then
  log_info "Cleaning up unused Docker resources globally..."

  if [[ "$CLEAN_CONTAINERS" = true ]]; then
    log_info "Removing all stopped containers..."
    if [[ "$DRY_RUN" = false ]]; then
      docker container prune -f
    else
      log_info "(Dry Run) Would run: docker container prune -f"
    fi
  fi

  if [[ "$CLEAN_IMAGES" = true ]]; then
    log_info "Removing dangling images..."
    if [[ "$DRY_RUN" = false ]]; then
      docker image prune -f
    else
      log_info "(Dry Run) Would run: docker image prune -f"
    fi
  fi

  if [[ "$CLEAN_VOLUMES" = true ]]; then
    log_info "Removing unused volumes..."
    if [[ "$DRY_RUN" = false ]]; then
      docker volume prune -f
    else
      log_info "(Dry Run) Would run: docker volume prune -f"
    fi
  fi

  if [[ "$CLEAN_NETWORKS" = true ]]; then
    log_info "Removing unused networks..."
    if [[ "$DRY_RUN" = false ]]; then
      docker network prune -f
    else
      log_info "(Dry Run) Would run: docker network prune -f"
    fi
  fi

  if [[ "$CLEAN_CONTAINERS" = true && "$CLEAN_IMAGES" = true && \
        "$CLEAN_VOLUMES" = true && "$CLEAN_NETWORKS" = true ]]; then
    log_info "Running full system prune for comprehensive cleanup..."
    if [[ "$DRY_RUN" = false ]]; then
      docker system prune -f
    else
      log_info "(Dry Run) Would run: docker system prune -f"
    fi
  fi

  log_success "Global cleanup process completed."
fi

log_success "Cleanup script finished."
