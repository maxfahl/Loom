#!/bin/bash

# spring-project-initializer.sh
#
# Purpose: Automates the creation of a new Spring Boot project using Spring Initializr.
#          It prompts for project details, downloads the project, unzips it,
#          adds a basic README.md, and initializes a Git repository.
#
# Usage:
#   ./spring-project-initializer.sh
#
# Features:
#   - Interactive prompts for project metadata (group, artifact, name, Java version, Spring Boot version).
#   - Allows selection of common dependencies.
#   - Downloads project from start.spring.io.
#   - Initializes a Git repository and creates an initial commit.
#   - Creates a basic README.md.
#
# Configuration:
#   - Default values can be set in the script or overridden via prompts.
#
# Error Handling:
#   - Checks for required commands (curl, unzip, git).
#   - Validates user input for Java and Spring Boot versions.
#   - Reports download and unzip failures.

# --- Configuration ---
DEFAULT_GROUP_ID="com.example"
DEFAULT_ARTIFACT_ID="demo"
DEFAULT_NAME="DemoApplication"
DEFAULT_JAVA_VERSION="21"
DEFAULT_SPRING_BOOT_VERSION="3.3.0" # Check for latest stable on start.spring.io
DEFAULT_PACKAGING="jar"
DEFAULT_LANGUAGE="java"
DEFAULT_BUILD_TOOL="maven" # or gradle

# --- Colors for better readability ---
RED="\\033[0;31m"
GREEN="\\033[0;32m"
YELLOW="\\033[0;33m"
BLUE="\\033[0;34m"
NC="\\033[0m" # No Color

# --- Helper Functions ---

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
    exit 1
}

check_command() {
    command -v "$1" >/dev/null 2>&1 || log_error "Error: '$1' is not installed. Please install it to proceed."
}

prompt_input() {
    local prompt_text="$1"
    local default_value="$2"
    local result_var="$3"
    read -rp "${BLUE}${prompt_text}${NC} [${default_value}]: " input
    eval "$result_var=\${input:-${default_value}}"
}

# --- Main Script Logic ---

log_info "Starting Spring Boot Project Initializer..."

# 1. Check for required commands
check_command "curl"
check_command "unzip"
check_command "git"

# 2. Gather project details
log_info "Please provide project details:"

prompt_input "Group ID" "$DEFAULT_GROUP_ID" GROUP_ID
prompt_input "Artifact ID" "$DEFAULT_ARTIFACT_ID" ARTIFACT_ID
prompt_input "Project Name (e.g., MyAwesomeApp)" "$DEFAULT_NAME" NAME
prompt_input "Java Version (e.g., 17, 21)" "$DEFAULT_JAVA_VERSION" JAVA_VERSION
prompt_input "Spring Boot Version (e.g., 3.3.0)" "$DEFAULT_SPRING_BOOT_VERSION" SPRING_BOOT_VERSION

# Validate Java Version
if ! [[ "$JAVA_VERSION" =~ ^(17|21)$ ]]; then
    log_warning "Unsupported Java version '$JAVA_VERSION'. Recommended versions are 17 or 21."
    prompt_input "Please enter a supported Java Version (17, 21)" "$DEFAULT_JAVA_VERSION" JAVA_VERSION
    if ! [[ "$JAVA_VERSION" =~ ^(17|21)$ ]]; then
        log_error "Invalid Java version. Exiting."
    fi
fi

# Validate Spring Boot Version (basic check)
if ! [[ "$SPRING_BOOT_VERSION" =~ ^3\.[0-9]+\.[0-9]+$ ]]; then
    log_warning "Spring Boot version '$SPRING_BOOT_VERSION' might not be a valid 3.x version."
    prompt_input "Please enter a valid Spring Boot 3.x Version (e.g., 3.3.0)" "$DEFAULT_SPRING_BOOT_VERSION" SPRING_BOOT_VERSION
    if ! [[ "$SPRING_BOOT_VERSION" =~ ^3\.[0-9]+\.[0-9]+$ ]]; then
        log_error "Invalid Spring Boot version. Exiting."
    fi
