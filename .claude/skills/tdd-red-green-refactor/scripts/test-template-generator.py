#!/usr/bin/env python3

# test-template-generator.py
# Description: Generates boilerplate test files for a given source file,
#              encouraging test-first development.
# Usage: python3 test-template-generator.py <source_file_path> [--lang <language>] [--output-dir <dir>]
#
# Options:
#   --lang <language>   Specify the language of the source file: 'ts' (TypeScript, default), 'py' (Python).
#   --output-dir <dir>  Specify the directory where the test file should be created.
#                       Defaults to a 'test/' or '__tests__/' subdirectory relative to the source file.
#   --help              Display this help message.

import os
import argparse
import re
from typing import List
import ast

# --- Configuration Variables ---
COLOR_RESET = "\033[0m"
COLOR_RED = "\033[0;31m"
COLOR_GREEN = "\033[0;32m"
COLOR_YELLOW = "\033[0;33m"
COLOR_BLUE = "\033[0;34m"
COLOR_CYAN = "\033[0;36m"

# --- Helper Functions ---
def log_info(message: str):
    print(f"{COLOR_BLUE}[INFO]{COLOR_RESET} {message}")

def log_success(message: str):
    print(f"{COLOR_GREEN}[SUCCESS]{COLOR_RESET} {message}")

def log_warning(message: str):
    print(f"{COLOR_YELLOW}[WARNING]{COLOR_RESET} {message}")

def log_error(message: str):
    print(f"{COLOR_RED}[ERROR]{COLOR_RESET} {message}")
    exit(1)

def generate_ts_test_content(source_file_name: str, functions: List[str]) -> str:
    imports = ''.join([f"  {{ {func} }},
" for func in functions])
    if imports:
        imports = f"import {{
{imports}}} from './{source_file_name.replace('.ts', '')}';\n\n"

    test_blocks = []
    for func in functions:
        test_blocks.append(f"describe('{func}', () => {{\n  it('should do something', () => {{\n    // Arrange
    // Act
    // Assert
    expect(true).toBe(false); // Failing test by default (Red phase)
  }});
}})")

    return f"""// {source_file_name.replace('.ts', '.test.ts')}
{imports}describe('{source_file_name.replace('.ts', '')}', () => {{
  // Add setup/teardown here if needed
}})

{ 'textbackslashn'.join(test_blocks)}"""

def generate_py_test_content(source_file_name: str, functions: List[str]) -> str:
    imports = ''.join([f"from {source_file_name.replace('.py', '')} import {func}\n" for func in functions])
    if imports:
        imports = f"{imports}\n"

    test_blocks = []
    for func in functions:
        test_blocks.append(f"def test_{func}():
    # Arrange
    # Act
    # Assert
    assert False # Failing test by default (Red phase)\n")

    return f"""# test_{source_file_name}
import pytest
{imports}
{ 'textbackslashn'.join(test_blocks)}"""

def extract_functions_ts(file_path: str) -> List[str]:
    functions = []
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        # Regex to find exported functions (simple, might miss some cases)
        matches = re.findall(r'export\s+(?:async\s+)?function\s+([a-zA-Z_][a-zA-Z0-9_]*)\(.*\)', content)
        functions.extend(matches)
        # Regex to find exported const arrow functions
        matches = re.findall(r'export\s+const\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*(?:async\s+)?\(.*
)\s*=>', content)
        functions.extend(matches)
    return functions

def extract_functions_py(file_path: str) -> List[str]:
    functions = []
    with open(file_path, 'r', encoding='utf-8') as f:
        tree = ast.parse(f.read())
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                functions.append(node.name)
    return functions

def main():
    parser = argparse.ArgumentParser(
        description="Generate boilerplate test files for a given source file."
    )
    parser.add_argument(
        "source_file_path",
        help="Path to the source file for which to generate tests."
    )
    parser.add_argument(
        "--lang",
        default="ts",
        choices=["ts", "py"],
        help="Language of the source file (default: ts)"
    )
    parser.add_argument(
        "--output-dir",
        help="Directory where the test file should be created."
    )
    args = parser.parse_args()

    source_file_path = os.path.abspath(args.source_file_path)

    if not os.path.exists(source_file_path):
        log_error(f"Source file not found: {source_file_path}")

    source_dir = os.path.dirname(source_file_path)
    source_file_name = os.path.basename(source_file_path)
    base_name, ext = os.path.splitext(source_file_name)

    if args.output_dir:
        output_dir = os.path.abspath(args.output_dir)
    else:
        if args.lang == "ts":
            output_dir = os.path.join(source_dir, "__tests__")
        elif args.lang == "py":
            output_dir = os.path.join(source_dir, "test")
        else:
            log_error("Unsupported language for default output directory.")

    os.makedirs(output_dir, exist_ok=True)

    test_file_name = ""
    test_content = ""
    functions_to_test: List[str] = []

    if args.lang == "ts":
        test_file_name = f"{base_name}.test.ts"
        functions_to_test = extract_functions_ts(source_file_path)
        test_content = generate_ts_test_content(source_file_name, functions_to_test)
    elif args.lang == "py":
        test_file_name = f"test_{base_name}.py"
        functions_to_test = extract_functions_py(source_file_path)
        test_content = generate_py_test_content(source_file_name, functions_to_test)

    test_file_path = os.path.join(output_dir, test_file_name)

    if os.path.exists(test_file_path):
        log_warning(f"Test file already exists: {test_file_path}. Skipping creation.")
    else:
        with open(test_file_path, 'w', encoding='utf-8') as f:
            f.write(test_content)
        log_success(f"Generated test file: {test_file_path}")
        if functions_to_test:
            log_info(f"Detected functions: {', '.join(functions_to_test)}. Boilerplate tests created.")
        else:
            log_warning("No functions detected in source file. Generated an empty test file.")

    log_success("Test template generation complete!")

if __name__ == "__main__":
    main()
