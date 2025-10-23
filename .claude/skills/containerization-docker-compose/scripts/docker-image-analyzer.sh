#!/bin/bash
# docker-image-analyzer.sh: A script to analyze a Docker image for size, layers, and potential issues.
#
# This script provides insights into a Docker image's composition, helping identify areas for optimization
# and potential security concerns. It leverages `docker history` and optionally `dive` for detailed analysis.
#
# Usage:
#    ./docker-image-analyzer.sh -i <image_name:tag> [--dive] [--verbose]
#
# Examples:
#    # Analyze a local Docker image
#    ./docker-image-analyzer.sh -i myapp:1.0.0
#
#    # Analyze an image with dive (if installed)
#    ./docker-image-analyzer.sh -i myapp:1.0.0 --dive
#
#    # Analyze with verbose output
#    ./docker-image-analyzer.sh -i myapp:1.0.0 --verbose
#
# Configuration:
#    - Requires Docker to be installed and running.
#    - Optionally requires `dive` for detailed layer analysis (install with `brew install dive` or `apt install dive`).
#
# Error Handling:
#    - Exits if Docker is not running or the image is not found.
#    - Provides informative messages for `dive` not being installed.
#
# Dependencies:
#    - Docker CLI
#    - Optional: `dive` (https://github.com/wagoodman/dive)
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

check_docker() {
    if ! command -v docker &> /dev/null; then
        log_error "Docker CLI not found. Please install Docker."
    fi
    if ! docker info &> /dev/null; then
        log_error "Docker daemon is not running. Please start Docker."
    fi
}

check_dive() {
    if command -v dive &> /dev/null; then
        echo "true"
    else
        echo "false"
    fi
}
# --- Helper Functions --- END

# --- Main Logic --- START

IMAGE_NAME=""
USE_DIVE="false"
VERBOSE="false"

# Parse command-line arguments
while [[ $# -gt 0 ]]; do
    key="$1"
    case $key in
        -i|--image)
        IMAGE_NAME="$2"
        shift # past argument
        shift # past value
        ;;
        --dive)
        USE_DIVE="true"
        shift # past argument
        ;;
        --verbose)
        VERBOSE="true"
        shift # past argument
        ;;
        -h|--help)
        echo "Usage: $0 -i <image_name:tag> [--dive] [--verbose]"
        echo ""
        echo "Options:"
        echo "  -i, --image    Name and tag of the Docker image to analyze (e.g., myapp:1.0.0)."
        echo "  --dive         Use 'dive' for detailed layer analysis (requires 'dive' to be installed)."
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
if [[ -z "$IMAGE_NAME" ]]; then
    log_error "Image name (-i or --image) is required. Use -h for help."
fi

# Check Docker installation and status
check_docker

log_info "Analyzing Docker image: $IMAGE_NAME"

# Check if image exists locally
if ! docker image inspect "$IMAGE_NAME" &> /dev/null; then
    log_error "Docker image '$IMAGE_NAME' not found locally. Please pull or build it first."
fi

# Basic image information
echo -e "\n${GREEN}--- Basic Image Information ---${NC}"
docker image inspect "$IMAGE_NAME" --format '{{json .}}' | jq '. | {Id: .Id, RepoTags: .RepoTags, Size: .Size, VirtualSize: .VirtualSize, Created: .Created, Os: .Os, Architecture: .Architecture}'

# Image history and layer sizes
echo -e "\n${GREEN}--- Image History and Layer Sizes ---${NC}"
docker history "$IMAGE_NAME"

# Detailed layer analysis with dive
if [[ "$USE_DIVE" == "true" ]]; then
    if [[ "$(check_dive)" == "true" ]]; then
        echo -e "\n${GREEN}--- Detailed Layer Analysis with Dive ---${NC}"
        log_info "Starting dive analysis. Press Ctrl+C to exit dive."
        dive "$IMAGE_NAME"
    else
        log_warning "'dive' is not installed. Skipping detailed layer analysis. Install it with 'brew install dive' (macOS) or 'apt install dive' (Debian/Ubuntu) for more insights."
    fi
fi

log_info "Docker image analysis finished."

# --- Main Logic --- END
