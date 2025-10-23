#!/usr/bin/env bash

################################################################################
# pre-commit-hook.sh
#
# PURPOSE:
#   Git pre-commit hook that enforces atomic commit rules automatically.
#   Install this in .git/hooks/pre-commit to prevent non-atomic commits.
#
# INSTALLATION:
#   cp pre-commit-hook.sh .git/hooks/pre-commit
#   chmod +x .git/hooks/pre-commit
#
#   OR use symlink to auto-update:
#   ln -sf ../../.devdev/skills/atomic-commits/scripts/pre-commit-hook.sh .git/hooks/pre-commit
#
# CONFIGURATION:
#   Create .atomic-commit.config in repo root:
#
#   # .atomic-commit.config
#   ATOMIC_ENFORCE=true           # Block non-atomic commits
#   ATOMIC_MAX_FILES=20           # Max files per commit
#   ATOMIC_MAX_LINES=500          # Max lines per commit
#   ATOMIC_CHECK_DEBUG=true       # Check for debug code
#   ATOMIC_CHECK_SECRETS=true     # Check for secrets
#   ATOMIC_AUTO_FORMAT=false      # Auto-format before commit
#
# BYPASS:
#   To bypass this hook for emergency commits:
#   git commit --no-verify -m "emergency fix"
#
# EXIT CODES:
#   0 - All checks passed, commit allowed
#   1 - Violations found, commit blocked
################################################################################

set -euo pipefail

# Colors
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

# Default configuration
ATOMIC_ENFORCE="${ATOMIC_ENFORCE:-true}"
ATOMIC_MAX_FILES="${ATOMIC_MAX_FILES:-20}"
ATOMIC_MAX_LINES="${ATOMIC_MAX_LINES:-500}"
ATOMIC_CHECK_DEBUG="${ATOMIC_CHECK_DEBUG:-true}"
ATOMIC_CHECK_SECRETS="${ATOMIC_CHECK_SECRETS:-true}"
ATOMIC_AUTO_FORMAT="${ATOMIC_AUTO_FORMAT:-false}"
ATOMIC_CHECK_MESSAGE="${ATOMIC_CHECK_MESSAGE:-true}"

# Load config file if exists
CONFIG_FILE=".atomic-commit.config"
if [[ -f "$CONFIG_FILE" ]]; then
    # shellcheck disable=SC1090
    source "$CONFIG_FILE"
fi

# Counters
VIOLATIONS=0
WARNINGS=0

################################################################################
# Helper Functions
################################################################################

log_info() {
    echo -e "${BLUE}[pre-commit]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[pre-commit]${NC} ✓ $1"
}

log_warning() {
    ((WARNINGS++))
    echo -e "${YELLOW}[pre-commit]${NC} ⚠ $1"
}

log_error() {
    ((VIOLATIONS++))
    echo -e "${RED}[pre-commit]${NC} ✗ $1"
}

################################################################################
# Check Functions
################################################################################

check_file_count() {
    local file_count
    file_count=$(git diff --cached --name-only | wc -l | tr -d ' ')

    if [[ $file_count -gt $ATOMIC_MAX_FILES ]]; then
        log_error "Too many files: $file_count > $ATOMIC_MAX_FILES"
        echo "  Consider splitting into smaller commits."
        return 1
    fi

    return 0
}

check_line_count() {
    local lines_added lines_deleted total_lines

    lines_added=$(git diff --cached --numstat | awk '{sum+=$1} END {print sum+0}')
    lines_deleted=$(git diff --cached --numstat | awk '{sum+=$2} END {print sum+0}')
    total_lines=$((lines_added + lines_deleted))

    if [[ $total_lines -gt $ATOMIC_MAX_LINES ]]; then
        log_error "Too many lines changed: $total_lines > $ATOMIC_MAX_LINES"
        echo "  Consider splitting into smaller commits."
        return 1
    fi

    return 0
}

check_debug_code() {
    if [[ "$ATOMIC_CHECK_DEBUG" != "true" ]]; then
        return 0
    fi

    local patterns=(
        "console\.log"
        "console\.debug"
        "console\.error"
        "debugger;"
        "print\("
        "println!"
        "fmt\.Println"
        "pdb\.set_trace"
    )

    local found=false

    for pattern in "${patterns[@]}"; do
        if git diff --cached | grep -E "^\+.*$pattern" > /dev/null 2>&1; then
            if [[ "$found" == "false" ]]; then
                log_error "Debug code detected:"
                found=true
            fi
            echo "  - $pattern"
        fi
    done

    [[ "$found" == "false" ]] && return 0 || return 1
}

