#!/bin/bash

# docker-prune-all.sh
# Description: Safely cleans up all unused Docker resources (stopped containers, dangling images, unused volumes, networks).
# Usage: ./docker-prune-all.sh [--dry-run]

# --- Helper Functions ---
COLOR_RED="\033[0;31m"
COLOR_GREEN="\033[0;32m"
COLOR_YELLOW="\033[0;33m"
COLOR_BLUE="\033[0;34m"
COLOR_NC="\033[0m" # No Color

print_info() { echo -e "${COLOR_BLUE}[INFO]${COLOR_NC} $1"; }
print_success() { echo -e "${COLOR_GREEN}[SUCCESS]${COLOR_NC} $1"; }
print_warning() { echo -e "${COLOR_YELLOW}[WARNING]${COLOR_NC} $1"; }
print_error() { echo -e "${COLOR_RED}[ERROR]${COLOR_NC} $1"; }

show_help() {
  echo "Usage: $0 [--dry-run]"
  echo ""
  echo "Safely cleans up all unused Docker resources (stopped containers, dangling images, unused volumes, networks)."
  echo ""
  echo "Arguments:"
  echo "  --dry-run   (Optional) Show what would be removed without actually removing anything."
  echo ""
  echo "Examples:"
  echo "  $0             # Perform actual cleanup"
  echo "  $0 --dry-run   # See what would be cleaned up"
  exit 0
}

# --- Main Logic ---

DRY_RUN=false
if [ "$1" == "--dry-run" ]; then
  DRY_RUN=true
  print_info "Dry run enabled. No resources will be removed."
elif [ -n "$1" ]; then
  print_error "Unknown argument: $1"
  show_help
fi

print_info "Starting Docker resource cleanup..."

# Function to execute prune command
execute_prune() {
  local command_desc="$1"
  local prune_command="$2"

  print_info "Checking for $command_desc..."
  if $DRY_RUN; then
    print_info "Dry run: Would execute: docker $prune_command"
    # For dry run, we can try to list what *would* be pruned
    case "$prune_command" in
      "container prune -f") docker ps -a -f status=exited -q | xargs -r docker inspect --format '{{.Name}} ({{.ID}})'
                            ;;
      "image prune -f") docker images -f dangling=true -q | xargs -r docker inspect --format '{{.RepoTags}} ({{.ID}})'
                         ;;
      "volume prune -f") docker volume ls -f dangling=true -q | xargs -r docker volume inspect --format '{{.Name}}'
                          ;;
      "network prune -f") docker network ls -f dangling=true -q | xargs -r docker network inspect --format '{{.Name}}'
                           ;;
      *)
        # Fallback for other prune commands if needed
        ;;
    esac
  else
    print_info "Executing: docker $prune_command"
    docker $prune_command
    if [ $? -eq 0 ]; then
      print_success "$command_desc cleanup complete."
    else
      print_error "$command_desc cleanup failed."
    fi
  fi
}

# Prune stopped containers
execute_prune "stopped containers" "container prune -f"

# Prune dangling images (images not associated with any container)
execute_prune "dangling images" "image prune -f"

# Prune unused volumes (volumes not used by any container)
# WARNING: This can remove data. User should be aware.
print_warning "WARNING: Volume pruning can remove persistent data. Ensure no important data is in unused volumes."
execute_prune "unused volumes" "volume prune -f"

# Prune unused networks
execute_prune "unused networks" "network prune -f"

print_info "Docker resource cleanup process finished."
if $DRY_RUN; then
  print_info "To perform actual cleanup, run without --dry-run: $0"
fi
