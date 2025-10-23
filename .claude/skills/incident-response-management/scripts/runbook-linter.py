#!/usr/bin/env python3

"""
runbook-linter.py: Validates Markdown runbook files for common issues.

This script checks Markdown runbook files for adherence to a defined structure,
presence of required sections, and potential issues like broken link formats
or outdated command patterns. It helps maintain the quality and reliability
of incident response documentation.

Usage:
    python runbook-linter.py --path docs/runbooks/api-service-runbook.md
    python runbook-linter.py --path docs/runbooks/ # To lint all .md files in a directory

Configuration:
    - REQUIRED_SECTIONS: List of top-level headers that must be present.
    - OUTDATED_COMMAND_PATTERNS: Regex patterns to flag potentially outdated commands.
"""

import argparse
import os
import re
import sys
from glob import glob

# Configuration
REQUIRED_SECTIONS = [
    "Metadata",
    "Symptoms",
    "Detection",
    "Impact",
    "Troubleshooting Steps",
    "Mitigation & Resolution",
    "Communication",
    "Escalation",
    "Post-Mortem",
]

# Regex patterns to flag potentially outdated commands or practices
# This is a simplified example; real-world patterns would be more extensive.
OUTDATED_COMMAND_PATTERNS = [
    r"docker run --rm -it old-image:1.0", # Example: specific old image version
    r"apt-get update && apt-get install -y old-package", # Example: old package name
    r"kubectl apply -f old-config.yaml", # Example: specific old config file
]

def lint_runbook(filepath):
    print(f"\n🔍 Linting: {filepath}")
    warnings = []
    errors = []

    try:
        with open(filepath, 'r') as f:
            content = f.read()
    except FileNotFoundError:
        errors.append(f"File not found: {filepath}")
        return errors, warnings
    except Exception as e:
        errors.append(f"Error reading file {filepath}: {e}")
        return errors, warnings

    lines = content.splitlines()

    # Check for required sections
    found_sections = set()
    for line in lines:
        match = re.match(r"^#+\s*(.*)$", line)
        if match:
            section_title = match.group(1).strip()
            if section_title in REQUIRED_SECTIONS:
                found_sections.add(section_title)

    for section in REQUIRED_SECTIONS:
        if section not in found_sections:
            warnings.append(f"Missing required section: '#{section}'")

    # Check for broken link formats (simple check for now: [text](url) and url starts with http/https)
    for i, line in enumerate(lines):
        # Markdown link format: [text](url)
        for match in re.finditer(r"[.*?](.*?)", line):
            url = match.group(1)
            if url and not (url.startswith("http://") or url.startswith("https://") or url.startswith("#") or url.startswith("/")):
                warnings.append(f"Line {i+1}: Potentially malformed or relative link: '{url}'. Ensure absolute URLs or valid internal anchors.")

    # Check for outdated command patterns
    for i, line in enumerate(lines):
        for pattern in OUTDATED_COMMAND_PATTERNS:
            if re.search(pattern, line):
                warnings.append(f"Line {i+1}: Potentially outdated command pattern found: '{line.strip()}'")

    return errors, warnings

def main():
    parser = argparse.ArgumentParser(
        description="Validates Markdown runbook files for common issues.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("--path", required=True,
                        help="Path to a Markdown runbook file or a directory containing runbooks.")

    args = parser.parse_args()

    files_to_lint = []
    if os.path.isfile(args.path):
        files_to_lint.append(args.path)
    elif os.path.isdir(args.path):
        files_to_lint.extend(glob(os.path.join(args.path, "**/*.md"), recursive=True))
    else:
        print(f"Error: Path is neither a file nor a directory: {args.path}")
        sys.exit(1)

    if not files_to_lint:
        print(f"No Markdown files found at: {args.path}")
        sys.exit(0)

    total_errors = 0
    total_warnings = 0

    for filepath in files_to_lint:
        errors, warnings = lint_runbook(filepath)
        if errors:
            total_errors += len(errors)
            for error in errors:
                print(f"  ❌ ERROR: {error}")
        if warnings:
            total_warnings += len(warnings)
            for warning in warnings:
                print(f"  ⚠️ WARNING: {warning}")

        if not errors and not warnings:
            print("  ✅ No issues found.")

    print(f"\n--- Linting Summary ---")
    if total_errors > 0:
        print(f"❌ Total Errors: {total_errors}")
    if total_warnings > 0:
        print(f"⚠️ Total Warnings: {total_warnings}")
    if total_errors == 0 and total_warnings == 0:
        print("✅ All runbooks passed linting with no issues.")
    else:
        print("Please review the reported issues.")

    if total_errors > 0:
        sys.exit(1)

if __name__ == "__main__":
    main()
