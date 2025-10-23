#!/bin/bash

# jest-init.sh
# Description: Initializes a new JavaScript/TypeScript project with Jest configured,
#              including package.json scripts and a basic jest.config.js.
# Usage: ./jest-init.sh [project_name] [--lang <language>]
#
# Options:
#   --project <name>    Name of the new project directory. If not provided, initializes in current directory.
#   --lang <language>   Specify the primary language: 'js' (JavaScript, default), 'ts' (TypeScript).
#   --help              Display this help message.

set -euo pipefail

# --- Configuration Variables ---
COLOR_RESET="\033[0m"
COLOR_RED="\033[0;31m"
COLOR_GREEN="\033[0;32m"
COLOR_YELLOW="\033[0;33m"
COLOR_BLUE="\033[0;34m"

DEFAULT_PROJECT_NAME=""
DEFAULT_LANG="js"

# --- Helper Functions ---
log_info() {
  echo -e "${COLOR_BLUE}[INFO]${COLOR_RESET} $1"
}

log_success() {
  echo -e "${COLOR_GREEN}[SUCCESS]${COLOR_RESET} $1"
}

log_warning() {
  echo -e "${COLOR_YELLOW}[WARNING]${COLOR_RESET} $1"
}

log_error() {
  echo -e "${COLOR_RED}[ERROR]${COLOR_RESET} $1" >&2
  exit 1
}

show_help() {
  grep "^# Usage:" "$0" | sed -e 's/^# //' -e 's/^Usage: //'
  grep "^#   --" "$0" | sed -e 's/^#   //'
  exit 0
}

install_npm_deps() {
  local deps=("$@")
  log_info "Installing npm dependencies: ${deps[*]}..."
  npm install --save-dev "${deps[@]}" > /dev/null || log_error "Failed to install npm dependencies."
  log_success "npm dependencies installed."
}

# --- Main Logic ---
main() {
  local project_name="$DEFAULT_PROJECT_NAME"
  local lang="$DEFAULT_LANG"
  local project_dir

  # Parse arguments
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --project)
        project_name="$2"
        shift 2
        ;;
      --lang)
        lang="$2"
        shift 2
        ;;
      --help)
        show_help
        ;;
      -*)
        log_error "Unknown option: $1. Use --help for usage."
        ;;
      *)
        # Positional argument, assume it's project name if not already set
        if [[ -z "$project_name" ]]; then
          project_name="$1"
        else
          log_error "Unexpected argument: $1. Use --help for usage."
        fi
        shift
        ;;
    esac
  done

  project_dir="$(pwd)"
  if [[ -n "$project_name" ]]; then
    project_dir="$project_name"
  fi

  if [[ -n "$project_name" && ! -d "$project_dir" ]]; then
    log_info "Creating project directory: $project_dir"
    mkdir -p "$project_dir" || log_error "Failed to create directory $project_dir"
  fi

  cd "$project_dir" || log_error "Failed to change to directory $project_dir"

  log_info "Initializing Jest project in $(pwd) for language: $lang"

  # 1. Initialize npm project
  if [[ ! -f "package.json" ]]; then
    log_info "No package.json found. Initializing npm..."
    npm init -y > /dev/null || log_error "Failed to initialize npm."
    log_success "npm initialized."
  else
    log_info "package.json already exists. Skipping npm init."
  fi

  # 2. Install Jest and related dependencies
  if [[ "$lang" == "ts" ]]; then
    install_npm_deps "jest" "typescript" "ts-jest" "@types/jest" "@types/node"
  else
    install_npm_deps "jest"
  fi

  # 3. Configure TypeScript (if lang is ts)
  if [[ "$lang" == "ts" ]]; then
    if [[ ! -f "tsconfig.json" ]]; then
      log_info "Initializing tsconfig.json..."
      npx tsc --init --rootDir src --outDir dist --esModuleInterop --strict --skipLibCheck > /dev/null || log_error "Failed to initialize tsconfig.json."
      log_success "tsconfig.json created."
    else
      log_info "tsconfig.json already exists. Skipping creation."
    fi
  fi

  # 4. Create jest.config.js
  if [[ ! -f "jest.config.js" && ! -f "jest.config.ts" ]]; then
    log_info "Creating jest.config.js..."
    if [[ "$lang" == "ts" ]]; then
      echo "module.exports = { preset: 'ts-jest', testEnvironment: 'node', testMatch: ['**/__tests__/**/*.+(ts|tsx|js)', '**/?(*.)+(spec|test).+(ts|tsx|js)'] };" > jest.config.js
    else
      echo "module.exports = { testEnvironment: 'node', testMatch: ['**/__tests__/**/*.+(js)', '**/?(*.)+(spec|test).+(js)'] };" > jest.config.js
    fi
    log_success "jest.config.js created."
  else
    log_info "Jest config already exists. Skipping creation."
  fi

  # 5. Add sample source and test files
  local src_dir="src"
  local test_dir="__tests__"
  local src_file="${src_dir}/index.${lang}"
  local test_file="${test_dir}/index.test.${lang}"

  mkdir -p "${src_dir}"
  mkdir -p "${test_dir}"

  if [[ ! -f "$src_file" ]]; then
    log_info "Creating sample source file: $src_file..."
    if [[ "$lang" == "ts" ]]; then
      echo 'export function sum(a: number, b: number): number {
  return a + b;
}' > "$src_file"
    else
      echo 'exports.sum = (a, b) => a + b;' > "$src_file"
    fi
    log_success "Sample $src_file created."
  else
    log_info "$src_file already exists. Skipping creation."
  fi

  if [[ ! -f "$test_file" ]]; then
    log_info "Creating sample test file: $test_file..."
    if [[ "$lang" == "ts" ]]; then
      echo 'import { sum } from '../src/index';

describe('sum', () => {
  it('should add two numbers', () => {
    expect(sum(1, 2)).toBe(3);
  });
});' > "$test_file"
    else
      echo 'const { sum } = require('../src/index');

describe('sum', () => {
  it('should add two numbers', () => {
    expect(sum(1, 2)).toBe(3);
  });
});' > "$test_file"
    fi
    log_success "Sample $test_file created."
  else
    log_info "$test_file already exists. Skipping creation."
  fi

  # 6. Add test script to package.json
  log_info "Adding test script to package.json..."
  npm pkg set scripts.test="jest --watchAll" || log_error "Failed to add test script."
  log_success "Test script added to package.json."

  log_success "Jest project initialization complete!"
  log_info "To run tests: npm test"
}

# --- Script Entry Point ---
main "$@"
