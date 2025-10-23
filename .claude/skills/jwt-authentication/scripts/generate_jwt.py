#!/usr/bin/env python3

"""
generate_jwt.py

Purpose:
  Automates the creation of JWT tokens for development and testing purposes.
  It allows specifying payload data, secret key, algorithm, and expiration time,
  saving developers from manually encoding tokens or using online tools.

Pain Point Solved:
  Manually crafting JWTs for testing different scenarios (e.g., expired tokens,
  specific roles) is tedious and error-prone. This script provides a quick,
  configurable, and repeatable way to generate JWTs.

Usage Examples:
  # Generate a basic JWT with default settings (HS256, 1 hour expiry)
  python scripts/generate_jwt.py --payload '{"userId": "testuser", "role": "guest"}' --secret "your-super-secret-key"

  # Generate a JWT with a custom expiration time (e.g., 30 minutes)
  python scripts/generate_jwt.py --payload '{"userId": "admin"}' --secret "your-super-secret-key" --expires-in 30m

  # Generate a JWT with a custom algorithm (e.g., RS256 - requires private key file)
  # python scripts/generate_jwt.py --payload '{"userId": "api_client"}' --private-key-file "private.pem" --algorithm RS256 --expires-in 24h

  # Generate a JWT that is already expired (for testing error handling)
  python scripts/generate_jwt.py --payload '{"userId": "expired"}' --secret "your-super-secret-key" --expires-in -5m

Dependencies:
  - PyJWT: pip install PyJWT
  - cryptography: pip install cryptography (required for RS256/ES256 algorithms)
  - python-dateutil: pip install python-dateutil (for flexible expiry parsing)
"""

import jwt
import datetime
import time
import argparse
import json
import os
from dateutil.relativedelta import relativedelta

# --- Configuration ---
# Default algorithm for symmetric keys
DEFAULT_ALGORITHM = "HS256"
# Default expiration time: 1 hour
DEFAULT_EXPIRES_IN = "1h"

def parse_time_string(time_str: str) -> datetime.timedelta:
    """
    Parses a time string (e.g., "1h", "30m", "7d") into a timedelta object.
    Supports 's' (seconds), 'm' (minutes), 'h' (hours), 'd' (days).
    Negative values are allowed for creating expired tokens.
    """
    if not time_str:
        return datetime.timedelta(hours=1) # Default to 1 hour if empty

    unit = time_str[-1]
    value = int(time_str[:-1])

    if unit == 's':
        return datetime.timedelta(seconds=value)
    elif unit == 'm':
        return datetime.timedelta(minutes=value)
    elif unit == 'h':
        return datetime.timedelta(hours=value)
    elif unit == 'd':
        return datetime.timedelta(days=value)
    else:
        raise ValueError(f"Invalid time unit: {unit}. Use s, m, h, or d.")

def generate_jwt_token(
    payload: dict,
    secret_or_private_key: str,
    algorithm: str,
    expires_in: str,
    issuer: str = None,
    audience: str = None,
    key_id: str = None
) -> str:
    """
    Generates a JWT token with the given payload, secret/private key, and algorithm.

    Args:
        payload (dict): The data to encode into the token.
        secret_or_private_key (str): The secret key (for HSxxx) or private key content (for RSxxx/ESxxx).
        algorithm (str): The signing algorithm (e.g., 'HS256', 'RS256', 'ES256').
        expires_in (str): A string representing the expiration time (e.g., "1h", "30m", "7d").
        issuer (str, optional): The 'iss' claim.
        audience (str, optional): The 'aud' claim.
        key_id (str, optional): The 'kid' header parameter.

    Returns:
        str: The encoded JWT token.
    """
    headers = {}
    if key_id:
        headers['kid'] = key_id

    # Calculate expiration time
    try:
        delta = parse_time_string(expires_in)
        expiration_time = datetime.datetime.utcnow() + delta
    except ValueError as e:
        print(f"Error parsing expires-in: {e}", file=os.stderr)
        exit(1)

    # Add standard JWT claims
    claims = {
        **payload,
        'exp': expiration_time,
        'iat': datetime.datetime.utcnow(),
        'nbf': datetime.datetime.utcnow() - datetime.timedelta(seconds=10) # 10 seconds before issued at
    }

    if issuer:
        claims['iss'] = issuer
    if audience:
        claims['aud'] = audience

    try:
        encoded_jwt = jwt.encode(
            claims,
            secret_or_private_key,
            algorithm=algorithm,
            headers=headers
        )
        return encoded_jwt
    except Exception as e:
        print(f"Error encoding JWT: {e}", file=os.stderr)
        exit(1)

def main():
    parser = argparse.ArgumentParser(
        description="Generate JWT tokens for development and testing.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        '--payload',
        type=str,
        required=True,
        help="JSON string for the JWT payload (e.g., '{"userId": "123", "role": "admin"}')"
    )
    parser.add_argument(
        '--secret',
        type=str,
        help=f"Secret key for symmetric algorithms (e.g., {DEFAULT_ALGORITHM}). Required if --private-key-file is not used."
    )
    parser.add_argument(
        '--private-key-file',
        type=str,
        help="Path to a file containing the private key for asymmetric algorithms (e.g., RS256, ES256). Required if --secret is not used."
    )
    parser.add_argument(
        '--algorithm',
        type=str,
        default=DEFAULT_ALGORITHM,
        help=f"Signing algorithm (e.g., HS256, RS256, ES256). Default: {DEFAULT_ALGORITHM}"
    )
    parser.add_argument(
        '--expires-in',
        type=str,
        default=DEFAULT_EXPIRES_IN,
        help=f"Expiration time (e.g., '1h', '30m', '7d'). Default: {DEFAULT_EXPIRES_IN}"
    )
    parser.add_argument(
        '--issuer',
        type=str,
        help="Optional: 'iss' (issuer) claim for the JWT."
    )
    parser.add_argument(
        '--audience',
        type=str,
        help="Optional: 'aud' (audience) claim for the JWT."
    )
    parser.add_argument(
        '--kid',
        type=str,
        help="Optional: 'kid' (Key ID) header parameter for the JWT."
    )

    args = parser.parse_args()

    if not args.secret and not args.private_key_file:
        parser.error("Either --secret or --private-key-file must be provided.")
    if args.secret and args.private_key_file:
        parser.error("Cannot use both --secret and --private-key-file. Choose one.")

    try:
        payload_data = json.loads(args.payload)
    except json.JSONDecodeError:
        print("Error: --payload must be a valid JSON string.", file=os.stderr)
        exit(1)

    secret_or_key_content = None
    if args.secret:
        secret_or_key_content = args.secret
    elif args.private_key_file:
        try:
            with open(args.private_key_file, 'r') as f:
                secret_or_key_content = f.read()
        except FileNotFoundError:
            print(f"Error: Private key file not found at {args.private_key_file}", file=os.stderr)
            exit(1)
        except Exception as e:
            print(f"Error reading private key file: {e}", file=os.stderr)
            exit(1)

    print(f"Generating JWT with algorithm: {args.algorithm}, expires in: {args.expires_in}")
    print(f"Payload: {json.dumps(payload_data, indent=2)}")

    token = generate_jwt_token(
        payload_data,
        secret_or_key_content,
        args.algorithm,
        args.expires_in,
        args.issuer,
        args.audience,
        args.kid
    )

    print("
--- Generated JWT ---")
    print(token)
    print("---------------------
")

if __name__ == "__main__":
    main()
