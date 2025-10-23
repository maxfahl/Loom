#!/bin/bash

# security-header-check.sh
#
# Purpose: Checks a given URL for the presence and basic configuration of common
# HTTP security headers. This helps identify and remediate A05:2021-Security
# Misconfiguration related to web server and application headers.
#
# Usage:
#   ./security-header-check.sh --url <target-url> [--verbose]
#
# Examples:
#   ./security-header-check.sh --url https://www.example.com
#   ./security-header-check.sh --url http://localhost:3000 --verbose
#
# Requirements:
#   - curl installed.

# --- Configuration ---
TARGET_URL=""
VERBOSE=false

# ANSI escape codes for colored output
COLOR_GREEN='\033[92m'
COLOR_RED='\033[91m'
COLOR_YELLOW='\033[93m'
COLOR_BLUE='\033[94m'
COLOR_RESET='\033[0m'

# --- Functions ---

# Function to display script usage
usage() {
    echo "Usage: $0 --url <target-url> [--verbose] [--help]"
    echo ""
    echo "  --url <target-url> : (Required) The URL of the web application to check."
    echo "  --verbose          : (Optional) Show all HTTP response headers."
    echo "  --help             : Display this help message."
    exit 1
}

# Function to parse command-line arguments
parse_args() {
    while [[ "$#" -gt 0 ]]; do
        case "$1" in
            --url)
                TARGET_URL="$2"
                shift
                ;;
            --verbose)
                VERBOSE=true
                ;;
            --help)
                usage
                ;;
            *)
                echo -e "${COLOR_RED}Error: Unknown parameter: $1${COLOR_RESET}"
                usage
                ;;
        esac
        shift
    done

    if [[ -z "$TARGET_URL" ]]; then
        echo -e "${COLOR_RED}Error: --url is a required parameter.${COLOR_RESET}"
        usage
    fi
}

# Function to check for a specific header
check_header() {
    local header_name="$1"
    local header_value="$2"
    local required="$3"
    local recommendation="$4"

    if echo "$header_value" | grep -qi "^$header_name:"; then
        echo -e "  ${COLOR_GREEN}✅ Found: $header_value${COLOR_RESET}"
    else
        if [[ "$required" == "true" ]]; then
            echo -e "  ${COLOR_RED}❌ Missing: $header_name${COLOR_RESET}"
            echo -e "     ${COLOR_YELLOW}Recommendation: $recommendation${COLOR_RESET}"
        else
            echo -e "  ${COLOR_YELLOW}⚠️ Optional: $header_name not found.${COLOR_RESET}"
            echo -e "     ${COLOR_YELLOW}Recommendation: $recommendation${COLOR_RESET}"
        fi
    fi
}

# --- Main Script Logic ---

parse_args "$@"

echo -e "${COLOR_BLUE}--- HTTP Security Header Check ---${COLOR_RESET}"
echo -e "Target URL: ${COLOR_YELLOW}$TARGET_URL${COLOR_RESET}"
echo "----------------------------------"

# Check if curl is installed
if ! command -v curl &> /dev/null; then
    echo -e "${COLOR_RED}Error: curl is not installed or not in PATH. Please install it.${COLOR_RESET}"
    exit 1
fi

# Fetch headers
HTTP_HEADERS=$(curl -s -I -L "$TARGET_URL")
CURL_STATUS=$?

if [[ $CURL_STATUS -ne 0 ]]; then
    echo -e "${COLOR_RED}Error: Failed to fetch headers from $TARGET_URL. Curl exited with status $CURL_STATUS.${COLOR_RESET}"
    echo -e "Please check the URL and network connectivity.${COLOR_RESET}"
    exit 1
fi

if $VERBOSE; then
    echo -e "\n${COLOR_BLUE}--- All HTTP Response Headers ---${COLOR_RESET}"
    echo "$HTTP_HEADERS"
    echo "-----------------------------------"
fi

echo -e "\n${COLOR_BLUE}--- Security Header Analysis ---${COLOR_RESET}"

# X-Content-Type-Options
check_header "X-Content-Type-Options" "$HTTP_HEADERS" "true" "Set to 'nosniff' to prevent browsers from MIME-sniffing a response away from the declared content-type."

# X-Frame-Options
check_header "X-Frame-Options" "$HTTP_HEADERS" "true" "Set to 'DENY' or 'SAMEORIGIN' to prevent clickjacking attacks."

# Strict-Transport-Security (HSTS)
check_header "Strict-Transport-Security" "$HTTP_HEADERS" "true" "Enforce secure (HTTP over TLS) connections to the server. Requires HTTPS."

# Content-Security-Policy
check_header "Content-Security-Policy" "$HTTP_HEADERS" "true" "Mitigate XSS and data injection attacks by specifying trusted sources of content."

# X-XSS-Protection (Deprecated, but still useful for older browsers)
check_header "X-XSS-Protection" "$HTTP_HEADERS" "false" "Set to '1; mode=block' to enable browser's XSS filter. CSP is preferred."

# Referrer-Policy
check_header "Referrer-Policy" "$HTTP_HEADERS" "false" "Control how much referrer information is included with requests. Recommended: 'no-referrer-when-downgrade' or 'same-origin'."

# Permissions-Policy (formerly Feature-Policy)
check_header "Permissions-Policy" "$HTTP_HEADERS" "false" "Allow or deny the use of browser features in its own frame and in iframes it embeds."

echo -e "\n${COLOR_BLUE}--- Analysis Complete ---${COLOR_RESET}"
