#!/bin/bash

# check-outdated-deps.sh
#
# Description:
#   Checks for outdated Rust dependencies in the current project using `cargo outdated`.
#   Provides a summary of outdated dependencies and suggests commands to update them.
#
# Usage:
#   ./check-outdated-deps.sh [--update-all] [--dry-run]
#
# Options:
#   --update-all : Automatically updates all outdated dependencies to their latest compatible versions.
#   --dry-run    : Shows what would be updated without actually performing the updates.
#   --help       : Display this help message.
#
# Examples:
#   ./check-outdated-deps.sh
#   ./check-outdated-deps.sh --update-all
#   ./check-outdated-deps.sh --dry-run
#
# Prerequisites:
#   - `cargo-outdated` must be installed: `cargo install cargo-outdated`
#
# Error Handling:
#   - Exits if `cargo-outdated` is not installed.
#   - Exits if not run in a Cargo project directory.
#
# Configuration:
#   None directly, relies on `cargo-outdated` configuration.

set -e # Exit immediately if a command exits with a non-zero status.

# --- Helper Functions ---
print_help() {
    echo "Usage: $0 [--update-all] [--dry-run]"
    echo ""
    echo "Options:"
    echo "  --update-all : Automatically updates all outdated dependencies to their latest compatible versions."
    echo "  --dry-run    : Shows what would be updated without actually performing the updates."
    echo "  --help       : Display this help message."
    echo ""
    echo "Examples:"
    echo "  $0"
    echo "  $0 --update-all"
    echo "  $0 --dry-run"
    echo ""
    echo "Prerequisites:"
    echo "  - `cargo-outdated` must be installed: `cargo install cargo-outdated`"
    exit 0
}

log_info() {
    echo -e "\033[0;34mINFO: $1\033[0m" # Blue color
}

log_success() {
    echo -e "\033[0;32mSUCCESS: $1\033[0m" # Green color
}

log_warning() {
    echo -e "\033[0;33mWARNING: $1\033[0m" # Yellow color
}

log_error() {
    echo -e "\033[0;31mERROR: $1\033[0m" # Red color
    exit 1
}

# --- Argument Parsing ---
UPDATE_ALL=false
DRY_RUN=false

for arg in "$@"; do
    case $arg in
        --update-all)
            UPDATE_ALL=true
            shift
            ;;
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        --help)
            print_help
            ;;
        *)
            log_error "Unknown option: $arg"
            print_help
            ;;
    esac
done

# --- Pre-requisite Checks ---
if ! command -v cargo-outdated &> /dev/null; then
    log_error "`cargo-outdated` is not installed. Please install it using: cargo install cargo-outdated"
fi

if [ ! -f "Cargo.toml" ]; then
    log_error "Not a Cargo project. Please run this script from the root of a Rust project (where Cargo.toml is located)."
fi

log_info "Checking for outdated dependencies..."

if [ "$DRY_RUN" = true ]; then
    log_info "Dry run mode: Showing potential updates without applying them."
    cargo outdated --workspace --exit-code 0
    log_success "Dry run complete. No changes were applied."
elif [ "$UPDATE_ALL" = true ]; then
    log_info "Updating all outdated dependencies..."
    cargo update
    log_success "All dependencies updated to their latest compatible versions."
    log_info "It is recommended to run `cargo outdated` again to see if any transitive dependencies are still outdated or if newer incompatible versions are available."
else
    # Default behavior: just list outdated dependencies
    cargo outdated --workspace || log_warning "Some dependencies are outdated. Consider running with --update-all or manually updating."
    log_info "To update dependencies, run `cargo update` or `cargo outdated --update` for specific updates."
fi

log_success "Dependency check complete."
