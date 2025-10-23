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
SYNC_ITEMS=(
    ".claude/agents"
    ".claude/commands"
    "docs/development/CODE_REVIEW_PRINCIPLES.md"
    "docs/development/DESIGN_PRINCIPLES.md"
    "docs/development/SECURITY_REVIEW_CHECKLIST.md"
    "docs/development/YOLO_MODE.md"
    "prompts/templates/story-template.md"
    "scripts/migrate-stories.sh"
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
    local item_path=$1
    local source_base_path="$LOOM_SOURCE_ROOT/$item_path"
    local target_base_path="$TARGET_DIR/$item_path"

    if [ ! -e "$source_base_path" ]; then
        echo -e "${YELLOW}⚠️ Warning: Source item does not exist, skipping: $source_base_path${NC}"
        return
    fi

    # If it's a directory, sync its contents recursively
    if [ -d "$source_base_path" ]; then
        echo -e "${BLUE}Syncing directory: $item_path${NC}"
        find "$source_base_path" -type f | while read -r source_file; do
            local relative_path="${source_file#$LOOM_SOURCE_ROOT/}"
            sync_single_file "$relative_path"
        done
    # If it's a single file
    else
        sync_single_file "$item_path"
    fi
}

# Function to sync a single file
sync_single_file() {
    local file_relative_path=$1
    local source_file="$LOOM_SOURCE_ROOT/$file_relative_path"
    local target_file="$TARGET_DIR/$file_relative_path"

    local source_hash=$(get_file_hash "$source_file")
    local target_hash=$(get_file_hash "$target_file")

    # 1. If target does not exist
    if [ -z "$target_hash" ]; then
        echo -e "  ${GREEN}CREATE${NC}:  $file_relative_path"
        if [ "$DRY_RUN" = "false" ]; then
            mkdir -p "$(dirname "$target_file")"
            cp "$source_file" "$target_file"
        fi
    # 2. If hashes are different
    elif [ "$source_hash" != "$target_hash" ]; then
        echo -e "  ${YELLOW}UPDATE${NC}:  $file_relative_path (hashes differ)"
        if [ "$DRY_RUN" = "false" ]; then
            cp "$source_file" "$target_file"
        fi
    # 3. If hashes are the same
    else
        # Quiet by default, uncomment to be verbose
        # echo -e "  SKIP:    $file_relative_path (hashes match)"
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

echo ""
echo -e "${GREEN}✅ Synchronization complete.${NC}"
echo ""
