#!/usr/bin/env bash
#
# hotfix-workflow.sh - Streamlined Git Flow hotfix workflow
#
# Purpose:
#   Manages emergency production fixes following Git Flow conventions.
#   Guides through hotfix creation, testing, and deployment.
#
# Usage:
#   ./hotfix-workflow.sh create <version>     Create hotfix branch
#   ./hotfix-workflow.sh finalize <version>   Finalize hotfix
#   ./hotfix-workflow.sh status               Show hotfix status
#
# Options:
#   --main <branch>         Main branch name (default: main)
#   --develop <branch>      Develop branch name (default: develop)
#   --remote <name>         Remote name (default: origin)
#   --auto-version          Auto-increment patch version
#   --dry-run               Show what would be done
#   -h, --help              Show this help
#
# Examples:
#   ./hotfix-workflow.sh create 1.2.1
#   ./hotfix-workflow.sh create --auto-version
#   ./hotfix-workflow.sh finalize 1.2.1
#
# Environment Variables:
#   GIT_FLOW_MAIN       Override main branch name
#   GIT_FLOW_DEVELOP    Override develop branch name
#
# Exit Codes:
#   0 - Success
#   1 - Invalid arguments
#   2 - Git errors
#   3 - Validation errors
#

set -euo pipefail

# Configuration
MAIN_BRANCH="${GIT_FLOW_MAIN:-main}"
DEVELOP_BRANCH="${GIT_FLOW_DEVELOP:-develop}"
REMOTE="origin"
AUTO_VERSION=false
DRY_RUN=false
COMMAND=""
VERSION=""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
NC='\033[0m'

log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
log_warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }
log_urgent() { echo -e "${MAGENTA}[URGENT]${NC} $1"; }

show_help() {
    sed -n '/^#/,/^$/p' "$0" | sed 's/^# \?//' | tail -n +2 | head -n -1
    exit 0
}

execute() {
    if [ "$DRY_RUN" = true ]; then
        echo -e "${YELLOW}[DRY-RUN]${NC} $*"
    else
        "$@"
    fi
}

