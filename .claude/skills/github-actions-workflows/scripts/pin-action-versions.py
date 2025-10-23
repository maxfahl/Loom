#!/usr/bin/env python3

# pin-action-versions.py
#
# Purpose:
#   Automatically updates GitHub Actions references in a workflow file to use
#   specific commit SHAs instead of floating tags (e.g., @v3) or branches (e.g., @main).
#   This enhances security and ensures workflow stability by preventing unexpected
#   changes from action updates.
#
# Usage:
#   python3 pin-action-versions.py <workflow_file> [--dry-run]
#
# Arguments:
#   <workflow_file> : The path to the GitHub Actions workflow YAML file.
#   --dry-run       : Optional. If present, the script will only print the changes
#                     it would make without actually modifying the file.
#
# Example:
#   python3 pin-action-versions.py .github/workflows/ci.yml
#   python3 pin-action-versions.py .github/workflows/deploy.yml --dry-run
#
# Configuration:
#   - Requires a GitHub Personal Access Token (PAT) with 'repo' scope.
#     Set it as an environment variable: export GITHUB_TOKEN="YOUR_PAT"
#   - Requires 'PyYAML' and 'requests' Python packages:
#     pip install PyYAML requests
#
# Error Handling:
#   - Exits if GITHUB_TOKEN environment variable is not set.
#   - Exits if the workflow file does not exist or is not a valid YAML.
#   - Reports if an action's SHA cannot be retrieved.
#   - Provides informative messages for all actions.

import argparse
import os
import re
import sys
import yaml
import requests

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

def get_github_sha(action_ref, github_token):
    """
    Fetches the latest commit SHA for a given GitHub Action reference.
    action_ref format: 'owner/repo@version' (e.g., 'actions/checkout@v3')
    """
    parts = action_ref.split('@')
    if len(parts) != 2:
        log_warn(f"Invalid action reference format: {action_ref}. Skipping.")
        return None

    owner_repo = parts[0]
    version_tag = parts[1]
    owner, repo = owner_repo.split('/')

    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json"
    }

    # Try to get SHA for a tag or branch
    url = f"https://api.github.com/repos/{owner}/{repo}/git/ref/tags/{version_tag}"
    response = requests.get(url, headers=headers)
    if response.status_code == 404: # Not a tag, try as a branch
        url = f"https://api.github.com/repos/{owner}/{repo}/git/ref/heads/{version_tag}"
        response = requests.get(url, headers=headers)

    if response.status_code == 200:
        ref_data = response.json()
        if 'object' in ref_data and 'sha' in ref_data['object']:
            return ref_data['object']['sha']
        elif 'sha' in ref_data: # For branch refs, sha is directly in the ref_data
            return ref_data['sha']
    elif response.status_code == 403:
        log_error(f"GitHub API rate limit exceeded or token permissions insufficient. Response: {response.json()}")
    else:
        log_warn(f"Could not retrieve SHA for '{action_ref}'. Status: {response.status_code}, Response: {response.json()}")
    return None

def pin_action_versions(workflow_file, dry_run):
    """
    Reads a GitHub Actions workflow file, pins action versions to SHAs, and writes back.
    """
    github_token = os.environ.get("GITHUB_TOKEN")
    if not github_token:
        log_error("GITHUB_TOKEN environment variable not set. Please set it to a GitHub Personal Access Token with 'repo' scope.")

    try:
        with open(workflow_file, 'r') as f:
            workflow_content = f.read()
            workflow_data = yaml.safe_load(workflow_content)
    except FileNotFoundError:
        log_error(f"Workflow file '{workflow_file}' not found.")
    except yaml.YAMLError as e:
        log_error(f"Error parsing YAML in '{workflow_file}': {e}")

    if not workflow_data or 'jobs' not in workflow_data:
        log_warn(f"No jobs found in workflow file '{workflow_file}'. Skipping.")
        return

    updated_workflow_content = workflow_content
    changes_made = False

    # Use regex to find 'uses:' lines and replace them
    # This approach preserves comments and original formatting better than re-dumping YAML
    # Regex: ^(\s*-\s*uses:\s*)([^#\s]+)(.*)$
    # Group 1: indentation and '- uses:'
    # Group 2: action reference (e.g., actions/checkout@v3)
    # Group 3: any trailing comments
    uses_pattern = re.compile(r'^(\s*-\s*uses:\s*)([^#\s]+)(.*)$', re.MULTILINE)

    for match in uses_pattern.finditer(workflow_content):
        full_line = match.group(0)
        indent_uses = match.group(1)
        action_ref = match.group(2).strip()
        trailing_comment = match.group(3)

        if '@' not in action_ref:
            log_warn(f"Action '{action_ref}' does not specify a version. Skipping pinning.")
            continue

        current_version = action_ref.split('@')[1]
        if re.match(r'^[0-9a-f]{40}$', current_version):
            log_info(f"Action '{action_ref}' is already pinned to a SHA. Skipping.")
            continue

        log_info(f"Attempting to pin action: {action_ref}")
        sha = get_github_sha(action_ref, github_token)

        if sha:
            new_action_ref = f"{action_ref.split('@')[0]}@{sha}"
            log_info(f"Resolved '{action_ref}' to '{new_action_ref}'")
            new_line = f"{indent_uses}{new_action_ref}{trailing_comment}"
            updated_workflow_content = updated_workflow_content.replace(full_line, new_line)
            changes_made = True
        else:
            log_warn(f"Failed to get SHA for '{action_ref}'. Keeping original reference.")

    if changes_made:
        if dry_run:
            log_info("Dry run: The following changes would be applied:")
            print(updated_workflow_content)
        else:
            try:
                with open(workflow_file, 'w') as f:
                    f.write(updated_workflow_content)
                log_info(f"Successfully updated action versions in '{workflow_file}'.")
            except IOError:
                log_error(f"Failed to write to file '{workflow_file}'. Check permissions.")
    else:
        log_info("No pinnable action versions found or no changes needed.")

def main():
    parser = argparse.ArgumentParser(
        description="Automatically pins GitHub Actions versions to commit SHAs in a workflow file.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "workflow_file",
        help="The path to the GitHub Actions workflow YAML file (e.g., '.github/workflows/ci.yml')."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="If present, the script will only print the changes it would make without actually modifying the file."
    )

    args = parser.parse_args()

    pin_action_versions(args.workflow_file, args.dry_run)

if __name__ == "__main__":
    main()
