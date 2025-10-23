#!/usr/bin/env python3

import os
import re
import argparse
import sys

EXCLUDE_DIRS = ['node_modules', 'dist', '.git', '.angular']

# Simplified and corrected Regex Patterns
SUBSCRIBE_PATTERN = re.compile(r'\.subscribe\(')
UNSUBSCRIBE_PATTERNS = [
    re.compile(r'takeUntil'),
    re.compile(r'take\(1\)'),
    re.compile(r'first\(\)'),
]

def find_potential_leaks(filepath, root_dir):
    potential_leaks = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # If a known unsubscription pattern exists anywhere in the file, assume it's safe.
        # This is a simplified heuristic.
        if any(pattern.search(content) for pattern in UNSUBSCRIBE_PATTERNS):
            return []

        # If no unsubscription patterns are found, flag all subscriptions.
        for i, line in enumerate(content.splitlines()):
            if SUBSCRIBE_PATTERN.search(line):
                potential_leaks.append({
                    'file': os.path.relpath(filepath, root_dir),
                    'line': i + 1,
                    'code': line.strip(),
                })

    except Exception as e:
        print(f"Error reading file {filepath}: {e}")
    return potential_leaks

def main():
    parser = argparse.ArgumentParser(description="Scans for potential RxJS memory leaks.")
    parser.add_argument("path", nargs='?', default='.', help="The directory to scan.")
    args = parser.parse_args()

    scan_path = args.path
    if not os.path.isdir(scan_path):
        print(f"Error: Scan path '{scan_path}' is not a valid directory.")
        return

    print(f"Scanning for RxJS memory leaks in '{scan_path}'...")

    all_potential_leaks = []
    for root, dirs, files in os.walk(scan_path):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for file in files:
            if file.endswith('.ts') and not file.endswith('.spec.ts'):
                filepath = os.path.join(root, file)
                leaks = find_potential_leaks(filepath, scan_path)
                if leaks:
                    all_potential_leaks.extend(leaks)
    
    if not all_potential_leaks:
        print("No potential RxJS memory leaks detected!")
        return

    print(f"{len(all_potential_leaks)} potential RxJS memory leaks detected:")
    for leak in all_potential_leaks:
        print(f"  - {leak['file']}:{leak['line']}: {leak['code']}")

if __name__ == "__main__":
    main()
