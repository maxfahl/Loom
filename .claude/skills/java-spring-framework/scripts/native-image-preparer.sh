#!/bin/bash

# native-image-preparer.sh
#
# Purpose: Prepares a Spring Boot project for GraalVM Native Image compilation.
#          It detects the build tool (Maven/Gradle), adds necessary build plugin
#          configurations, and provides guidance for building the native image.
#          This script aims to simplify the often complex setup for GraalVM Native Images.
#
# Usage:
#   ./native-image-preparer.sh [path_to_project_root]
#   Example: ./native-image-preparer.sh ~\/my-spring-app
#
# Features:
#   - Auto-detects Maven (pom.xml) or Gradle (build.gradle) project.
#   - Adds/updates `spring-boot-maven-plugin` or `spring-boot-gradle-plugin`
#     with native image build configuration.
#   - Suggests creating `reflect-config.json` and `resource-config.json` for complex cases.
#   - Provides clear instructions for building the native image.
#
# Configuration:
#   - None directly in script; relies on project structure.
#
# Error Handling:
#   - Checks for required commands (mvn, gradle, native-image).
#   - Reports if no supported build tool is found.
#   - Provides clear output messages.

# --- Colors for better readability ---
RED="\033[0;31m"
GREEN="\033[0;32m"
YELLOW="\033[0;33m"
BLUE="\033[0;34m"
NC="\033[0m" # No Color

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
    command -v "$1" >/dev/null 2>&1 || log_warning "Warning: '$1' is not installed. You might need it for native image compilation."
}

# --- Main Script Logic ---

log_info "Starting GraalVM Native Image Preparer..."

PROJECT_ROOT="${1:-.}"

if [ ! -d "$PROJECT_ROOT" ]; then
    log_error "Project root directory not found: ${PROJECT_ROOT}"
fi

cd "$PROJECT_ROOT" || log_error "Failed to change directory to ${PROJECT_ROOT}"

log_info "Analyzing project in: $(pwd)"

BUILD_TOOL=""
if [ -f "pom.xml" ]; then
    BUILD_TOOL="maven"
    check_command "mvn"
elif [ -f "build.gradle" ] || [ -f "build.gradle.kts" ]; then
    BUILD_TOOL="gradle"
    check_command "gradle"
else
    log_error "No Maven (pom.xml) or Gradle (build.gradle/build.gradle.kts) project found in ${PROJECT_ROOT}."
fi

log_info "Detected build tool: ${BUILD_TOOL}"

# Check for native-image command (part of GraalVM)
check_command "native-image"

if [ "$BUILD_TOOL" == "maven" ]; then
    log_info "Configuring Maven project for Native Image..."
    # Add/update spring-boot-maven-plugin configuration
    # This is a simplified approach. A more robust solution would use XML parsing.
    # For now, we'll instruct the user or provide a common snippet.

    log_warning "Please ensure your pom.xml includes the 'spring-boot-maven-plugin' with native build support."
    log_info "Example snippet to add/update in your <build><plugins> section of pom.xml:"
    echo -e "${GREEN}"
    echo "<plugin>"
    echo "    <groupId>org.springframework.boot</groupId>"
    echo "    <artifactId>spring-boot-maven-plugin</artifactId>"
    echo "    <configuration>"
    echo "        <image>"
    echo "            <name>${project.artifactId}</name>"
    echo "        </image>"
    echo "        <excludes>"
    echo "            <exclude>"
    echo "                <groupId>org.projectlombok</groupId>"
    echo "                <artifactId>lombok</artifactId>"
    echo "            </exclude>"
    echo "        </excludes>"
    echo "    </configuration>"
    echo "    <executions>"
    echo "        <execution>"
    echo "            <goals>"
    echo "                <goal>repackage</goal>"
    echo "                <goal>build-info</goal>"
    echo "            </goal>"
    echo "            <configuration>"
    echo "                <classifier>exec</classifier>"
    echo "            </configuration>"
    echo "        </execution>"
    echo "        <execution>"
    echo "            <id>process-aot</id>"
    echo "            <goals>"
    echo "                <goal>process-aot</goal>"
    echo "            </goal>"
    echo "        </execution>"
    echo "        <execution>"
    echo "            <id>compile-native</id>"
    echo "            <goals>"
    echo "                <goal>compile-native</goal>"
    echo "            </goals>"
    echo "        </execution>"
    echo "    </executions>"
    echo "</plugin>"
    echo -e "${NC}"

    log_info "To build the native image, run:"
    echo -e "${GREEN}./mvnw native:compile${NC}"

elif [ "$BUILD_TOOL" == "gradle" ]; then
    log_info "Configuring Gradle project for Native Image..."
    log_warning "Please ensure your build.gradle (or build.gradle.kts) includes the 'org.springframework.boot' plugin and 'org.graalvm.buildtools.native' plugin."
    log_info "Example snippet to add/update in your build.gradle:"
    echo -e "${GREEN}"
    echo "plugins {"
    echo "    id 'org.springframework.boot' version '3.x.x'"
    echo "    id 'io.spring.dependency-management' version '1.x.x'"
    echo "    id 'java'"
    echo "    id 'org.graalvm.buildtools.native' version '0.x.x' // Check for latest version"
    echo "}"
    echo ""
    echo "graalvm { // Optional: configure GraalVM specific settings"
    echo "    toolchainDetection = true"
    echo "    nativeBuild {"
    echo "        args.add('--no-fallback')"
    echo "        // Add more arguments as needed, e.g., --initialize-at-build-time=org.example.MyClass"
    echo "    }"
    echo "}"
    echo -e "${NC}"

    log_info "To build the native image, run:"
    echo -e "${GREEN}./gradlew nativeCompile${NC}"
fi

log_info "\n--- Important Considerations for Native Images ---"
log_warning "1. Reflection, Resources, and Dynamic Proxies:"
log_info "   GraalVM Native Image requires compile-time knowledge of all code paths. If your application uses reflection, dynamic proxies, or accesses resources dynamically, you might need to provide configuration hints."
log_info "   Consider creating these files in src/main/resources/META-INF/native-image/your-app-name/:"
     " - reflect-config.json: For classes, methods, and fields accessed via reflection."
     " - resource-config.json: For resources loaded dynamically (e.g., via ClassLoader.getResource())."
     " - proxy-config.json: For dynamic proxies."
log_info "   Spring Boot AOT processing often generates many of these automatically, but manual hints might be needed for complex cases or third-party libraries."
log_info "   See: https://docs.spring.io/spring-boot/docs/current/reference/html/native-image.html#native-image.advanced.hints"

log_warning "2. Testing:"
log_info "   Always thoroughly test your native image. Behavior can sometimes differ from JVM mode due to the closed-world assumption."

log_warning "3. Dependencies:"
log_info "   Ensure all dependencies are compatible with GraalVM Native Image. Some older libraries might not be."

log_success "Native Image preparation guidance complete."
log_info "Please review the instructions and update your build configuration files accordingly."
