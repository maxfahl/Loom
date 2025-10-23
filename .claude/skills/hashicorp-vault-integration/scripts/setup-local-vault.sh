#!/bin/bash

# setup-local-vault.sh
# Description: Sets up a local HashiCorp Vault server in development mode using Docker.
#              This script initializes, unseals, and enables a KV secrets engine for quick
#              development and testing purposes. It outputs the VAULT_ADDR and root token.
#
# Usage:
#   ./setup-local-vault.sh [--port <port>] [--kv-path <path>] [--no-docker-pull]
#
# Options:
#   --port <port>         Specify the port for Vault UI/API (default: 8200).
#   --kv-path <path>      Specify the path for the KV secrets engine (default: secret).
#   --no-docker-pull      Skip pulling the Docker image if it already exists.
#   -h, --help            Display this help message.
#
# Examples:
#   ./setup-local-vault.sh
#   ./setup-local-vault.sh --port 8201 --kv-path my-app-secrets
#   ./setup-local-vault.sh --no-docker-pull

VAULT_PORT=8200
KV_SECRETS_PATH="secret"
NO_DOCKER_PULL=false

# Function to display help message
display_help() {
    echo "Usage: $0 [OPTIONS]"
    echo "Sets up a local HashiCorp Vault server in development mode using Docker."
    echo ""
    echo "Options:"
    echo "  --port <port>         Specify the port for Vault UI/API (default: ${VAULT_PORT})."
    echo "  --kv-path <path>      Specify the path for the KV secrets engine (default: ${KV_SECRETS_PATH})."
    echo "  --no-docker-pull      Skip pulling the Docker image if it already exists."
    echo "  -h, --help            Display this help message."
    echo ""
    echo "Examples:"
    echo "  $0"
    echo "  $0 --port 8201 --kv-path my-app-secrets"
    echo "  $0 --no-docker-pull"
    exit 0
}

# Parse command-line arguments
while [[ "$#" -gt 0 ]]; do
    key="$1"
    case $key in
        --port)
        VAULT_PORT="$2"
        shift # past argument
        shift # past value
        ;;
        --kv-path)
        KV_SECRETS_PATH="$2"
        shift # past argument
        shift # past value
        ;;
        --no-docker-pull)
        NO_DOCKER_PULL=true
        shift # past argument
        ;;
        -h|--help)
        display_help
        ;;
        *)
        echo "Unknown option: $1"
        display_help
        ;;
    esac
done

# Check if Docker is running
if ! docker info &> /dev/null; then
    echo -e "\e[31mError: Docker is not running. Please start Docker and try again.\e[0m"
    exit 1
fi

# Stop and remove any existing Vault container
echo "Stopping and removing any existing 'dev-vault' container..."
docker stop dev-vault &> /dev/null
docker rm dev-vault &> /dev/null

# Pull Vault Docker image if not skipped
if [ "$NO_DOCKER_PULL" = false ]; then
    echo "Pulling HashiCorp Vault Docker image..."
    docker pull hashicorp/vault:latest
    if [ $? -ne 0 ]; then
        echo -e "\e[31mError: Failed to pull Docker image. Check your internet connection or Docker setup.\e[0m"
        exit 1
    fi
fi

echo "Starting Vault in development mode on port ${VAULT_PORT}..."
# Start Vault in dev mode, exposing the specified port
docker run -d --cap-add=IPC_LOCK --name dev-vault -p "${VAULT_PORT}:8200" hashicorp/vault:latest dev

# Wait for Vault to be ready
echo "Waiting for Vault to start..."
sleep 5 # Give Vault some time to start

VAULT_ADDR="http://127.0.0.1:${VAULT_PORT}"
export VAULT_ADDR

# Get the root token from the Docker logs
ROOT_TOKEN=$(docker logs dev-vault 2>&1 | grep 'Root Token:' | awk '{print $NF}')

if [ -z "$ROOT_TOKEN" ]; then
    echo -e "\e[31mError: Could not retrieve Vault root token. Check Docker logs for 'dev-vault'.\e[0m"
    exit 1
fi

export VAULT_TOKEN="$ROOT_TOKEN"

echo -e "\n\e[32mVault started successfully!\e[0m"
echo -e "\e[34m------------------------------------\e[0m"
echo -e "\e[34mVault Address: \e[33m${VAULT_ADDR}\e[0m"
echo -e "\e[34mRoot Token:    \e[33m${ROOT_TOKEN}\e[0m"
echo -e "\e[34m------------------------------------\e[0m"
echo ""

echo "Enabling KV Secrets Engine at path '${KV_SECRETS_PATH}'..."
vault secrets enable -path="${KV_SECRETS_PATH}" kv-v2
if [ $? -ne 0 ]; then
    echo -e "\e[31mError: Failed to enable KV secrets engine. Check Vault status.\e[0m"
    exit 1
fi
echo -e "\e[32mKV Secrets Engine enabled at '${KV_SECRETS_PATH}'.\e[0m"

echo "\nTo interact with Vault, set these environment variables in your current shell:"
echo "export VAULT_ADDR='${VAULT_ADDR}'"
echo "export VAULT_TOKEN='${ROOT_TOKEN}'"
echo ""
echo "You can access the Vault UI at: ${VAULT_ADDR}"
echo "Remember to stop the container with: docker stop dev-vault"
