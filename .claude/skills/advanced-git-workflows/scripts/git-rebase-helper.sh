#!/bin/bash

# git-rebase-helper.sh
# Description: An interactive script to simplify common Git interactive rebase operations.
#              It provides a menu to squash, fixup, reword, or edit commits easily.
# Usage: ./git-rebase-helper.sh [number_of_commits]
#        If number_of_commits is not provided, it defaults to 5.

# Configuration:
# You can set your preferred editor by setting the GIT_EDITOR environment variable.
# export GIT_EDITOR="code --wait" # For VS Code
# export GIT_EDITOR="nano" # For Nano

# --- Helper Functions ---

# Function to display colored output
function echo_color() {
    COLOR=$1
    TEXT=$2
    case $COLOR in
        "red")    echo -e "\033[0;31m${TEXT}\033[0m";;
        "green")  echo -e "\033[0;32m${TEXT}\033[0m";;
        "yellow") echo -e "\033[0;33m${TEXT}\033[0m";;
        "blue")   echo -e "\033[0;34m${TEXT}\033[0m";;
        "purple") echo -e "\033[0;35m${TEXT}\033[0m";;
        "cyan")   echo -e "\033[0;36m${TEXT}\033[0m";;
        *)        echo "${TEXT}";;
    esac
}

# Function to display usage information
function display_usage() {
    echo_color "cyan" "Usage: $(basename "$0") [number_of_commits]"
    echo "  number_of_commits: Optional. The number of commits from HEAD~ to include in the interactive rebase."
    echo "                     Defaults to 5 if not provided."
    echo "Description: This script simplifies interactive rebase operations by providing a menu."
    echo "             It helps in squashing, fixup, reordering, or editing commits."
    echo "             Ensure you are on the branch you want to rebase."
    echo "             Your default Git editor will be used for the interactive rebase."
    echo "Examples:"
    echo "  $(basename "$0")"             # Rebase last 5 commits
    echo "  $(basename "$0") 10"          # Rebase last 10 commits
    echo "  GIT_EDITOR=\"code --wait\" $(basename "$0")" # Use VS Code as editor
    exit 0
}

# --- Main Script Logic ---

# Check for --help or -h
if [[ "$1" == "--help" || "$1" == "-h" ]]; then
    display_usage
fi

# Check if inside a Git repository
git rev-parse --is-inside-work-tree > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo_color "red" "Error: Not inside a Git repository. Please run this script from a Git repository."
    exit 1
fi

# Determine number of commits to rebase
NUM_COMMITS=${1:-5} # Default to 5 if no argument is provided

# Validate NUM_COMMITS is a positive integer
if ! [[ "$NUM_COMMITS" =~ ^[1-9][0-9]*$ ]]; then
    echo_color "red" "Error: Invalid number of commits specified. Please provide a positive integer."
    display_usage
fi

# Get current branch name
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)

echo_color "blue" "Starting interactive rebase on branch: ${CURRENT_BRANCH}"
echo_color "blue" "Rebasing last ${NUM_COMMITS} commits (HEAD~${NUM_COMMITS}..HEAD)"

echo_color "yellow" "\nYour default Git editor will open. Follow the instructions within the editor to:"
echo_color "yellow" "  - 'pick' (use commit)"
echo_color "yellow" "  - 'reword' (use commit, but edit commit message)"
echo_color "yellow" "  - 'edit' (use commit, but stop for amending)"
echo_color "yellow" "  - 'squash' (use commit, but meld into previous commit)"
echo_color "yellow" "  - 'fixup' (like 'squash', but discard this commit's log message)"
echo_color "yellow" "  - 'drop' (remove commit)"
echo_color "yellow" "You can also reorder lines to change the order of commits.\n"

# Perform the interactive rebase
# The GIT_SEQUENCE_EDITOR is set to true to ensure the default editor is used.
# This is a common way to ensure the interactive rebase prompt appears.
GIT_SEQUENCE_EDITOR=true git rebase -i HEAD~${NUM_COMMITS}

# Check the exit status of the rebase command
if [ $? -eq 0 ]; then
    echo_color "green" "\nInteractive rebase completed successfully!"
    echo_color "green" "Run 'git log --oneline' to see the updated history."
else
    echo_color "red" "\nInteractive rebase failed or was aborted."
    echo_color "red" "If conflicts occurred, resolve them and then run 'git rebase --continue'."
    echo_color "red" "To abort, run 'git rebase --abort'."
fi

exit 0
