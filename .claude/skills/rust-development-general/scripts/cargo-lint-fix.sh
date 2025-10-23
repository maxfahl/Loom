#!/bin/bash
# cargo-lint-fix.sh
#
# Description:
#   Automates running `cargo fmt` and `cargo clippy --fix` across the project.
#   Ensures code style consistency and automatically fixes common linting issues.
#
# Usage:
#   ./cargo-lint-fix.sh [OPTIONS] [-- <cargo_args>]
#
# Options:
#   -d, --dry-run   Perform a dry run without applying changes.
#   -c, --clippy-only Run only clippy, skip rustfmt.
#   -f, --fmt-only  Run only rustfmt, skip clippy.
#   -h, --help      Display this help message.
#
# Arguments after --:
#   Any arguments after `--` will be passed directly to `cargo fmt` and `cargo clippy`.
#   E.g., `./cargo-lint-fix.sh -- -p my_crate` to run only for `my_crate`.
#
# Examples:
#   ./cargo-lint-fix.sh
#   ./cargo-lint-fix.sh --dry-run
#   ./cargo-lint-fix.sh --clippy-only
#   ./cargo-lint-fix.sh -- -p my_specific_crate
#
# Error Handling:
#   Exits with an error if `cargo fmt` or `cargo clippy` fail (unless dry-run).
#   Provides informative messages for each step.

set -euo pipefail

DRY_RUN=false
CLIPPY_ONLY=false
FMT_ONLY=false
CARGO_ARGS=""

# --- Helper Functions ---
print_help() {
    grep '^#' "$0" | cut -c 2- | sed -n '/^Usage:/,/^Examples:/p'
    exit 0
}

# --- Argument Parsing ---
while [[ $# -gt 0 ]]; do
    case "$1" in
        -d|--dry-run)
            DRY_RUN=true
            ;;
        -c|--clippy-only)
            CLIPPY_ONLY=true
            ;;
        -f|--fmt-only)
            FMT_ONLY=true
            ;;
        -h|--help)
            print_help
            ;;
        --)
            shift
            CARGO_ARGS="$@"
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

# Check for conflicting options
if $CLIPPY_ONLY && $FMT_ONLY; then
    echo "Error: Cannot use --clippy-only and --fmt-only together."
    exit 1
fi

# Run rustfmt
if ! $CLIPPY_ONLY; then
    echo "🎨 Running cargo fmt..."
    FMT_COMMAND="cargo fmt --all"
    if $DRY_RUN; then
        FMT_COMMAND="$FMT_COMMAND --check"
    fi
    if [ -n "$CARGO_ARGS" ]; then
        FMT_COMMAND="$FMT_COMMAND $CARGO_ARGS"
    fi

    if eval "$FMT_COMMAND"; then
        echo "✅ cargo fmt completed."
    else
        echo "❌ cargo fmt failed or found unformatted files."
        if $DRY_RUN; then
            echo "Run without --dry-run to apply formatting."
        fi
        exit 1
    fi
fi

# Run clippy
if ! $FMT_ONLY; then
    echo "🔍 Running cargo clippy..."
    CLIPPY_COMMAND="cargo clippy --workspace --all-targets -- -D warnings"
    if ! $DRY_RUN; then
        CLIPPY_COMMAND="$CLIPPY_COMMAND --fix"
    fi
    if [ -n "$CARGO_ARGS" ]; then
        CLIPPY_COMMAND="$CLIPPY_COMMAND $CARGO_ARGS"
    fi

    if eval "$CLIPPY_COMMAND"; then
        echo "✅ cargo clippy completed."
    else
        echo "❌ cargo clippy failed or found linting issues."
        if $DRY_RUN; then
            echo "Run without --dry-run to apply fixes."
        fi
        exit 1
    fi
fi

echo "🎉 Linting and formatting checks complete."
