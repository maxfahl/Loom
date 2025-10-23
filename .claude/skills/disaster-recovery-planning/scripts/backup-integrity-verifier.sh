#!/bin/bash

# backup-integrity-verifier.sh: Automates the process of restoring a small sample of data
# from the latest backup and verifying its integrity. This script is designed to be
# run periodically to ensure that backups are valid and recoverable.
#
# Features:
# - Restores a specified backup to a temporary location.
# - Performs basic integrity checks (e.g., file existence, checksums, database connectivity).
# - Cleans up temporary restoration files.
# - Supports dry-run mode.
#
# Usage:
#   ./backup-integrity-verifier.sh [OPTIONS]
#
# Options:
#   -b, --backup-path <PATH>    Required. Path to the backup file or directory to verify.
#   -t, --temp-dir <PATH>       Optional. Temporary directory for restoration. Defaults to /tmp/dr_verify.
#   -c, --checksum-file <PATH>  Optional. Path to a checksum file (e.g., SHA256SUMS) within the backup
#                               to verify against restored files.
#   -d, --db-check <TYPE>       Optional. Perform a database connectivity check. TYPE can be 'postgres' or 'mysql'.
#   -u, --db-user <USER>        Optional. Database user for connectivity check.
#   -p, --db-pass <PASS>        Optional. Database password for connectivity check.
#   -n, --db-name <NAME>        Optional. Database name for connectivity check.
#   -h, --db-host <HOST>        Optional. Database host for connectivity check. Defaults to localhost.
#   --dry-run                   Perform a dry run without actual restoration or cleanup.
#   --help                      Display this help message.
#
# Examples:
#   ./backup-integrity-verifier.sh -b /mnt/backups/app_data_2025-10-18.tar.gz
#   ./backup-integrity-verifier.sh -b /mnt/backups/db_dump.sql -d postgres -u admin -p secret -n app_db
#   ./backup-integrity-verifier.sh -b /mnt/backups/my_app_backup.zip --checksum-file manifest/SHA256SUMS
#   ./backup-integrity-verifier.sh -b /mnt/backups/latest.tar.gz --dry-run

set -euo pipefail

# --- Configuration ----
BACKUP_PATH=""
TEMP_DIR="/tmp/dr_verify_$(date +%Y%m%d%H%M%S)"
CHECKSUM_FILE=""
DB_CHECK_TYPE=""
DB_USER=""
DB_PASS=""
DB_NAME=""
DB_HOST="localhost"
DRY_RUN=0

# --- Helper Functions ---
log_info()    { echo -e "\033[0;34m[INFO]\033[0m $1"; }
log_success() { echo -e "\033[0;32m[SUCCESS]\033[0m $1"; }
log_warn()    { echo -e "\033[0;33m[WARN]\033[0m $1"; }
log_error()   { echo -e "\033[0;31m[ERROR]\033[0m $1" >&2; exit 1; }

print_help() {
    grep '^# ' "$0" | sed -e 's/^# //g' -e 's/^#$//g'
    exit 0
}

cleanup() {
    if [ "$DRY_RUN" -eq 1 ]; then
        log_info "Dry run: Skipping cleanup of $TEMP_DIR"
        return
    fi
    if [ -d "$TEMP_DIR" ]; then
        log_info "Cleaning up temporary directory: $TEMP_DIR"
        rm -rf "$TEMP_DIR"
    fi
}

# --- Argument Parsing ---
while [[ $# -gt 0 ]]; do
    key="$1"
    case $key in
        -b|--backup-path)
        BACKUP_PATH="$2"
        shift # past argument
        shift # past value
        ;;
        -t|--temp-dir)
        TEMP_DIR="$2"
        shift # past argument
        shift # past value
        ;;
        -c|--checksum-file)
        CHECKSUM_FILE="$2"
        shift # past argument
        shift # past value
        ;;
        -d|--db-check)
        DB_CHECK_TYPE="$2"
        shift # past argument
        shift # past value
        ;;
        -u|--db-user)
        DB_USER="$2"
        shift # past argument
        shift # past value
        ;;
        -p|--db-pass)
        DB_PASS="$2"
        shift # past argument
        shift # past value
        ;;
        -n|--db-name)
        DB_NAME="$2"
        shift # past argument
        shift # past value
        ;;
        -h|--db-host)
        DB_HOST="$2"
        shift # past argument
        shift # past value
        ;;
        --dry-run)
        DRY_RUN=1
        shift # past argument
        ;;
        --help)
        print_help
        ;;
        *)
        log_error "Unknown option: $1"
        ;;
    esac
done

# --- Validation ---
if [ -z "$BACKUP_PATH" ]; then
    log_error "Error: --backup-path is required. Use --help for usage."
fi

if [ ! -f "$BACKUP_PATH" ] && [ ! -d "$BACKUP_PATH" ]; then
    log_error "Error: Backup path '$BACKUP_PATH' does not exist."
