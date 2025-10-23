#!/bin/bash

# db-migration-helper.sh
#
# This script simplifies database migration workflows for both Django and Flask (using Flask-Migrate).
# It handles environment variable loading and provides options for creating, applying, or rolling back migrations.
#
# Usage:
#   ./db-migration-helper.sh [options]
#
# Options:
#   --framework <django|flask>  Specify the framework (auto-detects if not provided).
#   --action <makemigrations|migrate|rollback|init|upgrade|downgrade>  Specify the migration action.
#                                 - Django: makemigrations, migrate, rollback (to a specific migration name/number)
#                                 - Flask: init, migrate, upgrade, downgrade (to a specific migration name/number)
#   --name <migration_name>     For Django makemigrations or Flask migrate, provide a name for the migration.
#   --target <migration_target> For rollback/downgrade, specify the migration name/number to revert to.
#   --dry-run                   Show what would be done without actually executing commands.
#   -h, --help                  Display this help message.
#
# Examples:
#   ./db-migration-helper.sh --framework django --action makemigrations --name "AddUserProfile"
#   ./db-migration-helper.sh --action migrate # Auto-detect framework, apply all pending migrations
#   ./db-migration-helper.sh --framework flask --action migrate -n "AddUserTable"
#   ./db-migration-helper.sh --framework flask --action upgrade
#   ./db-migration-helper.sh --framework django --action rollback --target "0001_initial"
#   ./db-migration-helper.sh --framework flask --action downgrade --target "base"
#
# Requirements:
#   - Python 3 and pip
#   - For Django: Django installed, manage.py in project root.
#   - For Flask: Flask, Flask-SQLAlchemy, Flask-Migrate installed, run.py in project root.
#   - python-dotenv (will be installed if not present) for .env loading.

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
FRAMEWORK=""
ACTION=""
MIGRATION_NAME=""
MIGRATION_TARGET=""
DRY_RUN=false

# --- Parse Arguments ---
while [[ $# -gt 0 ]]; do
    key="$1"
    case $key in
        --framework)
        FRAMEWORK="$2"
        shift # past argument
        shift # past value
        ;;
        --action)
        ACTION="$2"
        shift # past argument
        shift # past value
        ;;
        --name)
        MIGRATION_NAME="$2"
        shift # past argument
        shift # past value
        ;;
        --target)
        MIGRATION_TARGET="$2"
        shift # past argument
        shift # past value
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

# --- Auto-detect Framework ---
if [ -z "$FRAMEWORK" ]; then
    if [ -f "manage.py" ]; then
        FRAMEWORK="django"
        log_info "Framework auto-detected: Django"
    elif [ -f "run.py" ] && [ -d "app" ]; then
        FRAMEWORK="flask"
        log_info "Framework auto-detected: Flask"
    else
        log_error "Could not auto-detect framework. Please specify with --framework <django|flask>."
    fi
fi

# --- Validate Framework and Action ---
if [ "$FRAMEWORK" != "django" ] && [ "$FRAMEWORK" != "flask" ]; then
    log_error "Invalid framework specified: $FRAMEWORK. Must be 'django' or 'flask'."
fi

if [ -z "$ACTION" ]; then
    log_error "No action specified. Use --action <makemigrations|migrate|rollback|init|upgrade|downgrade>."
fi

# --- Check for python-dotenv and install if missing ---
if ! python3 -c "import dotenv" &> /dev/null; then
    log_warning "python-dotenv not found. Installing..."
    if $DRY_RUN; then
        log_info "(Dry run) pip install python-dotenv"
    else
        pip install python-dotenv || log_error "Failed to install python-dotenv. Please install it manually: pip install python-dotenv"
        log_success "python-dotenv installed."
    fi
fi

# --- Load .env file ---
if [ -f ".env" ]; then
    log_info "Loading environment variables from .env file..."
    if $DRY_RUN; then
        log_info "(Dry run) Source .env"
    else
        # Use python-dotenv to load .env variables into the current shell session
        # This is a bit tricky with bash, a common way is to parse it.
        # For simplicity, we'll just source it if it's a simple key=value file.
        # A more robust solution would be to use `python -c 'import dotenv; print(dotenv.main.dotenv_values())'`
        # and then export each variable.
        # For now, assuming simple .env format.
        set -a # automatically export all variables
        source .env
        set +a
        log_success "Environment variables loaded."
    fi
