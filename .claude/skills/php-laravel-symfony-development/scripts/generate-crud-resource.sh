#!/bin/bash

# generate-crud-resource.sh
#
# Description:
#   Automates the generation of CRUD (Create, Read, Update, Delete) resources
#   for a given model in either Laravel or Symfony frameworks.
#   This script aims to reduce boilerplate code and ensure consistency.
#
# Usage:
#   ./generate-crud-resource.sh --framework=[laravel|symfony] --model=ModelName [--api-only] [--force]
#
# Arguments:
#   --framework   Specify the framework: 'laravel' or 'symfony'. (Required)
#   --model       The name of the model to generate CRUD for (e.g., 'Product', 'BlogPost'). (Required)
#   --api-only    (Optional) For Laravel, generates API resources (controller, request, resource).
#                 For Symfony, generates API Platform resources.
#   --force       (Optional) Overwrite existing files without confirmation.
#
# Examples:
#   ./generate-crud-resource.sh --framework=laravel --model=Product
#   ./generate-crud-resource.sh --framework=laravel --model=Order --api-only
#   ./generate-crud-resource.sh --framework=symfony --model=Task
#
# Requirements:
#   - For Laravel: 'php artisan' command must be available in the project root.
#   - For Symfony: 'php bin/console' command must be available in the project root,
#     and API Platform bundle should be installed if --api-only is used.
#
# Exit Codes:
#   0 - Success
#   1 - Invalid arguments or missing requirements
#   2 - Generation failed

# --- Configuration ---
LARAVEL_ARTISAN="php artisan"
SYMFONY_CONSOLE="php bin/console"

# --- Helper Functions ---

# Function to display script usage
usage() {
    echo "Usage: $0 --framework=[laravel|symfony] --model=ModelName [--api-only] [--force]"
    echo ""
    echo "Arguments:"
    echo "  --framework   Specify the framework: 'laravel' or 'symfony'. (Required)"
    echo "  --model       The name of the model to generate CRUD for (e.g., 'Product', 'BlogPost'). (Required)"
    echo "  --api-only    (Optional) For Laravel, generates API resources (controller, request, resource)."
    echo "                For Symfony, generates API Platform resources."
    echo "  --force       (Optional) Overwrite existing files without confirmation."
    echo ""
    echo "Examples:"
    echo "  $0 --framework=laravel --model=Product"
    echo "  $0 --framework=laravel --model=Order --api-only"
    echo "  $0 --framework=symfony --model=Task"
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
        exit 2
    fi
}

# --- Main Logic ---

# Parse arguments
FRAMEWORK=""
MODEL_NAME=""
API_ONLY=false
FORCE=false

for i in "$@"; do
    case $i in
        --framework=*) 
            FRAMEWORK="${i#*=}"
            shift
            ;;
        --model=*) 
            MODEL_NAME="${i#*=}"
            shift
            ;;
        --api-only)
            API_ONLY=true
            shift
            ;;
        --force)
            FORCE=true
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
if [ -z "$FRAMEWORK" ] || [ -z "$MODEL_NAME" ]; then
    color_echo "red" "Error: --framework and --model are required."
    usage
fi

if [ "$FRAMEWORK" != "laravel" ] && [ "$FRAMEWORK" != "symfony" ]; then
    color_echo "red" "Error: Invalid framework specified. Must be 'laravel' or 'symfony'."
    usage
fi

color_echo "yellow" "Generating CRUD resources for model: $MODEL_NAME (Framework: $FRAMEWORK, API Only: $API_ONLY)"

