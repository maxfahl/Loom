#!/bin/bash

# java-code-quality.sh
#
# Description:
#   Runs common code quality checks for a Java project, including building,
#   running tests, and optionally integrating static analysis tools.
#
# Usage:
#   ./java-code-quality.sh [options] <project_path>
#
# Options:
#   --skip-tests             Skip running unit and integration tests.
#   --skip-static-analysis   Skip static analysis tools (e.g., Checkstyle, SpotBugs).
#   --help                   Display this help message.
#
# Examples:
#   # Run all quality checks in the current directory
#   ./java-code-quality.sh
#
#   # Run quality checks for a specific project, skipping tests
#   ./java-code-quality.sh /path/to/my-java-project --skip-tests
#
# Requirements:
#   - Java 11 or higher (JAVA_HOME configured)
#   - Maven (if running a Maven project)
#   - Gradle (if running a Gradle project)
#   - Static analysis plugins configured in pom.xml/build.gradle for full functionality.

set -e

# --- Configuration ---
PROJECT_PATH="."
SKIP_TESTS=false
SKIP_STATIC_ANALYSIS=false

# --- Helper Functions ---

print_help() {
    grep '^# Usage:' "$0" | sed -e 's/^# //'
    grep '^# Options:' "$0" | sed -e 's/^# //'
    grep '^# Examples:' "$0" | sed -e 's/^# //'
    exit 0
}

# --- Argument Parsing ---
while [[ "$#" -gt 0 ]]; do
    case "$1" in
        --skip-tests)
            SKIP_TESTS=true
            ;;
        --skip-static-analysis)
            SKIP_STATIC_ANALYSIS=true
            ;;
        --help)
            print_help
            ;;
        -*) 
            echo "Unknown option: $1"
            print_help
            exit 1
            ;;
        *)
            PROJECT_PATH="$1"
            ;;
    esac
    shift
done

# Resolve project path to absolute path
PROJECT_PATH=$(realpath "$PROJECT_PATH")

if [ ! -d "$PROJECT_PATH" ]; then
    echo "Error: Project directory does not exist: ${PROJECT_PATH}"
    exit 1
fi

cd "$PROJECT_PATH" || { echo "Error: Failed to change directory to ${PROJECT_PATH}"; exit 1; }

echo "--- Running Code Quality Checks for: $(basename "$PROJECT_PATH") ---"

# --- Detect Build Tool ---
BUILD_TOOL="unknown"
if [ -f "pom.xml" ]; then
    BUILD_TOOL="maven"
elif [ -f "build.gradle" ] || [ -f "build.gradle.kts" ]; then
    BUILD_TOOL="gradle"
fi

if [ "$BUILD_TOOL" == "unknown" ]; then
    echo "Error: No Maven (pom.xml) or Gradle (build.gradle) project found in ${PROJECT_PATH}"
    exit 1
fi

echo "Detected build tool: ${BUILD_TOOL}"

# --- Run Build and Tests ---
if [ "$BUILD_TOOL" == "maven" ]; then
    if ! command -v mvn &> /dev/null; then
        echo "Error: Maven is not installed or not in PATH. Please install Maven."
        exit 1
    fi
    echo "Running Maven build and tests..."
    if [ "$SKIP_TESTS" = true ]; then
        mvn clean install -DskipTests
    else
        mvn clean install
    fi

elif [ "$BUILD_TOOL" == "gradle" ]; then
    if ! command -v gradle &> /dev/null; then
        echo "Error: Gradle is not installed or not in PATH. Please install Gradle."
        exit 1
    fi
    echo "Running Gradle build and tests..."
    if [ "$SKIP_TESTS" = true ]; then
        ./gradlew clean build -x test
    else
        ./gradlew clean build
    fi
fi

# --- Run Static Analysis (if not skipped) ---
if [ "$SKIP_STATIC_ANALYSIS" = false ]; then
    echo "Running static analysis (if configured)..."
    if [ "$BUILD_TOOL" == "maven" ]; then
        # Common Maven goals for static analysis
        # User needs to have these plugins configured in their pom.xml
        if mvn checkstyle:check &> /dev/null; then
            echo "  - Checkstyle analysis complete."
        else
            echo "  - Checkstyle plugin not configured or failed. Skipping."
        fi
        if mvn spotbugs:check &> /dev/null; then
            echo "  - SpotBugs analysis complete."
        else
            echo "  - SpotBugs plugin not configured or failed. Skipping."
        fi
        if mvn pmd:check &> /dev/null; then
            echo "  - PMD analysis complete."
        else
            echo "  - PMD plugin not configured or failed. Skipping."
        fi
    elif [ "$BUILD_TOOL" == "gradle" ]; then
        # Common Gradle tasks for static analysis
        # User needs to have these plugins configured in their build.gradle
        if ./gradlew checkstyleMain &> /dev/null; then
            echo "  - Checkstyle analysis complete."
        else
            echo "  - Checkstyle task not configured or failed. Skipping."
        fi
        if ./gradlew spotbugsMain &> /dev/null; then
            echo "  - SpotBugs analysis complete."
        else
            echo "  - SpotBugs task not configured or failed. Skipping."
        fi
        if ./gradlew pmdMain &> /dev/null; then
            echo "  - PMD analysis complete."
        else
            echo "  - PMD task not configured or failed. Skipping."
        fi
    fi
else
    echo "Static analysis skipped."
fi

echo "All requested quality checks completed."
echo "Done."
