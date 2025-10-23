#!/bin/bash

# nmap-scan-script.sh
# Description: Performs a targeted Nmap scan on a specified host or IP range for common ports.
#              This script is intended for use within a defined scope and with explicit authorization.

# Usage: ./nmap-scan-script.sh -t <target> [-p <ports>] [-o <output_file>] [-v]
# Example: ./nmap-scan-script.sh -t 192.168.1.1 -p 22,80,443 -o nmap_results.txt -v
# Example: ./nmap-scan-script.sh -t example.com

# --- Configuration ---
DEFAULT_PORTS="21,22,23,25,53,80,110,135,139,143,443,445,3389,8080,8443"
OUTPUT_DIR="nmap_scans"

# --- Helper Functions ---
print_help() {
    echo "Usage: $0 -t <target> [-p <ports>] [-o <output_file>] [-v] [--dry-run]"
    echo ""
    echo "  -t <target>        : Target host or IP range (e.g., example.com, 192.168.1.0/24)."
    echo "  -p <ports>         : Comma-separated list of ports to scan (e.g., 80,443,8080)."
    echo "                     Default: ${DEFAULT_PORTS}"
    echo "  -o <output_file>   : Save Nmap output to the specified file. If not provided, prints to stdout."
    echo "  -v                 : Verbose mode. Show Nmap command output in real-time."
    echo "  --dry-run          : Print the Nmap command that would be executed without running it."
    echo "  -h, --help         : Display this help message."
    echo "\nEnvironment Variables:"
    echo "  NMAP_PATH          : Path to the Nmap executable (default: nmap)."
    echo "\nNote: Ensure Nmap is installed and in your PATH, or specify NMAP_PATH."
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
PORTS="${DEFAULT_PORTS}"
OUTPUT_FILE=""
VERBOSE=0
DRY_RUN=0
NMAP_EXEC="${NMAP_PATH:-nmap}" # Use NMAP_PATH env var or default to 'nmap'

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
        -v)
            VERBOSE=1
            shift # past argument
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

# Validate target
if [ -z "${TARGET}" ]; then
    log_message "ERROR" "Target not specified. Use -t option."
    print_help
fi

# Check if Nmap is installed
if ! command -v "${NMAP_EXEC}" &> /dev/null; then
    log_message "ERROR" "Nmap executable not found at '${NMAP_EXEC}'. Please install Nmap or set NMAP_PATH environment variable."
    exit 1
fi

# Construct Nmap command
NMAP_COMMAND=("${NMAP_EXEC}" -p "${PORTS}" "${TARGET}")

# Add verbose flag if set
if [ "${VERBOSE}" -eq 1 ]; then
    NMAP_COMMAND+=("-v")
fi

# Handle output file
if [ -n "${OUTPUT_FILE}" ]; then
    # Ensure output directory exists
    mkdir -p "${OUTPUT_DIR}"
    FULL_OUTPUT_PATH="${OUTPUT_DIR}/$(basename "${OUTPUT_FILE}")"
    NMAP_COMMAND+=("-oN" "${FULL_OUTPUT_PATH}")
    log_message "INFO" "Nmap output will be saved to: ${FULL_OUTPUT_PATH}"
fi

# Dry run logic
if [ "${DRY_RUN}" -eq 1 ]; then
    log_message "INFO" "Dry run: The following Nmap command would be executed:"
    echo "${NMAP_COMMAND[@]}"
    exit 0
fi

log_message "INFO" "Starting Nmap scan on ${TARGET} for ports ${PORTS}..."

# Execute Nmap command
if [ "${VERBOSE}" -eq 1 ]; then
    "${NMAP_COMMAND[@]}"
else
    # Capture output silently unless verbose is enabled
    NMAP_RAW_OUTPUT=$("${NMAP_COMMAND[@]}")
    NMAP_EXIT_CODE=$?
    if [ -n "${OUTPUT_FILE}" ]; then
        log_message "SUCCESS" "Nmap scan complete. Results saved to ${FULL_OUTPUT_PATH}"
    else
        echo "${NMAP_RAW_OUTPUT}"
        log_message "SUCCESS" "Nmap scan complete."
    fi

    if [ "${NMAP_EXIT_CODE}" -ne 0 ]; then
        log_message "WARN" "Nmap exited with non-zero status: ${NMAP_EXIT_CODE}. Check output for details."
    fi
fi

log_message "SUCCESS" "Nmap scan script finished."