else
    log_warning "No .env file found. Proceeding without loading environment variables."
fi

# --- Determine Python executable ---
PYTHON_EXEC="python3"
if [ -d ".venv" ]; then
    if [ -f ".venv/bin/python" ]; then
        PYTHON_EXEC=".venv/bin/python"
    elif [ -f ".venv/Scripts/python.exe" ]; then # Windows
        PYTHON_EXEC=".venv/Scripts/python.exe"
    fi
    log_info "Using Python executable: $PYTHON_EXEC (from virtual environment)"
else
    log_warning "No virtual environment (.venv) found. Using system Python: $PYTHON_EXEC. Consider activating your venv."
fi

# --- Execute Migration Commands ---
if [ "$FRAMEWORK" == "django" ]; then
    case $ACTION in
        makemigrations)
            CMD="$PYTHON_EXEC manage.py makemigrations"
            [ -n "$MIGRATION_NAME" ] && CMD="$CMD $MIGRATION_NAME"
            log_info "Running Django makemigrations..."
            if $DRY_RUN; then log_info "(Dry run) $CMD"; else $CMD || log_error "Django makemigrations failed."; fi
            log_success "Django makemigrations complete."
            ;;
        migrate)
            CMD="$PYTHON_EXEC manage.py migrate"
            log_info "Running Django migrate..."
            if $DRY_RUN; then log_info "(Dry run) $CMD"; else $CMD || log_error "Django migrate failed."; fi
            log_success "Django migrate complete."
            ;;
        rollback)
            if [ -z "$MIGRATION_TARGET" ]; then
                log_error "For Django rollback, --target <migration_name_or_number> is required."
            fi
            CMD="$PYTHON_EXEC manage.py migrate --fake $MIGRATION_TARGET"
            log_info "Running Django rollback to $MIGRATION_TARGET..."
            if $DRY_RUN; then log_info "(Dry run) $CMD"; else $CMD || log_error "Django rollback failed."; fi
            log_success "Django rollback to $MIGRATION_TARGET complete. Note: This only fakes the migration state. You might need to manually revert database changes."
            ;;
        *)
            log_error "Invalid action for Django: $ACTION. Supported actions: makemigrations, migrate, rollback."
            ;;
    esac
elif [ "$FRAMEWORK" == "flask" ]; then
    case $ACTION in
        init)
            CMD="$PYTHON_EXEC -m flask db init"
            log_info "Running Flask-Migrate init..."
            if $DRY_RUN; then log_info "(Dry run) $CMD"; else $CMD || log_error "Flask-Migrate init failed."; fi
            log_success "Flask-Migrate init complete."
            ;;
        migrate)
            CMD="$PYTHON_EXEC -m flask db migrate"
            [ -n "$MIGRATION_NAME" ] && CMD="$CMD -m \"$MIGRATION_NAME\""
            log_info "Running Flask-Migrate migrate..."
            if $DRY_RUN; then log_info "(Dry run) $CMD"; else $CMD || log_error "Flask-Migrate migrate failed."; fi
            log_success "Flask-Migrate migrate complete."
            ;;
        upgrade)
            CMD="$PYTHON_EXEC -m flask db upgrade"
            log_info "Running Flask-Migrate upgrade..."
            if $DRY_RUN; then log_info "(Dry run) $CMD"; else $CMD || log_error "Flask-Migrate upgrade failed."; fi
            log_success "Flask-Migrate upgrade complete."
            ;;
        downgrade)
            if [ -z "$MIGRATION_TARGET" ]; then
                log_error "For Flask downgrade, --target <migration_name_or_number> is required (e.g., 'base' for initial state)."
            fi
            CMD="$PYTHON_EXEC -m flask db downgrade $MIGRATION_TARGET"
            log_info "Running Flask-Migrate downgrade to $MIGRATION_TARGET..."
            if $DRY_RUN; then log_info "(Dry run) $CMD"; else $CMD || log_error "Flask-Migrate downgrade failed."; fi
            log_success "Flask-Migrate downgrade to $MIGRATION_TARGET complete."
            ;;
        *)
            log_error "Invalid action for Flask: $ACTION. Supported actions: init, migrate, upgrade, downgrade."
            ;;
    esac
fi
