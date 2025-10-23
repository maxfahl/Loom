#!/usr/bin/env python3

# validate-dependency-rule.py
#
# Purpose:
#   Scans the codebase to ensure that the Clean Architecture dependency rule is not violated.
#   It identifies instances where an inner layer directly imports or depends on a module
#   from an outer layer, which is a critical anti-pattern. This helps maintain architectural
#   integrity over time.
#
# Usage:
#   ./validate-dependency-rule.py [-p <project_root>] [-c <config_file>]
#
# Arguments:
#   -p, --project-root  Optional. The root directory of your project. Defaults to the current directory.
#   -c, --config        Optional. Path to a YAML configuration file defining layer order and aliases.
#                       Defaults to a basic configuration.
#
# Configuration (YAML example for -c):
#   layer_order:
#     - domain
#     - application
#     - infrastructure
#     - presentation
#   layer_aliases:
#     domain: [entities, value-objects]
#     application: [use-cases, ports, dtos]
#     infrastructure: [persistence, services, config]
#     presentation: [controllers, routes, middlewares]
#
# Error Handling:
#   Prints detailed error messages for dependency violations.
#   Exits with a non-zero status code if violations are found.
#
# Colored Output:
#   Uses ANSI escape codes for colored output (green for success, red for error, yellow for warnings).

import os
import re
import argparse
import sys
import yaml

# --- Colors ---
GREEN = "\033[0;32m"
RED = "\033[0;31m"
YELLOW = "\033[0;33m"
NC = "\033[0m" # No Color

DEFAULT_LAYER_ORDER = [
    "domain",
    "application",
    "infrastructure",
    "presentation",
]

DEFAULT_LAYER_ALIASES = {
    "domain": ["entities", "value-objects"],
    "application": ["use-cases", "ports", "dtos"],
    "infrastructure": ["persistence", "services", "config"],
    "presentation": ["controllers", "routes", "middlewares"],
}

def get_layer_from_path(filepath, base_dir, layer_order, layer_aliases):
    """Determines the Clean Architecture layer of a given file path."""
    relative_path = os.path.relpath(filepath, base_dir)
    parts = relative_path.split(os.sep)

    if not parts:
        return None

    # Check for direct layer names (e.g., 'domain/entities')
    for i, layer_name in enumerate(layer_order):
        if parts[0] == layer_name:
            # Check for sub-aliases if available
            if len(parts) > 1 and layer_name in layer_aliases:
                for alias in layer_aliases[layer_name]:
                    if parts[1] == alias:
                        return layer_name, i
            return layer_name, i

    return None

def analyze_file_for_dependencies(filepath, base_dir, layer_map, layer_order_map):
    """Analyzes a TypeScript file for import statements and checks for dependency violations."""
    violations = []
    current_layer_info = get_layer_from_path(filepath, base_dir, list(layer_map.keys()), layer_map)

    if not current_layer_info:
        return violations # File is not in a recognized Clean Architecture layer

    current_layer_name, current_layer_index = current_layer_info

    with open(filepath, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            # Regex to find import paths (handles various import syntaxes)
            match = re.search(r"from\s+['"]([^'"]+)['"]", line)
            if match:
                imported_path_raw = match.group(1)
                # Resolve relative paths
                if imported_path_raw.startswith('.'):
                    imported_path = os.path.abspath(os.path.join(os.path.dirname(filepath), imported_path_raw))
                else:
                    # Assume absolute imports are fine or handled by build system
                    # For simplicity, we only check relative paths within the project structure
                    continue

                # Ensure the imported path is within the project's base_dir
                if not imported_path.startswith(base_dir):
                    continue

                imported_layer_info = get_layer_from_path(imported_path, base_dir, list(layer_map.keys()), layer_map)

                if imported_layer_info:
                    imported_layer_name, imported_layer_index = imported_layer_info

                    # Check dependency rule: inner layer (higher index) should not depend on outer layer (lower index)
                    if current_layer_index > imported_layer_index:
                        violations.append({
                            "file": filepath,
                            "line": line_num,
                            "current_layer": current_layer_name,
                            "imported_layer": imported_layer_name,
                            "imported_path": imported_path_raw,
                            "message": f"Layer '{current_layer_name}' (index {current_layer_index}) imports from outer layer '{imported_layer_name}' (index {imported_layer_index})."
                        })
    return violations

def main():
    parser = argparse.ArgumentParser(
        description="Validate Clean Architecture dependency rules in TypeScript files."
    )
    parser.add_argument(
        "-p", "--project-root",
        default=".",
        help="The root directory of your project. Defaults to current directory."
    )
    parser.add_argument(
        "-c", "--config",
        help="Path to a YAML configuration file defining layer order and aliases."
    )
    args = parser.parse_args()

    project_root = os.path.abspath(args.project_root)
    base_src_dir = os.path.join(project_root, "src")

    layer_order = DEFAULT_LAYER_ORDER
    layer_aliases = DEFAULT_LAYER_ALIASES

    if args.config:
        try:
            with open(args.config, 'r') as f:
                config = yaml.safe_load(f)
                if 'layer_order' in config: 
                    layer_order = config['layer_order']
                if 'layer_aliases' in config: 
                    layer_aliases = config['layer_aliases']
        except FileNotFoundError:
            print(f"{RED}Error: Configuration file not found at {args.config}{NC}")
            sys.exit(1)
        except yaml.YAMLError as e:
            print(f"{RED}Error parsing YAML configuration file: {e}{NC}")
            sys.exit(1)

    # Create a combined layer map for easier lookup
    # { 'domain': 0, 'application': 1, ... }
    layer_order_map = {layer: i for i, layer in enumerate(layer_order)}
    
    # Expand layer_aliases to include direct layer names for get_layer_from_path
    full_layer_map = {}
    for layer_name, aliases in layer_aliases.items():
        full_layer_map[layer_name] = aliases # Keep original aliases
        # Add the layer name itself as an alias for direct matching
        if layer_name not in full_layer_map[layer_name]:
            full_layer_map[layer_name].append(layer_name)

    all_violations = []

    print(f"{YELLOW}Scanning for Clean Architecture dependency violations in {base_src_dir}...{NC}")

    for root, _, files in os.walk(base_src_dir):
        for file in files:
            if file.endswith((".ts", ".tsx")):
                filepath = os.path.join(root, file)
                all_violations.extend(analyze_file_for_dependencies(filepath, base_src_dir, full_layer_map, layer_order_map))

    if all_violations:
        print(f"{RED}\n--- Dependency Rule Violations Found ({len(all_violations)}) ---"{NC})
        for violation in all_violations:
            print(f"{RED}  File: {violation['file']}:{violation['line']}{NC}")
            print(f"{RED}    Violation: {violation['message']}{NC}")
            print(f"{RED}    Imported: {violation['imported_path']}{NC}")
            print("\n")
        sys.exit(1)
    else:
        print(f"{GREEN}No Clean Architecture dependency violations found!{NC}")
        sys.exit(0)

if __name__ == "__main__":
    main()
