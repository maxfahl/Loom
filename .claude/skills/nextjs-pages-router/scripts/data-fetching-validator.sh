#!/usr/bin/env bash
#
# Next.js Data Fetching Validator
#
# Validates proper use of data fetching methods across your Next.js Pages Router codebase.
# Checks for common anti-patterns and provides actionable recommendations.
#
# Usage:
#   ./data-fetching-validator.sh [OPTIONS]
#
# Options:
#   -d, --directory DIR    Pages directory to scan (default: ./pages)
#   -v, --verbose          Show detailed output
#   -j, --json             Output results in JSON format
#   -f, --fix              Auto-fix simple issues (use with caution)
#   --strict               Enable strict mode (more warnings)
#   --exclude PATTERN      Exclude files matching pattern
#   -h, --help             Show this help message
#
# Examples:
#   # Scan default pages directory
#   ./data-fetching-validator.sh
#
#   # Scan specific directory with verbose output
#   ./data-fetching-validator.sh -d src/pages -v
#
#   # Generate JSON report
#   ./data-fetching-validator.sh --json > report.json
#
# Exit codes:
#   0 - No issues found
#   1 - Issues found (warnings or errors)
#   2 - Script error
#
# Author: DevDev AI
# Version: 1.0.0

set -eo pipefail

# Colors
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# Default values
PAGES_DIR="./pages"
VERBOSE=false
JSON_OUTPUT=false
AUTO_FIX=false
STRICT_MODE=false
EXCLUDE_PATTERN=""

# Counters
ERROR_COUNT=0
WARNING_COUNT=0
INFO_COUNT=0

# Issues array (for JSON output)
declare -a ISSUES=()

# Functions
print_error() {
    if [[ "$JSON_OUTPUT" == false ]]; then
        echo -e "${RED}✗ ERROR: $1${NC}" >&2
    fi
    ISSUES+=("{\"type\":\"error\",\"message\":\"$1\",\"file\":\"${2:-}\"}")
    ((ERROR_COUNT++))
}

print_warning() {
    if [[ "$JSON_OUTPUT" == false ]]; then
        echo -e "${YELLOW}⚠ WARNING: $1${NC}"
    fi
    ISSUES+=("{\"type\":\"warning\",\"message\":\"$1\",\"file\":\"${2:-}\"}")
    ((WARNING_COUNT++))
}

print_info() {
    if [[ "$JSON_OUTPUT" == false ]] && [[ "$VERBOSE" == true ]]; then
        echo -e "${BLUE}ℹ INFO: $1${NC}"
    fi
    ((INFO_COUNT++))
}

print_success() {
    if [[ "$JSON_OUTPUT" == false ]]; then
        echo -e "${GREEN}✓ $1${NC}"
    fi
}

print_header() {
    if [[ "$JSON_OUTPUT" == false ]]; then
        echo -e "${BOLD}${CYAN}$1${NC}"
    fi
}

show_help() {
    sed -n '/^#/,/^$/p' "$0" | sed 's/^# \?//' | head -n -1
}

# Check if file should be excluded
should_exclude() {
    local file="$1"
    if [[ -n "$EXCLUDE_PATTERN" ]] && echo "$file" | grep -q "$EXCLUDE_PATTERN"; then
        return 0
    fi
    return 1
}

# Check for missing getStaticPaths in dynamic SSG routes
check_missing_static_paths() {
    local file="$1"
    local filename=$(basename "$file")

    # Check if file is a dynamic route (contains [])
    if [[ ! "$filename" =~ \[.*\] ]]; then
        return 0
    fi

    # Skip if it's in the api directory
    if [[ "$file" =~ /api/ ]]; then
        return 0
    fi

    # Check if file has getStaticProps but no getStaticPaths
    if grep -q "getStaticProps" "$file"; then
        if ! grep -q "getStaticPaths" "$file"; then
            print_error "Dynamic route missing getStaticPaths: Must export getStaticPaths when using getStaticProps with dynamic routes" "$file"
            if [[ "$AUTO_FIX" == true ]]; then
                print_info "Auto-fix not available for this issue. Please add getStaticPaths manually."
            fi
        else
            print_success "Dynamic route properly configured: $file" if [[ "$VERBOSE" == true ]]
        fi
    fi
}

