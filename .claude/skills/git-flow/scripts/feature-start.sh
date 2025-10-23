#!/usr/bin/env bash
#
# feature-start.sh - Create feature branches with Git Flow conventions
#
# Purpose:
#   Streamlines feature branch creation with proper naming, tracking,
#   and automatic syncing with develop branch.
#
# Usage:
#   ./feature-start.sh [options] <feature-name>
#
# Options:
#   -d, --develop <branch>    Develop branch name (default: develop)
#   -r, --remote <name>       Remote name (default: origin)
#   -j, --jira <ticket>       JIRA ticket number to prepend
#   -p, --prefix <prefix>     Custom prefix (default: feature/)
#   --no-push                 Don't push to remote
#   --dry-run                 Show what would be done
#   -h, --help                Show this help
#
# Examples:
#   ./feature-start.sh user-authentication
#   ./feature-start.sh --jira PROJ-123 oauth2-integration
#   ./feature-start.sh --no-push dashboard-redesign
#   ./feature-start.sh --prefix spike/ performance-analysis
#
# Environment Variables:
#   GIT_FLOW_DEVELOP    Override develop branch name
#   JIRA_PROJECT        Default JIRA project prefix
#
# Exit Codes:
#   0 - Success
#   1 - Invalid arguments or validation failed
#   2 - Git errors
#

set -euo pipefail

# Configuration
DEVELOP_BRANCH="${GIT_FLOW_DEVELOP:-develop}"
REMOTE="origin"
PREFIX="feature/"
JIRA_TICKET=""
FEATURE_NAME=""
PUSH_TO_REMOTE=true
DRY_RUN=false

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
log_warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

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

# Validate feature name
validate_feature_name() {
    local name="$1"

    # Check if empty
    if [ -z "$name" ]; then
        log_error "Feature name cannot be empty"
        return 1
    fi

    # Check for invalid characters
    if [[ ! "$name" =~ ^[a-z0-9-]+$ ]]; then
        log_error "Feature name must contain only lowercase letters, numbers, and hyphens"
        log_error "Got: $name"
        return 1
    fi

    # Check for consecutive hyphens
    if [[ "$name" =~ -- ]]; then
        log_warning "Feature name contains consecutive hyphens"
    fi

    # Check for leading/trailing hyphens
    if [[ "$name" =~ ^- ]] || [[ "$name" =~ -$ ]]; then
        log_error "Feature name cannot start or end with a hyphen"
        return 1
    fi

    # Suggest better naming
    if [ ${#name} -lt 5 ]; then
        log_warning "Feature name is quite short. Consider a more descriptive name."
    fi

    return 0
}

# Parse arguments
POSITIONAL_ARGS=()
while [[ $# -gt 0 ]]; do
    case $1 in
        -d|--develop)
            DEVELOP_BRANCH="$2"
            shift 2
            ;;
        -r|--remote)
            REMOTE="$2"
            shift 2
            ;;
        -j|--jira)
            JIRA_TICKET="$2"
            shift 2
            ;;
        -p|--prefix)
            PREFIX="$2"
            shift 2
            ;;
        --no-push)
            PUSH_TO_REMOTE=false
            shift
            ;;
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        -h|--help)
            show_help
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

