#!/usr/bin/env python3

# secrets-sync.py
#
# Purpose:
#   Securely synchronizes environment variables from a local .env file to CI/CD platform secrets
#   (e.g., GitHub Secrets, GitLab CI/CD Variables). This automates the tedious and error-prone
#   manual process of updating secrets.
#
# Usage:
#   python3 secrets-sync.py --owner <repo_owner> --repo <repo_name> [--env-file <path_to_env>] [--dry-run]
#
# Requirements:
#   - PyGithub: pip install PyGithub
#   - python-dotenv: pip install python-dotenv
#
# Configuration:
#   - GITHUB_TOKEN: A GitHub Personal Access Token with 'repo' scope (for private repos)
#                   or 'public_repo' scope (for public repos). Must be set as an
#                   environment variable or passed via --github-token (less secure).
#
# Exit Codes:
#   0: All secrets synchronized successfully or dry-run completed.
#   1: An error occurred during synchronization.

import os
import argparse
import json
from dotenv import load_dotenv
from github import Github
from github.GithubException import UnknownObjectException, BadCredentialsException, GithubException

# --- Colors for better readability ---
RED = "\033[0;31m"
GREEN = "\033[0;32m"
YELLOW = "\033[0;33m"
BLUE = "\033[0;34m"
NC = "\033[0m" # No Color

def log_info(message):
    print(f"{BLUE}[INFO]{NC} {message}")

def log_success(message):
    print(f"{GREEN}[SUCCESS]{NC} {message}")

def log_warn(message):
    print(f"{YELLOW}[WARN]{NC} {message}")

def log_error(message):
    print(f"{RED}[ERROR]{NC} {message}")

def get_github_repo(g, owner, repo_name):
    """Fetches the GitHub repository object."""
    try:
        log_info(f"Attempting to access repository: {owner}/{repo_name}")
        return g.get_user(owner).get_repo(repo_name)
    except UnknownObjectException:
        try:
            return g.get_organization(owner).get_repo(repo_name)
        except UnknownObjectException:
            log_error(f"Repository '{owner}/{repo_name}' not found or you don't have access.")
            return None
    except BadCredentialsException:
        log_error("Bad credentials. Please check your GITHUB_TOKEN.")
        return None
    except GithubException as e:
        log_error(f"GitHub API error: {e}")
        return None

def get_local_secrets(env_file_path):
    """Loads secrets from the .env file."""
    log_info(f"Loading secrets from {env_file_path}")
    if not os.path.exists(env_file_path):
        log_error(f"Error: .env file not found at '{env_file_path}'")
        return None

    # Load .env file into a dictionary
    local_secrets = {}
    with open(env_file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                if '=' in line:
                    key, value = line.split('=', 1)
                    local_secrets[key.strip()] = value.strip()
    return local_secrets

def get_remote_secrets(repo):
    """Fetches existing secrets from the GitHub repository."""
    log_info(f"Fetching existing secrets from GitHub for {repo.full_name}")
    remote_secrets = {}
    try:
        for secret in repo.get_secrets():
            remote_secrets[secret.name] = "********" # Value is not exposed by API
    except GithubException as e:
        log_error(f"Could not fetch remote secrets: {e}")
        return None
    return remote_secrets

def sync_secrets(repo, local_secrets, dry_run):
    """Synchronizes local secrets to GitHub repository secrets."""
    if not local_secrets:
        log_warn("No local secrets found to synchronize.")
        return 0

    remote_secrets_names = {s.name for s in repo.get_secrets()}
    updated_count = 0
    created_count = 0

    for key, value in local_secrets.items():
        if key in remote_secrets_names:
            log_info(f"Updating secret: {key}")
            if not dry_run:
                try:
                    repo.create_secret(key, value)
                    log_success(f"  Secret '{key}' updated.")
                    updated_count += 1
                except GithubException as e:
                    log_error(f"  Failed to update secret '{key}': {e}")
            else:
                log_info(f"  (Dry-run) Secret '{key}' would be updated.")
        else:
            log_info(f"Creating new secret: {key}")
            if not dry_run:
                try:
                    repo.create_secret(key, value)
                    log_success(f"  Secret '{key}' created.")
                    created_count += 1
                except GithubException as e:
                    log_error(f"  Failed to create secret '{key}': {e}")
            else:
                log_info(f"  (Dry-run) Secret '{key}' would be created.")
    
    log_info("\n--- Synchronization Summary ---")
    log_info(f"Secrets created: {created_count}")
    log_info(f"Secrets updated: {updated_count}")
    if dry_run:
        log_warn("This was a DRY RUN. No changes were actually made to GitHub secrets.")
    
    return 0

def main():
    parser = argparse.ArgumentParser(
        description="Securely synchronize environment variables from a .env file to GitHub repository secrets."
    )
    parser.add_argument(
        "--owner",
        required=True,
        help="GitHub repository owner (username or organization)."
    )
    parser.add_argument(
        "--repo",
        required=True,
        help="GitHub repository name."
    )
    parser.add_argument(
        "--env-file",
        default=".env",
        help="Path to the .env file (default: ./.env)."
    )
    parser.add_argument(
        "--github-token",
        help="GitHub Personal Access Token. Recommended to use GITHUB_TOKEN env var instead."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Perform a dry run without making any actual changes to GitHub secrets."
    )
    parser.add_argument(
        "-h", "--help",
        action="help",
        default=argparse.SUPPRESS,
        help="Show this help message and exit."
    )

    args = parser.parse_args()

    github_token = args.github_token or os.environ.get("GITHUB_TOKEN")
    if not github_token:
        log_error("GitHub token not found. Please set the GITHUB_TOKEN environment variable or use --github-token.")
        log_error("A token with 'repo' scope (for private repos) or 'public_repo' scope (for public repos) is required.")
        return 1

    try:
        g = Github(github_token)
    except Exception as e:
        log_error(f"Failed to initialize GitHub client: {e}")
        return 1

    repo = get_github_repo(g, args.owner, args.repo)
    if not repo:
        return 1

    local_secrets = get_local_secrets(args.env_file)
    if local_secrets is None:
        return 1

    return sync_secrets(repo, local_secrets, args.dry_run)

if __name__ == "__main__":
    exit(main())
