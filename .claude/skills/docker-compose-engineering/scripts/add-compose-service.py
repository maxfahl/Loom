#!/usr/bin/env python3

"""
add-compose-service.py

Purpose:
  Adds a new service definition to an existing docker-compose.yml file.
  This script helps automate the process of extending a multi-container application
  by adding new services with their configurations (image, ports, volumes, environment variables).

Usage:
  python3 add-compose-service.py <service_name> --image <image_name> [--file <path/to/docker-compose.yml>] 
    [--ports <host_port:container_port>] [--volumes <host_path:container_path>] 
    [--env <KEY=VALUE>] [--depends-on <service_name>] [--healthcheck-cmd <command>] 
    [--healthcheck-interval <duration>] [--healthcheck-timeout <duration>] 
    [--healthcheck-retries <count>]

Arguments:
  <service_name>       : The name of the new service (e.g., api, redis, worker).
  --image              : The Docker image for the service (e.g., nginx:alpine, myapp:latest).
  --file               : (Optional) Path to the docker-compose.yml file. Defaults to './docker-compose.yml'.
  --ports              : (Optional) Port mappings, e.g., '8080:80'. Can be specified multiple times.
  --volumes            : (Optional) Volume mappings, e.g., './data:/var/lib/data'. Can be specified multiple times.
  --env                : (Optional) Environment variables, e.g., 'DEBUG=true'. Can be specified multiple times.
  --depends-on         : (Optional) Service name this new service depends on. Can be specified multiple times.
  --healthcheck-cmd    : (Optional) Command for healthcheck, e.g., 'CMD curl -f http://localhost/ || exit 1'.
  --healthcheck-interval: (Optional) Healthcheck interval (e.g., 30s).
  --healthcheck-timeout: (Optional) Healthcheck timeout (e.g., 10s).
  --healthcheck-retries: (Optional) Healthcheck retries (e.g., 5).
  --help               : Show this help message and exit.

Examples:
  python3 add-compose-service.py myapp --image myapp:latest --ports 8000:80 --env DEBUG=true
  python3 add-compose-service.py worker --image myworker:1.0 --env QUEUE_NAME=tasks --depends-on redis
  python3 add-compose-service.py monitoring --image prom/prometheus --ports 9090:9090 
    --volumes ./prometheus.yml:/etc/prometheus/prometheus.yml --healthcheck-cmd 'CMD curl -f http://localhost:9090/-/ready || exit 1'

Features:
  - Adds a new service to an existing docker-compose.yml.
  - Supports image, ports, volumes, environment variables, and dependencies.
  - Can add healthcheck configuration.
  - Preserves comments and formatting where possible (using roundtrip_dump).
  - Includes basic error handling and verbose output.

Dependencies:
  - Python 3.x
  - PyYAML library (pip install pyyaml)
"""

import argparse
import os
import sys
import ruamel.yaml # For preserving comments and order

def main():
    parser = argparse.ArgumentParser(
        description="Add a new service definition to an existing docker-compose.yml file.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "service_name",
        help="The name of the new service (e.g., api, redis, worker)."
    )
    parser.add_argument(
        "--image",
        required=True,
        help="The Docker image for the service (e.g., nginx:alpine, myapp:latest)."
    )
    parser.add_argument(
        "--file",
        default="docker-compose.yml",
        help="Path to the docker-compose.yml file. Defaults to './docker-compose.yml'."
    )
    parser.add_argument(
        "--ports",
        action="append",
        help="Port mappings, e.g., '8080:80'. Can be specified multiple times."
    )
    parser.add_argument(
        "--volumes",
        action="append",
        help="Volume mappings, e.g., './data:/var/lib/data'. Can be specified multiple times."
    )
    parser.add_argument(
        "--env",
        action="append",
        help="Environment variables, e.g., 'DEBUG=true'. Can be specified multiple times."
    )
    parser.add_argument(
        "--depends-on",
        action="append",
        help="Service name this new service depends on. Can be specified multiple times."
    )
    parser.add_argument(
        "--healthcheck-cmd",
        help="Command for healthcheck, e.g., 'CMD curl -f http://localhost/ || exit 1'."
    )
    parser.add_argument(
        "--healthcheck-interval",
        help="Healthcheck interval (e.g., 30s)."
    )
    parser.add_argument(
        "--healthcheck-timeout",
        help="Healthcheck timeout (e.g., 10s)."
    )
    parser.add_argument(
        "--healthcheck-retries",
        type=int,
        help="Healthcheck retries (e.g., 5)."
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

    if service_name in data['services']:
        print(f"Error: Service '{service_name}' already exists in {compose_file_path}", file=sys.stderr)
        sys.exit(1)

    new_service = ruamel.yaml.comments.CommentedMap()
    new_service['image'] = args.image

    if args.ports:
        new_service['ports'] = ruamel.yaml.comments.CommentedSeq(args.ports)
    if args.volumes:
        new_service['volumes'] = ruamel.yaml.comments.CommentedSeq(args.volumes)
    if args.env:
        new_service['environment'] = ruamel.yaml.comments.CommentedSeq(args.env)
    if args.depends_on:
        new_service['depends_on'] = ruamel.yaml.comments.CommentedSeq(args.depends_on)

    if args.healthcheck_cmd:
        healthcheck = ruamel.yaml.comments.CommentedMap()
        healthcheck['test'] = ruamel.yaml.comments.CommentedSeq(args.healthcheck_cmd.split())
        if args.healthcheck_interval: healthcheck['interval'] = args.healthcheck_interval
        if args.healthcheck_timeout: healthcheck['timeout'] = args.healthcheck_timeout
        if args.healthcheck_retries: healthcheck['retries'] = args.healthcheck_retries
        new_service['healthcheck'] = healthcheck

    data['services'][service_name] = new_service

    if args.dry_run:
        print(f"[DRY RUN] Would add service '{service_name}' to {compose_file_path}. Content would be:\n")
        yaml.dump(data, sys.stdout)
        print("\nNo file was modified.")
    else:
        try:
            with open(compose_file_path, 'w', encoding='utf-8') as f:
                yaml.dump(data, f)
            print(f"Successfully added service '{service_name}' to {compose_file_path}")
        except IOError as e:
            print(f"Error writing to file {compose_file_path}: {e}", file=sys.stderr)
            sys.exit(1)

if __name__ == "__main__":
    main()
