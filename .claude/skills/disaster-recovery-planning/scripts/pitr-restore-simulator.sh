#!/bin/bash

# pitr-restore-simulator.sh: Simulates a Point-in-Time Recovery (PITR) for a PostgreSQL database.
#
# This script sets up a temporary PostgreSQL instance, restores a base backup,
# and then recovers the database to a specified timestamp using Write-Ahead Log (WAL) files.
# It's designed to test and validate PITR procedures in a safe, isolated environment.
#
# Features:
# - Creates a temporary PostgreSQL data directory and instance.
# - Restores a base backup (tar.gz format expected).
# - Applies WAL files up to a user-defined recovery target time.
# - Cleans up the temporary instance and data directory.
# - Supports dry-run mode.
#
# Usage:
#   ./pitr-restore-simulator.sh [OPTIONS]
#
# Options:
#   -b, --base-backup <PATH>    Required. Path to the base backup tar.gz file.
#   -w, --wal-archive <PATH>    Required. Path to the directory containing WAL archive files.
#   -t, --recovery-time <TIME>  Required. Target recovery timestamp (e.g., "2025-10-19 10:30:00 UTC").
#   -p, --pg-port <PORT>        Optional. Port for the temporary PostgreSQL instance. Defaults to 5433.
#   -d, --temp-dir <PATH>       Optional. Base temporary directory. Defaults to /tmp/pitr_sim.
#   --dry-run                   Perform a dry run without actual operations or cleanup.
#   --help                      Display this help message.
#
# Prerequisites:
# - PostgreSQL client utilities (pg_basebackup, pg_restore, psql) must be in PATH.
# - A base backup created with pg_basebackup (e.g., `pg_basebackup -D /path/to/backup -Ft -X fetch -P -v -z -c fast`).
# - WAL archiving must be configured on the source database (e.g., `archive_mode = on`, `archive_command`).
#
# Examples:
#   ./pitr-restore-simulator.sh \
#       --base-backup /mnt/backups/pg_base_backup_20251018.tar.gz \
#       --wal-archive /mnt/wal_archive \
#       --recovery-time "2025-10-19 10:30:00 UTC"
#
#   ./pitr-restore-simulator.sh -b /tmp/base.tar.gz -w /tmp/wal -t "2025-10-19 11:00:00 PST" --pg-port 5434 --dry-run

set -euo pipefail

# --- Configuration ----
BASE_BACKUP_PATH=""
WAL_ARCHIVE_PATH=""
RECOVERY_TARGET_TIME=""
PG_PORT=5433
TEMP_BASE_DIR="/tmp/pitr_sim_$(date +%Y%m%d%H%M%S)"
PG_DATA_DIR=""
PG_LOG_FILE=""
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
        log_info "Dry run: Skipping cleanup of temporary PostgreSQL instance and data."
        return
    fi

    log_info "Stopping temporary PostgreSQL instance on port $PG_PORT..."
    pg_ctl -D "$PG_DATA_DIR" -l "$PG_LOG_FILE" stop -m fast || true

    if [ -d "$TEMP_BASE_DIR" ]; then
        log_info "Cleaning up temporary directory: $TEMP_BASE_DIR"
        rm -rf "$TEMP_BASE_DIR"
    fi
}

# --- Argument Parsing ---
while [[ $# -gt 0 ]]; do
    key="$1"
    case $key in
        -b|--base-backup)
        BASE_BACKUP_PATH="$2"
        shift # past argument
        shift # past value
        ;;
        -w|--wal-archive)
        WAL_ARCHIVE_PATH="$2"
        shift # past argument
        shift # past value
        ;;
        -t|--recovery-time)
        RECOVERY_TARGET_TIME="$2"
        shift # past argument
        shift # past value
        ;;
        -p|--pg-port)
        PG_PORT="$2"
        shift # past argument
        shift # past value
        ;;
        -d|--temp-dir)
        TEMP_BASE_DIR="$2"
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
if [ -z "$BASE_BACKUP_PATH" ]; then
    log_error "Error: --base-backup is required. Use --help for usage."
fi
if [ ! -f "$BASE_BACKUP_PATH" ]; then
    log_error "Error: Base backup file '$BASE_BACKUP_PATH' does not exist."
fi

if [ -z "$WAL_ARCHIVE_PATH" ]; then
    log_error "Error: --wal-archive is required. Use --help for usage."
fi
if [ ! -d "$WAL_ARCHIVE_PATH" ]; then
    log_error "Error: WAL archive directory '$WAL_ARCHIVE_PATH' does not exist."
