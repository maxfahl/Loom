#!/bin/bash

# generate-workflow-boilerplate.sh
#
# Purpose:
#   Scaffolds a new GitHub Actions workflow file (.yml) with a basic structure,
#   including common jobs like build, test, and deploy, and incorporating
#   best practices such as action version pinning and caching.
#
# Usage:
#   ./generate-workflow-boilerplate.sh <workflow_name> [--type <ci|cd|full>] [--dry-run]
#
# Arguments:
#   <workflow_name> : The name of the new workflow file (e.g., "nodejs-ci").
#                     The script will create a file named <workflow_name>.yml.
#   --type          : Optional. Specifies the type of workflow to generate.
#                     - 'ci' (default): Basic CI workflow (build, test).
#                     - 'cd': Basic CD workflow (deploy).
#                     - 'full': CI/CD workflow (build, test, deploy).
#   --dry-run       : Optional. If present, the script will only print the actions
#                     it would take without actually creating any files.
#
# Example:
#   ./generate-workflow-boilerplate.sh my-app-ci
#   ./generate-workflow-boilerplate.sh deploy-prod --type cd
#   ./generate-workflow-boilerplate.sh full-pipeline --type full --dry-run
#
# Configuration:
#   None directly. Workflow content can be customized by editing the script.
#
# Error Handling:
#   - Exits if no workflow name is provided.
#   - Exits if the workflow file already exists.
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

WORKFLOW_NAME=""
WORKFLOW_TYPE="ci"
DRY_RUN=false

# Parse arguments
while [[ $# -gt 0 ]]; do
  case "$1" in
    --type)
      shift
      WORKFLOW_TYPE="$1"
      if [[ "$WORKFLOW_TYPE" != "ci" && "$WORKFLOW_TYPE" != "cd" && "$WORKFLOW_TYPE" != "full" ]]; then
        log_error "Invalid workflow type: $WORKFLOW_TYPE. Must be 'ci', 'cd', or 'full'."
      fi
      ;;
    --dry-run)
      DRY_RUN=true
      ;;
    *)
      if [[ -z "$WORKFLOW_NAME" ]]; then
        WORKFLOW_NAME="$1"
      else
        log_error "Unknown argument: $1"
      fi
      ;;
  esac
  shift
done

if [[ -z "$WORKFLOW_NAME" ]]; then
  log_error "Usage: $0 <workflow_name> [--type <ci|cd|full>] [--dry-run]"
fi

WORKFLOW_DIR=".github/workflows"
WORKFLOW_FILE="$WORKFLOW_DIR/$WORKFLOW_NAME.yml"

if "$DRY_RUN"; then
  log_warn "Dry run enabled. No files will be created."
fi

log_info "Scaffolding new GitHub Actions workflow: '$WORKFLOW_NAME.yml' (Type: $WORKFLOW_TYPE)..."

if [[ -f "$WORKFLOW_FILE" ]]; then
  log_error "Workflow file '$WORKFLOW_FILE' already exists. Aborting."
fi

# Create workflow directory
if "$DRY_RUN"; then
  log_info "Would create directory: $WORKFLOW_DIR"
else
  mkdir -p "$WORKFLOW_DIR" || log_error "Failed to create directory '$WORKFLOW_DIR'."
  log_info "Created directory: $WORKFLOW_DIR"
fi

# --- Workflow Content ---
WORKFLOW_CONTENT="name: ${WORKFLOW_NAME}\n\non:\n  push:\n    branches:\n      - main\n  pull_request:\n    branches:\n      - main\n  workflow_dispatch:\n\njobs:\n"

if [[ "$WORKFLOW_TYPE" == "ci" || "$WORKFLOW_TYPE" == "full" ]]; then
  WORKFLOW_CONTENT+="  build:\n    runs-on: ubuntu-22.04\n    steps:\n      - name: Checkout code\n        uses: actions/checkout@a81eb75e2b2a0f13038f3d79a26232f9679b33cd # Pin to specific SHA\n      - name: Setup Node.js\n        uses: actions/setup-node@64ed1c7eab4cce3362f2c96964c0867f10b380f8 # Pin to specific SHA\n        with:\n          node-version: '18'\n      - name: Cache Node.js modules\n        uses: actions/cache@v3\n        with:\n          path: ~/.npm\n          key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
          restore-keys: |\n            ${{ runner.os }}-node-
      - name: Install dependencies\n        run: npm ci\n      - name: Build project\n        run: npm run build\n\n  test:\n    needs: build\n    runs-on: ubuntu-22.04\n    steps:\n      - name: Checkout code\n        uses: actions/checkout@a81eb75e2b2a0f13038f3d79a26232f9679b33cd # Pin to specific SHA\n      - name: Setup Node.js\n        uses: actions/setup-node@64ed1c7eab4cce3362f2c96964c0867f10b380f8 # Pin to specific SHA\n        with:\n          node-version: '18'\n      - name: Cache Node.js modules\n        uses: actions/cache@v3\n        with:\n          path: ~/.npm\n          key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
          restore-keys: |\n            ${{ runner.os }}-node-
      - name: Install dependencies\n        run: npm ci\n      - name: Run tests\n        run: npm test\n"
fi

if [[ "$WORKFLOW_TYPE" == "cd" || "$WORKFLOW_TYPE" == "full" ]]; then
  WORKFLOW_CONTENT+="  deploy:\n    needs: [build, test] # Depends on build and test jobs\n    runs-on: ubuntu-22.04\n    if: github.ref == 'refs/heads/main' && github.event_name == 'push' # Only deploy on push to main\n    environment: production # Example environment\n    steps:\n      - name: Checkout code\n        uses: actions/checkout@a81eb75e2b2a0f13038f3d79a26232f9679b33cd # Pin to specific SHA\n      - name: Configure AWS Credentials\n        uses: aws-actions/configure-aws-credentials@v4 # Pin to specific SHA\n        with:\n          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1\n      - name: Deploy application\n        run: |\n          echo "Deploying application to production..."\n          # Add your deployment commands here, e.g.,\n          # aws s3 sync ./build s3://your-prod-bucket\n          # aws cloudfront create-invalidation --distribution-id YOUR_DISTRIBUTION_ID --paths "/*"\n"
fi

# Write workflow content to file
if "$DRY_RUN"; then
  log_info "Would create file: $WORKFLOW_FILE"
  echo "$WORKFLOW_CONTENT"
else
  echo "$WORKFLOW_CONTENT" > "$WORKFLOW_FILE" || log_error "Failed to create workflow file '$WORKFLOW_FILE'."
  log_info "Created workflow file: $WORKFLOW_FILE"
fi

log_info "GitHub Actions workflow '$WORKFLOW_NAME.yml' boilerplate generation complete."
log_info "Remember to replace placeholder SHAs with actual SHAs for actions and customize the workflow content."
