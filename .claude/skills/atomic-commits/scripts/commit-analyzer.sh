#!/usr/bin/env bash

################################################################################
# commit-analyzer.sh
#
# PURPOSE:
#   Analyzes staged Git changes to validate they form one logical, atomic unit.
#   Prevents non-atomic commits before they happen.
#
# USAGE:
#   ./commit-analyzer.sh [options]
#
# OPTIONS:
#   --strict          Exit with error code if violations found (for CI/CD)
#   --auto-fix        Attempt to auto-fix issues (format, remove debug code)
#   --verbose         Show detailed analysis
#   --help            Show this help message
#
# EXAMPLES:
#   ./commit-analyzer.sh                    # Analyze and warn
#   ./commit-analyzer.sh --strict           # Block commit if non-atomic
#   ./commit-analyzer.sh --verbose          # Show detailed breakdown
#
# ENVIRONMENT VARIABLES:
#   ATOMIC_MAX_FILES=20        Maximum files per commit (default: 20)
#   ATOMIC_MAX_LINES=500       Maximum lines changed (default: 500)
#   ATOMIC_ALLOW_MIXED=false   Allow mixed change types (default: false)
#
# EXIT CODES:
#   0 - Staged changes are atomic
#   1 - Violations found (use --strict to enforce)
#   2 - No staged changes
#   3 - Invalid options
################################################################################

set -euo pipefail

# Colors for output
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default configuration
STRICT_MODE=false
AUTO_FIX=false
VERBOSE=false
MAX_FILES="${ATOMIC_MAX_FILES:-20}"
MAX_LINES="${ATOMIC_MAX_LINES:-500}"
ALLOW_MIXED="${ATOMIC_ALLOW_MIXED:-false}"

# Counters
VIOLATIONS=0
WARNINGS=0

################################################################################
# Helper Functions
################################################################################

print_header() {
    echo -e "${BLUE}╔════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║${NC}          Atomic Commit Analyzer                              ${BLUE}║${NC}"
    echo -e "${BLUE}╚════════════════════════════════════════════════════════════════╝${NC}"
}

print_usage() {
    grep "^#" "$0" | grep -v "^#!/" | sed 's/^# //' | sed 's/^#//'
}

log_info() {
    echo -e "${BLUE}ℹ${NC}  $1"
}

log_success() {
    echo -e "${GREEN}✓${NC}  $1"
}

log_warning() {
    ((WARNINGS++))
    echo -e "${YELLOW}⚠${NC}  $1"
}

log_error() {
    ((VIOLATIONS++))
    echo -e "${RED}✗${NC}  $1"
}

################################################################################
# Analysis Functions
################################################################################

check_staged_changes() {
    if ! git diff --cached --quiet; then
        return 0
    else
        echo -e "${YELLOW}No staged changes found.${NC}"
        echo "Use 'git add <files>' to stage changes before committing."
        exit 2
    fi
}

analyze_file_count() {
    local file_count
    file_count=$(git diff --cached --name-only | wc -l | tr -d ' ')

    log_info "Files changed: $file_count"

    if [[ $file_count -gt $MAX_FILES ]]; then
        log_error "Too many files ($file_count > $MAX_FILES). Consider splitting into smaller commits."
        return 1
    elif [[ $file_count -gt $((MAX_FILES / 2)) ]]; then
        log_warning "Large number of files ($file_count). Verify they're all related."
    else
        log_success "File count is reasonable ($file_count files)"
    fi

    return 0
}

analyze_line_count() {
    local lines_added lines_deleted total_lines

    lines_added=$(git diff --cached --numstat | awk '{sum+=$1} END {print sum+0}')
    lines_deleted=$(git diff --cached --numstat | awk '{sum+=$2} END {print sum+0}')
    total_lines=$((lines_added + lines_deleted))

    log_info "Lines changed: +$lines_added -$lines_deleted (total: $total_lines)"

    if [[ $total_lines -gt $MAX_LINES ]]; then
        log_error "Too many lines changed ($total_lines > $MAX_LINES). Consider splitting."
        return 1
    elif [[ $total_lines -gt $((MAX_LINES / 2)) ]]; then
        log_warning "Large changeset ($total_lines lines). Ensure it's one logical change."
    else
        log_success "Line count is reasonable ($total_lines lines)"
    fi

    return 0
}

