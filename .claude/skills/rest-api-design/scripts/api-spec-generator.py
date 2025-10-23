#!/usr/bin/env python3
"""
api-spec-generator.py: Generates a basic OpenAPI (Swagger) specification YAML file.

This script helps kickstart API documentation by generating a foundational OpenAPI
spec based on a resource name and its fields. It supports defining basic CRUD
operations and common data types.

Usage:
    python3 api-spec-generator.py [OPTIONS]

Options:
    --resource <name>       Required: The name of the API resource (e.g., 'User', 'Product').
    --fields <json_string>  Required: JSON string of fields for the resource.
                            Example: '[{"name":"id","type":"string","format":"uuid"},{"name":"name","type":"string"}]'.
    --output-file <path>    Specify the output YAML file path. Defaults to './openapi.yaml'.
    --dry-run               Print the actions that would be taken without
                            actually creating or modifying files.
    --help                  Show this help message and exit.

Example:
    python3 api-spec-generator.py --resource Product --fields '[{"name":"id","type":"string","format":"uuid"},{"name":"name","type":"string"},{"name":"price","type":"number","format":"float"},{"name":"description","type":"string","nullable":true}]' --output-file ./product_api.yaml
    python3 api-spec-generator.py --resource Order --fields '[{"name":"id","type":"string","format":"uuid"},{"name":"userId","type":"string"},{"name":"total","type":"number"}]'
"""

import argparse
import json
import sys
from pathlib import Path
from typing import List, Dict, Any
import yaml
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

def generate_openapi_spec(
    resource_name: str,
    fields: List[Dict[str, Any]]
) -> Dict[str, Any]:
    resource_lower = resource_name.lower()
    resource_plural = resource_lower + "s" if not resource_lower.endswith("s") else resource_lower

    properties = {}
    required_fields = []
    for field in fields:
        field_name = field["name"]
        field_type = field["type"]
        field_format = field.get("format")
        field_nullable = field.get("nullable", False)

        prop_def = {"type": field_type}
        if field_format: prop_def["format"] = field_format
        if field_nullable: prop_def["nullable"] = True

        properties[field_name] = prop_def
        if not field_nullable and field_name != "id": # ID is often auto-generated
            required_fields.append(field_name)

    schema_name = resource_name
    schema_name_input = f"{resource_name}Input"

    spec = {
        "openapi": "3.0.0",
        "info": {
            "title": f"{resource_name} API",
            "version": "1.0.0",
            "description": f"API for managing {resource_plural}."
        },
        "servers": [
            {"url": "/api/v1"}
        ],
        "paths": {
            f"/{resource_plural}": {
                "get": {
                    "summary": f"Get all {resource_plural}",
                    "responses": {
                        "200": {
                            "description": f"A list of {resource_plural}",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "array",
                                        "items": {"$ref": f"#/components/schemas/{schema_name}"}
                                    }
                                }
                            }
                        }
                    }
                },
                "post": {
                    "summary": f"Create a new {resource_name}",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {"$ref": f"#/components/schemas/{schema_name_input}"}
                            }
                        }
                    },
                    "responses": {
                        "201": {
                            "description": f"The created {resource_name}",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": f"#/components/schemas/{schema_name}"}
                                }
                            }
                        }
                    }
                }
            },
            f"/{resource_plural}/{{id}}": {
                "get": {
                    "summary": f"Get a {resource_name} by ID",
                    "parameters": [
                        {
                            "name": "id",
                            "in": "path",
                            "required": True,
                            "schema": {"type": "string", "format": "uuid"}
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": f"The {resource_name} object",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": f"#/components/schemas/{schema_name}"}
                                }
                            }
                        },
                        "404": {"description": f"{resource_name} not found"}
                    }
                },
                "put": {
                    "summary": f"Update a {resource_name} by ID",
                    "parameters": [
                        {
                            "name": "id",
                            "in": "path",
                            "required": True,
                            "schema": {"type": "string", "format": "uuid"}
                        }
                    ],
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {"$ref": f"#/components/schemas/{schema_name_input}"}
                            }
                        }
                    },
                    "responses": {
                        "200": {
                            "description": f"The updated {resource_name}",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": f"#/components/schemas/{schema_name}"}
                                }
                            }
                        },
                        "404": {"description": f"{resource_name} not found"}
                    }
                },
                "delete": {
                    "summary": f"Delete a {resource_name} by ID",
                    "parameters": [
                        {
                            "name": "id",
                            "in": "path",
                            "required": True,
                            "schema": {"type": "string", "format": "uuid"}
                        }
                    ],
                    "responses": {
                        "204": {"description": f"{resource_name} deleted successfully"},
                        "404": {"description": f"{resource_name} not found"}
                    }
                }
            }
        },
        "components": {
            "schemas": {
                schema_name: {
                    "type": "object",
                    "properties": properties,
                    "required": required_fields
                },
                schema_name_input: {
                    "type": "object",
                    "properties": {k: v for k, v in properties.items() if k != "id"},
                    "required": [r for r in required_fields if r != "id"]
                }
            }
        }
    }
    return spec

def main():
    parser = argparse.ArgumentParser(
        description="Generates a basic OpenAPI (Swagger) specification YAML file."
    )
    parser.add_argument(
        "--resource",
        type=str,
        required=True,
        help="The name of the API resource (e.g., 'User', 'Product')."
    )
    parser.add_argument(
        "--fields",
        type=str,
        required=True,
        help="JSON string of fields for the resource. Example: '[{"name":"id","type":"string","format":"uuid"},{"name":"name","type":"string"}]'."
    )
    parser.add_argument(
        "--output-file",
        type=str,
        default="./openapi.yaml",
        help="Specify the output YAML file path. Defaults to './openapi.yaml'."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the actions that would be taken without actually creating or modifying files."
    )
    args = parser.parse_args()

    output_file_path = Path(args.output_file)
    dry_run = args.dry_run

    try:
        fields_data = json.loads(args.fields)
    except json.JSONDecodeError:
        print_error("Invalid JSON string provided for --fields.")
        sys.exit(1)

    print_info(f"Generating OpenAPI spec for resource: {args.resource}")
    if dry_run:
        print_warning("Running in DRY-RUN mode. No files will be created or modified.")

    openapi_spec = generate_openapi_spec(args.resource, fields_data)

    if dry_run:
        print_info(f"Would write OpenAPI spec to: {output_file_path}")
        print_info(f"Generated OpenAPI Spec (partial):\n---\n{yaml.dump(openapi_spec, indent=2, default_flow_style=False)[:1000]}...\n---")
    else:
        try:
            output_file_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_file_path, "w") as f:
                yaml.dump(openapi_spec, f, indent=2, default_flow_style=False)
            print_success(f"Successfully generated OpenAPI spec to: {output_file_path}")
        except IOError as e:
            print_error(f"Error writing to file {output_file_path}: {e}")
            sys.exit(1)

if __name__ == "__main__":
    main()
