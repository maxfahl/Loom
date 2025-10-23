#!/usr/bin/env python3

# tf-module-version-updater.py
#
# Purpose:
#   Updates the version constraint of a specified Terraform module within a root
#   Terraform configuration file (e.g., main.tf). This script helps manage
#   module dependencies and ensures that configurations use desired module versions.
#
# Usage:
#   python3 tf-module-version-updater.py <config_file> <module_name> <new_version> [--dry-run]
#
# Arguments:
#   <config_file> : The path to the root Terraform configuration file (e.g., "main.tf").
#   <module_name> : The name of the module to update (as defined in the 'module' block).
#   <new_version> : The new version constraint to set (e.g., "~> 1.2.0", "1.3.0").
#   --dry-run     : Optional. If present, the script will only print the changes
#                   it would make without actually modifying the file.
#
# Example:
#   python3 tf-module-version-updater.py main.tf my-vpc-module "~> 2.0.0"
#   python3 tf-module-version-updater.py prod/main.tf aws-s3-bucket "1.0.5" --dry-run
#
# Configuration:
#   None.
#
# Error Handling:
#   - Exits if incorrect number of arguments are provided.
#   - Exits if the specified config file does not exist.
#   - Reports if the module or version attribute is not found.
#   - Provides informative messages for all actions.

import argparse
import re
import sys

# --- Colors for better readability ---
class Colors:
    GREEN = '\033[0;32m'
    YELLOW = '\033[0;33m'
    RED = '\033[0;31m'
    BLUE = '\033[0;34m'
    NC = '\033[0m' # No Color

def log_info(message):
    print(f"{Colors.GREEN}[INFO]{Colors.NC} {message}")

def log_warn(message):
    print(f"{Colors.YELLOW}[WARN]{Colors.NC} {message}")

def log_error(message):
    print(f"{Colors.RED}[ERROR]{Colors.NC} {message}", file=sys.stderr)
    sys.exit(1)

def update_module_version(config_file, module_name, new_version, dry_run):
    """
    Updates the version constraint of a specified Terraform module in a config file.
    """
    try:
        with open(config_file, 'r') as f:
            content = f.readlines()
    except FileNotFoundError:
        log_error(f"Configuration file '{config_file}' not found.")

    updated_content = []
    module_found = False
    version_updated = False
    in_module_block = False
    module_block_indent = 0

    # Regex to find module block start: module "module_name" {
    module_start_pattern = re.compile(r'^\s*module\s+"' + re.escape(module_name) + r'"\s*{")
    # Regex to find version attribute: version = "..."
    version_pattern = re.compile(r'^\s*(version\s*=\s*).*(?<!\\)"(.*)(?<!\\)"') # Handles escaped quotes

    for i, line in enumerate(content):
        if not in_module_block:
            match = module_start_pattern.match(line)
            if match:
                log_info(f"Found module '{module_name}' at line {i + 1}.")
                module_found = True
                in_module_block = True
                module_block_indent = len(line) - len(line.lstrip())
                updated_content.append(line)
                continue
        elif in_module_block:
            current_indent = len(line) - len(line.lstrip())
            if current_indent <= module_block_indent and line.strip() == '}': # End of module block
                in_module_block = False
                updated_content.append(line)
                continue

            match = version_pattern.match(line)
            if match:
                current_version = match.group(2)
                if current_version != new_version:
                    log_info(f"Updating version for module '{module_name}' from '{current_version}' to '{new_version}'.")
                    new_line = f"{match.group(1)}\"{new_version}\"\n"
                    updated_content.append(new_line)
                    version_updated = True
                else:
                    log_warn(f"Version for module '{module_name}' is already '{new_version}'. No change needed.")
                    updated_content.append(line)
                in_module_block = False # Assume version is usually one of the last attributes or we only care about the first one
                continue
        updated_content.append(line)

    if not module_found:
        log_error(f"Module '{module_name}' not found in '{config_file}'.")

    if not version_updated and module_found:
        log_warn(f"Version attribute for module '{module_name}' not found or already up-to-date in '{config_file}'.")
        log_warn("If the version attribute is missing, you might need to add it manually.")

    if version_updated:
        if dry_run:
            log_info("Dry run: The following changes would be applied:")
            print("".join(updated_content))
        else:
            try:
                with open(config_file, 'w') as f:
                    f.writelines(updated_content)
                log_info(f"Successfully updated module '{module_name}' version in '{config_file}'.")
            except IOError:
                log_error(f"Failed to write to file '{config_file}'. Check permissions.")
    else:
        log_info("No changes were applied.")

def main():
    parser = argparse.ArgumentParser(
        description="Update the version constraint of a Terraform module in a configuration file.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "config_file",
        help="The path to the root Terraform configuration file (e.g., 'main.tf')."
    )
    parser.add_argument(
        "module_name",
        help="The name of the module to update (as defined in the 'module' block)."
    )
    parser.add_argument(
        "new_version",
        help="The new version constraint to set (e.g., '~> 1.2.0', '1.3.0')."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="If present, the script will only print the changes it would make without actually modifying the file."
    )

    args = parser.parse_args()

    update_module_version(args.config_file, args.module_name, args.new_version, args.dry_run)

if __name__ == "__main__":
    main()
