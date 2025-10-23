#!/bin/bash

# Loom CLAUDE.md Deployment Script
# Purpose: Deploy or update CLAUDE.md in user projects with marker-based section replacement
#
# Usage: bash scripts/deploy-claude-md.sh [TARGET_DIR] [PROJECT_NAME] [TECH_STACK] [TDD_LEVEL] [PREVIEW_CMD] [TEST_CMD] [BUILD_CMD]
# Example: bash scripts/deploy-claude-md.sh /path/to/my-project "My Project" "Next.js 14, React 18, TypeScript" "STRICT" "npm run dev" "npm test" "npm run build"

set -e

# --- Configuration ---

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"
LOOM_SOURCE_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
TEMPLATE_FILE="$LOOM_SOURCE_ROOT/prompts/reference/claude-md-template.md"

TARGET_DIR="${1}"
PROJECT_NAME="${2:-My Project}"
TECH_STACK="${3:-Not specified}"
TDD_LEVEL="${4:-RECOMMENDED}"
PREVIEW_COMMAND="${5:-npm run dev}"
TEST_COMMAND="${6:-npm test}"
BUILD_COMMAND="${7:-npm run build}"

# Markers for identifying framework-managed sections
MARKER_START="<!-- LOOM_FRAMEWORK_START -->"
MARKER_END="<!-- LOOM_FRAMEWORK_END -->"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# --- Validation ---

if [ -z "$TARGET_DIR" ]; then
    echo -e "${RED}❌ Error: Target directory not provided.${NC}"
    echo "Usage: bash scripts/deploy-claude-md.sh [TARGET_DIR] [PROJECT_NAME] [TECH_STACK] [TDD_LEVEL] [PREVIEW_CMD] [TEST_CMD] [BUILD_CMD]"
    exit 1
fi

if [ ! -d "$TARGET_DIR" ]; then
    echo -e "${RED}❌ Error: Target directory '$TARGET_DIR' does not exist.${NC}"
    exit 1
fi

if [ ! -f "$TEMPLATE_FILE" ]; then
    echo -e "${RED}❌ Error: Template file not found at: $TEMPLATE_FILE${NC}"
    exit 1
fi

# --- Functions ---

# Extract framework section from template
extract_framework_section() {
    local template_file=$1
    awk "/$MARKER_START/,/$MARKER_END/" "$template_file"
}

# Replace placeholders in content
replace_placeholders() {
    local content="$1"
    local date=$(date +"%Y-%m-%d")

    # Replace all placeholders
    content="${content//\[PROJECT_NAME\]/$PROJECT_NAME}"
    content="${content//\[YYYY-MM-DD\]/$date}"
    content="${content//\[TECH_STACK\]/$TECH_STACK}"
    content="${content//\[TDD_LEVEL\]/$TDD_LEVEL}"
    content="${content//\[PREVIEW_COMMAND\]/$PREVIEW_COMMAND}"
    content="${content//\[TEST_COMMAND\]/$TEST_COMMAND}"
    content="${content//\[BUILD_COMMAND\]/$BUILD_COMMAND}"

    # Handle conditional TDD sections
    if [ "$TDD_LEVEL" = "STRICT" ]; then
        content=$(echo "$content" | sed '/\[IF STRICT\]/,/\[IF RECOMMENDED\]/!d;//d')
    elif [ "$TDD_LEVEL" = "RECOMMENDED" ]; then
        content=$(echo "$content" | sed '/\[IF RECOMMENDED\]/,/\[IF OPTIONAL\]/!d;//d')
    else
        content=$(echo "$content" | sed '/\[IF OPTIONAL\]/,/^$/!d;//d')
    fi

    echo "$content"
}

# --- Main Execution ---

TARGET_FILE="$TARGET_DIR/CLAUDE.md"

