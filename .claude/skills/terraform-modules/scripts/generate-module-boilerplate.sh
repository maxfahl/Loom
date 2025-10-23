#!/bin/bash

# generate-module-boilerplate.sh
#
# Purpose:
#   Scaffolds a new Terraform module with recommended directory structure and basic files.
#   This script helps developers quickly set up a new module, ensuring consistency
#   and adherence to best practices from the start.
#
# Usage:
#   ./generate-module-boilerplate.sh <module_name> [--dry-run]
#
# Arguments:
#   <module_name> : The name of the new Terraform module (e.g., "aws-s3-bucket").
#   --dry-run     : Optional. If present, the script will only print the actions
#                   it would take without actually creating any files or directories.
#
# Example:
#   ./generate-module-boilerplate.sh my-new-module
#   ./generate-module-boilerplate.sh vpc-module --dry-run
#
# Configuration:
#   None directly. Module content can be customized by editing the script.
#
# Error Handling:
#   - Exits if no module name is provided.
#   - Exits if the module directory already exists.
#   - Provides informative messages for all actions.

set -euo pipefail

# --- Colors for better readability ---
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# --- Functions ---

log_info() {
  echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
  echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
  echo -e "${RED}[ERROR]${NC} $1" >&2
  exit 1
}

# --- Main Script Logic ---

MODULE_NAME=""
DRY_RUN=false

# Parse arguments
for arg in "$@"; do
  case $arg in
    --dry-run)
      DRY_RUN=true
      shift
      ;;
    *)
      if [[ -z "$MODULE_NAME" ]]; then
        MODULE_NAME="$arg"
      else
        log_error "Unknown argument: $arg"
      fi
      shift
      ;;
  esac
done

if [[ -z "$MODULE_NAME" ]]; then
  log_error "Usage: $0 <module_name> [--dry-run]"
fi

MODULE_DIR="./$MODULE_NAME"

if [[ -d "$MODULE_DIR" ]]; then
  log_error "Module directory '$MODULE_DIR' already exists. Aborting."
fi

log_info "Scaffolding new Terraform module: '$MODULE_NAME'..."
if "$DRY_RUN"; then
  log_warn "Dry run enabled. No files will be created."
fi

# Create main module directory
if "$DRY_RUN"; then
  log_info "Would create directory: $MODULE_DIR"
else
  mkdir -p "$MODULE_DIR" || log_error "Failed to create directory '$MODULE_DIR'."
  log_info "Created directory: $MODULE_DIR"
fi

# Create subdirectories
for sub_dir in "examples" "patterns" "scripts"; do
  if "$DRY_RUN"; then
    log_info "Would create directory: $MODULE_DIR/$sub_dir"
  else
    mkdir -p "$MODULE_DIR/$sub_dir" || log_error "Failed to create directory '$MODULE_DIR/$sub_dir'."
    log_info "Created directory: $MODULE_DIR/$sub_dir"
  fi
done

# Create core Terraform files
declare -A tf_files
tf_files["main.tf"]="
# Main resources for the ${MODULE_NAME} module
"
tf_files["variables.tf"]="
# Input variables for the ${MODULE_NAME} module

variable \"name_prefix\" {
  description = \"A prefix to add to resource names.\"
  type        = string
  default     = \"\"
}
"
tf_files["outputs.tf"]="
# Output values for the ${MODULE_NAME} module

output \"module_name\" {
  description = \"The name of the module.\"
  value       = \"${MODULE_NAME}\" 
}
"
tf_files["versions.tf"]="
# Terraform and provider version constraints

terraform {
  required_version = \">= 1.0.0\"

  required_providers {
    aws = {
      source  = \"hashicorp/aws\"
      version = \"~> 5.0\"
    }
    # Add other providers as needed
  }
}
"
tf_files["README.md"]="
# Terraform Module: ${MODULE_NAME}

This module provisions X, Y, and Z.

## Usage

```terraform
module \"${MODULE_NAME}\" {
  source = \"./modules/${MODULE_NAME}\" # Or your module source

  # Required variables
  # name_prefix = \"my-app-\" 

  # Optional variables
  # ...
}
```

## Requirements

| Name | Version |
|------|---------|
| <a name=\"requirement_terraform\"></a> [terraform](#requirement_terraform) | >= 1.0.0 |
| <a name=\"requirement_aws\"></a> [aws](#requirement_aws) | ~> 5.0 |

## Providers

| Name | Version |
|------|---------|
| <a name=\"provider_aws\"></a> [aws](#provider_aws) | ~> 5.0 |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name=\"input_name_prefix\"></a> [name_prefix](#input_name_prefix) | A prefix to add to resource names. | `string` | `""` | no |

## Outputs

| Name | Description |
|------|-------------|
| <a name=\"output_module_name\"></a> [module_name](#output_module_name) | The name of the module. |
"

for tf_file in "${!tf_files[@]}"; do
  FILE_PATH="$MODULE_DIR/$tf_file"
  if "$DRY_RUN"; then
    log_info "Would create file: $FILE_PATH"
  else
    echo "${tf_files[$tf_file]}" > "$FILE_PATH" || log_error "Failed to create file '$FILE_PATH'."
    log_info "Created file: $FILE_PATH"
  fi
done

# Create example main.tf
EXAMPLE_DIR="$MODULE_DIR/examples/basic-usage"
if "$DRY_RUN"; then
  log_info "Would create directory: $EXAMPLE_DIR"
else
  mkdir -p "$EXAMPLE_DIR" || log_error "Failed to create directory '$EXAMPLE_DIR'."
  log_info "Created directory: $EXAMPLE_DIR"
fi

EXAMPLE_MAIN_TF_CONTENT="
# Example usage of the ${MODULE_NAME} module

module \"${MODULE_NAME}_example\" {
  source = \"../../\" # Adjust path if module is in a different location

  name_prefix = \"example-\" 
}

output \"example_module_name\" {
  value = module.${MODULE_NAME}_example.module_name
}
"
if "$DRY_RUN"; then
  log_info "Would create file: $EXAMPLE_DIR/main.tf"
else
  echo "$EXAMPLE_MAIN_TF_CONTENT" > "$EXAMPLE_DIR/main.tf" || log_error "Failed to create file '$EXAMPLE_DIR/main.tf'."
  log_info "Created file: $EXAMPLE_DIR/main.tf"
fi

log_info "Module '$MODULE_NAME' boilerplate generation complete."
if ! "$DRY_RUN"; then
  log_info "Next steps: cd $MODULE_DIR && terraform init"
fi
