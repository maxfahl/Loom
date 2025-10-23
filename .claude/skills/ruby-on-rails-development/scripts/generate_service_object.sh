#!/bin/bash

# generate_service_object.sh
#
# Description:
#   Scaffolds a new Ruby Service Object in a Rails application.
#   Service Objects encapsulate complex business logic, keeping controllers and models lean.
#   This script creates a file in `app/services/` with a basic class structure,
#   including an `initialize` method and a `call` method.
#
# Usage:
#   ./generate_service_object.sh <ServiceObjectName> [OPTIONS]
#
# Arguments:
#   <ServiceObjectName>  The name of the service object (e.g., CreateUser, ProcessOrder).
#                        Will be converted to snake_case for the filename.
#
# Options:
#   -h, --help           Display this help message.
#   -d, --dry-run        Show what would be created without actually creating the file.
#
# Example Usage:
#   ./generate_service_object.sh CreateUser
#   ./generate_service_object.sh ProcessPayment --dry-run
#
# Production-ready features:
#   - Argument parsing with help text.
#   - Dry-run mode.
#   - Error handling for missing arguments and existing files.
#   - Standard Rails directory structure assumption.
#   - Basic class template.

# --- Configuration ---
SERVICES_DIR="app/services"
# ---------------------

# Function to display help message
display_help() {
  echo "Usage: $0 <ServiceObjectName> [OPTIONS]"
  echo ""
  echo "Arguments:"
  echo "  <ServiceObjectName>  The name of the service object (e.g., CreateUser, ProcessOrder)."
  echo "                       Will be converted to snake_case for the filename."
  echo ""
  echo "Options:"
  echo "  -h, --help           Display this help message."
  echo "  -d, --dry-run        Show what would be created without actually creating the file."
  echo ""
  echo "Example Usage:"
  echo "  $0 CreateUser"
  echo "  $0 ProcessPayment --dry-run"
  exit 0
}

# Function to convert CamelCase to snake_case
camel_to_snake() {
  echo "$1" | sed -r 's/([A-Z]+)([A-Z][a-z])/\1_\2/g' | sed -r 's/([a-z\d])([A-Z])/\1_\2/g' | tr '-' '_' | tr '[:upper:]' '[:lower:]'
}

# Parse arguments
SERVICE_NAME=""
DRY_RUN=false

while [[ "$#" -gt 0 ]]; do
  case "$1" in
    -h|--help)
      display_help
      ;;
    -d|--dry-run)
      DRY_RUN=true
      ;;
    *)
      if [[ -z "$SERVICE_NAME" ]]; then
        SERVICE_NAME="$1"
      else
        echo "Error: Unknown argument or too many arguments: $1" >&2
        display_help
      fi
      ;;
  esac
  shift
done

# Validate SERVICE_NAME
if [[ -z "$SERVICE_NAME" ]]; then
  echo "Error: Service Object name is required." >&2
  display_help
fi

# Convert service name to snake_case for filename
FILE_NAME="$(camel_to_snake "$SERVICE_NAME")_service.rb"
FILE_PATH="$SERVICES_DIR/$FILE_NAME"

# Ensure the services directory exists
if [[ ! -d "$SERVICES_DIR" ]]; then
  echo "Creating directory: $SERVICES_DIR"
  if ! $DRY_RUN; then
    mkdir -p "$SERVICES_DIR" || { echo "Error: Could not create directory $SERVICES_DIR" >&2; exit 1; }
  fi
fi

# Check if file already exists
if [[ -f "$FILE_PATH" ]]; then
  echo "Error: Service Object file '$FILE_PATH' already exists. Aborting." >&2
  exit 1
fi

# Generate file content
CLASS_NAME="${SERVICE_NAME}Service"
FILE_CONTENT='''\
# frozen_string_literal: true

class ${CLASS_NAME}
  # Initializes the service with necessary parameters.
  # @param args [Hash] A hash of arguments required by the service.
  def initialize(**args)
    # Example: @user = args[:user]
    # Example: @params = args[:params]
  end

  # Executes the core logic of the service.
  # @return [OpenStruct] A result object indicating success/failure and any relevant data.
  def call
    # Implement your business logic here.
    #
    # Example:
    # if some_condition_is_met?
    #   # Perform actions
    #   OpenStruct.new(success?: true, data: "Operation successful")
    # else
    #   OpenStruct.new(success?: false, error: "Operation failed: reason")
    # end
    OpenStruct.new(success?: false, error: "Service logic not implemented yet.")
  end

  private

  # Add private helper methods here if needed.
  # def some_private_method
  #   # ...
  # end
end
'''

# Output or create file
if $DRY_RUN; then
  echo "--- Dry Run: Would create '$FILE_PATH' with the following content ---"
  echo "$FILE_CONTENT"
  echo "--------------------------------------------------------------------"
else
  echo "Creating Service Object: $FILE_PATH"
  echo "$FILE_CONTENT" > "$FILE_PATH" || { echo "Error: Could not write to file $FILE_PATH" >&2; exit 1; }
  echo "Service Object '$CLASS_NAME' created successfully."
  echo "Remember to implement the 'call' method with your business logic."
fi

exit 0
