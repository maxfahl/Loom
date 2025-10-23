#!/bin/bash

# generate-swiftui-view.sh
#
# Description:
#   Generates a new SwiftUI View file with a basic structure and Xcode Preview.
#   This script automates the repetitive task of setting up new SwiftUI views,
#   saving developers time and ensuring consistency.
#
# Usage:
#   ./generate-swiftui-view.sh MyNewView
#   ./generate-swiftui-view.sh -n AnotherView -d ./Views
#
# Arguments:
#   -n, --name      <ViewName>  (Required) The name of the SwiftUI View (e.g., "LoginView").
#                                 Will create <ViewName>.swift.
#   -d, --directory <Path>      (Optional) The directory where the view file should be created.
#                                 Defaults to the current directory.
#   -h, --help                  Display this help message.
#
# Example:
#   To create a view named "ProfileView" in the "Sources/UI/Views" directory:
#   ./generate-swiftui-view.sh -n ProfileView -d Sources/UI/Views
#
# Production-ready features:
# - Argument parsing for flexibility.
# - Error handling for missing arguments or directory creation failures.
# - Informative output messages.
# - Cross-platform compatibility (standard bash commands).

# --- Configuration ---
DEFAULT_DIR="."

# --- Functions ---

# Function to display help message
display_help() {
    echo "Usage: $0 -n <ViewName> [-d <Path>]"
    echo ""
    echo "Arguments:"
    echo "  -n, --name      <ViewName>  (Required) The name of the SwiftUI View."
    echo "  -d, --directory <Path>      (Optional) The directory to create the view in. Defaults to current."
    echo "  -h, --help                  Display this help message."
    echo ""
    echo "Example:"
    echo "  $0 -n MyAwesomeView"
    echo "  $0 --name SettingsView --directory Sources/Settings"
    exit 0
}

# Function to generate the SwiftUI View content
generate_view_content() {
    local view_name=$1
    cat << EOF
import SwiftUI

struct ${view_name}: View {
    var body: some View {
        Text("Hello, ${view_name}!")
    }
}

struct ${view_name}_Previews: PreviewProvider {
    static var previews: some View {
        ${view_name}()
    }
}
EOF
}

# --- Main Script Logic ---

VIEW_NAME=""
OUTPUT_DIR="${DEFAULT_DIR}"

# Parse arguments
while [[ "$#" -gt 0 ]]; do
    case "$1" in
        -n|--name)
            VIEW_NAME="$2"
            shift # past argument
            ;;
        -d|--directory)
            OUTPUT_DIR="$2"
            shift # past argument
            ;;
        -h|--help)
            display_help
            ;;
        *)
            echo "Error: Unknown parameter passed: $1"
            display_help
            ;;
    esac
    shift # past argument or value
done

# Validate VIEW_NAME
if [ -z "${VIEW_NAME}" ]; then
    echo "Error: View name is required. Use -n or --name."
    display_help
fi

# Create directory if it doesn't exist
mkdir -p "${OUTPUT_DIR}"
if [ $? -ne 0 ]; then
    echo "Error: Could not create directory '${OUTPUT_DIR}'."
    exit 1
fi

FILE_PATH="${OUTPUT_DIR}/${VIEW_NAME}.swift"

# Check if file already exists
if [ -f "${FILE_PATH}" ]; then
    echo "Error: File '${FILE_PATH}' already exists. Aborting to prevent overwrite."
    exit 1
fi

# Generate content and write to file
generate_view_content "${VIEW_NAME}" > "${FILE_PATH}"

if [ $? -eq 0 ]; then
    echo "Successfully created SwiftUI View: '${FILE_PATH}'"
else
    echo "Error: Failed to create SwiftUI View file."
    exit 1
fi
