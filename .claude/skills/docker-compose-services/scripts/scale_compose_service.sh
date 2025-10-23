#!/bin/bash

# Docker Compose Service Scaler
# This script scales a specified service in a Docker Compose application.

# --- Functions ---
print_help() {
  echo "Usage: $0 <service_name> <replicas> [compose_file]"
  echo ""
  echo "Scales a Docker Compose service to the specified number of replicas."
  echo ""
  echo "Arguments:"
  echo "  <service_name>  The name of the service to scale (e.g., 'web', 'api')."
  echo "  <replicas>      The desired number of replicas for the service."
  echo "  [compose_file]  Optional: Path to the docker-compose.yml file (default: ./docker-compose.yml)."
  echo ""
  echo "Example:"
  echo "  $0 web 3                                  # Scale 'web' service to 3 replicas using default compose file"
  echo "  $0 api 1 ./docker-compose.prod.yml      # Scale 'api' service to 1 replica using a specific compose file"
  echo "  $0 --help"
}

# --- Main Script ---

# Check for help argument
if [[ "$1" == "--help" || "$1" == "-h" ]]; then
  print_help
  exit 0
fi

# Validate arguments
if [ "$#" -lt 2 ]; then
  echo "Error: Insufficient arguments provided."
  print_help
  exit 1
fi

SERVICE_NAME="$1"
REPLICAS="$2"
COMPOSE_FILE="${3:-docker-compose.yml}" # Default to docker-compose.yml if not provided

# Check if compose file exists
if [ ! -f "${COMPOSE_FILE}" ]; then
  echo "Error: Docker Compose file not found at '${COMPOSE_FILE}'."
  exit 1
fi

# Validate replicas is a number
if ! [[ "$REPLICAS" =~ ^[0-9]+$ ]]; then
  echo "Error: Replicas must be a positive integer."
  print_help
  exit 1
fi

echo "\n----------------------------------------------------"
echo "  Scaling service: ${SERVICE_NAME}"
echo "  To replicas: ${REPLICAS}"
echo "  Using Compose file: ${COMPOSE_FILE}"
echo "----------------------------------------------------\n"

# Execute the scale command
docker compose -f "${COMPOSE_FILE}" up -d --scale "${SERVICE_NAME}=${REPLICAS}" "${SERVICE_NAME}"

if [ $? -eq 0 ]; then
  echo "\n----------------------------------------------------"
  echo "  Successfully scaled service '${SERVICE_NAME}' to ${REPLICAS} replicas."
  echo "----------------------------------------------------\n"
  exit 0
elif [ $? -eq 1 ]; then
  echo "\n----------------------------------------------------"
  echo "  Failed to scale service '${SERVICE_NAME}'. Please check the logs above."
  echo "----------------------------------------------------\n"
  exit 1
fi
