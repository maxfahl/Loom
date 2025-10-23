#!/usr/bin/env bash

################################################################################
# Git Hooks Installer for Conventional Commits
#
# Purpose:
#   Install and configure git hooks to enforce Conventional Commits specification
#   Supports commit-msg validation and optional prepare-commit-msg templates
#
# Usage:
#   ./commit-hook-installer.sh [OPTIONS]
#
# Options:
#   -h, --help              Show this help message
#   --install               Install git hooks (default action)
#   --uninstall             Remove installed git hooks
#   --update                Update existing git hooks
#   --global                Install hooks globally (for all repos)
#   --check                 Check if hooks are installed
#   --hook-type TYPE        Hook type to install: commit-msg, prepare-commit-msg, both (default: both)
#   --validator-path PATH   Path to commit-validator.sh script
#   --template              Install prepare-commit-msg template helper
#   --strict                Enable strict validation mode
#   --allowed-types TYPES   Comma-separated list of allowed commit types
#   --require-scope         Require scope in all commits
#   --backup                Create backup of existing hooks before installing
#   --force                 Overwrite existing hooks without asking
#   -v, --verbose           Show verbose output
#
# Examples:
#   # Install hooks in current repository
#   ./commit-hook-installer.sh --install
#
#   # Install globally for all repositories
#   ./commit-hook-installer.sh --install --global
#
#   # Install with strict validation
#   ./commit-hook-installer.sh --install --strict --require-scope
#
#   # Install only commit-msg hook
#   ./commit-hook-installer.sh --install --hook-type commit-msg
#
#   # Check installation status
#   ./commit-hook-installer.sh --check
#
#   # Uninstall hooks
#   ./commit-hook-installer.sh --uninstall
#
#   # Install with custom validator
#   ./commit-hook-installer.sh --install --validator-path /path/to/validator.sh
#
# Exit Codes:
#   0 - Success
#   1 - Installation/uninstallation failed
#   2 - Invalid arguments or not a git repository
################################################################################

set -euo pipefail

# Default configuration
ACTION="install"
GLOBAL=false
HOOK_TYPE="both"
VALIDATOR_PATH=""
TEMPLATE=false
STRICT_MODE=false
ALLOWED_TYPES="feat,fix,refactor,perf,style,test,docs,build,ops,chore"
REQUIRE_SCOPE=false
BACKUP=true
FORCE=false
VERBOSE=false

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
BOLD='\033[1m'
NC='\033[0m'

print_error() {
    echo -e "${RED}ERROR: $*${NC}" >&2
}

print_success() {
    echo -e "${GREEN}✓ $*${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ $*${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $*${NC}"
}

print_verbose() {
    if [ "$VERBOSE" = true ]; then
        echo -e "${BLUE}  $*${NC}"
    fi
}

show_help() {
    sed -n '/^# Purpose:/,/^################################################################################$/p' "$0" | sed 's/^# //; s/^#//'
}

# Get hooks directory
get_hooks_dir() {
    if [ "$GLOBAL" = true ]; then
        local template_dir
        template_dir=$(git config --global init.templateDir 2>/dev/null || echo "")

        if [ -z "$template_dir" ]; then
            template_dir="$HOME/.git-templates"
            print_verbose "Setting global template directory to: $template_dir"
            git config --global init.templateDir "$template_dir"
        fi

        echo "$template_dir/hooks"
    else
        # Check if we're in a git repository
        if ! git rev-parse --git-dir > /dev/null 2>&1; then
            print_error "Not a git repository"
            exit 2
        fi

        local git_dir
        git_dir=$(git rev-parse --git-dir)
        echo "$git_dir/hooks"
    fi
}

