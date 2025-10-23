#!/bin/bash

# find-duplicate-code.sh
# Description: Scans a directory for potential code duplication *within each file* using a simple line-by-line comparison.
#              This script is a basic example; for robust *cross-file* analysis, consider dedicated tools like jscpd or pmd-cpd.

# Usage: ./find-duplicate-code.sh <directory> [min_lines] [exclude_pattern]
# Example: ./find-duplicate-code.sh ./src 10 "node_modules|dist"

# --- Configuration ---
DEFAULT_MIN_LINES=5
DEFAULT_EXCLUDE_PATTERN="node_modules|dist|.git|build|vendor"

# --- Helper Functions ---
print_help() {
    echo "Usage: $0 <directory> [min_lines] [exclude_pattern]"
    echo ""
    echo "Arguments:"
    echo "  <directory>       The directory to scan for duplicate code."
    echo "  [min_lines]       Optional. Minimum number of consecutive identical lines to consider as duplication. Default: ${DEFAULT_MIN_LINES}."
    echo "  [exclude_pattern] Optional. Regex pattern for directories/files to exclude. Default: \"${DEFAULT_EXCLUDE_PATTERN}\"."
    echo ""
    echo "Example:"
    echo "  $0 ./src 10 \"node_modules|dist\""
    echo "  $0 ."
    exit 0
}

# --- Main Logic ---

# Parse arguments
if [[ "$1" == "-h" || "$1" == "--help" ]]; then
    print_help
fi

TARGET_DIR="$1"
MIN_LINES=${2:-$DEFAULT_MIN_LINES}
EXCLUDE_PATTERN=${3:-$DEFAULT_EXCLUDE_PATTERN}

if [[ -z "$TARGET_DIR" ]]; then
    echo "Error: Missing target directory." >&2
    print_help
fi

if [[ ! -d "$TARGET_DIR" ]]; then
    echo "Error: Directory \"$TARGET_DIR\" not found." >&2
    exit 1
fi

echo "Scanning for intra-file duplicate code in: $(realpath "$TARGET_DIR")"
echo "Minimum consecutive lines for duplication: ${MIN_LINES}"
echo "Excluding patterns: ${EXCLUDE_PATTERN}"
echo "--------------------------------------------------"

# Prepare the exclude options for find
EXCLUDE_FIND_ARGS=()
if [[ -n "$EXCLUDE_PATTERN" ]]; then
    IFS='|' read -ra ADDR <<< "$EXCLUDE_PATTERN"
    for i in "${ADDR[@]}"; do
        EXCLUDE_FIND_ARGS+=("-path" "*/$i" "-prune" "-o")
    done
fi

# Find all relevant files, excluding specified patterns
find "$TARGET_DIR" "${EXCLUDE_FIND_ARGS[@]}" -type f \
    -name "*.ts" -o -name "*.tsx" -o \
    -name "*.js" -o -name "*.jsx" -o \
    -name "*.py" -o -name "*.java" -o \
    -name "*.c" -o -name "*.cpp" -o \
    -name "*.go" -o -name "*.php" -o \
    -name "*.rb" -o -name "*.cs" -o \
    -name "*.html" -o -name "*.css" -o \
    -name "*.scss" -o -name "*.less" -o \
    -name "*.json" -o -name "*.yaml" -o \
    -name "*.yml" -o -name "*.md"
) -print0 | while IFS= read -r -d $'\0' file; do
    echo "\n--- Checking file: $file ---"
    # Process each file with awk to find consecutive duplicate lines
    awk -v min_lines="$MIN_LINES" -v current_file="$file" 'BEGIN { OFS="\t"; found_duplicates=0 } {
        # Filter out common comment types and empty lines
        if ($0 ~ /^\s*(\/\/|#|\*|<!--|\/\*|\*\/)/ || $0 ~ /^\s*$/) {
            next;
        }

        content = $0;
        # Remove leading/trailing whitespace for comparison
        gsub(/^[ \t]+|[ \t]+$/, "", content);

        if (content == last_content) {
            current_count++;
        } else {
            if (current_count >= min_lines) {
                if (found_duplicates == 0) { print "Count", "Lines", "Content"; found_duplicates=1; } # Added header only once
                print current_count, last_line "-" (NR - 1), last_content;
            }
            current_count = 1;
            last_content = content;
            last_line = NR;
        }
    } END { 
        if (current_count >= min_lines) {
            if (found_duplicates == 0) { print "Count", "Lines", "Content"; found_duplicates=1; } # Added header only once
            print current_count, last_line "-" (NR), last_content; 
        }
        if (found_duplicates == 0) { print "No significant intra-file duplicates found." }
    }' "$file" | column -t -s $'\t'

done

echo "--------------------------------------------------"
echo "Scan complete. Note: This script checks for consecutive duplicate lines within each file."
echo "For cross-file duplication analysis, consider dedicated tools like jscpd (JavaScript/TypeScript) or pmd-cpd (Java/C#)."
