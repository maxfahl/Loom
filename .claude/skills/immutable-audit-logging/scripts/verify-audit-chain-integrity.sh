#!/bin/bash

# verify-audit-chain-integrity.sh
# This script verifies the cryptographic chain integrity of a newline-delimited JSON (NDJSON) audit log file.
# Each log entry is expected to contain 'eventHash' and 'previousEventHash' fields.
# It simulates downloading logs and then performs a local verification.

# Usage:
#   ./verify-audit-chain-integrity.sh -f <path_to_audit_log_file>
#   ./verify-audit-chain-integrity.sh --file /path/to/your/audit.log

# Requirements:
#   - jq: A lightweight and flexible command-line JSON processor.
#   - shasum (or sha256sum): For calculating SHA256 hashes.

set -euo pipefail

# --- Configuration ---
LOG_FILE=""

# --- Helper Functions ---
print_help() {
  echo "Usage: $0 -f <path_to_audit_log_file>"
  echo ""
  echo "Verifies the cryptographic chain integrity of an NDJSON audit log file."
  echo "Each log entry must contain 'eventHash' and 'previousEventHash' fields."
  echo ""
  echo "Options:"
  echo "  -f, --file <path>  Path to the NDJSON audit log file."
  echo "  -h, --help         Display this help message."
  echo ""
  echo "Example:"
  echo "  $0 -f ./examples/audit.log"
  exit 0
}

# Function to check for required commands
check_dependencies() {
  if ! command -v jq &> /dev/null;
  then
    echo "Error: 'jq' is not installed. Please install it to run this script."
  echo "  On macOS: brew install jq"
  echo "  On Debian/Ubuntu: sudo apt-get install jq"
    exit 1
  fi
  if ! command -v shasum &> /dev/null && ! command -v sha256sum &> /dev/null;
  then
    echo "Error: 'shasum' or 'sha256sum' is not installed. Please install one to run this script."
  echo "  On macOS: it's usually pre-installed."
  echo "  On Debian/Ubuntu: sudo apt-get install coreutils (provides sha256sum)"
    exit 1
  fi
}

# Function to calculate SHA256 hash (cross-platform)
calculate_sha256() {
  if command -v shasum &> /dev/null;
  then
    echo -n "$1" | shasum -a 256 | awk '{print $1}'
  else # Assume sha256sum is available
    echo -n "$1" | sha256sum | awk '{print $1}'
  fi
}

# --- Main Logic ---

# Parse arguments
while [[ $# -gt 0 ]]; do
  key="$1"
  case $key in
    -f|--file)
      LOG_FILE="$2"
      shift # past argument
      shift # past value
      ;;
    -h|--help)
      print_help
      ;;
    *)
      echo "Unknown option: $1"
      print_help
      ;;
  esac
done

if [[ -z "$LOG_FILE" ]]; then
  echo "Error: Audit log file path is required."
  print_help
fi

if [[ ! -f "$LOG_FILE" ]]; then
  echo "Error: Log file not found at '$LOG_FILE'."
  exit 1
fi

check_dependencies

echo "Verifying integrity of audit log: '$LOG_FILE'"

# Read log entries into an array
mapfile -t LOG_ENTRIES < "$LOG_FILE"

if [[ ${#LOG_ENTRIES[@]} -eq 0 ]]; then
  echo "No log entries found in '$LOG_FILE'. Integrity check passed (no data to verify)."
  exit 0
fi

PREVIOUS_EVENT_HASH=""
INTEGRITY_VALID=true

for i in "${!LOG_ENTRIES[@]}"; do
  ENTRY="${LOG_ENTRIES[$i]}"
  EVENT_ID=$(echo "$ENTRY" | jq -r '.id // "N/A"' || echo "N/A")
  CURRENT_EVENT_HASH=$(echo "$ENTRY" | jq -r '.eventHash // ""' || echo "")
  EXPECTED_PREVIOUS_HASH=$(echo "$ENTRY" | jq -r '.previousEventHash // ""' || echo "")

  if [[ -z "$CURRENT_EVENT_HASH" ]]; then
    echo "Error: Event ID '$EVENT_ID' (line $((i+1))) is missing 'eventHash'. Cannot verify integrity."
    INTEGRITY_VALID=false
    break
  fi

  # Recalculate hash of the current entry (excluding its own eventHash for calculation)
  # We need to reconstruct the JSON without the 'eventHash' field for recalculation
  RECALCULATED_DATA=$(echo "$ENTRY" | jq 'del(.eventHash)')
  RECALCULATED_CURRENT_HASH=$(calculate_sha256 "$RECALCULATED_DATA")

  if [[ "$CURRENT_EVENT_HASH" != "$RECALCULATED_CURRENT_HASH" ]]; then
    echo "Error: Event ID '$EVENT_ID' (line $((i+1))) hash mismatch."
  echo "  Expected: $RECALCULATED_CURRENT_HASH"
  echo "  Actual:   $CURRENT_EVENT_HASH"
    INTEGRITY_VALID=false
    break
  fi

  if [[ "$EXPECTED_PREVIOUS_HASH" != "$PREVIOUS_EVENT_HASH" ]]; then
    echo "Error: Event ID '$EVENT_ID' (line $((i+1))) previousEventHash mismatch."
  echo "  Expected previous hash: $PREVIOUS_EVENT_HASH"
  echo "  Actual previous hash:   $EXPECTED_PREVIOUS_HASH"
    INTEGRITY_VALID=false
    break
  fi

  PREVIOUS_EVENT_HASH="$CURRENT_EVENT_HASH"
  echo "Event ID '$EVENT_ID' (line $((i+1))): Verified ✅"
done

if $INTEGRITY_VALID; then
  echo "\nAudit log chain integrity: VALID ✅"
  exit 0
else
  echo "\nAudit log chain integrity: COMPROMISED ❌"
  exit 1
fi
