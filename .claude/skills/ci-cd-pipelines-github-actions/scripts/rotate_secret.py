#!/usr/bin/env python3

"""
GitHub Actions Secret Rotator

This script helps rotate GitHub repository secrets by prompting for a new value,
encrypting it, and updating the secret via the GitHub API. It requires a GitHub
Personal Access Token (PAT) with `repo` scope, set as an environment variable.

Usage:
    export GITHUB_TOKEN="YOUR_PAT_HERE"
    python3 rotate_secret.py --owner your-org --repo your-repo --secret-name MY_SECRET
    python3 rotate_secret.py -h # For help

Features:
- Securely prompts for new secret value.
- Encrypts the secret using the repository's public key.
- Updates the secret via GitHub API.
- Error handling for API calls and missing environment variables.
"""

import argparse
import os
import sys
import base64
from nacl import encoding, public

# This script assumes 'requests' is installed. If not, please install it:
# pip install requests PyNaCl
try:
    import requests
except ImportError:
    print("Error: 'requests' library not found. Please install it: pip install requests", file=sys.stderr)
    sys.exit(1)

try:
    from nacl import encoding, public
except ImportError:
    print("Error: 'PyNaCl' library not found. Please install it: pip install PyNaCl", file=sys.stderr)
    sys.exit(1)

GITHUB_API_URL = "https://api.github.com"

def get_repository_public_key(owner, repo, headers):
    """Fetches the public key for encrypting secrets."""
    url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/actions/secrets/public-key"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def encrypt_secret(public_key, secret_value):
    """Encrypts a secret value using the provided public key."""
    public_key_bytes = base64.b64decode(public_key)
    sealed_box = public.SealedBox(public.PublicKey(public_key_bytes))
    encrypted = sealed_box.encrypt(secret_value.encode("utf-8"))
    return base64.b64encode(encrypted).decode("utf-8")

def update_secret(owner, repo, secret_name, encrypted_value, key_id, headers):
    """Updates a repository secret with the encrypted value."""
    url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/actions/secrets/{secret_name}"
    data = {
        "encrypted_value": encrypted_value,
        "key_id": key_id
    }
    response = requests.put(url, headers=headers, json=data)
    response.raise_for_status()
    return response.status_code == 204

def main():
    parser = argparse.ArgumentParser(
        description="Rotate a GitHub repository secret.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "--owner",
        required=True,
        help="The owner of the repository (username or organization)."
    )
    parser.add_argument(
        "--repo",
        required=True,
        help="The name of the repository."
    )
    parser.add_argument(
        "--secret-name",
        required=True,
        help="The name of the secret to rotate."
    )

    args = parser.parse_args()

    github_token = os.environ.get("GITHUB_TOKEN")
    if not github_token:
        print("Error: GITHUB_TOKEN environment variable not set.", file=sys.stderr)
        print("Please set it to a GitHub Personal Access Token with 'repo' scope.", file=sys.stderr)
        sys.exit(1)

    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json"
    }

    try:
        print(f"Fetching public key for {args.owner}/{args.repo}...")
        public_key_data = get_repository_public_key(args.owner, args.repo, headers)
        public_key = public_key_data["key"]
        key_id = public_key_data["key_id"]
        print("Public key fetched successfully.")

        new_secret_value = input(f"Enter new value for secret '{args.secret_name}': ")
        if not new_secret_value:
            print("Secret value cannot be empty. Aborting.", file=sys.stderr)
            sys.exit(1)

        print(f"Encrypting secret '{args.secret_name}'...")
        encrypted_value = encrypt_secret(public_key, new_secret_value)
        print("Secret encrypted.")

        print(f"Updating secret '{args.secret_name}' in {args.owner}/{args.repo}...")
        if update_secret(args.owner, args.repo, args.secret_name, encrypted_value, key_id, headers):
            print(f"Successfully updated secret '{args.secret_name}'.")
        else:
            print(f"Failed to update secret '{args.secret_name}'.", file=sys.stderr)
            sys.exit(1)

    except requests.exceptions.RequestException as e:
        print(f"GitHub API error: {e}", file=sys.stderr)
        if e.response is not None:
            print(f"Response: {e.response.text}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
