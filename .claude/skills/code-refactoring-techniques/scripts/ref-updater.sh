#!/bin/bash

# ANSI escape codes for colored output
COLOR_GREEN="\033[92m"
COLOR_YELLOW="\033[93m"
COLOR_BLUE="\033[94m"
COLOR_RED="\033[91m"
COLOR_END="\033[0m"

# Function to display help message
show_help() {
    echo -e "${COLOR_BLUE}Usage: $(basename "$0") [OPTIONS] --old <OLD_REF> --new <NEW_REF>${COLOR_END}"
    echo ""
    echo -e "${COLOR_BLUE}Description:${COLOR_END}"
    echo "  Finds and replaces text references in files. Useful for updating imports, variable names, etc.,"
    echo "  after refactoring. Supports dry-run mode."
    echo ""
    echo -e "${COLOR_BLUE}Options:${COLOR_END}"
    echo "  -o, --old <OLD_REF>      The old text reference to find (e.g., 'oldFunctionName', 'import { OldClass }')."
    echo "  -n, --new <NEW_REF>      The new text reference to replace with (e.g., 'newFunctionName', 'import { NewClass }')."
    echo "  -p, --path <PATH>        Optional: Directory to start searching from. Defaults to current directory (.)."
    echo "  -i, --include <PATTERN>  Optional: Glob pattern for files to include (e.g., '*.ts', '*.tsx'). Default: '*.{ts,tsx,js,jsx,json}'."
    echo "  -e, --exclude <PATTERN>  Optional: Glob pattern for files/directories to exclude (e.g., 'node_modules', 'dist'). Can be used multiple times."
    echo "  -d, --dry-run            Perform a dry run without making any changes, just show what would be changed."
    echo "  -h, --help               Display this help message."
    echo ""
    echo -e "${COLOR_BLUE}Examples:${COLOR_END}"
    echo "  $(basename "$0") --old 'oldService' --new 'newService' --path src --dry-run"
    echo "  $(basename "$0") -o 'import { OldUtil } from \'./old-util\'' -n 'import { NewUtil } from \'./new-util\'' -i '*.ts'"
    echo "  $(basename "$0") -o 'myVariable' -n 'myRenamedVariable' -e 'node_modules' -e 'dist'"
    echo ""
    echo -e "${COLOR_YELLOW}Warning: Use with caution. Always commit your changes before running this script without --dry-run.${COLOR_END}"
}

# Initialize variables
OLD_REF=""
NEW_REF=""
SEARCH_PATH="."
INCLUDE_PATTERN="*.{ts,tsx,js,jsx,json}"
EXCLUDE_PATTERNS=("node_modules" ".git" "dist" "build")
DRY_RUN=false

# Parse command-line arguments
while [[ "$#" -gt 0 ]]; do
    key="$1"
    case $key in
        -o|--old)
        OLD_REF="$2"
        shift # past argument
        shift # past value
        ;;
        -n|--new)
        NEW_REF="$2"
        shift # past argument
        shift # past value
        ;;
        -p|--path)
        SEARCH_PATH="$2"
        shift # past argument
        shift # past value
        ;;
        -i|--include)
        INCLUDE_PATTERN="$2"
        shift # past argument
        shift # past value
        ;;
        -e|--exclude)
        EXCLUDE_PATTERNS+=("$2")
        shift # past argument
        shift # past value
        ;;
        -d|--dry-run)
        DRY_RUN=true
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

# Validate required arguments
if [ -z "$OLD_REF" ] || [ -z "$NEW_REF" ]; then
    echo -e "${COLOR_RED}Error: --old and --new arguments are required.${COLOR_END}"
    show_help
    exit 1
fi

# Construct find command for files
FIND_CMD="find \"$SEARCH_PATH\" -type f"

# Add include patterns
IFS=\'
' read -ra ADDR <<< "$INCLUDE_PATTERN"
FIND_CMD+=" \( -name \"${ADDR[0]}\""
for i in "${!ADDR[@]}"; do
    if [ "$i" -ne 0 ]; then
        FIND_CMD+=" -o -name \"${ADDR[$i]}\""
    fi
