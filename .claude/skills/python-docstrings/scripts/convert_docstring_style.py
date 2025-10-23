#!/usr/bin/env python3
"""
convert_docstring_style.py

This script converts docstrings in Python files from one style (e.g., reStructuredText)
to another (e.g., Google or NumPy style). This is useful for standardizing docstring
formats across a project.

Usage Examples:
    # Convert reST docstrings to Google style in a single file
    python convert_docstring_style.py src/my_module.py --from rst --to google

    # Convert reST docstrings to NumPy style in a directory with dry-run
    python convert_docstring_style.py src/ --from rst --to numpy --dry-run

    # Convert reST docstrings to Google style and overwrite the original files
    python convert_docstring_style.py src/ --from rst --to google --in-place
"""

import argparse
import os
import re
import sys
import textwrap

try:
    from colorama import Fore, Style, init
    init(autoreset=True)
except ImportError:
    class Color:
        def __getattr__(self, name):
            return ''
    Fore = Color()
    Style = Color()

def parse_rst_docstring(docstring_content):
    """Parses an reStructuredText docstring and extracts components."""
    summary = []
    description = []
    params = []
    returns = None
    raises = []

    lines = docstring_content.splitlines()
    current_section = summary

    param_pattern = re.compile(r':param\s+(?P<type>[^:]+):\s+(?P<name>[a-zA-Z_][a-zA-Z0-9_]*):\s*(?P<desc>.*)')
    type_pattern = re.compile(r':type\s+(?P<name>[a-zA-Z_][a-zA-Z0-9_]*):\s*(?P<type>.*)')
    return_pattern = re.compile(r':returns:\s*(?P<desc>.*)')
    rtype_pattern = re.compile(r':rtype:\s*(?P<type>.*)')
    raises_pattern = re.compile(r':raises\s+(?P<type>[^:]+):\s*(?P<desc>.*)')

    param_types = {}

    for line in lines:
        line = line.strip()
        if not line:
            if current_section is summary and summary:
                current_section = description
            continue

        param_match = param_pattern.match(line)
        type_match = type_pattern.match(line)
        return_match = return_pattern.match(line)
        rtype_match = rtype_pattern.match(line)
        raises_match = raises_pattern.match(line)

        if param_match:
            current_section = params
            params.append({
                "name": param_match.group('name'),
                "type": param_match.group('type'),
                "desc": param_match.group('desc')
            })
        elif type_match:
            param_types[type_match.group('name')] = type_match.group('type')
        elif return_match:
            current_section = returns
            returns = {"desc": return_match.group('desc'), "type": None}
        elif rtype_match:
            if returns: returns["type"] = rtype_match.group('type')
        elif raises_match:
            current_section = raises
            raises.append({"type": raises_match.group('type'), "desc": raises_match.group('desc')})
        else:
            if current_section is summary:
                summary.append(line)
            elif current_section is description:
                description.append(line)
            elif current_section is params and params:
                # Append to last param description
                params[-1]["desc"] += " " + line
            elif current_section is returns and returns:
                returns["desc"] += " " + line
            elif current_section is raises and raises:
                raises[-1]["desc"] += " " + line

    # Merge types from :type: into :param:
    for p in params:
        if p["name"] in param_types:
            p["type"] = param_types[p["name"]]

    return {
        "summary": " ".join(summary).strip(),
        "description": " ".join(description).strip(),
        "params": params,
        "returns": returns,
        "raises": raises
    }

def format_google_docstring(parsed_docstring, indent=""):
    """Formats parsed docstring into Google style."""
    lines = []
    if parsed_docstring["summary"]:
        lines.append(parsed_docstring["summary"])
    if parsed_docstring["description"]:
        lines.append("")
        lines.append(parsed_docstring["description"])

    if parsed_docstring["params"]:
        lines.append("")
        lines.append("Args:")
        for p in parsed_docstring["params"]:
            lines.append(f"    {p["name"]} ({p["type"] or 'Any'}): {p["desc"]}")

    if parsed_docstring["returns"] and parsed_docstring["returns"]["type"]:
        lines.append("")
        lines.append("Returns:")
        lines.append(f"    {parsed_docstring["returns"]["type"]}: {parsed_docstring["returns"]["desc"]}")

    if parsed_docstring["raises"]:
        lines.append("")
        lines.append("Raises:")
        for r in parsed_docstring["raises"]:
            lines.append(f"    {r["type"]}: {r["desc"]}")

    # Add triple quotes and indentation
    formatted_lines = [f'{indent}"""' + lines[0]] if lines else [f'{indent}"""'"""']
    for line in lines[1:]:
        formatted_lines.append(f'{indent}{line}')
    formatted_lines.append(f'{indent}"""'')

    return "\n".join(formatted_lines)

