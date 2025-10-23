#!/bin/bash

# generate-api-version-boilerplate.sh
#
# Purpose:
#   Scaffolds a new API version directory and basic endpoint files based on a chosen
#   versioning strategy (URI or Header). This script automates the repetitive task
#   of setting up the initial file structure for a new API version, ensuring consistency.
#
# Usage:
#   ./generate-api-version-boilerplate.sh --strategy <uri|header> --version <vX> --resource <resource_name> [--output-dir <path>]
#
# Examples:
#   ./generate-api-version-boilerplate.sh --strategy uri --version v2 --resource users
#   ./generate-api-version-boilerplate.sh --strategy header --version v1 --resource products --output-dir ./src/api
#   ./generate-api-version-boilerplate.sh -s uri -v v3 -r orders
#
# Configuration:
#   - Default output directory is './src/api'. Can be overridden with --output-dir.
#   - Script assumes a TypeScript environment for generated file extensions.
#
# Error Handling:
#   - Exits if required arguments are missing.
#   - Exits if the output directory cannot be created.
#   - Warns if files already exist and skips creation.

set -euo pipefail

# --- Configuration ---
DEFAULT_OUTPUT_DIR="./src/api"
OUTPUT_DIR=""
STRATEGY=""
VERSION=""
RESOURCE=""

# --- Functions ---

# Displays help message
show_help() {
  echo "Usage: $0 --strategy <uri|header> --version <vX> --resource <resource_name> [--output-dir <path>]"
  echo ""
  echo "Purpose: Scaffolds a new API version directory and basic endpoint files."
  echo ""
  echo "Options:"
  echo "  -s, --strategy    Versioning strategy: 'uri' or 'header'."
  echo "  -v, --version     API version (e.g., 'v1', 'v2')."
  echo "  -r, --resource    API resource name (e.g., 'users', 'products')."
  echo "  -o, --output-dir  Optional: Base directory to create the API structure (default: ./src/api)."
  echo "  -h, --help        Display this help message."
  echo ""
  echo "Examples:"
  echo "  $0 --strategy uri --version v2 --resource users"
  echo "  $0 -s header -v v1 -r products -o ./src/api"
  exit 0
}

# Parses command-line arguments
parse_args() {
  while [[ "$#" -gt 0 ]]; do
    case "$1" in
      -s|--strategy) STRATEGY="$2"; shift ;;
      -v|--version) VERSION="$2"; shift ;;
      -r|--resource) RESOURCE="$2"; shift ;;
      -o|--output-dir) OUTPUT_DIR="$2"; shift ;;
      -h|--help) show_help ;;
      *) echo "Unknown parameter: $1"; show_help ;;
    esac
    shift
  done
}

# Validates arguments
validate_args() {
  if [[ -z "$STRATEGY" || -z "$VERSION" || -z "$RESOURCE" ]]; then
    echo "Error: Missing required arguments. Strategy, Version, and Resource are mandatory." >&2
    show_help
  fi

  if [[ "$STRATEGY" != "uri" && "$STRATEGY" != "header" ]]; then
    echo "Error: Invalid strategy. Must be 'uri' or 'header'." >&2
    exit 1
  fi

  if [[ ! "$VERSION" =~ ^v[0-9]+$ ]]; then
    echo "Error: Invalid version format. Must be like 'v1', 'v2', etc." >&2
    exit 1
  fi

  if [[ -z "$OUTPUT_DIR" ]]; then
    OUTPUT_DIR="$DEFAULT_OUTPUT_DIR"
  fi
}

# Creates directory if it doesn't exist
create_dir_if_not_exists() {
  local dir_path="$1"
  if [[ ! -d "$dir_path" ]]; then
    echo "Creating directory: $dir_path"
    mkdir -p "$dir_path" || { echo "Error: Failed to create directory $dir_path" >&2; exit 1; }
  else
    echo "Directory already exists: $dir_path"
  fi
}

