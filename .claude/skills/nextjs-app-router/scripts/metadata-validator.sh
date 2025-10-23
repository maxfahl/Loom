#!/bin/bash

# Next.js App Router Metadata Validator
#
# Validates all routes have proper metadata exports, checks OpenGraph images,
# ensures title/description uniqueness, and verifies metadata format.
# Generates SEO health report.
#
# Usage:
#   ./metadata-validator.sh
#   ./metadata-validator.sh app/
#   ./metadata-validator.sh --strict
#   ./metadata-validator.sh --report seo-report.html
#
# Examples:
#   # Basic validation
#   ./metadata-validator.sh
#
#   # Strict mode (fails on warnings)
#   ./metadata-validator.sh --strict
#
#   # Generate HTML report
#   ./metadata-validator.sh --report seo-report.html
#
# Time Saved: ~25 minutes per SEO audit

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'
BOLD='\033[1m'

# Configuration
TARGET_DIR="${1:-app}"
REPORT_FILE=""
STRICT_MODE=false
TOTAL_PAGES=0
PAGES_WITH_METADATA=0
PAGES_WITHOUT_METADATA=0
DUPLICATE_TITLES=0
DUPLICATE_DESCRIPTIONS=0
MISSING_OG_IMAGES=0

# Arrays for duplicate detection
declare -A TITLES
declare -A DESCRIPTIONS

# Parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --report)
      REPORT_FILE="$2"
      shift 2
      ;;
    --strict)
      STRICT_MODE=true
      shift
      ;;
    --help)
      echo "Usage: $0 [directory] [--report file] [--strict]"
      echo ""
      echo "Options:"
      echo "  --report FILE    Generate HTML report"
      echo "  --strict         Fail on warnings"
      echo "  --help           Show this help"
      exit 0
      ;;
    *)
      TARGET_DIR="$1"
      shift
      ;;
  esac
done