# Get feature name from positional args
if [ ${#POSITIONAL_ARGS[@]} -eq 0 ]; then
    # Interactive mode
    echo -e "${BLUE}Feature Branch Creator${NC}"
    echo ""
    read -rp "Enter feature description (lowercase, hyphens): " FEATURE_NAME

    if [ -n "${JIRA_PROJECT:-}" ]; then
        read -rp "JIRA ticket number (or press Enter to skip): " JIRA_TICKET
    fi
else
    FEATURE_NAME="${POSITIONAL_ARGS[0]}"
fi

# Validate feature name
if ! validate_feature_name "$FEATURE_NAME"; then
    exit 1
fi

# Build full branch name
if [ -n "$JIRA_TICKET" ]; then
    # Remove any prefix if user included it
    JIRA_TICKET="${JIRA_TICKET#"${JIRA_PROJECT:-}"-}"
    JIRA_TICKET="${JIRA_TICKET#PROJ-}"
    JIRA_TICKET="${JIRA_TICKET#[A-Z]*-}"

    # Add project prefix if available
    if [ -n "${JIRA_PROJECT:-}" ]; then
        BRANCH_NAME="${PREFIX}${JIRA_PROJECT}-${JIRA_TICKET}-${FEATURE_NAME}"
    else
        BRANCH_NAME="${PREFIX}${JIRA_TICKET}-${FEATURE_NAME}"
    fi
else
    BRANCH_NAME="${PREFIX}${FEATURE_NAME}"
fi

log_info "Creating feature branch: $BRANCH_NAME"

# Check if git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    log_error "Not a git repository"
    exit 2
fi

# Check if branch already exists
if git show-ref --verify --quiet "refs/heads/$BRANCH_NAME"; then
    log_error "Branch '$BRANCH_NAME' already exists locally"
    log_error "Use: git checkout $BRANCH_NAME"
    exit 2
fi

# Check if develop branch exists
if ! git show-ref --verify --quiet "refs/heads/$DEVELOP_BRANCH"; then
    log_error "Develop branch '$DEVELOP_BRANCH' does not exist"
    log_error "Run flow-init.sh first or specify correct develop branch with -d"
    exit 2
fi

# Sync with remote develop
if git remote | grep -q "$REMOTE"; then
    log_info "Syncing with remote $DEVELOP_BRANCH..."

    if [ "$DRY_RUN" = false ]; then
        execute git checkout "$DEVELOP_BRANCH"

        # Fetch latest changes
        execute git fetch "$REMOTE" "$DEVELOP_BRANCH"

        # Check if local is behind remote
        LOCAL=$(git rev-parse "$DEVELOP_BRANCH")
        REMOTE_REF=$(git rev-parse "$REMOTE/$DEVELOP_BRANCH")

        if [ "$LOCAL" != "$REMOTE_REF" ]; then
            log_info "Local $DEVELOP_BRANCH is behind remote. Pulling changes..."
            execute git pull "$REMOTE" "$DEVELOP_BRANCH"
        else
            log_success "$DEVELOP_BRANCH is up to date"
        fi
    fi
else
    log_warning "Remote '$REMOTE' not configured. Creating branch from local $DEVELOP_BRANCH"
    execute git checkout "$DEVELOP_BRANCH"
fi

# Create feature branch
log_info "Creating branch: $BRANCH_NAME from $DEVELOP_BRANCH"
execute git checkout -b "$BRANCH_NAME" "$DEVELOP_BRANCH"

# Push to remote if requested
if [ "$PUSH_TO_REMOTE" = true ] && [ "$DRY_RUN" = false ]; then
    if git remote | grep -q "$REMOTE"; then
        log_info "Pushing branch to remote..."
        execute git push -u "$REMOTE" "$BRANCH_NAME"
    fi
fi

# Success message
echo ""
log_success "Feature branch created: $BRANCH_NAME"
echo ""
echo "Next steps:"
echo "  1. Make your changes: git add <files>"
echo "  2. Commit with conventional commits: git commit -m 'feat: description'"
echo "  3. Push changes: git push $REMOTE $BRANCH_NAME"
echo "  4. Create PR: $BRANCH_NAME → $DEVELOP_BRANCH"
echo ""

# Show suggested commit message format
if [ -n "$JIRA_TICKET" ]; then
    echo "Suggested commit format:"
    echo "  feat: implement feature description"
    echo ""
    echo "  Detailed explanation..."
    echo ""
    echo "  Refs: ${JIRA_PROJECT:-PROJ}-${JIRA_TICKET}"
    echo ""
fi

# Create PR template hint
if command -v gh &> /dev/null && [ "$DRY_RUN" = false ]; then
    echo "To create a pull request when ready:"
    echo "  gh pr create --base $DEVELOP_BRANCH --head $BRANCH_NAME --title 'feat: $FEATURE_NAME'"
    echo ""
fi

exit 0
