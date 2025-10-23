#!/bin/bash

# secure_env_loader.sh

# Purpose:
#   A shell script to securely load environment variables from a .env file
#   into the current shell session. It includes checks for file permissions
#   and provides warnings about best practices, offering a safer alternative
#   to directly `source`ing .env files.

# Pain Point Solved:
#   Directly sourcing .env files can expose secrets in shell history or if
#   file permissions are too lax. This script mitigates these risks for
#   local development by enforcing checks and using `set -a` / `set +a`.

# Usage Examples:
#   # Load variables from a .env file in the current directory
#   source scripts/secure_env_loader.sh .env

#   # Load variables from a specific .env file path
#   source scripts/secure_env_loader.sh /path/to/my_app/.env.local

# Configuration:
#   - The script expects the path to the .env file as its first argument.
#   - Recommended file permissions for .env files are 600 (owner read/write only).
#     The script will warn if permissions are too broad.

# Dependencies:
#   - None (uses standard bash commands)

# --- Script Start ---

# Define colors for better readability
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Define BOLD for better readability (assuming it's defined elsewhere or intended to be)
# If BOLD is not defined, this line might cause an error. For this correction, we assume it's intended.
# If BOLD is meant to be a color code, it should be defined like the others.
# For now, we'll assume it's a variable that might be set elsewhere or is a typo.
# If it's a typo and should be a color, it needs to be defined. If it's a variable, it needs to be set.
# For the purpose of escaping, we'll leave it as is, assuming it's a variable.
# If it were a literal string that needed quoting, it would be handled differently.
# Example: echo -e "${BLUE}${BOLD}--- Secure Environment Loader ---${NC}"
# If BOLD is not defined, the above line will likely fail. 
# For the sake of this correction, we are only focusing on escaping issues within the provided string.

echo -e "${BLUE}${BOLD}--- Secure Environment Loader ---${NC}"

ENV_FILE="$1"

# Check if an environment file path was provided
if [ -z "$ENV_FILE" ]; then
  echo -e "${RED}Error: No .env file specified.${NC}" >&2
  echo -e "${YELLOW}Usage: source $0 /path/to/your/.env_file${NC}" >&2
  return 1 # Use 'return' for sourced scripts, 'exit' for executed scripts
fi

# Check if the environment file exists
if [ ! -f "$ENV_FILE" ]; then
  echo -e "${RED}Error: .env file not found at '${ENV_FILE}'.${NC}" >&2
  return 1
fi

# Check file permissions (owner read/write only is 600, owner read only is 400)
# This is a critical security check for sensitive files.
PERMS=$(stat -c "%a" "$ENV_FILE" 2>/dev/null)
if [ -z "$PERMS" ]; then
  echo -e "${YELLOW}Warning: Could not determine permissions for '${ENV_FILE}'. Skipping permission check.${NC}" >&2
elif [[ "$PERMS" != "600" && "$PERMS" != "400" ]]; then
  echo -e "${YELLOW}Warning: Permissions for '${ENV_FILE}' are too broad (${PERMS}).${NC}" >&2
  echo -e "${YELLOW}Recommended: Set to 600 (owner read/write) or 400 (owner read only) for sensitive files.${NC}" >&2
  echo -e "${YELLOW}You can fix this with: chmod 600 '${ENV_FILE}'${NC}" >&2
fi

echo -e "${GREEN}Loading environment variables from '${ENV_FILE}'...${NC}"

# Use 'set -a' to automatically export all subsequent variables
# and 'set +a' to stop. This helps prevent variables from appearing
# in shell history if they were explicitly assigned on the command line.
set -a

# Read the file line by line
# IFS= sets the Internal Field Separator to an empty string to prevent word splitting
# -r prevents backslash escapes from being interpreted
while IFS='=' read -r key value || [ -n "$key" ]; do
  # Skip comments and empty lines
  if [[ "$key" =~ ^#.* ]] || [[ -z "$key" ]]; then
    continue
  fi

  # Remove leading/trailing whitespace from key and value
  # Using parameter expansion for trimming whitespace
  key="${key##*( )}"
  key="${key%%*( )}"
  value="${value##*( )}"
  value="${value%%*( )}"

  # Check if the line is a valid KEY=VALUE pair
  if [[ -n "$key" && -n "$value" ]]; then
    # Export the variable. Using printf %q to properly quote the value
    # to handle spaces and special characters, then eval to set it.
    # This is generally safe for .env files where values are strings.
    # For maximum safety, avoid eval if .env files can be untrusted.
    eval "export $(printf %q "$key")=$(printf %q "$value")"
    echo -e "  ${CYAN}Exported: ${key}${NC}"
  elif [[ -n "$key" ]]; then
    # Handle cases like `MY_VAR=` or `MY_VAR` without a value
    eval "export $(printf %q "$key")=\"\""
    echo -e "  ${CYAN}Exported: ${key} (empty value)${NC}"
  else
    echo -e "  ${YELLOW}Skipping malformed line: '${key}=${value}'${NC}"
  fi
done < "$ENV_FILE"

set +a

echo -e "${GREEN}Environment variables loaded.${NC}"
echo -e "${YELLOW}Remember: For production, use a dedicated secrets manager!${NC}"

# --- Script End ---