done
FIND_CMD+=" \)"

# Add exclude patterns for directories
for EXCL_DIR in "${EXCLUDE_PATTERNS[@]}"; do
    FIND_CMD+=" -not -path \"*/$EXCL_DIR/*\""
done

# Add exclude patterns for files (e.g., specific file names)
# This part can be extended if needed, for now, directory exclusion is primary.

echo -e "${COLOR_BLUE}--- Reference Updater ---${COLOR_END}"
echo -e "${COLOR_BLUE}Old Reference: ${COLOR_YELLOW}\'$OLD_REF\'${COLOR_END}"
echo -e "${COLOR_BLUE}New Reference: ${COLOR_YELLOW}\'$NEW_REF\'${COLOR_END}"
echo -e "${COLOR_BLUE}Search Path: ${COLOR_YELLOW}\'$SEARCH_PATH\'${COLOR_END}"
echo -e "${COLOR_BLUE}Include Files: ${COLOR_YELLOW}\'$INCLUDE_PATTERN\'${COLOR_END}"
echo -e "${COLOR_BLUE}Exclude Dirs: ${COLOR_YELLOW}\'${EXCLUDE_PATTERNS[*]}\'${COLOR_END}"

if [ "$DRY_RUN" = true ]; then
    echo -e "${COLOR_YELLOW}Performing DRY RUN. No changes will be made.${COLOR_END}"
else
    echo -e "${COLOR_RED}WARNING: This will modify files! Consider --dry-run first and commit your changes.${COLOR_END}"
    read -p "Are you sure you want to proceed? (y/N): " CONFIRM
    if [[ ! "$CONFIRM" =~ ^[yY]$ ]]; then
        echo -e "${COLOR_RED}Aborting.${COLOR_END}"
        exit 0
    fi
fi

# Find files and perform replacement
# Using eval to correctly interpret the constructed FIND_CMD with glob patterns
# This is generally safe here as inputs are controlled or validated.
FOUND_FILES=$(eval $FIND_CMD)

if [ -z "$FOUND_FILES" ]; then
    echo -e "${COLOR_YELLOW}No files found matching criteria.${COLOR_END}"
    exit 0
fi

for FILE in $FOUND_FILES; do
    if grep -qF "$OLD_REF" "$FILE"; then
        echo -e "${COLOR_BLUE}Processing file: ${FILE}${COLOR_END}"
        if [ "$DRY_RUN" = true ]; then
            # Show diff for dry run
            # Using a temporary file to simulate changes for diff
            TEMP_FILE=$(mktemp)
            sed "s|$(printf %s "$OLD_REF" | sed -e \'s/[\/&]/\\&/g\')|$(printf %s "$NEW_REF" | sed -e \'s/[\/&]/\\&/g\')|g" "$FILE" > "$TEMP_FILE"
            diff -u "$FILE" "$TEMP_FILE" || true # || true to prevent diff from exiting with 1 if differences exist
            rm "$TEMP_FILE"
        else
            # Perform in-place replacement
            # Using a temporary file for safety with sed -i
            sed -i.bak "s|$(printf %s "$OLD_REF" | sed -e \'s/[\/&]/\\&/g\')|$(printf %s "$NEW_REF" | sed -e \'s/[\/&]/\\&/g\')|g" "$FILE"
            if [ $? -eq 0 ]; then
                echo -e "${COLOR_GREEN}  Replaced reference in ${FILE}${COLOR_END}"
                rm "${FILE}.bak" # Remove backup file
            else
                echo -e "${COLOR_RED}  Error replacing reference in ${FILE}${COLOR_END}"
            fi
        fi
    fi
done

echo -e "\n${COLOR_BLUE}--- Reference Update Complete ---${COLOR_END}"
if [ "$DRY_RUN" = true ]; then
    echo -e "${COLOR_YELLOW}No files were modified (dry run).{COLOR_END}"
else
    echo -e "${COLOR_GREEN}Files have been updated.${COLOR_END}"
fi
