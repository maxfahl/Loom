#!/bin/bash

# strict-mode-initializer.sh
# Description: Initializes a new TypeScript project with a recommended tsconfig.json
#              configured for strict mode and common best practices.
# Usage: ./strict-mode-initializer.sh [project_name]
#        If project_name is not provided, it initializes in the current directory.

set -euo pipefail

# --- Configuration Variables ---
# These can be overridden by environment variables or command-line flags in a more complex script.
DEFAULT_PROJECT_NAME=""
TSCONFIG_CONTENT='''
{
  "compilerOptions": {
    "target": "es2021",
    "module": "commonjs",
    "lib": ["es2021", "dom"],
    "strict": true, /* Enable all strict type-checking options */
    "esModuleInterop": true, /* Emit additional JavaScript to ease support for importing CommonJS modules. This enables `allowSyntheticDefaultImports` for type compatibility. */
    "skipLibCheck": true, /* Skip type checking all .d.ts files. */
    "forceConsistentCasingInFileNames": true, /* Ensure that casing is correct in imports. */
    "moduleResolution": "node", /* Resolve modules using Node.js style */
    "outDir": "./dist", /* Specify an output folder for all emitted files. */
    "rootDir": "./src", /* Specify the root folder within your source files. */
    "declaration": true, /* Generate .d.ts files for your modules. */
    "sourceMap": true, /* Create source map files for emitted JavaScript files. */
    "noEmitOnError": true, /* Do not emit outputs if any errors were reported. */
    "noUncheckedIndexedAccess": true, /* Add '| undefined' to index signatures for objects with no explicit index signatures. */
    "exactOptionalPropertyTypes": true, /* Report errors for optional properties that are not explicitly undefined. */
    "noImplicitOverride": true, /* Ensure overriding members are marked with an 'override' modifier. */
    "noImplicitReturns": true, /* Report error when not all code paths in a function return a value. */
    "useUnknownInCatchVariables": true /* Type catch clause variables as 'unknown' instead of 'any'. */
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
'''

# --- Helper Functions ---
log_info() {
  echo -e "\033[0;34m[INFO]\033[0m $1"
}

log_success() {
  echo -e "\033[0;32m[SUCCESS]\033[0m $1"
}

log_error() {
  echo -e "\033[0;31m[ERROR]\033[0m $1" >&2
  exit 1
}

# --- Main Logic ---
main() {
  local project_dir="$(pwd)"
  local project_name="$DEFAULT_PROJECT_NAME"

  if [[ -n "$1" ]]; then
    project_name="$1"
    project_dir="$project_name"
  fi

  if [[ -n "$project_name" && ! -d "$project_dir" ]]; then
    log_info "Creating project directory: $project_dir"
    mkdir -p "$project_dir" || log_error "Failed to create directory $project_dir"
  fi

  cd "$project_dir" || log_error "Failed to change to directory $project_dir"

  log_info "Initializing new TypeScript project in $(pwd)"

  # Check if package.json exists, if not, initialize npm
  if [[ ! -f "package.json" ]]; then
    log_info "No package.json found. Initializing npm..."
    npm init -y > /dev/null || log_error "Failed to initialize npm."
    log_success "npm initialized."
  else
    log_info "package.json already exists. Skipping npm init."
  fi

  # Install TypeScript if not already installed
  if ! npm list typescript &> /dev/null; then
    log_info "TypeScript not found. Installing TypeScript..."
    npm install --save-dev typescript > /dev/null || log_error "Failed to install TypeScript."
    log_success "TypeScript installed."
  else
    log_info "TypeScript already installed. Skipping installation."
  fi

  # Create src directory
  if [[ ! -d "src" ]]; then
    log_info "Creating src/ directory..."
    mkdir -p src || log_error "Failed to create src/ directory."
    log_success "src/ directory created."
  else
    log_info "src/ directory already exists. Skipping creation."
  fi

  # Create tsconfig.json
  if [[ ! -f "tsconfig.json" ]]; then
    log_info "Creating tsconfig.json with strict mode configuration..."
    echo "$TSCONFIG_CONTENT" > tsconfig.json || log_error "Failed to write tsconfig.json"
    log_success "tsconfig.json created with strict mode enabled."
  else
    log_info "tsconfig.json already exists. Skipping creation. Please review its content manually."
  fi

  # Create a sample index.ts file
  if [[ ! -f "src/index.ts" ]]; then
    log_info "Creating a sample src/index.ts file..."
    echo 'function greet(name: string): void {
  console.log(`Hello, ${name.toUpperCase()}!`);
}

greet("World");
// greet(null); // Uncomment to see strictNullChecks error
' > src/index.ts || log_error "Failed to write src/index.ts"
    log_success "Sample src/index.ts created."
  else
    log_info "src/index.ts already exists. Skipping creation."
  fi

  log_success "TypeScript strict mode project initialization complete!"
  log_info "To compile, run: npx tsc"
  log_info "To run the compiled code: node dist/index.js"
}

# --- Script Entry Point ---
main "$@"
