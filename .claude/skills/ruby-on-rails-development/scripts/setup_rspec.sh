#!/bin/bash

# setup_rspec.sh
#
# Description:
#   Automates the setup of RSpec and FactoryBot in a Ruby on Rails project.
#   It adds the necessary gems to the Gemfile, runs bundle install,
#   and initializes RSpec configuration files. Optionally, it can generate
#   a basic spec file for a given model or controller.
#
# Usage:
#   ./setup_rspec.sh [OPTIONS] [MODEL_OR_CONTROLLER_NAME]
#
# Arguments:
#   [MODEL_OR_CONTROLLER_NAME]  Optional. The name of a model or controller
#                                 to generate a basic spec file for (e.g., User, PostsController).
#                                 If omitted, only RSpec setup is performed.
#
# Options:
#   -h, --help           Display this help message.
#   -d, --dry-run        Show what would be done without actually modifying files or running commands.
#
# Example Usage:
#   ./setup_rspec.sh
#   ./setup_rspec.sh User
#   ./setup_rspec.sh ProductsController --dry-run
#
# Production-ready features:
#   - Argument parsing with help text.
#   - Dry-run mode.
#   - Checks for existing RSpec setup to prevent re-initialization.
#   - Adds RSpec and FactoryBot gems to Gemfile.
#   - Runs `bundle install` and `rails generate rspec:install`.
#   - Can generate basic spec files for models/controllers.
#   - Error handling for `rails` and `bundle` commands.
#

# --- Configuration ---
RSPEC_GEMS=(
  "gem 'rspec-rails', '~> 6.0', group: [:development, :test]"
  "gem 'factory_bot_rails', '~> 6.0', group: :test"
  "gem 'shoulda-matchers', '~> 5.0', group: :test" # Optional, but common
)
# ---------------------

# Function to display help message
display_help() {
  echo "Usage: $0 [OPTIONS] [MODEL_OR_CONTROLLER_NAME]"
  echo ""
  echo "Arguments:"
  echo "  [MODEL_OR_CONTROLLER_NAME]  Optional. The name of a model or controller"
  echo "                                to generate a basic spec file for (e.g., User, PostsController)."
  echo "                                If omitted, only RSpec setup is performed."
  echo ""
  echo "Options:"
  echo "  -h, --help           Display this help message."
  echo "  -d, --dry-run        Show what would be done without actually modifying files or running commands."
  echo ""
  echo "Example Usage:"
  echo "  $0"
  echo "  $0 User"
  echo "  $0 ProductsController --dry-run"
  exit 0
}

# Parse arguments
TARGET_NAME=""
DRY_RUN=false

while [[ "$#" -gt 0 ]]; do
  case "$1" in
    -h|--help)
      display_help
      ;;
    -d|--dry-run)
      DRY_RUN=true
      ;;
    *)
      if [[ -z "$TARGET_NAME" ]]; then
        TARGET_NAME="$1"
      else
        echo "Error: Unknown argument or too many arguments: $1" >&2
        display_help
      fi
      ;;
  esac
  shift
done

# Check if `rails` and `bundle` commands are available
check_commands() {
  if ! command -v rails &> /dev/null; then
    echo "Error: 'rails' command not found. Please ensure you are in a Rails project directory and Rails is installed." >&2
    exit 1
  fi
  if ! command -v bundle &> /dev/null; then
    echo "Error: 'bundle' command not found. Please ensure Bundler is installed." >&2
    exit 1
  fi
}

# Function to add gems to Gemfile
add_gems_to_gemfile() {
  local gemfile="Gemfile"
  if [ ! -f "$gemfile" ]; then
    echo "Error: Gemfile not found in the current directory." >&2
    exit 1
  fi

  echo "Adding RSpec and FactoryBot gems to Gemfile..."
  for gem_line in "${RSPEC_GEMS[@]}"; do
    if ! grep -qF "$gem_line" "$gemfile"; then
      if $DRY_RUN; then
        echo "  Would add: $gem_line"
      else
        echo "$gem_line" >> "$gemfile"
        echo "  Added: $gem_line"
      fi
    else
      echo "  Gem already present: $gem_line"
    fi
  done
}

# Main logic
check_commands

if [ -d "spec" ]; then
  echo "RSpec seems to be already installed (spec/ directory exists). Skipping initial setup."
else
  echo "RSpec not detected. Proceeding with installation."
  add_gems_to_gemfile

  if $DRY_RUN; then
    echo "Would run: bundle install"
    echo "Would run: rails generate rspec:install"
  else
    echo "Running bundle install..."
    bundle install || { echo "Error: bundle install failed." >&2; exit 1; }

    echo "Running rails generate rspec:install..."
    rails generate rspec:install || { echo "Error: rails generate rspec:install failed." >&2; exit 1; }
    echo "RSpec installed and configured successfully."
  fi
fi

if [[ -n "$TARGET_NAME" ]]; then
  echo "Generating spec file for $TARGET_NAME..."
  if $DRY_RUN; then
    echo "Would run: rails generate rspec:model $TARGET_NAME" # Simplified, actual command depends on type
  else
    # Attempt to determine if it's a model or controller based on naming convention
    if [[ "$TARGET_NAME" == *"Controller" ]]; then
      rails generate rspec:controller "$(echo "$TARGET_NAME" | sed 's/Controller$//')" || { echo "Error: Failed to generate controller spec." >&2; exit 1; }
    else
      rails generate rspec:model "$TARGET_NAME" || { echo "Error: Failed to generate model spec." >&2; exit 1; }
    fi
    echo "Basic spec file for '$TARGET_NAME' generated."
  fi
fi

if $DRY_RUN; then
  echo "Dry run complete. No changes were made."
else
  echo "RSpec setup complete."
  echo "Remember to customize your spec files and start writing tests!"
fi

exit 0
