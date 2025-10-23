#!/usr/bin/env python3

import argparse
import os
import subprocess
import sys
import json
from datetime import datetime

try:
    import shodan
except ImportError:
    print("Shodan library not found. Please install it: pip install shodan", file=sys.stderr)
    sys.exit(1)

# --- Configuration ---
SHODAN_API_KEY_ENV = "SHODAN_API_KEY"
SUBFINDER_PATH = "subfinder" # Assumes subfinder is in PATH or specified by user
OUTPUT_DIR = "recon_results"

# --- Helper Functions ---
def print_colored(text, color):
    colors = {
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "magenta": "\033[95m",
        "cyan": "\033[96m",
        "white": "\033[97m",
        "reset": "\033[0m"
    }
    print(f"{colors.get(color, colors['reset'])}{text}{colors['reset']}")

def run_command(command, dry_run=False, capture_output=True, shell=False):
    """Runs a shell command and returns its output."""
    print_colored(f"Executing: {' '.join(command) if isinstance(command, list) else command}", "blue")
    if dry_run:
        return "", "", 0

    try:
        result = subprocess.run(
            command,
            capture_output=capture_output,
            text=True,
            check=False,
            shell=shell
        )
        if result.returncode != 0:
            print_colored(f"Command failed with exit code {result.returncode}: {result.stderr}", "red")
        return result.stdout, result.stderr, result.returncode
    except FileNotFoundError:
        print_colored(f"Error: Command not found. Make sure '{command[0]}' is installed and in your PATH.", "red")
        return "", f"Command not found: {command[0]}", 127
    except Exception as e:
        print_colored(f"An unexpected error occurred: {e}", "red")
        return "", str(e), 1


def get_shodan_api(api_key):
    """Initializes and returns a Shodan API object."""
    if not api_key:
        print_colored(f"Shodan API key not provided. Set {SHODAN_API_KEY_ENV} environment variable or use --shodan-key argument.", "yellow")
        return None
    return shodan.Shodan(api_key)

# --- Reconnaissance Functions ---
def enumerate_subdomains(domain, output_file=None, dry_run=False):
    """Enumerates subdomains using subfinder."""
    print_colored(f"[*] Starting subdomain enumeration for {domain}...", "cyan")
    command = [SUBFINDER_PATH, "-d", domain, "-silent"]
    if output_file:
        command.extend(["-o", output_file])

    stdout, stderr, returncode = run_command(command, dry_run=dry_run)

    if returncode == 0 and not dry_run:
        if output_file:
            print_colored(f"[+] Subdomains saved to {output_file}", "green")
            with open(output_file, 'r') as f:
                subdomains = [line.strip() for line in f if line.strip()]
        else:
            subdomains = [line.strip() for line in stdout.splitlines() if line.strip()]
            for sub in subdomains:
                print(f"    - {sub}")
        print_colored(f"[+] Found {len(subdomains)} subdomains.", "green")
        return subdomains
    elif dry_run:
        print_colored("[+] Subdomain enumeration (dry run) simulated.", "green")
        return []
    else:
        print_colored("[-] Subdomain enumeration failed.", "red")
        return []

def shodan_lookup(domain, api, output_file=None, dry_run=False):
    """Performs a Shodan lookup for the given domain."""
    if not api:
        return []

    print_colored(f"[*] Performing Shodan lookup for {domain}...", "cyan")
    if dry_run:
        print_colored("[+] Shodan lookup (dry run) simulated.", "green")
        return []

    try:
        results = api.host(domain) # Shodan can resolve domain to IP
        shodan_data = {
            "ip_str": results.get("ip_str"),
            "ports": results.get("ports"),
            "org": results.get("org"),
            "os": results.get("os"),
            "data": results.get("data") # Raw data for more details
        }
        print_colored(f"[+] Shodan found information for {domain} (IP: {shodan_data['ip_str']})", "green")
        print(f"    Organization: {shodan_data['org']}")
        print(f"    Operating System: {shodan_data['os']}")
        print(f"    Open Ports: {', '.join(map(str, shodan_data['ports'])) if shodan_data['ports'] else 'None'}")

        if output_file:
            with open(output_file, 'w') as f:
                json.dump(shodan_data, f, indent=4)
            print_colored(f"[+] Shodan results saved to {output_file}", "green")
        return [shodan_data]
    except shodan.exception.APIError as e:
        print_colored(f"[-] Shodan API Error: {e}", "red")
        return []
    except Exception as e:
        print_colored(f"[-] An unexpected error during Shodan lookup: {e}", "red")
        return []

# --- Main Logic ---
def main():
    parser = argparse.ArgumentParser(
        description="Automate initial reconnaissance for a target domain.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("domain", help="The target domain (e.g., example.com).")
    parser.add_argument("--shodan-key", help=f"Shodan API key. Can also be set via {SHODAN_API_KEY_ENV} environment variable.")
    parser.add_argument("--no-subdomains", action="store_true", help="Skip subdomain enumeration.")
    parser.add_argument("--no-shodan", action="store_true", help="Skip Shodan lookup.")
    parser.add_argument("--output", "-o", action="store_true", help="Save results to files in a timestamped directory.")
    parser.add_argument("--dry-run", action="store_true", help="Show commands that would be run without executing them.")
    parser.add_argument("--subfinder-path", default=SUBFINDER_PATH,
                        help=f"Path to the subfinder executable (default: {SUBFINDER_PATH}).")

    args = parser.parse_args()

    # Update subfinder path if provided
    global SUBFINDER_PATH
    SUBFINDER_PATH = args.subfinder_path

    # Determine output directory
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    domain_safe = args.domain.replace('.', '_')
    session_output_dir = os.path.join(OUTPUT_DIR, f"{domain_safe}_{current_time}")

    if args.output and not args.dry_run:
        os.makedirs(session_output_dir, exist_ok=True)
        print_colored(f"[+] Results will be saved to: {session_output_dir}", "green")

    # Get Shodan API key
    shodan_api_key = args.shodan_key or os.getenv(SHODAN_API_KEY_ENV)
    shodan_api = get_shodan_api(shodan_api_key) if not args.no_shodan else None

    all_subdomains = []
    if not args.no_subdomains:
        subdomain_output_file = os.path.join(session_output_dir, "subdomains.txt") if args.output else None
        all_subdomains = enumerate_subdomains(args.domain, subdomain_output_file, args.dry_run)

    if not args.no_shodan:
        shodan_output_file = os.path.join(session_output_dir, "shodan_results.json") if args.output else None
        shodan_lookup(args.domain, shodan_api, shodan_output_file, args.dry_run)

        # Also check subdomains with Shodan if found
        if all_subdomains:
            print_colored("\n[*] Performing Shodan lookup for discovered subdomains...", "cyan")
            for i, sub in enumerate(all_subdomains):
                print_colored(f"    ({i+1}/{len(all_subdomains)}) Looking up: {sub}", "blue")
                sub_shodan_output_file = os.path.join(session_output_dir, f"shodan_{sub.replace('.', '_')}.json") if args.output else None
                shodan_lookup(sub, shodan_api, sub_shodan_output_file, args.dry_run)

    print_colored("\n[+] Reconnaissance complete!", "green")
    if args.output and not args.dry_run:
        print_colored(f"All results are in: {session_output_dir}", "green")

if __name__ == "__main__":
    main()
