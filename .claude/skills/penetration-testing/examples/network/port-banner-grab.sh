#!/bin/bash

# port-banner-grab.sh
# Description: Attempts to grab banners from specified open ports on a target host.
#              This helps in identifying service versions running on those ports.

# Usage: ./port-banner-grab.sh -t <target> -p <ports> [-o <output_file>] [--dry-run]
# Example: ./port-banner-grab.sh -t example.com -p 21,22,80,443
# Example: ./port-banner-grab.sh -t 192.168.1.100 -p 8080 -o banners.txt

# --- Configuration ---
OUTPUT_DIR="banner_grabs"

# --- Helper Functions ---
print_help() {
    echo "Usage: $0 -t <target> -p <ports> [-o <output_file>] [--dry-run] [-h]"
    echo ""
    echo "  -t <target>        : Target host or IP address (e.g., example.com, 192.168.1.100)."
    echo "  -p <ports>         : Comma-separated list of ports to grab banners from (e.g., 21,22,80,443)."
    echo "  -o <output_file>   : Save banner grab results to the specified file. If not provided, prints to stdout."
    echo "  --dry-run          : Print the commands that would be executed without running them."
    echo "  -h, --help         : Display this help message."
    echo "\nNote: This script uses netcat (nc). Ensure it is installed and in your PATH."
    exit 0
}

log_message() {
    local type="$1"
    local message="$2"
    local color_code=""

    case "$type" in
        "INFO") color_code="\033[0;34m" ;; # Blue
        "SUCCESS") color_code="\033[0;32m" ;; # Green
        "WARN") color_code="\033[0;33m" ;; # Yellow
        "ERROR") color_code="\033[0;31m" ;; # Red
        *) color_code="\033[0m" ;; # Reset
    esac
    echo -e "${color_code}[$(date +'%Y-%m-%d %H:%M:%S')] [$type] ${message}\033[0m"
}

# --- Main Logic ---
TARGET=""
PORTS=""
OUTPUT_FILE=""
DRY_RUN=0

# Parse arguments
while [[ "$#" -gt 0 ]]; do
    key="$1"
    case $key in
        -t)
            TARGET="$2"
            shift # past argument
            shift # past value
            ;; 
        -p)
            PORTS="$2"
            shift # past argument
            shift # past value
            ;; 
        -o)
            OUTPUT_FILE="$2"
            shift # past argument
            shift # past value
            ;; 
        --dry-run)
            DRY_RUN=1
            shift # past argument
            ;; 
        -h|--help)
            print_help
            ;; 
        *)
            log_message "ERROR" "Unknown option: $1"
            print_help
            ;; 
    esac
done

# Validate target and ports
if [ -z "${TARGET}" ] || [ -z "${PORTS}" ]; then
    log_message "ERROR" "Target and ports must be specified. Use -t and -p options."
    print_help
fi

# Check if netcat (nc) is installed
if ! command -v nc &> /dev/null; then
    log_message "ERROR" "netcat (nc) not found. Please install it to use this script."
    exit 1
fi

# Prepare output
OUTPUT_CONTENT=""
if [ -n "${OUTPUT_FILE}" ]; then
    mkdir -p "${OUTPUT_DIR}"
    FULL_OUTPUT_PATH="${OUTPUT_DIR}/$(basename "${OUTPUT_FILE}")"
    log_message "INFO" "Banner grab results will be saved to: ${FULL_OUTPUT_PATH}"
    # Clear file if it exists
    > "${FULL_OUTPUT_PATH}"
fi

log_message "INFO" "Starting banner grabbing for ${TARGET} on ports ${PORTS}..."

IFS=',' read -ra PORT_ARRAY <<< "${PORTS}"
for PORT in "${PORT_ARRAY[@]}"; do
    log_message "INFO" "Attempting to grab banner from ${TARGET}:${PORT}"
    COMMAND="echo | nc -nv -w 1 ${TARGET} ${PORT}"

    if [ "${DRY_RUN}" -eq 1 ]; then
        log_message "INFO" "Dry run: The following command would be executed:"
        echo "  ${COMMAND}"
        OUTPUT_CONTENT+="--- Dry Run: ${TARGET}:${PORT} ---\\n"
        OUTPUT_CONTENT+="Command: ${COMMAND}\\n\\n"
    else
        BANNER_RESULT=$(eval "${COMMAND}" 2>&1)
        EXIT_CODE=$?

        if [ "${EXIT_CODE}" -eq 0 ]; then
            log_message "SUCCESS" "Banner grabbed from ${TARGET}:${PORT}"
            echo "--- ${TARGET}:${PORT} ---"
            echo "${BANNER_RESULT}"
            echo ""
            OUTPUT_CONTENT+="--- ${TARGET}:${PORT} ---\\n"
            OUTPUT_CONTENT+="${BANNER_RESULT}\\n\\n"
        else
            log_message "WARN" "Failed to grab banner from ${TARGET}:${PORT} (Exit Code: ${EXIT_CODE}). Output: ${BANNER_RESULT}"
            OUTPUT_CONTENT+="--- ${TARGET}:${PORT} (Failed) ---\\n"
            OUTPUT_CONTENT+="${BANNER_RESULT}\\n\\n"
        fi
    fi
done

if [ -n "${OUTPUT_FILE}" ] && [ "${DRY_RUN}" -eq 0 ]; then
    echo -e "${OUTPUT_CONTENT}" >> "${FULL_OUTPUT_PATH}"
    log_message "SUCCESS" "All banner grab results appended to ${FULL_OUTPUT_PATH}"
elif [ -n "${OUTPUT_FILE}" ] && [ "${DRY_RUN}" -eq 1 ]; then
    log_message "INFO" "Dry run complete. No actual output written."
fi

log_message "SUCCESS" "Banner grabbing script finished."
