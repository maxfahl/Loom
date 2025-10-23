#!/usr/bin/env python3

# suggest-constants-extraction.py
# Description: Scans a given TypeScript file for frequently repeated "magic strings"
#              or "magic numbers" and suggests extracting them into a centralized
#              constants file. It highlights potential candidates for constants.

import argparse
import os
import re
from collections import defaultdict

def find_magic_values(file_path, min_occurrences=2):
    """Finds magic strings and numbers in a file that occur at least min_occurrences times."""
    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}")
        return {}, {}

    magic_strings = defaultdict(list)
    magic_numbers = defaultdict(list)

    with open(file_path, 'r') as f:
        for i, line in enumerate(f, 1):
            # Skip comments and import/export statements for simplicity
            if re.match(r'^\s*(\/\/|\/\*|\*|import|export)', line):
                continue

            # Find strings (simple double/single quoted strings)
            for match in re.finditer(r'"([^'"\\]*(?:\\.[^'"\\]*)*)"|"([^'\\]*(?:\\.[^'\\]*)*)"', line):
                value = match.group(1) if match.group(1) is not None else match.group(2)
                if value and len(value) > 2 and not value.isspace(): # Ignore very short or empty strings
                    magic_strings[value].append(i)

            # Find numbers (integers and floats, excluding common version numbers or simple indices)
            # This regex tries to be smart about not catching parts of variable names or versions
            for match in re.finditer(r'\b(?<![a-zA-Z_.-])(\d+(?:\.\d+)?)(?![a-zA-Z_.-])\b', line):
                value = match.group(1)
                # Heuristic: ignore 0, 1, 2, and numbers that look like array indices or simple counts
                if value not in ["0", "1", "2"] and not (value.isdigit() and len(value) < 2):
                    magic_numbers[value].append(i)

    suggested_strings = {k: v for k, v in magic_strings.items() if len(v) >= min_occurrences}
    suggested_numbers = {k: v for k, v in magic_numbers.items() if len(v) >= min_occurrences}

    return suggested_strings, suggested_numbers

def main():
    parser = argparse.ArgumentParser(
        description="Suggests extracting magic strings and numbers from a TypeScript file into constants."
    )
    parser.add_argument("file_path", help="Path to the TypeScript file to analyze.")
    parser.add_argument("-m", "--min-occurrences", type=int, default=2,
                        help="Minimum number of occurrences for a value to be suggested as a constant. Default: 2.")
    parser.add_argument("-o", "--output-file",
                        help="Optional: Suggests a path for the new constants file (e.g., ./src/constants/app.ts).")

    args = parser.parse_args()

    if not args.file_path.endswith(('.ts', '.tsx')):
        print(f"Warning: This script is optimized for TypeScript files. Analyzing {args.file_path} anyway.")

    suggested_strings, suggested_numbers = find_magic_values(args.file_path, args.min_occurrences)

    print(f"\n--- Analysis for {args.file_path} ---")
    print(f"Minimum occurrences for suggestion: {args.min_occurrences}")
    print("-------------------------------------")

    if not suggested_strings and not suggested_numbers:
        print("No significant magic strings or numbers found for extraction.")
        return

    if suggested_strings:
        print("\nSuggested Magic Strings to Extract:")
        for value, lines in suggested_strings.items():
            print(f"  - '{value}' (Occurrences: {len(lines)}, Lines: {lines})")

    if suggested_numbers:
        print("\nSuggested Magic Numbers to Extract:")
        for value, lines in suggested_numbers.items():
            print(f"  - {value} (Occurrences: {len(lines)}, Lines: {lines})")

    if suggested_strings or suggested_numbers:
        print("\n--- Suggested Constants File Structure (TypeScript) ---")
        if args.output_file:
            print(f"// {args.output_file}")
        else:
            print("// src/constants/app.ts (Example path)")
        print("\nexport const APP_CONSTANTS = {")
        for value in suggested_strings:
            # Simple variable name generation
            var_name = re.sub(r'[^a-zA-Z0-9_]', '', value.upper().replace(' ', '_'))
            if not var_name: var_name = "STRING_VALUE"
            print(f"    {var_name}: '{value}',")
        for value in suggested_numbers:
            var_name = re.sub(r'[^a-zA-Z0-9_.]', '', value.upper().replace('.', '_'))
            if not var_name: var_name = "NUMBER_VALUE"
            print(f"    {var_name}: {value},")
        print("};")
        print("\n// Example of how to use in your file:")
        if args.output_file:
            const_file_name = os.path.basename(args.output_file).split('.')[0]
            print(f"// import {{ APP_CONSTANTS }} from './constants/{const_file_name}';")
        else:
            print("// import { APP_CONSTANTS } from './constants/app';")
        print("// console.log(APP_CONSTANTS.YOUR_CONSTANT_NAME);")

    print("\nNote: This script provides suggestions. Manual review and refactoring are required.")

if __name__ == "__main__":
    main()
