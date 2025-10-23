#!/usr/bin/env python3

"""
duplicate-code-detector.py

Description:
  A Python script to find and report duplicate code blocks within a specified
  directory or file. Duplicate code often leads to maintenance headaches and
  can be a source of bugs.

Usage:
  python3 duplicate-code-detector.py <path_to_directory_or_file> [--min-lines N] [--exclude-dirs "node_modules,dist"]

Examples:
  python3 scripts/duplicate-code-detector.py src/
  python3 scripts/duplicate-code-detector.py . --min-lines 10
  python3 scripts/duplicate-code-detector.py src/components/ --exclude-dirs "__tests__,mocks"

Configuration Options:
  --min-lines N: Minimum number of consecutive lines to consider a duplicate block. Default: 5.
  --exclude-dirs "dir1,dir2": Comma-separated list of directory names to exclude from the search.

Exit Codes:
  0: No duplicate code blocks found or analysis completed successfully.
  1: Duplicate code blocks found.
"""

import argparse
import os
import hashlib
import sys
from collections import defaultdict

class Color:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[0;33m'
    BLUE = '\033[0;34m'
    NC = '\033[0m' # No Color

def print_color(color, message):
    print(f"{color}{message}{Color.NC}")

def get_file_lines(filepath: str) -> list[str]:
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.readlines()
    except Exception as e:
        print_color(Color.RED, f"Error reading file {filepath}: {e}")
        return []

def hash_block(lines: list[str]) -> str:
    # Join lines and hash them. Normalize whitespace for better duplicate detection.
    normalized_block = "".join(line.strip() for line in lines)
    return hashlib.md5(normalized_block.encode('utf-8')).hexdigest()

def find_duplicates(files_content: dict[str, list[str]], min_lines: int) -> dict:
    hashes = defaultdict(list)
    duplicates = defaultdict(list)

    for filepath, lines in files_content.items():
        for i in range(len(lines) - min_lines + 1):
            block = lines[i : i + min_lines]
            block_hash = hash_block(block)
            hashes[block_hash].append((filepath, i + 1, block))

    for block_hash, occurrences in hashes.items():
        if len(occurrences) > 1:
            # Filter out occurrences within the same file at very close proximity
            # to avoid reporting minor self-duplication (e.g., a loop with similar lines)
            filtered_occurrences = []
            for i, (filepath1, line_num1, block1) in enumerate(occurrences):
                is_unique_occurrence = True
                for j, (filepath2, line_num2, block2) in enumerate(occurrences):
                    if i != j and filepath1 == filepath2 and abs(line_num1 - line_num2) < min_lines:
                        is_unique_occurrence = False
                        break
                if is_unique_occurrence:
                    filtered_occurrences.append((filepath1, line_num1, block1))
            
            if len(filtered_occurrences) > 1:
                duplicates[block_hash].extend(filtered_occurrences)

    return duplicates

def main():
    parser = argparse.ArgumentParser(
        description="Find duplicate code blocks in TypeScript/JavaScript files."
    )
    parser.add_argument(
        "path",
        help="Path to the directory or file to analyze."
    )
    parser.add_argument(
        "--min-lines",
        type=int,
        default=5,
        help="Minimum number of consecutive lines to consider a duplicate block. Default: 5."
    )
    parser.add_argument(
        "--exclude-dirs",
        type=str,
        default="node_modules,dist,.git,build",
        help="Comma-separated list of directory names to exclude from the search."
    )

    args = parser.parse_args()

    target_path = args.path
    exclude_dirs = [d.strip() for d in args.exclude_dirs.split(',') if d.strip()]

    files_to_analyze = {}

    if os.path.isfile(target_path):
        if target_path.endswith(('.ts', '.js', '.tsx', '.jsx')):
            files_to_analyze[target_path] = get_file_lines(target_path)
    elif os.path.isdir(target_path):
        for root, dirs, files in os.walk(target_path):
            # Modify dirs in-place to skip excluded directories
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            for file in files:
                if file.endswith(('.ts', '.js', '.tsx', '.jsx')):
                    filepath = os.path.join(root, file)
                    files_to_analyze[filepath] = get_file_lines(filepath)
    else:
        print_color(Color.RED, f"Error: Path '{target_path}' is not a valid file or directory.")
        sys.exit(1)

    if not files_to_analyze:
        print_color(Color.YELLOW, "No relevant files found to analyze.")
        sys.exit(0)

    print_color(Color.BLUE, "\n--- Duplicate Code Detection ---")
    print_color(Color.BLUE, f"Analyzing {len(files_to_analyze)} files for duplicates of {args.min_lines} or more lines.")
    print_color(Color.BLUE, "---------------------------------")

    duplicates = find_duplicates(files_to_analyze, args.min_lines)

    if duplicates:
        print_color(Color.RED, "\n--- Duplicate Code Found! ---")
        for block_hash, occurrences in duplicates.items():
            print_color(Color.YELLOW, f"\nDuplicate Block (Hash: {block_hash[:8]}...)")
            for filepath, line_num, block in occurrences:
                print_color(Color.YELLOW, f"  - {filepath}:L{line_num}")
            print_color(Color.BLUE, "  --- Code Snippet ---")
            for line in occurrences[0][2]: # Print the first occurrence's block
                sys.stdout.write(f"    {line.rstrip()}\n")
            print_color(Color.BLUE, "  --------------------")
        sys.exit(1)
    else:
        print_color(Color.GREEN, "\n--- No Duplicate Code Found! ---")

    sys.exit(0)

if __name__ == "__main__":
    main()
