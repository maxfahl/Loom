#!/usr/bin/env python3
"""
Figma Asset Extractor

This script fetches specific assets (e.g., icons, illustrations, logos) from a
Figma file by their node IDs or names, and exports them into various image
formats (SVG, PNG, JPG) to a local directory. It supports scaling and format
conversion.

Usage:
  python3 figma-asset-extractor.py --file-key <FIGMA_FILE_KEY> --token <FIGMA_ACCESS_TOKEN> \
    --nodes <NODE_ID_OR_NAME_1> [<NODE_ID_OR_NAME_2> ...] \
    [--output-dir <OUTPUT_DIRECTORY>] [--format <FORMAT>] [--scale <SCALE>] [--dry-run]

Example:
  python3 figma-asset-extractor.py --file-key "YOUR_FILE_KEY" --token "YOUR_PERSONAL_ACCESS_TOKEN" \
    --nodes "Icon/24px/Home" "123:456" --output-dir "./assets" --format "svg"
  python3 figma-asset-extractor.py --file-key "YOUR_FILE_KEY" --token "YOUR_PERSONAL_ACCESS_TOKEN" \
    --nodes "Logo" --format "png" --scale 2 --dry-run

Configuration:
  - FIGMA_FILE_KEY: The unique identifier for your Figma file.
  - FIGMA_ACCESS_TOKEN: Your Figma Personal Access Token.
  - OUTPUT_DIRECTORY: Directory to save the exported assets (default: ./exported_assets).
  - FORMAT: Image format for export (svg, png, jpg) (default: png).
  - SCALE: Scale factor for raster formats (png, jpg) (default: 1).
  - DRY_RUN: If set, the script will only list what would be exported without downloading.

Error Handling:
  - Catches network errors, API errors, and file write errors.
  - Provides informative messages for issues like missing API key, file key, or invalid nodes.
"""

import argparse
import os
import json
import requests
import sys
import time

# --- Configuration ---
FIGMA_API_BASE_URL = "https://api.figma.com/v1"

