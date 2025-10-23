#!/usr/bin/env python3
"""
api-resource-generator.py: Generates boilerplate code for a new API resource.

This script creates basic model/schema, controller/handler, and routing entry
files for a given resource, based on its name and fields. It helps accelerate
the development of new API endpoints by providing a structured starting point.

Usage:
    python3 api-resource-generator.py [OPTIONS]

Options:
    --resource <name>       Required: The name of the API resource (e.g., 'User', 'Product').
    --fields <json_string>  Required: JSON string of fields for the resource.
                            Example: '[{"name":"id","type":"string",""format":"uuid"},{"name":"name","type":"string"}]'.
    --output-dir <path>     Specify the output directory for the generated files.
                            Defaults to './src/resources'.
    --dry-run               Print the actions that would be taken without
                            actually creating or modifying files.
    --help                  Show this help message and exit.

Example:
    python3 api-resource-generator.py --resource Product --fields '[{"name":"id","type":"string","format":"uuid"},{"name":"name","type":"string"},{"name":"price","type":"number","format":"float"}]' --output-dir ./src/api/v1/resources
    python3 api-resource-generator.py --resource User --fields '[{"name":"id","type":"string","format":"uuid"},{"name":"email","type":"string"},{"name":"password","type":"string"}]'
"""

import argparse
import json
import sys
from pathlib import Path
from typing import List, Dict, Any
from colorama import Fore, Style, init

# Initialize colorama for cross-platform colored output
init(autoreset=True)

def print_success(message):
    print(f"{Fore.GREEN}✓ {message}{Style.RESET_ALL}")

def print_info(message):
    print(f"{Fore.CYAN}ℹ {message}{Style.RESET_ALL}")

def print_warning(message):
    print(f"{Fore.YELLOW}▲ {message}{Style.RESET_ALL}")

def print_error(message):
    print(f"{Fore.RED}✗ {message}{Style.RESET_ALL}")

def to_camel_case(snake_str: str) -> str:
    components = snake_str.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])

def to_pascal_case(snake_str: str) -> str:
    return ''.join(x.title() for x in snake_str.split('_'))

def generate_model_content(resource_name: str, fields: List[Dict[str, Any]]) -> str:
    pascal_name = to_pascal_case(resource_name)
    properties = []
    for field in fields:
        field_name = field["name"]
        field_type = field["type"]
        nullable = "?" if field.get("nullable", False) else ""
        properties.append(f