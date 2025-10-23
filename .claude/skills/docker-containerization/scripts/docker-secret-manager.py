import argparse
import os
import sys
import yaml

# --- Colors for better readability ---
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def log_info(message):
    print(f"{Colors.OKBLUE}[INFO]{Colors.ENDC} {message}")

def log_warn(message):
    print(f"{Colors.WARNING}[WARN]{Colors.ENDC} {message}")

def log_error(message):
    print(f"{Colors.FAIL}[ERROR]{Colors.ENDC} {message}", file=sys.stderr)

def log_success(message):
    print(f"{Colors.OKGREEN}[SUCCESS]{Colors.ENDC} {message}")

# --- Simple XOR encryption/decryption (NOT for production use!) ---
def xor_encrypt_decrypt(data, key):
    if not key:
        raise ValueError("Encryption key cannot be empty.")
    key_bytes = key.encode('utf-8')
    data_bytes = data.encode('utf-8')
    encrypted_bytes = bytearray()
    for i in range(len(data_bytes)):
        encrypted_bytes.append(data_bytes[i] ^ key_bytes[i % len(key_bytes)])
    return encrypted_bytes.hex()

def xor_decrypt(hex_data, key):
    if not key:
        raise ValueError("Decryption key cannot be empty.")
    key_bytes = key.encode('utf-8')
    encrypted_bytes = bytearray.fromhex(hex_data)
    decrypted_bytes = bytearray()
    for i in range(len(encrypted_bytes)):
        decrypted_bytes.append(encrypted_bytes[i] ^ key_bytes[i % len(key_bytes)])
    return decrypted_bytes.decode('utf-8')

# --- Main functions ---
def encrypt_secret(args):
    secret_value = args.value
    encryption_key = os.environ.get('DOCKER_SECRET_KEY')
    if not encryption_key:
        encryption_key = input(f"{Colors.BOLD}Enter encryption key (DOCKER_SECRET_KEY env var recommended):{Colors.ENDC} ")

    if not encryption_key:
        log_error("Encryption key is required.")
        sys.exit(1)

    try:
        encrypted_value = xor_encrypt_decrypt(secret_value, encryption_key)
        log_success(f"Encrypted secret for '{args.name}': {encrypted_value}")
        log_warn("WARNING: This encryption method (XOR) is for local development convenience ONLY and is NOT secure for production environments.")
        log_warn("For production, use Docker Secrets, Kubernetes Secrets, or dedicated secret management solutions.")
    except Exception as e:
        log_error(f"Encryption failed: {e}")
        sys.exit(1)

def decrypt_secret(args):
    encrypted_value = args.value
    encryption_key = os.environ.get('DOCKER_SECRET_KEY')
    if not encryption_key:
        encryption_key = input(f"{Colors.BOLD}Enter decryption key (DOCKER_SECRET_KEY env var recommended):{Colors.ENDC} ")

    if not encryption_key:
        log_error("Decryption key is required.")
        sys.exit(1)

    try:
        decrypted_value = xor_decrypt(encrypted_value, encryption_key)
        log_success(f"Decrypted secret: {decrypted_value}")
    except Exception as e:
        log_error(f"Decryption failed. Check key and encrypted value: {e}")
        sys.exit(1)

def inject_into_compose(args):
    compose_file = args.compose_file
    secret_name = args.name
    encrypted_value = args.value
    service_name = args.service

    encryption_key = os.environ.get('DOCKER_SECRET_KEY')
    if not encryption_key:
        encryption_key = input(f"{Colors.BOLD}Enter decryption key (DOCKER_SECRET_KEY env var recommended):{Colors.ENDC} ")

    if not encryption_key:
        log_error("Decryption key is required to inject secrets.")
        sys.exit(1)

    try:
        decrypted_value = xor_decrypt(encrypted_value, encryption_key)
    except Exception as e:
        log_error(f"Decryption failed. Cannot inject secret: {e}")
        sys.exit(1)

    if not os.path.exists(compose_file):
        log_error(f"Docker Compose file not found: {compose_file}")
        sys.exit(1)

    try:
        with open(compose_file, 'r') as f:
            compose_config = yaml.safe_load(f)

        if not compose_config or 'services' not in compose_config:
            log_error(f"Invalid or empty Docker Compose file: {compose_file}")
            sys.exit(1)

        if service_name not in compose_config['services']:
            log_error(f"Service '{service_name}' not found in {compose_file}")
            sys.exit(1)

        service = compose_config['services'][service_name]
        if 'environment' not in service:
            service['environment'] = {}
        service['environment'][secret_name] = decrypted_value

        if not args.dry_run:
            with open(compose_file, 'w') as f:
                yaml.dump(compose_config, f, default_flow_style=False, sort_keys=False)
            log_success(f"Secret '{secret_name}' injected into service '{service_name}' in {compose_file}")
        else:
            log_info(f"Dry-run: Secret '{secret_name}' would be injected into service '{service_name}' in {compose_file}")
            log_info("--- Modified docker-compose.yml (dry-run) ---")
            print(yaml.dump(compose_config, default_flow_style=False, sort_keys=False))
            log_info("---------------------------------------------")

    except yaml.YAMLError as e:
        log_error(f"Error parsing Docker Compose file: {e}")
        sys.exit(1)
    except Exception as e:
        log_error(f"Failed to inject secret into Docker Compose: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description="Docker Secret Manager for local development. WARNING: Uses simple XOR encryption, NOT for production!",
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument(
        "--key",
        help="Encryption/decryption key. Recommended to set via DOCKER_SECRET_KEY environment variable."
    )

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Encrypt command
    encrypt_parser = subparsers.add_parser('encrypt', help='Encrypt a secret value')
    encrypt_parser.add_argument('name', help='Name of the secret (e.g., DB_PASSWORD)')
    encrypt_parser.add_argument('value', help='The secret value to encrypt')
    encrypt_parser.set_defaults(func=encrypt_secret)

    # Decrypt command
    decrypt_parser = subparsers.add_parser('decrypt', help='Decrypt an encrypted secret value')
    decrypt_parser.add_argument('value', help='The encrypted secret value (hex string)')
    decrypt_parser.set_defaults(func=decrypt_secret)

    # Inject command
    inject_parser = subparsers.add_parser(
        'inject',
        help='Inject a decrypted secret into a Docker Compose service environment variables.'
    )
    inject_parser.add_argument('--compose-file', default='docker-compose.yml', help='Path to the docker-compose.yml file.')
    inject_parser.add_argument('--service', required=True, help='Name of the service in docker-compose.yml to inject into.')
    inject_parser.add_argument('name', help='Name of the environment variable (e.g., DB_PASSWORD)')
    inject_parser.add_argument('value', help='The encrypted secret value (hex string) to decrypt and inject.')
    inject_parser.add_argument('--dry-run', action='store_true', help='Show what would be changed without writing to file.')
    inject_parser.set_defaults(func=inject_into_compose)

    args = parser.parse_args()

    if args.key:
        os.environ['DOCKER_SECRET_KEY'] = args.key

    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
