#!/bin/bash

# check-access.sh
# Description: Simulates an access check against a local RBAC policy file.
#              This script is for development and testing purposes to quickly verify
#              if a user with specific roles has permission to perform an action
#              on a resource based on a generated policy file.
#
# Usage:
#   ./check-access.sh -p <policy_file> -u <user_id> -r <role1,role2> -res <resource> -a <action>
#
# Examples:
#   ./check-access.sh -p rbac_policy.json -u user123 -r admin -res products -a delete
#   ./check-access.sh -p rbac_policy.yaml -u user456 -r editor,viewer -res orders -a read
#   ./check-access.sh --policy rbac_policy.json --user testuser --roles viewer --resource users --action read

POLICY_FILE=""
USER_ID=""
ROLES=""
RESOURCE=""
ACTION=""

# Function to display help message
display_help() {
    echo "Usage: $0 [OPTIONS]"
    echo "Simulates an RBAC access check against a local policy file."
    echo ""
    echo "Options:"
    echo "  -p, --policy <file>     Path to the RBAC policy file (JSON or YAML)."
    echo "  -u, --user <id>         User ID for the access check."
    echo "  -r, --roles <role1,role2> Comma-separated list of roles assigned to the user."
    echo "  -res, --resource <name> Resource name (e.g., 'products', 'users')."
    echo "  -a, --action <name>     Action name (e.g., 'read', 'write', 'delete')."
    echo "  -h, --help              Display this help message."
    echo ""
    echo "Examples:"
    echo "  $0 -p rbac_policy.json -u user123 -r admin -res products -a delete"
    echo "  $0 -p rbac_policy.yaml -u user456 -r editor,viewer -res orders -a read"
    exit 0
}

# Parse command-line arguments
while [[ "$#" -gt 0 ]]; do
    key="$1"
    case $key in
        -p|--policy)
        POLICY_FILE="$2"
        shift # past argument
        shift # past value
        ;;
        -u|--user)
        USER_ID="$2"
        shift # past argument
        shift # past value
        ;;
        -r|--roles)
        ROLES="$2"
        shift # past argument
        shift # past value
        ;;
        -res|--resource)
        RESOURCE="$2"
        shift # past argument
        shift # past value
        ;;
        -a|--action)
        ACTION="$2"
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

# Validate required arguments
if [ -z "$POLICY_FILE" ] || [ -z "$USER_ID" ] || [ -z "$ROLES" ] || [ -z "$RESOURCE" ] || [ -z "$ACTION" ]; then
    echo "Error: All arguments (-p, -u, -r, -res, -a) are required."
    display_help
fi

# Check if policy file exists
if [ ! -f "$POLICY_FILE" ]; then
    echo "Error: Policy file '$POLICY_FILE' not found."
    exit 1
fi

# Determine file type and parse using appropriate tool (jq for JSON, yq for YAML)
FILE_EXTENSION="${POLICY_FILE##*.}"

# Convert comma-separated roles to an array
IFS=',' read -r -a USER_ROLES_ARRAY <<< "$ROLES"

# Function to check permission
check_permission() {
    local policy_content="$1"
    local role_to_check="$2"
    local resource_to_check="$3"
    local action_to_check="$4"

    # Check if the role exists in the policy
    if ! echo "$policy_content" | grep -q "\"$role_to_check\":"; then
        return 1 # Role not found
    fi

    # Construct the permission string to look for
    local required_permission="${action_to_check}:${resource_to_check}"

    # Extract permissions for the given role and check if the required permission exists
    if [[ "$FILE_EXTENSION" == "json" ]]; then
        local role_permissions=$(echo "$policy_content" | jq -r ".permissions.\"$role_to_check\"[]")
    elif [[ "$FILE_EXTENSION" == "yaml" ]]; then
        # yq output is one item per line, so grep works well
        local role_permissions=$(echo "$policy_content" | yq ".permissions.\"$role_to_check\"[]" -r)
    fi

    if echo "$role_permissions" | grep -q "^${required_permission}$\""; then
        return 0 # Permission found
    else
        return 1 # Permission not found
    fi
}

POLICY_CONTENT=""
if [[ "$FILE_EXTENSION" == "json" ]]; then
    if ! command -v jq &> /dev/null;
    then
        echo "Error: 'jq' is not installed. Please install it to process JSON policy files."
        exit 1
    fi
    POLICY_CONTENT=$(cat "$POLICY_FILE")
elif [[ "$FILE_EXTENSION" == "yaml" ]]; then
    if ! command -v yq &> /dev/null;
    then
        echo "Error: 'yq' is not installed. Please install it to process YAML policy files (e.g., pip install yq or brew install yq)."
        exit 1
    fi
    POLICY_CONTENT=$(cat "$POLICY_FILE")
else
    echo "Error: Unsupported policy file format. Only JSON and YAML are supported."
    exit 1
fi

ACCESS_GRANTED=0
for role in "${USER_ROLES_ARRAY[@]}"; do
    if check_permission "$POLICY_CONTENT" "$role" "$RESOURCE" "$ACTION"; then
        echo -e "\e[32mAccess GRANTED\e[0m for user '${USER_ID}' with role '${role}' to perform '${ACTION}' on '${RESOURCE}'."
        ACCESS_GRANTED=1
        break # Access granted by at least one role
    fi
done

if [ $ACCESS_GRANTED -eq 0 ]; then
    echo -e "\e[31mAccess DENIED\e[0m for user '${USER_ID}' with roles '${ROLES}' to perform '${ACTION}' on '${RESOURCE}'."
    exit 1
fi
