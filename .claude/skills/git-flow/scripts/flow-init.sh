#!/usr/bin/env bash
#
# flow-init.sh - Initialize Git Flow structure in a repository
#
# Purpose:
#   Sets up Git Flow branching model with proper branch structure,
#   protection rules, and configuration. Handles both new and existing repos.
#
# Usage:
#   ./flow-init.sh [options]
#
# Options:
#   --main-branch <name>      Name for main branch (default: main)
#   --develop-branch <name>   Name for develop branch (default: develop)
#   --dry-run                 Show what would be done without executing
#   --force                   Force initialization even if branches exist
#   --skip-protection         Don't set up branch protection rules
#   --remote <name>           Remote name (default: origin)
#   -h, --help                Show this help message
#
# Examples:
#   ./flow-init.sh
#   ./flow-init.sh --main-branch master --develop-branch dev
#   ./flow-init.sh --dry-run
#   ./flow-init.sh --force --skip-protection
#
# Environment Variables:
#   GIT_FLOW_MAIN      Override main branch name
#   GIT_FLOW_DEVELOP   Override develop branch name
#
# Requirements:
#   - git
#   - gh (GitHub CLI) for branch protection (optional)
#
# Exit Codes:
#   0 - Success
#   1 - Invalid arguments or git not found
#   2 - Repository already initialized (use --force to override)
#   3 - Remote repository issues
#

set -euo pipefail

# Default configuration
MAIN_BRANCH="${GIT_FLOW_MAIN:-main}"
DEVELOP_BRANCH="${GIT_FLOW_DEVELOP:-develop}"
REMOTE="origin"
DRY_RUN=false
FORCE=false
SKIP_PROTECTION=false

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Helper functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

show_help() {
    sed -n '/^#/,/^$/p' "$0" | sed 's/^# \?//' | tail -n +2 | head -n -1
    exit 0
}

execute() {
    if [ "$DRY_RUN" = true ]; then
        echo -e "${YELLOW}[DRY-RUN]${NC} $*"
    else
        log_info "Executing: $*"
        "$@"
    fi
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --main-branch)
            MAIN_BRANCH="$2"
            shift 2
            ;;
        --develop-branch)
            DEVELOP_BRANCH="$2"
            shift 2
            ;;
        --remote)
            REMOTE="$2"
            shift 2
            ;;
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        --force)
            FORCE=true
            shift
            ;;
        --skip-protection)
            SKIP_PROTECTION=true
            shift
            ;;
        -h|--help)
            show_help
            ;;
        *)
            log_error "Unknown option: $1"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

# Validate git is installed
if ! command -v git &> /dev/null; then
    log_error "git is not installed. Please install git first."
    exit 1
fi

# Check if we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    log_error "Not a git repository. Run 'git init' first."
    exit 1
fi

log_info "Initializing Git Flow in repository: $(basename "$(git rev-parse --show-toplevel)")"
log_info "Main branch: $MAIN_BRANCH"
log_info "Develop branch: $DEVELOP_BRANCH"
log_info "Remote: $REMOTE"

# Check if already initialized
if git show-ref --verify --quiet "refs/heads/$DEVELOP_BRANCH" && [ "$FORCE" = false ]; then
    log_error "Git Flow appears to be already initialized (develop branch exists)."
    log_error "Use --force to reinitialize."
    exit 2
fi

# Ensure main branch exists
if ! git show-ref --verify --quiet "refs/heads/$MAIN_BRANCH"; then
    log_warning "$MAIN_BRANCH branch doesn't exist. Creating it..."
    execute git checkout -b "$MAIN_BRANCH"

    # Create initial commit if needed
    if ! git rev-parse HEAD &> /dev/null; then
        log_info "Creating initial commit..."
        echo "# $(basename "$(git rev-parse --show-toplevel)")" > README.md
        execute git add README.md
        execute git commit -m "chore: initial commit"
    fi
fi

# Ensure we're on main branch
execute git checkout "$MAIN_BRANCH"

# Create develop branch
if git show-ref --verify --quiet "refs/heads/$DEVELOP_BRANCH"; then
    log_warning "$DEVELOP_BRANCH branch already exists."
else
    log_info "Creating $DEVELOP_BRANCH branch from $MAIN_BRANCH..."
    execute git checkout -b "$DEVELOP_BRANCH" "$MAIN_BRANCH"
fi

# Set up remote tracking
if git remote | grep -q "$REMOTE"; then
    log_info "Setting up remote tracking..."

    # Push main branch
    if [ "$DRY_RUN" = false ]; then
        if git ls-remote --heads "$REMOTE" "$MAIN_BRANCH" | grep -q "$MAIN_BRANCH"; then
            log_warning "Remote $MAIN_BRANCH already exists, skipping push"
        else
            execute git push -u "$REMOTE" "$MAIN_BRANCH"
        fi

        # Push develop branch
        if git ls-remote --heads "$REMOTE" "$DEVELOP_BRANCH" | grep -q "$DEVELOP_BRANCH"; then
            log_warning "Remote $DEVELOP_BRANCH already exists, skipping push"
        else
            execute git push -u "$REMOTE" "$DEVELOP_BRANCH"
        fi
    fi
else
    log_warning "Remote '$REMOTE' not found. Skipping remote setup."
    log_warning "Add remote with: git remote add $REMOTE <url>"
fi

