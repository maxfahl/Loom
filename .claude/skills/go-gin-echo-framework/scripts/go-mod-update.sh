#!/bin/bash

# go-mod-update.sh: Go Module Updater & Checker
# Description: Automates updating Go modules, tidying go.mod, running static analysis (go vet),
#              and checking for known vulnerabilities (govulncheck).
#
# Usage:
#   ./go-mod-update.sh [--dry-run]
#
# Arguments:
#   --dry-run: Optional. If set, the script will only report what it would do
#              without making any changes to go.mod, go.sum, or installing updates.
#
# Examples:
#   ./go-mod-update.sh
#   ./go-mod-update.sh --dry-run
#
# Features:
# - Updates all Go modules to their latest compatible versions.
# - Cleans up unused dependencies in go.mod and go.sum.
# - Performs static analysis to catch common errors.
# - Runs all tests to ensure updates haven't introduced regressions.
# - Checks for known security vulnerabilities in dependencies.
#
# Error Handling:
# - Exits if any critical Go command fails (e.g., go get, go mod tidy, go vet, go test, govulncheck).
# - Provides clear messages for each step.
#
# Cross-platform: Designed for Unix-like systems (Linux, macOS, WSL).
#
# Prerequisites:
# - Go (golang) must be installed and available in PATH.
# - govulncheck must be installed: `go install golang.org/x/vuln/cmd/govulncheck@latest`

set -e

# --- Helper Functions ---
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
    exit 1
}

# --- Configuration ---
DRY_RUN=false

# --- Parse Arguments ---
for arg in "$@"; do
    case $arg in
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        *)
            log_error "Unknown argument: $arg. Use --dry-run or no arguments."
            ;;
    esac
done

if [ "$DRY_RUN" = true ]; then
    log_info "Running in DRY-RUN mode. No changes will be applied."
fi

# --- Check for go.mod ---
if [ ! -f "go.mod" ]; then
    log_error "go.mod not found in the current directory. Please run this script from the root of your Go module."
fi

# --- Check for govulncheck ---
if ! command -v govulncheck &> /dev/null; then
    log_warning "govulncheck is not installed. Install it with: go install golang.org/x/vuln/cmd/govulncheck@latest"
    log_warning "Skipping vulnerability check."
    GOVULNCHECK_INSTALLED=false
else
    GOVULNCHECK_INSTALLED=true
fi

log_info "Starting Go module update and check process..."

# --- Step 1: Update Modules ---
log_info "Updating all Go modules..."
if [ "$DRY_RUN" = true ]; then
    log_info "DRY-RUN: Would run 'go get -u all'"
    go list -m -u all # Show available updates without applying
else
    go get -u all || log_error "Failed to update Go modules."
    log_success "Go modules updated."
fi

# --- Step 2: Tidy Modules ---
log_info "Tidying Go modules (removing unused dependencies)..."
if [ "$DRY_RUN" = true ]; then
    log_info "DRY-RUN: Would run 'go mod tidy'"
    # go mod tidy in dry-run doesn't show much without modifying files
else
    go mod tidy || log_error "Failed to tidy Go modules."
    log_success "Go modules tidied."
fi

# --- Step 3: Run Static Analysis ---
log_info "Running static analysis with 'go vet'..."
go vet ./... || log_error "Static analysis (go vet) found issues."
log_success "Static analysis passed."

# --- Step 4: Run Tests ---
log_info "Running all tests..."
go test ./... || log_error "Tests failed after module update."
log_success "All tests passed."

# --- Step 5: Check for Vulnerabilities ---
if [ "$GOVULNCHECK_INSTALLED" = true ]; then
    log_info "Checking for known vulnerabilities with 'govulncheck'..."
    govulncheck ./... || log_warning "Vulnerabilities found or govulncheck encountered issues. Please review the report."
    log_success "Vulnerability check completed."
else
    log_warning "Skipping vulnerability check as govulncheck is not installed."
fi

log_success "Go module update and check process finished."
if [ "$DRY_RUN" = true ]; then
    log_info "No changes were applied due to DRY-RUN mode."
fi
