#!/usr/bin/env python3

import argparse
import json
import yaml
import os
from typing import Dict, List, Any

def generate_policy(roles: List[str], resources: List[str], actions: List[str], output_format: str) -> Dict[str, Any]:
    """
    Generates a basic RBAC policy structure.

    Args:
        roles (List[str]): List of role names (e.g., "admin", "editor").
        resources (List[str]): List of resource names (e.g., "users", "products").
        actions (List[str]): List of action names (e.g., "read", "write", "delete").
        output_format (str): Desired output format ("json" or "yaml").

    Returns:
        Dict[str, Any]: A dictionary representing the RBAC policy.
    """
    policy: Dict[str, Any] = {
        "version": "1.0",
        "description": "Generated RBAC Policy",
        "roles": {},
        "permissions": {}
    }

    # Define roles
    for role in roles:
        policy["roles"][role] = {
            "description": f"Role for {role}",
            "inherits": [] # Can be extended to support role inheritance
        }

    # Define permissions (example: all roles can read all resources)
    for role in roles:
        policy["permissions"][role] = []
        for resource in resources:
            for action in actions:
                # Example: Grant all actions on all resources to admin, read-only to viewer
                if role == "admin":
                    policy["permissions"][role].append(f"{action}:{resource}")
                elif role == "editor" and action in ["read", "write"]:
                    policy["permissions"][role].append(f"{action}:{resource}")
                elif role == "viewer" and action == "read":
                    policy["permissions"][role].append(f"{action}:{resource}")
                # Add more complex logic here as needed

    return policy

def main():
    parser = argparse.ArgumentParser(
        description="Generate a basic RBAC policy configuration.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "-r", "--roles",
        nargs="+",
        default=["admin", "editor", "viewer"],
        help="Space-separated list of role names (e.g., 'admin editor viewer').
"
             "Default: admin editor viewer"
    )
    parser.add_argument(
        "-res", "--resources",
        nargs="+",
        default=["users", "products", "orders"],
        help="Space-separated list of resource names (e.g., 'users products').
"
             "Default: users products orders"
    )
    parser.add_argument(
        "-a", "--actions",
        nargs="+",
        default=["read", "write", "delete"],
        help="Space-separated list of action names (e.g., 'read write').
"
             "Default: read write delete"
    )
    parser.add_argument(
        "-f", "--format",
        choices=["json", "yaml"],
        default="json",
        help="Output format for the policy file (json or yaml).
"
             "Default: json"
    )
    parser.add_argument(
        "-o", "--output",
        default="rbac_policy",
        help="Output file name (without extension). Default: rbac_policy"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the policy to stdout instead of writing to a file."
    )

    args = parser.parse_args()

    policy_data = generate_policy(args.roles, args.resources, args.actions, args.format)

    if args.dry_run:
        if args.format == "json":
            print(json.dumps(policy_data, indent=2))
        else:
            print(yaml.dump(policy_data, indent=2, sort_keys=False))
    else:
        output_filename = f"{args.output}.{args.format}"
        try:
            with open(output_filename, "w") as f:
                if args.format == "json":
                    json.dump(policy_data, f, indent=2)
                else:
                    yaml.dump(policy_data, f, indent=2, sort_keys=False)
            print(f"RBAC policy successfully generated and saved to {output_filename}")
        except IOError as e:
            print(f"Error writing to file {output_filename}: {e}")
            exit(1)

if __name__ == "__main__":
    main()
