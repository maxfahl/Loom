#!/usr/bin/env python3

"""
rotate_jwt_secret.py

Purpose:
  Generates a cryptographically secure random string suitable for a JWT secret key
  and can optionally update a .env file. It also provides crucial guidance on the
  key rotation process, which is a critical security practice.

Pain Point Solved:
  Securely generating and managing secret keys, especially during rotation, can be
  complex and lead to insecure practices if not handled correctly. This script
  automates key generation and assists with .env file updates, while reminding
  developers of important rotation considerations.

Usage Examples:
  # Generate a new secret key and print it to console
  python scripts/rotate_jwt_secret.py

  # Generate a new secret key and update the JWT_SECRET in a .env file
  python scripts/rotate_jwt_secret.py --output-env .env --key-name JWT_SECRET

  # Generate a new secret key with a custom length (e.g., 64 bytes for a longer key)
  python scripts/rotate_jwt_secret.py --length 64

Configuration:
  - `--length`: Length of the random bytes for the key (default: 32, results in ~43 char base64 string).
                A length of 32 bytes (256 bits) is generally considered sufficient for security.
  - `--output-env`: Path to a .env file to update. If specified, the script will update
                    the key specified by `--key-name` in this file.
  - `--key-name`: The name of the key to update in the .env file (default: JWT_SECRET).

Dependencies:
  - None (uses standard Python libraries)
"""

import os
import base64
import argparse
import sys

def generate_jwt_secret(length: int = 32) -> str:
    """
    Generates a secure random string suitable for a JWT secret key.
    Uses os.urandom for cryptographically strong random bytes.
    Base64 encodes it to make it URL-safe and readable.
    """
    try:
        return base64.urlsafe_b64encode(os.urandom(length)).decode('utf-8').rstrip('=')
    except Exception as e:
        print(f"Error generating random bytes: {e}", file=sys.stderr)
        sys.exit(1)

def update_env_file(file_path: str, key_name: str, new_key: str) -> None:
    """
    Updates or adds a key-value pair in a .env file.
    Preserves comments and other lines.
    """
    lines = []
    key_found = False
    try:
        with open(file_path, 'r') as f:
            for line in f:
                # Check if the line starts with the key_name followed by '='
                if line.strip().startswith(f"{key_name}="):
                    lines.append(f"{key_name}={new_key}\n")
                    key_found = True
                else:
                    lines.append(line)
    except FileNotFoundError:
        print(f"\033[0;33mWarning: '{file_path}' not found. Creating a new one.\033[0m")

    if not key_found:
        if lines and not lines[-1].endswith('\n'): # Ensure last line has newline if adding
            lines.append('\n')
        lines.append(f"{key_name}={new_key}\n")

    try:
        with open(file_path, 'w') as f:
            f.writelines(lines)
        print(f"\033[0;32mSuccessfully updated '{key_name}' in '{file_path}' with the new key.\033[0m")
    except IOError as e:
        print(f"\033[0;31mError writing to '{file_path}': {e}\033[0m", file=sys.stderr)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description="Generate and rotate JWT secret keys.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        '--length',
        type=int,
        default=32,
        help="Length of the random bytes for the key (default: 32, results in ~43 char base64 string).""
                A length of 32 bytes (256 bits) is generally considered sufficient for security."
    )
    parser.add_argument(
        '--output-env',
        type=str,
        help="Path to a .env file to update. If specified, the script will update the JWT_SECRET key in this file."
    )
    parser.add_argument(
        '--key-name',
        type=str,
        default="JWT_SECRET",
        help="The name of the key to update in the .env file (default: JWT_SECRET)."
    )

    args = parser.parse_args()

    if args.length <= 0:
        print("\033[0;31mError: --length must be a positive integer.\033[0m", file=sys.stderr)
        sys.exit(1)

    new_secret = generate_jwt_secret(args.length)

    print("\n\033[1;34m--- JWT Secret Key Rotation Script ---\\033[0m")
    print(f"\033[0;32mGenerated new JWT Secret Key:\033[0m {new_secret}")
    print("\n\033[1;33mIMPORTANT CONSIDERATIONS FOR JWT KEY ROTATION:\033[0m")
    print("1.  \033[0;36mApplication Restart\033[0m: Your application needs to be restarted or reloaded to pick up the new key.")
    print("2.  \033[0;36mOld Tokens\033[0m: Tokens signed with the old key will become invalid immediately unless your application supports multiple valid keys during a transition period.")
    print("    Consider a grace period where both old and new keys are accepted for a short time.")
    print("3.  \033[0;36mEnvironment Variables\033[0m: If your application reads the key from environment variables, ensure the new key is set in your deployment environment.")
    print("4.  \033[0;36mSecurity\033[0m: Keep this key secure. Do not commit it to version control. Store keys in a secure environment.")
    print("5.  \033[0;36mKey ID (kid)\033[0m: For more advanced scenarios, especially in microservices, consider using Key IDs (kid) in JWT headers to identify which key was used to sign the token, allowing for smoother transitions.")

    if args.output_env:
        print(f"\nAttempting to update '{args.key_name}' in '{args.output_env}'...")
        update_env_file(args.output_env, args.key_name, new_secret)
    else:
        print("\nTo use this key, you can set it as an environment variable:")
        print(f"\033[0;35mexport {args.key_name}='{new_secret}'\033[0m")
        print("\nOr add it to your .env file manually.")

if __name__ == "__main__":
    main()