classify_file_type() {
    local file=$1

    case "$file" in
        *.ts|*.tsx|*.js|*.jsx|*.py|*.go|*.rs|*.java|*.c|*.cpp|*.h)
            echo "source"
            ;;
        *.test.ts|*.test.tsx|*.test.js|*.spec.ts|*.spec.js|*_test.go|*_test.py)
            echo "test"
            ;;
        *.md|*.txt|*.adoc|docs/*)
            echo "docs"
            ;;
        *.json|*.yaml|*.yml|*.toml|*.ini|*.env*|Dockerfile|docker-compose.yml)
            echo "config"
            ;;
        *.css|*.scss|*.sass|*.less)
            echo "style"
            ;;
        *.sql|migrations/*)
            echo "migration"
            ;;
        package.json|package-lock.json|Cargo.toml|Cargo.lock|go.mod|go.sum|requirements.txt|poetry.lock)
            echo "dependency"
            ;;
        *)
            echo "other"
            ;;
    esac
}

analyze_file_types() {
    local -A type_counts
    local files

    files=$(git diff --cached --name-only)

    while IFS= read -r file; do
        local type
        type=$(classify_file_type "$file")
        ((type_counts[$type]++)) || type_counts[$type]=1
    done <<< "$files"

    log_info "File type distribution:"
    for type in "${!type_counts[@]}"; do
        echo "    - $type: ${type_counts[$type]}"
    done

    # Check for mixed concerns
    local type_count=${#type_counts[@]}
    if [[ $type_count -gt 3 ]] && [[ "$ALLOW_MIXED" == "false" ]]; then
        log_error "Too many file types ($type_count). This suggests mixed concerns."
        echo "    Consider separating: source, tests, docs, config into different commits."
        return 1
    elif [[ $type_count -eq 3 ]]; then
        # Common valid pattern: source + test + docs
        if [[ -n "${type_counts[source]}" && -n "${type_counts[test]}" && -n "${type_counts[docs]}" ]]; then
            log_success "Valid pattern: source + tests + docs"
        else
            log_warning "Multiple file types detected. Verify they're related."
        fi
    else
        log_success "File types are focused"
    fi

    return 0
}

detect_debug_code() {
    local debug_patterns=(
        "console\.log"
        "console\.debug"
        "debugger;"
        "print\("
        "println!"
        "fmt\.Println"
        "TODO:"
        "FIXME:"
        "XXX:"
    )

    local found_debug=false

    for pattern in "${debug_patterns[@]}"; do
        if git diff --cached | grep -E "^\+.*$pattern" > /dev/null 2>&1; then
            if [[ "$found_debug" == "false" ]]; then
                log_error "Debug code detected in staged changes:"
                found_debug=true
            fi
            echo "    - Found: $pattern"
        fi
    done

    if [[ "$found_debug" == "true" ]]; then
        echo "    Remove debug statements before committing."
        return 1
    else
        log_success "No debug code detected"
    fi

    return 0
}

detect_secrets() {
    local secret_patterns=(
        "api[_-]?key"
        "password\s*="
        "secret\s*="
        "token\s*="
        "aws[_-]?secret"
        "private[_-]?key"
        "-----BEGIN.*PRIVATE KEY-----"
    )

    local found_secret=false

    for pattern in "${secret_patterns[@]}"; do
        if git diff --cached | grep -iE "^\+.*$pattern" > /dev/null 2>&1; then
            if [[ "$found_secret" == "false" ]]; then
                log_error "Potential secrets detected in staged changes:"
                found_secret=true
            fi
            echo "    - Potential secret pattern: $pattern"
        fi
    done

    if [[ "$found_secret" == "true" ]]; then
        echo "    Review carefully! Never commit secrets."
        return 1
    else
        log_success "No obvious secrets detected"
    fi

    return 0
}

analyze_change_types() {
    local diff_output
    diff_output=$(git diff --cached)

    local has_additions=false
    local has_deletions=false
    local has_modifications=false

    if echo "$diff_output" | grep -E "^new file mode" > /dev/null; then
        has_additions=true
    fi

    if echo "$diff_output" | grep -E "^deleted file mode" > /dev/null; then
        has_deletions=true
    fi

    if echo "$diff_output" | grep -E "^\+.*[a-zA-Z]" > /dev/null; then
        has_modifications=true
    fi

    local change_count=0
    [[ "$has_additions" == "true" ]] && ((change_count++))
    [[ "$has_deletions" == "true" ]] && ((change_count++))
    [[ "$has_modifications" == "true" ]] && ((change_count++))

    if [[ $change_count -gt 1 ]]; then
        log_warning "Multiple change types detected (additions, deletions, modifications)."
        echo "    Ensure all changes serve one logical purpose."
    else
        log_success "Focused change type"
    fi
}

suggest_split_strategy() {
    if [[ $VIOLATIONS -eq 0 ]]; then
        return 0
    fi

    echo ""
    echo -e "${BLUE}📋 Suggested Split Strategy:${NC}"
    echo ""
    echo "1. Reset staged changes: git reset HEAD"
    echo "2. Stage related files by category:"
    echo "   - Tests with their implementation: git add src/feature.ts tests/feature.test.ts"
    echo "   - Docs separately: git add README.md docs/"
    echo "   - Config separately: git add config/ package.json"
    echo "3. Use interactive staging for mixed files: git add -p file.ts"
    echo "4. Commit each logical unit separately"
    echo ""
    echo "Or use the automation script:"
    echo "  ./commit-splitter.py --interactive"
}

################################################################################
# Main Analysis
################################################################################

main() {
    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --strict)
                STRICT_MODE=true
                shift
                ;;
            --auto-fix)
                AUTO_FIX=true
                shift
                ;;
            --verbose)
                VERBOSE=true
                shift
                ;;
            --help)
                print_usage
                exit 0
                ;;
            *)
                echo -e "${RED}Error: Unknown option $1${NC}"
                print_usage
                exit 3
                ;;
        esac
    done

    print_header
    check_staged_changes

    echo ""
    echo -e "${BLUE}Running atomic commit analysis...${NC}"
    echo ""

    # Run all checks
    analyze_file_count || true
    analyze_line_count || true
    analyze_file_types || true
    detect_debug_code || true
    detect_secrets || true
    analyze_change_types || true

    # Print summary
    echo ""
    echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"

    if [[ $VIOLATIONS -eq 0 ]] && [[ $WARNINGS -eq 0 ]]; then
        echo -e "${GREEN}✓ All checks passed! Staged changes appear atomic.${NC}"
        echo ""
        exit 0
    elif [[ $VIOLATIONS -eq 0 ]]; then
        echo -e "${YELLOW}⚠ $WARNINGS warning(s) found. Review before committing.${NC}"
        echo ""
        exit 0
    else
        echo -e "${RED}✗ $VIOLATIONS violation(s) and $WARNINGS warning(s) found.${NC}"
        suggest_split_strategy

        if [[ "$STRICT_MODE" == "true" ]]; then
            echo -e "${RED}Commit blocked in strict mode.${NC}"
            exit 1
        else
            echo -e "${YELLOW}Consider fixing violations before committing.${NC}"
            echo ""
            exit 0
        fi
    fi
}

main "$@"
