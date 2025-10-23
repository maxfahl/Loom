import argparse
import requests
import os
import sys
import json

# test-auth-flow.py
#
# Purpose:
#   Simulates a full authentication flow (e.g., register, login, get token) and then
#   makes a request to a protected endpoint, verifying the token's validity.
#   This script is useful for quick smoke tests of the authentication system
#   and protected API routes, especially during development or CI/CD.
#
# Usage:
#   python test-auth-flow.py [--base-url <api_base_url>] \
#                             [--register-path <path>] [--login-path <path>] \
#                             [--protected-path <path>] \
#                             [--username <user>] [--password <pass>] \
#                             [--dry-run]
#
# Arguments:
#   --base-url <api_base_url>: Optional. The base URL of the API (e.g., http://localhost:3000).
#                              Defaults to 'http://localhost:3000'.
#                              Can also be set via the API_BASE_URL environment variable.
#   --register-path <path>:    Optional. Path to the registration endpoint (default: /auth/register).
#   --login-path <path>:       Optional. Path to the login endpoint (default: /auth/login).
#   --protected-path <path>:   Optional. Path to a protected endpoint (default: /api/protected).
#   --username <user>:         Optional. Username for testing (default: testuser).
#   --password <pass>:         Optional. Password for testing (default: testpassword).
#   --dry-run:                 Optional. If set, the script will only show what would be done
#                              without actually making requests.
#
# Examples:
#   python test-auth-flow.py
#   python test-auth-flow.py --base-url https://my-api.com --username myuser --password mypass
#   API_BASE_URL="http://localhost:4000" python test-auth-flow.py --protected-path /admin/dashboard
#   python test-auth-flow.py --dry-run
#
# Features:
#   - Configurable API endpoints and user credentials.
#   - Simulates registration, login, and access to a protected resource.
#   - Extracts and uses authentication tokens (assumes JWT in 'access_token' field).
#   - Provides clear console output with color for better readability.
#   - Includes a dry-run mode for safety.
#   - Handles HTTP errors gracefully.
#   - Supports environment variables for configuration.

class Color:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def print_color(color, message):
    print(f"{color}{message}{Color.END}")

def main():
    parser = argparse.ArgumentParser(
        description="Simulates an authentication flow and tests a protected API endpoint."
    )
    parser.add_argument(
        "--base-url",
        default=os.environ.get("API_BASE_URL", "http://localhost:3000"),
        help="Base URL of the API (default: http://localhost:3000). Can be set via API_BASE_URL env var."
    )
    parser.add_argument(
        "--register-path",
        default="/auth/register",
        help="Path to the registration endpoint (default: /auth/register)"
    )
    parser.add_argument(
        "--login-path",
        default="/auth/login",
        help="Path to the login endpoint (default: /auth/login)"
    )
    parser.add_argument(
        "--protected-path",
        default="/api/protected",
        help="Path to a protected endpoint (default: /api/protected)"
    )
    parser.add_argument(
        "--username",
        default="testuser",
        help="Username for testing (default: testuser)"
    )
    parser.add_argument(
        "--password",
        default="testpassword",
        help="Password for testing (default: testpassword)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="If set, only show what would be done without actually making requests."
    )

    args = parser.parse_args()

    base_url = args.base_url
    register_url = f"{base_url}{args.register_path}"
    login_url = f"{base_url}{args.login_path}"
    protected_url = f"{base_url}{args.protected_path}"
    username = args.username
    password = args.password
    dry_run = args.dry_run

    print_color(Color.BLUE, f"Starting authentication flow test for API: {base_url}")
    if dry_run:
        print_color(Color.YELLOW, "DRY RUN: No actual HTTP requests will be made.")

    auth_token = None

    # 1. Register User (Optional, depends on API setup)
    print_color(Color.BLUE, f"\nAttempting to register user at {register_url}...")
    if not dry_run:
        try:
            register_payload = {"username": username, "password": password}
            response = requests.post(register_url, json=register_payload)
            response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
            print_color(Color.GREEN, f"Registration successful (Status: {response.status_code}).")
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 409: # Conflict, user already exists
                print_color(Color.YELLOW, f"User '{username}' already exists. Skipping registration.")
            else:
                print_color(Color.RED, f"Registration failed (Status: {e.response.status_code}): {e.response.text}")
                sys.exit(1)
        except requests.exceptions.ConnectionError as e:
            print_color(Color.RED, f"Connection error during registration: {e}")
            sys.exit(1)
        except Exception as e:
            print_color(Color.RED, f"An unexpected error occurred during registration: {e}")
            sys.exit(1)
    else:
        print_color(Color.YELLOW, f"Dry run: Would attempt to register user '{username}' at {register_url}")

    # 2. Login User
    print_color(Color.BLUE, f"\nAttempting to log in user '{username}' at {login_url}...")
    if not dry_run:
        try:
            login_payload = {"username": username, "password": password}
            response = requests.post(login_url, json=login_payload)
            response.raise_for_status()
            login_data = response.json()
            auth_token = login_data.get("access_token") # Assuming JWT is returned as 'access_token'

            if auth_token:
                print_color(Color.GREEN, f"Login successful (Status: {response.status_code}). Token obtained.")
            else:
                print_color(Color.RED, f"Login successful, but no 'access_token' found in response: {login_data}")
                sys.exit(1)
        except requests.exceptions.HTTPError as e:
            print_color(Color.RED, f"Login failed (Status: {e.response.status_code}): {e.response.text}")
            sys.exit(1)
        except requests.exceptions.ConnectionError as e:
            print_color(Color.RED, f"Connection error during login: {e}")
            sys.exit(1)
        except json.JSONDecodeError:
            print_color(Color.RED, f"Login response was not valid JSON: {response.text}")
            sys.exit(1)
        except Exception as e:
            print_color(Color.RED, f"An unexpected error occurred during login: {e}")
            sys.exit(1)
    else:
        print_color(Color.YELLOW, f"Dry run: Would attempt to log in user '{username}' at {login_url}")

    # 3. Access Protected Endpoint
    print_color(Color.BLUE, f"\nAttempting to access protected endpoint at {protected_url}...")
    if not dry_run:
        if not auth_token:
            print_color(Color.RED, "Cannot test protected endpoint: No authentication token available.")
            sys.exit(1)

        headers = {"Authorization": f"Bearer {auth_token}"}
        try:
            response = requests.get(protected_url, headers=headers)
            response.raise_for_status()
            print_color(Color.GREEN, f"Successfully accessed protected endpoint (Status: {response.status_code}).")
            print_color(Color.GREEN, f"Response: {response.text[:200]}...") # Print first 200 chars
        except requests.exceptions.HTTPError as e:
            print_color(Color.RED, f"Failed to access protected endpoint (Status: {e.response.status_code}): {e.response.text}")
            sys.exit(1)
        except requests.exceptions.ConnectionError as e:
            print_color(Color.RED, f"Connection error accessing protected endpoint: {e}")
            sys.exit(1)
        except Exception as e:
            print_color(Color.RED, f"An unexpected error occurred accessing protected endpoint: {e}")
            sys.exit(1)
    else:
        print_color(Color.YELLOW, f"Dry run: Would attempt to access protected endpoint '{protected_url}' with token.")

    print_color(Color.BLUE, "\nAuthentication flow test complete.")

if __name__ == "__main__":
    main()
