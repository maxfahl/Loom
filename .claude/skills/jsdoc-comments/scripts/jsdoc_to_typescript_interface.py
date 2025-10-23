#!/usr/bin/env python3
"""
jsdoc_to_typescript_interface.py

This script converts JSDoc `@typedef` definitions found in JavaScript/TypeScript files
into TypeScript interface definitions. This is useful for migrating JSDoc-based
type definitions to native TypeScript interfaces.

Usage Examples:
    # Convert JSDoc typedefs in a single file and print to console (dry-run)
    python jsdoc_to_typescript_interface.py src/types.js --dry-run

    # Convert JSDoc typedefs in a single file and append to a .d.ts file
    python jsdoc_to_typescript_interface.py src/types.js --output-file src/global.d.ts

    # Convert JSDoc typedefs from all .js and .ts files in a directory
    python jsdoc_to_typescript_interface.py src/ --output-file types.d.ts
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

def jsdoc_type_to_ts_type(jsdoc_type):
    """Converts a JSDoc type string to a TypeScript type string."""
    jsdoc_type = jsdoc_type.strip()
    if jsdoc_type.startswith("{}") and jsdoc_type.endswith("{}"):
        jsdoc_type = jsdoc_type[1:-1] # Remove curly braces

    # Basic type mapping
    type_map = {
        "string": "string",
        "number": "number",
        "boolean": "boolean",
        "object": "object",
        "Array": "any[]", # Generic array, might be refined later
        "Function": "Function",
        "Date": "Date",
        "RegExp": "RegExp",
        "null": "null",
        "undefined": "undefined",
        "void": "void",
        "any": "any",
    }

    # Handle array types like Array<string> or string[]
    array_match = re.match(r'Array<([a-zA-Z0-9_]+)>', jsdoc_type)
    if array_match:
        inner_type = array_match.group(1)
        return f"{type_map.get(inner_type, inner_type)}[]"
    if jsdoc_type.endswith("[]"):
        base_type = jsdoc_type[:-2]
        return f"{type_map.get(base_type, base_type)}[]"

    # Handle union types like {string|number}
    if '|' in jsdoc_type:
        parts = [jsdoc_type_to_ts_type(p.strip()) for p in jsdoc_type.split('|')]
        return " | ".join(parts)

    # Handle optional types (e.g., {string=})
    if jsdoc_type.endswith("="):
        return f"{jsdoc_type_to_ts_type(jsdoc_type[:-1])} | undefined"

    return type_map.get(jsdoc_type, jsdoc_type) # Return original if no mapping

def parse_jsdoc_typedef(content):
    """Parses JSDoc @typedef blocks and extracts interface definitions."""
    interfaces = []
    # Regex to find JSDoc typedef blocks
    typedef_block_pattern = re.compile(
        r'/\\*\\*\s*\n'
        r'(?:\\s*\\*\\s*@typedef\\s*\\{\\s*object\\s*\\}\\s*(?P<typedef_name>[a-zA-Z_$][a-zA-Z0-9_$]*)\\s*\n'
        r'(?P<properties>(?:\\s*\\*\\s*@property\\s*\\{[^}]+\\\\\\}\s*[a-zA-Z_$][a-zA-Z0-9_$]*(?:\\s*-\\s*.*)?\\s*)*)

    )\\s*\\*/', re.DOTALL | re.MULTILINE
    )

    property_pattern = re.compile(r'@property\s*\{(?P<type>[^}]+)\\}\s*(?P<name>[a-zA-Z_$][a-zA-Z0-9_$]*)(?P<optional>\\?)?(?:\\s*-\\s*(?P<description>.*))?')

    for match in typedef_block_pattern.finditer(content):
        typedef_name = match.group('typedef_name')
        properties_block = match.group('properties')
        ts_properties = []

        for prop_match in property_pattern.finditer(properties_block):
            prop_name = prop_match.group('name')
            prop_type = jsdoc_type_to_ts_type(prop_match.group('type'))
            prop_optional = "?" if prop_match.group('optional') else ""
            ts_properties.append(f"  {prop_name}{prop_optional}: {prop_type};")

        if ts_properties:
            interfaces.append(f"interface {typedef_name} {{\n" + "\n".join(ts_properties) + "\n}}")

    return interfaces

def main():
    parser = argparse.ArgumentParser(
        description="Convert JSDoc @typedefs to TypeScript interfaces.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "path",
        help="Path to a JavaScript/TypeScript file or directory to scan."
    )
    parser.add_argument(
        "--output-file",
        help="Optional: Path to an output .d.ts file. If not provided, prints to stdout."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the generated TypeScript interfaces to stdout without writing to a file."
    )

    args = parser.parse_args()

    target_files = []
    if os.path.isfile(args.path):
        target_files.append(args.path)
    elif os.path.isdir(args.path):
        for root, _, files in os.walk(args.path):
            for file in files:
                if file.endswith((".js", ".ts", ".jsx", ".tsx")):
                    target_files.append(os.path.join(root, file))
    else:
        print(f"{Fore.RED}Error: Invalid path '{args.path}'. Must be a file or directory.{Style.RESET_ALL}", file=sys.stderr)
        sys.exit(1)

    if not target_files:
        print(f"{Fore.YELLOW}No JavaScript/TypeScript files found in '{args.path}'.{Style.RESET_ALL}")
        sys.exit(0)

    all_interfaces = []
    for file_path in target_files:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            interfaces = parse_jsdoc_typedef(content)
            if interfaces:
                all_interfaces.extend(interfaces)
        except Exception as e:
            print(f"{Fore.RED}Error processing file '{file_path}': {e}{Style.RESET_ALL}", file=sys.stderr)

    if not all_interfaces:
        print(f"{Fore.YELLOW}No JSDoc @typedef definitions found in the scanned files.{Style.RESET_ALL}")
        sys.exit(0)

    output_content = "\n\n".join(all_interfaces)

    if args.dry_run or not args.output_file:
        print(f"{Fore.CYAN}--- Generated TypeScript Interfaces ---{Style.RESET_ALL}")
        print(output_content)
        print(f"{Fore.CYAN}---------------------------------------{Style.RESET_ALL}")
    else:
        try:
            output_dir = os.path.dirname(args.output_file)
            if output_dir: os.makedirs(output_dir, exist_ok=True)
            mode = 'a' if os.path.exists(args.output_file) else 'w'
            with open(args.output_file, mode, encoding="utf-8") as f:
                f.write(output_content + "\n")
            print(f"{Fore.GREEN}Successfully {'appended' if mode == 'a' else 'created'} TypeScript interfaces to '{args.output_file}'.{Style.RESET_ALL}")
        except IOError as e:
            print(f"{Fore.RED}Error writing to output file '{args.output_file}': {e}{Style.RESET_ALL}", file=sys.stderr)
            sys.exit(1)

if __name__ == "__main__":
    main()
