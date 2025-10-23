#!/bin/bash

# Next.js App Router Server/Client Component Analyzer
#
# Analyzes component boundaries and flags anti-patterns like Server Components
# in Client Components, data fetching in Client Components, or missing 'use client'
# directives. Provides actionable recommendations.
#
# Usage:
#   ./server-client-analyzer.sh
#   ./server-client-analyzer.sh app/
#   ./server-client-analyzer.sh --fix-auto
#   ./server-client-analyzer.sh --report report.txt
#
# Examples:
#   # Analyze current directory
#   ./server-client-analyzer.sh
#
#   # Analyze specific directory
#   ./server-client-analyzer.sh app/components
#
#   # Generate report file
#   ./server-client-analyzer.sh --report analysis.txt
#
#   # Analyze with auto-fix suggestions
#   ./server-client-analyzer.sh --fix-auto
#
# Time Saved: ~15 minutes per code review

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color
BOLD='\033[1m'

# Counters
TOTAL_FILES=0
TOTAL_ISSUES=0
TOTAL_WARNINGS=0
CLIENT_COMPONENTS=0
SERVER_COMPONENTS=0

# Configuration
TARGET_DIR="${1:-.}"
REPORT_FILE=""
AUTO_FIX=false

# Parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --report)
      REPORT_FILE="$2"
      shift 2
      ;;
    --fix-auto)
      AUTO_FIX=true
      shift
      ;;
    --help)
      echo "Usage: $0 [directory] [--report file] [--fix-auto]"
      echo ""
      echo "Options:"
      echo "  --report FILE    Generate report to file"
      echo "  --fix-auto       Show auto-fix suggestions"
      echo "  --help           Show this help message"
      exit 0
      ;;
    *)
      TARGET_DIR="$1"
      shift
      ;;
  esac
done

# Logging functions
log_error() {
    echo -e "${RED}✗${NC} $1"
    [ -n "$REPORT_FILE" ] && echo "[ERROR] $1" >> "$REPORT_FILE"
}

log_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
    [ -n "$REPORT_FILE" ] && echo "[WARNING] $1" >> "$REPORT_FILE"
}

log_success() {
    echo -e "${GREEN}✓${NC} $1"
    [ -n "$REPORT_FILE" ] && echo "[OK] $1" >> "$REPORT_FILE"
}

log_info() {
    echo -e "${BLUE}ℹ${NC} $1"
    [ -n "$REPORT_FILE" ] && echo "[INFO] $1" >> "$REPORT_FILE"
}

# Initialize report
if [ -n "$REPORT_FILE" ]; then
    echo "Next.js App Router Analysis Report" > "$REPORT_FILE"
    echo "Generated: $(date)" >> "$REPORT_FILE"
    echo "Directory: $TARGET_DIR" >> "$REPORT_FILE"
    echo "===========================================" >> "$REPORT_FILE"
    echo "" >> "$REPORT_FILE"
fi

echo -e "${BOLD}Next.js App Router Component Analyzer${NC}"
echo "Analyzing: $TARGET_DIR"
echo ""

# Check if directory exists
if [ ! -d "$TARGET_DIR" ]; then
    log_error "Directory not found: $TARGET_DIR"
    exit 1
fi

# Check for use client directive
check_use_client() {
    local file=$1
    grep -q "^['\"]use client['\"]" "$file" 2>/dev/null
}

# Check for use server directive
check_use_server() {
    local file=$1
    grep -q "^['\"]use server['\"]" "$file" 2>/dev/null
}

# Check for React hooks
check_react_hooks() {
    local file=$1
    grep -qE "(useState|useEffect|useContext|useReducer|useCallback|useMemo|useRef|useLayoutEffect)" "$file" 2>/dev/null
}

# Check for event handlers
check_event_handlers() {
    local file=$1
    grep -qE "(onClick|onChange|onSubmit|onFocus|onBlur|onMouseEnter|onMouseLeave)" "$file" 2>/dev/null
}

# Check for browser APIs
check_browser_apis() {
    local file=$1
    grep -qE "(window\.|document\.|localStorage|sessionStorage|navigator\.|location\.)" "$file" 2>/dev/null
}

# Check for data fetching
check_data_fetching() {
    local file=$1
    grep -qE "(fetch\(|axios\.|db\.|prisma\.|sql)" "$file" 2>/dev/null
}

# Check for async component
check_async_component() {
    local file=$1
    grep -qE "export default async function" "$file" 2>/dev/null
}

# Check for Server Component imports in Client Component
check_server_in_client() {
    local file=$1
    # This is a simplified check - would need more sophisticated analysis in production
    if check_use_client "$file"; then
        # Look for imports that might be Server Components
        grep -E "^import.*from ['\"]\.\/.*['\"]" "$file" | while read -r import_line; do
            local imported_file=$(echo "$import_line" | sed -E "s/.*from ['\"]([^'\"]+)['\"].*/\1/")
            local base_dir=$(dirname "$file")
            local full_path="$base_dir/$imported_file"

            # Add .tsx/.ts extension if missing
            [ ! -f "$full_path" ] && full_path="${full_path}.tsx"
            [ ! -f "$full_path" ] && full_path="${full_path}.ts"

            if [ -f "$full_path" ]; then
                if ! check_use_client "$full_path" && check_async_component "$full_path"; then
                    return 0  # Found Server Component import
                fi
            fi
        done
    fi
    return 1
}

