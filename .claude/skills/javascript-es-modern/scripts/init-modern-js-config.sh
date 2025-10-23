#!/bin/bash

# init-modern-js-config.sh
#
# Purpose:
#   Automates the setup of a modern JavaScript/TypeScript project with recommended
#   ESLint, Prettier, and TypeScript configurations. This script ensures a
#   consistent and best-practice development environment from the start.
#
# Usage:
#   ./init-modern-js-config.sh [OPTIONS]
#
# Options:
#   -h, --help        Display this help message.
#   -y, --yes         Skip confirmation prompts and use default values.
#   -t, --typescript  Initialize with TypeScript configuration (default: true).
#   -e, --eslint      Initialize with ESLint configuration (default: true).
#   -p, --prettier    Initialize with Prettier configuration (default: true).
#   -f, --force       Overwrite existing configuration files without prompt.
#
# Examples:
#   ./init-modern-js-config.sh
#   ./init-modern-js-config.sh --yes --typescript --eslint --prettier
#   ./init-modern-js-config.sh -y -t -e -p
#   ./init-modern-js-config.sh --no-typescript # Initialize without TypeScript
#
# Requirements:
#   - Node.js and npm/yarn/pnpm installed.
#   - Basic understanding of ESLint, Prettier, and TypeScript.

# --- Configuration ---
DEFAULT_TYPESCRIPT=true
DEFAULT_ESLINT=true
DEFAULT_PRETTIER=true
SKIP_CONFIRMATION=false
FORCE_OVERWRITE=false

# --- Colors for output ---
GREEN="\033[0;32m"
YELLOW="\033[0;33m"
RED="\033[0;31m"
BLUE="\033[0;34m"
NC="\033[0m" # No Color

# --- Helper Functions ---

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1" >&2
}

display_help() {
    grep '^#' "$0" | cut -c 3-
    exit 0
}

confirm() {
    if [ "$SKIP_CONFIRMATION" = true ]; then
        return 0
    fi
    read -r -p "$(echo -e "${YELLOW}$1 (y/N): ${NC}")" response
    case "$response" in
        [yY][eE][sS]|[yY])
            true
            ;; 
        *)
            false
            ;; 
    esac
}

check_command() {
    if ! command -v "$1" &> /dev/null; then
        log_error "$1 is not installed. Please install it to proceed."
        exit 1
    fi
}

# --- Argument Parsing ---
for arg in "$@"; do
    case $arg in
        -h|--help)
            display_help
            ;; 
        -y|--yes)
            SKIP_CONFIRMATION=true
            ;; 
        -t|--typescript)
            DEFAULT_TYPESCRIPT=true
            ;; 
        --no-typescript)
            DEFAULT_TYPESCRIPT=false
            ;; 
        -e|--eslint)
            DEFAULT_ESLINT=true
            ;; 
        --no-eslint)
            DEFAULT_ESLINT=false
            ;; 
        -p|--prettier)
            DEFAULT_PRETTIER=true
            ;; 
        --no-prettier)
            DEFAULT_PRETTIER=false
            ;; 
        -f|--force)
            FORCE_OVERWRITE=true
            ;; 
        *)
            log_warn "Unknown option: $arg. Ignoring."
            ;; 
    esac
done

# --- Main Script Logic ---

log_info "Starting modern JavaScript/TypeScript project configuration setup..."

# Check for npm/yarn/pnpm
if command -v pnpm &> /dev/null; then
    PACKAGE_MANAGER="pnpm"
elif command -v yarn &> /dev/null; then
    PACKAGE_MANAGER="yarn"
elif command -v npm &> /dev/null; then
    PACKAGE_MANAGER="npm"
else
    log_error "No package manager (npm, yarn, or pnpm) found. Please install one to proceed."
    exit 1
fi
log_info "Using package manager: $PACKAGE_MANAGER"

# Initialize package.json if it doesn't exist
if [ ! -f package.json ]; then
    log_info "package.json not found. Initializing a new one."
    if confirm "Do you want to initialize a new package.json?"; then
        $PACKAGE_MANAGER init -y
        log_success "package.json initialized."
    else
        log_error "Aborting: package.json is required."
        exit 1
    fi
fi

# --- TypeScript Setup ---
if [ "$DEFAULT_TYPESCRIPT" = true ]; then
    log_info "Setting up TypeScript..."
    if [ -f tsconfig.json ] && [ "$FORCE_OVERWRITE" = false ]; then
        log_warn "tsconfig.json already exists. Use -f or --force to overwrite."
        if ! confirm "Do you want to skip TypeScript setup?"; then
            log_info "Skipping TypeScript setup."
            DEFAULT_TYPESCRIPT=false # Disable further TS actions
        fi
    fi

    if [ "$DEFAULT_TYPESCRIPT" = true ]; then
        log_info "Installing TypeScript and @types/node..."
        $PACKAGE_MANAGER add -D typescript @types/node || { log_error "Failed to install TypeScript dependencies."; exit 1; }

        log_info "Creating tsconfig.json..."
        cat << EOF > tsconfig.json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "lib": ["ES2022", "DOM"],
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "moduleResolution": "Node",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "allowSyntheticDefaultImports": true,
    "declaration": true,
    "outDir": "./dist",
    "rootDir": "./src"
  },
  "include": ["src/**/*.ts", "src/**/*.tsx"],
  "exclude": ["node_modules", "dist"]
}
EOF
        log_success "tsconfig.json created with modern settings."
        log_info "Remember to create a 'src' directory for your source files."
    fi
fi

