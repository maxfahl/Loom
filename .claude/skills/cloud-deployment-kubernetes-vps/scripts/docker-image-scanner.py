#!/usr/bin/env python3

# docker-image-scanner.py
# Description: Scans a Docker image for known vulnerabilities using Trivy, providing a report and optionally failing if critical vulnerabilities are found.
# Purpose: Integrates security scanning into the development or CI/CD workflow, ensuring only secure images are deployed.

import subprocess
import json
import argparse
import sys
import os

# --- Script Start ---

def run_command(command, check_error=True, capture_output=True):
    """Runs a shell command and returns its output."""
    try:
        result = subprocess.run(command, check=check_error, capture_output=capture_output, text=True, encoding='utf-8')
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {' '.join(command)}", file=sys.stderr)
        print(f"Stdout: {e.stdout}", file=sys.stderr)
        print(f"Stderr: {e.stderr}", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print(f"Error: Command not found. Please ensure '{command[0]}' is installed and in your PATH.", file=sys.stderr)
        sys.exit(1)

def install_trivy():
    """Installs Trivy if not found."""
    print("Trivy not found. Attempting to install Trivy...")
    if sys.platform == "darwin": # macOS
        install_cmd = ["brew", "install", "trivy"]
    elif "linux" in sys.platform:
        # Check for apt (Debian/Ubuntu)
        if run_command(["which", "apt-get"], check_error=False, capture_output=True):
            install_cmd = [
                "sudo", "apt-get", "update", "-y",
                "&&", "sudo", "apt-get", "install", "-y", "wget", "apt-transport-https", "gnupg", "lsb-release",
                "&&", "wget", "-qO", "-", "https://aquasecurity.github.io/trivy-repo/deb/public.key", "|", "sudo", "apt-key", "add", "-",
                "&&", "echo", "deb https://aquasecurity.github.io/trivy-repo/deb", "$(lsb_release -sc)", "main", "|", "sudo", "tee", "/etc/apt/sources.list.d/trivy.list",
                "&&", "sudo", "apt-get", "update", "-y",
                "&&", "sudo", "apt-get", "install", "-y", "trivy"
            ]
        # Check for yum (RHEL/CentOS)
        elif run_command(["which", "yum"], check_error=False, capture_output=True):
            install_cmd = [
                "sudo", "yum", "install", "-y", "yum-utils",
                "&&", "sudo", "yum-config-manager", "--add-repo", "https://aquasecurity.github.io/trivy-repo/rpm/releases/$releasever/x86_64/",
                "&&", "sudo", "yum", "install", "-y", "trivy"
            ]
        else:
            print("Error: Unsupported Linux distribution for automatic Trivy installation. Please install Trivy manually.", file=sys.stderr)
            sys.exit(1)
    else:
        print("Error: Unsupported OS for automatic Trivy installation. Please install Trivy manually.", file=sys.stderr)
        sys.exit(1)

    print(f"Running Trivy installation command: {' '.join(install_cmd)}")
    run_command(install_cmd, check_error=True, capture_output=False) # Display install output
    print("Trivy installed successfully.")

def main():
    parser = argparse.ArgumentParser(description="Scan a Docker image for vulnerabilities using Trivy.")
    parser.add_argument("--image", required=True, help="Name of the Docker image to scan (e.g., 'my-app:1.0.0').")
    parser.add_argument("--severity", default="HIGH,CRITICAL", help="Comma-separated list of vulnerability severities to report (e.g., 'LOW,MEDIUM,HIGH,CRITICAL'). Default: HIGH,CRITICAL.")
    parser.add_argument("--exit-code", type=int, default=0, help="Exit code to use if vulnerabilities of specified severity are found. Default: 0 (do not fail).")
    parser.add_argument("--ignore-unfixed", action="store_true", help="Only show vulnerabilities that have a fix available.")
    parser.add_argument("--format", default="table", choices=["table", "json"], help="Output format for the scan results. Default: table.")
    parser.add_argument("--output", help="Path to save the scan report. If not specified, prints to stdout.")

    args = parser.parse_args()

    # Check if Trivy is installed, if not, try to install it
    if not run_command(["which", "trivy"], check_error=False, capture_output=True):
        install_trivy()

    print(f"Scanning Docker image: {args.image} for vulnerabilities with severities: {args.severity}")

    trivy_cmd = [
        "trivy", "image",
        "--severity", args.severity,
        "--format", args.format,
    ]

    if args.ignore_unfixed:
        trivy_cmd.append("--ignore-unfixed")

    trivy_cmd.append(args.image)

    # Run Trivy scan
    print(f"Executing Trivy command: {' '.join(trivy_cmd)}")
    scan_output = run_command(trivy_cmd, check_error=False) # Don't check_error here, as Trivy exits with 1 on vulns

    if args.output:
        with open(args.output, "w", encoding='utf-8') as f:
            f.write(scan_output)
        print(f"Scan report saved to {args.output}")
    else:
        print("\n--- Trivy Scan Results ---")
        print(scan_output)
        print("--------------------------")

    # Check for vulnerabilities and exit code
    if args.exit_code != 0:
        if args.format == "json":
            try:
                report = json.loads(scan_output)
                vulnerabilities_found = False
                for result in report.get("Results", []):
                    for vuln in result.get("Vulnerabilities", []):
                        if vuln["Severity"] in args.severity.split(","):
                            vulnerabilities_found = True
                            break
                    if vulnerabilities_found:
                        break
                if vulnerabilities_found:
                    print(f"Critical vulnerabilities found. Exiting with code {args.exit_code}.", file=sys.stderr)
                    sys.exit(args.exit_code)
            except json.JSONDecodeError:
                print("Error: Could not parse Trivy JSON output.", file=sys.stderr)
                sys.exit(1)
        else:
            # For table format, just check if Trivy reported any vulnerabilities of the specified severity
            # Trivy exits with 0 if no vulnerabilities, 1 if vulnerabilities found, 2 on error
            # We already captured output, so we need to re-evaluate based on content
            # A simpler check for table format is to see if it contains vulnerability details
            if "Total:" in scan_output and "(UNKNOWN:" not in scan_output: # Basic check to see if vulnerabilities are listed
                # This is a heuristic, a more robust check would parse table or use JSON format
                print(f"Vulnerabilities of specified severity found. Exiting with code {args.exit_code}.", file=sys.stderr)
                sys.exit(args.exit_code)

    print("Docker image scan completed.")

if __name__ == "__main__":
    main()
