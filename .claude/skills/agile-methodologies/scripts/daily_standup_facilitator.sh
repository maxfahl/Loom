#!/bin/bash

# daily_standup_facilitator.sh
# This script facilitates a daily stand-up meeting by prompting each team member
# for their updates and summarizing blockers.

# --- Configuration ---
# Default team members (can be overridden by command-line arguments)
DEFAULT_TEAM_MEMBERS=("Alice" "Bob" "Charlie")

# Output file for blockers (optional)
BLOCKERS_FILE="daily_standup_blockers_$(date +%Y-%m-%d).txt"

# --- Functions ---
function display_help() {
    echo "Usage: $0 [OPTIONS] [TEAM_MEMBER1 TEAM_MEMBER2 ...]"
    echo ""
    echo "Facilitates a daily stand-up meeting."
    echo "Prompts each team member for their updates and summarizes blockers."
    echo ""
    echo "Options:"
    echo "  -h, --help        Display this help message."
    echo "  -o, --output FILE Save identified blockers to FILE (default: $BLOCKERS_FILE)."
    echo "  -n, --no-output   Do not save blockers to a file."
    echo ""
    echo "If team members are provided as arguments, they will be used. Otherwise, defaults to:"
    echo "  ${DEFAULT_TEAM_MEMBERS[@]}"
    echo ""
    echo "Example:"
    echo "  $0                # Use default team members"
    echo "  $0 John Jane      # Specify team members John and Jane"
    echo "  $0 -o my_blockers.txt # Use default team, save blockers to my_blockers.txt"
}

function colored_echo() {
    local color="$1"
    local message="$2"
    case "$color" in
        "red")    echo -e "\033[0;31m${message}\033[0m" ;; 
        "green")  echo -e "\033[0;32m${message}\033[0m" ;; 
        "yellow") echo -e "\033[0;33m${message}\033[0m" ;; 
        "blue")   echo -e "\033[0;34m${message}\033[0m" ;; 
        *)        echo "${message}" ;; 
    esac
}

# --- Main Script ---

TEAM_MEMBERS=()
SAVE_BLOCKERS=true

# Parse command-line arguments
while [[ $# -gt 0 ]]; do
    key="$1"
    case $key in
        -h|--help)
            display_help
            exit 0
            ;; 
        -o|--output)
            BLOCKERS_FILE="$2"
            shift # past argument
            shift # past value
            ;; 
        -n|--no-output)
            SAVE_BLOCKERS=false
            shift # past argument
            ;; 
        *)
            TEAM_MEMBERS+=("$1") # Save it as a team member
            shift
            ;; 
    esac
done

# If no team members provided as arguments, use defaults
if [ ${#TEAM_MEMBERS[@]} -eq 0 ]; then
    TEAM_MEMBERS=("${DEFAULT_TEAM_MEMBERS[@]}")
fi

colored_echo "blue" "\n--- Daily Stand-up Facilitator ---"
colored_echo "blue" "Today's Date: $(date +%Y-%m-%d)"
colored_echo "blue" "Team Members: ${TEAM_MEMBERS[@]}"

ALL_BLOCKERS=()

for member in "${TEAM_MEMBERS[@]}"; do
    colored_echo "yellow" "\n--- ${member}'s Update ---"

    read -p "What did ${member} do yesterday? " YESTERDAY
    read -p "What will ${member} do today? " TODAY
    read -p "Are there any blockers for ${member}? (Type 'none' or leave empty if none) " BLOCKERS

    if [[ -n "$BLOCKERS" && "$(echo "$BLOCKERS" | tr '[:upper:]' '[:lower:]')" != "none" ]]; then
        ALL_BLOCKERS+=("${member}: ${BLOCKERS}")
        colored_echo "red" "Blocker identified for ${member}!"
    else
        colored_echo "green" "No blockers for ${member}."
    fi
done

colored_echo "blue" "\n--- Stand-up Summary ---"

if [ ${#ALL_BLOCKERS[@]} -gt 0 ]; then
    colored_echo "red" "\nIdentified Blockers:"
    for blocker in "${ALL_BLOCKERS[@]}"; do
        colored_echo "red" "- ${blocker}"
    done

    if $SAVE_BLOCKERS; then
        echo "Identified Blockers:" > "$BLOCKERS_FILE"
        for blocker in "${ALL_BLOCKERS[@]}"; do
            echo "- ${blocker}" >> "$BLOCKERS_FILE"
        done
        colored_echo "green" "Blockers saved to '$BLOCKERS_FILE'"
    fi
else
    colored_echo "green" "No blockers reported today! Great job, team!"
fi

colored_echo "blue" "\n--- Stand-up Complete ---"
