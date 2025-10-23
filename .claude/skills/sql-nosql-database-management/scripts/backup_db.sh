#!/bin/bash
"""
Database Backup Utility

This script performs a logical backup (dump) of a specified database.
It supports PostgreSQL (pg_dump), MySQL (mysqldump), and MongoDB (mongodump).

Usage:
    ./backup_db.sh --type <db_type> --host <host> --port <port> --user <user> --db <database> [--output <file_path>] [--password <password>]

Examples:
    # PostgreSQL backup
    ./backup_db.sh --type pg --host localhost --port 5432 --user postgres --db myapp_db --output ./backups/myapp_db_$(date +%Y%m%d%H%M%S).sql

    # MySQL backup with password from environment variable
    MYSQL_PWD="mysecret" ./backup_db.sh --type mysql --host 127.0.0.1 --port 3306 --user root --db myapp_db --output ./backups/myapp_db_$(date +%Y%m%d%H%M%S).sql

    # MongoDB backup
    ./backup_db.sh --type mongo --host localhost --port 27017 --db myapp_db --output ./backups/myapp_db_$(date +%Y%m%d%H%M%S)

Configuration:
    - Requires pg_dump, mysqldump, or mongodump to be installed and in PATH.
    - Passwords can be provided via --password or environment variables (e.g., PGPASSWORD, MYSQL_PWD).
"""

# --- Configuration ---
DEFAULT_OUTPUT_DIR="./backups"

# --- Helper Functions ---
print_help() {
    echo "Usage: $(basename "$0") --type <db_type> --host <host> --port <port> --user <user> --db <database> [--output <file_path>] [--password <password>]"
    echo ""
    echo "Options:"
    echo "  --type <db_type>    Database type: 'pg' (PostgreSQL), 'mysql', 'mongo' (MongoDB). (Required)"
    echo "  --host <host>       Database host. (Required)"
    echo "  --port <port>       Database port. (Required)"
    echo "  --user <user>       Database user. (Required for pg, mysql)"
    echo "  --db <database>     Database name. (Required)"
    echo "  --output <file_path> Output file path. Defaults to ./backups/<db_name>_<timestamp>.(sql|dump)"
    echo "  --password <password> Database password. (Optional, can use env vars like PGPASSWORD, MYSQL_PWD)"
    echo "  -h, --help          Show this help message and exit."
    echo ""
    echo "Examples:"
    echo "  ./backup_db.sh --type pg --host localhost --port 5432 --user postgres --db myapp_db --output ./backups/myapp_db_$(date +%Y%m%d%H%M%S).sql"
    echo "  MYSQL_PWD=\"mysecret\" ./backup_db.sh --type mysql --host 127.0.0.1 --port 3306 --user root --db myapp_db --output ./backups/myapp_db_$(date +%Y%m%d%H%M%S).sql"
    echo "  ./backup_db.sh --type mongo --host localhost --port 27017 --db myapp_db --output ./backups/myapp_db_$(date +%Y%m%d%H%M%S)"
    exit 0
}

# --- Argument Parsing ---
DB_TYPE=""
DB_HOST=""
DB_PORT=""
DB_USER=""
DB_NAME=""
OUTPUT_FILE=""
DB_PASSWORD=""

while [[ $# -gt 0 ]]; do
    key="$1"
    case $key in
        --type)
        DB_TYPE="$2"
        shift # past argument
        shift # past value
        ;;
        --host)
        DB_HOST="$2"
        shift # past argument
        shift # past value
        ;;
        --port)
        DB_PORT="$2"
        shift # past argument
        shift # past value
        ;;
        --user)
        DB_USER="$2"
        shift # past argument
        shift # past value
        ;;
        --db)
        DB_NAME="$2"
        shift # past argument
        shift # past value
        ;;
        --output)
        OUTPUT_FILE="$2"
        shift # past argument
        shift # past value
        ;;
        --password)
        DB_PASSWORD="$2"
        shift # past argument
        shift # past value
        ;;
        -h|--help)
        print_help
        ;;
        *)
        echo -e "\033[91mUnknown option: $1\033[0m" >&2
        print_help
        ;;
    esac
done

# --- Validation ---
if [[ -z "$DB_TYPE" || -z "$DB_HOST" || -z "$DB_PORT" || -z "$DB_NAME" ]]; then
    echo -e "\033[91mError: Missing required arguments. --type, --host, --port, --db are mandatory.\033[0m" >&2
    print_help
fi

if [[ "$DB_TYPE" == "pg" || "$DB_TYPE" == "mysql" ]] && [[ -z "$DB_USER" ]]; then
    echo -e "\033[91mError: --user is required for PostgreSQL and MySQL backups.\033[0m" >&2
    print_help
fi

# --- Set default output file if not provided ---
if [[ -z "$OUTPUT_FILE" ]]; then
    mkdir -p "$DEFAULT_OUTPUT_DIR" || { echo -e "\033[91mError: Could not create output directory $DEFAULT_OUTPUT_DIR\033[0m" >&2; exit 1; }
    TIMESTAMP=$(date +%Y%m%d%H%M%S)
    case "$DB_TYPE" in
        pg|mysql)
            OUTPUT_FILE="${DEFAULT_OUTPUT_DIR}/${DB_NAME}_${TIMESTAMP}.sql"
            ;; 
        mongo)
            OUTPUT_FILE="${DEFAULT_OUTPUT_DIR}/${DB_NAME}_${TIMESTAMP}" # mongodump creates a directory
            ;; 
        *)
            echo -e "\033[91mError: Unknown database type for default output file extension.\033[0m" >&2
            exit 1
            ;; 
    esac
fi

# --- Perform Backup ---
echo -e "\033[34mStarting backup for ${DB_TYPE} database '${DB_NAME}' on ${DB_HOST}:${DB_PORT}...\033[0m"

case "$DB_TYPE" in
    pg)
        export PGPASSWORD="${DB_PASSWORD}"
        if ! pg_dump -h "${DB_HOST}" -p "${DB_PORT}" -U "${DB_USER}" -d "${DB_NAME}" > "${OUTPUT_FILE}"; then
            echo -e "\033[91mError: PostgreSQL backup failed!\033[0m" >&2
            exit 1
        fi
        unset PGPASSWORD
        ;; 
    mysql)
        export MYSQL_PWD="${DB_PASSWORD}"
        if ! mysqldump -h "${DB_HOST}" -P "${DB_PORT}" -u "${DB_USER}" "${DB_NAME}" > "${OUTPUT_FILE}"; then
            echo -e "\033[91mError: MySQL backup failed!\033[0m" >&2
            exit 1
        fi
        unset MYSQL_PWD
        ;; 
    mongo)
        if ! mongodump --host "${DB_HOST}" --port "${DB_PORT}" --db "${DB_NAME}" --out "${OUTPUT_FILE}"; then
            echo -e "\033[91mError: MongoDB backup failed!\033[0m" >&2
            exit 1
        fi
        ;; 
    *)
        echo -e "\033[91mError: Unsupported database type: ${DB_TYPE}. Supported types are 'pg', 'mysql', 'mongo'.\033[0m" >&2
        exit 1
        ;; 
esac

echo -e "\033[32mDatabase backup completed successfully to: ${OUTPUT_FILE}\033[0m"
