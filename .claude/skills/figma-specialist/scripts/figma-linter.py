#!/usr/bin/env python3
"""
Figma File Structure Linter

This script analyzes a Figma file's structure and content against a set of
predefined best practices. It generates a report highlighting deviations,
helping maintain design system hygiene and improving automation compatibility.

It checks for:
- Inconsistent layer naming (e.g., generic names like "Rectangle 1", "Group 2").
- Missing Auto Layout on frames intended to be responsive.
- Usage of detached instances (components that have been unlinked).
- Frames without descriptive names.

Usage:
  python3 figma-linter.py --file-key <FIGMA_FILE_KEY> --token <FIGMA_ACCESS_TOKEN> [--output <OUTPUT_PATH>] [--dry-run]

Example:
  python3 figma-linter.py --file-key "YOUR_FILE_KEY" --token "YOUR_PERSONAL_ACCESS_TOKEN" --output "./figma-lint-report.json"
  python3 figma-linter.py --file-key "YOUR_FILE_KEY" --token "YOUR_PERSONAL_ACCESS_TOKEN" --dry-run

Configuration:
  - FIGMA_FILE_KEY: The unique identifier for your Figma file.
  - FIGMA_ACCESS_TOKEN: Your Figma Personal Access Token.
  - OUTPUT_PATH: Path to save the generated JSON report (default: ./figma-lint-report.json).
  - DRY_RUN: If set, the script will print the report to stdout instead of writing to a file.

Error Handling:
  - Catches network errors, API errors, and file write errors.
  - Provides informative messages for common issues like missing API key or file key.
"""

import argparse
import os
import json
import requests
import sys

# --- Configuration ---
FIGMA_API_BASE_URL = "https://api.figma.com/v1"

# --- Helper Functions ---
def get_figma_file_data(file_key: str, access_token: str) -> dict:
    """
    Fetches the full content of a Figma file.

    Args:
        file_key (str): The key of the Figma file.
        access_token (str): Your Figma Personal Access Token.

    Returns:
        dict: The JSON representation of the Figma file.

    Raises:
        requests.exceptions.RequestException: For network-related errors.
        ValueError: For API errors or invalid responses.
    """
    headers = {
        "X-Figma-Token": access_token,
    }
    url = f"{FIGMA_API_BASE_URL}/files/{file_key}"

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
        data = response.json()
        if "document" not in data:
            raise ValueError("Invalid Figma API response: 'document' key not found.")
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Figma file data: {e}", file=sys.stderr)
        if e.response is not None:
            print(f"Response status: {e.response.status_code}", file=sys.stderr)
            print(f"Response body: {e.response.text}", file=sys.stderr)
        raise
    except json.JSONDecodeError:
        print("Error: Could not decode JSON response from Figma API.", file=sys.stderr)
        raise ValueError("Invalid JSON response from Figma API.")
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        raise

def lint_figma_file(file_data: dict) -> dict:
    """
    Lints the Figma file data against predefined best practices.

    Args:
        file_data (dict): The full JSON representation of the Figma file.

    Returns:
        dict: A report of linting issues found.
    """
    issues = {
        "generic_layer_names": [],
        "frames_without_auto_layout": [],
        "detached_instances": [],
        "unnamed_frames": []
    }

    def traverse(node):
        node_type = node.get("type")
        node_name = node.get("name")
        node_id = node.get("id")

        # Check for generic layer names
        if node_name and (node_name.startswith("Rectangle ") or
                          node_name.startswith("Group ") or
                          node_name.startswith("Vector ") or
                          node_name.startswith("Path ") or
                          node_name.startswith("Ellipse ") or
                          node_name.startswith("Text ") or
                          node_name.startswith("Frame ") or
                          node_name.startswith("Component ") or
                          node_name.startswith("Instance ")):
            issues["generic_layer_names"].append({"id": node_id, "name": node_name, "type": node_type})

        # Check for frames without Auto Layout (if applicable, requires more advanced checks)
        # This is a simplified check. A real linter might look for specific layout properties.
        if node_type == "FRAME" and not node.get("layoutMode") and node_name and not node_name.startswith("Page ") and not node_name.startswith("Cover "):
            issues["frames_without_auto_layout"].append({"id": node_id, "name": node_name})

        # Check for detached instances
        if node_type == "INSTANCE" and not node.get("componentId"):
            issues["detached_instances"].append({"id": node_id, "name": node_name})

        # Check for unnamed frames (beyond generic names already caught)
        if node_type == "FRAME" and not node_name:
             issues["unnamed_frames"].append({"id": node_id, "name": "(Unnamed Frame)"})

        if "children" in node:
            for child in node["children"]:
                traverse(child)

    traverse(file_data["document"])
    return issues

def main():
    parser = argparse.ArgumentParser(
        description="Figma File Structure Linter: Analyzes Figma files for best practice adherence.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "--file-key",
        type=str,
        default=os.environ.get("FIGMA_FILE_KEY"),
        help="The Figma file key. Can also be set via FIGMA_FILE_KEY environment variable."
    )
    parser.add_argument(
        "--token",
        type=str,
        default=os.environ.get("FIGMA_ACCESS_TOKEN"),
        help="Your Figma Personal Access Token. Can also be set via FIGMA_ACCESS_TOKEN environment variable."
    )
    parser.add_argument(
        "--output",
        type=str,
        default="./figma-lint-report.json",
        help="Path to save the generated JSON report."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="If set, the script will print the report to stdout instead of writing to a file."
    )

    args = parser.parse_args()

    file_key = args.file_key
    access_token = args.token
    output_path = args.output
    dry_run = args.dry_run

    if not file_key:
        print("Error: Figma file key is required. Use --file-key or set FIGMA_FILE_KEY environment variable.", file=sys.stderr)
        sys.exit(1)
    if not access_token:
        print("Error: Figma access token is required. Use --token or set FIGMA_ACCESS_TOKEN environment variable.", file=sys.stderr)
        sys.exit(1)

    try:
        print(f"Fetching Figma file data for linting: {file_key}...")
        file_data = get_figma_file_data(file_key, access_token)
        print("Analyzing file structure...")
        lint_report = lint_figma_file(file_data)

        if dry_run:
            print("\n--- Dry Run Lint Report ---")
            print(json.dumps(lint_report, indent=2))
            print("--- End Dry Run Lint Report ---")
        else:
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(lint_report, f, indent=2, ensure_ascii=False)
            print(f"Successfully generated lint report to {output_path}")

    except (requests.exceptions.RequestException, ValueError) as e:
        print(f"Script failed: {e}", file=sys.stderr)
        sys.exit(1)
    except IOError as e:
        print(f"Error writing to file {output_path}: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