echo ""
echo -e "${BLUE}================================================${NC}"
echo -e "${BLUE}      Loom CLAUDE.md Deployment Script         ${NC}"
echo -e "${BLUE}================================================${NC}"
echo -e "Template:    ${YELLOW}$TEMPLATE_FILE${NC}"
echo -e "Target:      ${YELLOW}$TARGET_FILE${NC}"
echo -e "Project:     ${YELLOW}$PROJECT_NAME${NC}"
echo -e "TDD Level:   ${YELLOW}$TDD_LEVEL${NC}"
echo -e "${BLUE}================================================${NC}"
echo ""

# Read the template
TEMPLATE_CONTENT=$(cat "$TEMPLATE_FILE")

# Extract framework section from template
FRAMEWORK_SECTION=$(extract_framework_section "$TEMPLATE_FILE")

# Replace placeholders in entire template
PROCESSED_TEMPLATE=$(replace_placeholders "$TEMPLATE_CONTENT")

# Check if target CLAUDE.md exists
if [ -f "$TARGET_FILE" ]; then
    echo -e "${YELLOW}Found existing CLAUDE.md${NC}"

    # Check if it has Loom markers
    if grep -q "$MARKER_START" "$TARGET_FILE" && grep -q "$MARKER_END" "$TARGET_FILE"; then
        echo -e "${GREEN}✓ Loom markers detected - performing marker-based update${NC}"

        # Extract sections: before markers, between markers, after markers
        BEFORE_MARKERS=$(awk "/$MARKER_START/{exit} {print}" "$TARGET_FILE")
        AFTER_MARKERS=$(awk "/$MARKER_END/{flag=1; next} flag" "$TARGET_FILE")

        # Extract framework section from processed template
        NEW_FRAMEWORK_SECTION=$(echo "$PROCESSED_TEMPLATE" | awk "/$MARKER_START/,/$MARKER_END/")

        # Reconstruct file: keep user sections, replace framework section
        {
            echo "$BEFORE_MARKERS"
            echo ""
            echo "$NEW_FRAMEWORK_SECTION"
            echo ""
            echo "$AFTER_MARKERS"
        } > "$TARGET_FILE"

        echo -e "${GREEN}✅ Updated framework section in existing CLAUDE.md${NC}"
        echo -e "${GREEN}   User customizations preserved${NC}"

    else
        echo -e "${YELLOW}⚠️  No Loom markers found in existing CLAUDE.md${NC}"
        echo -e "${YELLOW}   This appears to be a custom CLAUDE.md file.${NC}"
        echo ""
        echo -e "${BLUE}Creating LOOM_FRAMEWORK.md as a separate file...${NC}"

        LOOM_FRAMEWORK_FILE="$TARGET_DIR/LOOM_FRAMEWORK.md"
        echo "$PROCESSED_TEMPLATE" > "$LOOM_FRAMEWORK_FILE"

        echo -e "${GREEN}✅ Created LOOM_FRAMEWORK.md${NC}"
        echo -e "${YELLOW}   Your existing CLAUDE.md was preserved${NC}"
        echo -e "${YELLOW}   You can merge the two files manually if desired${NC}"
    fi

else
    echo -e "${BLUE}No existing CLAUDE.md found - creating new file${NC}"

    # Create new CLAUDE.md with processed template
    echo "$PROCESSED_TEMPLATE" > "$TARGET_FILE"

    echo -e "${GREEN}✅ Created new CLAUDE.md${NC}"
fi

echo ""
echo -e "${GREEN}✅ Deployment complete${NC}"
echo ""

# Show file location
echo -e "${BLUE}File location:${NC} $TARGET_FILE"

# Show marker info
if [ -f "$TARGET_FILE" ] && grep -q "$MARKER_START" "$TARGET_FILE"; then
    echo ""
    echo -e "${BLUE}ℹ️  Marker-based updating enabled${NC}"
    echo -e "   Framework sections between markers will be auto-updated on future runs"
    echo -e "   Add your customizations outside the markers to preserve them"
fi

echo ""