def format_numpy_docstring(parsed_docstring, indent=""):
    """Formats parsed docstring into NumPy style."""
    lines = []
    if parsed_docstring["summary"]:
        lines.append(parsed_docstring["summary"])
    if parsed_docstring["description"]:
        lines.append("")
        lines.append(parsed_docstring["description"])

    if parsed_docstring["params"]:
        lines.append("")
        lines.append("Parameters")
        lines.append("----------")
        for p in parsed_docstring["params"]:
            lines.append(f"{p["name"]} : {p["type"] or 'Any'}")
            lines.append(f"    {p["desc"]}")

    if parsed_docstring["returns"] and parsed_docstring["returns"]["type"]:
        lines.append("")
        lines.append("Returns")
        lines.append("-------")
        lines.append(f"{parsed_docstring["returns"]["type"]}")
        lines.append(f"    {parsed_docstring["returns"]["desc"]}")

    if parsed_docstring["raises"]:
        lines.append("")
        lines.append("Raises")
        lines.append("------")
        for r in parsed_docstring["raises"]:
            lines.append(f"{r["type"]}")
            lines.append(f"    {r["desc"]}")

    # Add triple quotes and indentation
    formatted_lines = [f'{indent}"""' + lines[0]] if lines else [f'{indent}"""'"""']
    for line in lines[1:]:
        formatted_lines.append(f'{indent}{line}')
    formatted_lines.append(f'{indent}"""'')

    return "\n".join(formatted_lines)

def process_file(file_path, from_style, to_style, in_place, dry_run):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Find all docstrings
    # This regex is a bit simplified and might need refinement for complex cases
    # It looks for triple-quoted strings immediately after def/class
    docstring_pattern = re.compile(
        r'^(\s*)(?:def|class)\s+[^:]+:\s*\n'  # def or class line
        r'\1\s*("""(?:[^\\]|\\.)*?"""|"""(?:[^\\]|\\.)*?""")', # docstring
        re.MULTILINE | re.DOTALL
    )

    new_content = content
    replacements_made = 0

    for match in reversed(list(docstring_pattern.finditer(content))):
        full_match = match.group(0)
        indent = match.group(1)
        docstring_raw = match.group(2)

        # Remove quotes from docstring content
        docstring_content = docstring_raw[3:-3]

        if from_style == "rst":
            parsed = parse_rst_docstring(docstring_content)
        else:
            print(f"{Fore.RED}Error: Unsupported source style '{from_style}'.{Style.RESET_ALL}", file=sys.stderr)
            return False

        if to_style == "google":
            new_docstring = format_google_docstring(parsed, indent)
        elif to_style == "numpy":
            new_docstring = format_numpy_docstring(parsed, indent)
        else:
            print(f"{Fore.RED}Error: Unsupported target style '{to_style}'.{Style.RESET_ALL}", file=sys.stderr)
            return False

        # Replace the old docstring with the new one
        # Need to handle the original indentation of the docstring
        # The new_docstring already includes the correct indentation
        start_index = match.start(2) # Start of the docstring quotes
        end_index = match.end(2)     # End of the docstring quotes

        # Reconstruct the full line including def/class and the new docstring
        # This is tricky because the regex captures the def/class line and the docstring
        # A simpler approach is to replace just the docstring part
        new_content = new_content[:start_index] + new_docstring + new_content[end_index:]
        replacements_made += 1

    if replacements_made > 0:
        if dry_run:
            print(f"{Fore.CYAN}--- DRY RUN: Converted Docstrings in {file_path} ---
{Style.RESET_ALL}")
            print(new_content)
            print(f"{Fore.CYAN}--------------------------------------------------{Style.RESET_ALL}")
        elif in_place:
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(new_content)
                print(f"{Fore.GREEN}Converted {replacements_made} docstrings in '{file_path}' to {to_style} style.{Style.RESET_ALL}")
            except IOError as e:
                print(f"{Fore.RED}Error writing to file '{file_path}': {e}{Style.RESET_ALL}", file=sys.stderr)
                return False
        else:
            print(f"{Fore.GREEN}Converted {replacements_made} docstrings in '{file_path}' to {to_style} style. (Not saved, use --in-place to save or --dry-run to preview){Style.RESET_ALL}")
    else:
        print(f"{Fore.YELLOW}No docstrings found or converted in '{file_path}'.{Style.RESET_ALL}")

    return True

def main():
    parser = argparse.ArgumentParser(
        description="Convert Python docstring styles.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "path",
        help="Path to a Python file or directory to scan."
    )
    parser.add_argument(
        "--from",
        dest="from_style",
        choices=["rst"],
        required=True,
        help="Source docstring style (e.g., rst)."
    )
    parser.add_argument(
        "--to",
        dest="to_style",
        choices=["google", "numpy"],
        required=True,
        help="Target docstring style (e.g., google, numpy)."
    )
    parser.add_argument(
        "--in-place",
        action="store_true",
        help="Modify files in place. Use with caution."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the converted content to stdout without modifying files."
    )

    args = parser.parse_args()

    target_files = []
    if os.path.isfile(args.path):
        target_files.append(args.path)
    elif os.path.isdir(args.path):
        for root, _, files in os.walk(args.path):
            for file in files:
                if file.endswith(".py"):
                    target_files.append(os.path.join(root, file))
    else:
        print(f"{Fore.RED}Error: Invalid path '{args.path}'. Must be a file or directory.{Style.RESET_ALL}", file=sys.stderr)
        sys.exit(1)

    if not target_files:
        print(f"{Fore.YELLOW}No Python files found in '{args.path}'.{Style.RESET_ALL}")
        sys.exit(0)

    for file_path in target_files:
        process_file(file_path, args.from_style, args.to_style, args.in_place, args.dry_run)

if __name__ == "__main__":
    main()
