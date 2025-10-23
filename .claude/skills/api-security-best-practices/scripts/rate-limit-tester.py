#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
rate-limit-tester.py: A script to test the effectiveness of an API endpoint's
rate limiting mechanism.

This script sends a configurable number of requests to a target URL within a
short period and analyzes the responses to determine if rate limits are being
enforced as expected. This helps verify that APIs are protected against
brute-force attacks and resource exhaustion.

Usage:
    python3 rate-limit-tester.py <url> [--requests <num>] [--interval <sec>] \
                                [--expected-status <code_list>] [--headers <json_string>] \
                                [--verbose]

Examples:
    python3 rate-limit-tester.py https://api.example.com/login --requests 20 --interval 0.1 --expected-status 200,429
    python3 rate-limit-tester.py https://api.example.com/data --requests 100 --headers '{"Authorization": "Bearer YOUR_TOKEN"}'
"""

import argparse
import requests
import time
import json
import sys

# --- Helper Functions ---
def print_color(text, color):
    """Prints text in a specified color."""
    colors = {
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "magenta": "\033[95m",
        "cyan": "\033[96m",
        "white": "\033[97m",
        "reset": "\033[0m",
    }
    sys.stdout.write(f"{colors.get(color, colors['reset'])}{text}{colors['reset']}\n")

def main():
    parser = argparse.ArgumentParser(
        description="Test API endpoint rate limiting.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "url",
        help="The target API endpoint URL."
    )
    parser.add_argument(
        "--requests",
        type=int,
        default=10,
        help="Number of requests to send (default: 10)."
    )
    parser.add_argument(
        "--interval",
        type=float,
        default=0.05,
        help="Interval between requests in seconds (default: 0.05)."
    )
    parser.add_argument(
        "--expected-status",
        type=str,
        default="200,429",
        help="Comma-separated list of expected HTTP status codes (e.g., '200,429')."
    )
    parser.add_argument(
        "--headers",
        type=str,
        default="{}",
        help="JSON string of custom headers (e.g., '{\"Authorization\": \"Bearer TOKEN\"}')."
    )
    parser.add_argument(
        "--method",
        type=str,
        default="GET",
        choices=["GET", "POST", "PUT", "DELETE", "PATCH"],
        help="HTTP method to use for requests (default: GET)."
    )
    parser.add_argument(
        "--data",
        type=str,
        help="JSON string of request body data for POST/PUT/PATCH requests."
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output for each request."
    )
    args = parser.parse_args()

    print_color("Starting Rate Limit Test...", "magenta")
    print_color(f"Target URL: {args.url}", "blue")
    print_color(f"Number of requests: {args.requests}", "blue")
    print_color(f"Interval between requests: {args.interval}s", "blue")

    expected_status_codes = [int(code) for code in args.expected_status.split(',')]
    print_color(f"Expected status codes: {expected_status_codes}", "blue")

    try:
        custom_headers = json.loads(args.headers)
    except json.JSONDecodeError:
        print_color("Error: Invalid JSON format for --headers. Please provide a valid JSON string.", "red")
        sys.exit(1)
    print_color(f"Custom Headers: {custom_headers}", "blue")

    request_data = None
    if args.data:
        try:
            request_data = json.loads(args.data)
            print_color(f"Request Data: {request_data}", "blue")
        except json.JSONDecodeError:
            print_color("Error: Invalid JSON format for --data. Please provide a valid JSON string.", "red")
            sys.exit(1)

    status_code_counts = {}
    successful_requests = 0
    rate_limited_responses = 0
    total_time_taken = 0

    for i in range(args.requests):
        start_time = time.time()
        try:
            if args.method == "GET":
                response = requests.get(args.url, headers=custom_headers, timeout=5)
            elif args.method == "POST":
                response = requests.post(args.url, headers=custom_headers, json=request_data, timeout=5)
            elif args.method == "PUT":
                response = requests.put(args.url, headers=custom_headers, json=request_data, timeout=5)
            elif args.method == "DELETE":
                response = requests.delete(args.url, headers=custom_headers, timeout=5)
            elif args.method == "PATCH":
                response = requests.patch(args.url, headers=custom_headers, json=request_data, timeout=5)
            else:
                print_color(f"Error: Unsupported HTTP method: {args.method}", "red")
                sys.exit(1)

            end_time = time.time()
            response_time = (end_time - start_time) * 1000 # in ms
            total_time_taken += response_time

            status_code = response.status_code
            status_code_counts[status_code] = status_code_counts.get(status_code, 0) + 1

            if status_code == 429:
                rate_limited_responses += 1
            elif status_code in expected_status_codes:
                successful_requests += 1

            if args.verbose:
                print_color(f"  Request {i+1}: Status={status_code}, Time={response_time:.2f}ms, Headers={response.headers.get('X-RateLimit-Remaining', 'N/A')}", "white")

        except requests.exceptions.RequestException as e:
            print_color(f"  Request {i+1}: Error - {e}", "red")
            status_code_counts["Error"] = status_code_counts.get("Error", 0) + 1
        except Exception as e:
            print_color(f"  Request {i+1}: Unexpected Error - {e}", "red")
            status_code_counts["Unexpected Error"] = status_code_counts.get("Unexpected Error", 0) + 1

        time.sleep(args.interval)

    print_color("\n--- Test Results ---", "cyan")
    print_color(f"Total Requests Sent: {args.requests}", "blue")
    print_color(f"Total Time Taken: {total_time_taken:.2f}ms", "blue")
    print_color(f"Average Response Time: {total_time_taken / args.requests:.2f}ms", "blue")
    print_color("Status Code Distribution:", "blue")
    for code, count in status_code_counts.items():
        color = "green" if code in expected_status_codes else "yellow" if code == 429 else "red"
        print_color(f"  {code}: {count} times", color)

    if rate_limited_responses > 0:
        print_color(f"\n[SUCCESS] Rate limiting appears to be active. Detected {rate_limited_responses} rate-limited responses (429).", "green")
        sys.exit(0)
    else:
        print_color("\n[WARNING] No rate-limited responses (429) detected. Rate limiting might not be effective or configured correctly.", "yellow")
        sys.exit(1)

if __name__ == "__main__":
    main()
