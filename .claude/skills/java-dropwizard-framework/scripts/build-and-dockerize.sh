#!/bin/bash

# build-and-dockerize.sh
#
# Purpose:
#   Automates the process of building a DropWizard application into a fat JAR
#   and then creating a Docker image for it. This streamlines the build and
#   containerization steps for deployment.
#
# Usage:
#   ./build-and-dockerize.sh
#   ./build-and-dockerize.sh --project-dir /path/to/my-app --tag my-app:1.0.0
#   ./build-and-dockerize.sh --help
#
# Options:
#   --project-dir   Path to the DropWizard project root (where pom.xml is located)
#   --tag           Docker image tag (e.g., my-app:1.0.0). Defaults to artifactId:version.
#   --dry-run       Show commands without executing them
#   --help          Display this help message

# --- Configuration ---
DEFAULT_PROJECT_DIR="."
DRY_RUN=false

# --- Functions ---

# Function to display help message
display_help() {
    grep '^# Usage:' "$0" | sed -e 's/^# //' -e 's/^Usage:/Usage:\n /'
    grep '^# Options:' "$0" | sed -e 's/^# //' -e 's/^Options:/Options:\n/'
    exit 0
}

# Function to extract Maven project properties
get_maven_property() {
    local prop_name="$1"
    local pom_file="$2"
    grep -oP "<${prop_name}>\K[^<]+(?=</${prop_name}>)" "$pom_file" | head -1
}

# --- Main Script Logic ---

# Parse command-line arguments
while [[ "$#" -gt 0 ]]; do
    case "$1" in
        --project-dir) PROJECT_DIR="$2"; shift ;; 
        --tag) DOCKER_TAG="$2"; shift ;; 
        --dry-run) DRY_RUN=true ;; 
        --help) display_help ;; 
        *) echo "Unknown parameter passed: $1"; display_help ;; 
    esac
    shift
done

PROJECT_DIR="${PROJECT_DIR:-$DEFAULT_PROJECT_DIR}"

if [ ! -f "$PROJECT_DIR/pom.xml" ]; then
    echo "Error: pom.xml not found in $PROJECT_DIR. Please specify the correct project directory." >&2
    exit 1
fi

# Extract artifactId and version from pom.xml
ARTIFACT_ID=$(get_maven_property "artifactId" "$PROJECT_DIR/pom.xml")
VERSION=$(get_maven_property "version" "$PROJECT_DIR/pom.xml")

if [ -z "$ARTIFACT_ID" ] || [ -z "$VERSION" ]; then
    echo "Error: Could not extract artifactId or version from pom.xml." >&2
    exit 1
fi

# Set default Docker tag if not provided
DOCKER_TAG="${DOCKER_TAG:-${ARTIFACT_ID}:${VERSION}}"

FAT_JAR_NAME="${ARTIFACT_ID}-${VERSION}.jar"
FAT_JAR_PATH="${PROJECT_DIR}/target/${FAT_JAR_NAME}"

echo "--- DropWizard Build and Dockerize ---"
echo "  Project Directory: $PROJECT_DIR"
echo "  Artifact ID: $ARTIFACT_ID"
echo "  Version: $VERSION"
echo "  Fat JAR: $FAT_JAR_PATH"
echo "  Docker Image Tag: $DOCKER_TAG"
echo ""

# --- Step 1: Build the Fat JAR ---
echo "Building DropWizard fat JAR..."
BUILD_COMMAND="mvn -f ${PROJECT_DIR}/pom.xml clean install"

if [ "$DRY_RUN" = true ]; then
    echo "Dry run: Would execute: $BUILD_COMMAND"
else
    $BUILD_COMMAND
    if [ $? -ne 0 ]; then
        echo "Error: Maven build failed." >&2
        exit 1
    fi
    if [ ! -f "$FAT_JAR_PATH" ]; then
        echo "Error: Fat JAR not found at $FAT_JAR_PATH after build." >&2
        exit 1
    fi
    echo "Fat JAR built successfully: $FAT_JAR_PATH"
fi

echo ""

# --- Step 2: Create Dockerfile if it doesn't exist ---
DOCKERFILE_PATH="${PROJECT_DIR}/Dockerfile"
if [ ! -f "$DOCKERFILE_PATH" ]; then
    echo "Dockerfile not found. Generating a basic one..."
    if [ "$DRY_RUN" = true ]; then
        echo "Dry run: Would create Dockerfile at $DOCKERFILE_PATH"
        cat <<EOF_DRY_RUN
FROM openjdk:17-jre-slim

WORKDIR /app

COPY target/${FAT_JAR_NAME} /app/${FAT_JAR_NAME}
COPY src/main/resources/config.yml /app/config.yml

EXPOSE 8080 8081

CMD ["java", "-jar", "${FAT_JAR_NAME}", "server", "config.yml"]
EOF_DRY_RUN
    else
        cat <<EOF > "$DOCKERFILE_PATH"
FROM openjdk:17-jre-slim

WORKDIR /app

COPY target/${FAT_JAR_NAME} /app/${FAT_JAR_NAME}
COPY src/main/resources/config.yml /app/config.yml

EXPOSE 8080 8081

CMD ["java", "-jar", "${FAT_JAR_NAME}", "server", "config.yml"]
EOF
        echo "Basic Dockerfile generated at $DOCKERFILE_PATH"
    fi
else
    echo "Existing Dockerfile found at $DOCKERFILE_PATH. Using it."
fi

echo ""

# --- Step 3: Build Docker Image ---
echo "Building Docker image..."
DOCKER_BUILD_COMMAND="docker build -t ${DOCKER_TAG} ${PROJECT_DIR}"

if [ "$DRY_RUN" = true ]; then
    echo "Dry run: Would execute: $DOCKER_BUILD_COMMAND"
else
    $DOCKER_BUILD_COMMAND
    if [ $? -ne 0 ]; then
        echo "Error: Docker image build failed." >&2
        exit 1
    fi
    echo "Docker image '${DOCKER_TAG}' built successfully."
    echo "To run your Docker image: docker run -p 8080:8080 -p 8081:8081 ${DOCKER_TAG}"
fi

echo ""

echo "Build and Dockerize process complete."
