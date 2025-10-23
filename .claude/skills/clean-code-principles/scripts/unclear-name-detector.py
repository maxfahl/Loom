#!/usr/bin/env python3

"""
unclear-name-detector.py

Description:
  A Python script that attempts to flag variables or functions with very short,
  generic, or potentially unclear names in TypeScript/JavaScript files.
  This helps enforce meaningful naming conventions.

Usage:
  python3 unclear-name-detector.py <path_to_directory_or_file> [--min-length N] [--generic-names "temp,data,val"]

Examples:
  python3 scripts/unclear-name-detector.py src/
  python3 scripts/unclear-name-detector.py . --min-length 2 --generic-names "a,b,c,x,y,z,tmp,temp,data,val,obj,item"

Configuration Options:
  --min-length N: Report names shorter than this length (excluding common loop counters like 'i', 'j'). Default: 1.
  --generic-names "name1,name2": Comma-separated list of generic names to flag.

Exit Codes:
  0: No unclear names found or analysis completed successfully.
  1: Unclear names found.
"""

import argparse
import os
import re
import sys

class Color:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[0;33m'
    BLUE = '\033[0;34m'
    NC = '\033[0m' # No Color

def print_color(color, message):
    print(f"{color}{message}{Color.NC}")

def analyze_file(filepath: str, min_length: int, generic_names: set) -> list:
    results = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Regex to find potential variable/function names
        # This is a heuristic and might have false positives/negatives.
        # It looks for identifiers that are not keywords or numbers.
        name_pattern = re.compile(r'\b([a-zA-Z_][a-zA-Z0-9_]*)\b')

        # Common keywords to ignore (not exhaustive)
        keywords = {
            "function", "class", "const", "let", "var", "if", "else", "for", "while",
            "return", "import", "export", "default", "async", "await", "new", "this",
            "super", "try", "catch", "finally", "switch", "case", "break", "continue",
            "typeof", "instanceof", "delete", "void", "in", "of", "get", "set",
            "true", "false", "null", "undefined", "NaN", "Infinity", "debugger",
            "enum", "interface", "type", "public", "private", "protected", "static"
        }

        # Common loop counters to ignore
        loop_counters = {"i", "j", "k"}

        for line_num, line in enumerate(content.splitlines(), 1):
            for match in name_pattern.finditer(line):
                name = match.group(1)

                if name in keywords or name in loop_counters:
                    continue

                # Check for generic names
                if name.lower() in generic_names:
                    results.append({
                        "file": filepath,
                        "line": line_num,
                        "name": name,
                        "reason": f"Generic name '{name}' detected."
                    })
                # Check for short names (excluding single-char loop counters already handled)
                elif len(name) < min_length:
                    results.append({
                        "file": filepath,
                        "line": line_num,
                        "name": name,
                        "reason": f"Name '{name}' is too short (min-length: {min_length})."
                    })

    except Exception as e:
        print_color(Color.RED, f"Error processing file {filepath}: {e}")
    return results

def main():
    parser = argparse.ArgumentParser(
        description="Detect potentially unclear variable/function names in TypeScript/JavaScript files."
    )
    parser.add_argument(
        "path",
        help="Path to the directory or file to analyze."
    )
    parser.add_argument(
        "--min-length",
        type=int,
        default=1,
        help="Report names shorter than this length (excluding common loop counters). Default: 1."
    )
    parser.add_argument(
        "--generic-names",
        type=str,
        default="temp,data,val,obj,item,arg,param,res,ret,e,err,cb,fn",
        help="Comma-separated list of generic names to flag. Default: temp,data,val,obj,item,arg,param,res,ret,e,err,cb,fn"
    )

    args = parser.parse_args()

    target_path = args.path
    generic_names_set = {n.strip().lower() for n in args.generic_names.split(',') if n.strip()}

    all_results = []

    if os.path.isfile(target_path):
        if target_path.endswith(('.ts', '.js', '.tsx', '.jsx')):
            all_results.extend(analyze_file(target_path, args.min_length, generic_names_set))
    elif os.path.isdir(target_path):
        for root, _, files in os.walk(target_path):
            for file in files:
                if file.endswith(('.ts', '.js', '.tsx', '.jsx')):
                    filepath = os.path.join(root, file)
                    all_results.extend(analyze_file(filepath, args.min_length, generic_names_set))
    else:
        print_color(Color.RED, f"Error: Path '{target_path}' is not a valid file or directory.")
        sys.exit(1)

    if all_results:
        print_color(Color.YELLOW, "\n--- Unclear Name Detection Report ---")
        for res in all_results:
            print_color(Color.YELLOW, f"File: {res['file']}:L{res['line']}")
            print_color(Color.YELLOW, f"  Name: {res['name']}")
            print_color(Color.YELLOW, f"  Reason: {res['reason']}")
        print_color(Color.RED, "\nPotentially unclear names detected. Consider refactoring for clarity.")
        sys.exit(1)
    else:
        print_color(Color.GREEN, "\n--- Unclear Name Detection Report ---")
        print_color(Color.GREEN, "No potentially unclear names detected.")

    sys.exit(0)

if __name__ == "__main__":
    main()
