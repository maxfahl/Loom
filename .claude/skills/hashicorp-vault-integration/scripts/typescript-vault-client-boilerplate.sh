#!/bin/bash

# typescript-vault-client-boilerplate.sh
# Description: Generates boilerplate TypeScript code for interacting with a Vault KV secrets engine
#              using the 'hashi-vault-js' client library. This script helps quickly set up
#              a basic Vault client wrapper and example usage in a TypeScript project.
#
# Usage:
#   ./typescript-vault-client-boilerplate.sh [--output-dir <directory>] [--client-name <name>]
#
# Options:
#   --output-dir <directory>  Specify the output directory for the generated files (default: src/vault).
#   --client-name <name>      Specify the base name for the generated client files (default: vault-client).
#   -h, --help                Display this help message.
#
# Examples:
#   ./typescript-vault-client-boilerplate.sh
#   ./typescript-vault-client-boilerplate.sh --output-dir src/config --client-name secrets-manager

OUTPUT_DIR="src/vault"
CLIENT_NAME="vault-client"

# Function to display help message
display_help() {
    echo "Usage: $0 [OPTIONS]"
    echo "Generates boilerplate TypeScript code for HashiCorp Vault client integration."
    echo ""
    echo "Options:"
    echo "  --output-dir <directory>  Specify the output directory for the generated files (default: ${OUTPUT_DIR})."
    echo "  --client-name <name>      Specify the base name for the generated client files (default: ${CLIENT_NAME})."
    echo "  -h, --help                Display this help message."
    echo ""
    echo "Examples:"
    echo "  $0"
    echo "  $0 --output-dir src/config --client-name secrets-manager"
    exit 0
}

# Parse command-line arguments
while [[ "$#" -gt 0 ]]; do
    key="$1"
    case $key in
        --output-dir)
        OUTPUT_DIR="$2"
        shift # past argument
        shift # past value
        ;;
        --client-name)
        CLIENT_NAME="$2"
        shift # past argument
        shift # past value
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

# Create output directory
mkdir -p "${OUTPUT_DIR}"

echo "Installing 'hashi-vault-js' and '@types/node' (if not already installed)..."
# Check if npm is available
if ! command -v npm &> /dev/null; then
    echo -e "\e[31mError: npm not found. Please install Node.js and npm.\e[0m"
    exit 1
fi

# Check if hashi-vault-js is already in package.json
if ! grep -q "hashi-vault-js" package.json 2>/dev/null; then
    npm install hashi-vault-js
    if [ $? -ne 0 ]; then
        echo -e "\e[31mError: Failed to install hashi-vault-js. Check npm or network connection.\e[0m"
        exit 1
    fi
fi

# Check if @types/node is already in package.json
if ! grep -q "@types/node" package.json 2>/dev/null; then
    npm install --save-dev @types/node
    if [ $? -ne 0 ]; then
        echo -e "\e[31mError: Failed to install @types/node. Check npm or network connection.\e[0m"
        exit 1
    fi
fi

# Create Vault client service file
CLIENT_FILE="${OUTPUT_DIR}/${CLIENT_NAME}.service.ts"
echo "Creating ${CLIENT_FILE}..."
cat <<EOF > "${CLIENT_FILE}"
import Vault from 'hashi-vault-js';

/**
 * Configuration interface for the Vault client.
 */
export interface VaultClientConfig {
  vaultAddr: string;
  vaultToken?: string; // For dev/testing, use AppRole/K8s auth in production
  apiVersion?: string;
}

/**
 * A service class to interact with HashiCorp Vault.
 * Encapsulates the 'hashi-vault-js' client and provides common operations.
 */
export class VaultClientService {
  private vault: Vault;
  private readonly vaultAddr: string;

  constructor(config?: VaultClientConfig) {
    this.vaultAddr = config?.vaultAddr || process.env.VAULT_ADDR || '';
    const vaultToken = config?.vaultToken || process.env.VAULT_TOKEN;

    if (!this.vaultAddr) {
      throw new Error('Vault address (VAULT_ADDR) is not set. Provide it via config or environment variable.');
    }

    // In production, prefer authentication methods like AppRole, Kubernetes Auth, etc.
    // Direct token usage should be limited to development or highly controlled environments.
    this.vault = new Vault({
      apiVersion: config?.apiVersion || 'v1',
      endpoint: this.vaultAddr,
      token: vaultToken, // Be cautious with direct token usage in production
    });

    console.log(`VaultClientService initialized for ${this.vaultAddr}`);
  }

  /**
   * Authenticates with Vault using a token.
   * In production, consider using more secure methods like AppRole or Kubernetes Auth.
   * @param token The Vault token to use for authentication.
   */
  public setToken(token: string): void {
    this.vault.token = token;
    console.log('Vault token updated.');
  }

