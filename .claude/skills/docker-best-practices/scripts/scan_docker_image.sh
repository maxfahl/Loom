#!/bin/bash

# Docker Image Vulnerability Scanner Wrapper
# This script uses Trivy to scan a Docker image for known vulnerabilities.
# Trivy: https://aquasecurity.github.io/trivy/

# --- Configuration ---
TRIVY_SEVERITY="HIGH,CRITICAL" # Comma-separated list of severities to report (UNKNOWN,LOW,MEDIUM,HIGH,CRITICAL)
TRIVY_FORMAT="table"         # Output format (table, json, template)

# --- Functions ---
print_help() {
  echo "Usage: $0 <image_name_or_id>"
  echo ""
  echo "Scans a Docker image for vulnerabilities using Trivy."
  echo ""
  echo "Arguments:"
  echo "  <image_name_or_id>  The name or ID of the Docker image to scan (e.g., my-app:latest, nginx:1.21)"
  echo ""
  echo "Configuration (Environment Variables):"
  echo "  TRIVY_SEVERITY  Comma-separated list of severities to report (default: ${TRIVY_SEVERITY})"
  echo "  TRIVY_FORMAT    Output format (default: ${TRIVY_FORMAT})"
  echo ""
  echo "Example:"
  echo "  $0 my-app:latest"
  echo "  TRIVY_SEVERITY=CRITICAL $0 my-app:prod"
  echo "  $0 --help"
}

check_trivy_installed() {
  if ! command -v trivy &> /dev/null
  then
    echo "Error: Trivy is not installed or not in your PATH."
    echo "Please install Trivy: https://aquasecurity.github.io/trivy/latest/getting-started/installation/"
    exit 1
  fi
}

# --- Main Script ---

# Check for help argument
if [[ "$1" == "--help" || "$1" == "-h" ]]; then
  print_help
  exit 0
fi

# Check if image name is provided
if [ -z "$1" ]; then
  echo "Error: No Docker image name or ID provided."
  print_help
  exit 1
fi

IMAGE_TO_SCAN="$1"

check_trivy_installed

echo "\n----------------------------------------------------"
echo "  Starting vulnerability scan for image: ${IMAGE_TO_SCAN}"
echo "  Reporting severities: ${TRIVY_SEVERITY}"
echo "----------------------------------------------------\n"

# Run Trivy scan
# --ignore-unfixed: Only show vulnerabilities that have a fix available
# --exit-code 1: Exit with 1 if vulnerabilities of specified severity are found
trivy image \
  --severity "${TRIVY_SEVERITY}" \
  --format "${TRIVY_FORMAT}" \
  --ignore-unfixed \
  "${IMAGE_TO_SCAN}"

TRIVY_EXIT_CODE=$?

if [ ${TRIVY_EXIT_CODE} -eq 0 ]; then
  echo "\n----------------------------------------------------"
  echo "  Scan completed: No vulnerabilities found with severity ${TRIVY_SEVERITY}."
  echo "----------------------------------------------------\n"
  exit 0
elif [ ${TRIVY_EXIT_CODE} -eq 1 ]; then
  echo "\n----------------------------------------------------"
  echo "  Scan completed: Vulnerabilities found with severity ${TRIVY_SEVERITY}."
  echo "  Please review the report above."
  echo "----------------------------------------------------\n"
  exit 1
else
  echo "\n----------------------------------------------------"
  echo "  Scan completed with unexpected exit code: ${TRIVY_EXIT_CODE}."
  echo "  An error might have occurred during the scan."
  echo "----------------------------------------------------\n"
  exit ${TRIVY_EXIT_CODE}
fi
