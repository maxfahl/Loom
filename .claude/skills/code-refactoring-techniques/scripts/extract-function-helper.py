#!/usr/bin/env python3

import argparse
import os
import re
import sys

# ANSI escape codes for colored output
COLOR_GREEN = "\033[92m"
COLOR_YELLOW = "\033[93m"
COLOR_BLUE = "\033[94m"
COLOR_RED = "\033[91m"
COLOR_END = "\033[0m"

def get_code_block(filepath: str, start_line: int, end_line: int) -> list[str]:
    """
    Reads a specific block of code from a file.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        # Adjust for 0-based indexing
        return [line.rstrip() for line in lines[start_line - 1:end_line]]
    except FileNotFoundError:
        print(f"{COLOR_RED}Error: File not found at {filepath}{COLOR_END}")
        sys.exit(1)
    except IndexError:
        print(f"{COLOR_RED}Error: Line numbers out of range for file {filepath}{COLOR_END}")
        sys.exit(1)

def analyze_code_block(full_file_lines: list[str], start_line: int, end_line: int) -> tuple[list[str], list[str]]:
    """
    Analyzes a code block to suggest parameters and return values.
    This is a heuristic and may not be perfect for all TypeScript code.
    """
    block_lines = [line.strip() for line in full_file_lines[start_line - 1:end_line]]
    before_block_lines = [line.strip() for line in full_file_lines[:start_line - 1]]
    after_block_lines = [line.strip() for line in full_file_lines[end_line:]]

    # Simple regex to find potential variable declarations and usages
    # This is a very basic heuristic and will miss many cases.
    variable_pattern = re.compile(r'(?:const|let|var)\s+([a-zA-Z_$][a-zA-Z0-9_$]*)')
    usage_pattern = re.compile(r'\b([a-zA-Z_$][a-zA-Z0-9_$]*)\b')

    declared_in_block = set()
    used_in_block = set()

    for line in block_lines:
        # Find declarations within the block
        for match in variable_pattern.finditer(line):
            declared_in_block.add(match.group(1))
        # Find all identifiers used in the block
        for match in usage_pattern.finditer(line):
            used_in_block.add(match.group(1))

    # Parameters: variables used in block but not declared in block, and declared before block
    potential_params = set()
    declared_before_block = set()
    for line in before_block_lines:
        for match in variable_pattern.finditer(line):
            declared_before_block.add(match.group(1))

    for var_name in used_in_block:
        if var_name not in declared_in_block and var_name in declared_before_block:
            potential_params.add(var_name)

    # Return values: variables declared in block and used after block
    potential_returns = set()
    used_after_block = set()
    for line in after_block_lines:
        for match in usage_pattern.finditer(line):
            used_after_block.add(match.group(1))

    for var_name in declared_in_block:
        if var_name in used_after_block:
            potential_returns.add(var_name)

    return sorted(list(potential_params)), sorted(list(potential_returns))

def main():
    parser = argparse.ArgumentParser(
        description=f"{COLOR_BLUE}Interactive Extract Function Helper for TypeScript.{COLOR_END}\n"
                    "Helps in extracting a code block into a new function by suggesting parameters and return values.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        '--file',
        type=str,
        required=True,
        help='Path to the TypeScript file to refactor.'
    )
    args = parser.parse_args()

    filepath = args.file

    if not os.path.exists(filepath):
        print(f"{COLOR_RED}Error: File not found at {filepath}{COLOR_END}")
        sys.exit(1)

    print(f"{COLOR_BLUE}--- Extract Function Helper ---{COLOR_END}")
    print(f"Analyzing file: {filepath}\n")

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            full_file_lines = f.readlines()
    except Exception as e:
        print(f"{COLOR_RED}Error reading file: {e}{COLOR_END}")
        sys.exit(1)

    num_lines = len(full_file_lines)
    print(f"File has {num_lines} lines.")

    while True:
        try:
            start_line = int(input(f"{COLOR_YELLOW}Enter start line number of the code block to extract: {COLOR_END}"))
            end_line = int(input(f"{COLOR_YELLOW}Enter end line number of the code block to extract: {COLOR_END}"))

            if not (1 <= start_line <= end_line <= num_lines):
                raise ValueError("Invalid line numbers.")
            break
        except ValueError as e:
            print(f"{COLOR_RED}Invalid input: {e}. Please enter valid line numbers.{COLOR_END}")

    code_block = get_code_block(filepath, start_line, end_line)
    print(f"\n{COLOR_BLUE}--- Selected Code Block ---{COLOR_END}")
    for i, line in enumerate(code_block):
        print(f"{start_line + i:4d} | {line}")
    print(f"{COLOR_BLUE}--------------------------{COLOR_END}\n")

    potential_params, potential_returns = analyze_code_block(full_file_lines, start_line, end_line)

    print(f"{COLOR_BLUE}--- Analysis Results ---{COLOR_END}")
    print(f"Suggested Parameters: {COLOR_GREEN}{potential_params if potential_params else 'None'}{COLOR_END}")
    print(f"Suggested Return Values: {COLOR_GREEN}{potential_returns if potential_returns else 'None'}{COLOR_END}\n")

    function_name = input(f"{COLOR_YELLOW}Enter desired new function name (e.g., 'processPayment'): {COLOR_END}")
    return_type = input(f"{COLOR_YELLOW}Enter desired return type (e.g., 'string', 'void', 'Promise<void>'): {COLOR_END}")

    param_declarations = []
    for param in potential_params:
        param_type = input(f"{COLOR_YELLOW}Enter type for parameter '{param}': {COLOR_END}")
        param_declarations.append(f"{param}: {param_type}")

    suggested_signature = f"function {function_name}({', '.join(param_declarations)}): {return_type} {{\n    // ... extracted code ...\n}}"

    print(f"\n{COLOR_BLUE}--- Suggested New Function Signature ---{COLOR_END}")
    print(f"{COLOR_GREEN}{suggested_signature}{COLOR_END}")
    print(f"\n{COLOR_YELLOW}Please manually replace the selected code block in {filepath} with a call to this new function.{COLOR_END}")
    print(f"{COLOR_BLUE}----------------------------------------{COLOR_END}")

if __name__ == '__main__':
    main()
