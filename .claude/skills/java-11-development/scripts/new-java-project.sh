#!/bin/bash

# new-java-project.sh
#
# Description:
#   Bootstraps a new Java 11 project using either Maven or Gradle.
#   It creates a basic project structure, including a 'Main' class,
#   and configures the chosen build tool.
#
# Usage:
#   ./new-java-project.sh
#   ./new-java-project.sh --name my-project --group com.example --build-tool maven
#
# Options:
#   --name <project_name>    Specify the project name (kebab-case recommended).
#   --group <group_id>       Specify the group ID (e.g., com.example).
#   --build-tool <tool>      Specify the build tool: 'maven' or 'gradle'.
#   --help                   Display this help message.
#
# Examples:
#   # Interactive mode
#   ./new-java-project.sh
#
#   # Non-interactive mode for Maven project
#   ./new-java-project.sh --name my-maven-app --group com.example --build-tool maven
#
#   # Non-interactive mode for Gradle project
#   ./new-java-project.sh --name my-gradle-app --group com.example --build-tool gradle
#
# Requirements:
#   - Java 11 or higher (JAVA_HOME configured)
#   - Maven (if 'maven' build tool is chosen)
#   - Gradle (if 'gradle' build tool is chosen)

set -e

# --- Configuration ---
DEFAULT_PROJECT_NAME="my-java-app"
DEFAULT_GROUP_ID="com.example"
DEFAULT_BUILD_TOOL="maven" # or "gradle"

# --- Helper Functions ---

print_help() {
    grep '^# Usage:' "$0" | sed -e 's/^# //' -e 's/^Usage:/Usage:\n /'
    grep '^# Options:' "$0" | sed -e 's/^# //' -e 's/^Options:/Options:\n /'
    grep '^# Examples:' "$0" | sed -e 's/^# //' -e 's/^Examples:/Examples:\n /'
    exit 0
}

# --- Argument Parsing ---
PROJECT_NAME=""
GROUP_ID=""
BUILD_TOOL=""

while [[ "$#" -gt 0 ]]; do
    case "$1" in
        --name)
            PROJECT_NAME="$2"
            shift
            ;;
        --group)
            GROUP_ID="$2"
            shift
            ;;
        --build-tool)
            BUILD_TOOL="$2"
            shift
            ;;
        --help)
            print_help
            ;;
        *)
            echo "Unknown parameter: $1"
            print_help
            exit 1
            ;;
    esac
    shift
done

# --- Interactive Prompts (if arguments not provided) ---
if [ -z "$PROJECT_NAME" ]; then
    read -rp "Enter project name (e.g., my-java-app) [${DEFAULT_PROJECT_NAME}]: " input_name
    PROJECT_NAME="${input_name:-$DEFAULT_PROJECT_NAME}"
fi

if [ -z "$GROUP_ID" ]; then
    read -rp "Enter group ID (e.g., com.example) [${DEFAULT_GROUP_ID}]: " input_group
    GROUP_ID="${input_group:-$DEFAULT_GROUP_ID}"
fi

if [ -z "$BUILD_TOOL" ]; then
    read -rp "Choose build tool (maven/gradle) [${DEFAULT_BUILD_TOOL}]: " input_tool
    BUILD_TOOL="${input_tool:-$DEFAULT_BUILD_TOOL}"
fi

# Validate build tool
if [[ "$BUILD_TOOL" != "maven" && "$BUILD_TOOL" != "gradle" ]]; then
    echo "Error: Invalid build tool specified. Must be 'maven' or 'gradle'."
    exit 1
fi

echo "--- Creating Java 11 Project: ${PROJECT_NAME} ---"
echo "  Group ID: ${GROUP_ID}"
echo "  Build Tool: ${BUILD_TOOL}"

# --- Project Generation ---
if [ "$BUILD_TOOL" == "maven" ]; then
    echo "Generating Maven project..."
    if ! command -v mvn &> /dev/null; then
        echo "Error: Maven is not installed or not in PATH. Please install Maven."
        exit 1
    fi
    mvn archetype:generate \
        -DgroupId="${GROUP_ID}" \
        -DartifactId="${PROJECT_NAME}" \
        -DarchetypeArtifactId=maven-archetype-quickstart \
        -DarchetypeVersion=1.4 \
        -DinteractiveMode=false \
        -Djava.version=11 # Specify Java 11
    
    cd "${PROJECT_NAME}" || { echo "Error: Failed to change directory to ${PROJECT_NAME}"; exit 1; }

    # Update pom.xml to explicitly use Java 11 and add main class
    # This sed command is for macOS/BSD. For Linux, use 'sed -i'
    if [[ "$OSTYPE" == "darwin"* ]]; then
        sed -i '' 's|<maven.compiler.source>1.7</maven.compiler.source>|<maven.compiler.source>11</maven.compiler.source>|g' pom.xml
        sed -i '' 's|<maven.compiler.target>1.7</maven.compiler.target>|<maven.compiler.target>11</maven.compiler.target>|g' pom.xml
        sed -i '' '/<artifactId>maven-jar-plugin</artifactId>/a \				<configuration>\n					<archive>\n						<manifest>\n							<addClasspath>true</addClasspath>\n							<mainClass>'