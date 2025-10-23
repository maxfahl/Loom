#!/usr/bin/env python3

import argparse
import os

def generate_hcl_policy(path: str, capabilities: list[str], description: str) -> str:
    """
    Generates a HashiCorp Vault policy in HCL format.

    Args:
        path (str): The path in Vault to which the policy applies (e.g., "secret/data/my-app/*").
        capabilities (list[str]): A list of capabilities (e.g., "read", "write", "list", "delete", "sudo").
        description (str): A human-readable description for the policy.

    Returns:
        str: The generated policy in HCL format.
    """
    capabilities_str = ', '.join([f'"{cap}"' for cap in capabilities])
    policy_hcl = f"""
# {description}
path \"{path}\" {{
  capabilities = [{capabilities_str}]
}}
"""
    return policy_hcl

def main():
    parser = argparse.ArgumentParser(
        description="Generate a basic HashiCorp Vault policy in HCL format.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "-p", "--path",
        required=True,
        help="The path in Vault to which the policy applies (e.g., 'secret/data/my-app/*')."
    )
    parser.add_argument(
        "-c", "--capabilities",
        nargs='+',
        default=["read"],
        choices=["read", "write", "list", "delete", "sudo", "create", "update", "patch"],
        help="Space-separated list of capabilities (e.g., 'read write').\n             Default: read"
    )
    parser.add_argument(
        "-d", "--description",
        default="Generated Vault policy",
        help="A human-readable description for the policy."
    )
    parser.add_argument(
        "-o", "--output",
        default="vault_policy.hcl",
        help="Output file name for the HCL policy. Default: vault_policy.hcl"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the policy to stdout instead of writing to a file."
    )

    args = parser.parse_args()

    policy_hcl = generate_hcl_policy(args.path, args.capabilities, args.description)

    if args.dry_run:
        print(policy_hcl)
    else:
        try:
            with open(args.output, "w") as f:
                f.write(policy_hcl)
            print(f"Vault policy successfully generated and saved to {args.output}")
            print("\nTo apply this policy to Vault, use:\n")
            print(f"  vault policy write <policy-name> {args.output}")
        except IOError as e:
            print(f"Error writing to file {args.output}: {e}")
            exit(1)

if __name__ == "__main__":
    main()
