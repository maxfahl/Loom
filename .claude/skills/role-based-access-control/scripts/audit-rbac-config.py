#!/usr/bin/env python3

import argparse
import json
import yaml
import os
from typing import Dict, List, Any, Tuple

def load_policy(file_path: str) -> Tuple[Dict[str, Any], str]:
    """
    Loads an RBAC policy from a JSON or YAML file.

    Args:
        file_path (str): Path to the policy file.

    Returns:
        Tuple[Dict[str, Any], str]: A tuple containing the loaded policy and its format ('json' or 'yaml').

    Raises:
        ValueError: If the file format is unsupported or parsing fails.
        FileNotFoundError: If the file does not exist.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Policy file not found: {file_path}")

    _, ext = os.path.splitext(file_path)
    ext = ext.lower()

    with open(file_path, 'r') as f:
        if ext == '.json':
            return json.load(f), 'json'
        elif ext in ('.yaml', '.yml'):
            return yaml.safe_load(f), 'yaml'
        else:
            raise ValueError(f"Unsupported file format: {ext}. Only JSON and YAML are supported.")

def audit_policy(policy: Dict[str, Any]) -> List[str]:
    """
    Audits an RBAC policy for common issues and returns a list of findings.

    Args:
        policy (Dict[str, Any]): The loaded RBAC policy.

    Returns:
        List[str]: A list of strings, each describing a finding.
    """
    findings: List[str] = []

    defined_roles = set(policy.get("roles", {}).keys())
    defined_permissions = set()

    # Collect all unique permissions defined in the policy
    for role, perms in policy.get("permissions", {}).items():
        if isinstance(perms, list):
            for perm in perms:
                defined_permissions.add(perm)

    # 1. Check for undefined roles in permissions
    for role_in_perms in policy.get("permissions", {}).keys():
        if role_in_perms not in defined_roles:
            findings.append(f"WARNING: Role '{role_in_perms}' is used in permissions but not defined in the roles section.")

    # 2. Check for unused roles (roles defined but not assigned any permissions)
    for role in defined_roles:
        if role not in policy.get("permissions", {}):
            findings.append(f"INFO: Role '{role}' is defined but has no permissions assigned.")

    # 3. Identify potentially overly broad permissions (e.g., "*:*" or "delete:*")
    for role, perms in policy.get("permissions", {}).items():
        if isinstance(perms, list):
            for perm in perms:
                if perm == "*:*" or perm.endswith(":*") or perm.startswith("delete:"):
                    findings.append(f"POTENTIAL RISK: Role '{role}' has broad permission '{perm}'. Consider more granular access.")

    # 4. Check for duplicate permissions within a role (less critical, but good to flag)
    for role, perms in policy.get("permissions", {}).items():
        if isinstance(perms, list):
            if len(perms) != len(set(perms)):
                findings.append(f"INFO: Role '{role}' has duplicate permissions.")

    # 5. Check for policy version (if not present or unexpected)
    if "version" not in policy:
        findings.append("WARNING: Policy file does not specify a version.")
    elif policy["version"] != "1.0": # Assuming 1.0 is the expected version
        findings.append(f"INFO: Policy version is '{policy["version"]}', expected '1.0'.")

    return findings

def main():
    parser = argparse.ArgumentParser(
        description="Audit an RBAC policy configuration file for common issues.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "file",
        help="Path to the RBAC policy file (JSON or YAML)."
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Show all findings, including INFO messages."
    )

    args = parser.parse_args()

    print(f"Auditing RBAC policy file: {args.file}\n")

    try:
        policy, file_format = load_policy(args.file)
        findings = audit_policy(policy)

        if not findings:
            print("\033[92mNo issues found in the RBAC policy.\033[0m") # Green color
        else:
            print("\033[93mAudit Findings:\033[0m") # Yellow color
            for finding in findings:
                if args.verbose or not finding.startswith("INFO:"):
                    if finding.startswith("WARNING:") or finding.startswith("POTENTIAL RISK:"):
                        print(f"  \033[91m- {finding}\033[0m") # Red color for warnings/risks
                    else:
                        print(f"  - {finding}")
            print("\n\033[93mAudit complete. Review findings above.\033[0m")

    except FileNotFoundError as e:
        print(f"\033[91mError: {e}\033[0m")
        exit(1)
    except ValueError as e:
        print(f"\033[91mError: {e}\033[0m")
        exit(1)
    except Exception as e:
        print(f"\033[91mAn unexpected error occurred: {e}\033[0m")
        exit(1)

if __name__ == "__main__":
    main()
