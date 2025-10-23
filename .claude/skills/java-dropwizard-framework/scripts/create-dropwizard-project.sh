#!/bin/bash

# create-dropwizard-project.sh
#
# Purpose:
#   Automates the creation of a new DropWizard project using the Maven archetype.
#   It prompts for project details (Group ID, Artifact ID, Version, Package)
#   and then executes the 'mvn archetype:generate' command.
#   This script saves time by providing a guided setup and handling the Maven command.
#
# Usage:
#   ./create-dropwizard-project.sh
#   ./create-dropwizard-project.sh --group-id com.example --artifact-id my-app
#
# Options:
#   --group-id      Maven Group ID (e.g., com.example)
#   --artifact-id   Maven Artifact ID (e.g., my-dropwizard-app)
#   --version       Project Version (e.g., 1.0.0-SNAPSHOT)
#   --package       Base Package (e.g., com.example.my_app)
#   --archetype-version DropWizard Archetype Version (e.g., 5.0.0)
#   --dry-run       Show the Maven command without executing it
#   --help          Display this help message

# --- Configuration ---
DEFAULT_GROUP_ID="com.example"
DEFAULT_ARTIFACT_ID="my-dropwizard-app"
DEFAULT_VERSION="1.0.0-SNAPSHOT"
DEFAULT_ARCHETYPE_VERSION="5.0.0" # DropWizard 5.x requires Java 17+
DRY_RUN=false

# --- Functions ---

# Function to display help message
display_help() {
    grep '^# Usage:' "$0" | sed -e 's/^# //' -e 's/^Usage:/Usage:\n /'
    grep '^# Options:' "$0" | sed -e 's/^# //' -e 's/^Options:/Options:\n/'
    exit 0
}

# Function to prompt for input with a default value
prompt_for_input() {
    local prompt_text="$1"
    local default_value="$2"
    local input_var="$3"
    read -rp "$prompt_text [$default_value]: " input
    eval "$input_var=\"${input:-\$default_value}\""
}

# --- Main Script Logic ---

# Parse command-line arguments
while [[ "$#" -gt 0 ]]; do
    case "$1" in
        --group-id) GROUP_ID="$2"; shift ;; 
        --artifact-id) ARTIFACT_ID="$2"; shift ;; 
        --version) VERSION="$2"; shift ;; 
        --package) PACKAGE="$2"; shift ;; 
        --archetype-version) ARCHETYPE_VERSION="$2"; shift ;; 
        --dry-run) DRY_RUN=true ;; 
        --help) display_help ;; 
        *) echo "Unknown parameter passed: $1"; display_help ;; 
    esac
    shift
done

echo "--- DropWizard Project Creator ---"

# Prompt for missing values if not provided via arguments
prompt_for_input "Enter Group ID" "${GROUP_ID:-$DEFAULT_GROUP_ID}" GROUP_ID
prompt_for_input "Enter Artifact ID" "${ARTIFACT_ID:-$DEFAULT_ARTIFACT_ID}" ARTIFACT_ID
prompt_for_input "Enter Project Version" "${VERSION:-$DEFAULT_VERSION}" VERSION

# Default package is derived from group ID and artifact ID if not provided
if [ -z "$PACKAGE" ]; then
    DEFAULT_PACKAGE=$(echo "$GROUP_ID.$ARTIFACT_ID" | tr '-' '_' | tr '.' '_') # Basic sanitization
    prompt_for_input "Enter Base Package" "$DEFAULT_PACKAGE" PACKAGE
fi

prompt_for_input "Enter DropWizard Archetype Version (e.g., 5.0.0 for Java 17+)" "$DEFAULT_ARCHETYPE_VERSION" ARCHETYPE_VERSION

echo ""
echo "Project Details:"
echo "  Group ID: $GROUP_ID"
echo "  Artifact ID: $ARTIFACT_ID"
echo "  Version: $VERSION"
echo "  Package: $PACKAGE"
echo "  DropWizard Archetype Version: $ARCHETYPE_VERSION"
echo ""

# Construct the Maven command
MAVEN_COMMAND="mvn archetype:generate \
  -DarchetypeGroupId=io.dropwizard \
  -DarchetypeArtifactId=dropwizard-archetype \
  -DarchetypeVersion=${ARCHETYPE_VERSION} \
  -DgroupId=${GROUP_ID} \
  -DartifactId=${ARTIFACT_ID} \
  -Dversion=${VERSION} \
  -Dpackage=${PACKAGE} \
  -DinteractiveMode=false"

echo "Generated Maven Command:"
echo "$MAVEN_COMMAND"
echo ""

if [ "$DRY_RUN" = true ]; then
    echo "Dry run complete. The command above would have been executed."
    exit 0
fi

read -rp "Proceed with project creation? (y/N): " confirm
if [[ "$confirm" =~ ^[Yy]$ ]]; then
    echo "Creating DropWizard project..."
    # Execute the Maven command
    eval "$MAVEN_COMMAND"

    if [ $? -eq 0 ]; then
        echo ""
        echo "DropWizard project '$ARTIFACT_ID' created successfully!"
        echo "Navigate into the project directory: cd $ARTIFACT_ID"
        echo "To build: mvn clean install"
        echo "To run: java -jar $ARTIFACT_ID/target/$ARTIFACT_ID-$VERSION.jar server $ARTIFACT_ID/config.yml"
        echo ""
        echo "Consider updating the archetype version in the generated pom.xml if a newer stable version is available."
    else
        echo "Error: Failed to create DropWizard project."
        exit 1
    fi
else
    echo "Project creation cancelled."
    exit 0
fi
