#!/bin/bash

# ANSI escape codes for colored output
COLOR_GREEN="\033[92m"
COLOR_YELLOW="\033[93m"
COLOR_BLUE="\033[94m"
COLOR_RED="\033[91m"
COLOR_END="\033[0m"

# Function to display help message
show_help() {
    echo -e "${COLOR_BLUE}Usage: $(basename "$0") [OPTIONS]${COLOR_END}"
    echo ""
    echo -e "${COLOR_BLUE}Description:${COLOR_END}"
    echo "  Automates code formatting with Prettier and linting with ESLint for TypeScript projects."
    echo "  Ensures code consistency and adherence to project standards after refactoring."
    echo ""
    echo -e "${COLOR_BLUE}Options:${COLOR_END}"
    echo "  -p, --path <PATH>        Optional: Path to the directory or file to process. Defaults to current directory (.)."
    echo "  -f, --no-format          Skip Prettier formatting."
    echo "  -l, --no-lint            Skip ESLint linting and fixing."
    echo "  -h, --help               Display this help message."
    echo ""
    echo -e "${COLOR_BLUE}Examples:${COLOR_END}"
    echo "  $(basename "$0")                                # Format and lint current directory"
    echo "  $(basename "$0") --path src/components           # Format and lint a specific directory"
    echo "  $(basename "$0") -p src/utils/my-file.ts -f    # Lint a specific file, skip formatting"
    echo "  $(basename "$0") --no-lint                      # Format current directory, skip linting"
    echo ""
    echo -e "${COLOR_YELLOW}Note: This script assumes 'prettier' and 'eslint' are installed and configured in your project."
}

# Initialize variables
TARGET_PATH="."
RUN_FORMAT=true
RUN_LINT=true

# Parse command-line arguments
while [[ "$#" -gt 0 ]]; do
    key="$1"
    case $key in
        -p|--path)
        TARGET_PATH="$2"
        shift # past argument
        shift # past value
        ;;
        -f|--no-format)
        RUN_FORMAT=false
        shift # past argument
        ;;
        -l|--no-lint)
        RUN_LINT=false
        shift # past argument
        ;;
        -h|--help)
        show_help
        exit 0
        ;;
        *)
        echo -e "${COLOR_RED}Unknown option: $1${COLOR_END}"
        show_help
        exit 1
        ;;
    esac
done

echo -e "${COLOR_BLUE}--- Code Formatter and Linter ---${COLOR_END}"
echo -e "${COLOR_BLUE}Target Path: ${COLOR_YELLOW}\'$TARGET_PATH\'${COLOR_END}"

# Check for prettier and eslint executables
if ! command -v prettier &> /dev/null; then
    echo -e "${COLOR_RED}Error: 'prettier' command not found. Please install it (e.g., npm install -g prettier or as a dev dependency).${COLOR_END}"
    RUN_FORMAT=false # Disable formatting if prettier is not found
fi

if ! command -v eslint &> /dev/null; then
    echo -e "${COLOR_RED}Error: 'eslint' command not found. Please install it (e.g., npm install -g eslint or as a dev dependency).${COLOR_END}"
    RUN_LINT=false # Disable linting if eslint is not found
fi

# Run Prettier
if [ "$RUN_FORMAT" = true ]; then
    echo -e "\n${COLOR_BLUE}Running Prettier...${COLOR_END}"
    # Use find to get only .ts, .tsx, .js, .jsx files and pipe to prettier
    find "$TARGET_PATH" -type f \( -name "*.ts" -o -name "*.tsx" -o -name "*.js" -o -name "*.jsx" \) -not -path "*/node_modules/*" -print0 | xargs -0 prettier --write
    if [ $? -eq 0 ]; then
        echo -e "${COLOR_GREEN}Prettier formatting complete.${COLOR_END}"
    else
        echo -e "${COLOR_RED}Prettier formatting failed or encountered issues.${COLOR_END}"
    fi
else
    echo -e "\n${COLOR_YELLOW}Skipping Prettier formatting.${COLOR_END}"
fi

# Run ESLint
if [ "$RUN_LINT" = true ]; then
    echo -e "\n${COLOR_BLUE}Running ESLint...${COLOR_END}"
    # ESLint typically handles file discovery and exclusions itself based on .eslintrc and .eslintignore
    eslint "$TARGET_PATH" --fix --ext .ts,.tsx,.js,.jsx
    if [ $? -eq 0 ]; then
        echo -e "${COLOR_GREEN}ESLint linting and fixing complete.${COLOR_END}"
    else
        echo -e "${COLOR_RED}ESLint found issues or failed.${COLOR_END}"
    fi
else
    echo -e "\n${COLOR_YELLOW}Skipping ESLint linting.${COLOR_END}"
fi

echo -e "\n${COLOR_BLUE}--- Process Complete ---${COLOR_END}"
