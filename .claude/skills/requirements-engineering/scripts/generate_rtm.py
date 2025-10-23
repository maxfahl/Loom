#!/usr/bin/env python3

"""
generate_rtm.py

This script generates a Requirement Traceability Matrix (RTM) in CSV format.
It scans specified directories for requirement documents (Markdown files) and
mock test files, extracting IDs and linking them to create a traceability report.

Usage:
    python3 generate_rtm.py --req-dir <req_path> --test-dir <test_path> [--output <output_file>] [--dry-run]

Examples:
    # Generate RTM from default directories
    python3 generate_rtm.py --req-dir ./requirements --test-dir ./tests

    # Generate RTM and save to a specific CSV file
    python3 generate_rtm.py --req-dir ./requirements --test-dir ./tests --output rtm_report.csv

    # Dry-run to see the RTM content without saving
    python3 generate_rtm.py --req-dir ./requirements --test-dir ./tests --dry-run

    # Get help
    python3 generate_rtm.py --help
"""

import argparse
import os
import re
import csv
import sys

def extract_requirement_id(file_path):
    """Extracts requirement ID (FR-ID, NFR-ID, or User Story Name) from a Markdown file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Try to find FR-ID or NFR-ID
    match_fr = re.search(r'^**FR-ID:**\s*(FR-[A-Z0-9-]+)', content, re.MULTILINE)
    if match_fr: return match_fr.group(1)

    match_nfr = re.search(r'^**NFR-ID:**\s*(NFR-[A-Z0-9-]+)', content, re.MULTILINE)
    if match_nfr: return match_nfr.group(1)

    # Try to find User Story name from the first H3 header
    match_us = re.search(r'^### User Story: (.+)', content, re.MULTILINE)
    if match_us: return f"US-{match_us.group(1).replace(' ', '')}"

    return None

def extract_test_ids(file_path):
    """Extracts test IDs (e.g., test_FR_001) from a Python test file."""
    test_ids = []
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Example: looking for test function names like test_FR_001, test_US_Login
    matches = re.findall(r'def (test_[a-zA-Z0-9_]+)\(.*\):', content)
    for match in matches:
        test_ids.append(match)
    return test_ids

def main():
    parser = argparse.ArgumentParser(
        description="Generate a Requirement Traceability Matrix (RTM) in CSV format.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "--req-dir",
        required=True,
        help="Path to the directory containing requirement Markdown files."
    )
    parser.add_argument(
        "--test-dir",
        required=True,
        help="Path to the directory containing test files (e.g., Python .py files)."
    )
    parser.add_argument(
        "--output",
        default="rtm.csv",
        help="Output CSV file name for the RTM. Defaults to 'rtm.csv'."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="If set, prints the RTM content to stdout instead of writing to a file."
    )

    args = parser.parse_args()

    requirements = {}
    tests = {}

    # Scan requirement files
    print(f"Scanning requirements in: {args.req_dir}")
    for root, _, files in os.walk(args.req_dir):
        for file in files:
            if file.endswith(".md"):
                req_file_path = os.path.join(root, file)
                req_id = extract_requirement_id(req_file_path)
                if req_id:
                    requirements[req_id] = {"path": req_file_path, "tests": []}
                    print(f"  Found requirement: {req_id} ({req_file_path})")

    # Scan test files and link to requirements
    print(f"\nScanning tests in: {args.test_dir}")
    for root, _, files in os.walk(args.test_dir):
        for file in files:
            if file.endswith(".py"):
                test_file_path = os.path.join(root, file)
                found_test_ids = extract_test_ids(test_file_path)
                for test_id in found_test_ids:
                    # Heuristic: try to link test_FR_001 to FR-001, test_US_Login to US-Login
                    linked_req_id = None
                    for req_id_prefix in ["FR-", "NFR-", "US-"]:
                        if test_id.startswith(f"test_{req_id_prefix.replace('-','')}"):
                            # Extract the part after test_FR_ or test_US_
                            potential_req_id_suffix = test_id[len(f"test_{req_id_prefix.replace('-','')}"):]
                            # Reconstruct the full req_id as it appears in requirements dict
                            for full_req_id in requirements.keys():
                                if full_req_id.startswith(req_id_prefix) and potential_req_id_suffix in full_req_id:
                                    linked_req_id = full_req_id
                                    break
                        if linked_req_id: break

                    if linked_req_id and linked_req_id in requirements:
                        requirements[linked_req_id]["tests"].append(test_id)
                        print(f"  Linked test: {test_id} ({test_file_path}) to {linked_req_id}")
                    else:
                        print(f"  Found test: {test_id} ({test_file_path}) - No direct requirement link found.")

    # Prepare RTM data
    rtm_data = [["Requirement ID", "Requirement Path", "Linked Tests"]]
    for req_id, data in requirements.items():
        linked_tests = ", ".join(data["tests"]) if data["tests"] else "N/A"
        rtm_data.append([req_id, data["path"], linked_tests])

    if args.dry_run:
        print("\n--- Generated RTM Content (Dry Run) ---")
        for row in rtm_data:
            print(",".join(row))
        print("----------------------------------------\n")
    else:
        try:
            with open(args.output, 'w', newline='', encoding='utf-8') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerows(rtm_data)
            print(f"\nSuccessfully generated RTM at: {args.output}")
        except IOError as e:
            print(f"Error writing RTM to {args.output}: {e}", file=sys.stderr)
            sys.exit(1)

if __name__ == "__main__":
    main()
