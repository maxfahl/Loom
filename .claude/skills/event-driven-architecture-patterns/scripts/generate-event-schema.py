

import argparse
import yaml
import os
from typing import Dict, Any

def generate_ts_interface(event_name: str, event_data: Dict[str, Any]) -> str:
    """Generates a TypeScript interface string for a given event."""
    interface_name = f"{event_name}Event"
    type_field = f"type: '{event_name}';"
    payload_properties = []

    properties = event_data.get('properties', {})
    for prop_name, prop_data in properties.items():
        ts_type = ""
        if prop_data['type'] == 'string':
            ts_type = 'string'
            if prop_data.get('format') == 'date-time':
                ts_type = 'string; // ISO 8601 date-time'
        elif prop_data['type'] == 'number':
            ts_type = 'number'
        elif prop_data['type'] == 'boolean':
            ts_type = 'boolean'
        elif prop_data['type'] == 'array':
            item_type = 'any'
            if 'items' in prop_data and 'properties' in prop_data['items']:
                # Handle inline object types for array items
                item_props = []
                for item_prop_name, item_prop_data in prop_data['items']['properties'].items():
                    item_ts_type = ""
                    if item_prop_data['type'] == 'string':
                        item_ts_type = 'string'
                    elif item_prop_data['type'] == 'number':
                        item_ts_type = 'number'
                    item_props.append(f"        {item_prop_name}: {item_ts_type};")
                item_type = f"{{
{'
'.join(item_props)}
      }}"
            elif 'items' in prop_data and 'type' in prop_data['items']:
                item_type = prop_data['items']['type']
            ts_type = f"Array<{item_type}>"
        elif prop_data['type'] == 'object':
            ts_type = 'any' # For simplicity, can be expanded to nested interfaces

        description = prop_data.get('description', '').strip()
        comment = f"  /** {description} */" if description else ""
        payload_properties.append(f"{comment}
  {prop_name}: {ts_type};")

    payload_str = "\n".join(payload_properties)

    return f"""
export interface {interface_name} {{
  {type_field}
  payload: {{
{payload_str}
  }};
}} """

def main():
    parser = argparse.ArgumentParser(
        description="Generate TypeScript event interfaces from a YAML definition.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "-i", "--input",
        required=True,
        help="Path to the input YAML file containing event definitions."
    )
    parser.add_argument(
        "-o", "--output-dir",
        required=True,
        help="Directory where the generated TypeScript files will be saved."
    )
    parser.add_argument(
        "-f", "--output-file",
        help="Optional: Single file name for all generated interfaces. If not provided, creates one file per event."
    )
    parser.add_argument(
        "-d", "--dry-run",
        action="store_true",
        help="Perform a dry run without writing any files."
    )

    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"Error: Input file '{args.input}' not found.")
        exit(1)

    os.makedirs(args.output_dir, exist_ok=True)

    with open(args.input, 'r') as f:
        config = yaml.safe_load(f)

    if 'events' not in config:
        print("Error: YAML file must contain an 'events' key.")
        exit(1)

    all_interfaces_content = []
    for event_name, event_data in config['events'].items():
        ts_interface = generate_ts_interface(event_name, event_data)
        all_interfaces_content.append(ts_interface)

        if not args.output_file:
            output_path = os.path.join(args.output_dir, f"{event_name.lower()}-event.ts")
            if not args.dry_run:
                with open(output_path, 'w') as f:
                    f.write(ts_interface)
                print(f"Generated '{output_path}'")
            else:
                print(f"Dry run: Would generate '{output_path}' with content:\n{ts_interface}")

    if args.output_file:
        output_path = os.path.join(args.output_dir, args.output_file)
        final_content = "\n".join(all_interfaces_content)
        if not args.dry_run:
            with open(output_path, 'w') as f:
                f.write(final_content)
            print(f"Generated '{output_path}'")
        else:
            print(f"Dry run: Would generate '{output_path}' with content:\n{final_content}")

if __name__ == "__main__":
    main()
