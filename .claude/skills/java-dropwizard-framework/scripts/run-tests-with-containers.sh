#!/bin/bash

# run-tests-with-containers.sh
#
# Purpose:
#   Automates the execution of DropWizard tests, particularly focusing on
#   integration tests that might leverage Testcontainers. It ensures a consistent
#   way to run tests and provides guidance for Testcontainers setup.
#
# Usage:
#   ./run-tests-with-containers.sh
#   ./run-tests-with-containers.sh --project-dir /path/to/my-app --skip-unit-tests
#   ./run-tests-with-containers.sh --help
#
# Options:
#   --project-dir       Path to the DropWizard project root (where pom.xml is located)
#   --skip-unit-tests   Skip unit tests and only run integration tests (e.g., using Maven Failsafe plugin)
#   --clean-containers  Attempt to clean up Docker containers after tests (use with caution)
#   --dry-run           Show commands without executing them
#   --help              Display this help message

# --- Configuration ---
DEFAULT_PROJECT_DIR="."
SKIP_UNIT_TESTS=false
CLEAN_CONTAINERS=false
DRY_RUN=false

# --- Functions ---

# Function to display help message
display_help() {
    grep '^# Usage:' "$0" | sed -e 's/^# //' -e 's/^Usage:/Usage:\n /'
    grep '^# Options:' "$0" | sed -e 's/^# //' -e 's/^Options:/Options:\n/'
    exit 0
}

# --- Main Script Logic ---

# Parse command-line arguments
while [[ "$#" -gt 0 ]]; do
    case "$1" in
        --project-dir) PROJECT_DIR="$2"; shift ;;
        --skip-unit-tests) SKIP_UNIT_TESTS=true ;;
        --clean-containers) CLEAN_CONTAINERS=true ;;
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

echo "--- DropWizard Test Runner ---"
echo "  Project Directory: $PROJECT_DIR"
if [ "$SKIP_UNIT_TESTS" = true ]; then
    echo "  Skipping Unit Tests: Yes (running integration tests only)"
else
    echo "  Skipping Unit Tests: No (running all tests)"
fi
echo "  Clean Containers After Tests: $CLEAN_CONTAINERS"
echo ""

# Determine Maven command
MAVEN_TEST_COMMAND="mvn -f ${PROJECT_DIR}/pom.xml clean verify"
if [ "$SKIP_UNIT_TESTS" = true ]; then
    # Assumes integration tests are run by Failsafe plugin in 'verify' phase
    MAVEN_TEST_COMMAND="mvn -f ${PROJECT_DIR}/pom.xml clean install -DskipTests -Dinvoker.skip=true && mvn -f ${PROJECT_DIR}/pom.xml verify"
    echo "Note: '--skip-unit-tests' assumes your integration tests are configured to run during the 'verify' phase (e.g., via Maven Failsafe Plugin) and unit tests are skipped with -DskipTests."
fi

# --- Run Tests ---
echo "Running tests..."
if [ "$DRY_RUN" = true ]; then
    echo "Dry run: Would execute: $MAVEN_TEST_COMMAND"
else
    $MAVEN_TEST_COMMAND
    TEST_EXIT_CODE=$?

    if [ $TEST_EXIT_CODE -ne 0 ]; then
        echo "Error: Tests failed." >&2
        # Attempt to list running containers for debugging if tests failed
        echo "Listing running Docker containers (if any):"
        docker ps
        exit $TEST_EXIT_CODE
    else
        echo "All tests passed successfully."
    fi
fi

# --- Clean up containers (optional) ---
if [ "$CLEAN_CONTAINERS" = true ]; then
    echo ""
    echo "Attempting to clean up Docker containers..."
    if [ "$DRY_RUN" = true ]; then
        echo "Dry run: Would execute: docker rm -f $(docker ps -aq --filter label=org.testcontainers.session-id)"
    else
        # This command attempts to stop and remove containers started by Testcontainers
        # It relies on Testcontainers labeling its containers with a session ID.
        # This might not catch all containers if they are not properly labeled or managed.
        docker rm -f $(docker ps -aq --filter label=org.testcontainers.session-id)
        if [ $? -ne 0 ]; then
            echo "Warning: Could not clean up all Testcontainers-managed Docker containers. Manual cleanup might be required." >&2
        else
            echo "Testcontainers-managed Docker containers cleaned up."
        fi
    fi
fi

echo ""
echo "Test execution complete."

# Exit with the test command's exit code
exit $TEST_EXIT_CODE