fi

# Dependencies selection
echo -e "${BLUE}Common Dependencies (comma-separated, e.g., web,data-jpa,security):${NC}"
echo "  - web (Spring Web)"
echo "  - data-jpa (Spring Data JPA)"
echo "  - security (Spring Security)"
echo "  - devtools (Spring Boot DevTools)"
echo "  - actuator (Spring Boot Actuator)"
echo "  - validation (Bean Validation)"
echo "  - test (Spring Boot Test)"
read -rp "${BLUE}Enter dependencies:${NC} [web,data-jpa,security,validation,actuator,devtools,test]: " DEPENDENCIES_INPUT
DEPENDENCIES=${DEPENDENCIES_INPUT:-"web,data-jpa,security,validation,actuator,devtools,test"}

# 3. Construct the Spring Initializr URL
INITIALIZR_URL="https://start.spring.io/starter.zip?type=${DEFAULT_BUILD_TOOL}&language=${DEFAULT_LANGUAGE}&platformVersion=${SPRING_BOOT_VERSION}&packaging=${DEFAULT_PACKAGING}&javaVersion=${JAVA_VERSION}&groupId=${GROUP_ID}&artifactId=${ARTIFACT_ID}&name=${NAME}&description=${NAME}&packageName=${GROUP_ID}.${ARTIFACT_ID}&dependencies=${DEPENDENCIES}"

PROJECT_DIR="${ARTIFACT_ID}"
ZIP_FILE="${PROJECT_DIR}.zip"

log_info "Downloading project from Spring Initializr..."
log_info "URL: ${INITIALIZR_URL}"

# 4. Download and unzip the project
curl -s -L -o "$ZIP_FILE" "$INITIALIZR_URL"
if [ $? -ne 0 ]; then
    log_error "Failed to download project from Spring Initializr. Check your internet connection or parameters."
fi

log_info "Unzipping project to ./${PROJECT_DIR}..."
unzip -q "$ZIP_FILE" -d "$PROJECT_DIR"
if [ $? -ne 0 ]; then
    log_error "Failed to unzip project."
fi

rm "$ZIP_FILE"

# 5. Add a basic README.md
log_info "Creating basic README.md..."
cat << EOF > "${PROJECT_DIR}/README.md"
# ${NAME}

This is a Spring Boot application generated by the \`spring-project-initializer.sh\` script.

## Project Structure

- \`src/main/java\`: Main application source code.
- \`src/test/java\`: Test source code.
- \`src/main/resources\`: Configuration and static resources.
- \`pom.xml\` (Maven) or \`build.gradle\` (Gradle): Project build configuration.

## Getting Started

### Prerequisites
- Java ${JAVA_VERSION} SDK
- Maven or Gradle

### Build and Run
\`\`\`bash
# For Maven
cd ${PROJECT_DIR}
./mvnw spring-boot:run

# For Gradle
cd ${PROJECT_DIR}
./gradlew bootRun
\`\`\`

### Explore
- **Actuator Endpoints**: \`http://localhost:8080/actuator\` (if actuator dependency included)
- **H2 Console**: \`http://localhost:8080/h2-console\` (if h2 dependency included and configured)

## Dependencies
${DEPENDENCIES}

## Further Reading
- [Spring Boot Documentation](https://docs.spring.io/spring-boot/docs/current/reference/html/)
- [Spring Initializr](https://start.spring.io/)
EOF

# 6. Initialize Git repository
log_info "Initializing Git repository in ./${PROJECT_DIR}..."
(
    cd "$PROJECT_DIR" || log_error "Failed to change directory to ${PROJECT_DIR}"
    git init -q
    git add .
    git commit -q -m "Initial commit: Spring Boot project generated by initializer script"
)

log_success "Project '${NAME}' created successfully in ./${PROJECT_DIR}"
log_info "To get started, navigate to the project directory: cd ${PROJECT_DIR}"
log_info "Then run: ./mvnw spring-boot:run (for Maven) or ./gradlew bootRun (for Gradle)"
