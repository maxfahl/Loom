#!/bin/bash

# docker-build-run.sh
#
# Description:
#   Simplifies the Docker build process for a Rust web application and runs the container.
#   It handles common build arguments, port mappings, and image tagging.
#
# Usage:
#   ./docker-build-run.sh <image_name> <app_port> [build_args...]
#
# Arguments:
#   <image_name> : The name for the Docker image (e.g., my-rust-app).
#   <app_port>   : The port your Rust application listens on inside the container.
#   [build_args...] : Optional additional arguments to pass to `docker build`.
#
# Options:
#   --no-cache   : Build image without using cache.
#   --run-only   : Skip building and only run the existing image.
#   --help       : Display this help message.
#
# Examples:
#   ./docker-build-run.sh my-actix-app 8080
#   ./docker-build-run.sh my-rocket-app 8000 --no-cache
#   ./docker-build-run.sh my-app 8080 --run-only
#
# Prerequisites:
#   - Docker must be installed and running.
#   - A `Dockerfile` must exist in the current directory.
#
# Error Handling:
#   - Exits if Docker is not running.
#   - Exits if `Dockerfile` is not found.
#   - Exits if required arguments are missing.
#   - Exits if docker commands fail.
#
# Configuration:
#   - Assumes `Dockerfile` is in the current directory.
#   - Assumes the application binds to 0.0.0.0 inside the container.

set -e # Exit immediately if a command exits with a non-zero status.

# --- Helper Functions ---
print_help() {
    echo "Usage: $0 <image_name> <app_port> [options]"
    echo ""
    echo "Arguments:"
    echo "  <image_name> : The name for the Docker image (e.g., my-rust-app)."
    echo "  <app_port>   : The port your Rust application listens on inside the container."
    echo ""
    echo "Options:"
    echo "  --no-cache   : Build image without using cache."
    echo "  --run-only   : Skip building and only run the existing image."
    echo "  --help       : Display this help message."
    echo ""
    echo "Examples:"
    echo "  $0 my-actix-app 8080"
    echo "  $0 my-rocket-app 8000 --no-cache"
    echo "  $0 my-app 8080 --run-only"
    echo ""
    echo "Prerequisites:"
    echo "  - Docker must be installed and running."
    echo "  - A `Dockerfile` must exist in the current directory."
    exit 0
}

log_info() {
    echo -e "\033[0;34mINFO: $1\033[0m" # Blue color
}

log_success() {
    echo -e "\033[0;32mSUCCESS: $1\033[0m" # Green color
}

log_error() {
    echo -e "\033[0;31mERROR: $1\033[0m" # Red color
    exit 1
}

# --- Argument Parsing ---
IMAGE_NAME=""
APP_PORT=""
BUILD_ARGS=""
NO_CACHE=false
RUN_ONLY=false

POSITIONAL_ARGS=()
while [[ $# -gt 0 ]]; do
    case "$1" in
        --no-cache)
            NO_CACHE=true
            shift
            ;;
        --run-only)
            RUN_ONLY=true
            shift
            ;;
        --help)
            print_help
            ;;
        -*)
            BUILD_ARGS+=" $1"
            shift
            ;;
        *)
            POSITIONAL_ARGS+=("$1")
            shift
            ;;
    esac
done

set -- "${POSITIONAL_ARGS[@]}" # Restore positional arguments

IMAGE_NAME=$1
APP_PORT=$2

if [ -z "$IMAGE_NAME" ] || [ -z "$APP_PORT" ]; then
    log_error "Missing required arguments: <image_name> and <app_port>."
    print_help
fi

# --- Pre-requisite Checks ---
if ! command -v docker &> /dev/null; then
    log_error "Docker is not installed. Please install Docker to use this script."
fi

if ! docker info &> /dev/null; then
    log_error "Docker daemon is not running. Please start Docker."
fi

if [ ! -f "Dockerfile" ]; then
    log_error "Dockerfile not found in the current directory. Please ensure a Dockerfile exists."
fi

# --- Build Docker Image ---
if [ "$RUN_ONLY" = false ]; then
    log_info "Building Docker image '$IMAGE_NAME' நான"
    BUILD_COMMAND="docker build -t $IMAGE_NAME"
    if [ "$NO_CACHE" = true ]; then
        BUILD_COMMAND+=" --no-cache"
    fi
    BUILD_COMMAND+=" $BUILD_ARGS ."
    
    log_info "Executing: $BUILD_COMMAND"
    eval "$BUILD_COMMAND" || log_error "Docker image build failed."
    log_success "Docker image '$IMAGE_NAME' built successfully."
else
    log_info "Skipping build. Running existing image '$IMAGE_NAME'."
    if ! docker images --format \"{{.Repository}}\" | grep -q "^$IMAGE_NAME$"; then
        log_error "Image '$IMAGE_NAME' does not exist. Cannot run with --run-only. Please build it first."
    fi
fi

# --- Run Docker Container ---
log_info "Running Docker container for '$IMAGE_NAME' on port $APP_PORT..."

# Stop and remove any existing container with the same name
if docker ps -a --format '{{.Names}}' | grep -q "^${IMAGE_NAME}-container$"; then
    log_info "Stopping and removing existing container '${IMAGE_NAME}-container'..."
    docker stop "${IMAGE_NAME}-container" &> /dev/null || true
    docker rm "${IMAGE_NAME}-container" &> /dev/null || true
fi

docker run -d \
    --name "${IMAGE_NAME}-container" \
    -p "$APP_PORT:$APP_PORT" \
    "$IMAGE_NAME" || log_error "Failed to run Docker container."

log_success "Docker container '${IMAGE_NAME}-container' is running and accessible on http://localhost:$APP_PORT"
log_info "To stop the container: docker stop ${IMAGE_NAME}-container"
log_info "To view logs: docker logs ${IMAGE_NAME}-container"
