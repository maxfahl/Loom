#!/usr/bin/env python3
"""
docker-healthcheck-tester.py: A Python script to test Docker Compose healthchecks locally.

This script parses a `docker-compose.yml` file, extracts healthcheck configurations
for each service, and then attempts to execute these healthcheck commands locally
(or simulate their execution) to verify their correctness and expected behavior.
This helps in debugging healthcheck configurations before deployment.

Usage:
    python3 docker-healthcheck-tester.py -f <docker-compose.yml> [--service <service_name>] [--verbose]

Examples:
    # Test healthchecks for all services in docker-compose.dev.yml
    python3 docker-healthcheck-tester.py -f ../examples/docker-compose.dev.yml

    # Test healthcheck for a specific service (e.g., 'app')
    python3 docker-healthcheck-tester.py -f ../examples/docker-compose.dev.yml --service app

    # Test with verbose output
    python3 docker-healthcheck-tester.py -f ../examples/docker-compose.dev.yml --verbose

Configuration:
    - Requires `docker-compose.yml` file with healthcheck definitions.
    - The script attempts to execute the healthcheck commands directly. Ensure necessary
      executables (e.g., `curl`, `pg_isready`) are available in the environment where
      the script is run, or mock them for testing.

Error Handling:
    - Exits if the Docker Compose file is not found or is invalid YAML.
    - Reports success or failure for each healthcheck tested.

Dependencies:
    - PyYAML (install with: `pip install PyYAML`)
    - subprocess (built-in)
    - argparse (built-in)
    - os (built-in)
    - sys (built-in)
"""

import argparse
import os
import sys
import yaml
import subprocess
import time

# Colors for output
RED = '\033[0;31m'
GREEN = '\033[0;32m'
YELLOW = '\033[0;33m'
NC = '\033[0m' # No Color

def log_error(message):
    print(f"{RED}ERROR: {message}{NC}", file=sys.stderr)

def log_warning(message):
    print(f"{YELLOW}WARNING: {message}{NC}", file=sys.stderr)

def log_info(message, verbose):
    if verbose:
        print(f"{GREEN}INFO: {message}{NC}")

def parse_docker_compose(file_path: str) -> dict:
    """Parses a docker-compose.yml file and returns its content."""
    try:
        with open(file_path, 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        log_error(f"Docker Compose file not found at '{file_path}'")
        sys.exit(1)
    except yaml.YAMLError as e:
        log_error(f"Invalid YAML in Docker Compose file '{file_path}': {e}")
        sys.exit(1)
    except Exception as e:
        log_error(f"Error reading Docker Compose file '{file_path}': {e}")
        sys.exit(1)

def execute_healthcheck_command(command: list, service_name: str, verbose: bool) -> bool:
    """Executes a healthcheck command and returns True if successful, False otherwise."""
    log_info(f"  Executing healthcheck for '{service_name}': {' '.join(command)}", verbose)
    try:
        # Use shell=True for CMD-SHELL, otherwise pass as list
        if command[0] == "CMD-SHELL":
            result = subprocess.run(command[1], shell=True, capture_output=True, text=True, check=False)
        elif command[0] == "CMD":
            result = subprocess.run(command[1:], capture_output=True, text=True, check=False)
        else:
            log_warning(f"  Unsupported healthcheck command type for '{service_name}': {command[0]}. Only CMD and CMD-SHELL are supported.")
            return False

        if verbose:
            log_info(f"    Stdout: {result.stdout.strip()}", verbose)
            log_info(f"    Stderr: {result.stderr.strip()}", verbose)

        if result.returncode == 0:
            log_info(f"  Healthcheck for '{service_name}' PASSED.", verbose)
            return True
        else:
            log_warning(f"  Healthcheck for '{service_name}' FAILED with exit code {result.returncode}.")
            return False
    except FileNotFoundError:
        log_warning(f"  Healthcheck command executable not found for '{service_name}'. Ensure it's in your PATH.")
        return False
    except Exception as e:
        log_warning(f"  Error executing healthcheck for '{service_name}': {e}")
        return False

def main():
    parser = argparse.ArgumentParser(
        description="Test Docker Compose healthchecks locally.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "-f", "--file",
        required=True,
        help="Path to the docker-compose.yml file."
    )
    parser.add_argument(
        "--service",
        help="Optional: Name of a specific service to test. If omitted, all services with healthchecks are tested."
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output."
    )

    args = parser.parse_args()

    compose_config = parse_docker_compose(args.file)

    if "services" not in compose_config:
        log_error("No services found in the Docker Compose file.")
        sys.exit(1)

    services_to_test = {}
    if args.service:
        if args.service in compose_config["services"]:
            services_to_test[args.service] = compose_config["services"][args.service]
        else:
            log_error(f"Service '{args.service}' not found in the Docker Compose file.")
            sys.exit(1)
    else:
        services_to_test = compose_config["services"]

    overall_status = True
    print(f"\n{GREEN}--- Starting Healthcheck Test ---{NC}")

    for service_name, service_config in services_to_test.items():
        if "healthcheck" in service_config and "test" in service_config["healthcheck"]:
            healthcheck_command = service_config["healthcheck"]["test"]
            interval = service_config["healthcheck"].get("interval", "30s")
            timeout = service_config["healthcheck"].get("timeout", "30s")
            retries = service_config["healthcheck"].get("retries", 3)

            print(f"\n{YELLOW}Testing healthcheck for service: {service_name}{NC}")
            log_info(f"  Command: {healthcheck_command}", args.verbose)
            log_info(f"  Interval: {interval}, Timeout: {timeout}, Retries: {retries}", args.verbose)

            # Simulate retries
            service_passed = False
            for i in range(retries):
                log_info(f"  Attempt {i + 1}/{retries}...", args.verbose)
                if execute_healthcheck_command(healthcheck_command, service_name, args.verbose):
                    service_passed = True
                    break
                if i < retries - 1:
                    time.sleep(1) # Small delay between retries for local testing

            if service_passed:
                print(f"{GREEN}Healthcheck for '{service_name}' PASSED.{NC}")
            else:
                print(f"{RED}Healthcheck for '{service_name}' FAILED after {retries} attempts.{NC}")
                overall_status = False
        else:
            log_info(f"Service '{service_name}' has no healthcheck defined. Skipping.", args.verbose)

    print(f"\n{GREEN}--- Healthcheck Test Finished ---{NC}")
    if overall_status:
        print(f"{GREEN}All specified healthchecks passed successfully.{NC}")
        sys.exit(0)
    else:
        print(f"{RED}Some healthchecks failed. Please review the output above.{NC}")
        sys.exit(1)

if __name__ == "__main__":
    main()
