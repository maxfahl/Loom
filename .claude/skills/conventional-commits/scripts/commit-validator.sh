#!/usr/bin/env bash

################################################################################
# Conventional Commits Validator
#
# Purpose:
#   Validates commit messages against the Conventional Commits v1.0.0 specification
#   Can be used as a git hook, in CI/CD pipelines, or standalone validation
#
# Usage:
#   ./commit-validator.sh [OPTIONS] [COMMIT_MESSAGE_FILE|COMMIT_MESSAGE]
#
# Options:
#   -h, --help              Show this help message
#   -f, --file FILE         Validate commit message from file (default: stdin)
#   -m, --message MSG       Validate commit message string directly
#   -r, --range RANGE       Validate commit range (e.g., HEAD~5..HEAD)
#   -v, --verbose           Show detailed validation information
#   -s, --strict            Enable strict mode (enforce body for breaking changes)
#   --allowed-types TYPES   Comma-separated list of allowed types (default: feat,fix,refactor,perf,style,test,docs,build,ops,chore)
#   --max-length N          Maximum length for description (default: 100)
#   --require-scope         Require scope for all commits
#   --color                 Enable colored output (auto-detected for TTY)
#   --no-color              Disable colored output
#
# Examples:
#   # Validate from git commit-msg hook
#   ./commit-validator.sh -f .git/COMMIT_EDITMSG
#
#   # Validate a string directly
#   ./commit-validator.sh -m "feat(api): add user authentication"
#
#   # Validate last 5 commits
#   ./commit-validator.sh -r HEAD~5..HEAD
#
#   # Strict mode with custom types
#   ./commit-validator.sh --strict --allowed-types "feat,fix,docs" -m "feat: add feature"
#
# Exit Codes:
#   0 - Validation successful
#   1 - Validation failed
#   2 - Invalid arguments or configuration error
################################################################################

set -euo pipefail

# Default configuration
ALLOWED_TYPES="feat,fix,refactor,perf,style,test,docs,build,ops,chore,revert"
MAX_DESCRIPTION_LENGTH=100
VERBOSE=false
STRICT_MODE=false
REQUIRE_SCOPE=false
COLOR_OUTPUT=""

# Color codes
if [ -t 1 ]; then
    COLOR_OUTPUT="auto"
fi

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Helper function to print colored output
print_color() {
    local color=$1
    shift
    if [ "$COLOR_OUTPUT" = "auto" ] || [ "$COLOR_OUTPUT" = "always" ]; then
        echo -e "${color}$*${NC}"
    else
        echo "$*"
    fi
}

print_error() {
    print_color "$RED" "ERROR: $*" >&2
}

print_success() {
    print_color "$GREEN" "SUCCESS: $*"
}

print_warning() {
    print_color "$YELLOW" "WARNING: $*"
}

print_info() {
    print_color "$BLUE" "INFO: $*"
}

show_help() {
    sed -n '/^# Purpose:/,/^################################################################################$/p' "$0" | sed 's/^# //; s/^#//'
}

