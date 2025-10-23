#!/usr/bin/env python3

"""
generate_secret.py

Purpose:
  Generates cryptographically secure random strings suitable for various types of secrets
  (e.g., API keys, database passwords, encryption keys). It allows specifying length
  and character sets.

Pain Point Solved:
  Manually generating strong, random secrets is often done insecurely or with insufficient
  entropy. This script provides a reliable way to create high-quality secrets for
  initial setup, populating .env files, or secret managers.

Usage Examples:
  # Generate a 32-character generic secret (base64 encoded)
  python scripts/generate_secret.py

  # Generate a 64-character API key
  python scripts/generate_secret.py --length 64 --type apikey

  # Generate a 20-character password with special characters
  python scripts/generate_secret.py --length 20 --type password --include-special

  # Generate a hex-encoded encryption key
  python scripts/generate_secret.py --length 32 --encoding hex

Configuration:
  - `--length`: Length of the random bytes to generate (default: 32). The final string length
                will vary based on encoding.
  - `--type`: Type of secret to generate. Influences character set for 'password' type.
              Options: 'generic' (default), 'apikey', 'password'.
  - `--encoding`: Encoding for the output string. Options: 'base64' (default), 'hex'.
  - `--include-special`: For 'password' type, include special characters (e.g., !@#$%^&*).

Dependencies:
  - None (uses standard Python libraries)
"""

import os
import base64
import binascii
import argparse
import string
import random
import sys

def generate_random_bytes(length: int) -> bytes:
    """
    Generates cryptographically strong random bytes.
    """
    try:
        return os.urandom(length)
    except Exception as e:
        print(f"Error generating random bytes: {e}", file=sys.stderr)
        sys.exit(1)

def generate_password(
    length: int,
    include_special: bool = False,
    chars: str = None
) -> str:
    """
    Generates a random password string.
    """
    if chars is None:
        chars = string.ascii_letters + string.digits
        if include_special:
            chars += string.punctuation.replace("'", "").replace('"', "") # Avoid quotes for easier handling

    if not chars:
        print("Error: No characters available for password generation.", file=sys.stderr)
        sys.exit(1)

    return ''.join(random.SystemRandom().choice(chars) for _ in range(length))

def main():
    parser = argparse.ArgumentParser(
        description="Generate cryptographically secure random strings for secrets.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        '--length',
        type=int,
        default=32,
        help="Length of the random bytes to generate (default: 32)." \
             "The final string length will vary based on encoding."
    )
    parser.add_argument(
        '--type',
        type=str,
        default="generic",
        choices=['generic', 'apikey', 'password'],
        help="Type of secret to generate. Influences character set for 'password' type."
            "Options: 'generic' (default), 'apikey', 'password'."
    )
    parser.add_argument(
        '--encoding',
        type=str,
        default="base64",
        choices=['base64', 'hex'],
        help="Encoding for the output string. Options: 'base64' (default), 'hex'."
    )
    parser.add_argument(
        '--include-special',
        action='store_true',
        help="For 'password' type, include special characters (e.g., !@#$%^&*)."
    )

    args = parser.parse_args()

    if args.length <= 0:
        print("\033[0;31mError: --length must be a positive integer.\033[0m", file=sys.stderr)
        sys.exit(1)

    print(f"\n\033[1;34m--- Secure Secret Generator ---\\033[0m")

    if args.type == 'password':
        secret = generate_password(args.length, args.include_special)
        print(f"\033[0;32mGenerated Password:\033[0m {secret}")
        print(f"\033[0;33mNote: Password length is approximate to --length due to character set constraints.\033[0m")
    else:
        random_bytes = generate_random_bytes(args.length)
        if args.encoding == 'base64':
            # urlsafe_b64encode is good for API keys, etc., avoids + and /
            secret = base64.urlsafe_b64encode(random_bytes).decode('utf-8').rstrip('=')
        elif args.encoding == 'hex':
            secret = binascii.hexlify(random_bytes).decode('utf-8')
        else:
            # Should not happen due to choices in argparse
            print("\033[0;31mError: Invalid encoding specified.\033[0m", file=sys.stderr)
            sys.exit(1)

        print(f"\033[0;32mGenerated {args.type.capitalize()} Secret ({args.encoding}):\033[0m {secret}")

    print("\n\033[1;33mIMPORTANT SECURITY NOTE:\033[0m")
    print("  This script generates a strong secret. Ensure you store it securely.")
    print("  - Do NOT commit secrets to version control (Git, SVN, etc.).")
    print("  - For production, use a dedicated secret management solution (e.g., AWS Secrets Manager, HashiCorp Vault).")
    print("  - For local development, use .env files and ensure they are .gitignore'd.")
    print("  - Restrict file permissions for any local files storing secrets (e.g., chmod 600).")

if __name__ == "__main__":
    main()
