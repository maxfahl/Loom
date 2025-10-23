#!/bin/bash
#
# detect-hardcoded-secrets.sh: Scans a specified directory for patterns that commonly indicate
# hardcoded secrets like API keys, passwords, and tokens.
#
# This script uses `grep` with a set of predefined regular expressions to identify potential leaks,
# helping prevent accidental exposure of sensitive credentials.
#
# Usage:
#   ./detect-hardcoded-secrets.sh <directory_to_scan> [--exclude-dir <dir>] [--dry-run]
#
# Examples:
#   ./detect-hardcoded-secrets.sh .
#   ./detect-hardcoded-secrets.sh ./src --exclude-dir node_modules
#   ./detect-hardcoded-secrets.sh /var/www/my-app --dry-run
#
# Configuration:
#   SECRETS_PATTERNS_FILE: Path to a file containing additional regex patterns (one per line).
#   EXCLUDE_PATTERNS_FILE: Path to a file containing additional glob patterns to exclude.
#
# Exit Codes:
#   0: No hardcoded secrets found.
#   1: Hardcoded secrets found or an error occurred.

# --- Configuration ---
# Default patterns to search for. Add more as needed.
# These are basic examples; real-world patterns can be more complex.
DEFAULT_SECRETS_PATTERNS=(
    "AKIA[0-9A-Z]{16}" # AWS Access Key ID
    "[sS][eE][cC][rR][eE][tT](_?[kK][eE][yY])?" # Generic secret_key, secretkey, secret
    "[pP][aA][sS][sS][wW][oO][rR][dD]" # Generic password
    "[aA][pP][iI](_?[kK][eE][yY])?" # Generic api_key, apikey
    "[tT][oO][kK][eE][nN]" # Generic token
    "[bB][eE][aA][rR][eE][rR] [A-Za-z0-9-_=]+\.[A-Za-z0-9-_=]+\.[A-Za-z0-9-_.+/=]*" # JWT token
    "-----BEGIN (RSA|EC|PGP) PRIVATE KEY-----" # Private keys
    "sk_live_[0-9a-zA-Z]{24}" # Stripe Live Secret Key
    "pk_live_[0-9a-zA-Z]{24}" # Stripe Live Publishable Key (less critical but good to flag)
    "ghp_[0-9a-zA-Z]{36}" # GitHub Personal Access Token
    "xoxb-[0-9]{12}-[0-9]{12}-[0-9a-zA-Z]{24}" # Slack Bot User OAuth Access Token
)

# Default directories/files to exclude from scanning
DEFAULT_EXCLUDE_PATTERNS=(
    ".git"
    "node_modules"
    "vendor"
    "build"
    "dist"
    "*.min.js"
    "*.map"
    "*.lock"
    "*.log"
    "*.bak"
    "*.tmp"
    "*.swp"
    "*.swo"
    "*.DS_Store"
    "*.env.example" # Often contains placeholder secrets
)

# --- Functions ---
print_help() {
    echo "Usage: $0 <directory_to_scan> [--exclude-dir <dir>] [--dry-run]"
    echo ""
    echo "Scans a directory for hardcoded secrets using predefined and custom regex patterns."
    echo ""
    echo "Arguments:"
    echo "  <directory_to_scan>   The root directory to start scanning from."
    echo ""
    echo "Options:"
    echo "  --exclude-dir <dir>   Exclude a specific directory (can be used multiple times)."
    echo "  --dry-run             Perform a dry run without actually scanning, just show configuration."
    echo "  --help                Display this help message."
    echo ""
    echo "Configuration (Environment Variables or Files):"
    echo "  SECRETS_PATTERNS_FILE: Path to a file containing additional regex patterns (one per line)."
    echo "  EXCLUDE_PATTERNS_FILE: Path to a file containing additional glob patterns to exclude."
    echo ""
    echo "Exit Codes:"
    echo "  0: No hardcoded secrets found."
    echo "  1: Hardcoded secrets found or an error occurred."
}

# Function to print colored output
print_color() {
    local text="$1"
    local color="$2"
    case "$color" in
        "red")    echo -e "\033[0;31m${text}\033[0m";; # Red
        "green")  echo -e "\033[0;32m${text}\033[0m";; # Green
        "yellow") echo -e "\033[0;33m${text}\033[0m";; # Yellow
        "blue")   echo -e "\033[0;34m${text}\033[0m";; # Blue
        "cyan")   echo -e "\033[0;36m${text}\033[0m";; # Cyan
        *)
            echo "${text}";;
    esac
}

