#!/bin/bash

# docker-image-analyzer.sh
# Description: Analyzes a Dockerfile for common best practices and suggests optimizations.
#              Can optionally run a vulnerability scan using Trivy.
# Usage: ./docker-image-analyzer.sh <path_to_dockerfile> [--scan]
#        ./docker-image-analyzer.sh /path/to/my/Dockerfile --scan

# --- Configuration ---
TRIVY_SCAN_ENABLED=false

# --- Helper Functions ---
COLOR_RED="\033[0;31m"
COLOR_GREEN="\033[0;32m"
COLOR_YELLOW="\033[0;33m"
COLOR_BLUE="\033[0;34m"
COLOR_NC="\033[0m" # No Color

print_info() { echo -e "${COLOR_BLUE}[INFO]${COLOR_NC} $1"; }
print_success() { echo -e "${COLOR_GREEN}[SUCCESS]${COLOR_NC} $1"; }
print_warning() { echo -e "${COLOR_YELLOW}[WARNING]${COLOR_NC} $1"; }
print_error() { echo -e "${COLOR_RED}[ERROR]${COLOR_NC} $1"; }

show_help() {
  echo "Usage: $0 <path_to_dockerfile> [--scan]"
  echo ""
  echo "Analyzes a Dockerfile for common best practices and suggests optimizations."
  echo "Optionally runs a vulnerability scan using Trivy."
  echo ""
  echo "Arguments:"
  echo "  <path_to_dockerfile>  Path to the Dockerfile to analyze."
  echo "  --scan                (Optional) Run a Trivy vulnerability scan on the built image."
  echo ""
  echo "Examples:"
  echo "  $0 ./Dockerfile"
  echo "  $0 /app/backend/Dockerfile --scan"
  exit 0
}

# --- Main Logic ---

if [ -z "$1" ]; then
  print_error "No Dockerfile path provided."
  show_help
fi

DOCKERFILE_PATH="$1"

if [ ! -f "$DOCKERFILE_PATH" ]; then
  print_error "Dockerfile not found at: $DOCKERFILE_PATH"
  exit 1
fi

# Check for --scan argument
if [ "$2" == "--scan" ]; then
  TRIVY_SCAN_ENABLED=true
  print_info "Trivy scan enabled."
fi

print_info "Analyzing Dockerfile: $DOCKERFILE_PATH"

# 1. Check for Multi-stage build
if grep -qi "FROM .* AS" "$DOCKERFILE_PATH"; then
  print_success "Multi-stage build detected. Good for image size optimization."
else
  print_warning "Multi-stage build not detected. Consider using it to reduce image size."
fi

# 2. Check for minimal base image (basic check)
BASE_IMAGE=$(grep -iE '^FROM\s+([^\s]+)' "$DOCKERFILE_PATH" | head -n 1 | awk '{print $2}')
if [[ "$BASE_IMAGE" =~ (alpine|slim|distroless) ]]; then
  print_success "Minimal base image ('$BASE_IMAGE') likely used. Good for security and size."
else
  print_warning "Base image ('$BASE_IMAGE') might not be minimal. Consider 'alpine', 'slim', or 'distroless' variants."
fi

# 3. Check for .dockerignore
DOCKERFILE_DIR=$(dirname "$DOCKERFILE_PATH")
if [ -f "$DOCKERFILE_DIR/.dockerignore" ]; then
  print_success ".dockerignore file found in '$DOCKERFILE_DIR'. Good for build context optimization."
else
  print_warning "No .dockerignore file found in '$DOCKERFILE_DIR'. Consider creating one to exclude unnecessary files."
fi

# 4. Check for pinned image versions
if grep -qE '^FROM\s+[^:]+:[^\s]+$' "$DOCKERFILE_PATH"; then
  print_success "Image versions appear to be pinned. Good for reproducibility."
else
  print_warning "Some base images might not be pinned to a specific version. Avoid 'latest' tag in production."
fi

# 5. Check for non-root user
if grep -qiE '^USER\s+(?!root)' "$DOCKERFILE_PATH"; then
  print_success "Non-root user instruction ('USER') found. Good for security."
else
  print_warning "No explicit non-root user instruction ('USER') found. Running as root is a security risk."
fi

# 6. Check for HEALTHCHECK
if grep -qi '^HEALTHCHECK' "$DOCKERFILE_PATH"; then
  print_success "HEALTHCHECK instruction found. Good for container orchestration."
else
  print_warning "No HEALTHCHECK instruction found. Consider adding one for robust container management."
fi

# 7. Check for combined RUN commands (basic heuristic)
# This is a simple check, more complex analysis would be needed for full accuracy
if grep -E 'RUN\s+.*\s*&&\s*.*' "$DOCKERFILE_PATH" | grep -qE 'rm -rf /var/lib/apt/lists/\*|rm -rf /tmp/\*'; then
  print_success "Combined RUN commands with cleanup detected. Good for reducing layers and image size."
else
  print_warning "Consider combining RUN commands and cleaning up temporary files (e.g., apt caches) in the same layer."
fi

# --- Trivy Scan (if enabled) ---
if $TRIVY_SCAN_ENABLED; then
  print_info "Attempting to build image for Trivy scan..."
  IMAGE_NAME="temp-scan-image:$(date +%s)"
  DOCKERFILE_DIR=$(dirname "$DOCKERFILE_PATH")

  if docker build -f "$DOCKERFILE_PATH" -t "$IMAGE_NAME" "$DOCKERFILE_DIR"; then
    print_success "Image '$IMAGE_NAME' built successfully. Running Trivy scan..."
    if command -v trivy &> /dev/null; then
      trivy image "$IMAGE_NAME"
      print_info "Trivy scan complete. Remember to remove the temporary image: docker rmi $IMAGE_NAME"
    else
      print_error "Trivy not found. Please install Trivy (https://aquasecurity.github.io/trivy/latest/getting-started/installation/) to enable vulnerability scanning."
    fi
    # Clean up temporary image (optional, user can do it manually)
    # docker rmi "$IMAGE_NAME"
  else
    print_error "Failed to build image for Trivy scan. Check your Dockerfile for errors."
  fi
fi

print_info "Dockerfile analysis complete."