if [ "$FRAMEWORK" == "laravel" ]; then
    # Check for Laravel artisan command
    if ! command -v $LARAVEL_ARTISAN &> /dev/null; then
        color_echo "red" "Error: 'php artisan' command not found. Are you in a Laravel project root?"
        exit 1
    fi

    MODEL_PATH="app/Models/${MODEL_NAME}.php"
    if [ -f "$MODEL_PATH" ] && [ "$FORCE" = false ]; then
        color_echo "yellow" "Warning: Model '$MODEL_NAME' already exists. Use --force to overwrite."
        read -p "Continue and potentially overwrite? (y/N): " confirm
        if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
            color_echo "red" "Aborting."
            exit 0
        fi
    fi

    # Generate Model, Migration, Controller, and Resource (API or Web)
    if [ "$API_ONLY" = true ]; then
        run_command "$LARAVEL_ARTISAN make:model ${MODEL_NAME} -mcr --api" \
                    "Laravel Model, Migration, API Controller, and API Resource generated successfully."
                    "Failed to generate Laravel API resources."
        run_command "$LARAVEL_ARTISAN make:request ${MODEL_NAME}StoreRequest" \
                    "Laravel Store Request generated successfully."
                    "Failed to generate Laravel Store Request."
        run_command "$LARAVEL_ARTISAN make:request ${MODEL_NAME}UpdateRequest" \
                    "Laravel Update Request generated successfully."
                    "Failed to generate Laravel Update Request."
    else
        run_command "$LARAVEL_ARTISAN make:model ${MODEL_NAME} -mcr" \
                    "Laravel Model, Migration, and Web Controller generated successfully."
                    "Failed to generate Laravel Web resources."
        run_command "$LARAVEL_ARTISAN make:request ${MODEL_NAME}StoreRequest" \
                    "Laravel Store Request generated successfully."
                    "Failed to generate Laravel Store Request."
        run_command "$LARAVEL_ARTISAN make:request ${MODEL_NAME}UpdateRequest" \
                    "Laravel Update Request generated successfully."
                    "Failed to generate Laravel Update Request."
    fi

    color_echo "green" "Laravel CRUD generation complete for $MODEL_NAME."

elif [ "$FRAMEWORK" == "symfony" ]; then
    # Check for Symfony console command
    if ! command -v $SYMFONY_CONSOLE &> /dev/null; then
        color_echo "red" "Error: 'php bin/console' command not found. Are you in a Symfony project root?"
        exit 1
    fi

    ENTITY_PATH="src/Entity/${MODEL_NAME}.php"
    if [ -f "$ENTITY_PATH" ] && [ "$FORCE" = false ]; then
        color_echo "yellow" "Warning: Entity '$MODEL_NAME' already exists. Use --force to overwrite."
        read -p "Continue and potentially overwrite? (y/N): " confirm
        if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
            color_echo "red" "Aborting."
            exit 0
        fi
    fi

    # Generate Entity
    run_command "$SYMFONY_CONSOLE make:entity ${MODEL_NAME}" \
                "Symfony Entity generated successfully. Remember to add fields interactively."
                "Failed to generate Symfony Entity."

    # Generate Controller
    if [ "$API_ONLY" = true ]; then
        # Assuming API Platform is installed and configured
        color_echo "yellow" "Note: For API Platform, you typically configure resources via annotations/attributes on the Entity itself."
        color_echo "yellow" "Generating a generic API controller. Consider using API Platform's built-in operations."
        run_command "$SYMFONY_CONSOLE make:controller ${MODEL_NAME}ApiController" \
                    "Symfony API Controller generated successfully."
                    "Failed to generate Symfony API Controller."
    else
        run_command "$SYMFONY_CONSOLE make:controller ${MODEL_NAME}Controller" \
                    "Symfony Web Controller generated successfully."
                    "Failed to generate Symfony Web Controller."
    fi

    # Generate Repository
    run_command "$SYMFONY_CONSOLE make:repository ${MODEL_NAME}" \
                "Symfony Repository generated successfully."
                "Failed to generate Symfony Repository."

    color_echo "green" "Symfony CRUD generation complete for $MODEL_NAME."
    color_echo "yellow" "Remember to run 'php bin/console make:migration' and 'php bin/console doctrine:migrations:migrate' after defining entity fields."
fi

color_echo "green" "Script finished."
