#!/bin/bash

# Story Migration Automation Script
# Purpose: Migrate stories from old locations to correct location per meta prompt spec
# Usage: bash scripts/migrate-stories.sh [FEATURE_NAME] [DRY_RUN]
# Example: bash scripts/migrate-stories.sh my-feature true

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
FEATURE_NAME="${1:-my-feature}"
DRY_RUN="${2:-false}"

# Print header
echo ""
echo -e "${BLUE}================================================${NC}"
echo -e "${BLUE}         Story Migration Script${NC}"
echo -e "${BLUE}================================================${NC}"
echo -e "Feature: ${YELLOW}$FEATURE_NAME${NC}"
echo -e "Dry Run: ${YELLOW}$DRY_RUN${NC}"
echo -e "${BLUE}================================================${NC}"
echo ""

# Step 1: Check for stories at old locations
echo -e "${YELLOW}[Step 1] Checking for stories at old locations...${NC}"

# Find stories at docs/stories/
OLD_STORIES_DOCS=""
if [ -d "docs/stories" ]; then
  OLD_STORIES_DOCS=$(find docs/stories -name "*.md" -type f 2>/dev/null || echo "")
fi

# Find stories at features/*/stories/
OLD_STORIES_FEATURES=""
if [ -d "features" ]; then
  OLD_STORIES_FEATURES=$(find features -name "*.md" -path "*/stories/*" -type f 2>/dev/null || echo "")
fi

# Find stories at docs/development/features/*/stories/ (wrong location - should be in epics/*/stories/)
OLD_STORIES_WRONG_DEV=""
if [ -d "docs/development/features" ]; then
  OLD_STORIES_WRONG_DEV=$(find docs/development/features -name "*.md" -path "*/stories/*" -not -path "*/epics/*" -type f 2>/dev/null || echo "")
fi

# Combine all old stories
ALL_OLD_STORIES=$(echo -e "${OLD_STORIES_DOCS}\n${OLD_STORIES_FEATURES}\n${OLD_STORIES_WRONG_DEV}" | grep -v "^$" || echo "")

# Count stories
DOCS_COUNT=0
if [ -n "$OLD_STORIES_DOCS" ]; then
  DOCS_COUNT=$(echo "$OLD_STORIES_DOCS" | grep -c "\.md$" || echo 0)
fi

FEATURES_COUNT=0
if [ -n "$OLD_STORIES_FEATURES" ]; then
  FEATURES_COUNT=$(echo "$OLD_STORIES_FEATURES" | grep -c "\.md$" || echo 0)
fi

WRONG_DEV_COUNT=0
if [ -n "$OLD_STORIES_WRONG_DEV" ]; then
  WRONG_DEV_COUNT=$(echo "$OLD_STORIES_WRONG_DEV" | grep -c "\.md$" || echo 0)
fi

TOTAL_COUNT=$((DOCS_COUNT + FEATURES_COUNT + WRONG_DEV_COUNT))

echo -e "Found ${GREEN}$DOCS_COUNT${NC} stories at ${YELLOW}docs/stories/${NC}"
echo -e "Found ${GREEN}$FEATURES_COUNT${NC} stories at ${YELLOW}features/*/stories/${NC}"
echo -e "Found ${GREEN}$WRONG_DEV_COUNT${NC} stories at ${YELLOW}docs/development/features/*/stories/${NC} (wrong location)"
echo -e "Total stories to migrate: ${GREEN}$TOTAL_COUNT${NC}"
echo ""

# Exit if no stories found
if [ $TOTAL_COUNT -eq 0 ]; then
  echo -e "${GREEN}✅ No stories found at old locations - nothing to migrate${NC}"
  echo ""
  exit 0
fi

# Step 2: Create epic directories
echo -e "${YELLOW}[Step 2] Creating epic directories...${NC}"

# Extract unique epic numbers from story filenames
# Story files are named X.Y.md where X is the epic number
EPIC_NUMBERS=""

if [ -n "$ALL_OLD_STORIES" ]; then
  EPIC_NUMBERS=$(echo "$ALL_OLD_STORIES" | while read -r file; do
    if [ -n "$file" ] && [ -f "$file" ]; then
      filename=$(basename "$file")
      # Extract epic number (first number before first dot)
      epic=$(echo "$filename" | sed -E 's/^([0-9]+)\..*$/\1/')
      if [[ "$epic" =~ ^[0-9]+$ ]]; then
        echo "$epic"
      fi
    fi
  done | sort -u -n)
fi

if [ -z "$EPIC_NUMBERS" ]; then
  echo -e "${RED}❌ Could not extract epic numbers from story filenames${NC}"
  exit 1
fi

# Create directories for each epic
for EPIC in $EPIC_NUMBERS; do
  EPIC_DIR="docs/development/features/$FEATURE_NAME/epics/epic-$EPIC"
  STORIES_DIR="$EPIC_DIR/stories"

  if [ "$DRY_RUN" = "true" ]; then
    echo -e "${BLUE}[DRY RUN]${NC} Would create: ${GREEN}$STORIES_DIR${NC}"
  else
    mkdir -p "$STORIES_DIR"
    echo -e "${GREEN}✅ Created:${NC} $STORIES_DIR"
  fi
done

echo ""

