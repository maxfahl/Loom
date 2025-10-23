#!/bin/bash

# tdd-init.sh
# Description: Initializes a new project with a basic testing framework setup.
#              Supports Jest for JavaScript/TypeScript and Pytest for Python.
# Usage: ./tdd-init.sh [project_name] [--lang <language>] [--test-runner <runner>]
#
# Options:
#   --project <name>    Name of the new project directory. If not provided, initializes in current directory.
#   --lang <language>   Specify the primary language: 'js', 'ts' (TypeScript), 'py' (Python).
#                       Defaults to 'ts'.
#   --test-runner <runner> Specify the test runner: 'jest' (for js/ts), 'pytest' (for py).
#                       Defaults based on language.
#   --help              Display this help message.

set -euo pipefail

# --- Configuration Variables ---
COLOR_RESET="\033[0m"
COLOR_RED="\033[0;31m"
COLOR_GREEN="\033[0;32m"
COLOR_YELLOW="\033[0;33m"
COLOR_BLUE="\033[0;34m"

DEFAULT_PROJECT_NAME=""
DEFAULT_LANG="ts"
DEFAULT_TEST_RUNNER=""

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

install_pip_deps() {
  local deps=("$@")
  log_info "Installing pip dependencies: ${deps[*]}..."
  python3 -m pip install "${deps[@]}" > /dev/null || log_error "Failed to install pip dependencies."
  log_success "pip dependencies installed."
}

# --- Main Logic ---
main() {
  local project_name="$DEFAULT_PROJECT_NAME"
  local lang="$DEFAULT_LANG"
  local test_runner="$DEFAULT_TEST_RUNNER"
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
      --test-runner)
        test_runner="$2"
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

  log_info "Initializing TDD project in $(pwd) for language: $lang"

  case "$lang" in
    js|ts)
      if [[ -z "$test_runner" ]]; then test_runner="jest"; fi
      if [[ "$test_runner" != "jest" ]]; then log_error "Only 'jest' is supported for JS/TS."; fi

      if [[ ! -f "package.json" ]]; then
        log_info "Initializing npm project..."
        npm init -y > /dev/null || log_error "Failed to initialize npm."
        log_success "npm initialized."
      else
        log_info "package.json already exists. Skipping npm init."
      fi

      if [[ "$lang" == "ts" ]]; then
        log_info "Setting up TypeScript..."
        install_npm_deps "typescript" "ts-jest" "@types/jest" "@types/node"
        if [[ ! -f "tsconfig.json" ]]; then
          npx tsc --init --rootDir src --outDir dist --esModuleInterop --strict --skipLibCheck > /dev/null || log_error "Failed to initialize tsconfig.json."
          log_success "tsconfig.json created."
        else
          log_info "tsconfig.json already exists. Skipping creation."
        fi
        # Add a sample src/index.ts
        if [[ ! -f "src/index.ts" ]]; then
          mkdir -p src
          echo 'export function add(a: number, b: number): number { return a + b; }' > src/index.ts
          log_success "Sample src/index.ts created."
        else
          log_info "src/index.ts already exists. Skipping creation."
        fi
      else # js
        install_npm_deps "jest"
        # Add a sample index.js
        if [[ ! -f "index.js" ]]; then
          echo 'exports.add = (a, b) => a + b;' > index.js
          log_success "Sample index.js created."
        else
          log_info "index.js already exists. Skipping creation."
        fi
      fi

      log_info "Setting up Jest..."
      if [[ ! -f "jest.config.js" && ! -f "jest.config.ts" ]]; then
        # npx jest --init --forceExit --detectOpenHandles --passWithNoTests --testEnvironment=node > /dev/null || log_error "Failed to initialize Jest."
        # Simplified Jest config creation
        echo "module.exports = { preset: 'ts-jest', testEnvironment: 'node', testMatch: ['**/__tests__/**/*.+(ts|tsx|js)', '**/?(*.)+(spec|test).+(ts|tsx|js)'] };" > jest.config.js
        log_success "jest.config.js created."
      else
        log_info "Jest config already exists. Skipping creation."
      fi

      # Add a sample test file
      local test_file="test/index.test.${lang}"
      if [[ ! -f "$test_file" ]]; then
        mkdir -p test
        if [[ "$lang" == "ts" ]]; then
          echo 'import { add } from '../src/index';

describe('add', () => {
  it('should add two numbers', () => {
    expect(add(1, 2)).toBe(3);
  });
});' > "$test_file"
        else
          echo 'const { add } = require('../index');

describe('add', () => {
  it('should add two numbers', () => {
    expect(add(1, 2)).toBe(3);
  });
});' > "$test_file"
        fi
        log_success "Sample $test_file created."
      else
        log_info "$test_file already exists. Skipping creation."
      fi

      log_info "Adding test script to package.json..."
      npm pkg set scripts.test="jest --watchAll" || log_error "Failed to add test script."
      log_success "Test script added to package.json."
      log_success "Project initialized for TDD with Jest!"
      log_info "To run tests: npm test"
      ;;
    py)
      if [[ -z "$test_runner" ]]; then test_runner="pytest"; fi
      if [[ "$test_runner" != "pytest" ]]; then log_error "Only 'pytest' is supported for Python."; fi

      if [[ ! -d "venv" ]]; then
        log_info "Creating virtual environment..."
        python3 -m venv venv > /dev/null || log_error "Failed to create virtual environment."
        log_success "Virtual environment created."
      else
        log_info "Virtual environment 'venv' already exists. Skipping creation."
      fi

      log_info "Installing pytest..."
      source venv/bin/activate || log_error "Failed to activate virtual environment."
      install_pip_deps "pytest"
      deactivate # Deactivate after installation

      # Add a sample main.py
      if [[ ! -f "main.py" ]]; then
        echo 'def add(a, b):
    return a + b' > main.py
        log_success "Sample main.py created."
      else
        log_info "main.py already exists. Skipping creation."
      fi

      # Add a sample test_main.py
      if [[ ! -f "test_main.py" ]]; then
        echo 'from main import add

def test_add():
    assert add(1, 2) == 3' > test_main.py
        log_success "Sample test_main.py created."
      else
        log_info "test_main.py already exists. Skipping creation."
      fi

      log_success "Project initialized for TDD with Pytest!"
      log_info "To run tests: source venv/bin/activate && pytest"
      ;;
    *)
      log_error "Unsupported language: $lang. Choose 'js', 'ts', or 'py'."
      ;;
  esac

  log_success "TDD project initialization complete!"
}

# --- Script Entry Point ---
main "$@"
