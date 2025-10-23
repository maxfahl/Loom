#!/bin/bash

# OpenSSL mTLS Setup Script
#
# This script demonstrates how to generate a Certificate Authority (CA),
# server certificate, and client certificate using OpenSSL for mutual TLS (mTLS).
# This setup is suitable for development and testing environments to simulate
# secure communication where both client and server authenticate each other.
#
# Usage:
#   ./openssl_mtls_setup.sh --output-dir ./mtls_certs
#   ./openssl_mtls_setup.sh -h # For help
#
# Requirements:
#   - OpenSSL: Must be installed and available in your PATH.
#
# Features:
# - Generates a Root CA key and certificate.
# - Generates a server key, CSR, and certificate signed by the Root CA.
# - Generates a client key, CSR, and certificate signed by the Root CA.
# - Configurable output directory.
#
# Note: For production environments, consider using a dedicated PKI solution
#       or a private CA service from your cloud provider.

set -e

# --- Configuration Defaults ---
DEFAULT_OUTPUT_DIR="./mtls_certs"
CA_DAYS=3650 # 10 years
SERVER_DAYS=730 # 2 years
CLIENT_DAYS=365 # 1 year
KEY_SIZE=2048

# --- Functions ---

print_help() {
  echo "Usage: $(basename "$0") [OPTIONS]"
  echo "Generate CA, server, and client certificates for mTLS using OpenSSL."
  echo ""
  echo "Options:"
  echo "  --output-dir <PATH>    Output directory for generated files. Default: '$DEFAULT_OUTPUT_DIR'"
  echo "  -h, --help             Display this help message."
  echo ""
  echo "Examples:"
  echo "  $(basename "$0") --output-dir ./my_mtls_setup"
}

check_openssl_installed() {
  if ! command -v openssl &> /dev/null;
  then
    echo "Error: OpenSSL is not installed or not found in your PATH." >&2
    echo "Please install OpenSSL to use this script." >&2
    exit 1
  fi
}

# --- Main Logic ---

check_openssl_installed

OUTPUT_DIR="$DEFAULT_OUTPUT_DIR"

while [[ "$#" -gt 0 ]]; do
  key="$1"
  case $key in
    --output-dir)
      OUTPUT_DIR="$2"
      shift 2
      ;; 
    -h|--help)
      print_help
      exit 0
      ;; 
    *)
      echo "Unknown option: $1" >&2
      print_help
      exit 1
      ;; 
  esac
done

# Create output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"

echo "Generating Root CA..."
# Generate CA private key
openssl genrsa -out "${OUTPUT_DIR}/ca.key" "$KEY_SIZE"
# Generate CA certificate
openssl req -x509 -new -nodes -key "${OUTPUT_DIR}/ca.key" -sha256 -days "$CA_DAYS" \
    -out "${OUTPUT_DIR}/ca.crt" -subj "/C=US/ST=CA/L=SanFrancisco/O=MyOrg/OU=CA/CN=MyRootCA"
if [[ $? -ne 0 ]]; then echo "❌ Failed to generate CA." >&2; exit 1; fi
echo "✅ Root CA generated: ${OUTPUT_DIR}/ca.key, ${OUTPUT_DIR}/ca.crt"

echo "\nGenerating Server Certificate..."
# Generate server private key
openssl genrsa -out "${OUTPUT_DIR}/server.key" "$KEY_SIZE"
# Generate server CSR
openssl req -new -key "${OUTPUT_DIR}/server.key" -out "${OUTPUT_DIR}/server.csr" \
    -subj "/C=US/ST=CA/L=SanFrancisco/O=MyOrg/OU=Server/CN=localhost"
# Sign server certificate with CA
openssl x509 -req -in "${OUTPUT_DIR}/server.csr" -CA "${OUTPUT_DIR}/ca.crt" \
    -CAkey "${OUTPUT_DIR}/ca.key" -CAcreateserial -out "${OUTPUT_DIR}/server.crt" \
    -days "$SERVER_DAYS" -sha256
if [[ $? -ne 0 ]]; then echo "❌ Failed to generate server certificate." >&2; exit 1; fi
echo "✅ Server certificate generated: ${OUTPUT_DIR}/server.key, ${OUTPUT_DIR}/server.crt"

echo "\nGenerating Client Certificate..."
# Generate client private key
openssl genrsa -out "${OUTPUT_DIR}/client.key" "$KEY_SIZE"
# Generate client CSR
openssl req -new -key "${OUTPUT_DIR}/client.key" -out "${OUTPUT_DIR}/client.csr" \
    -subj "/C=US/ST=CA/L=SanFrancisco/O=MyOrg/OU=Client/CN=MyClient"
# Sign client certificate with CA
openssl x509 -req -in "${OUTPUT_DIR}/client.csr" -CA "${OUTPUT_DIR}/ca.crt" \
    -CAkey "${OUTPUT_DIR}/ca.key" -CAcreateserial -out "${OUTPUT_DIR}/client.crt" \
    -days "$CLIENT_DAYS" -sha256
if [[ $? -ne 0 ]]; then echo "❌ Failed to generate client certificate." >&2; exit 1; fi
echo "✅ Client certificate generated: ${OUTPUT_DIR}/client.key, ${OUTPUT_DIR}/client.crt"

echo "\nAll mTLS certificates and keys generated successfully in '$OUTPUT_DIR'."