# Check for invalid revalidate values
check_revalidate_values() {
    local file="$1"

    # Find revalidate values
    while IFS= read -r line; do
        if [[ "$line" =~ revalidate:[[:space:]]*([0-9]+) ]]; then
            local revalidate_value="${BASH_REMATCH[1]}"

            if [[ "$revalidate_value" -lt 1 ]]; then
                print_error "Invalid revalidate value: $revalidate_value (must be >= 1)" "$file"
            elif [[ "$revalidate_value" -lt 10 ]]; then
                print_warning "Very aggressive revalidate value: $revalidate_value seconds (consider increasing to reduce server load)" "$file"
            elif [[ "$revalidate_value" -gt 86400 ]]; then
                print_warning "Very large revalidate value: $revalidate_value seconds (>24 hours, consider using static generation instead)" "$file"
            elif [[ "$VERBOSE" == true ]]; then
                print_info "Revalidate value: $revalidate_value seconds in $file"
            fi
        fi
    done < "$file"
}

# Check for mixed data fetching methods
check_mixed_data_fetching() {
    local file="$1"

    local has_static=$(grep -c "getStaticProps" "$file" || true)
    local has_server=$(grep -c "getServerSideProps" "$file" || true)

    if [[ "$has_static" -gt 0 ]] && [[ "$has_server" -gt 0 ]]; then
        print_error "Mixed data fetching methods: Cannot use both getStaticProps and getServerSideProps in the same file" "$file"
    fi
}

# Check for legacy getInitialProps
check_legacy_methods() {
    local file="$1"

    if grep -q "getInitialProps" "$file"; then
        print_warning "Legacy method detected: getInitialProps disables automatic static optimization. Consider using getStaticProps or getServerSideProps instead" "$file"
    fi
}

# Check for client-side fetching in pages
check_client_side_fetching() {
    local file="$1"

    # Skip _app and _document
    if [[ "$file" =~ _app\.(tsx|ts|jsx|js)$ ]] || [[ "$file" =~ _document\.(tsx|ts|jsx|js)$ ]]; then
        return 0
    fi

    # Check if file has useEffect with fetch but no data fetching methods
    if grep -q "useEffect" "$file" && grep -q "fetch(" "$file"; then
        if ! grep -q "getStaticProps\|getServerSideProps" "$file"; then
            if [[ "$STRICT_MODE" == true ]]; then
                print_warning "Client-side data fetching detected: Consider using getStaticProps or getServerSideProps for better SEO and performance" "$file"
            fi
        fi
    fi
}

# Check fallback configuration
check_fallback_config() {
    local file="$1"

    if grep -q "getStaticPaths" "$file"; then
        if ! grep -q "fallback:" "$file"; then
            print_warning "Missing fallback configuration: getStaticPaths should specify a fallback strategy" "$file"
        else
            # Check if using fallback: true without isFallback check
            if grep -q "fallback:[[:space:]]*true" "$file"; then
                if ! grep -q "router.isFallback\|isFallback" "$file"; then
                    print_warning "Fallback true without loading state: Should check router.isFallback when using fallback: true" "$file"
                fi
            fi
        fi
    fi
}

# Check for API route fetching in data fetching methods
check_api_route_fetching() {
    local file="$1"

    if grep -q "getStaticProps\|getServerSideProps" "$file"; then
        if grep -q "fetch.*localhost.*\/api\/\|fetch.*\/api\/" "$file"; then
            print_error "Anti-pattern detected: Fetching from API routes in data fetching methods. Import shared logic directly instead" "$file"
        fi
    fi
}

# Check for non-serializable data
check_serialization() {
    local file="$1"

    if grep -q "getStaticProps\|getServerSideProps" "$file"; then
        # Check for Date objects in return
        if grep -A 10 "return[[:space:]]*{" "$file" | grep -q "new Date()"; then
            print_warning "Potential serialization issue: Returning Date objects. Convert to ISO string using .toISOString()" "$file"
        fi

        # Check for functions in return
        if grep -A 10 "return[[:space:]]*{" "$file" | grep -q "().*=>"; then
            print_error "Serialization error: Cannot return functions from data fetching methods" "$file"
        fi
    fi
}

# Check for proper error handling
check_error_handling() {
    local file="$1"

    if grep -q "getStaticProps\|getServerSideProps" "$file"; then
        if ! grep -q "try\|catch" "$file"; then
            if [[ "$STRICT_MODE" == true ]]; then
                print_warning "Missing error handling: Consider adding try-catch blocks in data fetching methods" "$file"
            fi
        fi

        # Check for notFound or redirect handling
        if ! grep -q "notFound:\|redirect:" "$file"; then
            if [[ "$STRICT_MODE" == true ]]; then
                print_info "No error handling: Consider returning notFound or redirect for error cases in $file"
            fi
        fi
    fi
}

