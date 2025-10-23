#!/bin/bash
#
# setup-prettier.sh: Initializes a project with Prettier and best-practice defaults.
#
# This script automates the following:
# 1. Installs `prettier` as an exact dev dependency.
# 2. Creates a `.prettierrc.json` file with recommended settings.
# 3. Creates a `.prettierignore` file with sensible defaults.
# 4. Adds `format` and `check:format` scripts to `package.json`.

set -e # Exit immediately if a command exits with a non-zero status.

# --- Color Codes ---
COLOR_GREEN="\033[0;32m"
COLOR_YELLOW="\033[0;33m"
COLOR_RED="\033[0;31m"
COLOR_RESET="\033[0m"

# --- Helper Functions ---
function print_success() {
  echo -e "${COLOR_GREEN}✅ $1${COLOR_RESET}"
}

function print_warning() {
  echo -e "${COLOR_YELLOW}⚠️ $1${COLOR_RESET}"
}

function print_error() {
  echo -e "${COLOR_RED}❌ $1${COLOR_RESET}"
  exit 1
}

# --- Main Logic ---

# 1. Check for package.json
if [ ! -f "package.json" ]; then
  print_error "No package.json found. Please run 'npm init' first."
fi

# 2. Install Prettier
print_warning "Installing Prettier as a dev dependency..."
npm install --save-dev --save-exact prettier
print_success "Prettier installed successfully."

# 3. Create .prettierrc.json
PRETTIER_CONFIG_PATH=".prettierrc.json"
if [ -f "$PRETTIER_CONFIG_PATH" ]; then
  print_warning "'.prettierrc.json' already exists. Skipping creation."
else
  echo '{
  "semi": true,
  "singleQuote": true,
  "trailingComma": "es5",
  "tabWidth": 2,
  "printWidth": 80
}' > $PRETTIER_CONFIG_PATH
  print_success "Created '.prettierrc.json' with recommended settings."
fi

# 4. Create .prettierignore
PRETTIER_IGNORE_PATH=".prettierignore"
if [ -f "$PRETTIER_IGNORE_PATH" ]; then
  print_warning "'.prettierignore' already exists. Skipping creation."
else
  echo "# Ignore artifacts
node_modules
coverage
dist
build

# Ignore package manager files
package-lock.json
yarn.lock
pnpm-lock.yaml

# Ignore environment files
.env*
" > $PRETTIER_IGNORE_PATH
  print_success "Created '.prettierignore' with default entries."
fi

# 5. Add scripts to package.json
# Using python to safely edit JSON (jq is not always available)
python -c "
import json

with open('package.json', 'r+') as f:
    data = json.load(f)
    if 'scripts' not in data:
        data['scripts'] = {}
    data['scripts']['format'] = 'prettier --write .'
    data['scripts']['check:format'] = 'prettier --check .'
    f.seek(0)
    json.dump(data, f, indent=2)
    f.truncate()
"
print_success "Added 'format' and 'check:format' scripts to package.json."

print_success "Prettier setup complete!"