fi

if [ -n "$DB_CHECK_TYPE" ]; then
    if [ -z "$DB_USER" ] || [ -z "$DB_NAME" ]; then
        log_error "Error: --db-user and --db-name are required for database checks."
    fi
    if [ "$DB_CHECK_TYPE" != "postgres" ] && [ "$DB_CHECK_TYPE" != "mysql" ]; then
        log_error "Error: Invalid --db-check type. Must be 'postgres' or 'mysql'."
    fi
fi

# --- Main Logic ---
log_info "Starting backup integrity verification for: $BACKUP_PATH"
log_info "Temporary restoration directory: $TEMP_DIR"

if [ "$DRY_RUN" -eq 1 ]; then
    log_info "Dry run enabled. No actual restoration or cleanup will occur."
fi

# Ensure cleanup is called on exit
trap cleanup EXIT

if [ "$DRY_RUN" -eq 0 ]; then
    log_info "Creating temporary directory: $TEMP_DIR"
    mkdir -p "$TEMP_DIR"
fi

# Restore backup
log_info "Restoring backup..."
if [ "$DRY_RUN" -eq 0 ]; then
    if [[ "$BACKUP_PATH" == *.tar.gz || "$BACKUP_PATH" == *.tgz ]]; then
        tar -xzf "$BACKUP_PATH" -C "$TEMP_DIR"
    elif [[ "$BACKUP_PATH" == *.zip ]]; then
        unzip "$BACKUP_PATH" -d "$TEMP_DIR"
    elif [[ "$BACKUP_PATH" == *.sql ]]; then
        cp "$BACKUP_PATH" "$TEMP_DIR/dump.sql"
    elif [ -d "$BACKUP_PATH" ]; then
        cp -r "$BACKUP_PATH"/* "$TEMP_DIR"/
    else
        log_error "Unsupported backup file type or directory structure: $BACKUP_PATH"
    fi
    log_success "Backup restored to $TEMP_DIR"
else
    log_info "Dry run: Skipping backup restoration."
fi

# Perform integrity checks
log_info "Performing integrity checks..."

# 1. Check for expected files/directories (basic check)
if [ "$DRY_RUN" -eq 0 ]; then
    if [ -z "$(ls -A "$TEMP_DIR")" ]; then
        log_error "Restoration failed: Temporary directory '$TEMP_DIR' is empty."
    else
        log_success "Temporary directory '$TEMP_DIR' contains restored files."
    fi
else
    log_info "Dry run: Skipping file existence check."
fi

# 2. Checksum verification
if [ -n "$CHECKSUM_FILE" ]; then
    log_info "Verifying checksums using $CHECKSUM_FILE..."
    if [ "$DRY_RUN" -eq 0 ]; then
        if [ ! -f "$TEMP_DIR/$CHECKSUM_FILE" ]; then
            log_warn "Checksum file '$TEMP_DIR/$CHECKSUM_FILE' not found in restored backup. Skipping checksum verification."
        else
            # Determine checksum type (sha256sum, md5sum, etc.)
            CHECKSUM_COMMAND=""
            if grep -q "sha256" "$TEMP_DIR/$CHECKSUM_FILE"; then
                CHECKSUM_COMMAND="sha256sum -c"
            elif grep -q "md5" "$TEMP_DIR/$CHECKSUM_FILE"; then
                CHECKSUM_COMMAND="md5sum -c"
            else
                log_warn "Unknown checksum format in '$TEMP_DIR/$CHECKSUM_FILE'. Skipping checksum verification."
            fi

            if [ -n "$CHECKSUM_COMMAND" ]; then
                (cd "$TEMP_DIR" && $CHECKSUM_COMMAND "$CHECKSUM_FILE") || log_error "Checksum verification failed!"
                log_success "Checksum verification passed."
            fi
        fi
    else
        log_info "Dry run: Skipping checksum verification."
    fi
fi

# 3. Database connectivity check
if [ -n "$DB_CHECK_TYPE" ]; then
    log_info "Performing database connectivity check ($DB_CHECK_TYPE)..."
    if [ "$DRY_RUN" -eq 0 ]; then
        if [ "$DB_CHECK_TYPE" == "postgres" ]; then
            PGPASSWORD="$DB_PASS" psql -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME" -c "SELECT 1;" > /dev/null 2>&1 || log_error "PostgreSQL connectivity check failed!"
            log_success "PostgreSQL connectivity check passed."
        elif [ "$DB_CHECK_TYPE" == "mysql" ]; then
            mysql -h "$DB_HOST" -u "$DB_USER" -p"$DB_PASS" -D "$DB_NAME" -e "SELECT 1;" > /dev/null 2>&1 || log_error "MySQL connectivity check failed!"
            log_success "MySQL connectivity check passed."
        fi
    else
        log_info "Dry run: Skipping database connectivity check."
    fi
fi

log_success "Backup integrity verification completed successfully!"
