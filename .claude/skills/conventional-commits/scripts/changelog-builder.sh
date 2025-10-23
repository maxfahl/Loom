#!/usr/bin/env bash

################################################################################
# Conventional Commits Changelog Builder
#
# Purpose:
#   Automatically generate CHANGELOG.md from conventional commits
#   Supports semantic versioning and categorizes changes by type
#
# Usage:
#   ./changelog-builder.sh [OPTIONS]
#
# Options:
#   -h, --help                Show this help message
#   -o, --output FILE         Output file (default: CHANGELOG.md)
#   -r, --range RANGE         Git commit range (default: all commits)
#   -v, --version VERSION     Version to use in changelog (auto-detect if not specified)
#   -t, --tag TAG             Generate changelog for specific tag
#   --since-tag TAG           Generate changelog since specific tag
#   --unreleased              Include unreleased changes section
#   --no-header               Don't include changelog header
#   --group-by TYPE           Group by: type, scope, or date (default: type)
#   --include-all             Include all commit types (default: feat, fix, perf, refactor)
#   --breaking-first          Show breaking changes first
#   --link-commits            Add links to commit hashes (requires --repo-url)
#   --link-issues             Auto-link issue references (requires --repo-url)
#   --repo-url URL            Repository URL for commit/issue links
#   --format FORMAT           Output format: markdown, json, html (default: markdown)
#   --dry-run                 Preview output without writing to file
#   -v, --verbose             Show verbose output
#
# Examples:
#   # Generate full changelog
#   ./changelog-builder.sh
#
#   # Generate changelog for v2.0.0
#   ./changelog-builder.sh -v 2.0.0 --since-tag v1.0.0
#
#   # Generate with commit links
#   ./changelog-builder.sh --repo-url https://github.com/user/repo --link-commits
#
#   # Preview unreleased changes
#   ./changelog-builder.sh --unreleased --dry-run
#
#   # Custom output file with all commits
#   ./changelog-builder.sh -o RELEASE_NOTES.md --include-all
#
# Exit Codes:
#   0 - Success
#   1 - Error generating changelog
#   2 - Invalid arguments
################################################################################

set -euo pipefail

# Default configuration
OUTPUT_FILE="CHANGELOG.md"
COMMIT_RANGE=""
VERSION=""
TAG=""
SINCE_TAG=""
UNRELEASED=false
NO_HEADER=false
GROUP_BY="type"
INCLUDE_ALL=false
BREAKING_FIRST=true
LINK_COMMITS=false
LINK_ISSUES=false
REPO_URL=""
FORMAT="markdown"
DRY_RUN=false
VERBOSE=false

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_error() {
    echo -e "${RED}ERROR: $*${NC}" >&2
}

print_success() {
    echo -e "${GREEN}SUCCESS: $*${NC}"
}

print_info() {
    if [ "$VERBOSE" = true ]; then
        echo -e "${BLUE}INFO: $*${NC}"
    fi
}

show_help() {
    sed -n '/^# Purpose:/,/^################################################################################$/p' "$0" | sed 's/^# //; s/^#//'
}

# Get version from git tags or commits
auto_detect_version() {
    local version

    # Try to get latest tag
    version=$(git describe --tags --abbrev=0 2>/dev/null || echo "")

    if [ -z "$version" ]; then
        # No tags, use 0.1.0
        version="0.1.0"
    fi

    echo "$version"
}

# Parse commit message
parse_commit() {
    local commit_msg="$1"
    local first_line
    first_line=$(echo "$commit_msg" | head -n1)

    # Extract type, scope, breaking, description
    local type=""
    local scope=""
    local breaking=false
    local description=""

    # Check for breaking change indicator
    if [[ "$first_line" =~ ! ]]; then
        breaking=true
    fi

    # Extract type
    if [[ "$first_line" =~ ^([a-z]+) ]]; then
        type="${BASH_REMATCH[1]}"
    fi

    # Extract scope
    if [[ "$first_line" =~ \(([a-z0-9-]+)\) ]]; then
        scope="${BASH_REMATCH[1]}"
    fi

    # Extract description
    description=$(echo "$first_line" | sed -E 's/^[a-z]+(\([a-z0-9-]+\))?!?: //')

    # Check for BREAKING CHANGE in footer
    if echo "$commit_msg" | grep -qE '^BREAKING[- ]CHANGE:'; then
        breaking=true
    fi

    echo "$type|$scope|$breaking|$description"
}

