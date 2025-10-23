#!/usr/bin/env python3
import argparse
import yaml
import os

def generate_typescript_interface(config_path, output_path):
    """
    Generates a TypeScript interface for an AuditEvent based on a YAML configuration.

    Args:
        config_path (str): Path to the YAML configuration file.
        output_path (str): Path to the output TypeScript file.
    """
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
    except FileNotFoundError:
        print(f"Error: Configuration file not found at '{config_path}'")
        return
    except yaml.YAMLError as e:
        print(f"Error parsing YAML configuration: {e}")
        return

    interface_name = config.get('interfaceName', 'AuditEvent')
    fields = config.get('fields', [])

    ts_interface = f"export interface {interface_name} {{
"

    for field in fields:
        name = field.get('name')
        type_ = field.get('type')
        optional = field.get('optional', False)
        description = field.get('description', '')

        if not name or not type_:
            print(f"Warning: Skipping malformed field in config: {field}")
            continue

        optional_char = '?' if optional else ''
        ts_interface += f"  {name}{optional_char}: {type_}; // {description}\n"

    ts_interface += "} 
"

    try:
        with open(output_path, 'w') as f:
            f.write(ts_interface)
        print(f"Successfully generated TypeScript interface to '{output_path}'")
    except IOError as e:
        print(f"Error writing TypeScript file: {e}")

def main():
    parser = argparse.ArgumentParser(
        description="Generate a TypeScript interface for an AuditEvent from a YAML configuration.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        '-c', '--config',
        default='audit-event-config.yaml',
        help='Path to the YAML configuration file (default: audit-event-config.yaml)'
    )
    parser.add_argument(
        '-o', '--output',
        default='audit-event.interface.ts',
        help='Path to the output TypeScript file (default: audit-event.interface.ts)'
    )
    args = parser.parse_args()

    # Ensure output directory exists
    output_dir = os.path.dirname(args.output)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    generate_typescript_interface(args.config, args.output)

if __name__ == "__main__":
    main()
