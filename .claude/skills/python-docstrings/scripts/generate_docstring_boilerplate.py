#!/usr/bin/env python3
"""
generate_docstring_boilerplate.py

This script generates docstring boilerplate (Google or NumPy style) for a given
Python function or class. It parses the function/class signature to pre-fill
parameters and return types.

Usage Examples:
    # Generate Google-style docstring for 'my_function' in 'src/utils.py'
    python generate_docstring_boilerplate.py src/utils.py my_function --style google

    # Generate NumPy-style docstring for 'MyClass' in 'src/models.py' with dry-run
    python generate_docstring_boilerplate.py src/models.py MyClass --style numpy --dry-run

    # Generate docstring for a specific line number (e.g., if multiple functions have the same name)
    python generate_docstring_boilerplate.py src/api.py fetch_data --line 15
"""

import argparse
import ast
import os
import sys
import re

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

def format_google_docstring(name, params, returns, is_class, indent=""):
    """Formats a docstring in Google style."""
    docstring_lines = []
    docstring_lines.append(f"{indent}"""A brief description of this {'class' if is_class else 'function'}.

{indent}    A more detailed explanation of what this {'class' if is_class else 'function'} does.
")

    if params:
        docstring_lines.append(f"{indent}    Args:")
        for param_name, param_type in params:
            docstring_lines.append(f"{indent}        {param_name} ({param_type}): Description of {param_name}.")
        docstring_lines.append("") # Blank line after args

    if returns and not is_class:
        docstring_lines.append(f"{indent}    Returns:")
        docstring_lines.append(f"{indent}        {returns}: Description of the return value.")
        docstring_lines.append("") # Blank line after returns

    docstring_lines.append(f"{indent}""" )
    return "\n".join(docstring_lines)

def format_numpy_docstring(name, params, returns, is_class, indent=""):
    """Formats a docstring in NumPy style."""
    docstring_lines = []
    docstring_lines.append(f"{indent}"""A brief description of this {'class' if is_class else 'function'}.

{indent}    A more detailed explanation of what this {'class' if is_class else 'function'} does.
")

    if params:
        docstring_lines.append(f"{indent}    Parameters")
        docstring_lines.append(f"{indent}    ----------")
        for param_name, param_type in params:
            docstring_lines.append(f"{indent}    {param_name} : {param_type}")
            docstring_lines.append(f"{indent}        Description of {param_name}.")
        docstring_lines.append("") # Blank line after parameters

    if returns and not is_class:
        docstring_lines.append(f"{indent}    Returns")
        docstring_lines.append(f"{indent}    ------- ")
        docstring_lines.append(f"{indent}    {returns}")
        docstring_lines.append(f"{indent}        Description of the return value.")
        docstring_lines.append("") # Blank line after returns

    docstring_lines.append(f"{indent}""" )
    return "\n".join(docstring_lines)

class FunctionVisitor(ast.NodeVisitor):
    def __init__(self, target_name, target_line=None):
        self.target_name = target_name
        self.target_line = target_line
        self.found_entity = None
        self.found_line_num = -1

    def visit_FunctionDef(self, node):
        if node.name == self.target_name and (self.target_line is None or node.lineno == self.target_line):
            self.found_entity = node
            self.found_line_num = node.lineno
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node):
        if node.name == self.target_name and (self.target_line is None or node.lineno == self.target_line):
            self.found_entity = node
            self.found_line_num = node.lineno
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        if node.name == self.target_name and (self.target_line is None or node.lineno == self.target_line):
            self.found_entity = node
            self.found_line_num = node.lineno
        self.generic_visit(node)

def parse_python_signature(file_path, target_name, target_line):
    """Parses a Python file to extract function/class signature details."""
    with open(file_path, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read(), filename=file_path)

    visitor = FunctionVisitor(target_name, target_line)
    visitor.visit(tree)

    if not visitor.found_entity:
        return None, None, None, None, -1

    node = visitor.found_entity
    params = []
    returns = ""
    is_class = isinstance(node, ast.ClassDef)

    if not is_class:
        # Function or AsyncFunction
        for arg in node.args.args:
            param_name = arg.arg
            param_type = ast.unparse(arg.annotation).strip() if arg.annotation else "Any"
            params.append((param_name, param_type))
        if node.returns:
            returns = ast.unparse(node.returns).strip()
        else:
            returns = "None"
    else:
        # Class
        # For classes, we don't extract params/returns in the same way as functions
        # The docstring will describe attributes and methods.
        pass

    # Get indentation from the original file content
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        indent = get_indentation(lines[node.lineno - 1])

    return params, returns, is_class, indent, node.lineno

def main():
    parser = argparse.ArgumentParser(
        description="Generate Python docstring boilerplate.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "file_path",
        help="Path to the Python file."
    )
    parser.add_argument(
        "target_name",
        help="Name of the function or class to document."
    )
    parser.add_argument(
        "--style",
        choices=["google", "numpy"],
        default="google",
        help="Docstring style to generate (default: google)."
    )
    parser.add_argument(
        "--line",
        type=int,
        help="Optional: Line number of the function/class definition (1-indexed)."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the generated docstring to stdout without modifying the file."
    )

    args = parser.parse_args()

    if not os.path.exists(args.file_path):
        print(f"{Fore.RED}Error: File not found at '{args.file_path}'.{Style.RESET_ALL}", file=sys.stderr)
        sys.exit(1)

    params, returns, is_class, indent, found_line = parse_python_signature(args.file_path, args.target_name, args.line)

    if found_line == -1:
        print(f"{Fore.RED}Error: Function or class '{args.target_name}' not found in '{args.file_path}'", file=sys.stderr)
        if args.line:
            print(f"{Fore.RED} at line {args.line}.{Style.RESET_ALL}", file=sys.stderr)
        else:
            print(f"{Fore.RED}. Consider using --line if multiple matches exist.{Style.RESET_ALL}", file=sys.stderr)
        sys.exit(1)

    if args.style == "google":
        docstring_block = format_google_docstring(args.target_name, params, returns, is_class, indent)
    elif args.style == "numpy":
        docstring_block = format_numpy_docstring(args.target_name, params, returns, is_class, indent)
    else:
        docstring_block = "" # Should not happen due to argparse choices

    with open(args.file_path, "r", encoding="utf-8") as f:
        code_lines = f.readlines()

    # Check if a docstring already exists
    # A docstring is typically the first statement in a function/class body
    # We need to find the line after the def/class statement
    insert_line_num = found_line
    if is_class:
        # For classes, the docstring is after the class header, potentially after bases/keywords
        # Find the first line that is not part of the class definition itself
        for i in range(found_line, len(code_lines)):
            stripped_line = code_lines[i].strip()
            if stripped_line and not stripped_line.startswith('#') and not stripped_line.startswith('@'):
                insert_line_num = i + 1
                break
    else:
        # For functions, it's usually the line after the def statement
        insert_line_num = found_line + 1

    # Check if there's already a docstring at the insert_line_num
    if insert_line_num < len(code_lines) and code_lines[insert_line_num].strip().startswith('"""') and code_lines[insert_line_num].strip().endswith('"""'):
        print(f"{Fore.YELLOW}Warning: A docstring already exists for '{args.target_name}' at line {insert_line_num + 1}. Skipping.{Style.RESET_ALL}", file=sys.stderr)
        sys.exit(0)

    if args.dry_run:
        print(f"{Fore.CYAN}--- DRY RUN: Generated Docstring for {args.target_name} ---
{Style.RESET_ALL}")
        print(docstring_block)
        print(f"{Fore.CYAN}--------------------------------------------------{Style.RESET_ALL}")
    else:
        # Insert docstring block after the found line
        new_code_lines = code_lines[:insert_line_num] + [docstring_block + "\n"] + code_lines[insert_line_num:]
        try:
            with open(args.file_path, "w", encoding="utf-8") as f:
                f.writelines(new_code_lines)
            print(f"{Fore.GREEN}Successfully generated {args.style}-style docstring for '{args.target_name}' in '{args.file_path}'.{Style.RESET_ALL}")
        except IOError as e:
            print(f"{Fore.RED}Error writing to file '{args.file_path}': {e}{Style.RESET_ALL}", file=sys.stderr)
            sys.exit(1)

if __name__ == "__main__":
    main()
