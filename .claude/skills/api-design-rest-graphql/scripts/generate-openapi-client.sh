#!/bin/bash
# generate-openapi-client.sh: A script to generate client SDKs from an OpenAPI/Swagger specification.
#
# This script leverages the OpenAPI Generator CLI tool to automatically generate client libraries
# in various programming languages. This significantly speeds up client integration with your API.
#
# Usage:
#    ./generate-openapi-client.sh -s <openapi_spec.yaml> -l <language> -o <output_directory> [--dry-run] [--verbose]
#
# Examples:
#    # Generate a TypeScript client for the User Management API
#    ./generate-openapi-client.sh -s ../examples/rest-api-spec.yaml -l typescript-fetch -o ./clients/typescript-user-client
#
#    # Generate a Python client
#    ./generate-openapi-client.sh -s ../examples/rest-api-spec.yaml -l python -o ./clients/python-user-client
#
#    # Dry run: show the command that would be executed without actually generating
#    ./generate-openapi-client.sh -s ../examples/rest-api-spec.yaml -l typescript-fetch -o ./clients/typescript-user-client --dry-run
#
# Configuration:
#    - Requires Java Runtime Environment (JRE) to be installed.
#    - Requires the OpenAPI Generator CLI JAR. This script will attempt to download it if not found.
#    - Supported languages can be listed using `java -jar openapi-generator-cli.jar list`.
#
# Error Handling:
#    - Exits if required arguments are missing.
#    - Exits if OpenAPI Generator CLI fails.
#    - Provides informative messages for download failures.
#
# Dependencies:
#    - Java Runtime Environment (JRE)
#    - curl (for downloading the JAR)
#

# --- Configuration --- START
OPENAPI_GENERATOR_CLI_VERSION="7.0.1" # Use a specific version for consistency
OPENAPI_GENERATOR_CLI_URL="https://repo1.maven.org/maven2/org/openapitools/openapi-generator-cli/${OPENAPI_GENERATOR_CLI_VERSION}/openapi-generator-cli-${OPENAPI_GENERATOR_CLI_VERSION}.jar"
OPENAPI_GENERATOR_CLI_JAR="openapi-generator-cli-${OPENAPI_GENERATOR_CLI_VERSION}.jar"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color
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

check_java() {
    if type -p java > /dev/null; then
        _java=java
    elif [[ -n "$JAVA_HOME" ]] && [[ -x "$JAVA_HOME/bin/java" ]];  then
        _java="$JAVA_HOME/bin/java"
    fi
    if [[ "$_java" ]]; then
        version=$("$_java" -version 2>&1 | awk -F '"' '/version/ {print $2}')
        log_info "Java is installed, version: $version"
    else
        log_error "Java Runtime Environment (JRE) not found. Please install Java to run OpenAPI Generator CLI."
    fi
}

download_generator_cli() {
    if [[ ! -f "$OPENAPI_GENERATOR_CLI_JAR" ]]; then
        log_info "OpenAPI Generator CLI JAR not found. Downloading from $OPENAPI_GENERATOR_CLI_URL..."
        curl -sL "$OPENAPI_GENERATOR_CLI_URL" -o "$OPENAPI_GENERATOR_CLI_JAR"
        if [[ $? -ne 0 ]]; then
            log_error "Failed to download OpenAPI Generator CLI JAR. Please check your internet connection or the URL."
        fi
        log_info "Download complete."
    else
        log_info "OpenAPI Generator CLI JAR already exists."
    fi
}

# --- Helper Functions --- END

# --- Main Logic --- START

SPEC_FILE=""
LANGUAGE=""
OUTPUT_DIR=""
DRY_RUN="false"
VERBOSE="false"

# Parse command-line arguments
while [[ $# -gt 0 ]]; do
    key="$1"
    case $key in
        -s|--spec)
        SPEC_FILE="$2"
        shift # past argument
        shift # past value
        ;;
        -l|--lang)
        LANGUAGE="$2"
        shift # past argument
        shift # past value
        ;;
        -o|--output)
        OUTPUT_DIR="$2"
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
        echo "Usage: $0 -s <openapi_spec.yaml> -l <language> -o <output_directory> [--dry-run] [--verbose]"
        echo ""
        echo "Options:"
        echo "  -s, --spec     Path to the OpenAPI/Swagger specification file (YAML or JSON)."
        echo "  -l, --lang     Target language for the client SDK (e.g., typescript-fetch, python, go)."
        echo "  -o, --output   Output directory for the generated client SDK."
        echo "  --dry-run      Show the command that would be executed without actually generating."
        echo "  --verbose      Enable verbose output."
        echo "  -h, --help     Display this help message."
        exit 0
        ;;
        *)
        log_error "Unknown option: $1"
        ;;
    esac
done

# Validate required arguments
if [[ -z "$SPEC_FILE" || -z "$LANGUAGE" || -z "$OUTPUT_DIR" ]]; then
    log_error "All of -s, -l, and -o are required. Use -h for help."
fi

# Check if spec file exists
if [[ ! -f "$SPEC_FILE" ]]; then
    log_error "OpenAPI specification file '$SPEC_FILE' not found."
fi

# Ensure Java is installed
check_java

# Download OpenAPI Generator CLI if not present
download_generator_cli

# Construct the generation command
GENERATE_CMD="java -jar $OPENAPI_GENERATOR_CLI_JAR generate -i $SPEC_FILE -g $LANGUAGE -o $OUTPUT_DIR"

log_info "OpenAPI Generator command: $GENERATE_CMD"

if [[ "$DRY_RUN" == "true" ]]; then
    log_warning "Dry run enabled. The following command would be executed:"
    echo "$GENERATE_CMD"
    log_warning "No client SDK was generated."
else
    log_info "Generating client SDK for '$LANGUAGE' in '$OUTPUT_DIR'..."
    eval "$GENERATE_CMD"
    if [[ $? -ne 0 ]]; then
        log_error "OpenAPI Generator CLI failed to generate the client SDK."
    fi
    log_info "Client SDK generation complete. Check '$OUTPUT_DIR' for generated files."
fi

log_info "Script finished."

# --- Main Logic --- END
