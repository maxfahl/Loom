#!/usr/bin/env python
#
# init-prettierignore.py: Generates a comprehensive .prettierignore file.
#
# This script creates a .prettierignore file with a list of common patterns
# for different project types to prevent accidental formatting of generated
# or sensitive files.

import argparse
import os

# --- Color Codes (for POSIX systems) ---
COLOR_GREEN = "\033[0;32m"
COLOR_YELLOW = "\033[0;33m"
COLOR_RESET = "\033[0m"

def print_success(message):
    print(f"{COLOR_GREEN}✅ {message}{COLOR_RESET}")

def print_warning(message):
    print(f"{COLOR_YELLOW}⚠️ {message}{COLOR_RESET}")

# --- Ignore Patterns ---

PATTERNS = {
    "common": [
        "# Ignore build output and artifacts",
        "node_modules/",
        "dist/",
        "build/",
        "coverage/",
        ".turbo/",
        ".next/",
        ".nuxt/",
        ".svelte-kit/",
    ],
    "project_files": [
        "# Ignore package manager lock files",
        "package-lock.json",
        "yarn.lock",
        "pnpm-lock.yaml",
    ],
    "config_files": [
        "# Ignore environment variables",
        ".env*",
        "!.env.example",
    ],
    "python": [
        "# Python specific",
        "__pycache__/",
        "*.pyc",
        "*.pyo",
        "*.pyd",
        ".Python",
        "env/",
        "venv/",
    ],
    "other": [
        "# Other",
        "*.log",
        "*.min.*
    ]
}

def main():
    """Main function to generate the .prettierignore file."""
    parser = argparse.ArgumentParser(
        description="Generate a .prettierignore file.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "--path",
        default=".",
        help="The directory to create the .prettierignore file in. Defaults to current directory."
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite an existing .prettierignore file."
    )
    args = parser.parse_args()

    file_path = os.path.join(args.path, ".prettierignore")

    if os.path.exists(file_path) and not args.force:
        print_warning(f"'.prettierignore' already exists at {file_path}. Use --force to overwrite.")
        return

    all_patterns = []
    for category in PATTERNS.values():
        all_patterns.extend(category)
        all_patterns.append("\n")

    try:
        with open(file_path, "w") as f:
            f.write("\n".join(all_patterns))
        print_success(f"Successfully created .prettierignore at {file_path}")
    except IOError as e:
        print(f"Error writing to file: {e}")

if __name__ == "__main__":
    main()
