#!/bin/bash

# fixture_dependency_graph.sh
#
# This script generates a simple text-based dependency graph for pytest fixtures
# within a specified Python test file or directory. It identifies fixtures and
# their direct dependencies (other fixtures they request).
#
# Usage Examples:
#   # Generate graph for a single test file
#   ./fixture_dependency_graph.sh tests/unit/test_my_module.py
#
#   # Generate graph for all test files in a directory
#   ./fixture_dependency_graph.sh tests/
#
#   # Generate graph and save to a file
#   ./fixture_dependency_graph.sh tests/ > fixture_graph.txt
#
#   # Generate graph with verbose output (showing files processed)
#   ./fixture_dependency_graph.sh -v tests/

# --- Configuration ---
COLOR_RED="\033[0;31m"
COLOR_GREEN="\033[0;32m"
COLOR_YELLOW="\033[0;33m"
COLOR_BLUE="\033[0;34m"
COLOR_CYAN="\033[0;36m"
COLOR_RESET="\033[0m"

VERBOSE=0

# --- Functions ---

print_help() {
    echo -e "${COLOR_CYAN}Usage: $0 [-v] <path>"${COLOR_RESET}
    echo ""
    echo "  -v, --verbose   Enable verbose output."
    echo "  <path>          The path to a Python test file or directory to scan."
    echo ""
    echo "This script identifies pytest fixtures and their dependencies."
    echo "It looks for functions decorated with @pytest.fixture and their arguments."
    exit 1
}

process_file() {
    local file="$1"
    if [ "$VERBOSE" -eq 1 ]; then
        echo -e "${COLOR_BLUE}Processing file: $file"${COLOR_RESET}
    fi

    # Extract fixture definitions and their dependencies
    # This regex looks for lines defining a fixture and then the function definition line
    # It captures the fixture name and its arguments (dependencies)
    grep -E -A 1 "^@pytest\.fixture|^@fixture" "$file" | \
    awk 'BEGIN {RS="--"; FS="\n"} {
        fixture_name=""; dependencies="";
        for (i=1; i<=NF; i++) {
            if ($i ~ /^@pytest\.fixture|^@fixture/) {
                # This is the decorator line, ignore for name extraction
            } else if ($i ~ /^def /) {
                # This is the function definition line
                match($i, /^def ([a-zA-Z0-9_]+)\(.*\):/);
                fixture_name = substr($i, RSTART+4, RLENGTH-5);
                dependencies = substr($i, RSTART+length("def "fixture_name"(")+1, RLENGTH-length("def "fixture_name"(")-2);
                gsub(/ /, "", dependencies); # Remove spaces
                gsub(/,/, " ", dependencies); # Replace commas with spaces for easy iteration
                break;
            }
        }
        if (fixture_name != "") {
            print fixture_name":"dependencies;
        }
    }' | \
    while IFS=":" read -r fixture_name deps;
    do
        echo -e "${COLOR_GREEN}Fixture: ${fixture_name}"${COLOR_RESET}
        if [ -n "$deps" ]; then
            for dep in $deps;
            do
                # Filter out self-references or non-fixture arguments like 'request'
                if [[ "$dep" != "" && "$dep" != "request" && "$dep" != "$fixture_name" ]]; then
                    echo -e "  ${COLOR_YELLOW}└── Depends on: ${dep}"${COLOR_RESET}
                fi
            done
        else
            echo -e "  ${COLOR_YELLOW}(No explicit dependencies)${COLOR_RESET}"
        fi
    done
}

# --- Main Logic ---

# Parse arguments
while [[ "$#" -gt 0 ]]; do
    case "$1" in
        -v|--verbose)
            VERBOSE=1
            shift
            ;;
        -h|--help)
            print_help
            ;;
        -*)
            echo -e "${COLOR_RED}Unknown option: $1"${COLOR_RESET}
            print_help
            ;;
        *)
            TARGET_PATH="$1"
            shift
            ;;
    esac
done

if [ -z "$TARGET_PATH" ]; then
    echo -e "${COLOR_RED}Error: No path provided."${COLOR_RESET}
    print_help
fi

if [ -f "$TARGET_PATH" ]; then
    # It's a file
    if [[ "$TARGET_PATH" == *.py ]]; then
        process_file "$TARGET_PATH"
    else
        echo -e "${COLOR_RED}Error: Provided file is not a Python file: $TARGET_PATH"${COLOR_RESET}
        exit 1
    fi
elif [ -d "$TARGET_PATH" ]; then
    # It's a directory
    find "$TARGET_PATH" -name "*.py" -print0 | while IFS= read -r -d $'\0' file;
    do
        # Only process files that look like test files or conftest.py
        if [[ $(basename "$file") == test_*.py || $(basename "$file") == conftest.py ]]; then
            process_file "$file"
        fi
    done
else
    echo -e "${COLOR_RED}Error: Path does not exist or is not a file/directory: $TARGET_PATH"${COLOR_RESET}
    exit 1
fi

exit 0