# Generate changelog section for a commit type
generate_type_section() {
    local type="$1"
    local title="$2"
    local commits="$3"

    if [ -z "$commits" ]; then
        return
    fi

    echo ""
    echo "### $title"
    echo ""

    while IFS='|' read -r sha scope breaking description; do
        local line="- "

        if [ -n "$scope" ]; then
            line+="**${scope}**: "
        fi

        line+="$description"

        # Add commit link if enabled
        if [ "$LINK_COMMITS" = true ] && [ -n "$REPO_URL" ]; then
            line+=" ([${sha:0:7}](${REPO_URL}/commit/${sha}))"
        fi

        echo "$line"
    done <<< "$commits"
}

# Generate markdown changelog
generate_markdown_changelog() {
    local version="$1"
    local date
    date=$(date +%Y-%m-%d)

    # Header
    if [ "$NO_HEADER" = false ]; then
        echo "# Changelog"
        echo ""
        echo "All notable changes to this project will be documented in this file."
        echo ""
        echo "The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),"
        echo "and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html)."
        echo ""
    fi

    # Version header
    if [ "$UNRELEASED" = true ]; then
        echo "## [Unreleased]"
    else
        echo "## [$version] - $date"
    fi

    # Get commits in range
    local git_range=""
    if [ -n "$SINCE_TAG" ]; then
        git_range="${SINCE_TAG}..HEAD"
    elif [ -n "$TAG" ]; then
        local prev_tag
        prev_tag=$(git describe --tags --abbrev=0 "${TAG}^" 2>/dev/null || echo "")
        if [ -n "$prev_tag" ]; then
            git_range="${prev_tag}..${TAG}"
        else
            git_range="$TAG"
        fi
    elif [ -n "$COMMIT_RANGE" ]; then
        git_range="$COMMIT_RANGE"
    else
        git_range="HEAD"
    fi

    print_info "Using git range: $git_range"

    # Collect commits by type
    declare -A commits_by_type

    while IFS= read -r sha; do
        local msg
        msg=$(git log -1 --format=%B "$sha")

        # Skip merge commits
        if [[ "$msg" =~ ^Merge ]]; then
            continue
        fi

        # Parse commit
        IFS='|' read -r type scope breaking description <<< "$(parse_commit "$msg")"

        if [ -z "$type" ]; then
            continue
        fi

        # Skip if not in included types (unless include-all)
        if [ "$INCLUDE_ALL" = false ]; then
            if [[ ! "$type" =~ ^(feat|fix|perf|refactor)$ ]]; then
                continue
            fi
        fi

        # Store commit
        local key="$type"
        local value="${sha:0:7}|$scope|$breaking|$description"

        if [ -n "${commits_by_type[$key]:-}" ]; then
            commits_by_type[$key]+=$'\n'"$value"
        else
            commits_by_type[$key]="$value"
        fi

        # Also store in breaking if applicable
        if [ "$breaking" = true ]; then
            key="breaking"
            if [ -n "${commits_by_type[$key]:-}" ]; then
                commits_by_type[$key]+=$'\n'"$value"
            else
                commits_by_type[$key]="$value"
            fi
        fi

    done < <(git rev-list "$git_range" 2>/dev/null || echo "")

    # Generate sections
    if [ "$BREAKING_FIRST" = true ] && [ -n "${commits_by_type[breaking]:-}" ]; then
        generate_type_section "breaking" "⚠ BREAKING CHANGES" "${commits_by_type[breaking]}"
    fi

    # Features
    if [ -n "${commits_by_type[feat]:-}" ]; then
        generate_type_section "feat" "Features" "${commits_by_type[feat]}"
    fi

    # Bug Fixes
    if [ -n "${commits_by_type[fix]:-}" ]; then
        generate_type_section "fix" "Bug Fixes" "${commits_by_type[fix]}"
    fi

    # Performance
    if [ -n "${commits_by_type[perf]:-}" ]; then
        generate_type_section "perf" "Performance Improvements" "${commits_by_type[perf]}"
    fi

    # Refactoring
    if [ -n "${commits_by_type[refactor]:-}" ]; then
        generate_type_section "refactor" "Code Refactoring" "${commits_by_type[refactor]}"
    fi

    # Other types if include-all
    if [ "$INCLUDE_ALL" = true ]; then
        if [ -n "${commits_by_type[docs]:-}" ]; then
            generate_type_section "docs" "Documentation" "${commits_by_type[docs]}"
        fi

        if [ -n "${commits_by_type[style]:-}" ]; then
            generate_type_section "style" "Styles" "${commits_by_type[style]}"
        fi

        if [ -n "${commits_by_type[test]:-}" ]; then
            generate_type_section "test" "Tests" "${commits_by_type[test]}"
        fi

        if [ -n "${commits_by_type[build]:-}" ]; then
            generate_type_section "build" "Build System" "${commits_by_type[build]}"
        fi

        if [ -n "${commits_by_type[ops]:-}" ]; then
            generate_type_section "ops" "Operations" "${commits_by_type[ops]}"
        fi

        if [ -n "${commits_by_type[chore]:-}" ]; then
            generate_type_section "chore" "Chores" "${commits_by_type[chore]}"
        fi
    fi

    echo ""
}

