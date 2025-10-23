#!/bin/bash

# api-version-migrator.sh: Assists with API versioning tasks.
#
# This script helps in creating new API versions by:
# 1. Creating a new version directory (e.g., v2, v3).
# 2. Optionally copying files from a previous version as a starting point.
# 3. Providing guidance on updating routing configurations.
#
# Usage:
#   ./api-version-migrator.sh [OPTIONS]
#
# Options:
#   --new-version <version>   Required: The new API version to create (e.g., 'v2', 'v3').
#   --base-path <path>        Required: The base directory where API versions are located
#                             (e.g., 'src/api', 'routes').
#   --copy-from <version>     Optional: The existing API version to copy files from
#                             (e.g., 'v1'). If not provided, an empty directory is created.
#   --dry-run                 Print the actions that would be taken without
#                             actually creating or modifying files.
#   --help                    Show this help message and exit.
#
# Example:
#   ./api-version-migrator.sh --new-version v2 --base-path src/api --copy-from v1
#   ./api-version-migrator.sh --new-version v3 --base-path routes
#   ./api-version-migrator.sh --new-version v2 --base-path src/api --dry-run

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

NEW_VERSION=""
BASE_PATH=""
COPY_FROM_VERSION=""
DRY_RUN=false

# Parse arguments
while (( "$#" )); do
  case "$1" in
    --new-version)
      NEW_VERSION="$2"
      shift 2
      ;;
    --base-path)
      BASE_PATH="$2"
      shift 2
      ;;
    --copy-from)
      COPY_FROM_VERSION="$2"
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
if [ -z "$NEW_VERSION" ]; then
  print_error "Error: --new-version is required."
  show_help
  exit 1
fi

if [ -z "$BASE_PATH" ]; then
  print_error "Error: --base-path is required."
  show_help
  exit 1
fi

NEW_VERSION_DIR="${BASE_PATH}/${NEW_VERSION}"

print_info "Starting API version migration for new version: ${NEW_VERSION}"
if [ "$DRY_RUN" = true ]; then
  print_warning "Running in DRY-RUN mode. No files will be created or modified."
fi

# 1. Create new version directory
if [ -d "$NEW_VERSION_DIR" ]; then
  print_warning "Directory '${NEW_VERSION_DIR}' already exists. Skipping creation."
else
  if [ "$DRY_RUN" = true ]; then
    print_info "Would create directory: ${NEW_VERSION_DIR}"
  else
    mkdir -p "$NEW_VERSION_DIR"
    if [ $? -eq 0 ]; then
      print_success "Created directory: ${NEW_VERSION_DIR}"
    else
      print_error "Failed to create directory: ${NEW_VERSION_DIR}"
      exit 1
    fi
  fi
fi

# 2. Optionally copy files from a previous version
if [ -n "$COPY_FROM_VERSION" ]; then
  FROM_VERSION_DIR="${BASE_PATH}/${COPY_FROM_VERSION}"
  if [ ! -d "$FROM_VERSION_DIR" ]; then
    print_error "Error: Source version directory '${FROM_VERSION_DIR}' does not exist. Cannot copy files."
    exit 1
  fi

  print_info "Copying files from '${FROM_VERSION_DIR}' to '${NEW_VERSION_DIR}'"
  if [ "$DRY_RUN" = true ]; then
    print_info "Would copy contents of '${FROM_VERSION_DIR}' to '${NEW_VERSION_DIR}'"
  else
    cp -R "${FROM_VERSION_DIR}"/* "${NEW_VERSION_DIR}"/
    if [ $? -eq 0 ]; then
      print_success "Copied files from '${FROM_VERSION_DIR}' to '${NEW_VERSION_DIR}'"
    else
      print_error "Failed to copy files from '${FROM_VERSION_DIR}'"
      exit 1
    fi
  fi
else
  print_info "No --copy-from version specified. Creating empty new version directory."
fi

# 3. Guidance on updating routing configurations
print_info "\n--- Next Steps: Manual Configuration Update ---"
print_info "1. Update your main API router/gateway to include the new version's routes."
print_info "   Example (Express.js):"
print_info "     app.use('/api/${NEW_VERSION}', ${NEW_VERSION}_router);"
print_info "   Example (Django):"
print_info "     path('api/${NEW_VERSION}/', include('app_name.${NEW_VERSION}.urls')),"
print_info "2. Review and update any base URLs or version references in your client applications."
print_info "3. Make necessary code changes within '${NEW_VERSION_DIR}' to implement new features or breaking changes."
print_info "4. Update API documentation (e.g., OpenAPI spec) for the new version."

print_success "API version migration script finished."
