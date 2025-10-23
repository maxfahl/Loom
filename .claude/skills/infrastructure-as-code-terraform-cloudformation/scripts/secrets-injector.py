import argparse
import os
import sys
import json
import base64

# ANSI escape codes for colored output
COLOR_GREEN = "\033[92m"
COLOR_RED = "\033[91m"
COLOR_YELLOW = "\033[93m"
COLOR_BLUE = "\033[94m"
COLOR_RESET = "\033[0m"

def log_info(message):
    print(f"{COLOR_BLUE}[INFO]{COLOR_RESET} {message}")

def log_success(message):
    print(f"{COLOR_GREEN}[SUCCESS]{COLOR_RESET} {message}")

def log_warn(message):
    print(f"{COLOR_YELLOW}[WARN]{COLOR_RESET} {message}")

def log_error(message):
    print(f"{COLOR_RED}[ERROR]{COLOR_RESET} {message}")
    sys.exit(1)

def get_aws_secret(secret_name, aws_profile=None, aws_region=None):
    """Retrieves a secret from AWS Secrets Manager."""
    try:
        import boto3
        session_args = {}
        if aws_profile:
            session_args['profile_name'] = aws_profile
        if aws_region:
            session_args['region_name'] = aws_region

        session = boto3.Session(**session_args)
        client = session.client('secretsmanager')

        get_secret_value_response = client.get_secret_value(SecretId=secret_name)

        if 'SecretString' in get_secret_value_response:
            return get_secret_value_response['SecretString']
        else:
            return base64.b64decode(get_secret_value_response['SecretBinary']).decode('utf-8')
    except ImportError:
        log_error("Python 'boto3' library not found. Please install it (`pip install boto3`) to use AWS Secrets Manager.")
    except client.exceptions.ResourceNotFoundException:
        log_error(f"Secret '{secret_name}' not found in AWS Secrets Manager.")
    except Exception as e:
        log_error(f"Error retrieving secret '{secret_name}': {e}")
    return None

def main():
    parser = argparse.ArgumentParser(
        description="""
        Securely injects secrets from a specified secrets manager into IaC deployments.
        Currently supports AWS Secrets Manager.
        """,
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "secret_name",
        help="The name or ARN of the secret to retrieve (e.g., 'my-app/db-password')."
    )
    parser.add_argument(
        "-s", "--secrets-manager",
        choices=["aws-secrets-manager"],
        default="aws-secrets-manager",
        help="The secrets manager to use. (Default: aws-secrets-manager)"
    )
    parser.add_argument(
        "-f", "--format",
        choices=["env", "json", "file"],
        default="env",
        help="""
        Output format for the secret:
        - 'env': Prints as environment variables (KEY=VALUE).
        - 'json': Prints as a JSON object.
        - 'file': Writes the secret string directly to a file.
        (Default: env)
        """
    )
    parser.add_argument(
        "-o", "--output-file",
        help="Required if --format is 'file'. Path to the file to write the secret to."
    )
    parser.add_argument(
        "--aws-profile",
        help="AWS profile to use for AWS Secrets Manager access."
    )
    parser.add_argument(
        "--aws-region",
        help="AWS region to use for AWS Secrets Manager access."
    )
    parser.add_argument(
        "--prefix",
        help="Prefix to add to environment variable names (e.g., 'APP_'). Only applicable for 'env' format."
    )
    parser.add_argument(
        "--key-map",
        help="""
        JSON string mapping secret keys to desired environment variable names.
        Example: '{"db_user": "DB_USERNAME", "db_pass": "DB_PASSWORD"}'
        Only applicable for 'env' format when secret is a JSON string.
        """
    )

    args = parser.parse_args()

    secret_value = None
    if args.secrets_manager == "aws-secrets-manager":
        secret_value = get_aws_secret(args.secret_name, args.aws_profile, args.aws_region)
    else:
        log_error(f"Unsupported secrets manager: {args.secrets_manager}")

    if secret_value is None:
        log_error("Failed to retrieve secret.")

    if args.format == "env":
        try:
            # Assume secret_value is a JSON string for env vars
            secret_data = json.loads(secret_value)
            prefix = args.prefix if args.prefix else ""
            key_map = json.loads(args.key_map) if args.key_map else {}

            for key, value in secret_data.items():
                env_key = key_map.get(key, key).upper() # Use mapped key or uppercase original
                print(f"export {prefix}{env_key}=\"{value}\"")
            log_success("Secrets exported as environment variables.")
            log_warn("Remember to source this output in your shell (e.g., `eval $(python secrets-injector.py ...)`).")
        except json.JSONDecodeError:
            log_error("Secret is not a valid JSON string. Cannot export as environment variables from a single string secret.")
            log_error("If the secret is a plain string, consider using the 'file' format or manually setting the environment variable.")
    elif args.format == "json":
        try:
            # Pretty print JSON if it's a JSON string
            parsed_json = json.loads(secret_value)
            print(json.dumps(parsed_json, indent=2))
        except json.JSONDecodeError:
            # Otherwise, just print the string
            print(secret_value)
        log_success("Secret printed as JSON.")
    elif args.format == "file":
        if not args.output_file:
            log_error("Output file (--output-file) is required for 'file' format.")
        try:
            with open(args.output_file, "w") as f:
                f.write(secret_value)
            log_success(f"Secret successfully written to {args.output_file}")
        except Exception as e:
            log_error(f"Error writing secret to file {args.output_file}: {e}")

if __name__ == "__main__":
    main()
