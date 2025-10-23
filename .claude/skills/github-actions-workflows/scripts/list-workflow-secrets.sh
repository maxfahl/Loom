#!/bin/bash

# list-workflow-secrets.sh
#
# Purpose:
#   Lists GitHub repository secrets for a given repository.
#   This helps developers quickly review available secrets without navigating
#   the GitHub UI, which is useful for managing workflow configurations.
#
# Usage:
#   ./list-workflow-secrets.sh <owner/repo> [--dry-run]
#
# Arguments:
#   <owner/repo> : The GitHub repository in "owner/repo" format (e.g., "octocat/Spoon-Knife").
#   --dry-run    : Optional. If present, the script will only print the 'gh'
#                  command that would be executed without actually running it.
#
# Example:
#   ./list-workflow-secrets.sh myorg/my-repo
#   ./list-workflow-secrets.sh octocat/Spoon-Knife --dry-run
#
# Configuration:
#   - Requires the GitHub CLI ('gh') to be installed and authenticated.
#     Installation instructions: https://cli.github.com/
#     Authentication: `gh auth login`
#
# Error Handling:
#   - Exits if 'gh' CLI is not found.
#   - Exits if no repository is provided.
#   - Reports any errors from the 'gh' command.

set -euo pipefail

# --- Colors for better readability ---
GREEN='[0;32m'
YELLOW='[0;33m'
RED='[0;31m'
BLUE='[0;34m'
NC='[0m' # No Color

# --- Functions ---

log_info() {
  echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
  echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
  echo -e "${RED}[ERROR]${NC} $1" >&2
  exit 1
}

# --- Main Script Logic ---

REPO_NAME=""
DRY_RUN=false

# Parse arguments
for arg in "$@"; do
  case $arg in
    --dry-run)
      DRY_RUN=true
      shift
      ;; 
    *)
      if [[ -z "$REPO_NAME" ]]; then
        REPO_NAME="$arg"
      else
        log_error "Unknown argument or multiple repositories provided: $arg"
      fi
      shift
      ;; 
  esac
done

if [[ -z "$REPO_NAME" ]]; then
  log_error "Usage: $0 <owner/repo> [--dry-run]"
fi

# Validate gh CLI installation
if ! command -v gh &> /dev/null; then
  log_error "GitHub CLI ('gh') is not installed or not found in PATH. Please install it: https://cli.github.com/"
fi

log_info "Listing GitHub repository secrets for: '$REPO_NAME'"
if "$DRY_RUN"; then
  log_warn "Dry run enabled. Command will be printed but not executed."
fi

GH_SECRETS_CMD="gh secret list --repo $REPO_NAME"

if "$DRY_RUN"; then
  log_info "Would execute: $GH_SECRETS_CMD"
else
  if ! eval "$GH_SECRETS_CMD"; then
    log_error "Failed to list secrets for '$REPO_NAME'. Ensure you have access and are authenticated with 'gh auth login'."
  fi
  log_info "Successfully listed secrets for '$REPO_NAME'."
fi