# Create commit-msg hook
create_commit_msg_hook() {
    local hooks_dir="$1"
    local hook_file="$hooks_dir/commit-msg"

    print_verbose "Creating commit-msg hook at: $hook_file"

    # Determine validator path
    local validator_cmd
    if [ -n "$VALIDATOR_PATH" ]; then
        if [ ! -f "$VALIDATOR_PATH" ]; then
            print_error "Validator script not found: $VALIDATOR_PATH"
            return 1
        fi
        validator_cmd="$VALIDATOR_PATH"
    else
        # Try to find validator in same directory as this script
        local script_dir
        script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
        local default_validator="$script_dir/commit-validator.sh"

        if [ -f "$default_validator" ]; then
            validator_cmd="$default_validator"
            print_verbose "Using default validator: $validator_cmd"
        else
            # Embed inline validator
            validator_cmd="inline"
            print_verbose "Using inline validator"
        fi
    fi

    # Build hook options
    local hook_options=""
    if [ "$STRICT_MODE" = true ]; then
        hook_options+=" --strict"
    fi
    if [ "$REQUIRE_SCOPE" = true ]; then
        hook_options+=" --require-scope"
    fi
    if [ -n "$ALLOWED_TYPES" ]; then
        hook_options+=" --allowed-types \"$ALLOWED_TYPES\""
    fi

    # Create hook content
    if [ "$validator_cmd" = "inline" ]; then
        # Inline validator (basic version)
        cat > "$hook_file" << 'EOF'
#!/usr/bin/env bash

# Conventional Commits validation hook (inline version)

commit_msg_file=$1
commit_msg=$(cat "$commit_msg_file")

# Check for merge commits (allow them)
if [[ "$commit_msg" =~ ^Merge ]]; then
    exit 0
fi

# Check for revert commits (allow them)
if [[ "$commit_msg" =~ ^Revert ]]; then
    exit 0
fi

# Extract first line
first_line=$(echo "$commit_msg" | head -n1)

# Pattern: type(scope)!: description
pattern="^(feat|fix|refactor|perf|style|test|docs|build|ops|chore|revert)(\([a-z0-9-]+\))?!?: .+"

if ! [[ "$first_line" =~ $pattern ]]; then
    echo "ERROR: Commit message does not follow Conventional Commits format"
    echo ""
    echo "Format: <type>[optional scope]: <description>"
    echo ""
    echo "Example: feat(auth): add password reset functionality"
    echo ""
    echo "Valid types: feat, fix, refactor, perf, style, test, docs, build, ops, chore"
    echo ""
    echo "Your message:"
    echo "  $first_line"
    exit 1
fi

exit 0
EOF
    else
        # Use external validator
        cat > "$hook_file" << EOF
#!/usr/bin/env bash

# Conventional Commits validation hook
# Using validator: $validator_cmd

commit_msg_file=\$1

"$validator_cmd" --file "\$commit_msg_file" $hook_options

exit \$?
EOF
    fi

    chmod +x "$hook_file"
    return 0
}

# Create prepare-commit-msg hook
create_prepare_commit_msg_hook() {
    local hooks_dir="$1"
    local hook_file="$hooks_dir/prepare-commit-msg"

    print_verbose "Creating prepare-commit-msg hook at: $hook_file"

    cat > "$hook_file" << 'EOF'
#!/usr/bin/env bash

# Conventional Commits template helper

commit_msg_file=$1
commit_source=$2

# Only add template for new commits (not merge, squash, etc.)
if [ -z "$commit_source" ]; then
    # Check if file is empty or has only comments
    if ! grep -qv '^#' "$commit_msg_file" 2>/dev/null; then
        # Add template
        cat > "$commit_msg_file" << 'TEMPLATE'
# <type>[optional scope]: <description>
#
# [optional body]
#
# [optional footer(s)]
#
# Types:
#   feat:     A new feature
#   fix:      A bug fix
#   refactor: Code change that neither fixes a bug nor adds a feature
#   perf:     Performance improvement
#   style:    Code style/formatting changes
#   test:     Adding or updating tests
#   docs:     Documentation changes
#   build:    Build system or dependency changes
#   ops:      Operational/infrastructure changes
#   chore:    Miscellaneous changes
#
# Breaking changes: Add ! after type/scope (e.g., feat!: remove endpoint)
# Scope: Optional, describes section of codebase (e.g., feat(api): ...)
# Description: Use imperative mood, lowercase, no period at end
#
# Examples:
#   feat(auth): add password reset functionality
#   fix(api): resolve race condition in token refresh
#   docs: update installation guide
#   feat!: remove support for API v1
TEMPLATE
    fi
fi

exit 0
EOF

    chmod +x "$hook_file"
    return 0
}

# Backup existing hook
backup_hook() {
    local hook_file="$1"

    if [ -f "$hook_file" ]; then
        local backup_file="${hook_file}.backup.$(date +%Y%m%d_%H%M%S)"
        print_verbose "Backing up existing hook to: $backup_file"
        cp "$hook_file" "$backup_file"
        print_info "Backed up existing hook to: $(basename "$backup_file")"
    fi
}

