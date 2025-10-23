#!/usr/bin/env python3
"""
check_jsdoc_coverage.py

This script scans JavaScript/TypeScript files in a given directory and reports on the
percentage of functions and classes that have JSDoc comments.

Usage Examples:
    # Check JSDoc coverage in the current directory for .js and .ts files
    python check_jsdoc_coverage.py .

    # Check JSDoc coverage in 'src/' directory, only for .js files
    python check_jsdoc_coverage.py src/ --extensions js

    # Check JSDoc coverage with verbose output
    python check_jsdoc_coverage.py . -v
"""

import argparse
import os
import re
import sys

try:
    from colorama import Fore, Style, init
    init(autoreset=True)
except ImportError:
    class Color:
        def __getattr__(self, name):
            return ''
    Fore = Color()
    Style = Color()

def analyze_file_for_jsdoc(file_path):
    """Analyzes a single file for JSDoc coverage of functions and classes."""
    documented_entities = 0
    total_entities = 0
    undocumented_details = []

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Regex to find JSDoc comments (starts with /**, ends with */)
    jsdoc_pattern = re.compile(r'/
**
(?:[^*]|
**
(?!/))*
**
*/

    # Regex to find function or class declarations
    # This is a simplified regex and might not catch all edge cases
    entity_pattern = re.compile(
        r'(?:(?:export|declare|async|function|class)

    # Iterate through matches of entities
    for match in entity_pattern.finditer(content):
        total_entities += 1
        entity_start = match.start()
        entity_name = match.group(0).split(' ')[-1].split('(')[0].strip()

        # Look for a JSDoc comment immediately preceding this entity
        # Search backwards from entity_start for a JSDoc block
        preceding_text = content[:entity_start]
        jsdoc_match = None
        for jsdoc_m in jsdoc_pattern.finditer(preceding_text):
            # Check if the JSDoc is directly above the entity (no significant code in between)
            # This is a heuristic: check if there are only whitespace/comments between JSDoc and entity
            gap = preceding_text[jsdoc_m.end():]
            if not re.search(r'[^\s/*-]', gap):
                jsdoc_match = jsdoc_m

        if jsdoc_match:
            documented_entities += 1
        else:
            line_num = content.count('\n', 0, entity_start) + 1
            undocumented_details.append(f"  - {entity_name} (Line: {line_num})")

    return documented_entities, total_entities, undocumented_details

def main():
    parser = argparse.ArgumentParser(
        description="Check JSDoc coverage for JavaScript/TypeScript files.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "path",
        help="The path to the directory to scan."
    )
    parser.add_argument(
        "--extensions",
        nargs='*',
        default=["js", "ts", "jsx", "tsx"],
        help="File extensions to check (e.g., js ts jsx). Default: js ts jsx tsx."
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Show details of undocumented functions/classes."
    )

    args = parser.parse_args()
    target_path = args.path
    extensions = tuple(f".{ext}" for ext in args.extensions)

    if not os.path.isdir(target_path):
        print(f"{Fore.RED}Error: Provided path '{target_path}' is not a valid directory.{Style.RESET_ALL}", file=sys.stderr)
        sys.exit(1)

    total_documented = 0
    total_found = 0
    all_undocumented_details = []
    file_count = 0

    for root, _, files in os.walk(target_path):
        for file in files:
            if file.endswith(extensions):
                file_count += 1
                file_path = os.path.join(root, file)
                try:
                    documented, found, undocumented_details = analyze_file_for_jsdoc(file_path)
                    total_documented += documented
                    total_found += found
                    if undocumented_details:
                        all_undocumented_details.append(f"{Fore.YELLOW}File: {file_path}{Style.RESET_ALL}")
                        all_undocumented_details.extend(undocumented_details)
                except Exception as e:
                    print(f"{Fore.RED}Error processing file '{file_path}': {e}{Style.RESET_ALL}", file=sys.stderr)

    if file_count == 0:
        print(f"{Fore.YELLOW}No files with specified extensions found in '{target_path}'.{Style.RESET_ALL}")
        sys.exit(0)

    if total_found == 0:
        print(f"{Fore.YELLOW}No functions or classes found to document in the scanned files.{Style.RESET_ALL}")
        sys.exit(0)

    coverage_percentage = (total_documented / total_found) * 100 if total_found > 0 else 0

    print(f"\n{Fore.CYAN}--- JSDoc Coverage Report ---{Style.RESET_ALL}")
    print(f"Scanned files: {file_count}")
    print(f"Total functions/classes found: {total_found}")
    print(f"Documented functions/classes: {total_documented}")
    print(f"Coverage: {coverage_percentage:.2f}%
")

    if all_undocumented_details:
        print(f"{Fore.RED}Undocumented Entities:{Style.RESET_ALL}")
        if args.verbose:
            for detail in all_undocumented_details:
                print(detail)
        else:
            print(f"{Fore.YELLOW}  (Run with -v or --verbose to see details){Style.RESET_ALL}")
        sys.exit(1) # Indicate that undocumented entities were found
    else:
        print(f"{Fore.GREEN}All found functions and classes are documented!{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