# --- ESLint Setup ---
if [ "$DEFAULT_ESLINT" = true ]; then
    log_info "Setting up ESLint..."
    if [ -f .eslintrc.json ] && [ "$FORCE_OVERWRITE" = false ]; then
        log_warn ".eslintrc.json already exists. Use -f or --force to overwrite."
        if ! confirm "Do you want to skip ESLint setup?"; then
            log_info "Skipping ESLint setup."
            DEFAULT_ESLINT=false # Disable further ESLint actions
        fi
    fi

    if [ "$DEFAULT_ESLINT" = true ]; then
        log_info "Installing ESLint and plugins..."
        ESLINT_PLUGINS="eslint @typescript-eslint/eslint-plugin @typescript-eslint/parser eslint-plugin-prettier eslint-config-prettier"
        if [ "$DEFAULT_TYPESCRIPT" = true ]; then
            $PACKAGE_MANAGER add -D $ESLINT_PLUGINS || { log_error "Failed to install ESLint dependencies."; exit 1; }
        else
            $PACKAGE_MANAGER add -D eslint eslint-config-prettier || { log_error "Failed to install ESLint dependencies."; exit 1; }
        fi

        log_info "Creating .eslintrc.json..."
        if [ "$DEFAULT_TYPESCRIPT" = true ]; then
            cat << EOF > .eslintrc.json
{
  "root": true,
  "parser": "@typescript-eslint/parser",
  "plugins": ["@typescript-eslint"],
  "extends": [
    "eslint:recommended",
    "plugin:@typescript-eslint/recommended",
    "prettier"
  ],
  "parserOptions": {
    "ecmaVersion": "latest",
    "sourceType": "module"
  },
  "env": {
    "browser": true,
    "node": true,
    "es2022": true
  },
  "rules": {
    // Add or override ESLint rules here
    "@typescript-eslint/no-unused-vars": ["warn", { "argsIgnorePattern": "^_" }],
    "@typescript-eslint/explicit-module-boundary-types": "off",
    "no-console": "warn"
  }
}
EOF
        else
            cat << EOF > .eslintrc.json
{
  "root": true,
  "extends": [
    "eslint:recommended",
    "prettier"
  ],
  "parserOptions": {
    "ecmaVersion": "latest",
    "sourceType": "module"
  },
  "env": {
    "browser": true,
    "node": true,
    "es2022": true
  },
  "rules": {
    // Add or override ESLint rules here
    "no-console": "warn"
  }
}
EOF
        fi
        log_success ".eslintrc.json created."
    fi
fi

# --- Prettier Setup ---
if [ "$DEFAULT_PRETTIER" = true ]; then
    log_info "Setting up Prettier..."
    if [ -f .prettierrc.json ] && [ "$FORCE_OVERWRITE" = false ]; then
        log_warn ".prettierrc.json already exists. Use -f or --force to overwrite."
        if ! confirm "Do you want to skip Prettier setup?"; then
            log_info "Skipping Prettier setup."
            DEFAULT_PRETTIER=false # Disable further Prettier actions
        fi
    fi

    if [ "$DEFAULT_PRETTIER" = true ]; then
        log_info "Installing Prettier..."
        $PACKAGE_MANAGER add -D prettier || { log_error "Failed to install Prettier."; exit 1; }

        log_info "Creating .prettierrc.json..."
        cat << EOF > .prettierrc.json
{
  "semi": true,
  "trailingComma": "all",
  "singleQuote": true,
  "printWidth": 100,
  "tabWidth": 2,
  "useTabs": false
}
EOF
        log_success ".prettierrc.json created."

        log_info "Creating .prettierignore..."
        cat << EOF > .prettierignore
# Ignore artifacts:
build
dist
node_modules
coverage

# Ignore logs:
*.log

# Ignore generated files:
*.min.js
*.map

# Ignore specific files:
package-lock.json
yarn.lock
pnpm-lock.yaml
EOF
        log_success ".prettierignore created."
    fi
fi

# --- Add scripts to package.json ---
log_info "Adding lint and format scripts to package.json..."
# Using jq to safely add/update scripts
if command -v jq &> /dev/null; then
    if [ "$DEFAULT_TYPESCRIPT" = true ]; then
        jq '.scripts += {"lint": "eslint \"{src,apps,libs,test}/**/*.ts\" --fix", "format": "prettier --write \"{src,apps,libs,test}/**/*.ts\""}' package.json > tmp.$$.json && mv tmp.$$.json package.json
    else
        jq '.scripts += {"lint": "eslint \"{src,apps,libs,test}/**/*.js\" --fix", "format": "prettier --write \"{src,apps,libs,test}/**/*.js\""}' package.json > tmp.$$.json && mv tmp.$$.json package.json
    fi
    log_success "Added 'lint' and 'format' scripts to package.json."
else
    log_warn "jq not found. Please install it to automatically add scripts to package.json, or add them manually:"
    if [ "$DEFAULT_TYPESCRIPT" = true ]; then
        log_warn "  \"lint\": \"eslint \\\"{src,apps,libs,test}/**/*.ts\\\" --fix\""
        log_warn "  \"format\": \"prettier --write \\\"{src,apps,libs,test}/**/*.ts\\\"\""
    else
        log_warn "  \"lint\": \"eslint \\\"{src,apps,libs,test}/**/*.js\\\" --fix\""
        log_warn "  \"format\": \"prettier --write \\\"{src,apps,libs,test}/**/*.js\\\"\""
    fi
fi

log_success "Modern JavaScript/TypeScript configuration setup complete!"
log_info "You can now run: '$PACKAGE_MANAGER run lint' and '$PACKAGE_MANAGER run format'"
log_info "Remember to create a 'src' directory and start coding!"
