#!/usr/bin/env python3
# .devdev/skills/python-pep8/scripts/import-organizer.py

"""
Description:
This script automatically reorganizes imports in Python files according to
PEP 8 guidelines: standard library, third-party, local, sorted alphabetically.
It can operate in dry-run mode or apply changes directly.

Usage:
  python3 import-organizer.py [OPTIONS] <PATH>

Options:
  -h, --help       Show this help message and exit.
  -d, --dry-run    Perform a dry run; show what would be changed without writing to files.

Arguments:
  PATH             The path to a Python file or directory to process.

Requirements:
  - Python 3.6+
  - isort (pip install isort) - This script uses isort internally for robust import sorting.

Example Usage:
  python3 import-organizer.py my_module.py
  python3 import-organizer.py --dry-run my_project/
"""

import argparse
import os
import sys
import subprocess

# --- Colors for output ---
GREEN = "\033[0;32m"
YELLOW = "\033[0;33m"
RED = "\033[0;31m"
BLUE = "\033[0;34m"
NC = "\033[0m"  # No Color


def command_exists(cmd):
    """Check if a command exists."""
    return subprocess.call(f"type {cmd}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) == 0


def organize_imports_with_isort(filepath, dry_run):
    """Organizes imports in a single Python file using isort."""
    print(f"{BLUE}Processing file: {filepath}{NC}")
    isort_command = ["isort", filepath]

    if dry_run:
        isort_command.append("--check-only")
        isort_command.append("--diff")
        print(f"{YELLOW}Dry run: Checking imports for {filepath}{NC}")
    else:
        print(f"{YELLOW}Organizing imports for {filepath}{NC}")

    try:
        result = subprocess.run(isort_command, capture_output=True, text=True, check=False)

        if result.returncode == 0:
            if dry_run:
                if "would be reformatted" in result.stdout or "would be sorted" in result.stdout:
                    print(f"{YELLOW}Imports in {filepath} are not organized. Proposed changes:\n{result.stdout}{NC}")
                    return False # Indicates changes are needed
                else:
                    print(f"{GREEN}Imports in {filepath} are already organized.{NC}")
                    return True # Indicates no changes needed
            else:
                print(f"{GREEN}Imports in {filepath} organized successfully.{NC}")
                return True
        else:
            print(f"{RED}Error organizing imports in {filepath}:\n{result.stderr}{NC}", file=sys.stderr)
            return False
    except FileNotFoundError:
        print(f"{RED}Error: 'isort' command not found. Please install it: pip install isort{NC}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"{RED}An unexpected error occurred while running isort on {filepath}: {e}{NC}", file=sys.stderr)
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Organize Python imports according to PEP 8 using isort."
    )
    parser.add_argument(
        "path",
        type=str,
        help="The path to a Python file or directory to process."
    )
    parser.add_argument(
        "-d", "--dry-run",
        action="store_true",
        help="Perform a dry run; show what would be changed without writing to files."
    )

    args = parser.parse_args()

    if not command_exists("isort"):
        print(f"{RED}Error: 'isort' command not found. Please install it: pip install isort{NC}", file=sys.stderr)
        sys.exit(1)

    files_to_process = []
    if os.path.isfile(args.path):
        if args.path.endswith('.py'):
            files_to_process.append(args.path)
        else:
            print(f"{RED}Error: '{args.path}' is not a Python file.{NC}", file=sys.stderr)
            sys.exit(1)
    elif os.path.isdir(args.path):
        for root, _, files in os.walk(args.path):
            for file in files:
                if file.endswith('.py'):
                    files_to_process.append(os.path.join(root, file))
    else:
        print(f"{RED}Error: Path '{args.path}' is not a valid file or directory.{NC}", file=sys.stderr)
        sys.exit(1)

    if not files_to_process:
        print(f"{YELLOW}No Python files found to process in '{args.path}'.{NC}")
        sys.exit(0)

    all_successful = True
    for filepath in files_to_process:
        if not organize_imports_with_isort(filepath, args.dry_run):
            all_successful = False

    if not all_successful and not args.dry_run:
        print(f"{RED}\n--- Some files had errors during import organization. ---")
        sys.exit(1)
    elif not all_successful and args.dry_run:
        print(f"{YELLOW}\n--- Some files require import organization. Run without --dry-run to apply changes. ---")
        sys.exit(1)
    else:
        print(f"{GREEN}\n--- All specified Python files processed successfully. ---")


if __name__ == "__main__":
    main()
