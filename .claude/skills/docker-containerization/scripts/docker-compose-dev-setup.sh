#!/bin/bash

# docker-compose-dev-setup.sh
#
# Description:
#   Generates a basic docker-compose.yml file for local development.
#   It prompts the user for application type (Node.js, Python, etc.)
#   and allows adding common services like databases (PostgreSQL, MySQL)
#   and caching (Redis).
#
# Usage:
#   ./docker-compose-dev-setup.sh [--output <file_path>] [--dry-run]
#
# Arguments:
#   --output <file_path>: (Optional) Specify the output file path for docker-compose.yml.
#                         Defaults to 'docker-compose.yml' in the current directory.
#   --dry-run:            (Optional) If set, the script will only print the generated
#                         content to stdout without writing to a file.
#
# Examples:
#   ./docker-compose-dev-setup.sh
#   ./docker-compose-dev-setup.sh --output ./my-app/docker-compose.dev.yml
#   ./docker-compose-dev-setup.sh --dry-run
#
# Configuration:
#   Interactive prompts for application type and services.
#
# Error Handling:
#   - Validates user input for choices.
#   - Warns if output file already exists.

set -euo pipefail

# --- Colors for better readability ---
GREEN="\033[0;32m"
YELLOW="\033[0;33m"
RED="\033[0;31m"
BLUE="\033[0;34m"
NC="\033[0m" # No Color

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1" >&2
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_help() {
    echo "Usage: $0 [--output <file_path>] [--dry-run]"
    echo ""
    echo "Arguments:"
    echo "  --output <file_path>: (Optional) Specify the output file path for docker-compose.yml."
    echo "                        Defaults to 'docker-compose.yml' in the current directory."
    echo "  --dry-run:            (Optional) If set, the script will only print the generated"
    echo "                        content to stdout without writing to a file."
    echo ""
    echo "Description:"
    echo "  Generates a basic docker-compose.yml file for local development."
    echo "  It prompts the user for application type and allows adding common services."
    echo ""
    echo "Examples:"
    echo "  $0"
    echo "  $0 --output ./my-app/docker-compose.dev.yml"
    echo "  $0 --dry-run"
}

# --- Variables ---
OUTPUT_FILE="docker-compose.yml"
DRY_RUN=false
COMPOSE_CONTENT=""

# --- Parse arguments ---
while [[ $# -gt 0 ]]; do
    key="$1"
    case $key in
        --output)
        OUTPUT_FILE="$2"
        shift # past argument
        shift # past value
        ;;
        --dry-run)
        DRY_RUN=true
        shift # past argument
        ;;
        --help)
        print_help
        exit 0
        ;;
        *)
        log_error "Unknown option: $1"
        print_help
        exit 1
        ;;
    esac
done

