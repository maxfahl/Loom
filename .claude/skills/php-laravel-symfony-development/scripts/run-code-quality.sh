#!/bin/bash

# run-code-quality.sh
#
# Description:
#   Executes common code quality tools (PHPStan, PHP CS Fixer, PHPUnit) for
#   Laravel or Symfony applications. This helps maintain code standards,
#   catch potential bugs early, and ensure test coverage.
#
# Usage:
#   ./run-code-quality.sh --framework=[laravel|symfony] [--no-tests] [--fix-style]
#
# Arguments:
#   --framework     Specify the framework: 'laravel' or 'symfony'. (Required)
#   --no-tests      (Optional) Skip running PHPUnit tests.
#   --fix-style     (Optional) Automatically fix code style issues using PHP CS Fixer.
#
# Examples:
#   ./run-code-quality.sh --framework=laravel
#   ./run-code-quality.sh --framework=symfony --fix-style
#   ./run-code-quality.sh --framework=laravel --no-tests
#
# Requirements:
#   - PHPStan, PHP CS Fixer, and PHPUnit should be installed via Composer
#     and available in the project's vendor/bin directory.
#   - For Laravel: 'php artisan' command must be available.
#   - For Symfony: 'php bin/console' command must be available.
#
# Exit Codes:
#   0 - All checks passed or skipped successfully
#   1 - Invalid arguments or missing requirements
#   2 - Code quality check failed (e.g., PHPStan errors, PHPUnit failures)

# --- Configuration ---
PHPSTAN_BIN="vendor/bin/phpstan"
PHPCSFIXER_BIN="vendor/bin/php-cs-fixer"
PHPUNIT_BIN="vendor/bin/phpunit"

# --- Helper Functions ---

# Function to display script usage
usage() {
    echo "Usage: $0 --framework=[laravel|symfony] [--no-tests] [--fix-style]"
    echo ""
    echo "Arguments:"
    echo "  --framework     Specify the framework: 'laravel' or 'symfony'. (Required)"
    echo "  --no-tests      (Optional) Skip running PHPUnit tests."
    echo "  --fix-style     (Optional) Automatically fix code style issues using PHP CS Fixer."
    echo ""
    echo "Examples:"
    echo "  $0 --framework=laravel"
    echo "  $0 --framework=symfony --fix-style"
    echo "  $0 --framework=laravel --no-tests"
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
    local exit_on_fail=${4:-true} # Default to true

    color_echo "blue" "Executing: $cmd"
    if eval "$cmd"; then
        color_echo "green" "$success_msg"
        return 0
    else
        color_echo "red" "$error_msg"
        if [ "$exit_on_fail" = true ]; then
            exit 2
        fi
        return 1
    fi
}

# --- Main Logic ---

# Parse arguments
FRAMEWORK=""
NO_TESTS=false
FIX_STYLE=false

for i in "$@"; do
    case $i in
        --framework=*) 
            FRAMEWORK="${i#*=}"
            shift
            ;;
        --no-tests)
            NO_TESTS=true
            shift
            ;;
        --fix-style)
            FIX_STYLE=true
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

color_echo "yellow" "Starting code quality checks for $FRAMEWORK application..."

# --- PHPStan (Static Analysis) ---
color_echo "yellow" "Running PHPStan static analysis..."
if [ ! -f "$PHPSTAN_BIN" ]; then
    color_echo "red" "Warning: PHPStan not found at $PHPSTAN_BIN. Skipping static analysis."
else
    if [ "$FRAMEWORK" == "laravel" ]; then
        run_command "$PHPSTAN_BIN analyse --memory-limit=1G" \
                    "PHPStan analysis passed." \
                    "PHPStan analysis failed. See errors above."
    elif [ "$FRAMEWORK" == "symfony" ]; then
        run_command "$PHPSTAN_BIN analyse --memory-limit=1G" \
                    "PHPStan analysis passed." \
                    "PHPStan analysis failed. See errors above."
    fi
fi

# --- PHP CS Fixer (Code Style) ---
color_echo "yellow" "Running PHP CS Fixer for code style..."
if [ ! -f "$PHPCSFIXER_BIN" ]; then
    color_echo "red" "Warning: PHP CS Fixer not found at $PHPCSFIXER_BIN. Skipping code style check/fix."
else
    if [ "$FIX_STYLE" = true ]; then
        run_command "$PHPCSFIXER_BIN fix --config=.php-cs-fixer.dist.php" \
                    "Code style fixed successfully." \
                    "Failed to fix code style issues."
    else
        run_command "$PHPCSFIXER_BIN fix --config=.php-cs-fixer.dist.php --dry-run --stop-on-violation --using-cache=no" \
                    "Code style check passed. No issues found." \
                    "Code style issues found. Run with --fix-style to automatically fix them."
    fi
fi

# --- PHPUnit (Tests) ---
if [ "$NO_TESTS" = false ]; then
    color_echo "yellow" "Running PHPUnit tests..."
    if [ ! -f "$PHPUNIT_BIN" ]; then
        color_echo "red" "Warning: PHPUnit not found at $PHPUNIT_BIN. Skipping tests."
    else
        run_command "$PHPUNIT_BIN" \
                    "All tests passed successfully." \
                    "Tests failed. See details above."
    fi
else
    color_echo "yellow" "Skipping PHPUnit tests as requested."
fi

color_echo "green" "All requested code quality checks completed."