# Configure git-flow extension if available
if command -v git-flow &> /dev/null; then
    log_info "Configuring git-flow extension..."
    execute git config gitflow.branch.master "$MAIN_BRANCH"
    execute git config gitflow.branch.develop "$DEVELOP_BRANCH"
    execute git config gitflow.prefix.feature "feature/"
    execute git config gitflow.prefix.release "release/"
    execute git config gitflow.prefix.hotfix "hotfix/"
    execute git config gitflow.prefix.support "support/"
    execute git config gitflow.prefix.versiontag "v"
else
    log_warning "git-flow extension not found. Install it with:"
    log_warning "  macOS: brew install git-flow"
    log_warning "  Ubuntu/Debian: apt-get install git-flow"
fi

# Set up branch protection (requires GitHub CLI)
if [ "$SKIP_PROTECTION" = false ]; then
    if command -v gh &> /dev/null; then
        log_info "Setting up branch protection rules..."

        # Check if this is a GitHub repository
        if gh repo view &> /dev/null; then
            # Protect main branch
            if [ "$DRY_RUN" = false ]; then
                log_info "Protecting $MAIN_BRANCH branch..."
                gh api "repos/{owner}/{repo}/branches/$MAIN_BRANCH/protection" \
                    -X PUT \
                    -f required_status_checks='{"strict":true,"contexts":[]}' \
                    -f enforce_admins=false \
                    -f required_pull_request_reviews='{"required_approving_review_count":1}' \
                    -f restrictions=null \
                    -f allow_force_pushes=false \
                    -f allow_deletions=false 2>/dev/null || log_warning "Failed to set protection on $MAIN_BRANCH (may need admin permissions)"

                # Protect develop branch (slightly less strict)
                log_info "Protecting $DEVELOP_BRANCH branch..."
                gh api "repos/{owner}/{repo}/branches/$DEVELOP_BRANCH/protection" \
                    -X PUT \
                    -f required_status_checks='{"strict":false,"contexts":[]}' \
                    -f enforce_admins=false \
                    -f required_pull_request_reviews='{"required_approving_review_count":1}' \
                    -f restrictions=null \
                    -f allow_force_pushes=false \
                    -f allow_deletions=false 2>/dev/null || log_warning "Failed to set protection on $DEVELOP_BRANCH (may need admin permissions)"
            fi
        else
            log_warning "Not a GitHub repository. Skipping GitHub-specific protection rules."
        fi
    else
        log_warning "GitHub CLI (gh) not found. Skipping branch protection setup."
        log_warning "Install with: brew install gh (macOS) or https://cli.github.com"
    fi
fi

# Create .gitflow config file
if [ "$DRY_RUN" = false ]; then
    cat > "$(git rev-parse --show-toplevel)/.gitflow" <<EOF
# Git Flow Configuration
# Generated by flow-init.sh on $(date +%Y-%m-%d)

[gitflow "branch"]
    master = $MAIN_BRANCH
    develop = $DEVELOP_BRANCH

[gitflow "prefix"]
    feature = feature/
    release = release/
    hotfix = hotfix/
    support = support/
    versiontag = v

[gitflow "naming"]
    # Feature branch naming: feature/description-with-hyphens
    # Release branch naming: release/X.Y.Z (semantic versioning)
    # Hotfix branch naming: hotfix/X.Y.Z
EOF
    log_success "Created .gitflow configuration file"
fi

# Create BRANCHING.md documentation
if [ "$DRY_RUN" = false ]; then
    cat > "$(git rev-parse --show-toplevel)/BRANCHING.md" <<EOF
# Git Flow Branching Strategy

This repository uses the **Git Flow** branching model.

## Branch Structure

- **$MAIN_BRANCH**: Production-ready code. Protected branch.
- **$DEVELOP_BRANCH**: Integration branch for features. Protected branch.
- **feature/\***: Feature development branches
- **release/\***: Release preparation branches
- **hotfix/\***: Emergency production fixes

## Workflows

### Starting a Feature
\`\`\`bash
git checkout $DEVELOP_BRANCH
git pull $REMOTE $DEVELOP_BRANCH
git checkout -b feature/my-feature $DEVELOP_BRANCH
# Work on feature...
# Create PR: feature/my-feature → $DEVELOP_BRANCH
\`\`\`

### Creating a Release
\`\`\`bash
git checkout -b release/1.2.0 $DEVELOP_BRANCH
# Bump version, fix bugs...
# Merge to $MAIN_BRANCH and $DEVELOP_BRANCH, tag as v1.2.0
\`\`\`

### Creating a Hotfix
\`\`\`bash
git checkout -b hotfix/1.1.1 $MAIN_BRANCH
# Fix critical bug...
# Merge to $MAIN_BRANCH and $DEVELOP_BRANCH, tag as v1.1.1
\`\`\`

## Resources
- [Git Flow Documentation](https://nvie.com/posts/a-successful-git-branching-model/)
- Repository scripts: \`.devdev/skills/git-flow/scripts/\`
EOF
    log_success "Created BRANCHING.md documentation"
fi

# Summary
echo ""
log_success "Git Flow initialization complete!"
echo ""
echo "Branch structure:"
echo "  $MAIN_BRANCH    - Production releases"
echo "  $DEVELOP_BRANCH - Active development"
echo ""
echo "Next steps:"
echo "  1. Create a feature branch: git checkout -b feature/my-feature $DEVELOP_BRANCH"
echo "  2. Read BRANCHING.md for workflow details"
echo "  3. Use helper scripts in .devdev/skills/git-flow/scripts/"
echo ""

if [ "$DRY_RUN" = true ]; then
    log_warning "DRY-RUN mode was enabled. No changes were made."
fi

exit 0
