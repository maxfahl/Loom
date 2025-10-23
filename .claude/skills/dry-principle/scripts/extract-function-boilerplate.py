#!/usr/bin/env python3

# extract-function-boilerplate.py
# Description: Assists in refactoring by generating boilerplate for a new TypeScript function
#              based on a selected code block. It prompts the user for the function name
#              and attempts to identify potential parameters from variables used within
#              the block but defined outside it. It does NOT modify the file directly.

import argparse
import os
import re

def get_code_block(file_path, start_line, end_line):
    """Reads a specific code block from a file."""
    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}")
        return None

    with open(file_path, 'r') as f:
        lines = f.readlines()

    if start_line < 1 or end_line > len(lines) or start_line > end_line:
        print(f"Error: Invalid line range ({start_line}-{end_line}) for file {file_path}")
        return None

    # Adjust for 0-based indexing
    return [line.strip('\n') for line in lines[start_line - 1:end_line]]

def analyze_code_block(code_block):
    """Analyzes a code block to suggest parameters and return types (basic heuristic)."""
    defined_vars = set()
    used_vars = set()
    potential_params = set()

    # Simple regex to find variable declarations and usages
    # This is a very basic heuristic and won't cover all cases (e.g., class members, global vars)
    var_declaration_pattern = re.compile(r'(?:const|let|var)\s+([a-zA-Z_][a-zA-Z0-9_]*)')
    var_usage_pattern = re.compile(r'\b([a-zA-Z_][a-zA-Z0-9_]*)\b')

    for line in code_block:
        # Find declarations
        for match in var_declaration_pattern.finditer(line):
            defined_vars.add(match.group(1))

        # Find all word-like tokens that could be variables
        for match in var_usage_pattern.finditer(line):
            var_name = match.group(1)
            # Exclude common keywords, numbers, and already defined vars within the block
            if var_name not in ['function', 'class', 'if', 'else', 'for', 'while', 'return', 'new', 'this', 'true', 'false', 'null', 'undefined', 'import', 'export', 'const', 'let', 'var', 'type', 'interface', 'enum', 'async', 'await', 'console', 'log'] and not var_name.isdigit():
                used_vars.add(var_name)

    # Parameters are variables used but not defined within the block
    potential_params = used_vars - defined_vars

    # Basic attempt to guess return type (if any return statement is present)
    has_return = any(re.search(r'\breturn\b', line) for line in code_block)
    return_type = 'void'
    if has_return:
        # This is a very weak heuristic; a real parser would be needed for accuracy
        return_type = 'any' # Default to any if we can't be specific

    return list(potential_params), return_type

def main():
    parser = argparse.ArgumentParser(
        description="Generate boilerplate for extracting a TypeScript function from a code block."
    )
    parser.add_argument("file_path", help="Path to the TypeScript file.")
    parser.add_argument("start_line", type=int, help="Starting line number of the code block (1-indexed).")
    parser.add_argument("end_line", type=int, help="Ending line number of the code block (1-indexed).")
    parser.add_argument("-n", "--name", help="Optional: Name for the new function.")
    parser.add_argument("-d", "--dry-run", action="store_true",
                        help="Show generated boilerplate without prompting for function name.")

    args = parser.parse_args()

    code_block = get_code_block(args.file_path, args.start_line, args.end_line)
    if not code_block:
        return

    if not args.dry_run:
        print("\n--- Code Block to Extract ---")
        for i, line in enumerate(code_block):
            print(f"{args.start_line + i:4d} | {line}")
        print("-----------------------------")

    function_name = args.name
    if not function_name and not args.dry_run:
        function_name = input("Enter desired function name (e.g., processUserData): ").strip()
        if not function_name:
            print("Function name cannot be empty. Aborting.")
            return

    if not function_name:
        function_name = "extractedFunction" # Default for dry-run if not provided

    potential_params, return_type = analyze_code_block(code_block)

    param_str = ', '.join([f'{p}: any' for p in potential_params]) # Default to any type

    print("\n--- Generated Function Boilerplate (TypeScript) ---")
    print(f"function {function_name}({param_str}): {return_type} {{")
    for line in code_block:
        print(f"    {line}")
    print("}")
    print("---------------------------------------------------")

    print("\n--- Suggested Call Site Replacement ---")
    call_args = ', '.join(potential_params)
    print(f"{function_name}({call_args});")
    print("-------------------------------------")
    print("\nNote: This is a boilerplate. You will need to manually adjust types, imports, and actual code replacement.")

if __name__ == "__main__":
    main()
