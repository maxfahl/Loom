#!/usr/bin/env python3

"""
add-compose-healthcheck.py

Purpose:
  Adds or updates a health check configuration for a specified service
  in an existing docker-compose.yml file.

This script helps ensure that Docker can accurately determine the health
status of your services, enabling proper orchestration and automatic restarts.

Usage:
  python3 add-compose-healthcheck.py <service_name> --command <healthcheck_command> 
    [--file <path/to/docker-compose.yml>] [--interval <duration>] 
    [--timeout <duration>] [--retries <count>]

Arguments:
  <service_name>       : The name of the service to add/update the health check for.
  --command            : The health check command (e.g., 'CMD curl -f http://localhost/ || exit 1').
  --file               : (Optional) Path to the docker-compose.yml file. Defaults to './docker-compose.yml'.
  --interval           : (Optional) Healthcheck interval (e.g., 30s). Defaults to 30s.
  --timeout            : (Optional) Healthcheck timeout (e.g., 10s). Defaults to 10s.
  --retries            : (Optional) Healthcheck retries (e.g., 5). Defaults to 3.
  --help               : Show this help message and exit.

Examples:
  python3 add-compose-healthcheck.py web --command 'CMD curl -f http://localhost/ || exit 1'
  python3 add-compose-healthcheck.py db --command 'CMD pg_isready -U user -d mydatabase' --interval 5s --timeout 3s --retries 5

Features:
  - Adds or updates health check configuration for a service.
  - Supports command, interval, timeout, and retries.
  - Preserves comments and formatting where possible (using ruamel.yaml).
  - Includes basic error handling and verbose output.

Dependencies:
  - Python 3.x
  - ruamel.yaml library (pip install ruamel.yaml)
"""

import argparse
import os
import sys
import ruamel.yaml

def main():
    parser = argparse.ArgumentParser(
        description="Add or update a health check configuration for a specified service in a docker-compose.yml file.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "service_name",
        help="The name of the service to add/update the health check for."
    )
    parser.add_argument(
        "--command",
        required=True,
        help="The health check command (e.g., 'CMD curl -f http://localhost/ || exit 1')."
    )
    parser.add_argument(
        "--file",
        default="docker-compose.yml",
        help="Path to the docker-compose.yml file. Defaults to './docker-compose.yml'."
    )
    parser.add_argument(
        "--interval",
        default="30s",
        help="Healthcheck interval (e.g., 30s). Defaults to 30s."
    )
    parser.add_argument(
        "--timeout",
        default="10s",
        help="Healthcheck timeout (e.g., 10s). Defaults to 10s."
    )
    parser.add_argument(
        "--retries",
        type=int,
        default=3,
        help="Healthcheck retries (e.g., 5). Defaults to 3."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Perform a dry run without modifying the file."
    )

    args = parser.parse_args()

    compose_file_path = args.file
    service_name = args.service_name

    if not os.path.exists(compose_file_path):
        print(f"Error: docker-compose.yml file not found at {compose_file_path}", file=sys.stderr)
        sys.exit(1)

    yaml = ruamel.yaml.YAML()
    yaml.preserve_quotes = True
    yaml.indent(mapping=2, sequence=4, offset=2)

    try:
        with open(compose_file_path, 'r', encoding='utf-8') as f:
            data = yaml.load(f)
    except ruamel.yaml.YAMLError as e:
        print(f"Error parsing YAML file {compose_file_path}: {e}", file=sys.stderr)
        sys.exit(1)

    if 'services' not in data or not isinstance(data['services'], dict):
        print(f"Error: 'services' section not found or not a dictionary in {compose_file_path}", file=sys.stderr)
        sys.exit(1)

    if service_name not in data['services']:
        print(f"Error: Service '{service_name}' not found in {compose_file_path}", file=sys.stderr)
        sys.exit(1)

    service = data['services'][service_name]

    healthcheck = ruamel.yaml.comments.CommentedMap()
    healthcheck['test'] = ruamel.yaml.comments.CommentedSeq(args.command.split())
    healthcheck['interval'] = args.interval
    healthcheck['timeout'] = args.timeout
    healthcheck['retries'] = args.retries

    service['healthcheck'] = healthcheck

    if args.dry_run:
        print(f"[DRY RUN] Would add/update health check for service '{service_name}' in {compose_file_path}. Content would be:\n")
        yaml.dump(data, sys.stdout)
        print("\nNo file was modified.")
    else:
        try:
            with open(compose_file_path, 'w', encoding='utf-8') as f:
                yaml.dump(data, f)
            print(f"Successfully added/updated health check for service '{service_name}' in {compose_file_path}")
        except IOError as e:
            print(f"Error writing to file {compose_file_path}: {e}", file=sys.stderr)
            sys.exit(1)

if __name__ == "__main__":
    main()
