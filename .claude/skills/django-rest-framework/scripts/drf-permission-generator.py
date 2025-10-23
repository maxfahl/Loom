#!/usr/bin/env python3

# drf-permission-generator.py
# Description: Generates a custom DRF permission class template.
# Usage: python3 drf-permission-generator.py <permission_name> [--object-level] [--app <app_name>]
#
# Arguments:
#   permission_name: Name of the permission class (e.g., 'IsOwner', 'CanEditProduct').
#
# Options:
#   --object-level:  Generate a permission that checks object-level permissions (has_object_permission).
#                    By default, it generates a global permission (has_permission).
#   --app <app_name>: Specify the Django app where the permission should be created.
#                     Defaults to 'myapp' or the current directory if no app is found.
#   --help:          Display this help message.

import os
import sys
import argparse
from typing import List

# --- Configuration Variables ---
COLOR_RESET = "\033[0m"
COLOR_RED = "\033[0;31m"
COLOR_GREEN = "\033[0;32m"
COLOR_YELLOW = "\033[0;33m"
COLOR_BLUE = "\033[0;34m"

# --- Helper Functions ---
def log_info(message: str):
    print(f"{COLOR_BLUE}[INFO]{COLOR_RESET} {message}")

def log_success(message: str):
    print(f"{COLOR_GREEN}[SUCCESS]{COLOR_RESET} {message}")

def log_warning(message: str):
    print(f"{COLOR_YELLOW}[WARNING]{COLOR_RESET} {message}")

def log_error(message: str):
    print(f"{COLOR_RED}[ERROR]{COLOR_RESET} {message}")
    sys.exit(1)

def find_app_path(app_name: str | None) -> str:
    if app_name:
        app_path = os.path.join(os.getcwd(), app_name)
        if not os.path.isdir(app_path):
            log_error(f"App directory '{app_name}' not found. Please ensure it exists or specify a correct app name.")
        return app_path
    
    # Try to find an app in the current directory
    for entry in os.listdir(os.getcwd()):
        if os.path.isdir(entry) and os.path.exists(os.path.join(entry, "models.py")):
            log_info(f"Found Django app '{entry}'. Creating permission there.")
            return os.path.join(os.getcwd(), entry)
    
    log_error("Could not find a Django app in the current directory. Please specify an app name using --app.")

def generate_permission_content(permission_name: str, object_level: bool) -> str:
    if object_level:
        return f"""from rest_framework import permissions

class {permission_name}(permissions.BasePermission):
    """
    Custom object-level permission to allow only owners of an object to edit it.
    Assumes the model instance has an 'owner' attribute.
    Read-only access is allowed for any request.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the object.
        # Assuming 'obj' has an 'owner' attribute which is a User instance.
        return obj.owner == request.user
"""
    else:
        return f"""from rest_framework import permissions

class {permission_name}(permissions.BasePermission):
    """
    Custom global permission to allow access based on specific criteria.
    """

    def has_permission(self, request, view):
        # Read permissions are allowed to any request.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Example: Only allow authenticated users to write.
        # return request.user and request.user.is_authenticated

        # Example: Only allow admin users to write.
        # return request.user and request.user.is_staff

        # Default: Deny write access unless explicitly allowed.
        return False
"""

# --- Main Logic ---
def main():
    parser = argparse.ArgumentParser(
        description="Generate a custom DRF permission class template."
    )
    parser.add_argument(
        "permission_name",
        help="Name of the permission class (e.g., 'IsOwner', 'CanEditProduct')."
    )
    parser.add_argument(
        "--object-level",
        action="store_true",
        help="Generate a permission that checks object-level permissions (has_object_permission)."
    )
    parser.add_argument(
        "--app",
        help="Specify the Django app where the permission should be created."
    )
    args = parser.parse_args()

    permission_name = args.permission_name
    object_level = args.object_level
    app_name = args.app

    # Ensure permission name follows class naming conventions
    if not re.match(r'^[A-Z][a-zA-Z0-9]*$', permission_name):
        log_error(f"Invalid permission name '{permission_name}'. Must be a valid Python class name (e.g., IsOwner).")

    app_path = find_app_path(app_name)
    permissions_dir = os.path.join(app_path, "permissions")
    os.makedirs(permissions_dir, exist_ok=True)

    permission_file_path = os.path.join(permissions_dir, f"{permission_name.lower()}.py")

    if os.path.exists(permission_file_path):
        log_warning(f"Permission file '{permission_file_path}' already exists. Skipping creation.")
    else:
        permission_content = generate_permission_content(permission_name, object_level)
        with open(permission_file_path, "w") as f:
            f.write(permission_content)
        log_success(f"Generated custom permission: {permission_file_path}")
        log_info("Remember to customize the permission logic as needed.")

    # Add __init__.py if it doesn't exist
    init_file_path = os.path.join(permissions_dir, "__init__.py")
    if not os.path.exists(init_file_path):
        with open(init_file_path, "w") as f:
            f.write("")
        log_info(f"Created {init_file_path}")

    log_success("DRF permission generation complete!")

if __name__ == "__main__":
    main()