# Generates URI versioning boilerplate
generate_uri_boilerplate() {
  local api_dir="${OUTPUT_DIR}/${VERSION}"
  local resource_file="${api_dir}/${RESOURCE}.ts"
  local router_file="${api_dir}/index.ts"

  create_dir_if_not_exists "$api_dir"

  if [[ -f "$resource_file" ]]; then
    echo "Warning: Resource file '$resource_file' already exists. Skipping."
  else
    echo "Creating resource file: $resource_file"
    cat <<EOF > "$resource_file"
// ${RESOURCE}.ts - API v${VERSION} for ${RESOURCE} resource

import { Request, Response } from 'express'; // Example for Express.js

export const get${RESOURCE^} = (req: Request, res: Response) => {
  // Logic to fetch ${RESOURCE} for v${VERSION}
  res.status(200).json({ version: '${VERSION}', resource: '${RESOURCE}', data: [] });
};

export const create${RESOURCE^} = (req: Request, res: Response) => {
  // Logic to create ${RESOURCE} for v${VERSION}
  res.status(201).json({ version: '${VERSION}', resource: '${RESOURCE}', message: '${RESOURCE} created' });
};

// Add other CRUD operations as needed
EOF
  fi

  if [[ -f "$router_file" ]]; then
    echo "Warning: Router file '$router_file' already exists. Skipping."
  else
    echo "Creating router file: $router_file"
    cat <<EOF > "$router_file"
// index.ts - Router for API ${VERSION}

import { Router } from 'express';
import { get${RESOURCE^}, create${RESOURCE^} } from './${RESOURCE}';

const router = Router();

router.get('/${RESOURCE}', get${RESOURCE^});
router.post('/${RESOURCE}', create${RESOURCE^});

// Add other routes for ${RESOURCE} and other resources in v${VERSION}

export default router;
EOF
  fi

  echo "URI versioning boilerplate for ${VERSION}/${RESOURCE} generated successfully in ${api_dir}"
}

# Generates Header versioning boilerplate
generate_header_boilerplate() {
  local api_dir="${OUTPUT_DIR}"
  local resource_file="${api_dir}/${RESOURCE}.ts"
  local middleware_file="${api_dir}/versionMiddleware.ts"

  create_dir_if_not_exists "$api_dir"

  if [[ -f "$resource_file" ]]; then
    echo "Warning: Resource file '$resource_file' already exists. Skipping."
  else
    echo "Creating resource file: $resource_file"
    cat <<EOF > "$resource_file"
// ${RESOURCE}.ts - API logic for ${RESOURCE} resource with header versioning

import { Request, Response, NextFunction } from 'express'; // Example for Express.js

// Example data store (replace with actual database interaction)
const dataV1 = [{ id: 1, name: 'Item A' }];
const dataV2 = [{ id: 1, name: 'Item A', description: 'Description for A' }];

export const get${RESOURCE^} = (req: Request, res: Response) => {
  const requestedVersion = req.headers['x-api-version'] || 'v1'; // Default to v1 if header not present

  if (requestedVersion === 'v2') {
    res.status(200).json({ version: 'v2', resource: '${RESOURCE}', data: dataV2 });
  } else {
    // Default or v1 logic
    res.status(200).json({ version: 'v1', resource: '${RESOURCE}', data: dataV1 });
  }
};

export const create${RESOURCE^} = (req: Request, res: Response) => {
  const requestedVersion = req.headers['x-api-version'] || 'v1';

  if (requestedVersion === 'v2') {
    // v2 creation logic
    res.status(201).json({ version: 'v2', resource: '${RESOURCE}', message: '${RESOURCE} created with v2 logic' });
  } else {
    // v1 creation logic
    res.status(201).json({ version: 'v1', resource: '${RESOURCE}', message: '${RESOURCE} created with v1 logic' });
  }
};

// Add other CRUD operations as needed
EOF
  fi

  if [[ -f "$middleware_file" ]]; then
    echo "Warning: Middleware file '$middleware_file' already exists. Skipping."
  else
    echo "Creating version middleware file: $middleware_file"
    cat <<EOF > "$middleware_file"
// versionMiddleware.ts - Middleware to handle API versioning via headers

import { Request, Response, NextFunction } from 'express';

export const apiVersionMiddleware = (req: Request, res: Response, next: NextFunction) => {
  const requestedVersion = req.headers['x-api-version'];

  if (!requestedVersion) {
    console.warn('X-API-Version header not provided. Defaulting to v1.');
    // Optionally, you could enforce versioning:
    // return res.status(400).json({ error: 'X-API-Version header is required' });
  }

  // You might store the version in res.locals or req.version for later use
  res.locals.apiVersion = requestedVersion || 'v1';
  next();
};
EOF
  fi

  echo "Header versioning boilerplate for ${RESOURCE} (handling ${VERSION}) generated successfully in ${api_dir}"
  echo "Remember to integrate 'apiVersionMiddleware' into your Express app."
}

# --- Main Logic ---
parse_args "$@"
validate_args

echo "Generating API boilerplate..."
echo "Strategy: ${STRATEGY}"
echo "Version: ${VERSION}"
echo "Resource: ${RESOURCE}"
echo "Output Directory: ${OUTPUT_DIR}"

if [[ "$STRATEGY" == "uri" ]]; then
  generate_uri_boilerplate
elif [[ "$STRATEGY" == "header" ]]; then
  generate_header_boilerplate
fi

echo "Boilerplate generation complete."
