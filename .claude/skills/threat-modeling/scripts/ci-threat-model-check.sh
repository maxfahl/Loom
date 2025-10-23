#!/bin/bash

# ci-threat-model-check.sh
# This script checks for the existence and basic content of a threat model file
# within a specified component directory, suitable for CI/CD pipelines.

# --- Configuration ---
# Default threat model file names to look for
DEFAULT_TM_FILENAMES=("threat_model.md" "threat_model.yaml" "threat_model.yml")
# Keywords to check for within the threat model file to ensure it's not empty
# or a placeholder. Case-insensitive.
DEFAULT_KEYWORDS=("STRIDE" "threats" "countermeasures" "risk assessment")

# --- Functions ---

# Function to display script usage
usage() {
    echo "Usage: $0 -p <component_path> [-f <filename1,filename2>] [-k <keyword1,keyword2>] [-h]"
    echo ""
    echo "  -p <component_path> : (Required) Path to the component directory (e.g., ./src/auth-service)."
    echo "  -f <filenames>      : (Optional) Comma-separated list of threat model filenames to check for."
    echo "                        Defaults to: ${DEFAULT_TM_FILENAMES[*]}"
    echo "  -k <keywords>       : (Optional) Comma-separated list of keywords to search for in the TM file."
    echo "                        Defaults to: ${DEFAULT_KEYWORDS[*]}"
    echo "  -h                  : Display this help message."
    echo ""
    echo "Example: $0 -p ./services/user-api -f threat_model.md,security_review.yaml -k STRIDE,Authentication"
    exit 1
}

# Function to print messages in color
print_color() {
    COLOR=$1
    MESSAGE=$2
    NC='\033[0m' # No Color
    case "$COLOR" in
        "red")    echo -e "\033[0;31m${MESSAGE}${NC}" ;;
        "green")  echo -e "\033[0;32m${MESSAGE}${NC}" ;;
        "yellow") echo -e "\033[0;33m${MESSAGE}${NC}" ;;
        "blue")   echo -e "\033[0;34m${MESSAGE}${NC}" ;;
        *)        echo "${MESSAGE}" ;;
    esac
}

# --- Main Script ---

COMPONENT_PATH=""
TM_FILENAMES=("${DEFAULT_TM_FILENAMES[@]}")
KEYWORDS=("${DEFAULT_KEYWORDS[@]}")

# Parse command-line arguments
while getopts "p:f:k:h" opt; do
    case "$opt" in
        p) COMPONENT_PATH="$OPTARG" ;;
        f) IFS=',' read -r -a TM_FILENAMES <<< "$OPTARG" ;;
        k) IFS=',' read -r -a KEYWORDS <<< "$OPTARG" ;;
        h) usage ;;
        *) usage ;;
    esac
done

# Validate component path
if [ -z "$COMPONENT_PATH" ]; then
    print_color "red" "Error: Component path (-p) is required."
    usage
fi

if [ ! -d "$COMPONENT_PATH" ]; then
    print_color "red" "Error: Component directory '$COMPONENT_PATH' not found."
    exit 1
fi

print_color "blue" "Checking threat model for component: $COMPONENT_PATH"

# 1. Check for threat model file existence
TM_FILE_FOUND=""
for filename in "${TM_FILENAMES[@]}"; do
    if [ -f "$COMPONENT_PATH/$filename" ]; then
        TM_FILE_FOUND="$COMPONENT_PATH/$filename"
        break
    fi
done

if [ -z "$TM_FILE_FOUND" ]; then
    print_color "red" "Threat Model Check FAILED: No threat model file found in '$COMPONENT_PATH'."
    print_color "red" "Expected filenames: ${TM_FILENAMES[*]}"
    exit 1
else
    print_color "green" "Threat Model Check PASSED: Found threat model file: $TM_FILE_FOUND"
fi

# 2. Check for keywords within the threat model file
ALL_KEYWORDS_FOUND=true
for keyword in "${KEYWORDS[@]}"; do
    if ! grep -q -i "$keyword" "$TM_FILE_FOUND"; then
        print_color "red" "Threat Model Content Check FAILED: Keyword '$keyword' not found (case-insensitive) in $TM_FILE_FOUND."
        ALL_KEYWORDS_FOUND=false
    else
        print_color "green" "Threat Model Content Check PASSED: Keyword '$keyword' found in $TM_FILE_FOUND."
    fi
done

if ! $ALL_KEYWORDS_FOUND; then
    print_color "red" "Threat Model Check FAILED: One or more required keywords were missing from the threat model file."
    exit 1
else
    print_color "green" "Threat Model Check PASSED: All required keywords found in $TM_FILE_FOUND."
fi

print_color "green" "Threat Model CI Check completed successfully for $COMPONENT_PATH."
exit 0
