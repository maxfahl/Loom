
#!/bin/bash
# api-security-scan.sh: A script to perform basic API security scanning using OWASP ZAP.
#
# This script automates the process of running OWASP ZAP in a headless mode to perform
# a quick security scan on a specified API endpoint. It can be used in CI/CD pipelines
# to catch common vulnerabilities early in the development cycle.
#
# Usage:
#    ./api-security-scan.sh -t <target_url> [--zap-path <path_to_zap.sh>] [--report-format <html|json>] [--output <report_file>] [--dry-run] [--verbose]
#
# Examples:
#    # Scan a REST API endpoint and generate an HTML report
#    ./api-security-scan.sh -t http://localhost:3000/v1/users -r html -o api_security_report.html
#
#    # Scan a GraphQL API endpoint and generate a JSON report (requires ZAP to be configured for GraphQL)
#    ./api-security-scan.sh -t http://localhost:4000/graphql -r json -o graphql_security_report.json
#
#    # Dry run: show the ZAP command that would be executed
#    ./api-security-scan.sh -t http://localhost:3000/v1/users --dry-run
#
# Configuration:
#    - Requires OWASP ZAP to be installed. The script attempts to find it or you can specify its path.
#    - ZAP's command-line options can be extended for more advanced scans (e.g., active scan, authentication).
#
# Error Handling:
#    - Exits if required arguments are missing.
#    - Exits if ZAP is not found or fails to run.
#    - Provides informative messages for scan results.
#
# Dependencies:
#    - OWASP ZAP (download from https://www.zaproxy.org/download/)
#

# --- Configuration --- START
# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# Default ZAP path (adjust if ZAP is installed elsewhere)
DEFAULT_ZAP_PATH="/opt/homebrew/bin/zap.sh" # Common path for Homebrew on macOS
if [[ -z "$(command -v zap.sh)" ]]; then
    DEFAULT_ZAP_PATH="/usr/local/bin/zap.sh" # Another common path
fi
# --- Configuration --- END

# --- Helper Functions --- START
log_error() {
    echo -e "${RED}ERROR: $1${NC}" >&2
    exit 1
}

log_warning() {
    echo -e "${YELLOW}WARNING: $1${NC}" >&2
}

log_info() {
    if [[ "$VERBOSE" == "true" ]]; then
        echo -e "${GREEN}INFO: $1${NC}"
    fi
}

find_zap_sh() {
    if [[ -f "$ZAP_PATH" ]]; then
        echo "$ZAP_PATH"
        return 0
    fi

    if command -v zap.sh &> /dev/null; then
        echo "$(command -v zap.sh)"
        return 0
    fi

    if [[ -f "$DEFAULT_ZAP_PATH" ]]; then
        echo "$DEFAULT_ZAP_PATH"
        return 0
    fi

    log_error "OWASP ZAP (zap.sh) not found. Please install ZAP or specify its path using --zap-path."
}
# --- Helper Functions --- END

# --- Main Logic --- START

TARGET_URL=""
ZAP_PATH=""
REPORT_FORMAT="html"
OUTPUT_FILE=""
DRY_RUN="false"
VERBOSE="false"

# Parse command-line arguments
while [[ $# -gt 0 ]]; do
    key="$1"
    case $key in
        -t|--target)
        TARGET_URL="$2"
        shift # past argument
        shift # past value
        ;;
        --zap-path)
        ZAP_PATH="$2"
        shift # past argument
        shift # past value
        ;;
        -r|--report-format)
        REPORT_FORMAT="$2"
        shift # past argument
        shift # past value
        ;;
        -o|--output)
        OUTPUT_FILE="$2"
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
        echo "Usage: $0 -t <target_url> [--zap-path <path_to_zap.sh>] [--report-format <html|json>] [--output <report_file>] [--dry-run] [--verbose]"
        echo ""
        echo "Options:"
        echo "  -t, --target         The URL of the API endpoint to scan (e.g., http://localhost:3000/v1/users)."
        echo "  --zap-path           Optional: Path to the zap.sh script if not in PATH or default locations."
        echo "  -r, --report-format  Report format (html or json, default: html)."
        echo "  -o, --output         Output file for the scan report (e.g., report.html or report.json)."
        echo "  --dry-run            Show the ZAP command that would be executed without actually running the scan."
        echo "  --verbose            Enable verbose output."
        echo "  -h, --help           Display this help message."
        exit 0
        ;;
        *)
        log_error "Unknown option: $1"
        ;;
    esac
done

# Validate required arguments
if [[ -z "$TARGET_URL" ]]; then
    log_error "Target URL (-t or --target) is required. Use -h for help."
fi

# Find ZAP executable
ZAP_EXEC=$(find_zap_sh)
log_info "Using ZAP executable: $ZAP_EXEC" verbose

# Ensure output file is specified if not dry run
if [[ "$DRY_RUN" == "false" && -z "$OUTPUT_FILE" ]]; then
    log_error "Output file (-o or --output) is required when not in dry-run mode."
fi

# Construct ZAP command
# Using -cmd for command-line scan, -quickurl for target, -quickprogress for progress
# -silent for no GUI, -addoninstall zaproxy-graphql (if needed for GraphQL)
# -report_html or -report_json for report generation

ZAP_CMD="$ZAP_EXEC -cmd -quickurl $TARGET_URL -quickprogress -silent"

# Add report generation options
if [[ "$REPORT_FORMAT" == "html" ]]; then
    ZAP_CMD+=" -report_html $OUTPUT_FILE"
elif [[ "$REPORT_FORMAT" == "json" ]]; then
    ZAP_CMD+=" -report_json $OUTPUT_FILE"
else
    log_error "Unsupported report format: $REPORT_FORMAT. Supported formats are 'html' and 'json'."
fi

log_info "OWASP ZAP command: $ZAP_CMD"

if [[ "$DRY_RUN" == "true" ]]; then
    log_warning "Dry run enabled. The following command would be executed:"
    echo "$ZAP_CMD"
    log_warning "No security scan was performed."
else
    log_info "Starting OWASP ZAP security scan on '$TARGET_URL'..."
    eval "$ZAP_CMD"
    if [[ $? -ne 0 ]]; then
        log_error "OWASP ZAP scan failed. Check ZAP logs for details."
    fi
    log_info "Security scan complete. Report saved to '$OUTPUT_FILE'."
    log_info "Please review the report for any identified vulnerabilities."
fi

log_info "Script finished."

# --- Main Logic --- END
