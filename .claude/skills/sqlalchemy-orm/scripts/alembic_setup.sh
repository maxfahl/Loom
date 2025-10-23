#!/bin/bash

# alembic_setup.sh
#
# Purpose:
#   Automates the initial setup of Alembic for a new or existing SQLAlchemy project.
#   This script initializes Alembic in the current directory (or a specified one)
#   and optionally generates the first migration script based on existing models.
#
# Usage:
#   ./alembic_setup.sh [OPTIONS]
#
# Options:
#   --directory <path>    Specify the directory to initialize Alembic in.
#                         Defaults to the current working directory.
#   --message <msg>       Message for the initial migration.
#                         Defaults to "Initial migration".
#   --models-path <path>  Path to the Python file containing SQLAlchemy models.
#                         Required for autogeneration.
#   --db-url <url>        Database URL for Alembic to connect to for autogeneration.
#                         e.g., "postgresql://user:password@host:port/dbname"
#                         Required for autogeneration.
#   --no-autogenerate     Skip the initial autogeneration of a migration script.
#   --help                Display this help message.
#
# Examples:
#   ./alembic_setup.sh --message "Create users and products tables" --models-path "app/models.py" --db-url "sqlite:///./test.db"
#   ./alembic_setup.sh --directory "migrations" --no-autogenerate
#
# Requirements:
#   - Alembic must be installed (pip install alembic)
#   - SQLAlchemy must be installed (pip install sqlalchemy)
#   - The Python file specified by --models-path must be importable and contain
#     your SQLAlchemy Base and models.
#   - The database specified by --db-url must be accessible.

# --- Configuration ---
ALEMBIC_DIR="alembic"
MESSAGE="Initial migration"
MODELS_PATH=""
DB_URL=""
AUTOGENERATE=true

# --- Helper Functions ---
print_help() {
    grep "^# " "$0" | cut -c 3-
    exit 0
}

log_info() {
    echo -e "\033[0;34m[INFO]\033[0m $1"
}

log_success() {
    echo -e "\033[0;32m[SUCCESS]\033[0m $1"
}

log_error() {
    echo -e "\033[0;31m[ERROR]\033[0m $1" >&2
    exit 1
}

# --- Parse Arguments ---
while [[ "$#" -gt 0 ]]; do
    case "$1" in
        --directory)
            ALEMBIC_DIR="$2"
            shift
            ;;
        --message)
            MESSAGE="$2"
            shift
            ;;
        --models-path)
            MODELS_PATH="$2"
            shift
            ;;
        --db-url)
            DB_URL="$2"
            shift
            ;;
        --no-autogenerate)
            AUTOGENERATE=false
            ;;
        --help)
            print_help
            ;;
        *)
            log_error "Unknown option: $1. Use --help for usage."
            ;;
    esac
    shift
done

# --- Main Logic ---

# 1. Check for Alembic installation
if ! command -v alembic &> /dev/null; then
    log_error "Alembic is not installed. Please install it using 'pip install alembic'."
fi

# 2. Initialize Alembic environment
if [ ! -d "$ALEMBIC_DIR" ]; then
    log_info "Initializing Alembic environment in '$ALEMBIC_DIR'..."
    alembic init "$ALEMBIC_DIR" || log_error "Failed to initialize Alembic."
    log_success "Alembic environment initialized."
else
    log_info "Alembic environment already exists in '$ALEMBIC_DIR'."
fi

# 3. Configure env.py for autogeneration if models-path and db-url are provided
if $AUTOGENERATE; then
    if [ -z "$MODELS_PATH" ] || [ -z "$DB_URL" ]; then
        log_error "Both --models-path and --db-url are required for autogeneration. Use --no-autogenerate to skip."
    fi

    ENV_PY="$ALEMBIC_DIR/env.py"
    if [ ! -f "$ENV_PY" ]; then
        log_error "Alembic env.py not found at '$ENV_PY'."
    fi

    log_info "Configuring '$ENV_PY' for autogeneration..."

    # Backup original env.py
    cp "$ENV_PY" "${ENV_PY}.bak"

    # Replace target_metadata and import models
    # This is a simplified replacement. For complex setups, manual editing might be needed.
    sed -i '' "s/^# from myapp import mymodel$/from $(dirname "${MODELS_PATH}") import $(basename "${MODELS_PATH%.*}") as models/" "$ENV_PY"
    sed -i '' "s/^# target_metadata = mymodel.Base.metadata$/target_metadata = models.Base.metadata/" "$ENV_PY"
    sed -i '' "s/^# config.set_main_option('sqlalchemy.url', 'sqlite:\/\/\/path\/to\/database.db')$/config.set_main_option('sqlalchemy.url', '$DB_URL')/" "$ENV_PY"
    sed -i '' "s/^# from sqlalchemy import engine_from_config$/from sqlalchemy import engine_from_config/" "$ENV_PY"
    sed -i '' "s/^# from sqlalchemy import pool$/from sqlalchemy import pool/" "$ENV_PY"
    sed -i '' "s/^# from logging.config import fileConfig$/from logging.config import fileConfig/" "$ENV_PY"

    log_success "'$ENV_PY' configured. Please review it for correctness, especially the model import and target_metadata."

    # 4. Generate initial migration
    log_info "Generating initial migration with message: \"$MESSAGE\"..."
    alembic -c "$ALEMBIC_DIR/alembic.ini" revision --autogenerate -m "$MESSAGE" || log_error "Failed to autogenerate migration."
    log_success "Initial migration generated successfully."
else
    log_info "Skipping autogeneration as --no-autogenerate was specified."
fi

log_success "Alembic setup complete. Remember to review generated files and env.py."
