#!/bin/bash
# cargo-dep-audit.sh
#
# Description:
#   Audits project dependencies for known vulnerabilities using `cargo audit`.
#   Provides a summary report and includes options to ignore specific advisories.
#
# Usage:
#   ./cargo-dep-audit.sh [OPTIONS] [-- <cargo_audit_args>]
#
# Options:
#   -i, --ignore <advisory_id>  Ignore a specific advisory ID (can be used multiple times).
#   -h, --help                  Display this help message.
#
# Arguments after --:
#   Any arguments after `--` will be passed directly to `cargo audit`.
#   E.g., `./cargo-dep-audit.sh -- --json` to get JSON output.
#
# Examples:
#   ./cargo-dep-audit.sh
#   ./cargo-dep-audit.sh --ignore RUSTSEC-2020-0071
#   ./cargo-dep-audit.sh -i RUSTSEC-2020-0071 -i RUSTSEC-2021-0123
#   ./cargo-dep-audit.sh -- --deny warnings
#
# Error Handling:
#   - Checks if `cargo audit` is installed and guides the user if not.
#   - Exits with a non-zero status if vulnerabilities are found (unless ignored).
#   - Provides informative messages for each step.

set -euo pipefail

IGNORE_ADVISORIES=()
CARGO_AUDIT_ARGS=""

# --- Helper Functions ---
print_help() {
    grep '^#' "$0" | cut -c 2- | sed -n '/^Usage:/,/^Examples:/p'
    exit 0
}

# --- Argument Parsing ---
while [[ $# -gt 0 ]]; do
    case "$1" in
        -i|--ignore)
            if [[ -z "$2" ]]; then
                echo "Error: --ignore requires an advisory ID."
                print_help
            fi
            IGNORE_ADVISORIES+=("--ignore $2")
            shift
            ;;
        -h|--help)
            print_help
            ;;
        --)
            shift
            CARGO_AUDIT_ARGS="$@"
            break
            ;;
        *)
            echo "Error: Unknown option '$1'"
            print_help
            ;;
    esac
    shift
done

# --- Main Logic ---

# Check if cargo audit is installed
if ! command -v cargo-audit &> /dev/null;
then
    echo "❌ cargo-audit is not installed."
    echo "Please install it using: cargo install cargo-audit"
    exit 1
fi

echo "🔍 Running cargo audit for vulnerabilities..."

# Construct the cargo audit command
AUDIT_COMMAND=("cargo audit")
AUDIT_COMMAND+=("${IGNORE_ADVISORIES[@]}")
AUDIT_COMMAND+=("$CARGO_AUDIT_ARGS")

# Execute cargo audit
if "${AUDIT_COMMAND[@]}"; then
    echo "✅ No vulnerabilities found (or all found vulnerabilities were ignored)."
else
    echo "❌ Vulnerabilities found. Please review the report above."
    exit 1
fi

echo "🎉 Dependency audit complete."
