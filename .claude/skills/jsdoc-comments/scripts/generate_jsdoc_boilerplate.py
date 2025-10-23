#!/usr/bin/env python3
"""
generate_jsdoc_boilerplate.py

This script generates JSDoc boilerplate for a given JavaScript/TypeScript function or class.
It attempts to parse the function/class signature to pre-fill parameters and return types.

Usage Examples:
    # Generate JSDoc for a function named 'myFunction' in 'src/utils.js'
    python generate_jsdoc_boilerplate.py src/utils.js myFunction

    # Generate JSDoc for a class named 'MyClass' in 'src/models.ts' with dry-run
    python generate_jsdoc_boilerplate.py src/models.ts MyClass --dry-run

    # Generate JSDoc for a specific line number (e.g., if multiple functions have the same name)
    python generate_jsdoc_boilerplate.py src/api.js fetchData --line 15
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

def get_indentation(line):
    """Returns the leading whitespace of a line."""
    match = re.match(r'^(\s*)', line)
    return match.group(1) if match else ""

def generate_jsdoc(name, params, return_type, is_class, indent=""):
    """Generates the JSDoc block content."""
    jsdoc_lines = []
    jsdoc_lines.append(f"{indent}/**")
    jsdoc_lines.append(f"{indent} * @description A brief description of this {'class' if is_class else 'function'}.")
    jsdoc_lines.append(f"{indent} *")

    for param_name, param_type in params:
        jsdoc_lines.append(f"{indent} * @param {{{param_type}}} {param_name} - Description of {param_name}.")

    if not is_class and return_type:
        jsdoc_lines.append(f"{indent} * @returns {{{return_type}}} Description of the return value.")
    elif not is_class and not return_type:
        jsdoc_lines.append(f"{indent} * @returns {{{{void}}}} Description of the return value.")

    jsdoc_lines.append(f"{indent} */")
    return "\n".join(jsdoc_lines)

def parse_function_signature(code_lines, target_name, target_line):
    """Parses function/class signature to extract parameters and return type."""
    params = []
    return_type = ""
    is_class = False
    indent = ""

    # Regex for function declarations (JS/TS)
    # Handles: function funcName(param: Type): ReturnType { ... }
    #          funcName = (param: Type): ReturnType => { ... }
    #          async function funcName(param) { ... }
    #          funcName(param) { ... } (class method)
    #          const funcName = (param) => { ... }
    func_pattern = re.compile(r'(?:(?:async|function)\s+)?(?:(const|let|var)\s+)?(?P<name>[a-zA-Z_$][a-zA-Z0-9_$]*)\s*(?:=\s*)?(?:<[a-zA-Z0-9_, ]+>)?\((?P<params>[^)]*)\)(?:\:\s*(?P<return_type>[a-zA-Z0-9_<>|\[\]]+))?\s*(?:=>)?\s*[{;]')

    # Regex for class declarations
    class_pattern = re.compile(r'^(?:export\s+)?(?:abstract\s+)?class\s+(?P<name>[a-zA-Z_$][a-zA-Z0-9_$]*)')

    for i, line in enumerate(code_lines):
        current_line_num = i + 1

        if target_line and current_line_num != target_line:
            continue

        # Try to match class first
        class_match = class_pattern.search(line)
        if class_match and class_match.group('name') == target_name:
            is_class = True
            indent = get_indentation(line)
            return params, return_type, is_class, indent, current_line_num

        # Try to match function
        func_match = func_pattern.search(line)
        if func_match and func_match.group('name') == target_name:
            indent = get_indentation(line)
            param_str = func_match.group('params')
            if param_str:
                # Split parameters, handle default values and types
                for p in re.split(r',\s*', param_str):
                    p = p.strip()
                    if not p: continue
                    # Handle 'param: Type' or 'param = defaultValue'
                    if ':' in p:
                        name_part, type_part = p.split(':', 1)
                        params.append((name_part.strip(), type_part.strip()))
                    elif '=' in p:
                        name_part = p.split('=', 1)[0]
                        params.append((name_part.strip(), "any")) # Default to any if type not specified
                    else:
                        params.append((p, "any")) # Default to any

            return_type = func_match.group('return_type') or ""
            return params, return_type, is_class, indent, current_line_num

        if target_line and current_line_num == target_line:
            # If a specific line was requested but no match, stop here
            break

    return [], "", False, "", -1 # No match found

def main():
    parser = argparse.ArgumentParser(
        description="Generate JSDoc boilerplate for a function or class.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "file_path",
        help="Path to the JavaScript/TypeScript file."
    )
    parser.add_argument(
        "target_name",
        help="Name of the function or class to document."
    )
    parser.add_argument(
        "--line",
        type=int,
        help="Optional: Line number of the function/class definition (1-indexed)."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the generated JSDoc to stdout without modifying the file."
    )

    args = parser.parse_args()

    if not os.path.exists(args.file_path):
        print(f"{Fore.RED}Error: File not found at '{args.file_path}'.{Style.RESET_ALL}", file=sys.stderr)
        sys.exit(1)

    with open(args.file_path, "r", encoding="utf-8") as f:
        code_lines = f.readlines()

    params, return_type, is_class, indent, found_line = parse_function_signature(code_lines, args.target_name, args.line)

    if found_line == -1:
        print(f"{Fore.RED}Error: Function or class '{args.target_name}' not found in '{args.file_path}'", file=sys.stderr)
        if args.line:
            print(f"{Fore.RED} at line {args.line}.{Style.RESET_ALL}", file=sys.stderr)
        else:
            print(f"{Fore.RED}. Consider using --line if multiple matches exist.{Style.RESET_ALL}", file=sys.stderr)
        sys.exit(1)

    jsdoc_block = generate_jsdoc(args.target_name, params, return_type, is_class, indent)

    if args.dry_run:
        print(f"{Fore.CYAN}--- DRY RUN: Generated JSDoc for {args.target_name} ---
{jsdoc_block}
{Fore.CYAN}--------------------------------------------------{Style.RESET_ALL}")
    else:
        # Insert JSDoc block before the found line
        new_code_lines = code_lines[:found_line - 1] + [jsdoc_block + "\n"] + code_lines[found_line - 1:]
        try:
            with open(args.file_path, "w", encoding="utf-8") as f:
                f.writelines(new_code_lines)
            print(f"{Fore.GREEN}Successfully generated JSDoc for '{args.target_name}' in '{args.file_path}'.{Style.RESET_ALL}")
        except IOError as e:
            print(f"{Fore.RED}Error writing to file '{args.file_path}': {e}{Style.RESET_ALL}", file=sys.stderr)
            sys.exit(1)

if __name__ == "__main__":
    main()
