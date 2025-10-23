#!/bin/bash

# nest-feature-module-setup.sh
# Description: Automates the creation of a new NestJS feature module, including its dedicated directory,
#              module file, controller, and service, and registers it in the root app.module.ts.
#
# Usage:
#   bash nest-feature-module-setup.sh <feature-name>
#
# Arguments:
#   <feature-name>: The name of the new feature module (kebab-case, e.g., user-management).
#
# Features:
# - Creates a new directory for the feature module under src/.
# - Generates module, controller, and service files using NestJS CLI commands.
# - Automatically imports and adds the new module to the imports array of src/app.module.ts.
#
# Error Handling:
# - Exits if feature name is not provided.
# - Exits if NestJS CLI is not installed or project is not a NestJS project.
# - Checks for successful command execution.
#
# Configuration:
# - Assumes NestJS project structure with src/app.module.ts.

set -e # Exit immediately if a command exits with a non-zero status.

FEATURE_NAME_KEBAB=$1

# --- Helper Functions ---
log_info() {
  echo -e "\033[0;34m[INFO]\033[0m $1"
}

log_success() {
  echo -e "\033[0;32m[SUCCESS]\033[0m $1"
}

log_error() {
  echo -e "\033[0;31m[ERROR]\033[0m $1"
  exit 1
}

# Function to convert kebab-case to PascalCase
to_pascal_case() {
  echo "$1" | sed -r 's/(^|-)([a-z])/UG2/g'
}

# --- Main Script Logic ---

if [ -z "$FEATURE_NAME_KEBAB" ]; then
  log_error "Usage: bash nest-feature-module-setup.sh <feature-name>"
fi

# Check if NestJS CLI is available
if ! command -v nest &> /dev/null
then
    log_error "NestJS CLI (nest command) not found. Please install it globally: npm i -g @nestjs/cli"
fi

# Check if this is a NestJS project (by looking for nest-cli.json or src/app.module.ts)
if [ ! -f "nest-cli.json" ] && [ ! -f "src/app.module.ts" ]; then
  log_error "Not a NestJS project. Please run this script in the root of a NestJS project."
fi

FEATURE_NAME_PASCAL=$(to_pascal_case "$FEATURE_NAME_KEBAB")
MODULE_CLASS_NAME="${FEATURE_NAME_PASCAL}Module"
MODULE_PATH="src/${FEATURE_NAME_KEBAB}/${FEATURE_NAME_KEBAB}.module.ts"
APP_MODULE_PATH="src/app.module.ts"

log_info "Setting up new NestJS feature module: ${FEATURE_NAME_KEBAB}"

# 1. Generate the module, controller, and service using NestJS CLI
log_info "Generating ${FEATURE_NAME_KEBAB} module, controller, and service..."
nest g module "${FEATURE_NAME_KEBAB}" || log_error "Failed to generate module."
nest g controller "${FEATURE_NAME_KEBAB}" --no-spec -d "src/${FEATURE_NAME_KEBAB}" || log_error "Failed to generate controller."
nest g service "${FEATURE_NAME_KEBAB}" --no-spec -d "src/${FEATURE_NAME_KEBAB}" || log_error "Failed to generate service."

# 2. Update the generated module to include controller and service
log_info "Updating ${FEATURE_NAME_KEBAB}.module.ts to include controller and service..."
MODULE_FILE="src/${FEATURE_NAME_KEBAB}/${FEATURE_NAME_KEBAB}.module.ts"

# Add imports for controller and service
sed -i '' "/import { Module } from '@nestjs\/common';/a\nimport { ${FEATURE_NAME_PASCAL}Controller } from './${FEATURE_NAME_KEBAB}.controller';\nimport { ${FEATURE_NAME_PASCAL}Service } from './${FEATURE_NAME_KEBAB}.service';" "$MODULE_FILE" || log_error "Failed to add imports to module file."

# Add controller to @Module() decorator
sed -i '' "/controllers: \[ \]/c\    controllers: [${FEATURE_NAME_PASCAL}Controller]," "$MODULE_FILE" || log_error "Failed to add controller to module."

# Add service to @Module() decorator and export it
sed -i '' "/providers: \[ \]/c\    providers: [${FEATURE_NAME_PASCAL}Service],\n    exports: [${FEATURE_NAME_PASCAL}Service]," "$MODULE_FILE" || log_error "Failed to add service to module."

log_success "${FEATURE_NAME_KEBAB}.module.ts updated."

# 3. Import and register the new module in app.module.ts
log_info "Importing and registering ${MODULE_CLASS_NAME} in ${APP_MODULE_PATH}..."

# Add import statement to app.module.ts
sed -i '' "/import { Module } from '@nestjs\/common';/a\nimport { ${MODULE_CLASS_NAME} } from './${FEATURE_NAME_KEBAB}/${FEATURE_NAME_KEBAB}.module';" "$APP_MODULE_PATH" || log_error "Failed to add module import to app.module.ts."

# Add module to imports array in app.module.ts
sed -i '' "/imports: \[ \]/c\    imports: [${MODULE_CLASS_NAME}],