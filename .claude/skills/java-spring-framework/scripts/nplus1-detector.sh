#!/bin/bash

# nplus1-detector.sh
#
# Purpose: Analyzes application logs to detect potential N+1 query problems.
#          It looks for repetitive SQL SELECT statements that often indicate
#          inefficient data fetching patterns in ORM-based applications (like Spring Data JPA).
#
# Usage:
#   ./nplus1-detector.sh <path_to_application_log_file>
#   Example: ./nplus1-detector.sh target/logs/application.log
#
# Features:
#   - Filters log entries for SQL SELECT statements.
#   - Identifies sequences of identical or highly similar SELECT queries.
#   - Reports potential N+1 occurrences with surrounding log context.
#   - Configurable threshold for repetition detection.
#
# Configuration:
#   - `MIN_REPETITIONS`: Minimum number of consecutive identical/similar queries to flag as N+1.
#   - `CONTEXT_LINES`: Number of lines before and after the N+1 pattern to show for context.
#   - `SQL_PATTERN`: Regex to identify SQL SELECT statements in logs.
#
# Error Handling:
#   - Checks if the log file exists.
#   - Provides clear output messages.

# --- Configuration ---
MIN_REPETITIONS=5 # Flag if a query repeats this many times or more consecutively
CONTEXT_LINES=3   # Show this many lines before and after the N+1 pattern
SQL_PATTERN="(select|SELECT).*?(from|FROM).*?"

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

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
    exit 1
}

# Function to normalize SQL queries for comparison
# Removes specific values, aliases, and whitespace to compare query structure
normalize_sql() {
    echo "$1" \
    | sed -E 's/\'[^']*\'/[VALUE]/g' \
    | sed -E 's/[0-9]+/[NUMBER]/g' \
    | sed -E 's/as [a-zA-Z0-9_]+//gI' \
    | sed -E 's/\s+/ /g' \
    | tr -d '\n\t\r' \
    | sed -E 's/WHERE [^;]*//gI' # Remove WHERE clause for broader similarity
}

# --- Main Script Logic ---

log_info "Starting N+1 Query Detector..."

if [ -z "$1" ]; then
    log_error "Usage: $0 <path_to_application_log_file>"
fi

LOG_FILE="$1"

if [ ! -f "$LOG_FILE" ]; then
    log_error "Log file not found: ${LOG_FILE}"
fi

log_info "Analyzing log file: ${LOG_FILE} for N+1 query patterns..."
log_info "Minimum repetitions to flag: ${MIN_REPETITIONS}"

# Read log file line by line, keeping track of previous SQL queries
PREV_NORMALIZED_SQL=""
PREV_SQL_LINE=""
REPETITION_COUNT=0
START_LINE_INDEX=0
LINE_INDEX=0

# Store all lines to retrieve context later
ALL_LOG_LINES=()
while IFS= read -r line || [[ -n "$line" ]]; do
    ALL_LOG_LINES+=("$line")
    LINE_INDEX=$((LINE_INDEX + 1))

    if [[ "$line" =~ $SQL_PATTERN ]]; then
        CURRENT_SQL_LINE="$line"
        CURRENT_NORMALIZED_SQL=$(normalize_sql "$CURRENT_SQL_LINE")

        if [ "$CURRENT_NORMALIZED_SQL" == "$PREV_NORMALIZED_SQL" ] && [ -n "$CURRENT_NORMALIZED_SQL" ]; then
            REPETITION_COUNT=$((REPETITION_COUNT + 1))
        else
            # Check if previous sequence was an N+1
            if [ "$REPETITION_COUNT" -ge "$MIN_REPETITIONS" ]; then
                log_warning "\n--- POTENTIAL N+1 QUERY DETECTED (Lines $((START_LINE_INDEX - CONTEXT_LINES))) - $((LINE_INDEX - 1))) ---"
                log_warning "Query repeated ${REPETITION_COUNT} times:"
                echo -e "${YELLOW}${PREV_SQL_LINE}${NC}"
                log_info "Context around the N+1 pattern:"
                # Print context lines
                for ((i=START_LINE_INDEX - CONTEXT_LINES -1; i<LINE_INDEX -1; i++)); do
                    if [ "$i" -ge 0 ] && [ "$i" -lt "${#ALL_LOG_LINES[@]}" ]; then
                        echo "${ALL_LOG_LINES[$i]}"
                    fi
                done
                log_warning "-------------------------------------------------------------------"
            fi
            # Reset for new sequence
            PREV_NORMALIZED_SQL="$CURRENT_NORMALIZED_SQL"
            PREV_SQL_LINE="$CURRENT_SQL_LINE"
            REPETITION_COUNT=1
            START_LINE_INDEX=$LINE_INDEX
        fi
    else
        # If a non-SQL line breaks the sequence, check if previous sequence was an N+1
        if [ "$REPETITION_COUNT" -ge "$MIN_REPETITIONS" ]; then
            log_warning "\n--- POTENTIAL N+1 QUERY DETECTED (Lines $((START_LINE_INDEX - CONTEXT_LINES))) - $((LINE_INDEX - 1))) ---"
            log_warning "Query repeated ${REPETITION_COUNT} times:"
            echo -e "${YELLOW}${PREV_SQL_LINE}${NC}"
            log_info "Context around the N+1 pattern:"
            # Print context lines
            for ((i=START_LINE_INDEX - CONTEXT_LINES -1; i<LINE_INDEX -1; i++)); do
                if [ "$i" -ge 0 ] && [ "$i" -lt "${#ALL_LOG_LINES[@]}" ]; then
                    echo "${ALL_LOG_LINES[$i]}"
                fi
            done
            log_warning "-------------------------------------------------------------------"
        fi
        # Reset for new sequence
        PREV_NORMALIZED_SQL=""
        PREV_SQL_LINE=""
        REPETITION_COUNT=0
        START_LINE_INDEX=0
    fi
done

# Final check for N+1 at the end of the file
if [ "$REPETITION_COUNT" -ge "$MIN_REPETITIONS" ]; then
    log_warning "\n--- POTENTIAL N+1 QUERY DETECTED (Lines $((START_LINE_INDEX - CONTEXT_LINES))) - $((LINE_INDEX - 1))) ---"
    log_warning "Query repeated ${REPETITION_COUNT} times:"
    echo -e "${YELLOW}${PREV_SQL_LINE}${NC}"
    log_info "Context around the N+1 pattern:"
    # Print context lines
    for ((i=START_LINE_INDEX - CONTEXT_LINES -1; i<LINE_INDEX -1; i++)); do
        if [ "$i" -ge 0 ] && [ "$i" -lt "${#ALL_LOG_LINES[@]}" ]; then
            echo "${ALL_LOG_LINES[$i]}"
        fi
    done
    log_warning "-------------------------------------------------------------------"
fi

log_info "N+1 Query Detector finished analysis."
log_info "Review the warnings above for potential performance bottlenecks."