# --- Main script logic ---
main() {
    log_info "Starting Docker Compose development setup generator."

    COMPOSE_CONTENT="version: '3.8'\n\nservices:\n"

    # --- Application Service ---
    APP_TYPE=""
    while true; do
        log_info "Select application type:"
        echo "  1) Node.js (Express/NestJS)"
        echo "  2) Python (Django/Flask)"
        echo "  3) Go (Gin/Echo)"
        echo "  4) Other (Generic Dockerfile)"
        read -rp "Enter choice (1-4): " APP_CHOICE
        case $APP_CHOICE in
            1) APP_TYPE="nodejs"; break;;
            2) APP_TYPE="python"; break;;
            3) APP_TYPE="go"; break;;
            4) APP_TYPE="other"; break;;
            *) log_warn "Invalid choice. Please enter a number between 1 and 4.";;
        esac
    done

    APP_NAME="app"
    read -rp "Enter your application service name (default: app): " USER_APP_NAME
    if [[ -n "$USER_APP_NAME" ]]; then
        APP_NAME="$USER_APP_NAME"
    fi

    COMPOSE_CONTENT+="  ${APP_NAME}:\n"
    COMPOSE_CONTENT+="    build:\n"
    COMPOSE_CONTENT+="      context: .\n"
    COMPOSE_CONTENT+="      dockerfile: Dockerfile\n"
    COMPOSE_CONTENT+="    ports:\n"
    COMPOSE_CONTENT+="      - \"3000:3000\" # Adjust port as needed\n"
    COMPOSE_CONTENT+="    volumes:\n"
    COMPOSE_CONTENT+="      - .:/app\n"
    COMPOSE_CONTENT+="    environment:\n"
    COMPOSE_CONTENT+="      NODE_ENV: development # Example for Node.js\n"
    COMPOSE_CONTENT+="    # depends_on:\n"
    COMPOSE_CONTENT+="    #   - db\n"
    COMPOSE_CONTENT+="    #   - redis\n"
    COMPOSE_CONTENT+="\n"

    # --- Database Service ---
    ADD_DB=""
    read -rp "Add a database service? (y/N): " ADD_DB
    if [[ "$ADD_DB" =~ ^[Yy]$ ]]; then
        DB_TYPE=""
        while true; do
            log_info "Select database type:"
            echo "  1) PostgreSQL"
            echo "  2) MySQL"
            echo "  3) MongoDB"
            read -rp "Enter choice (1-3): " DB_CHOICE
            case $DB_CHOICE in
                1) DB_TYPE="postgres"; break;;
                2) DB_TYPE="mysql"; break;;
                3) DB_TYPE="mongo"; break;;
                *) log_warn "Invalid choice. Please enter a number between 1 and 3.";;
            esac
        done

        COMPOSE_CONTENT+="  db:\n"
        if [[ "$DB_TYPE" == "postgres" ]]; then
            COMPOSE_CONTENT+="    image: postgres:15-alpine\n"
            COMPOSE_CONTENT+="    environment:\n"
            COMPOSE_CONTENT+="      POSTGRES_DB: ${APP_NAME}_dev\n"
            COMPOSE_CONTENT+="      POSTGRES_USER: user\n"
            COMPOSE_CONTENT+="      POSTGRES_PASSWORD: password\n"
            COMPOSE_CONTENT+="    ports:\n"
            COMPOSE_CONTENT+="      - \"5432:5432\"\n"
        elif [[ "$DB_TYPE" == "mysql" ]]; then
            COMPOSE_CONTENT+="    image: mysql:8.0\n"
            COMPOSE_CONTENT+="    environment:\n"
            COMPOSE_CONTENT+="      MYSQL_DATABASE: ${APP_NAME}_dev\n"
            COMPOSE_CONTENT+="      MYSQL_USER: user\n"
            COMPOSE_CONTENT+="      MYSQL_PASSWORD: password\n"
            COMPOSE_CONTENT+="      MYSQL_ROOT_PASSWORD: rootpassword\n"
            COMPOSE_CONTENT+="    ports:\n"
            COMPOSE_CONTENT+="      - \"3306:3306\"\n"
        elif [[ "$DB_TYPE" == "mongo" ]]; then
            COMPOSE_CONTENT+="    image: mongo:6.0\n"
            COMPOSE_CONTENT+="    ports:\n"
            COMPOSE_CONTENT+="      - \"27017:27017\"\n"
        fi
        COMPOSE_CONTENT+="    volumes:\n"
        COMPOSE_CONTENT+="      - db_data:/var/lib/${DB_TYPE} # Adjust path for MongoDB if needed\n"
        COMPOSE_CONTENT+="\n"
    fi

    # --- Redis Service ---
    ADD_REDIS=""
    read -rp "Add a Redis caching service? (y/N): " ADD_REDIS
    if [[ "$ADD_REDIS" =~ ^[Yy]$ ]]; then
        COMPOSE_CONTENT+="  redis:\n"
        COMPOSE_CONTENT+="    image: redis:7-alpine\n"
        COMPOSE_CONTENT+="    ports:\n"
        COMPOSE_CONTENT+="      - \"6379:6379\"\n"
        COMPOSE_CONTENT+="    volumes:\n"
        COMPOSE_CONTENT+="      - redis_data:/data\n"
        COMPOSE_CONTENT+="\n"
    fi

    # --- Volumes Section ---
    COMPOSE_CONTENT+="volumes:\n"
    if [[ "$ADD_DB" =~ ^[Yy]$ ]]; then
        COMPOSE_CONTENT+="  db_data:\n"
    fi
    if [[ "$ADD_REDIS" =~ ^[Yy]$ ]]; then
        COMPOSE_CONTENT+="  redis_data:\n"
    fi

    # --- Output ---
    if $DRY_RUN; then
        log_info "Generated docker-compose.yml content (dry-run):\n"
        echo -e "$COMPOSE_CONTENT"
    else
        if [[ -f "$OUTPUT_FILE" ]]; then
            log_warn "Output file '$OUTPUT_FILE' already exists. Overwriting."
        fi
        echo -e "$COMPOSE_CONTENT" > "$OUTPUT_FILE"
        log_success "docker-compose.yml generated successfully at '$OUTPUT_FILE'"
        log_info "To start your services, run: docker compose -f '$OUTPUT_FILE' up -d"
    fi
}

main "$@"
