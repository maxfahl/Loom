#!/bin/bash

# k6-run-docker.sh
# Description: Runs a k6 test script inside a Docker container.
#              Handles mounting the current directory, passing environment variables,
#              and specifying the k6 test file.
# Usage: ./k6-run-docker.sh <k6_script_path> [k6_options...]
# Example: ./k6-run-docker.sh src/test.ts --vus 10 --duration 30s
# Example: BASE_URL=http://localhost:8080 ./k6-run-docker.sh src/api_test.ts

set -e # Exit immediately if a command exits with a non-zero status.

K6_IMAGE="grafana/k6:latest"

# Check if k6 script path is provided
if [ -z "$1" ]; then
  echo "Usage: $0 <k6_script_path> [k6_options...]"
  echo "Example: $0 src/test.ts --vus 10 --duration 30s"
  exit 1
fi

K6_SCRIPT_PATH="$1"
shift # Remove the first argument (k6_script_path) from the list of arguments
K6_OPTIONS="$@" # Remaining arguments are k6 options

# Resolve absolute path for mounting
CURRENT_DIR=$(pwd)

# Collect environment variables starting with K6_ or passed directly
# This is a basic approach; for more robust handling, consider a whitelist
ENV_VARS=""
for var in $(env | grep -E '^(K6_|BASE_URL|API_KEY)'); do
  ENV_VARS+="-e $var "
done

# Check if the script exists locally before trying to run in Docker
if [ ! -f "$K6_SCRIPT_PATH" ]; then
  echo "Error: k6 script '$K6_SCRIPT_PATH' not found in the current directory." >&2
  exit 1
fi

echo "Running k6 test '$K6_SCRIPT_PATH' with Docker..."
echo "K6 Options: $K6_OPTIONS"
echo "Environment Variables: $ENV_VARS"

# Run k6 in Docker
# -v $(pwd):/k6:ro mounts the current directory as /k6 inside the container (read-only)
# --rm removes the container after exit
# $ENV_VARS passes collected environment variables
# $K6_IMAGE specifies the k6 Docker image
# run /k6/$(basename $K6_SCRIPT_PATH) executes the script inside the container
# $K6_OPTIONS passes additional k6 CLI options
docker run --rm \
  -v "$CURRENT_DIR":/k6:ro \
  $ENV_VARS \
  $K6_IMAGE run /k6/"$K6_SCRIPT_PATH" $K6_OPTIONS

EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
  echo "k6 test completed successfully." >&2
else
  echo "k6 test failed with exit code $EXIT_CODE." >&2
fi

exit $EXIT_CODE