# Function to load patterns from a file
load_patterns_from_file() {
    local file_path="$1"
    local patterns_array_name="$2"
    if [[ -f "$file_path" ]]; then
        print_color "Loading additional patterns from: $file_path" "blue"
        while IFS= read -r line || [[ -n "$line" ]]; do
            # Skip empty lines and comments
            [[ -z "$line" || "${line:0:1}" == "#" ]] && continue
            eval "$patterns_array_name+=(\"$line\")"
        done < "$file_path"
    fi
}

# --- Main Script ---
SCAN_DIR=""
EXCLUDE_DIRS=()
DRY_RUN=false

# Parse arguments
while [[ "$#" -gt 0 ]]; do
    case "$1" in
        --exclude-dir)
            if [[ -z "$2" ]]; then
                print_color "Error: --exclude-dir requires an argument." "red"
                print_help
                exit 1
            fi
            EXCLUDE_DIRS+=("$2")
            shift 2
            ;; 
        --dry-run)
            DRY_RUN=true
            shift
            ;; 
        --help)
            print_help
            exit 0
            ;; 
        -*)
            print_color "Error: Unknown option $1" "red"
            print_help
            exit 1
            ;; 
        *)
            if [[ -z "$SCAN_DIR" ]]; then
                SCAN_DIR="$1"
            else
                print_color "Error: Too many arguments. Only one directory to scan is allowed." "red"
                print_help
                exit 1
            fi
            shift
            ;; 
    esac
done

if [[ -z "$SCAN_DIR" ]]; then
    print_color "Error: Please specify a directory to scan." "red"
    print_help
    exit 1
fi

if [[ ! -d "$SCAN_DIR" ]]; then
    print_color "Error: Directory '$SCAN_DIR' not found." "red"
    exit 1
fi

# Combine default and custom patterns
ALL_SECRETS_PATTERNS=("${DEFAULT_SECRETS_PATTERNS[@]}")
load_patterns_from_file "${SECRETS_PATTERNS_FILE:-}" ALL_SECRETS_PATTERNS

ALL_EXCLUDE_PATTERNS=("${DEFAULT_EXCLUDE_PATTERNS[@]}")
load_patterns_from_file "${EXCLUDE_PATTERNS_FILE:-}" ALL_EXCLUDE_PATTERNS
ALL_EXCLUDE_PATTERNS+=("${EXCLUDE_DIRS[@]}")

# Build grep exclude arguments
GREP_EXCLUDE_ARGS=""
for pattern in "${ALL_EXCLUDE_PATTERNS[@]}"; do
    GREP_EXCLUDE_ARGS+=" --exclude-dir=$pattern"
    GREP_EXCLUDE_ARGS+=" --exclude=$pattern"
done

if $DRY_RUN; then
    print_color "--- Dry Run Configuration ---" "cyan"
    print_color "Scan Directory: $SCAN_DIR" "blue"
    print_color "Search Patterns:" "blue"
    for pattern in "${ALL_SECRETS_PATTERNS[@]}"; do
        print_color "  - $pattern" "blue"
    done
    print_color "Exclude Patterns:" "blue"
    for pattern in "${ALL_EXCLUDE_PATTERNS[@]}"; do
        print_color "  - $pattern" "blue"
    done
    print_color "-----------------------------" "cyan"
    exit 0
fi

print_color "Starting hardcoded secrets scan in '$SCAN_DIR' ..." "cyan"
print_color "(Excluding: ${ALL_EXCLUDE_PATTERNS[*]})\n" "cyan"

SECRETS_FOUND=false

for pattern in "${ALL_SECRETS_PATTERNS[@]}"; do
    print_color "Searching for pattern: '$pattern'" "blue"
    # Using `grep -P` for Perl-compatible regular expressions for better pattern matching
    # -r: recursive
    # -n: show line number
    # -H: always print filename
    # -o: print only the matched (non-empty) parts of a matching line
    # -I: process a binary file as if it did not contain matching data
    # --color=always: force colored output even when piping
    # --exclude-dir and --exclude for ignoring files/directories
    MATCHES=$(grep -r -n -H -o -P -I --color=always "$pattern" "$SCAN_DIR" $GREP_EXCLUDE_ARGS 2>/dev/null)

    if [[ -n "$MATCHES" ]]; then
        SECRETS_FOUND=true
        print_color "  Potential secret found with pattern '$pattern':" "yellow"
        echo "$MATCHES"
        echo ""
    else
        print_color "  No matches found for pattern '$pattern'." "green"
    fi
done

if $SECRETS_FOUND; then
    print_color "\n[SCAN FAILED] Potential hardcoded secrets detected! Please review the output above." "red"
    exit 1
else
    print_color "\n[SCAN PASSED] No hardcoded secrets detected." "green"
    exit 0
fi