check_secrets() {
    if [[ "$ATOMIC_CHECK_SECRETS" != "true" ]]; then
        return 0
    fi

    local patterns=(
        "api[_-]?key"
        "password\s*="
        "secret\s*="
        "token\s*="
        "aws[_-]?secret"
        "private[_-]?key"
    )

    local found=false

    for pattern in "${patterns[@]}"; do
        if git diff --cached | grep -iE "^\+.*$pattern" > /dev/null 2>&1; then
            if [[ "$found" == "false" ]]; then
                log_error "Potential secrets detected:"
                found=true
            fi
            echo "  - $pattern"
        fi
    done

    [[ "$found" == "false" ]] && return 0 || return 1
}

check_large_files() {
    local max_size=5242880  # 5MB in bytes
    local files

    files=$(git diff --cached --name-only)

    while IFS= read -r file; do
        if [[ -f "$file" ]]; then
            local size
            size=$(wc -c < "$file")

            if [[ $size -gt $max_size ]]; then
                log_error "Large file detected: $file ($(numfmt --to=iec-i --suffix=B $size))"
                echo "  Consider using Git LFS for large files."
                return 1
            fi
        fi
    done <<< "$files"

    return 0
}

check_commit_message_format() {
    if [[ "$ATOMIC_CHECK_MESSAGE" != "true" ]]; then
        return 0
    fi

    # This runs after commit message is written
    # For pre-commit hook, we'll skip this check
    # Use commit-msg hook instead
    return 0
}

auto_format_code() {
    if [[ "$ATOMIC_AUTO_FORMAT" != "true" ]]; then
        return 0
    fi

    log_info "Auto-formatting code..."

    local files
    files=$(git diff --cached --name-only --diff-filter=ACM)

    # Try to detect and use project formatters
    if [[ -f "package.json" ]]; then
        # Node project - try prettier
        if command -v prettier > /dev/null 2>&1; then
            echo "$files" | grep -E '\.(ts|tsx|js|jsx|json|md)$' | xargs -r prettier --write
            echo "$files" | grep -E '\.(ts|tsx|js|jsx|json|md)$' | xargs -r git add
        fi
    fi

    if [[ -f "Cargo.toml" ]]; then
        # Rust project
        if command -v rustfmt > /dev/null 2>&1; then
            echo "$files" | grep -E '\.rs$' | xargs -r rustfmt
            echo "$files" | grep -E '\.rs$' | xargs -r git add
        fi
    fi

    if [[ -f "go.mod" ]]; then
        # Go project
        if command -v gofmt > /dev/null 2>&1; then
            echo "$files" | grep -E '\.go$' | xargs -r gofmt -w
            echo "$files" | grep -E '\.go$' | xargs -r git add
        fi
    fi

    return 0
}

################################################################################
# Main
################################################################################

main() {
    log_info "Running atomic commit checks..."

    # Run auto-format first if enabled
    auto_format_code || true

    # Run all checks
    check_file_count || true
    check_line_count || true
    check_debug_code || true
    check_secrets || true
    check_large_files || true

    # Print summary
    echo ""

    if [[ $VIOLATIONS -eq 0 ]] && [[ $WARNINGS -eq 0 ]]; then
        log_success "All pre-commit checks passed!"
        exit 0
    elif [[ $VIOLATIONS -eq 0 ]]; then
        log_warning "$WARNINGS warning(s) found, but allowing commit."
        exit 0
    else
        echo -e "${RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
        log_error "$VIOLATIONS violation(s) found!"
        echo ""

        if [[ "$ATOMIC_ENFORCE" == "true" ]]; then
            echo "Commit blocked. Fix violations before committing."
            echo ""
            echo "To bypass this hook (not recommended):"
            echo "  git commit --no-verify -m \"your message\""
            echo ""
            exit 1
        else
            echo "Violations detected but ATOMIC_ENFORCE=false"
            echo "Allowing commit to proceed."
            echo ""
            exit 0
        fi
    fi
}

main "$@"