# Check TypeScript types
check_typescript_types() {
    local file="$1"

    # Only check .ts and .tsx files
    if [[ ! "$file" =~ \.(tsx|ts)$ ]]; then
        return 0
    fi

    if grep -q "getStaticProps" "$file"; then
        if ! grep -q "GetStaticProps" "$file"; then
            print_warning "Missing TypeScript type: Import GetStaticProps from 'next'" "$file"
        fi
    fi

    if grep -q "getServerSideProps" "$file"; then
        if ! grep -q "GetServerSideProps" "$file"; then
            print_warning "Missing TypeScript type: Import GetServerSideProps from 'next'" "$file"
        fi
    fi

    if grep -q "getStaticPaths" "$file"; then
        if ! grep -q "GetStaticPaths" "$file"; then
            print_warning "Missing TypeScript type: Import GetStaticPaths from 'next'" "$file"
        fi
    fi
}

# Main scanning function
scan_file() {
    local file="$1"

    if should_exclude "$file"; then
        print_info "Skipping excluded file: $file"
        return 0
    fi

    if [[ "$VERBOSE" == true ]]; then
        print_info "Scanning: $file"
    fi

    check_missing_static_paths "$file"
    check_revalidate_values "$file"
    check_mixed_data_fetching "$file"
    check_legacy_methods "$file"
    check_client_side_fetching "$file"
    check_fallback_config "$file"
    check_api_route_fetching "$file"
    check_serialization "$file"
    check_error_handling "$file"
    check_typescript_types "$file"
}

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -d|--directory)
            PAGES_DIR="$2"
            shift 2
            ;;
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        -j|--json)
            JSON_OUTPUT=true
            shift
            ;;
        -f|--fix)
            AUTO_FIX=true
            shift
            ;;
        --strict)
            STRICT_MODE=true
            shift
            ;;
        --exclude)
            EXCLUDE_PATTERN="$2"
            shift 2
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            show_help
            exit 2
            ;;
    esac
done

# Validate pages directory
if [[ ! -d "$PAGES_DIR" ]]; then
    print_error "Pages directory not found: $PAGES_DIR"
    exit 2
fi

# Main execution
print_header "Next.js Data Fetching Validator"
echo ""

if [[ "$JSON_OUTPUT" == false ]]; then
    echo "Scanning directory: $PAGES_DIR"
    echo "Strict mode: $STRICT_MODE"
    echo ""
fi

# Find and scan all page files
file_count=0
while IFS= read -r -d '' file; do
    scan_file "$file"
    ((file_count++))
done < <(find "$PAGES_DIR" -type f \( -name "*.tsx" -o -name "*.ts" -o -name "*.jsx" -o -name "*.js" \) -print0)

# Print summary
if [[ "$JSON_OUTPUT" == true ]]; then
    echo "{"
    echo "  \"summary\": {"
    echo "    \"filesScanned\": $file_count,"
    echo "    \"errors\": $ERROR_COUNT,"
    echo "    \"warnings\": $WARNING_COUNT,"
    echo "    \"info\": $INFO_COUNT"
    echo "  },"
    echo "  \"issues\": ["
    printf "    %s" "${ISSUES[0]}"
    for issue in "${ISSUES[@]:1}"; do
        printf ",\n    %s" "$issue"
    done
    echo ""
    echo "  ]"
    echo "}"
else
    echo ""
    print_header "Summary"
    echo "Files scanned: $file_count"
    echo -e "${RED}Errors: $ERROR_COUNT${NC}"
    echo -e "${YELLOW}Warnings: $WARNING_COUNT${NC}"
    if [[ "$VERBOSE" == true ]]; then
        echo -e "${BLUE}Info: $INFO_COUNT${NC}"
    fi

    if [[ "$ERROR_COUNT" -eq 0 ]] && [[ "$WARNING_COUNT" -eq 0 ]]; then
        echo ""
        print_success "No issues found! Your data fetching implementation looks good."
    else
        echo ""
        echo -e "${YELLOW}Review the issues above and fix them to improve your Next.js application.${NC}"
    fi
fi

# Exit with appropriate code
if [[ "$ERROR_COUNT" -gt 0 ]] || [[ "$WARNING_COUNT" -gt 0 ]]; then
    exit 1
else
    exit 0
fi
