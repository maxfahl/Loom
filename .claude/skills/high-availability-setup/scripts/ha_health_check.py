#!/usr/bin/env python3

"""
HA Health Check Script

This script performs health checks on critical High Availability (HA) components
like HTTP/HTTPS endpoints and can be extended for database connectivity or other services.
It reports the status and can be integrated into monitoring or alerting systems.

Usage:
    python3 ha_health_check.py --config health_checks.json
    python3 ha_health_check.py --url https://example.com --type http
    python3 ha_health_check.py -h # For help

Configuration File (health_checks.json example):
    [
        {
            "name": "Web Server HTTP",
            "type": "http",
            "url": "http://localhost:80",
            "expected_status": 200,
            "timeout": 5
        },
        {
            "name": "API Endpoint HTTPS",
            "type": "https",
            "url": "https://api.example.com/health",
            "expected_status": 200,
            "timeout": 10
        },
        {
            "name": "Database TCP Port",
            "type": "tcp",
            "host": "db.example.com",
            "port": 5432,
            "timeout": 3
        }
    ]

Features:
- Supports HTTP/HTTPS and TCP health checks.
- Configurable via command-line arguments or a JSON configuration file.
- Customizable expected status codes and timeouts.
- Reports success or failure with clear messages.
- Exits with a non-zero status code on failure for CI/CD integration.
"""

import argparse
import json
import sys
import socket
import time
import os

try:
    import requests
except ImportError:
    print("Error: 'requests' library not found. Please install it: pip install requests", file=sys.stderr)
    sys.exit(1)

class HealthChecker:
    def __init__(self, timeout=5):
        self.timeout = timeout

    def check_http(self, url, expected_status=200):
        try:
            response = requests.get(url, timeout=self.timeout)
            if response.status_code == expected_status:
                return True, f"HTTP check successful. Status: {response.status_code}"
            else:
                return False, f"HTTP check failed. Expected {expected_status}, got {response.status_code}"
        except requests.exceptions.RequestException as e:
            return False, f"HTTP request failed: {e}"

    def check_https(self, url, expected_status=200):
        # HTTPS check is essentially the same as HTTP with requests library
        return self.check_http(url, expected_status)

    def check_tcp(self, host, port):
        try:
            with socket.create_connection((host, port), timeout=self.timeout):
                return True, f"TCP check successful. Connected to {host}:{port}"
        except socket.error as e:
            return False, f"TCP connection failed to {host}:{port}: {e}"

    def check_db(self, db_type, host, port, user, password, db_name):
        # Placeholder for database checks. Requires specific database drivers.
        # Example for PostgreSQL (requires psycopg2):
        # import psycopg2
        # try:
        #     conn = psycopg2.connect(host=host, port=port, user=user, password=password, dbname=db_name, connect_timeout=self.timeout)
        #     conn.close()
        #     return True, f"DB check successful. Connected to {db_type} at {host}:{port}"
        # except psycopg2.Error as e:
        #     return False, f"DB connection failed to {db_type} at {host}:{port}: {e}"
        return False, f"DB check for {db_type} not implemented in this script. Requires specific driver."

def run_check(checker, check_config):
    check_type = check_config["type"].lower()
    check_name = check_config.get("name", f"{check_type} check")
    timeout = check_config.get("timeout", checker.timeout)

    checker.timeout = timeout # Update checker timeout for this specific check

    print(f"Running check: {check_name}...")

    success = False
    message = ""

    if check_type == "http":
        success, message = checker.check_http(
            check_config["url"],
            check_config.get("expected_status", 200)
        )
    elif check_type == "https":
        success, message = checker.check_https(
            check_config["url"],
            check_config.get("expected_status", 200)
        )
    elif check_type == "tcp":
        success, message = checker.check_tcp(
            check_config["host"],
            check_config["port"]
        )
    elif check_type == "db":
        # Example for DB check, needs actual implementation with drivers
        success, message = checker.check_db(
            check_config.get("db_type", "generic"),
            check_config["host"],
            check_config["port"],
            check_config.get("user"),
            check_config.get("password"),
            check_config.get("db_name")
        )
    else:
        success = False
        message = f"Unknown check type: {check_type}"

    if success:
        print(f"  ✅ {check_name}: {message}")
    else:
        print(f"  ❌ {check_name}: {message}", file=sys.stderr)

    return success

def main():
    parser = argparse.ArgumentParser(
        description="Perform health checks on HA components.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "--config",
        help="Path to a JSON configuration file containing a list of checks."
    )
    parser.add_argument(
        "--url",
        help="URL for a single HTTP/HTTPS check."
    )
    parser.add_argument(
        "--type",
        choices=["http", "https", "tcp", "db"],
        help="Type of check for a single check (http, https, tcp, db). Required with --url/--host."
    )
    parser.add_argument(
        "--host",
        help="Host for a single TCP/DB check."
    )
    parser.add_argument(
        "--port",
        type=int,
        help="Port for a single TCP/DB check."
    )
    parser.add_argument(
        "--expected-status",
        type=int,
        default=200,
        help="Expected HTTP status code for HTTP/HTTPS checks. Default: 200"
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=5,
        help="Timeout in seconds for each check. Default: 5"
    )

    args = parser.parse_args()

    checker = HealthChecker(timeout=args.timeout)
    all_checks_passed = True
    checks_to_run = []

    if args.config:
        if not os.path.exists(args.config):
            print(f"Error: Configuration file not found at '{args.config}'.", file=sys.stderr)
            sys.exit(1)
        try:
            with open(args.config, 'r') as f:
                checks_to_run = json.load(f)
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON in configuration file '{args.config}': {e}", file=sys.stderr)
            sys.exit(1)
    elif args.url or args.host:
        if not args.type:
            print("Error: --type is required when specifying --url or --host.", file=sys.stderr)
            sys.exit(1)
        single_check = {"type": args.type, "timeout": args.timeout}
        if args.url:
            single_check["url"] = args.url
            single_check["expected_status"] = args.expected_status
        if args.host:
            single_check["host"] = args.host
        if args.port:
            single_check["port"] = args.port
        checks_to_run.append(single_check)
    else:
        print("Error: Either --config or (--url/--host and --type) must be provided.", file=sys.stderr)
        parser.print_help()
        sys.exit(1)

    if not checks_to_run:
        print("No health checks defined to run.", file=sys.stderr)
        sys.exit(1)

    for check_config in checks_to_run:
        if not run_check(checker, check_config):
            all_checks_passed = False

    if not all_checks_passed:
        print("\nOne or more health checks failed.", file=sys.stderr)
        sys.exit(1)
    else:
        print("\nAll health checks passed successfully.")

if __name__ == "__main__":
    main()