  /**
   * Reads a secret from the KV secrets engine (v2).
   * @param path The full path to the secret (e.g., 'secret/data/my-app/config').
   * @returns A promise that resolves with the secret data.
   */
  public async readKvSecret<T>(path: string): Promise<T | undefined> {
    try {
      const response = await this.vault.read(path);
      if (response && response.data && response.data.data) {
        console.log(`Successfully read secret from ${path}`);
        return response.data.data as T;
      } else {
        console.warn(`No data found at path: ${path}`);
        return undefined;
      }
    } catch (error) {
      console.error(`Error reading secret from Vault at ${path}:`, error);
      throw error;
    }
  }

  /**
   * Writes a secret to the KV secrets engine (v2).
   * @param path The full path to the secret (e.g., 'secret/data/my-app/config').
   * @param data The data to write as key-value pairs.
   * @returns A promise that resolves when the secret is written.
   */
  public async writeKvSecret(path: string, data: { [key: string]: any }): Promise<void> {
    try {
      await this.vault.write(path, { data });
      console.log(`Successfully wrote secret to ${path}`);
    } catch (error) {
      console.error(`Error writing secret to Vault at ${path}:`, error);
      throw error;
    }
  }

  /**
   * Deletes a secret from the KV secrets engine (v2).
   * @param path The full path to the secret.
   * @returns A promise that resolves when the secret is deleted.
   */
  public async deleteKvSecret(path: string): Promise<void> {
    try {
      await this.vault.delete(path);
      console.log(`Successfully deleted secret from ${path}`);
    } catch (error) {
      console.error(`Error deleting secret from Vault at ${path}:`, error);
      throw error;
    }
  }

  // Add more methods for other Vault operations (e.g., dynamic secrets, transit engine) as needed.
}
EOF

# Create example usage file
EXAMPLE_FILE="${OUTPUT_DIR}/${CLIENT_NAME}.example.ts"
echo "Creating ${EXAMPLE_FILE}..."
cat <<EOF > "${EXAMPLE_FILE}"
import { VaultClientService } from './${CLIENT_NAME}.service';

// Define an interface for your application's secrets
interface AppConfigSecrets {
  DATABASE_URL: string;
  API_KEY: string;
  SERVICE_ACCOUNT_EMAIL?: string;
}

async function runVaultExample() {
  try {
    // Initialize VaultClientService. It will try to use VAULT_ADDR and VAULT_TOKEN from env vars.
    // For production, consider passing a config object with specific auth methods.
    const vaultService = new VaultClientService();

    const secretPath = 'secret/data/my-app/config';

    // 1. Write a secret
    console.log('\n--- Writing Secret ---');
    await vaultService.writeKvSecret(secretPath, {
      DATABASE_URL: 'postgres://user:password@db:5432/mydb',
      API_KEY: 'super-secret-api-key-123',
      SERVICE_ACCOUNT_EMAIL: 'app@example.com',
    });

    // 2. Read the secret
    console.log('\n--- Reading Secret ---');
    const appSecrets = await vaultService.readKvSecret<AppConfigSecrets>(secretPath);
    if (appSecrets) {
      console.log('Retrieved Secrets:');
      console.log(`  DATABASE_URL: ${appSecrets.DATABASE_URL}`);
      console.log(`  API_KEY: ${appSecrets.API_KEY}`);
      console.log(`  SERVICE_ACCOUNT_EMAIL: ${appSecrets.SERVICE_ACCOUNT_EMAIL}`);
    }

    // 3. Update a secret (by writing to the same path)
    console.log('\n--- Updating Secret ---');
    await vaultService.writeKvSecret(secretPath, {
      DATABASE_URL: 'postgres://newuser:newpassword@newdb:5432/newmydb',
      API_KEY: 'updated-api-key-456',
    });

    const updatedSecrets = await vaultService.readKvSecret<AppConfigSecrets>(secretPath);
    if (updatedSecrets) {
      console.log('Updated Secrets:');
      console.log(`  DATABASE_URL: ${updatedSecrets.DATABASE_URL}`);
      console.log(`  API_KEY: ${updatedSecrets.API_KEY}`);
    }

    // 4. Delete the secret (uncomment to run)
    // console.log('\n--- Deleting Secret ---');
    // await vaultService.deleteKvSecret(secretPath);
    // const deletedSecrets = await vaultService.readKvSecret<AppConfigSecrets>(secretPath);
    // if (!deletedSecrets) {
    //   console.log('Secret successfully deleted.');
    // }

  } catch (error) {
    console.error('Vault example failed:', error);
  }
}

runVaultExample();
EOF

echo "\n\e[32mHashiCorp Vault TypeScript client boilerplate generated successfully in ${OUTPUT_DIR}/\e[0m"
echo "To run the example, ensure you have a Vault server running (e.g., using setup-local-vault.sh) and VAULT_ADDR/VAULT_TOKEN are set."
echo "Then navigate to your project root and run:"
echo "  \e[36mts-node ${EXAMPLE_FILE}\e[0m" # Assuming ts-node is installed