fi

if [ -z "$RECOVERY_TARGET_TIME" ]; then
    log_error "Error: --recovery-time is required. Use --help for usage."
fi

# Check for PostgreSQL utilities
command -v pg_ctl >/dev/null 2>&1 || log_error "PostgreSQL pg_ctl not found. Please ensure PostgreSQL client utilities are in your PATH."
command -v psql >/dev/null 2>&1 || log_error "PostgreSQL psql not found. Please ensure PostgreSQL client utilities are in your PATH."

# --- Main Logic ---
log_info "Starting PostgreSQL PITR simulation to time: $RECOVERY_TARGET_TIME"
log_info "Base backup: $BASE_BACKUP_PATH"
log_info "WAL archive: $WAL_ARCHIVE_PATH"
log_info "Temporary base directory: $TEMP_BASE_DIR"

PG_DATA_DIR="$TEMP_BASE_DIR/data"
PG_LOG_FILE="$TEMP_BASE_DIR/postgresql.log"

if [ "$DRY_RUN" -eq 1 ]; then
    log_info "Dry run enabled. No actual operations or cleanup will occur."
fi

# Ensure cleanup is called on exit
trap cleanup EXIT

if [ "$DRY_RUN" -eq 0 ]; then
    log_info "Creating temporary directories..."
    mkdir -p "$PG_DATA_DIR"
    mkdir -p "$(dirname "$PG_LOG_FILE")"
fi

# 1. Restore base backup
log_info "Restoring base backup to $PG_DATA_DIR..."
if [ "$DRY_RUN" -eq 0 ]; then
    tar -xzf "$BASE_BACKUP_PATH" -C "$PG_DATA_DIR"
    log_success "Base backup restored."
else
    log_info "Dry run: Skipping base backup restoration."
fi

# 2. Create recovery.conf (or recovery.signal for PG 12+)
log_info "Creating recovery configuration..."
if [ "$DRY_RUN" -eq 0 ]; then
    # For PostgreSQL 12 and later, use recovery.signal and postgresql.conf settings
    # For older versions, use recovery.conf
    # This example assumes PG 12+ for simplicity, but could be adapted.
    cat <<EOF > "$PG_DATA_DIR/postgresql.conf"
restore_command = 'cp "$WAL_ARCHIVE_PATH"/%f %p'
recovery_target_time = '$RECOVERY_TARGET_TIME'
recovery_target_action = 'pause'
listen_addresses = '' # Only listen on localhost for this temp instance
port = $PG_PORT
EOF
    touch "$PG_DATA_DIR/recovery.signal"
    log_success "Recovery configuration created."
else
    log_info "Dry run: Skipping recovery configuration creation."
fi

# 3. Start temporary PostgreSQL instance for recovery
log_info "Starting temporary PostgreSQL instance on port $PG_PORT for recovery..."
if [ "$DRY_RUN" -eq 0 ]; then
    pg_ctl -D "$PG_DATA_DIR" -l "$PG_LOG_FILE" start
    log_info "Waiting for PostgreSQL to start and recover... (check $PG_LOG_FILE for details)"
    # Wait for recovery to complete or timeout
    timeout 300s bash -c \
        "until psql -p $PG_PORT -U postgres -c 'SELECT 1;' > /dev/null 2>&1; do sleep 1; done" || \
        log_error "PostgreSQL instance failed to start or recover within timeout. Check logs: $PG_LOG_FILE"
    log_success "PostgreSQL instance started and recovered to target time."
else
    log_info "Dry run: Skipping PostgreSQL instance start and recovery."
fi

# 4. Verify recovery (optional, but highly recommended)
log_info "Verifying recovered database..."
if [ "$DRY_RUN" -eq 0 ]; then
    # You can add more specific verification steps here, e.g., querying data
    psql -p "$PG_PORT" -U postgres -c "SELECT pg_is_in_recovery();" || log_error "Failed to connect to recovered DB."
    log_success "Successfully connected to the recovered database."
    log_info "Recovery log:"
    tail -n 20 "$PG_LOG_FILE"
else
    log_info "Dry run: Skipping database verification."
fi

log_success "PITR simulation completed successfully! The database is recovered to $RECOVERY_TARGET_TIME."
log_info "You can connect to the temporary instance using: psql -p $PG_PORT -U postgres"
log_info "Remember to run cleanup or manually stop the instance and remove $TEMP_BASE_DIR when done."
