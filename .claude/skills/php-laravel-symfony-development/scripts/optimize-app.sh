#!/bin/bash

# optimize-app.sh
#
# Description:
#   Runs common performance optimization commands for Laravel or Symfony applications.
#   This script helps in preparing the application for production or improving development performance.
#
# Usage:
#   ./optimize-app.sh --framework=[laravel|symfony] [--env=production] [--clear-opcache]
#
# Arguments:
#   --framework     Specify the framework: 'laravel' or 'symfony'. (Required)
#   --env           (Optional) Specify the environment (e.g., 'production', 'staging').
#                   Defaults to 'production' for Symfony cache commands.
#   --clear-opcache (Optional) Attempt to clear PHP OPcache. Requires opcache.enable_cli=1.
#
# Examples:
#   ./optimize-app.sh --framework=laravel
#   ./optimize-app.sh --framework=symfony --env=prod --clear-opcache
#
# Requirements:
#   - For Laravel: 'php artisan' command must be available in the project root.
#   - For Symfony: 'php bin/console' command must be available in the project root.
#
# Exit Codes:
#   0 - Success
#   1 - Invalid arguments or missing requirements
#   2 - Optimization failed

# --- Configuration ---
LARAVEL_ARTISAN="php artisan"
SYMFONY_CONSOLE="php bin/console"

# --- Helper Functions ---

# Function to display script usage
usage() {
    echo "Usage: $0 --framework=[laravel|symfony] [--env=production] [--clear-opcache]"
    echo ""
    echo "Arguments:"
    echo "  --framework     Specify the framework: 'laravel' or 'symfony'. (Required)"
    echo "  --env           (Optional) Specify the environment (e.g., 'production', 'staging')."
    echo "                  Defaults to 'production' for Symfony cache commands."
    echo "  --clear-opcache (Optional) Attempt to clear PHP OPcache. Requires opcache.enable_cli=1."
    echo ""
    echo "Examples:"
    echo "  $0 --framework=laravel"
    echo "  $0 --framework=symfony --env=prod --clear-opcache"
    exit 1
}

# Function for colored output
color_echo() {
    local color=$1
    local message=$2
    case "$color" in
        "red")    echo -e "\033[0;31m${message}\033[0m" ;;
        "green")  echo -e "\033[0;32m${message}\033[0m" ;;
        "yellow") echo -e "\033[0;33m${message}\033[0m" ;;
        "blue")   echo -e "\033[0;34m${message}\033[0m" ;;
        *)        echo "${message}" ;;
    esac
}

# Function to run a command and check its success
run_command() {
    local cmd=$1
    local success_msg=$2
    local error_msg=$3

    color_echo "blue" "Executing: $cmd"
    if eval "$cmd"; then
        color_echo "green" "$success_msg"
    else
        color_echo "red" "$error_msg"
        # Do not exit immediately for optimization commands, some might be optional
    fi
}

# --- Main Logic ---

# Parse arguments
FRAMEWORK=""
ENV=""
CLEAR_OPCACHE=false

for i in "$@"; do
    case $i in
        --framework=*) 
            FRAMEWORK="${i#*=}"
            shift
            ;;
        --env=*) 
            ENV="${i#*=}"
            shift
            ;;
        --clear-opcache)
            CLEAR_OPCACHE=true
            shift
            ;;
        -h|--help)
            usage
            ;;
        *)
            color_echo "red" "Unknown option: $i"
            usage
            ;;
    esac
done

# Validate arguments
if [ -z "$FRAMEWORK" ]; then
    color_echo "red" "Error: --framework is required."
    usage
fi

if [ "$FRAMEWORK" != "laravel" ] && [ "$FRAMEWORK" != "symfony" ]; then
    color_echo "red" "Error: Invalid framework specified. Must be 'laravel' or 'symfony'."
    usage
fi

color_echo "yellow" "Starting optimization for $FRAMEWORK application..."

if [ "$FRAMEWORK" == "laravel" ]; then
    # Check for Laravel artisan command
    if ! command -v $LARAVEL_ARTISAN &> /dev/null; then
        color_echo "red" "Error: 'php artisan' command not found. Are you in a Laravel project root?"
        exit 1
    fi

    color_echo "yellow" "Running Laravel optimization commands..."
    run_command "$LARAVEL_ARTISAN optimize:clear" "Cleared cached bootstrap files." "Failed to clear cached bootstrap files."
    run_command "$LARAVEL_ARTISAN config:cache" "Configuration cached successfully." "Failed to cache configuration."
    run_command "$LARAVEL_ARTISAN route:cache" "Routes cached successfully." "Failed to cache routes."
    run_command "$LARAVEL_ARTISAN view:cache" "Views cached successfully." "Failed to cache views."
    run_command "$LARAVEL_ARTISAN event:cache" "Events cached successfully." "Failed to cache events."

    color_echo "green" "Laravel optimization complete."

elif [ "$FRAMEWORK" == "symfony" ]; then
    # Check for Symfony console command
    if ! command -v $SYMFONY_CONSOLE &> /dev/null; then
        color_echo "red" "Error: 'php bin/console' command not found. Are you in a Symfony project root?"
        exit 1
    fi

    SYMFONY_ENV_OPT=""
    if [ -n "$ENV" ]; then
        SYMFONY_ENV_OPT="--env=$ENV"
    else
        SYMFONY_ENV_OPT="--env=prod" # Default to prod for Symfony cache commands
    fi

    color_echo "yellow" "Running Symfony optimization commands (Environment: ${ENV:-prod})..."
    run_command "$SYMFONY_CONSOLE $SYMFONY_ENV_OPT cache:clear" "Symfony cache cleared successfully." "Failed to clear Symfony cache."
    run_command "$SYMFONY_CONSOLE $SYMFONY_ENV_OPT cache:warmup" "Symfony cache warmed up successfully." "Failed to warm up Symfony cache."
    run_command "$SYMFONY_CONSOLE assets:install --symlink --relative" "Symfony assets installed successfully." "Failed to install Symfony assets."
    run_command "$SYMFONY_CONSOLE doctrine:cache:clear-query" "Doctrine query cache cleared." "Failed to clear Doctrine query cache."
    run_command "$SYMFONY_CONSOLE doctrine:cache:clear-result" "Doctrine result cache cleared." "Failed to clear Doctrine result cache."
    run_command "$SYMFONY_CONSOLE doctrine:cache:clear-metadata" "Doctrine metadata cache cleared." "Failed to clear Doctrine metadata cache."

    color_echo "green" "Symfony optimization complete."
fi

if [ "$CLEAR_OPCACHE" = true ]; then
    color_echo "yellow" "Attempting to clear PHP OPcache..."
    # This command requires opcache.enable_cli=1 in php.ini
    run_command "php -r 'opcache_reset();'" "PHP OPcache cleared successfully." "Failed to clear PHP OPcache. Ensure 'opcache.enable_cli=1' in php.ini."
fi

color_echo "green" "Script finished."
