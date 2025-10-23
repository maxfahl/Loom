#!/bin/bash

# run-java-app.sh
#
# Description:
#   Compiles and runs a Java application. It can either run a single .java file
#   or execute a Maven/Gradle project's main class.
#
# Usage:
#   ./run-java-app.sh [options] <file_or_project_path>
#
# Options:
#   --main-class <class_name>  Specify the fully qualified main class name (e.g., com.example.App).
#                              Required if running a project and it cannot be auto-detected.
#   --args "<arguments>"       Arguments to pass to the Java application.
#   --help                     Display this help message.
#
# Examples:
#   # Run a single Java file
#   ./run-java-app.sh MyClass.java
#
#   # Run a Maven project (from its root directory)
#   ./run-java-app.sh /path/to/my-maven-project
#
#   # Run a Gradle project (from its root directory)
#   ./run-java-app.sh /path/to/my-gradle-project
#
#   # Run a project with a specific main class and arguments
#   ./run-java-app.sh /path/to/my-project --main-class com.example.MyMain --args "arg1 arg2"
#
# Requirements:
#   - Java 11 or higher (JAVA_HOME configured)
#   - Maven (if running a Maven project)
#   - Gradle (if running a Gradle project)

set -e

# --- Configuration ---
PROJECT_PATH="."
MAIN_CLASS=""
APP_ARGS=""

# --- Helper Functions ---

print_help() {
    grep '^# Usage:' "$0" | sed -e 's/^# //' -e 's/^Usage:/Usage:\n /'
    grep '^# Options:' "$0" | sed -e 's/^# //' -e 's/^Options:/Options:\n /'
    grep '^# Examples:' "$0" | sed -e 's/^# //' -e 's/^Examples:/Examples:\n /'
    exit 0
}

# --- Argument Parsing ---
while [[ "$#" -gt 0 ]]; do
    case "$1" in
        --main-class)
            MAIN_CLASS="$2"
            shift
            ;; 
        --args)
            APP_ARGS="$2"
            shift
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

if [ ! -e "$PROJECT_PATH" ]; then
    echo "Error: Path does not exist: ${PROJECT_PATH}"
    exit 1
fi

# --- Determine Project Type and Run ---
if [[ "$PROJECT_PATH" == *.java ]]; then
    echo "--- Running single Java file: $(basename "$PROJECT_PATH") ---"
    FILENAME=$(basename "$PROJECT_PATH")
    DIRNAME=$(dirname "$PROJECT_PATH")
    CLASSNAME="${FILENAME%.java}"

    cd "$DIRNAME" || { echo "Error: Failed to change directory to $DIRNAME"; exit 1; }

    echo "Compiling ${FILENAME}..."
    if ! javac "$FILENAME"; then
        echo "Error: Compilation failed."
        exit 1
    fi

    echo "Running ${CLASSNAME}..."
    java "$CLASSNAME" ${APP_ARGS}

elif [ -f "${PROJECT_PATH}/pom.xml" ]; then
    echo "--- Running Maven project: $(basename "$PROJECT_PATH") ---"
    if ! command -v mvn &> /dev/null; then
        echo "Error: Maven is not installed or not in PATH. Please install Maven."
        exit 1
    fi
    cd "$PROJECT_PATH" || { echo "Error: Failed to change directory to ${PROJECT_PATH}"; exit 1; }

    if [ -z "$MAIN_CLASS" ]; then
        echo "Attempting to auto-detect main class from pom.xml..."
        # This is a basic attempt. A more robust solution might parse XML.
        MAIN_CLASS=$(grep -oP '<mainClass>\K[^<]+(?=</mainClass>)' pom.xml | head -n 1)
        if [ -z "$MAIN_CLASS" ]; then
            echo "Warning: Could not auto-detect main class. Please specify with --main-class."
            exit 1
        else
            echo "Auto-detected main class: ${MAIN_CLASS}"
        fi
    fi

    echo "Building and running Maven project..."
    mvn clean compile exec:java -Dexec.mainClass="${MAIN_CLASS}" -Dexec.args="${APP_ARGS}"

elif [ -f "${PROJECT_PATH}/build.gradle" ] || [ -f "${PROJECT_PATH}/build.gradle.kts" ]; then
    echo "--- Running Gradle project: $(basename "$PROJECT_PATH") ---"
    if ! command -v gradle &> /dev/null; then
        echo "Error: Gradle is not installed or not in PATH. Please install Gradle."
        exit 1
    fi
    cd "$PROJECT_PATH" || { echo "Error: Failed to change directory to ${PROJECT_PATH}"; exit 1; }

    # Gradle 'run' task usually handles main class detection
    echo "Building and running Gradle project..."
    if [ -n "$APP_ARGS" ]; then
        ./gradlew run --args="${APP_ARGS}"
    else
        ./gradlew run
    fi

else
    echo "Error: No Java file, Maven (pom.xml), or Gradle (build.gradle) project found at ${PROJECT_PATH}"
    exit 1
fi

echo "Done."