# Validate semantic version
validate_version() {
    local version="$1"
    if [[ ! "$version" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
        log_error "Invalid semantic version: $version"
        log_error "Expected format: X.Y.Z (e.g., 1.2.1)"
        return 1
    fi
    return 0
}

# Get next patch version
get_next_patch_version() {
    local latest_tag
    latest_tag=$(git describe --tags --abbrev=0 2>/dev/null || echo "v0.0.0")
    latest_tag="${latest_tag#v}" # Remove 'v' prefix

    # Extract version parts
    IFS='.' read -r major minor patch <<< "$latest_tag"

    # Increment patch
    patch=$((patch + 1))

    echo "$major.$minor.$patch"
}

# Create hotfix branch
create_hotfix() {
    log_urgent "Creating emergency hotfix branch"

    # Determine version
    if [ "$AUTO_VERSION" = true ]; then
        VERSION=$(get_next_patch_version)
        log_info "Auto-generated version: $VERSION"
    elif [ -z "$VERSION" ]; then
        log_error "Version required. Use --auto-version or specify version."
        return 1
    fi

    # Validate version
    if ! validate_version "$VERSION"; then
        return 3
    fi

    local hotfix_branch="hotfix/$VERSION"

    # Check if hotfix branch already exists
    if git show-ref --verify --quiet "refs/heads/$hotfix_branch"; then
        log_error "Hotfix branch already exists: $hotfix_branch"
        return 2
    fi

    # Checkout main and update
    log_info "Checking out $MAIN_BRANCH (production code)..."
    execute git checkout "$MAIN_BRANCH"
    execute git pull "$REMOTE" "$MAIN_BRANCH"

    # Create hotfix branch from main
    log_info "Creating hotfix branch from $MAIN_BRANCH..."
    execute git checkout -b "$hotfix_branch" "$MAIN_BRANCH"

    # Push to remote
    log_info "Pushing hotfix branch to remote..."
    execute git push -u "$REMOTE" "$hotfix_branch"

    # Show success and next steps
    echo ""
    log_success "Hotfix branch created: $hotfix_branch"
    echo ""
    echo "🚨 EMERGENCY FIX WORKFLOW 🚨"
    echo ""
    echo "Next steps:"
    echo "  1. ⚠️  Fix the critical bug (minimal changes only)"
    echo "  2. 🧪 Test thoroughly in production-like environment"
    echo "  3. 💾 Commit: git commit -m 'fix: describe critical bug fix'"
    echo "  4. 🔧 Update version files if needed"
    echo "  5. ✅ Finalize: ./hotfix-workflow.sh finalize $VERSION"
    echo ""
    log_warning "Keep changes minimal and focused on the critical issue!"

    return 0
}

# Finalize hotfix
finalize_hotfix() {
    log_urgent "Finalizing hotfix $VERSION"

    if [ -z "$VERSION" ]; then
        log_error "Version required"
        return 1
    fi

    local hotfix_branch="hotfix/$VERSION"

    # Check if hotfix branch exists
    if ! git show-ref --verify --quiet "refs/heads/$hotfix_branch"; then
        log_error "Hotfix branch does not exist: $hotfix_branch"
        return 2
    fi

    # Checkout hotfix branch
    execute git checkout "$hotfix_branch"
    execute git pull "$REMOTE" "$hotfix_branch"

    # Check if there are uncommitted changes
    if ! git diff-index --quiet HEAD --; then
        log_error "Uncommitted changes detected. Commit or stash them first."
        return 2
    fi

    # Update version files
    log_info "Updating version files..."
    if [ -f "package.json" ] && [ "$DRY_RUN" = false ]; then
        npm version "$VERSION" --no-git-tag-version 2>/dev/null || true
        execute git add package.json
    fi

    # Commit version bump if there are staged changes
    if ! git diff-index --quiet --cached HEAD --; then
        execute git commit -m "chore: bump version to $VERSION"
    fi

    # Merge to main
    log_info "Merging hotfix to $MAIN_BRANCH..."
    execute git checkout "$MAIN_BRANCH"
    execute git pull "$REMOTE" "$MAIN_BRANCH"
    execute git merge --no-ff "$hotfix_branch" -m "Hotfix version $VERSION"

    # Tag the release
    local tag_name="v$VERSION"
    log_info "Creating tag: $tag_name"
    execute git tag -a "$tag_name" -m "Hotfix version $VERSION - emergency production fix"

    # Push main with tags
    log_info "Pushing $MAIN_BRANCH with tags..."
    execute git push "$REMOTE" "$MAIN_BRANCH" --tags

    # Merge to develop (or current release branch if exists)
    local target_branch="$DEVELOP_BRANCH"

    # Check if there's an active release branch
    local release_branches
    release_branches=$(git branch --list "release/*" | sed 's/^[* ]*//')

    if [ -n "$release_branches" ]; then
        local release_branch
        release_branch=$(echo "$release_branches" | head -n 1)
        log_warning "Active release branch found: $release_branch"
        log_warning "Merging to $release_branch instead of $DEVELOP_BRANCH"
        target_branch="$release_branch"
    fi

    log_info "Merging hotfix to $target_branch..."
    execute git checkout "$target_branch"
    execute git pull "$REMOTE" "$target_branch"
    execute git merge --no-ff "$hotfix_branch" -m "Merge hotfix $VERSION"
    execute git push "$REMOTE" "$target_branch"

    # Delete hotfix branch
    log_info "Cleaning up hotfix branch..."
    execute git branch -d "$hotfix_branch"
    execute git push "$REMOTE" --delete "$hotfix_branch"

    # Success message
    echo ""
    log_success "🎉 Hotfix $VERSION deployed successfully!"
    echo ""
    echo "Summary:"
    echo "  ✅ Merged to $MAIN_BRANCH"
    echo "  ✅ Tagged as $tag_name"
    echo "  ✅ Merged to $target_branch"
    echo "  ✅ Hotfix branch deleted"
    echo ""
    echo "🚀 Production fix is now live!"
    echo ""

    # Show deployment reminder
    log_warning "Don't forget to:"
    echo "  1. Deploy $MAIN_BRANCH to production"
    echo "  2. Verify the fix in production"
    echo "  3. Update incident documentation"
    echo "  4. Notify stakeholders"

    return 0
}

# Show hotfix status
show_status() {
    echo ""
    echo -e "${MAGENTA}=== Git Flow Hotfix Status ===${NC}"
    echo ""

    # Current branch
    local current_branch
    current_branch=$(git rev-parse --abbrev-ref HEAD)
    echo "Current branch: $current_branch"

    # Active hotfix branches
    local hotfix_branches
    hotfix_branches=$(git branch --list "hotfix/*" | sed 's/^[* ]*//')

    if [ -n "$hotfix_branches" ]; then
        echo ""
        log_urgent "Active hotfix branches:"
        echo "$hotfix_branches" | while read -r branch; do
            echo "  🚨 $branch"

            # Show commit count
            local commit_count
            commit_count=$(git rev-list --count "$MAIN_BRANCH..$branch" 2>/dev/null || echo "0")
            echo "     Commits ahead of $MAIN_BRANCH: $commit_count"
        done
    else
        echo ""
        log_success "No active hotfix branches"
    fi

    # Latest production tag
    local latest_tag
    latest_tag=$(git describe --tags --abbrev=0 "$MAIN_BRANCH" 2>/dev/null || echo "none")
    echo ""
    echo "Latest production tag: $latest_tag"

    # Check for uncommitted changes
    if ! git diff-index --quiet HEAD --; then
        echo ""
        log_warning "Uncommitted changes detected!"
    fi

    echo ""

    return 0
}

# Parse arguments
POSITIONAL_ARGS=()
while [[ $# -gt 0 ]]; do
    case $1 in
        --main)
            MAIN_BRANCH="$2"
            shift 2
            ;;
        --develop)
            DEVELOP_BRANCH="$2"
            shift 2
            ;;
        --remote)
            REMOTE="$2"
            shift 2
            ;;
        --auto-version)
            AUTO_VERSION=true
            shift
            ;;
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        -h|--help)
            show_help
            ;;
        create|finalize|status)
            COMMAND="$1"
            shift
            ;;
        -*)
            log_error "Unknown option: $1"
            exit 1
            ;;
        *)
            POSITIONAL_ARGS+=("$1")
            shift
            ;;
    esac
done

# Get version from positional args if provided
if [ ${#POSITIONAL_ARGS[@]} -gt 0 ]; then
    VERSION="${POSITIONAL_ARGS[0]}"
fi

# Validate command
if [ -z "$COMMAND" ]; then
    log_error "Command required: create, finalize, or status"
    echo "Use --help for usage information"
    exit 1
fi

# Check if in git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    log_error "Not a git repository"
    exit 2
fi

# Execute command
case "$COMMAND" in
    create)
        create_hotfix
        ;;
    finalize)
        finalize_hotfix
        ;;
    status)
        show_status
        ;;
    *)
        log_error "Unknown command: $COMMAND"
        exit 1
        ;;
esac

exit $?
