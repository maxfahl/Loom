#!/bin/bash

# validate_jwt.sh

# Purpose:
#   Provides a quick command-line utility to decode a JWT, display its header and payload,
#   and perform basic checks like expiration. It helps developers quickly inspect tokens
#   received from APIs or generated during development.

# Pain Point Solved:
#   Debugging JWT issues often involves copying tokens to online decoders. This script
#   offers a local, quick, and scriptable alternative, enhancing security by keeping
#   sensitive tokens off third-party websites.

# Usage Examples:
#   # Validate a JWT token
#   bash scripts/validate_jwt.sh <your_jwt_token>
#   bash scripts/validate_jwt.sh eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c

# Dependencies:
#   - base64: Usually available on most Unix-like systems (part of coreutils).
#   - jq: A lightweight and flexible command-line JSON processor. Install with:
#         sudo apt-get install jq (Debian/Ubuntu)
#         brew install jq (macOS)
#         choco install jq (Windows via Chocolatey)

# --- Script Start ---

# Check for necessary commands
command -v base64 >/dev/null 2>&1 || { echo >&2 "Error: 'base64' command not found. Please install it (usually part of coreutils)."; exit 1; }
command -v jq >/dev/null 2>&1 || { echo >&2 "Error: 'jq' command not found. Please install it (e.g., 'sudo apt-get install jq' or 'brew install jq')."; exit 1; }