# --- Helper Functions ---
def get_file_nodes(file_key: str, access_token: str) -> dict:
    """
    Fetches all nodes from a Figma file.

    Args:
        file_key (str): The key of the Figma file.
        access_token (str): Your Figma Personal Access Token.

    Returns:
        dict: A dictionary containing all nodes in the file.

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
        return data["document"]
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Figma file nodes: {e}", file=sys.stderr)
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

def find_node_ids(node_identifiers: list[str], all_nodes: dict) -> dict:
    """
    Finds Figma node IDs based on provided identifiers (ID or name).

    Args:
        node_identifiers (list[str]): List of node IDs or names to find.
        all_nodes (dict): The 'document' object from the Figma file API response.

    Returns:
        dict: A dictionary mapping found node identifiers to their IDs.
    """
    found_nodes = {}
    queue = [all_nodes]

    while queue:
        current_node = queue.pop(0)
        node_id = current_node.get("id")
        node_name = current_node.get("name")

        for identifier in node_identifiers:
            if identifier == node_id or identifier == node_name:
                found_nodes[identifier] = node_id

        if "children" in current_node:
            queue.extend(current_node["children"])
    return found_nodes

def get_image_export_urls(file_key: str, access_token: str, node_ids: list[str], export_format: str, scale: float) -> dict:
    """
    Requests image export URLs for specified Figma nodes.

    Args:
        file_key (str): The key of the Figma file.
        access_token (str): Your Figma Personal Access Token.
        node_ids (list[str]): List of node IDs to export.
        export_format (str): Format for export (svg, png, jpg).
        scale (float): Scale factor for raster formats.

    Returns:
        dict: A dictionary mapping node IDs to their export URLs.

    Raises:
        requests.exceptions.RequestException: For network-related errors.
        ValueError: For API errors or invalid responses.
    """
    headers = {
        "X-Figma-Token": access_token,
    }
    params = {
        "ids": ",".join(node_ids),
        "format": export_format,
    }
    if export_format in ["png", "jpg"]:
        params["scale"] = scale

    url = f"{FIGMA_API_BASE_URL}/images/{file_key}"

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        if "err" in data and data["err"] is not None:
            raise ValueError(f"Figma API error: {data['err']}")
        if "images" not in data:
            raise ValueError("Invalid Figma API response: 'images' key not found.")
        return data["images"]
    except requests.exceptions.RequestException as e:
        print(f"Error requesting image export URLs: {e}", file=sys.stderr)
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

def download_image(url: str, output_path: str) -> None:
    """
    Downloads an image from a given URL to a specified path.

    Args:
        url (str): The URL of the image to download.
        output_path (str): The local path to save the image.

    Raises:
        requests.exceptions.RequestException: For network-related errors during download.
        IOError: For file write errors.
    """
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
    except requests.exceptions.RequestException as e:
        print(f"Error downloading image from {url}: {e}", file=sys.stderr)
        raise
    except IOError as e:
        print(f"Error writing image to {output_path}: {e}", file=sys.stderr)
        raise

def main():
    parser = argparse.ArgumentParser(
        description="Figma Asset Extractor: Exports specific assets from a Figma file.",
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
        "--nodes",
        nargs='+',
        required=True,
        help="List of Figma node IDs or names to export (e.g., 'Icon/Home' '123:456')."
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="./exported_assets",
        help="Directory to save the exported assets."
    )
    parser.add_argument(
        "--format",
        type=str,
        choices=["svg", "png", "jpg"],
        default="png",
        help="Image format for export (svg, png, jpg)."
    )
    parser.add_argument(
        "--scale",
        type=float,
        default=1.0,
        help="Scale factor for raster formats (png, jpg). Ignored for SVG. (e.g., 2 for @2x assets)."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="If set, the script will only list what would be exported without downloading."
    )

    args = parser.parse_args()

    file_key = args.file_key
    access_token = args.token
    node_identifiers = args.nodes
    output_dir = args.output_dir
    export_format = args.format
    scale = args.scale
    dry_run = args.dry_run

    if not file_key:
        print("Error: Figma file key is required. Use --file-key or set FIGMA_FILE_KEY environment variable.", file=sys.stderr)
        sys.exit(1)
    if not access_token:
        print("Error: Figma access token is required. Use --token or set FIGMA_ACCESS_TOKEN environment variable.", file=sys.stderr)
        sys.exit(1)

    if export_format == "svg" and scale != 1.0:
        print("Warning: Scale factor is ignored for SVG format.", file=sys.stderr)

    try:
        print(f"Fetching file nodes from Figma file: {file_key}...")
        all_nodes = get_file_nodes(file_key, access_token)

        print(f"Searching for nodes: {', '.join(node_identifiers)}...")
        found_node_ids_map = find_node_ids(node_identifiers, all_nodes)

        if not found_node_ids_map:
            print(f"Error: No nodes found matching identifiers: {', '.join(node_identifiers)}", file=sys.stderr)
            sys.exit(1)

        node_ids_to_export = list(found_node_ids_map.values())
        print(f"Found {len(node_ids_to_export)} nodes to export.")

        if dry_run:
            print("\n--- Dry Run: Export would include ---")
            for identifier, node_id in found_node_ids_map.items():
                print(f"  - Identifier: '{identifier}', Node ID: '{node_id}', Format: {export_format}, Scale: {scale}")
            print("--- End Dry Run ---")
            sys.exit(0)

        os.makedirs(output_dir, exist_ok=True)
        print(f"Requesting export URLs for {len(node_ids_to_export)} nodes...")
        image_urls = get_image_export_urls(file_key, access_token, node_ids_to_export, export_format, scale)

        if not image_urls:
            print("No image URLs returned from Figma API.", file=sys.stderr)
            sys.exit(1)

        print("Downloading assets...")
        for identifier, node_id in found_node_ids_map.items():
            url = image_urls.get(node_id)
            if url:
                # Sanitize identifier for filename (replace invalid chars)
                safe_identifier = identifier.replace('/', '_').replace(':', '_').replace('=', '-').replace(' ', '-')
                filename = f"{safe_identifier}.{export_format}"
                output_path = os.path.join(output_dir, filename)
                try:
                    download_image(url, output_path)
                    print(f"  Downloaded '{identifier}' to {output_path}")
                except (requests.exceptions.RequestException, IOError) as e:
                    print(f"  Failed to download '{identifier}': {e}", file=sys.stderr)
            else:
                print(f"  No export URL found for node '{identifier}' (ID: {node_id}).", file=sys.stderr)

        print(f"\nAsset extraction complete. Assets saved to {output_dir}")

    except (requests.exceptions.RequestException, ValueError, IOError) as e:
        print(f"Script failed: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
