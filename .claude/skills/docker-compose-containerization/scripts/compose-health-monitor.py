#!/usr/bin/env python3

# compose-health-monitor.py
#
# Purpose:
#   Continuously monitors the health status of all services defined in a
#   docker-compose.yml file. It reports the status and can optionally display
#   logs for unhealthy services, providing quick insights into application readiness.
#
# Pain Point Solved:
#   Simplifies debugging and verification of multi-service applications during
#   development and testing, avoiding manual `docker compose ps` and `docker compose logs` commands.
#
# Usage:
#   ./compose-health-monitor.py [--compose-file <path>] [--interval <seconds>] [--show-logs]
#
# Examples:
#   ./compose-health-monitor.py
#   ./compose-health-monitor.py --compose-file docker-compose.prod.yml --interval 10 --show-logs
#
# Configuration:
#   - COMPOSE_FILE: Path to the docker-compose.yml file (default: docker-compose.yml).
#   - INTERVAL: How often to check health status in seconds (default: 5).
#   - SHOW_LOGS: Flag to display logs for unhealthy services.

import argparse
import json
import subprocess
import sys
import time
import os

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
    print(f"{Color.OKBLUE}[INFO]{Color.ENDC} {message}")

def log_success(message):
    print(f"{Color.OKGREEN}[HEALTHY]{Color.ENDC} {message}")

def log_warning(message):
    print(f"{Color.WARNING}[STARTING]{Color.ENDC} {message}")

def log_error(message):
    print(f"{Color.FAIL}[UNHEALTHY]{Color.ENDC} {message}", file=sys.stderr)

def run_command(cmd, check=True, capture_output=True):
    """Helper to run shell commands."""
    try:
        result = subprocess.run(cmd, check=check, capture_output=capture_output, text=True, shell=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        if check:
            log_error(f"Command failed: {cmd}\nStdout: {e.stdout}\nStderr: {e.stderr}")
            sys.exit(1)
        return None
    except FileNotFoundError:
        log_error(f"Command not found. Is Docker installed and in your PATH? Command: {cmd.split()[0]}")
        sys.exit(1)

def get_service_health(compose_file):
    """Gets the health status of all services in a Docker Compose project."""
    cmd = f"docker compose -f {compose_file} ps --format json"
    output = run_command(cmd)
    
    if not output:
        return {}

    services_health = {}
    try:
        containers = json.loads(f"[{output.replace('}
{', '},{')}]")
        for container in containers:
            name = container.get('Service')
            health = container.get('Health', 'no healthcheck')
            state = container.get('State')
            if name:
                services_health[name] = {'health': health, 'state': state, 'id': container.get('ID')}
    except json.JSONDecodeError:
        log_error(f"Failed to parse JSON output from 'docker compose ps'. Output: {output}")
        return {}
    return services_health

def display_logs(container_id):
    """Displays logs for a given container ID."""
    log_info(f"Fetching logs for container {container_id}...")
    cmd = f"docker logs {container_id}"
    logs = run_command(cmd, check=False)
    if logs:
        print(f"{Color.BOLD}--- Logs for {container_id} ---"{Color.ENDC})
        print(logs)
        print(f"{Color.BOLD}--- End of Logs ---"{Color.ENDC})
    else:
        log_warning(f"No logs found for container {container_id}.")

def main():
    parser = argparse.ArgumentParser(
        description="Monitor the health status of Docker Compose services."
    )
    parser.add_argument(
        "--compose-file",
        default="docker-compose.yml",
        help="Path to the docker-compose.yml file (default: docker-compose.yml)"
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=5,
        help="Interval in seconds to check health status (default: 5)"
    )
    parser.add_argument(
        "--show-logs",
        action="store_true",
        help="Display logs for unhealthy services"
    )

    args = parser.parse_args()

    if not os.path.exists(args.compose_file):
        log_error(f"Compose file not found: {args.compose_file}")
        sys.exit(1)

    log_info(f"Monitoring services in {args.compose_file} every {args.interval} seconds...")
    log_info("Press Ctrl+C to stop.")

    try:
        while True:
            print("\n" + "="*50)
            log_info(f"Checking health status at {time.strftime('%Y-%m-%d %H:%M:%S')}")
            services = get_service_health(args.compose_file)
            
            if not services:
                log_warning("No services found or running. Ensure your Docker Compose project is up.")
            
            all_healthy = True
            for service_name, data in services.items():
                health_status = data['health']
                container_state = data['state']
                container_id = data['id']

                if health_status == 'healthy':
                    log_success(f"Service '{service_name}' ({container_state})")
                elif health_status == 'unhealthy':
                    log_error(f"Service '{service_name}' ({container_state})")
                    all_healthy = False
                    if args.show_logs and container_id:
                        display_logs(container_id)
                elif health_status == 'starting':
                    log_warning(f"Service '{service_name}' ({container_state})")
                    all_healthy = False
                else: # no healthcheck or unknown status
                    log_info(f"Service '{service_name}' ({container_state}) - {health_status}")

            if all_healthy and services:
                log_success("All monitored services are healthy.")
            
            time.sleep(args.interval)

    except KeyboardInterrupt:
        log_info("Monitoring stopped by user.")
    except Exception as e:
        log_error(f"An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