# Function to base64url decode
base64url_decode() {
  local input=$1
  # Convert base64url to standard base64 characters
  local standard_base64=$(echo "$input" | tr -d '\n' | sed 's/-/+/g; s/_/\/+/g')

  # Add padding if necessary for standard base64 decoding
  # The length of base64 string must be a multiple of 4
  local len=${#standard_base64}
  local remainder=$((len % 4))
  local padded_base64="$standard_base64"
  if [ "$remainder" -eq 2 ]; then
    padded_base64="${standard_base64}=="
  elif [ "$remainder" -eq 3 ]; then
    padded_base64="${standard_base64}="
  fi

  echo "$padded_base64" | base64 --decode 2>/dev/null
}

# Check if a JWT token is provided as an argument
if [ -z "$1" ]; then
  echo "Usage: $0 <jwt_token>"
  echo "Example: $0 eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
  exit 1
fi

JWT_TOKEN="$1"

# Split the token into its three parts
IFS='.' read -r JWT_HEADER_ENC JWT_PAYLOAD_ENC JWT_SIGNATURE_ENC <<< "$JWT_TOKEN"

if [ -z "$JWT_HEADER_ENC" ] || [ -z "$JWT_PAYLOAD_ENC" ] || [ -z "$JWT_SIGNATURE_ENC" ]; then
  echo "Error: Invalid JWT format. Expected 3 parts separated by dots."
  exit 1
fi

echo "\033[1;34m--- JWT Token Parts ---\033[0m"
echo "\033[0;36mHeader (Encoded):\033[0m   $JWT_HEADER_ENC"
echo "\033[0;36mPayload (Encoded):\033[0m  $JWT_PAYLOAD_ENC"
echo "\033[0;36mSignature (Encoded):\033[0m $JWT_SIGNATURE_ENC"
echo ""

echo "\033[1;34m--- Decoding Header ---\033[0m"
DECODED_HEADER=$(base64url_decode "$JWT_HEADER_ENC")
if [ -z "$DECODED_HEADER" ]; then
  echo "\033[0;31mError: Could not decode header. Is it valid base64url?\033[0m"
  exit 1
fi
echo "$DECODED_HEADER" | jq .
echo ""

echo "\033[1;34m--- Decoding Payload ---\033[0m"
DECODED_PAYLOAD=$(base64url_decode "$JWT_PAYLOAD_ENC")
if [ -z "$DECODED_PAYLOAD" ]; then
  echo "\033[0;31mError: Could not decode payload. Is it valid base64url?\033[0m"
  exit 1
fi
echo "$DECODED_PAYLOAD" | jq .
echo ""

echo "\033[1;34m--- Signature Verification (Conceptual) ---\033[0m"
echo "Signature verification is crucial for JWT security but is complex to implement purely in a shell script."
echo "It requires:"
echo "1. The algorithm specified in the header (e.g., HS256, RS256)."
echo "2. The secret key (for HS256) or public key (for RS256) used to sign the token."
echo ""
echo "For HS256, you would typically re-sign the '\033[0;33m$JWT_HEADER_ENC.$JWT_PAYLOAD_ENC\033[0m' part with the secret key"
echo "and compare the result with '\033[0;33m$JWT_SIGNATURE_ENC\033[0m'."
echo ""
echo "For RS256/ES256, you would use the public key to verify the signature against the header.payload part."
echo "This often involves tools like 'openssl' with specific commands, which vary based on the algorithm and key format."
echo "\033[0;33mThis script does NOT perform cryptographic signature verification.\033[0m"
echo ""

# Extract algorithm from header for more context
ALGORITHM=$(echo "$DECODED_HEADER" | jq -r '.alg')
if [ "$ALGORITHM" != "null" ]; then
  echo "\033[0;32mAlgorithm (alg) from header:\033[0m $ALGORITHM"
else
  echo "\033[0;31mCould not extract algorithm from header.\033[0m"
fi

echo "\033[1;34m--- Token Claims Validation ---\033[0m"

# Check for expiration time (exp)
EXPIRATION_TIME=$(echo "$DECODED_PAYLOAD" | jq -r '.exp')
if [ "$EXPIRATION_TIME" != "null" ] && [ "$EXPIRATION_TIME" != "" ]; then
  if [[ "$EXPIRATION_TIME" =~ ^[0-9]+$ ]]; then
    CURRENT_TIME=$(date +%s)
    if (( CURRENT_TIME > EXPIRATION_TIME )); then
      echo "\033[0;31mToken Status: EXPIRED!\033[0m"
      echo "  Expiration time: $(date -r $EXPIRATION_TIME 2>/dev/null || echo "Invalid timestamp") (Unix: $EXPIRATION_TIME)"
      echo "  Current time:    $(date -r $CURRENT_TIME 2>/dev/null || echo "Invalid timestamp") (Unix: $CURRENT_TIME)"
    else
      echo "\033[0;32mToken Status: VALID (not expired).\033[0m"
      echo "  Expiration time: $(date -r $EXPIRATION_TIME 2>/dev/null || echo "Invalid timestamp") (Unix: $EXPIRATION_TIME)"
      echo "  Current time:    $(date -r $CURRENT_TIME 2>/dev/null || echo "Invalid timestamp") (Unix: $CURRENT_TIME)"
      TIME_LEFT=$((EXPIRATION_TIME - CURRENT_TIME))
      echo "  Time remaining:  $((TIME_LEFT / 3600))h $(( (TIME_LEFT % 3600) / 60 ))m $((TIME_LEFT % 60))s"
    fi
  else
    echo "\033[0;33mWarning: Expiration time (exp) in payload is not a valid Unix timestamp: $EXPIRATION_TIME\033[0m"
  fi
else
  echo "\033[0;33mWarning: No expiration time (exp) claim found in payload. Token will not expire naturally.\033[0m"
fi

# Check for issued at time (iat)
ISSUED_AT_TIME=$(echo "$DECODED_PAYLOAD" | jq -r '.iat')
if [ "$ISSUED_AT_TIME" != "null" ] && [ "$ISSUED_AT_TIME" != "" ]; then
  if [[ "$ISSUED_AT_TIME" =~ ^[0-9]+$ ]]; then
    echo "\033[0;32mIssued at (iat):\033[0m $(date -r $ISSUED_AT_TIME 2>/dev/null || echo "Invalid timestamp") (Unix: $ISSUED_AT_TIME)"
  else
    echo "\033[0;33mWarning: Issued at time (iat) in payload is not a valid Unix timestamp: $ISSUED_AT_TIME\033[0m"
  fi
else
  echo "\033[0;33mWarning: No issued at time (iat) claim found in payload.\033[0m"
fi

# Check for not before time (nbf)
NOT_BEFORE_TIME=$(echo "$DECODED_PAYLOAD" | jq -r '.nbf')
if [ "$NOT_BEFORE_TIME" != "null" ] && [ "$NOT_BEFORE_TIME" != "" ]; then
  if [[ "$NOT_BEFORE_TIME" =~ ^[0-9]+$ ]]; then
    CURRENT_TIME=$(date +%s)
    if (( CURRENT_TIME < NOT_BEFORE_TIME )); then
      echo "\033[0;31mToken Status: NOT YET VALID (nbf)!\033[0m"
      echo "  Not before time: $(date -r $NOT_BEFORE_TIME 2>/dev/null || echo "Invalid timestamp") (Unix: $NOT_BEFORE_TIME)"
      echo "  Current time:    $(date -r $CURRENT_TIME 2>/dev/null || echo "Invalid timestamp") (Unix: $CURRENT_TIME)"
    else
      echo "\033[0;32mToken Status: VALID (past nbf).\033[0m"
      echo "  Not before time: $(date -r $NOT_BEFORE_TIME 2>/dev/null || echo "Invalid timestamp") (Unix: $NOT_BEFORE_TIME)"
      echo "  Current time:    $(date -r $CURRENT_TIME 2>/dev/null || echo "Invalid timestamp") (Unix: $CURRENT_TIME)"
    fi
  else
    echo "\033[0;33mWarning: Not before time (nbf) in payload is not a valid Unix timestamp: $NOT_BEFORE_TIME\033[0m"
  fi
else
  echo "\033[0;33mWarning: No not before time (nbf) claim found in payload.\033[0m"
fi

# Check for issuer (iss)
ISSUER=$(echo "$DECODED_PAYLOAD" | jq -r '.iss')
if [ "$ISSUER" != "null" ] && [ "$ISSUER" != "" ]; then
  echo "\033[0;32mIssuer (iss):\033[0m $ISSUER"
else
  echo "\033[0;33mWarning: No issuer (iss) claim found in payload.\033[0m"
fi

# Check for audience (aud)
AUDIENCE=$(echo "$DECODED_PAYLOAD" | jq -r '.aud')
if [ "$AUDIENCE" != "null" ] && [ "$AUDIENCE" != "" ]; then
  echo "\033[0;32mAudience (aud):\033[0m $AUDIENCE"
else
  echo "\033[0;33mWarning: No audience (aud) claim found in payload.\033[0m"
fi

# Check for Key ID (kid) in header
KID=$(echo "$DECODED_HEADER" | jq -r '.kid')
if [ "$KID" != "null" ] && [ "$KID" != "" ]; then
  echo "\033[0;32mKey ID (kid) in header:\033[0m $KID"
else
  echo "\033[0;33mWarning: No Key ID (kid) found in header. Consider adding for key rotation management.\033[0m"
fi