# Analyze single file
analyze_file() {
    local file=$1
    local has_issues=false
    local is_client=false

    ((TOTAL_FILES++))

    # Determine if client or server component
    if check_use_client "$file"; then
        is_client=true
        ((CLIENT_COMPONENTS++))
    else
        ((SERVER_COMPONENTS++))
    fi

    echo -e "\n${BOLD}Analyzing:${NC} $file"

    # Anti-pattern 1: React hooks without 'use client'
    if ! check_use_client "$file" && check_react_hooks "$file"; then
        log_error "Uses React hooks but missing 'use client' directive"
        ((TOTAL_ISSUES++))
        has_issues=true

        if [ "$AUTO_FIX" = true ]; then
            log_info "Fix: Add 'use client' at the top of the file"
        fi
    fi

    # Anti-pattern 2: Event handlers without 'use client'
    if ! check_use_client "$file" && check_event_handlers "$file"; then
        log_error "Uses event handlers but missing 'use client' directive"
        ((TOTAL_ISSUES++))
        has_issues=true

        if [ "$AUTO_FIX" = true ]; then
            log_info "Fix: Add 'use client' at the top of the file"
        fi
    fi

    # Anti-pattern 3: Browser APIs without 'use client'
    if ! check_use_client "$file" && check_browser_apis "$file"; then
        log_error "Uses browser APIs but missing 'use client' directive"
        ((TOTAL_ISSUES++))
        has_issues=true

        if [ "$AUTO_FIX" = true ]; then
            log_info "Fix: Add 'use client' at the top of the file"
        fi
    fi

    # Anti-pattern 4: Data fetching in Client Component
    if check_use_client "$file" && check_data_fetching "$file" && check_react_hooks "$file"; then
        log_warning "Client Component appears to fetch data (prefer Server Components)"
        ((TOTAL_WARNINGS++))

        if [ "$AUTO_FIX" = true ]; then
            log_info "Suggestion: Move data fetching to Server Component or use route handler"
        fi
    fi

    # Anti-pattern 5: Async Server Component without proper typing
    if check_async_component "$file" && ! grep -q "Promise<" "$file"; then
        log_warning "Async component may be missing proper TypeScript types"
        ((TOTAL_WARNINGS++))

        if [ "$AUTO_FIX" = true ]; then
            log_info "Suggestion: Add proper async types to component props"
        fi
    fi

    # Anti-pattern 6: Server Component imported in Client Component (simplified check)
    if check_server_in_client "$file"; then
        log_error "Possible Server Component imported into Client Component"
        ((TOTAL_ISSUES++))
        has_issues=true

        if [ "$AUTO_FIX" = true ]; then
            log_info "Fix: Pass Server Component as children/props instead of importing"
        fi
    fi

    if ! $has_issues; then
        log_success "No issues found"
    fi
}

# Find all TypeScript/TSX files
echo "Scanning for TypeScript/TSX files..."
echo ""

# Process files
find "$TARGET_DIR" -type f \( -name "*.tsx" -o -name "*.ts" \) ! -path "*/node_modules/*" ! -path "*/.next/*" | while read -r file; do
    # Skip non-component files
    if [[ "$file" =~ (layout|page|loading|error|not-found|route)\.tsx?$ ]] || [[ "$file" =~ /components/ ]]; then
        analyze_file "$file"
    fi
done

# Summary
echo ""
echo -e "${BOLD}===========================================${NC}"
echo -e "${BOLD}Analysis Summary${NC}"
echo -e "${BOLD}===========================================${NC}"
echo ""
echo "Total files analyzed: $TOTAL_FILES"
echo "Server Components: $SERVER_COMPONENTS"
echo "Client Components: $CLIENT_COMPONENTS"
echo ""

if [ $TOTAL_ISSUES -eq 0 ] && [ $TOTAL_WARNINGS -eq 0 ]; then
    echo -e "${GREEN}✓ No issues found! Your components follow best practices.${NC}"
elif [ $TOTAL_ISSUES -eq 0 ]; then
    echo -e "${YELLOW}⚠ Found $TOTAL_WARNINGS warnings (no critical issues)${NC}"
else
    echo -e "${RED}✗ Found $TOTAL_ISSUES critical issues and $TOTAL_WARNINGS warnings${NC}"
fi

echo ""
echo "Recommendations:"
echo "  • Keep Server Components as default"
echo "  • Add 'use client' only when needed for interactivity"
echo "  • Fetch data in Server Components, not Client Components"
echo "  • Pass Server Components as props/children to Client Components"

if [ "$AUTO_FIX" = false ]; then
    echo ""
    echo "Tip: Run with --fix-auto for fix suggestions"
fi

if [ -n "$REPORT_FILE" ]; then
    echo ""
    echo "===========================================" >> "$REPORT_FILE"
    echo "Summary:" >> "$REPORT_FILE"
    echo "  Total files: $TOTAL_FILES" >> "$REPORT_FILE"
    echo "  Issues: $TOTAL_ISSUES" >> "$REPORT_FILE"
    echo "  Warnings: $TOTAL_WARNINGS" >> "$REPORT_FILE"
    echo ""
    log_info "Report saved to: $REPORT_FILE"
fi

# Exit with error code if issues found
[ $TOTAL_ISSUES -gt 0 ] && exit 1
exit 0
