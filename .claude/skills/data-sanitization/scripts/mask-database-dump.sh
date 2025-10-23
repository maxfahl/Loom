#!/bin/bash
# mask-database-dump.sh: A script to mask sensitive data within a database dump file.
#
# This script reads a database dump (e.g., SQL, CSV) and applies a series of
# masking rules defined in a configuration file. It uses `sed` for in-place
# text replacement, making it suitable for simple masking tasks.
# For more complex masking, consider using a dedicated data masking tool or a Python script.
#
# Usage:
#    ./mask-database-dump.sh -i <input_dump_file> -o <output_dump_file> -c <config_file.json> [--dry-run] [--verbose]
#
# Examples:
#    # Mask sensitive data in 'prod_dump.sql' and save to 'masked_dump.sql'
#    ./mask-database-dump.sh -i prod_dump.sql -o masked_dump.sql -c masking_rules.json
#
#    # Dry run: show changes without saving to output file
#    ./mask-database-dump.sh -i prod_dump.sql -c masking_rules.json --dry-run
#
# Configuration:
#    The config file should be a JSON file with an array of masking rules.
#    Each rule should have:
#    - "pattern": The regular expression to search for (e.g., "email='[^"]+'").
#    - "replacement": The replacement string (e.g., "email='masked@example.com'").
#
#    Example masking_rules.json:
#    [
#      { "pattern": "email='[^"]+'", "replacement": "email='masked@example.com'" },
#      { "pattern": "ssn='[^"]+'", "replacement": "ssn='XXX-XX-XXXX'" },
#      { "pattern": "password='[^"]+'", "replacement": "password='********'" }
#    ]
#
# Error Handling:
#    - Exits with an error if input file not found.
#    - Exits with an error if config file not found or is invalid JSON.
#    - Provides informative messages for `sed` failures.
#
# Dependencies:
#    - `sed` (built-in on most Unix-like systems)
#    - `jq` (for parsing JSON config, install with: `sudo apt-get install jq` or `brew install jq`)
#

# --- Configuration --- START
# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color
# --- Configuration --- END

# --- Helper Functions --- START
log_error() {
    echo -e "${RED}ERROR: $1${NC}" >&2
}

log_warning() {
    echo -e "${YELLOW}WARNING: $1${NC}" >&2
}

log_info() {
    if [[ "$VERBOSE" == "true" ]]; then
        echo -e "${GREEN}INFO: $1${NC}"
    fi
}

# --- Helper Functions --- END

# --- Main Logic --- START

INPUT_FILE=""
OUTPUT_FILE=""
CONFIG_FILE=""
DRY_RUN="false"
VERBOSE="false"

# Parse command-line arguments
while [[ $# -gt 0 ]]; do
    key="$1"
    case $key in
        -i|--input)
        INPUT_FILE="$2"
        shift # past argument
        shift # past value
        ;;
        -o|--output)
        OUTPUT_FILE="$2"
        shift # past argument
        shift # past value
        ;;
        -c|--config)
        CONFIG_FILE="$2"
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
        echo "Usage: $0 -i <input_dump_file> -o <output_dump_file> -c <config_file.json> [--dry-run] [--verbose]"
        echo ""
        echo "Options:"
        echo "  -i, --input    Input database dump file (e.g., .sql, .csv)"
        echo "  -o, --output   Output masked dump file (default: prints to stdout if --dry-run or -o is not provided)"
        echo "  -c, --config   JSON configuration file with masking rules"
        echo "  --dry-run      Show changes without saving to output file"
        echo "  --verbose      Enable verbose output"
        echo "  -h, --help     Display this help message"
        exit 0
        ;;
        *)
        log_error "Unknown option: $1"
        exit 1
        ;;
    esac
done

# Validate required arguments
if [[ -z "$INPUT_FILE" ]]; then
    log_error "Input file (-i or --input) is required."
    exit 1
fi

if [[ -z "$CONFIG_FILE" ]]; then
    log_error "Configuration file (-c or --config) is required."
    exit 1
fi

# Check if input file exists
if [[ ! -f "$INPUT_FILE" ]]; then
    log_error "Input file '$INPUT_FILE' not found."
    exit 1
fi

# Check if config file exists and is valid JSON
if [[ ! -f "$CONFIG_FILE" ]]; then
    log_error "Config file '$CONFIG_FILE' not found."
    exit 1
fi

# Check for jq dependency
if ! command -v jq &> /dev/null
then
    log_error "'jq' could not be found. Please install it (e.g., sudo apt-get install jq or brew install jq)."
    exit 1
fi

# Read masking rules from config file
MASKING_RULES=$(jq -c '.[]' "$CONFIG_FILE" 2>/dev/null)

if [[ $? -ne 0 ]]; then
    log_error "Invalid JSON in config file '$CONFIG_FILE'. Please check its format."
    exit 1
fi

log_info "Starting data masking process for '$INPUT_FILE'..."

TEMP_FILE=$(mktemp)
cp "$INPUT_FILE" "$TEMP_FILE"

for rule in $MASKING_RULES
do
    PATTERN=$(echo "$rule" | jq -r '.pattern')
    REPLACEMENT=$(echo "$rule" | jq -r '.replacement')

    if [[ -z "$PATTERN" || -z "$REPLACEMENT" ]]; then
        log_warning "Skipping malformed rule: $rule"
        continue
    fi

    log_info "Applying rule: s/$PATTERN/$REPLACEMENT/g"
    # Use a temporary file for sed to avoid issues with in-place editing on some systems
    sed -i "s/$PATTERN/$REPLACEMENT/g" "$TEMP_FILE"
    if [[ $? -ne 0 ]]; then
        log_warning "Sed command failed for pattern '$PATTERN'. Continuing with next rule."
    fi
done

if [[ "$DRY_RUN" == "true" ]]; then
    log_info "Dry run enabled. Displaying masked content (first 100 lines) without saving."
    head -n 100 "$TEMP_FILE"
    log_warning "Dry run complete. No changes were saved to a file."
elif [[ -z "$OUTPUT_FILE" ]]; then
    log_info "Output file not specified. Displaying masked content to stdout."
    cat "$TEMP_FILE"
else
    mv "$TEMP_FILE" "$OUTPUT_FILE"
    log_info "Successfully masked data and saved to '$OUTPUT_FILE'"
fi

rm -f "$TEMP_FILE" # Clean up temporary file

log_info "Data masking process finished."

# --- Main Logic --- END
