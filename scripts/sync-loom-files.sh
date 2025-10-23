#!/bin/bash

# Loom Files Synchronization Script
# Purpose: Intelligently copy agents, commands, and other configuration files
# from the Loom framework source to a target project directory.
#
# Usage: bash scripts/sync-loom-files.sh [TARGET_DIR] [DRY_RUN]
# Example: bash scripts/sync-loom-files.sh /path/to/my-project true

set -e

# --- Configuration ---

# The directory where this script is located, used to find the Loom source root.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"
LOOM_SOURCE_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

TARGET_DIR="${1}"
DRY_RUN="${2:-false}"

# Files and directories to sync
# Note: We sync from prompts/reference/* (templates) to target's .claude/* directories
SYNC_ITEMS=(
    ".claude/agents:.claude/agents"
    ".claude/AGENTS.md:.claude/AGENTS.md"
    ".claude/commands:.claude/commands"
    ".claude/skills:.claude/skills"
    "prompts/templates:prompts/templates"
)

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# --- Validation ---

if [ -z "$TARGET_DIR" ]; then
    echo -e "${RED}❌ Error: Target directory not provided.${NC}"
    echo "Usage: bash scripts/sync-loom-files.sh [TARGET_DIR] [DRY_RUN]"
    exit 1
fi

if [ ! -d "$TARGET_DIR" ]; then
    echo -e "${RED}❌ Error: Target directory '$TARGET_DIR' does not exist.${NC}"
    exit 1
fi

# --- Functions ---

# Function to get the SHA256 hash of a file
get_file_hash() {
    local file=$1
    if [ -f "$file" ]; then
        shasum -a 256 "$file" | awk '{print $1}'
    else
        echo ""
    fi
}

# Function to sync a single file or a directory
sync_item() {
    local item_spec=$1

    # Parse source:target mapping (e.g., ".claude/agents:.claude/agents")
    local source_path
    local target_path

    if [[ "$item_spec" == *":"* ]]; then
        source_path="${item_spec%%:*}"
        target_path="${item_spec##*:}"
    else
        # If no mapping, use same path for both
        source_path="$item_spec"
        target_path="$item_spec"
    fi

    local source_base_path="$LOOM_SOURCE_ROOT/$source_path"
    local target_base_path="$TARGET_DIR/$target_path"

    if [ ! -e "$source_base_path" ]; then
        echo -e "${YELLOW}⚠️ Warning: Source item does not exist, skipping: $source_base_path${NC}"
        return
    fi

    # If it's a directory, sync its contents recursively
    if [ -d "$source_base_path" ]; then
        echo -e "${BLUE}Syncing directory: $source_path → $target_path${NC}"
        find "$source_base_path" -type f | while read -r source_file; do
            # Get relative path from source directory
            local file_relative_to_source="${source_file#$source_base_path/}"
            # Build target file path
            local target_file="$target_base_path/$file_relative_to_source"
            sync_single_file "$source_file" "$target_file" "$file_relative_to_source"
        done
    # If it's a single file
    else
        local target_file="$target_base_path"
        sync_single_file "$source_base_path" "$target_file" "$source_path"
    fi
}

# Function to sync a single file
sync_single_file() {
    local source_file=$1
    local target_file=$2
    local display_path=$3

    local source_hash=$(get_file_hash "$source_file")
    local target_hash=$(get_file_hash "$target_file")

    # 1. If target does not exist
    if [ -z "$target_hash" ]; then
        echo -e "  ${GREEN}CREATE${NC}:  $display_path"
        if [ "$DRY_RUN" = "false" ]; then
            mkdir -p "$(dirname "$target_file")"
            cp "$source_file" "$target_file"
        fi
    # 2. If hashes are different
    elif [ "$source_hash" != "$target_hash" ]; then
        echo -e "  ${YELLOW}UPDATE${NC}:  $display_path (hashes differ)"
        if [ "$DRY_RUN" = "false" ]; then
            cp "$source_file" "$target_file"
        fi
    # 3. If hashes are the same
    else
        # Quiet by default, uncomment to be verbose
        # echo -e "  SKIP:    $display_path (hashes match)"
        :
    fi
}


# --- Main Execution ---

echo ""
echo -e "${BLUE}================================================${NC}"
echo -e "${BLUE}      Loom Framework Files Synchronization      ${NC}"
echo -e "${BLUE}================================================${NC}"
echo -e "Source:  ${YELLOW}$LOOM_SOURCE_ROOT${NC}"
echo -e "Target:  ${YELLOW}$TARGET_DIR${NC}"
echo -e "Dry Run: ${YELLOW}$DRY_RUN${NC}"
echo -e "${BLUE}================================================${NC}"
echo ""

for item in "${SYNC_ITEMS[@]}"; do
    sync_item "$item"
done

# --- Create Project Directories ---

echo -e "${BLUE}Creating project directories...${NC}"

# Create thinking sessions directory
THINKING_SESSIONS_DIR="$TARGET_DIR/.loom/thinking-sessions"
if [ ! -d "$THINKING_SESSIONS_DIR" ]; then
    echo -e "  ${GREEN}CREATE${NC}:  .loom/thinking-sessions/"
    if [ "$DRY_RUN" = "false" ]; then
        mkdir -p "$THINKING_SESSIONS_DIR"
    fi
else
    echo -e "  SKIP:    .loom/thinking-sessions/ (already exists)"
fi

# Create retrospectives directory
RETROSPECTIVES_DIR="$TARGET_DIR/.loom/retrospectives"
if [ ! -d "$RETROSPECTIVES_DIR" ]; then
    echo -e "  ${GREEN}CREATE${NC}:  .loom/retrospectives/"
    if [ "$DRY_RUN" = "false" ]; then
        mkdir -p "$RETROSPECTIVES_DIR"
    fi
else
    echo -e "  SKIP:    .loom/retrospectives/ (already exists)"
fi

echo ""
echo -e "${GREEN}✅ Synchronization complete.${NC}"
echo ""
