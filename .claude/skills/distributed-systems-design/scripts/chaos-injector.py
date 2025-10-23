#!/usr/bin/env python3

# chaos-injector.py
#
# Purpose:
#   A simple fault injection script to simulate network latency or service unavailability
#   for a given service. This helps in testing the resilience and fault tolerance
#   of distributed systems.
#
# Usage:
#   python3 chaos-injector.py <service_host> [--latency <ms>] [--unavailability <seconds>] [--port <port>] [--dry-run] [--help]
#
# Examples:
#   python3 chaos-injector.py my-service.example.com --latency 200 --port 8080
#   python3 chaos-injector.py 127.0.0.1 --unavailability 30
#   python3 chaos-injector.py backend-api --latency 500 --unavailability 10
#   python3 chaos-injector.py --help
#
# Configuration:
#   - Default port: 80 (can be overridden with --port)
#   - Latency: milliseconds to delay responses.
#   - Unavailability: seconds to make the service unreachable.
#
# Error Handling:
#   - Exits if service host is not provided.
#   - Validates input parameters.
#   - Provides clear error messages.
#
# Dry-run mode:
#   - With --dry-run, the script will print the commands it *would* execute
#     without actually modifying the system.
#
# Colored Output:
#   Uses ANSI escape codes for colored output (green for success, red for error, yellow for warnings, blue for info).

import argparse
import subprocess
import sys
import time

# --- Colors for output ---
GREEN = "\033[0;32m"
RED = "\033[0;31m"
YELLOW = "\033[0;33m"
BLUE = "\033[0;34m"
NC = "\033[0m" # No Color

def log_success(message):
    print(f"{GREEN}[SUCCESS]${NC} {message}")

def log_error(message):
    print(f"{RED}[ERROR]${NC} {message}", file=sys.stderr)
    sys.exit(1)

def log_warning(message):
    print(f"{YELLOW}[WARNING]${NC} {message}")

def log_info(message):
    print(f"{BLUE}[INFO]${NC} {message}")

def run_command(command, dry_run=False, description=""):
    log_info(f"Executing: {command}")
    if dry_run:
        log_warning(f"Dry-run: Skipping command execution: {command}")
        return True
    try:
        subprocess.run(command, shell=True, check=True, capture_output=True)
        log_success(f"Command executed successfully: {description}")
        return True
    except subprocess.CalledProcessError as e:
        log_error(f"Command failed: {description}\nStdout: {e.stdout.decode()}\nStderr: {e.stderr.decode()}")
        return False
    except FileNotFoundError:
        log_error(f"Command not found. Make sure 'sudo' and 'tc' (iproute2) are installed and in your PATH.")
        return False

def main():
    parser = argparse.ArgumentParser(
        description="Simulate network chaos (latency or unavailability) for a service.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("service_host", help="The hostname or IP address of the service to target.")
    parser.add_argument("--latency", type=int, default=0,
                        help="Add network latency in milliseconds (e.g., 200).")
    parser.add_argument("--unavailability", type=int, default=0,
                        help="Make the service unavailable for N seconds (e.g., 30).")
    parser.add_argument("--port", type=int, default=80,
                        help="The port of the service to target (default: 80).")
    parser.add_argument("--dry-run", action="store_true",
                        help="Print commands without executing them.")
    parser.add_argument("--interface", type=str, default="eth0",
                        help="Network interface to apply rules to (default: eth0)."
    )

    args = parser.parse_args()

    if not args.latency and not args.unavailability:
        log_error("Either --latency or --unavailability must be specified.")

    log_info(f"Targeting service: {args.service_host}:{args.port}")

    # --- Apply Chaos ---
    if args.latency > 0:
        log_info(f"Injecting {args.latency}ms latency to {args.service_host}:{args.port}...")
        # Add latency using tc (traffic control)
        # This command adds a netem (network emulation) delay to the specified interface
        # for traffic destined to the service host and port.
        add_latency_cmd = (
            f"sudo tc qdisc add dev {args.interface} root handle 1: prio && "
            f"sudo tc filter add dev {args.interface} protocol ip parent 1:0 prio 1 u32 "
            f"match ip dst {args.service_host} match ip dport {args.port} 0xffff flowid 1:1 && "
            f"sudo tc qdisc add dev {args.interface} parent 1:1 handle 10: netem delay {args.latency}ms"
        )
        if not run_command(add_latency_cmd, args.dry_run, f"Add {args.latency}ms latency to {args.service_host}:{args.port}"):
            log_error("Failed to inject latency. Ensure 'iproute2' is installed and you have sudo privileges.")

    if args.unavailability > 0:
        log_info(f"Making {args.service_host}:{args.port} unavailable for {args.unavailability} seconds...")
        # Block traffic using iptables
        block_cmd = f"sudo iptables -A OUTPUT -d {args.service_host} -p tcp --dport {args.port} -j DROP"
        if not run_command(block_cmd, args.dry_run, f"Block traffic to {args.service_host}:{args.port}"):
            log_error("Failed to block traffic. Ensure 'iptables' is installed and you have sudo privileges.")

        log_info(f"Service {args.service_host}:{args.port} will be unavailable for {args.unavailability} seconds.")
        if not args.dry_run:
            time.sleep(args.unavailability)

        log_info(f"Restoring availability for {args.service_host}:{args.port}...")
        # Unblock traffic using iptables
        unblock_cmd = f"sudo iptables -D OUTPUT -d {args.service_host} -p tcp --dport {args.port} -j DROP"
        if not run_command(unblock_cmd, args.dry_run, f"Unblock traffic to {args.service_host}:{args.port}"):
            log_error("Failed to unblock traffic. Manual intervention might be required.")

    # --- Clean up latency rules ---
    if args.latency > 0:
        log_info(f"Cleaning up latency rules for {args.service_host}:{args.port}...")
        # Delete tc rules
        delete_latency_cmd = f"sudo tc qdisc del dev {args.interface} root"
        if not run_command(delete_latency_cmd, args.dry_run, f"Remove latency rules from {args.interface}"):
            log_warning("Failed to remove latency rules. Manual cleanup might be required.")

    log_success("Chaos injection complete.")

if __name__ == "__main__":
    main()
