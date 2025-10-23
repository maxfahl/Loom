#!/usr/bin/env python3

# docker-image-optimizer.py
#
# Purpose:
#   Analyzes a Dockerfile and suggests optimizations (e.g., multi-stage builds,
#   reducing layers, using smaller base images) to create leaner and more secure
#   Docker images, improving build times and deployment efficiency.
#
# Usage:
#   python3 docker-image-optimizer.py <path_to_dockerfile> [--dry-run]
#
# Requirements:
#   - Python 3.6+
#
# Exit Codes:
#   0: Analysis completed successfully.
#   1: An error occurred during analysis or file not found.

import argparse
import os
import re

# --- Colors for better readability ---
RED = "\033[0;31m"
GREEN = "\033[0;32m"
YELLOW = "\033[0;33m"
BLUE = "\033[0;34m"
NC = "\033[0m" # No Color

def log_info(message):
    print(f"{BLUE}[INFO]{NC} {message}")

def log_success(message):
    print(f"{GREEN}[SUCCESS]{NC} {message}")

def log_warn(message):
    print(f"{YELLOW}[WARN]{NC} {message}")

def log_error(message):
    print(f"{RED}[ERROR]{NC} {message}")

def show_help():
    print("Usage: python3 docker-image-optimizer.py <path_to_dockerfile> [--dry-run]")
    print("")
    print("  Analyzes a Dockerfile and suggests optimizations for leaner and more secure images.")
    print("")
    print("Arguments:")
    print("  <path_to_dockerfile>  The path to the Dockerfile to analyze.")
    print("")
    print("Options:")
    print("  --dry-run             Perform analysis and suggest changes without modifying the file.")
    print("  -h, --help            Show this help message and exit.")
    print("")
    print("Examples:")
    print("  python3 docker-image-optimizer.py ./Dockerfile")
    print("  python3 docker-image-optimizer.py /app/Dockerfile --dry-run")

def analyze_dockerfile(dockerfile_path, dry_run):
    """Analyzes the Dockerfile and provides optimization suggestions."""
    if not os.path.exists(dockerfile_path):
        log_error(f"Error: Dockerfile not found at '{dockerfile_path}'")
        return 1

    log_info(f"Analyzing Dockerfile: {dockerfile_path}")
    suggestions = []
    content = []
    has_multiple_from = False
    run_commands_count = 0
    last_command = ""
    copy_before_run = False
    exposed_ports = []

    with open(dockerfile_path, 'r') as f:
        content = f.readlines()

    for i, line in enumerate(content):
        stripped_line = line.strip()
        upper_line = stripped_line.upper()

        if upper_line.startswith("FROM "):
            if run_commands_count > 0 and not has_multiple_from:
                suggestions.append(f"Line {i+1}: Consider using multi-stage builds to separate build-time dependencies from runtime dependencies. You have RUN commands before a second FROM.")
            if has_multiple_from:
                suggestions.append(f"Line {i+1}: Multiple FROM instructions detected. Ensure multi-stage builds are used effectively to minimize final image size.")
            has_multiple_from = True
            # Check for smaller base images
            if "-ALPINE" not in upper_line and \
               not re.search(r"FROM\s+(SCRATCH|DISTROLESS)", upper_line) and \
               not re.search(r"FROM\s+([A-Z0-9\/\-]+):latest", upper_line):
                suggestions.append(f"Line {i+1}: Consider using a smaller base image (e.g., Alpine, Distroless) if possible, or a specific version instead of 'latest'.")
            last_command = "FROM"
            run_commands_count = 0 # Reset for new stage

        elif upper_line.startswith("RUN "):
            run_commands_count += 1
            if last_command == "RUN":
                suggestions.append(f"Line {i+1}: Multiple consecutive RUN commands. Consider combining them with '&& \' to reduce image layers. Example: RUN apt-get update && apt-get install -y ...")
            last_command = "RUN"

        elif upper_line.startswith("COPY ") or upper_line.startswith("ADD "):
            if last_command == "RUN":
                copy_before_run = True
                suggestions.append(f"Line {i+1}: COPY/ADD instruction after RUN. This can invalidate the cache for subsequent RUN commands unnecessarily. Try to place COPY/ADD for application code after dependency installation.")
            last_command = "COPY/ADD"
        
        elif upper_line.startswith("EXPOSE "):
            ports = re.findall(r'\d+', stripped_line)
            exposed_ports.extend(ports)

    if not has_multiple_from:
        suggestions.append("No multi-stage build detected. For production images, consider using multi-stage builds to reduce the final image size by separating build dependencies.")

    if exposed_ports:
        suggestions.append(f"Exposed ports: {', '.join(exposed_ports)}. Ensure only necessary ports are exposed and consider using a non-root user.")

    log_info("\n--- Optimization Suggestions ---")
    if suggestions:
        for s in suggestions:
            log_warn(f"- {s}")
        if not dry_run:
            log_info("Consider applying these suggestions to optimize your Dockerfile.")
    else:
        log_success("No major optimization suggestions found. Your Dockerfile looks good!")

    return 0

def main():
    parser = argparse.ArgumentParser(
        description="Analyzes a Dockerfile and suggests optimizations for leaner and more secure images."
    )
    parser.add_argument(
        "dockerfile_path",
        help="The path to the Dockerfile to analyze."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Perform analysis and suggest changes without modifying the file."
    )
    parser.add_argument(
        "-h", "--help",
        action="help",
        default=argparse.SUPPRESS,
        help="Show this help message and exit."
    )

    args = parser.parse_args()

    return analyze_dockerfile(args.dockerfile_path, args.dry_run)

if __name__ == "__main__":
    exit(main())
