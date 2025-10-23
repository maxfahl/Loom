#!/bin/bash

# OpenSSL Certificate Generator
#
# This script automates the generation of private keys, Certificate Signing Requests (CSRs),
# and self-signed X.509 certificates using OpenSSL. It's useful for development,
# testing, or for generating CSRs to be signed by a Certificate Authority (CA).
#
# Usage:
#   ./generate_cert.sh --cn myapp.example.com --org "My Company" --country US --output-dir ./certs
#   ./generate_cert.sh -h # For help
#
# Requirements:
#   - OpenSSL: Must be installed and available in your PATH.
#
# Features:
# - Generates a private key (RSA).
# - Generates a Certificate Signing Request (CSR).
# - Generates a self-signed certificate.
# - Configurable Common Name (CN), Organization (O), Country (C).
# - Configurable key size and certificate validity period.
# - Outputs files to a specified directory.

set -e

# --- Configuration Defaults ---
DEFAULT_KEY_SIZE=2048
DEFAULT_DAYS=365
DEFAULT_OUTPUT_DIR="."

# --- Functions ---

print_help() {
  echo "Usage: $(basename "$0") [OPTIONS]"
  echo "Generate private keys, CSRs, and self-signed certificates using OpenSSL."
  echo ""
  echo "Options:"
  echo "  --cn <COMMON_NAME>     Required: Common Name (e.g., myapp.example.com)."
  echo "  --org <ORGANIZATION>   Required: Organization (e.g., My Company)."
  echo "  --country <COUNTRY>    Required: Two-letter Country Code (e.g., US)."
  echo "  --output-dir <PATH>    Output directory for generated files. Default: '$DEFAULT_OUTPUT_DIR'"
  echo "  --key-size <BITS>      RSA key size in bits. Default: $DEFAULT_KEY_SIZE"
  echo "  --days <DAYS>          Certificate validity period in days. Default: $DEFAULT_DAYS"
  echo "  -h, --help             Display this help message."
  echo ""
  echo "Examples:"
  echo "  $(basename "$0") --cn api.example.com --org \"Example Inc.\" --country US --output-dir ./certs"
  echo "  $(basename "$0") --cn client.example.com --org \"Example Client\" --country GB --key-size 4096 --days 730"
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

COMMON_NAME=""
ORGANIZATION=""
COUNTRY=""
OUTPUT_DIR="$DEFAULT_OUTPUT_DIR"
KEY_SIZE="$DEFAULT_KEY_SIZE"
DAYS="$DEFAULT_DAYS"

while [[ "$#" -gt 0 ]]; do
  key="$1"
  case $key in
    --cn)
      COMMON_NAME="$2"
      shift 2
      ;;
    --org)
      ORGANIZATION="$2"
      shift 2
      ;;
    --country)
      COUNTRY="$2"
      shift 2
      ;;
    --output-dir)
      OUTPUT_DIR="$2"
      shift 2
      ;;
    --key-size)
      KEY_SIZE="$2"
      shift 2
      ;;
    --days)
      DAYS="$2"
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

if [[ -z "$COMMON_NAME" || -z "$ORGANIZATION" || -z "$COUNTRY" ]]; then
  echo "Error: --cn, --org, and --country are required." >&2
  print_help
  exit 1
fi

# Create output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"

FILE_PREFIX="$(echo "$COMMON_NAME" | tr '.' '-')"
KEY_FILE="${OUTPUT_DIR}/${FILE_PREFIX}.key"
CSR_FILE="${OUTPUT_DIR}/${FILE_PREFIX}.csr"
CERT_FILE="${OUTPUT_DIR}/${FILE_PREFIX}.crt"

SUBJECT="/C=${COUNTRY}/O=${ORGANIZATION}/CN=${COMMON_NAME}"

echo "Generating RSA private key (${KEY_SIZE} bits) for ${COMMON_NAME}..."
openssl genrsa -out "$KEY_FILE" "$KEY_SIZE"
if [[ $? -ne 0 ]]; then echo "❌ Failed to generate private key." >&2; exit 1; fi
echo "✅ Private key generated: ${KEY_FILE}"

echo "Generating Certificate Signing Request (CSR) for ${COMMON_NAME}..."
openssl req -new -key "$KEY_FILE" -out "$CSR_FILE" -subj "$SUBJECT"
if [[ $? -ne 0 ]]; then echo "❌ Failed to generate CSR." >&2; exit 1; fi
echo "✅ CSR generated: ${CSR_FILE}"

echo "Generating self-signed certificate (${DAYS} days validity) for ${COMMON_NAME}..."
openssl x509 -req -days "$DAYS" -in "$CSR_FILE" -signkey "$KEY_FILE" -out "$CERT_FILE"
if [[ $? -ne 0 ]]; then echo "❌ Failed to generate self-signed certificate." >&2; exit 1; fi
echo "✅ Self-signed certificate generated: ${CERT_FILE}"

echo "\nAll files generated successfully in '$OUTPUT_DIR'."
