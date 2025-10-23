#!/bin/bash

# inject-secrets-env.sh
# Description: Fetches secrets from a local HashiCorp Vault instance and exports them
#              as environment variables for a child process. This is useful for local
#              development and testing where applications need Vault secrets.
#
# Usage:
#   ./inject-secrets-env.sh -a <vault_addr> -t <vault_token> -p <secret_path> -- <command_to_run>
#
# Options:
#   -a, --vault-addr <address>    Vault server address (e.g., http://127.0.0.1:8200).
#   -t, --vault-token <token>     Vault authentication token (e.g., root token or AppRole token).
#   -p, --secret-path <path>      Path to the KV secret in Vault (e.g., secret/data/my-app/config).
#   -h, --help                    Display this help message.
#
# Examples:
#   ./inject-secrets-env.sh -a http://127.0.0.1:8200 -t s.xxxxxx -p secret/data/my-app/config -- node app.js
#   ./inject-secrets-env.sh -a $VAULT_ADDR -t $VAULT_TOKEN -p secret/data/database -- npm start

VAULT_ADDR=""
VAULT_TOKEN=""
SECRET_PATH=""

# Function to display help message
display_help() {
    echo "Usage: $0 [OPTIONS] -- <command_to_run>"
    echo "Fetches secrets from Vault and injects them as environment variables for a child process."
    echo ""
    echo "Options:"
    echo "  -a, --vault-addr <address>    Vault server address (e.g., http://127.0.0.1:8200)."
    echo "  -t, --vault-token <token>     Vault authentication token."
    echo "  -p, --secret-path <path>      Path to the KV secret in Vault (e.g., secret/data/my-app/config)."
    echo "  -h, --help                    Display this help message."
    echo ""
    echo "Examples:"
    echo "  $0 -a http://127.0.0.1:8200 -t s.xxxxxx -p secret/data/my-app/config -- node app.js"
    echo "  $0 -a \$VAULT_ADDR -t \$VAULT_TOKEN -p secret/data/database -- npm start"
    exit 0
}

# Parse command-line arguments
while [[ "$#" -gt 0 ]]; do
    key="$1"
    case $key in
        -a|--vault-addr)
        VAULT_ADDR="$2"
        shift # past argument
        shift # past value
        ;;
        -t|--vault-token)
        VAULT_TOKEN="$2"
        shift # past argument
        shift # past value
        ;;
        -p|--secret-path)
        SECRET_PATH="$2"
        shift # past argument
        shift # past value
        ;;
        -h|--help)
        display_help
        ;;
        --)
        shift # past --
        break # stop processing arguments
        ;;
        *)
        echo "Unknown option: $1"
        display_help
        ;;
    esac
done

# The command to run is now in "$@"
COMMAND_TO_RUN="$@"

# Validate required arguments
if [ -z "$VAULT_ADDR" ] || [ -z "$VAULT_TOKEN" ] || [ -z "$SECRET_PATH" ] || [ -z "$COMMAND_TO_RUN" ]; then
    echo -e "\e[31mError: All Vault connection details (-a, -t, -p) and a command to run are required.\e[0m"
    display_help
fi

# Check for 'vault' CLI tool
if ! command -v vault &> /dev/null; then
    echo -e "\e[31mError: HashiCorp Vault CLI tool not found. Please install it.\e[0m"
    exit 1
fi

export VAULT_ADDR="$VAULT_ADDR"
export VAULT_TOKEN="$VAULT_TOKEN"

echo -e "\e[34mFetching secrets from Vault at '$\{SECRET_PATH\}'...\e[0m"

# Fetch secrets using Vault CLI and parse with jq
SECRETS_JSON=$(vault kv get -format=json "$SECRET_PATH" 2>/dev/null)

if [ $? -ne 0 ]; then
    echo -e "\e[31mError: Failed to fetch secrets from Vault. Check VAULT_ADDR, VAULT_TOKEN, and SECRET_PATH.\e[0m"
    echo "Vault CLI output:"
    vault kv get -format=json "$SECRET_PATH"
    exit 1
fi

# Extract data from the 'data' field of the KV v2 response
SECRET_DATA=$(echo "$SECRETS_JSON" | jq -r '.data.data')

if [ "$SECRET_DATA" == "null" ] || [ -z "$SECRET_DATA" ]; then
    echo -e "\e[31mError: No secret data found at '$\{SECRET_PATH\}' or path is incorrect.\e[0m"
    exit 1
fi

# Export each key-value pair as an environment variable
while IFS='=' read -r key value; do
    if [[ ! -z "$key" ]]; then
        export "$key"="$value"
        echo -e "\e[32mExported: \e[33m$key\e[0m"
    fi
done < <(echo "$SECRET_DATA" | jq -r 'to_entries|map("\(.key)=\(.value)")|.[]')

echo -e "\e[34mSecrets injected. Running command: \e[33m${COMMAND_TO_RUN}\e[0m"

# Execute the provided command
exec $COMMAND_TO_RUN