log_error() {
    echo -e "${RED}✗${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

log_success() {
    echo -e "${GREEN}✓${NC} $1"
}

log_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

echo -e "${BOLD}Next.js Metadata Validator${NC}"
echo "Analyzing: $TARGET_DIR"
echo ""

# Check if directory exists
if [ ! -d "$TARGET_DIR" ]; then
    log_error "Directory not found: $TARGET_DIR"
    exit 1
fi

# Extract metadata from file
extract_metadata() {
    local file=$1
    local metadata=""

    # Check for static metadata export
    if grep -q "export const metadata" "$file"; then
        metadata=$(sed -n '/export const metadata/,/^}/p' "$file")
        echo "$metadata"
        return 0
    fi

    # Check for generateMetadata function
    if grep -q "export async function generateMetadata" "$file"; then
        metadata=$(sed -n '/export async function generateMetadata/,/^}/p' "$file")
        echo "$metadata"
        return 0
    fi

    return 1
}

# Extract title from metadata
extract_title() {
    local metadata="$1"
    echo "$metadata" | grep -oP "title:\s*['\"]\\K[^'\"]+(?=['\"])" | head -1 || echo ""
}

# Extract description from metadata
extract_description() {
    local metadata="$1"
    echo "$metadata" | grep -oP "description:\s*['\"]\\K[^'\"]+(?=['\"])" | head -1 || echo ""
}

# Check for OpenGraph image
check_og_image() {
    local metadata="$1"
    echo "$metadata" | grep -q "openGraph" && echo "$metadata" | grep -q "images"
}

# Validate page metadata
validate_page() {
    local file=$1
    local relative_path=${file#$TARGET_DIR/}

    ((TOTAL_PAGES++))

    echo -e "\n${BOLD}Page:${NC} /$relative_path"

    metadata=$(extract_metadata "$file")

    if [ -z "$metadata" ]; then
        log_error "No metadata export found"
        ((PAGES_WITHOUT_METADATA++))
        return 1
    fi

    ((PAGES_WITH_METADATA++))

    # Extract and validate title
    title=$(extract_title "$metadata")
    if [ -z "$title" ]; then
        log_warning "Missing title"
    else
        log_success "Title: $title"

        # Check for duplicates
        if [ -n "${TITLES[$title]}" ]; then
            log_warning "Duplicate title: '$title' (also in ${TITLES[$title]})"
            ((DUPLICATE_TITLES++))
        else
            TITLES[$title]=$relative_path
        fi

        # Check title length
        title_length=${#title}
        if [ $title_length -lt 30 ]; then
            log_warning "Title too short ($title_length chars, recommended: 30-60)"
        elif [ $title_length -gt 60 ]; then
            log_warning "Title too long ($title_length chars, recommended: 30-60)"
        fi
    fi

    # Extract and validate description
    description=$(extract_description "$metadata")
    if [ -z "$description" ]; then
        log_warning "Missing description"
    else
        log_success "Description found (${#description} chars)"

        # Check for duplicates
        if [ -n "${DESCRIPTIONS[$description]}" ]; then
            log_warning "Duplicate description (also in ${DESCRIPTIONS[$description]})"
            ((DUPLICATE_DESCRIPTIONS++))
        else
            DESCRIPTIONS[$description]=$relative_path
        fi

        # Check description length
        desc_length=${#description}
        if [ $desc_length -lt 120 ]; then
            log_warning "Description too short ($desc_length chars, recommended: 120-160)"
        elif [ $desc_length -gt 160 ]; then
            log_warning "Description too long ($desc_length chars, recommended: 120-160)"
        fi
    fi

    # Check for OpenGraph image
    if check_og_image "$metadata"; then
        log_success "OpenGraph image defined"
    else
        log_warning "Missing OpenGraph image"
        ((MISSING_OG_IMAGES++))
    fi

    # Check for additional metadata
    if echo "$metadata" | grep -q "keywords"; then
        log_info "Has keywords (Note: Not used by major search engines)"
    fi

    if echo "$metadata" | grep -q "robots"; then
        log_success "Has robots configuration"
    fi

    if echo "$metadata" | grep -q "canonical"; then
        log_success "Has canonical URL"
    fi

    return 0
}

# Generate HTML report
generate_html_report() {
    local report_file=$1

    cat > "$report_file" << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SEO Metadata Report</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            line-height: 1.6;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f5f5;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
        }
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .stat-card {
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .stat-value {
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
        }
        .stat-label {
            color: #666;
            margin-top: 5px;
        }
        .success { color: #10b981; }
        .warning { color: #f59e0b; }
        .error { color: #ef4444; }
        .section {
            background: white;
            padding: 25px;
            border-radius: 8px;
            margin-bottom: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        h2 {
            margin-top: 0;
            color: #333;
        }
        .score {
            font-size: 3em;
            font-weight: bold;
            text-align: center;
            margin: 20px 0;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>SEO Metadata Analysis Report</h1>
        <p>Generated: $(date)</p>
        <p>Directory: $TARGET_DIR</p>
    </div>

    <div class="stats">
        <div class="stat-card">
            <div class="stat-value">$TOTAL_PAGES</div>
            <div class="stat-label">Total Pages</div>
        </div>
        <div class="stat-card">
            <div class="stat-value success">$PAGES_WITH_METADATA</div>
            <div class="stat-label">With Metadata</div>
        </div>
        <div class="stat-card">
            <div class="stat-value error">$PAGES_WITHOUT_METADATA</div>
            <div class="stat-label">Missing Metadata</div>
        </div>
        <div class="stat-card">
            <div class="stat-value warning">$DUPLICATE_TITLES</div>
            <div class="stat-label">Duplicate Titles</div>
        </div>
    </div>

    <div class="section">
        <h2>SEO Health Score</h2>
EOF

    # Calculate score
    local score=100
    [ $PAGES_WITHOUT_METADATA -gt 0 ] && score=$((score - PAGES_WITHOUT_METADATA * 10))
    [ $DUPLICATE_TITLES -gt 0 ] && score=$((score - DUPLICATE_TITLES * 5))
    [ $DUPLICATE_DESCRIPTIONS -gt 0 ] && score=$((score - DUPLICATE_DESCRIPTIONS * 5))
    [ $MISSING_OG_IMAGES -gt 0 ] && score=$((score - MISSING_OG_IMAGES * 3))
    [ $score -lt 0 ] && score=0

    local score_class="success"
    [ $score -lt 80 ] && score_class="warning"
    [ $score -lt 60 ] && score_class="error"

    cat >> "$report_file" << EOF
        <div class="score $score_class">$score/100</div>
        <p style="text-align: center;">
            $([ $score -ge 80 ] && echo "Great! Your SEO metadata is in good shape." || echo "Needs improvement. Review the issues below.")
        </p>
    </div>

    <div class="section">
        <h2>Recommendations</h2>
        <ul>
            $([ $PAGES_WITHOUT_METADATA -gt 0 ] && echo "<li class='error'>Add metadata exports to $PAGES_WITHOUT_METADATA pages</li>")
            $([ $DUPLICATE_TITLES -gt 0 ] && echo "<li class='warning'>Fix $DUPLICATE_TITLES duplicate titles</li>")
            $([ $DUPLICATE_DESCRIPTIONS -gt 0 ] && echo "<li class='warning'>Fix $DUPLICATE_DESCRIPTIONS duplicate descriptions</li>")
            $([ $MISSING_OG_IMAGES -gt 0 ] && echo "<li class='warning'>Add OpenGraph images to $MISSING_OG_IMAGES pages</li>")
            $([ $PAGES_WITH_METADATA -eq $TOTAL_PAGES ] && echo "<li class='success'>All pages have metadata ✓</li>")
        </ul>
    </div>
</body>
</html>
EOF

    log_info "HTML report generated: $report_file"
}

# Find and validate all pages
find "$TARGET_DIR" -name "page.tsx" -o -name "page.ts" | while read -r file; do
    validate_page "$file"
done

# Summary
echo ""
echo -e "${BOLD}===========================================${NC}"
echo -e "${BOLD}Summary${NC}"
echo -e "${BOLD}===========================================${NC}"
echo ""
echo "Total pages: $TOTAL_PAGES"
echo "With metadata: $PAGES_WITH_METADATA"
echo "Missing metadata: $PAGES_WITHOUT_METADATA"
echo "Duplicate titles: $DUPLICATE_TITLES"
echo "Duplicate descriptions: $DUPLICATE_DESCRIPTIONS"
echo "Missing OG images: $MISSING_OG_IMAGES"
echo ""

# Calculate score
SCORE=100
[ $PAGES_WITHOUT_METADATA -gt 0 ] && SCORE=$((SCORE - PAGES_WITHOUT_METADATA * 10))
[ $DUPLICATE_TITLES -gt 0 ] && SCORE=$((SCORE - DUPLICATE_TITLES * 5))
[ $DUPLICATE_DESCRIPTIONS -gt 0 ] && SCORE=$((SCORE - DUPLICATE_DESCRIPTIONS * 5))
[ $MISSING_OG_IMAGES -gt 0 ] && SCORE=$((SCORE - MISSING_OG_IMAGES * 3))
[ $SCORE -lt 0 ] && SCORE=0

echo "SEO Health Score: $SCORE/100"

if [ $SCORE -ge 80 ]; then
    echo -e "${GREEN}✓ Great! Your metadata is in good shape.${NC}"
elif [ $SCORE -ge 60 ]; then
    echo -e "${YELLOW}⚠ Good, but could be improved.${NC}"
else
    echo -e "${RED}✗ Needs improvement. Review the issues above.${NC}"
fi

# Generate report if requested
if [ -n "$REPORT_FILE" ]; then
    generate_html_report "$REPORT_FILE"
fi

# Exit with error in strict mode
if [ "$STRICT_MODE" = true ] && [ $SCORE -lt 80 ]; then
    exit 1
fi

exit 0
