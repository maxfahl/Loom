#!/usr/bin/env python3
"""
Figma Design Token Synchronizer

This script extracts design variables (tokens) from a specified Figma file
and converts them into a structured JSON format. This JSON can then be
consumed by development tools, build processes, or other scripts to
generate platform-specific design tokens (e.g., CSS variables, SCSS maps,
Tailwind config, etc.).

It leverages the Figma API to fetch variable collections and their modes,
providing a robust way to keep design decisions in sync with code.

Usage:
  python3 figma-token-sync.py --file-key <FIGMA_FILE_KEY> --token <FIGMA_ACCESS_TOKEN> [--output <OUTPUT_PATH>] [--dry-run]

Example:
  python3 figma-token-sync.py --file-key "YOUR_FILE_KEY" --token "YOUR_PERSONAL_ACCESS_TOKEN" --output "./design-tokens.json"
  python3 figma-token-sync.py --file-key "YOUR_FILE_KEY" --token "YOUR_PERSONAL_ACCESS_TOKEN" --dry-run

Configuration:
  - FIGMA_FILE_KEY: The unique identifier for your Figma file.
  - FIGMA_ACCESS_TOKEN: Your Figma Personal Access Token.
  - OUTPUT_PATH: Path to save the generated JSON file (default: ./design-tokens.json).
  - DRY_RUN: If set, the script will print the output to stdout instead of writing to a file.

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
def get_figma_variables(file_key: str, access_token: str) -> dict:
    """
    Fetches design variables and collections from a Figma file.

    Args:
        file_key (str): The key of the Figma file.
        access_token (str): Your Figma Personal Access Token.

    Returns:
        dict: A dictionary containing 'variables' and 'variableCollections'.

    Raises:
        requests.exceptions.RequestException: For network-related errors.
        ValueError: For API errors or invalid responses.
    """
    headers = {
        "X-Figma-Token": access_token,
    }
    url = f"{FIGMA_API_BASE_URL}/files/{file_key}/variables/local"

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
        data = response.json()
        if "meta" not in data:
            raise ValueError("Invalid Figma API response: 'meta' key not found.")
        return data["meta"]
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Figma variables: {e}", file=sys.stderr)
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

def format_variables_to_json(meta_data: dict) -> dict:
    """
    Formats the raw Figma variable data into a structured JSON object.

    Args:
        meta_data (dict): The 'meta' data from the Figma API response.

    Returns:
        dict: A structured dictionary of design tokens.
    """
    variables = meta_data.get("variables", [])
    variable_collections = meta_data.get("variableCollections", [])

    output = {}

    # Create a mapping for collection IDs to their names and modes
    collection_map = {
        col["id"]: {"name": col["name"], "modes": {mode["modeId"]: mode["name"] for mode in col["modes"]}}
        for col in variable_collections
    }

    for variable in variables:
        collection_id = variable["variableCollectionId"]
        if collection_id not in collection_map:
            continue

        collection_name = collection_map[collection_id]["name"]
        if collection_name not in output:
            output[collection_name] = {}

        for mode_id, value in variable["valuesByMode"].items():
            mode_name = collection_map[collection_id]["modes"].get(mode_id, "default")
            if mode_name not in output[collection_name]:
                output[collection_name][mode_name] = {}

            # Simple formatting: variable name -> value
            # More complex logic can be added here for specific token formats
            output[collection_name][mode_name][variable["name"]] = value

    return output

def main():
    parser = argparse.ArgumentParser(
        description="Figma Design Token Synchronizer: Extracts design variables from Figma and converts them to JSON.",
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
        default="./design-tokens.json",
        help="Path to save the generated JSON file."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="If set, the script will print the output to stdout instead of writing to a file."
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
        print(f"Fetching variables from Figma file: {file_key}...")
        meta_data = get_figma_variables(file_key, access_token)
        structured_tokens = format_variables_to_json(meta_data)

        if dry_run:
            print("\n--- Dry Run Output ---")
            print(json.dumps(structured_tokens, indent=2))
            print("--- End Dry Run Output ---")
        else:
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(structured_tokens, f, indent=2, ensure_ascii=False)
            print(f"Successfully synchronized design tokens to {output_path}")

    except (requests.exceptions.RequestException, ValueError) as e:
        print(f"Script failed: {e}", file=sys.stderr)
        sys.exit(1)
    except IOError as e:
        print(f"Error writing to file {output_path}: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