# Install hooks
install_hooks() {
    local hooks_dir
    hooks_dir=$(get_hooks_dir)

    # Create hooks directory if it doesn't exist
    mkdir -p "$hooks_dir"
    print_verbose "Hooks directory: $hooks_dir"

    # Install commit-msg hook
    if [ "$HOOK_TYPE" = "commit-msg" ] || [ "$HOOK_TYPE" = "both" ]; then
        local commit_msg_hook="$hooks_dir/commit-msg"

        if [ -f "$commit_msg_hook" ] && [ "$FORCE" = false ]; then
            print_warning "commit-msg hook already exists"
            read -p "Overwrite? (y/n) " -n 1 -r
            echo
            if [[ ! $REPLY =~ ^[Yy]$ ]]; then
                print_info "Skipping commit-msg hook installation"
            else
                if [ "$BACKUP" = true ]; then
                    backup_hook "$commit_msg_hook"
                fi
                create_commit_msg_hook "$hooks_dir"
                print_success "Installed commit-msg hook"
            fi
        else
            if [ -f "$commit_msg_hook" ] && [ "$BACKUP" = true ]; then
                backup_hook "$commit_msg_hook"
            fi
            create_commit_msg_hook "$hooks_dir"
            print_success "Installed commit-msg hook"
        fi
    fi

    # Install prepare-commit-msg hook
    if [ "$TEMPLATE" = true ] && ([ "$HOOK_TYPE" = "prepare-commit-msg" ] || [ "$HOOK_TYPE" = "both" ]); then
        local prepare_hook="$hooks_dir/prepare-commit-msg"

        if [ -f "$prepare_hook" ] && [ "$FORCE" = false ]; then
            print_warning "prepare-commit-msg hook already exists"
            read -p "Overwrite? (y/n) " -n 1 -r
            echo
            if [[ ! $REPLY =~ ^[Yy]$ ]]; then
                print_info "Skipping prepare-commit-msg hook installation"
            else
                if [ "$BACKUP" = true ]; then
                    backup_hook "$prepare_hook"
                fi
                create_prepare_commit_msg_hook "$hooks_dir"
                print_success "Installed prepare-commit-msg hook"
            fi
        else
            if [ -f "$prepare_hook" ] && [ "$BACKUP" = true ]; then
                backup_hook "$prepare_hook"
            fi
            create_prepare_commit_msg_hook "$hooks_dir"
            print_success "Installed prepare-commit-msg hook"
        fi
    fi

    echo ""
    print_success "Git hooks installation complete!"

    if [ "$GLOBAL" = true ]; then
        echo ""
        print_info "Hooks installed globally. Run 'git init' in existing repos to apply."
    fi
}

# Uninstall hooks
uninstall_hooks() {
    local hooks_dir
    hooks_dir=$(get_hooks_dir)

    local removed=false

    # Remove commit-msg hook
    if [ -f "$hooks_dir/commit-msg" ]; then
        if [ "$BACKUP" = true ]; then
            backup_hook "$hooks_dir/commit-msg"
        fi
        rm "$hooks_dir/commit-msg"
        print_success "Removed commit-msg hook"
        removed=true
    fi

    # Remove prepare-commit-msg hook
    if [ -f "$hooks_dir/prepare-commit-msg" ]; then
        if [ "$BACKUP" = true ]; then
            backup_hook "$hooks_dir/prepare-commit-msg"
        fi
        rm "$hooks_dir/prepare-commit-msg"
        print_success "Removed prepare-commit-msg hook"
        removed=true
    fi

    if [ "$removed" = false ]; then
        print_info "No hooks found to remove"
    else
        echo ""
        print_success "Git hooks uninstalled successfully!"
    fi
}

# Check hook installation
check_hooks() {
    local hooks_dir
    hooks_dir=$(get_hooks_dir)

    echo ""
    echo -e "${BOLD}Git Hooks Status${NC}"
    echo "Hooks directory: $hooks_dir"
    echo ""

    local has_hooks=false

    # Check commit-msg
    if [ -f "$hooks_dir/commit-msg" ]; then
        print_success "commit-msg hook is installed"
        has_hooks=true
    else
        print_warning "commit-msg hook is NOT installed"
    fi

    # Check prepare-commit-msg
    if [ -f "$hooks_dir/prepare-commit-msg" ]; then
        print_success "prepare-commit-msg hook is installed"
        has_hooks=true
    else
        print_info "prepare-commit-msg hook is NOT installed"
    fi

    echo ""

    if [ "$has_hooks" = false ]; then
        print_info "No conventional commits hooks are installed"
        print_info "Run with --install to install hooks"
    fi
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
            --install)
                ACTION="install"
                shift
                ;;
            --uninstall)
                ACTION="uninstall"
                shift
                ;;
            --update)
                ACTION="update"
                FORCE=true
                shift
                ;;
            --check)
                ACTION="check"
                shift
                ;;
            --global)
                GLOBAL=true
                shift
                ;;
            --hook-type)
                HOOK_TYPE="$2"
                shift 2
                ;;
            --validator-path)
                VALIDATOR_PATH="$2"
                shift 2
                ;;
            --template)
                TEMPLATE=true
                shift
                ;;
            --strict)
                STRICT_MODE=true
                shift
                ;;
            --allowed-types)
                ALLOWED_TYPES="$2"
                shift 2
                ;;
            --require-scope)
                REQUIRE_SCOPE=true
                shift
                ;;
            --backup)
                BACKUP=true
                shift
                ;;
            --force)
                FORCE=true
                shift
                ;;
            -v|--verbose)
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

    # Execute action
    case "$ACTION" in
        install|update)
            install_hooks
            ;;
        uninstall)
            uninstall_hooks
            ;;
        check)
            check_hooks
            ;;
        *)
            print_error "Invalid action: $ACTION"
            exit 2
            ;;
    esac
}

main "$@"