# Step 3: Move story files
echo -e "${YELLOW}[Step 3] Moving stories...${NC}"

MOVED_COUNT=0

# Process each story file
if [ -n "$ALL_OLD_STORIES" ]; then
  echo "$ALL_OLD_STORIES" | while read -r STORY_FILE; do
    if [ -n "$STORY_FILE" ] && [ -f "$STORY_FILE" ]; then
      FILENAME=$(basename "$STORY_FILE")

      # Extract epic number from filename
      EPIC=$(echo "$FILENAME" | sed -E 's/^([0-9]+)\..*$/\1/')

      # Validate epic number
      if ! [[ "$EPIC" =~ ^[0-9]+$ ]]; then
        echo -e "${RED}⚠️  Warning: Could not extract epic number from $FILENAME - skipping${NC}"
        continue
      fi

      # Construct target path
      EPIC_DIR="docs/development/features/$FEATURE_NAME/epics/epic-$EPIC"
      TARGET="$EPIC_DIR/stories/$FILENAME"

      if [ "$DRY_RUN" = "true" ]; then
        echo -e "${BLUE}[DRY RUN]${NC} Would move: ${YELLOW}$FILENAME${NC} → ${GREEN}epic-$EPIC/stories/${NC}"
      else
        mv "$STORY_FILE" "$TARGET"
        echo -e "${GREEN}✅ Moved:${NC} ${YELLOW}$FILENAME${NC} → ${GREEN}epic-$EPIC/stories/${NC}"
        MOVED_COUNT=$((MOVED_COUNT + 1))
      fi
    fi
  done
fi

echo ""

# Step 4: Clean up empty directories
echo -e "${YELLOW}[Step 4] Cleaning up empty directories...${NC}"

if [ "$DRY_RUN" = "true" ]; then
  echo -e "${BLUE}[DRY RUN]${NC} Would clean up empty directories after migration"
else
  # Remove docs/stories if empty
  if [ -d "docs/stories" ]; then
    if [ -z "$(ls -A docs/stories 2>/dev/null)" ]; then
      rmdir docs/stories 2>/dev/null && echo -e "${GREEN}✅ Removed empty:${NC} docs/stories/" || true
    else
      echo -e "${YELLOW}⚠️  docs/stories/ is not empty - not removing${NC}"
    fi
  fi

  # Remove empty features/*/stories/ directories
  if [ -d "features" ]; then
    find features -type d -name "stories" -empty -delete 2>/dev/null && echo -e "${GREEN}✅ Removed empty feature story directories${NC}" || true
  fi

  # Remove empty docs/development/features/*/stories/ (wrong location)
  if [ -d "docs/development/features" ]; then
    find docs/development/features -type d -name "stories" -not -path "*/epics/*" -empty -delete 2>/dev/null && echo -e "${GREEN}✅ Removed empty wrong-location directories${NC}" || true
  fi
fi

echo ""

# Step 5: Verification
echo -e "${YELLOW}[Step 5] Verification...${NC}"

if [ "$DRY_RUN" = "true" ]; then
  echo -e "${BLUE}[DRY RUN]${NC} Would verify migration of ${GREEN}$TOTAL_COUNT${NC} stories"
  echo -e "${BLUE}[DRY RUN]${NC} Stories would be located at: ${GREEN}docs/development/features/$FEATURE_NAME/epics/epic-*/stories/${NC}"
else
  # Count stories at new location
  NEW_STORY_COUNT=0
  if [ -d "docs/development/features/$FEATURE_NAME" ]; then
    NEW_STORY_COUNT=$(find "docs/development/features/$FEATURE_NAME" -name "*.md" -path "*/epics/*/stories/*" -type f 2>/dev/null | wc -l | tr -d ' ')
  fi

  # Verify counts match
  if [ "$NEW_STORY_COUNT" -eq "$TOTAL_COUNT" ]; then
    echo -e "${GREEN}✅ All $TOTAL_COUNT stories migrated successfully${NC}"
    echo ""
    echo -e "${GREEN}Migration Summary:${NC}"
    echo -e "  - Migrated stories: ${GREEN}$NEW_STORY_COUNT${NC}"
    echo -e "  - New location: ${GREEN}docs/development/features/$FEATURE_NAME/epics/epic-*/stories/${NC}"
    echo ""
    echo -e "Stories by epic:"
    for EPIC in $EPIC_NUMBERS; do
      EPIC_STORY_COUNT=$(find "docs/development/features/$FEATURE_NAME/epics/epic-$EPIC/stories" -name "*.md" -type f 2>/dev/null | wc -l | tr -d ' ')
      echo -e "  - Epic $EPIC: ${GREEN}$EPIC_STORY_COUNT${NC} stories"
    done
  else
    echo -e "${RED}❌ Migration count mismatch!${NC}"
    echo -e "  Expected: ${YELLOW}$TOTAL_COUNT${NC} stories"
    echo -e "  Found: ${YELLOW}$NEW_STORY_COUNT${NC} stories at new location"
    echo ""
    echo -e "${RED}Please investigate the discrepancy before proceeding.${NC}"
    exit 1
  fi
fi

echo ""
echo -e "${BLUE}================================================${NC}"
echo -e "${GREEN}✅ Migration complete!${NC}"
echo -e "${BLUE}================================================${NC}"
echo ""