# Main
main() {
    # Parse arguments
    while [ $# -gt 0 ]; do
        case "$1" in
            -h|--help)
                show_help
                exit 0
                ;;
            -o|--output)
                OUTPUT_FILE="$2"
                shift 2
                ;;
            -r|--range)
                COMMIT_RANGE="$2"
                shift 2
                ;;
            -v|--version)
                VERSION="$2"
                shift 2
                ;;
            -t|--tag)
                TAG="$2"
                shift 2
                ;;
            --since-tag)
                SINCE_TAG="$2"
                shift 2
                ;;
            --unreleased)
                UNRELEASED=true
                shift
                ;;
            --no-header)
                NO_HEADER=true
                shift
                ;;
            --group-by)
                GROUP_BY="$2"
                shift 2
                ;;
            --include-all)
                INCLUDE_ALL=true
                shift
                ;;
            --breaking-first)
                BREAKING_FIRST=true
                shift
                ;;
            --link-commits)
                LINK_COMMITS=true
                shift
                ;;
            --link-issues)
                LINK_ISSUES=true
                shift
                ;;
            --repo-url)
                REPO_URL="$2"
                shift 2
                ;;
            --format)
                FORMAT="$2"
                shift 2
                ;;
            --dry-run)
                DRY_RUN=true
                shift
                ;;
            --verbose)
                VERBOSE=true
                shift
                ;;
            *)
                print_error "Unknown argument: $1"
                echo "Use --help for usage information"
                exit 2
                ;;
        esac
    done

    # Check if we're in a git repository
    if ! git rev-parse --git-dir > /dev/null 2>&1; then
        print_error "Not a git repository"
        exit 1
    fi

    # Auto-detect version if not specified
    if [ -z "$VERSION" ] && [ "$UNRELEASED" = false ]; then
        VERSION=$(auto_detect_version)
        print_info "Auto-detected version: $VERSION"
    fi

    # Generate changelog
    print_info "Generating changelog..."

    local changelog
    case "$FORMAT" in
        markdown)
            changelog=$(generate_markdown_changelog "$VERSION")
            ;;
        *)
            print_error "Unsupported format: $FORMAT"
            exit 2
            ;;
    esac

    # Output
    if [ "$DRY_RUN" = true ]; then
        echo "$changelog"
    else
        echo "$changelog" > "$OUTPUT_FILE"
        print_success "Changelog written to $OUTPUT_FILE"
    fi
}

main "$@"
