#!/usr/bin/env python3

# compose-env-sync.py
#
# Purpose:
#   Analyzes a docker-compose.yml file to identify all environment variables used
#   and compares them against a .env file. It can generate a .env.example file
#   or report missing variables, ensuring consistency across environments.
#
# Pain Point Solved:
#   Prevents issues caused by missing or inconsistent environment variables,
#   especially in team environments or CI/CD pipelines.
#
# Usage:
#   ./compose-env-sync.py [--compose-file <path>] [--env-file <path>] [--generate-example] [--check-missing]
#
# Examples:
#   ./compose-env-sync.py --generate-example
#   ./compose-env-sync.py --check-missing --env-file .env.production
#
# Configuration:
#   - COMPOSE_FILE: Path to the docker-compose.yml file (default: docker-compose.yml).
#   - ENV_FILE: Path to the .env file (default: .env).
#   - GENERATE_EXAMPLE: Flag to generate or update .env.example.
#   - CHECK_MISSING: Flag to check for missing variables.

import argparse
import os
import re
import sys
import yaml

class Color:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def log_info(message):
    print(f"{Color.OKBLUE}[INFO] {Color.ENDC} {message}")

def log_success(message):
    print(f"{Color.OKGREEN}[SUCCESS] {Color.ENDC} {message}")

def log_warning(message):
    print(f"{Color.WARNING}[WARNING] {Color.ENDC} {message}")

def log_error(message):
    print(f"{Color.FAIL}[ERROR] {Color.ENDC} {message}", file=sys.stderr)

def parse_compose_file(compose_file_path):
    """Parses the docker-compose.yml file and extracts all referenced environment variables."""
    env_vars = set()
    try:
        with open(compose_file_path, 'r') as f:
            compose_content = f.read()
        
        # Use regex to find ${VAR} or $VAR patterns
        # This is more robust than YAML parsing for direct variable references
        # and also catches variables in commands, arguments, etc.
        matches = re.findall(r'\${?([a-zA-Z_][a-zA-Z0-9_]*)}?', compose_content)
        env_vars.update(matches)

        # Also parse environment section explicitly
        config = yaml.safe_load(compose_content)
        if isinstance(config, dict) and 'services' in config:
            for service_name, service_config in config['services'].items():
                if isinstance(service_config, dict) and 'environment' in service_config:
                    for env_var_entry in service_config['environment']:
                        if isinstance(env_var_entry, str):
                            # Format: VAR=value or VAR
                            match = re.match(r'^([a-zA-Z_][a-zA-Z0-9_]*)(?:=.*)?$', env_var_entry)
                            if match: 
                                env_vars.add(match.group(1))
                        elif isinstance(env_var_entry, dict):
                            # Format: {VAR: value}
                            env_vars.update(env_var_entry.keys())

    except FileNotFoundError:
        log_error(f"Compose file not found: {compose_file_path}")
        sys.exit(1)
    except yaml.YAMLError as e:
        log_error(f"Error parsing YAML in {compose_file_path}: {e}")
        sys.exit(1)
    except Exception as e:
        log_error(f"An unexpected error occurred while parsing {compose_file_path}: {e}")
        sys.exit(1)

    return sorted(list(env_vars))

def parse_env_file(env_file_path):
    """Parses a .env file and extracts defined environment variables."""
    env_vars = set()
    if not os.path.exists(env_file_path):
        return env_vars # Return empty set if file doesn't exist

    try:
        with open(env_file_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    match = re.match(r'^([a-zA-Z_][a-zA-Z0-9_]*)=.*$', line)
                    if match:
                        env_vars.add(match.group(1))
    except Exception as e:
        log_error(f"An unexpected error occurred while parsing {env_file_path}: {e}")
        sys.exit(1)
    return env_vars

def generate_env_example(compose_vars, example_file_path):
    """Generates or updates a .env.example file with variables from compose_vars."""
    log_info(f"Generating/updating {example_file_path}...")
    existing_example_vars = parse_env_file(example_file_path)
    
    updated_content = []
    # Preserve comments and order of existing variables if possible
    if os.path.exists(example_file_path):
        with open(example_file_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line.startswith('#') or not line:
                    updated_content.append(line)
                else:
                    var_name = line.split('=', 1)[0]
                    if var_name in compose_vars:
                        updated_content.append(f"{var_name}=") # Keep existing, but clear value
                        compose_vars.remove(var_name)
                    else:
                        # Variable no longer in compose file, keep as comment
                        updated_content.append(f"# {line} # Removed from compose file")
    
    # Add any new variables from compose_vars
    if compose_vars:
        if updated_content and updated_content[-1]: # Add a newline if content exists
            updated_content.append("")
        updated_content.append("# New variables from docker-compose.yml")
        for var in sorted(list(compose_vars)):
            updated_content.append(f"{var}=")

    try:
        with open(example_file_path, 'w') as f:
            f.write("\n".join(updated_content))
        log_success(f"Successfully generated/updated {example_file_path}")
    except Exception as e:
        log_error(f"Failed to write to {example_file_path}: {e}")
        sys.exit(1)

def check_missing_variables(compose_vars, env_vars, env_file_path):
    """Checks for variables in compose_vars that are missing in env_vars."""
    missing_in_env = [var for var in compose_vars if var not in env_vars]
    if missing_in_env:
        log_warning(f"The following variables are used in docker-compose.yml but are missing in {env_file_path}:")
        for var in missing_in_env:
            print(f"  - {var}")
        return False
    else:
        log_success(f"All variables used in docker-compose.yml are present in {env_file_path}.")
        return True

def main():
    parser = argparse.ArgumentParser(
        description="Synchronize environment variables between docker-compose.yml and .env files."
    )
    parser.add_argument(
        "--compose-file",
        default="docker-compose.yml",
        help="Path to the docker-compose.yml file (default: docker-compose.yml)"
    )
    parser.add_argument(
        "--env-file",
        default=".env",
        help="Path to the .env file (default: .env)"
    )
    parser.add_argument(
        "--generate-example",
        action="store_true",
        help="Generate or update .env.example with all variables found in docker-compose.yml"
    )
    parser.add_argument(
        "--check-missing",
        action="store_true",
        help="Check for variables used in docker-compose.yml but missing in the .env file"
    )

    args = parser.parse_args()

    log_info(f"Analyzing compose file: {args.compose_file}")
    compose_vars = parse_compose_file(args.compose_file)
    log_info(f"Found {len(compose_vars)} unique environment variables in {args.compose_file}.")

    if args.generate_example:
        generate_env_example(set(compose_vars), ".env.example")
    
    if args.check_missing:
        log_info(f"Checking for missing variables in {args.env_file}...")
        env_vars = parse_env_file(args.env_file)
        check_missing_variables(compose_vars, env_vars, args.env_file)

    if not args.generate_example and not args.check_missing:
        log_info("No action specified. Use --generate-example or --check-missing.")
        parser.print_help()

if __name__ == "__main__":
    main()
