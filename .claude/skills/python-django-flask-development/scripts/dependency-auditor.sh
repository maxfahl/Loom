#!/bin/bash

# dependency-auditor.sh
#
# This script automates the process of checking for outdated and vulnerable dependencies
# in a Python project. It integrates with tools like `pip-audit` and `safety` and can
# optionally update dependencies.
#
# Usage:
#   ./dependency-auditor.sh [options]
#
# Options:
#   --check-vulnerabilities  Run vulnerability checks using pip-audit and safety.
#   --update                 Upgrade all dependencies to their latest compatible versions.
#   --dry-run                Show what would be done without actually executing commands.
#   -h, --help               Display this help message.
#
# Examples:
#   ./dependency-auditor.sh --check-vulnerabilities
#   ./dependency-auditor.sh --update
#   ./dependency-auditor.sh --check-vulnerabilities --update
#   ./dependency-auditor.sh --dry-run --check-vulnerabilities
#
# Requirements:
#   - Python 3 and pip
#   - Project must have a requirements.txt or pyproject.toml (for Poetry).
#

# --- Colors for output ---
GREEN="\033[0;32m"
YELLOW="\033[0;33m"
RED="\033[0;31m"
BLUE="\033[0;34m"
NC="\033[0m" # No Color

# --- Helper Functions ---
log_success() { echo -e "${GREEN}✔ $1${NC}"; }
log_info() { echo -e "${BLUE}ℹ $1${NC}"; }
log_warning() { echo -e "${YELLOW}⚠ $1${NC}"; }
log_error() { echo -e "${RED}✖ $1${NC}"; exit 1; }

# --- Variables ---
CHECK_VULNERABILITIES=false
UPDATE_DEPENDENCIES=false
DRY_RUN=false

# --- Parse Arguments ---
while [[ $# -gt 0 ]]; do
    key="$1"
    case $key in
        --check-vulnerabilities)
        CHECK_VULNERABILITIES=true
        shift # past argument
        ;;
        --update)
        UPDATE_DEPENDENCIES=true
        shift # past argument
        ;;
        --dry-run)
        DRY_RUN=true
        shift # past argument
        ;;
        -h|--help)
        head -n 35 "$0" | grep "^#" | cut -c 3- # Display help from script header
        exit 0
        ;;
        *)
        log_error "Unknown option: $1"
        ;;
    esac
done

# --- Determine Python executable and package manager ---
PYTHON_EXEC="python3"
PIP_EXEC="pip"
POETRY_INSTALLED=false

if [ -d ".venv" ]; then
    if [ -f ".venv/bin/python" ]; then
        PYTHON_EXEC=".venv/bin/python"
        PIP_EXEC=".venv/bin/pip"
    elif [ -f ".venv/Scripts/python.exe" ]; then # Windows
        PYTHON_EXEC=".venv/Scripts/python.exe"
        PIP_EXEC=".venv/Scripts/pip"
    fi
    log_info "Using Python executable: $PYTHON_EXEC (from virtual environment)"
else
    log_warning "No virtual environment (.venv) found. Using system Python: $PYTHON_EXEC. Consider activating your venv."
fi

if command -v poetry &> /dev/null; then
    POETRY_INSTALLED=true
    log_info "Poetry detected. Will use Poetry for dependency management if pyproject.toml is found."
fi

# --- Check for requirements.txt or pyproject.toml ---
if [ -f "pyproject.toml" ] && $POETRY_INSTALLED; then
    PACKAGE_MANAGER="poetry"
    log_info "Detected pyproject.toml. Using Poetry for dependency management."
elif [ -f "requirements.txt" ]; then
    PACKAGE_MANAGER="pip"
    log_info "Detected requirements.txt. Using pip for dependency management."
else
    log_error "No requirements.txt or pyproject.toml found. Cannot proceed with dependency auditing/updating."
fi

# --- Install auditing tools if necessary ---
install_tool() {
    TOOL_NAME=$1
    INSTALL_CMD="$PIP_EXEC install $TOOL_NAME"
    if ! $PYTHON_EXEC -c "import $TOOL_NAME" &> /dev/null; then
        log_warning "$TOOL_NAME not found. Installing..."
        if $DRY_RUN; then
            log_info "(Dry run) $INSTALL_CMD"
        else
            $INSTALL_CMD || log_error "Failed to install $TOOL_NAME. Please install it manually: $INSTALL_CMD"
            log_success "$TOOL_NAME installed."
        fi
    fi
}

if $CHECK_VULNERABILITIES; then
    install_tool "pip-audit"
    install_tool "safety"
fi

# --- Perform actions ---
if $DRY_RUN; then
    log_warning "DRY RUN mode activated. No actual commands will be executed."
fi

if $CHECK_VULNERABILITIES; then
    log_info "Running vulnerability checks..."
    if [ "$PACKAGE_MANAGER" == "pip" ]; then
        if $DRY_RUN; then
            log_info "(Dry run) $PIP_EXEC freeze | pip-audit"
            log_info "(Dry run) $PIP_EXEC freeze | safety check --full-report --stdin"
        else
            log_info "Running pip-audit..."
            $PIP_EXEC freeze | pip-audit || log_warning "pip-audit found vulnerabilities or failed."
            log_info "Running safety check..."
            $PIP_EXEC freeze | safety check --full-report --stdin || log_warning "Safety found vulnerabilities or failed."
        fi
    elif [ "$PACKAGE_MANAGER" == "poetry" ]; then
        if $DRY_RUN; then
            log_info "(Dry run) poetry export --format=requirements.txt --without-hashes | pip-audit"
            log_info "(Dry run) poetry export --format=requirements.txt --without-hashes | safety check --full-report --stdin"
        else
            log_info "Running pip-audit (via poetry export)..."
            poetry export --format=requirements.txt --without-hashes | pip-audit || log_warning "pip-audit found vulnerabilities or failed."
            log_info "Running safety check (via poetry export)..."
            poetry export --format=requirements.txt --without-hashes | safety check --full-report --stdin || log_warning "Safety found vulnerabilities or failed."
        fi
    fi
    log_success "Vulnerability checks complete."
fi

if $UPDATE_DEPENDENCIES; then
    log_info "Updating dependencies..."
    if [ "$PACKAGE_MANAGER" == "pip" ]; then
        if [ ! -f "requirements.txt" ]; then
            log_error "requirements.txt not found. Cannot update pip dependencies."
        fi
        if $DRY_RUN; then
            log_info "(Dry run) $PIP_EXEC install --upgrade -r requirements.txt"
        else
            $PIP_EXEC install --upgrade -r requirements.txt || log_error "Failed to update pip dependencies."
            log_success "Pip dependencies updated."
        fi
    elif [ "$PACKAGE_MANAGER" == "poetry" ]; then
        if $DRY_RUN; then
            log_info "(Dry run) poetry update"
        else
            poetry update || log_error "Failed to update Poetry dependencies."
            log_success "Poetry dependencies updated."
        fi
    fi
fi

if ! $CHECK_VULNERABILITIES && ! $UPDATE_DEPENDENCIES; then
    log_warning "No action specified. Use --check-vulnerabilities or --update."
    head -n 35 "$0" | grep "^#" | cut -c 3-
    exit 1
fi

log_success "Dependency audit and update process finished."