# Validate a single commit message
validate_commit_message() {
    local message="$1"
    local errors=()
    local warnings=()

    # Split message into lines
    local first_line
    first_line=$(echo "$message" | head -n1)

    if [ "$VERBOSE" = true ]; then
        print_info "Validating: $first_line"
    fi

    # Remove any leading/trailing whitespace from first line
    first_line=$(echo "$first_line" | sed 's/^[[:space:]]*//; s/[[:space:]]*$//')

    # Check for empty message
    if [ -z "$first_line" ]; then
        errors+=("Commit message is empty")
        print_validation_result "$first_line" "${errors[@]}" "${warnings[@]}"
        return 1
    fi

    # Check for merge commits (allow them to pass)
    if [[ "$first_line" =~ ^Merge\ (branch|pull\ request|remote-tracking\ branch) ]]; then
        if [ "$VERBOSE" = true ]; then
            print_info "Merge commit detected, skipping validation"
        fi
        return 0
    fi

    # Check for revert commits (allow default format)
    if [[ "$first_line" =~ ^Revert\ \".*\" ]]; then
        if [ "$VERBOSE" = true ]; then
            print_info "Revert commit detected, skipping validation"
        fi
        return 0
    fi

    # Extract components using regex
    # Pattern: type(scope)!: description
    local type_pattern
    type_pattern="^($(echo "$ALLOWED_TYPES" | sed 's/,/|/g'))"
    local scope_pattern="\(([a-z0-9-]+)\)?"
    local breaking_pattern="!?"
    local separator_pattern=": "
    local description_pattern="(.+)$"

    local full_pattern="${type_pattern}${scope_pattern}${breaking_pattern}${separator_pattern}${description_pattern}"

    if [[ ! "$first_line" =~ $full_pattern ]]; then
        errors+=("Does not match Conventional Commits format: <type>[scope][!]: <description>")
        errors+=("Allowed types: $ALLOWED_TYPES")
        print_validation_result "$first_line" "${errors[@]}" "${warnings[@]}"
        return 1
    fi

    # Extract type
    local type
    type=$(echo "$first_line" | grep -oE "^[a-z]+")

    # Check if type is allowed
    if [[ ! ",$ALLOWED_TYPES," =~ ,$type, ]]; then
        errors+=("Invalid type '$type'. Allowed types: $ALLOWED_TYPES")
    fi

    # Extract scope (if present)
    local scope=""
    if [[ "$first_line" =~ \(([a-z0-9-]+)\) ]]; then
        scope="${BASH_REMATCH[1]}"
    fi

    # Check if scope is required
    if [ "$REQUIRE_SCOPE" = true ] && [ -z "$scope" ]; then
        errors+=("Scope is required but missing")
    fi

    # Extract breaking change indicator
    local has_breaking_indicator=false
    if [[ "$first_line" =~ ! ]]; then
        has_breaking_indicator=true
    fi

    # Extract description
    local description
    description=$(echo "$first_line" | sed -E 's/^[a-z]+(\([a-z0-9-]+\))?!?: //')

    # Check description format
    # Should not be capitalized
    if [[ "$description" =~ ^[A-Z] ]]; then
        errors+=("Description should not start with a capital letter")
    fi

    # Should not end with period
    if [[ "$description" =~ \.$ ]]; then
        errors+=("Description should not end with a period")
    fi

    # Check description length
    if [ ${#description} -gt "$MAX_DESCRIPTION_LENGTH" ]; then
        warnings+=("Description exceeds recommended length of $MAX_DESCRIPTION_LENGTH characters (current: ${#description})")
    fi

    # Check for imperative mood (basic heuristics)
    if [[ "$description" =~ ^(added|fixed|updated|changed|removed|deleted) ]]; then
        warnings+=("Use imperative mood: 'add' not 'added', 'fix' not 'fixed'")
    fi

    # Check for breaking changes
    local has_breaking_footer=false
    if echo "$message" | grep -qE '^BREAKING[- ]CHANGE:'; then
        has_breaking_footer=true
    fi

    # Validate breaking change consistency
    if [ "$has_breaking_indicator" = true ] && [ "$has_breaking_footer" = false ] && [ "$STRICT_MODE" = true ]; then
        warnings+=("Breaking change indicator (!) present but no BREAKING CHANGE footer found")
    fi

    # Check body format (if present)
    local line_count
    line_count=$(echo "$message" | wc -l)
    if [ "$line_count" -gt 1 ]; then
        local second_line
        second_line=$(echo "$message" | sed -n '2p')
        if [ -n "$second_line" ]; then
            errors+=("Second line must be blank (found: '$second_line')")
        fi
    fi

    # Print results
    print_validation_result "$first_line" "${errors[@]}" "${warnings[@]}"

    # Return error if any errors found
    if [ ${#errors[@]} -gt 0 ]; then
        return 1
    fi

    return 0
}

print_validation_result() {
    local commit_msg="$1"
    shift

    local errors=()
    local warnings=()

    # Separate errors and warnings
    while [ $# -gt 0 ]; do
        if [[ "$1" =~ ^ERROR: ]]; then
            errors+=("$1")
        else
            # Check if this is a warning or error based on remaining args
            local is_warning=false
            for arg in "$@"; do
                if [[ "$arg" =~ ^WARNING: ]]; then
                    is_warning=true
                    break
                fi
            done

            if [ -z "${errors[*]}" ] && [ "$is_warning" = true ]; then
                warnings+=("$1")
            else
                errors+=("$1")
            fi
        fi
        shift
    done

    if [ ${#errors[@]} -eq 0 ]; then
        print_success "Valid commit message"
        if [ "$VERBOSE" = true ] && [ ${#warnings[@]} -gt 0 ]; then
            for warning in "${warnings[@]}"; do
                print_warning "$warning"
            done
        fi
    else
        print_error "Invalid commit message:"
        echo "  $commit_msg"
        echo ""
        for error in "${errors[@]}"; do
            print_error "  - $error"
        done
        if [ ${#warnings[@]} -gt 0 ]; then
            echo ""
            for warning in "${warnings[@]}"; do
                print_warning "  - $warning"
            done
        fi
    fi
}

# Validate commit range
validate_commit_range() {
    local range="$1"
    local failed=0

    print_info "Validating commits in range: $range"
    echo ""

    # Get commit SHAs in range
    local commits
    commits=$(git rev-list "$range" 2>/dev/null) || {
        print_error "Invalid commit range: $range"
        return 2
    }

    # Validate each commit
    while IFS= read -r sha; do
        local message
        message=$(git log -1 --format=%B "$sha")
        local short_sha
        short_sha=$(git log -1 --format=%h "$sha")

        echo "[$short_sha]"
        if ! validate_commit_message "$message"; then
            failed=$((failed + 1))
        fi
        echo ""
    done <<< "$commits"

    if [ $failed -eq 0 ]; then
        print_success "All commits are valid!"
        return 0
    else
        print_error "$failed commit(s) failed validation"
        return 1
    fi
}

# Main
main() {
    local commit_message=""
    local commit_file=""
    local commit_range=""

    # Parse arguments
    while [ $# -gt 0 ]; do
        case "$1" in
            -h|--help)
                show_help
                exit 0
                ;;
            -f|--file)
                commit_file="$2"
                shift 2
                ;;
            -m|--message)
                commit_message="$2"
                shift 2
                ;;
            -r|--range)
                commit_range="$2"
                shift 2
                ;;
            -v|--verbose)
                VERBOSE=true
                shift
                ;;
            -s|--strict)
                STRICT_MODE=true
                shift
                ;;
            --allowed-types)
                ALLOWED_TYPES="$2"
                shift 2
                ;;
            --max-length)
                MAX_DESCRIPTION_LENGTH="$2"
                shift 2
                ;;
            --require-scope)
                REQUIRE_SCOPE=true
                shift
                ;;
            --color)
                COLOR_OUTPUT="always"
                shift
                ;;
            --no-color)
                COLOR_OUTPUT="never"
                shift
                ;;
            *)
                # Assume it's a file or message
                if [ -f "$1" ]; then
                    commit_file="$1"
                elif [ -z "$commit_message" ]; then
                    commit_message="$1"
                else
                    print_error "Unknown argument: $1"
                    echo "Use --help for usage information"
                    exit 2
                fi
                shift
                ;;
        esac
    done

    # Determine input source
    if [ -n "$commit_range" ]; then
        validate_commit_range "$commit_range"
        exit $?
    elif [ -n "$commit_file" ]; then
        if [ ! -f "$commit_file" ]; then
            print_error "File not found: $commit_file"
            exit 2
        fi
        commit_message=$(cat "$commit_file")
    elif [ -z "$commit_message" ]; then
        # Read from stdin
        commit_message=$(cat)
    fi

    # Validate
    validate_commit_message "$commit_message"
    exit $?
}

main "$@"
