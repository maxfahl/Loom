#!/bin/bash
# setup-masked-db-env.sh: A script to automate the setup of a non-production database environment with masked data.
#
# This script orchestrates the process of taking a production database dump,
# masking sensitive data using 'mask-database-dump.sh', and then restoring
# the masked data to a non-production database (e.g., development, staging).
# It assumes PostgreSQL for database operations but can be adapted for others.
#
# Usage:
#    ./setup-masked-db-env.sh -p <prod_db_name> -n <non_prod_db_name> -c <masking_config.json> [--dry-run] [--verbose]
#
# Examples:
#    # Setup a staging database 'my_app_staging' from 'my_app_prod' using 'masking_rules.json'
#    ./setup-masked-db-env.sh -p my_app_prod -n my_app_staging -c masking_rules.json
#
#    # Dry run: perform all steps except actual database restoration
#    ./setup-masked-db-env.sh -p my_app_prod -n my_app_staging -c masking_rules.json --dry-run
#
# Configuration:
#    - Requires 'pg_dump' and 'psql' to be in the PATH.
#    - Requires 'mask-database-dump.sh' to be in the same directory or specified via an environment variable.
#    - Database connection details should be configured via standard PostgreSQL environment variables
#      (e.g., PGHOST, PGPORT, PGUSER, PGPASSWORD, PGDATABASE) or .pgpass file.
#
# Error Handling:
#    - Exits if any critical command fails.
#    - Provides clear messages for each step.
#
# Dependencies:
#    - PostgreSQL client tools (pg_dump, psql)
#    - mask-database-dump.sh script
#

# --- Configuration --- START
# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# Path to the mask-database-dump.sh script. Adjust if it's not in the same directory.
MASK_SCRIPT="$(dirname "$0")"/mask-database-dump.sh
# --- Configuration --- END

# --- Helper Functions --- START
log_error() {
    echo -e "${RED}ERROR: $1${NC}" >&2
    exit 1
}

log_warning() {
    echo -e "${YELLOW}WARNING: $1${NC}" >&2
}

log_info() {
    if [[ "$VERBOSE" == "true" ]]; then
        echo -e "${GREEN}INFO: $1${NC}"
    fi
}

run_command() {
    local cmd="$@"
    log_info "Executing: $cmd"
    if [[ "$DRY_RUN" == "true" ]]; then
        echo -e "${YELLOW}DRY RUN: Would execute: $cmd${NC}"
        return 0
    else
        eval "$cmd"
        if [[ $? -ne 0 ]]; then
            log_error "Command failed: $cmd"
        fi
    fi
}
# --- Helper Functions --- END

# --- Main Logic --- START

PROD_DB_NAME=""
NON_PROD_DB_NAME=""
MASKING_CONFIG_FILE=""
DRY_RUN="false"
VERBOSE="false"

# Parse command-line arguments
while [[ $# -gt 0 ]]; do
    key="$1"
    case $key in
        -p|--prod-db)
        PROD_DB_NAME="$2"
        shift # past argument
        shift # past value
        ;;
        -n|--non-prod-db)
        NON_PROD_DB_NAME="$2"
        shift # past argument
        shift # past value
        ;;
        -c|--config)
        MASKING_CONFIG_FILE="$2"
        shift # past argument
        shift # past value
        ;;
        --dry-run)
        DRY_RUN="true"
        shift # past argument
        ;;
        --verbose)
        VERBOSE="true"
        shift # past argument
        ;;
        -h|--help)
        echo "Usage: $0 -p <prod_db_name> -n <non_prod_db_name> -c <masking_config.json> [--dry-run] [--verbose]"
        echo ""
        echo "Options:"
        echo "  -p, --prod-db      Name of the production database to dump."
        echo "  -n, --non-prod-db  Name of the non-production database to restore to."
        echo "  -c, --config       JSON configuration file with masking rules for mask-database-dump.sh."
        echo "  --dry-run          Perform all steps except actual database restoration."
        echo "  --verbose          Enable verbose output."
        echo "  -h, --help         Display this help message."
        exit 0
        ;;
        *)
        log_error "Unknown option: $1"
        ;;
    esac
done

# Validate required arguments
if [[ -z "$PROD_DB_NAME" || -z "$NON_PROD_DB_NAME" || -z "$MASKING_CONFIG_FILE" ]]; then
    log_error "All of -p, -n, and -c are required. Use -h for help."
fi

# Check if mask-database-dump.sh exists
if [[ ! -f "$MASK_SCRIPT" ]]; then
    log_error "Masking script '$MASK_SCRIPT' not found. Please ensure it's in the same directory or update MASK_SCRIPT variable."
fi

# Check if config file exists
if [[ ! -f "$MASKING_CONFIG_FILE" ]]; then
    log_error "Masking configuration file '$MASKING_CONFIG_FILE' not found."
fi

# Check for pg_dump and psql dependencies
if ! command -v pg_dump &> /dev/null
then
    log_error "'pg_dump' could not be found. Please ensure PostgreSQL client tools are installed and in your PATH."
fi

if ! command -v psql &> /dev/null
then
    log_error "'psql' could not be found. Please ensure PostgreSQL client tools are installed and in your PATH."
fi

log_info "Starting setup of masked non-production database environment..."

# 1. Create temporary dump file names
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
PROD_DUMP_FILE="/tmp/${PROD_DB_NAME}_${TIMESTAMP}_prod.sql"
MASKED_DUMP_FILE="/tmp/${NON_PROD_DB_NAME}_${TIMESTAMP}_masked.sql"

# 2. Dump production database
log_info "Dumping production database '$PROD_DB_NAME' to '$PROD_DUMP_FILE' நான"
run_command "pg_dump -Fc -d $PROD_DB_NAME -f $PROD_DUMP_FILE"

# 3. Mask sensitive data in the dump
log_info "Masking sensitive data in '$PROD_DUMP_FILE' using '$MASKING_CONFIG_FILE' நான"
run_command "$MASK_SCRIPT -i $PROD_DUMP_FILE -o $MASKED_DUMP_FILE -c $MASKING_CONFIG_FILE --verbose $([[ \"$DRY_RUN\" == \"true\" ]] && echo \"--dry-run\")"

# 4. Drop and create non-production database
log_info "Dropping and creating non-production database '$NON_PROD_DB_NAME' நான"
run_command "dropdb --if-exists $NON_PROD_DB_NAME"
run_command "createdb $NON_PROD_DB_NAME"

# 5. Restore masked data to non-production database
log_info "Restoring masked data from '$MASKED_DUMP_FILE' to '$NON_PROD_DB_NAME' நான"
run_command "pg_restore -d $NON_PROD_DB_NAME $MASKED_DUMP_FILE"

log_info "Cleaning up temporary dump files நான"
run_command "rm -f $PROD_DUMP_FILE $MASKED_DUMP_FILE"

log_info "Setup of masked non-production database environment for '$NON_PROD_DB_NAME' completed successfully! நான"

# --- Main Logic --- END
