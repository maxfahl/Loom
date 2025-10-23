#!/usr/bin/env python3

import argparse
import json
import yaml
from collections import defaultdict

def load_dfd(file_path):
    """Loads a DFD from a JSON or YAML file."""
    try:
        with open(file_path, 'r') as f:
            if file_path.endswith('.json'):
                return json.load(f)
            elif file_path.endswith('.yaml') or file_path.endswith('.yml'):
                return yaml.safe_load(f)
            else:
                raise ValueError("Unsupported file format. Please use .json or .yaml")
    except FileNotFoundError:
        print(f"Error: DFD file not found at {file_path}")
        exit(1)
    except (json.JSONDecodeError, yaml.YAMLError) as e:
        print(f"Error parsing DFD file {file_path}: {e}")
        exit(1)

def apply_stride(dfd_data):
    """Applies STRIDE methodology to DFD components and interactions."""
    threats = defaultdict(lambda: defaultdict(list))

    # Define STRIDE categories and their relevance to DFD elements
    stride_categories = {
        "Spoofing": ["process", "external_entity", "user"], # Impersonation
        "Tampering": ["data_flow", "data_store"], # Unauthorized modification
        "Repudiation": ["process", "external_entity", "user"], # Denying actions
        "Information Disclosure": ["data_flow", "data_store"], # Unauthorized access to data
        "Denial of Service": ["process", "external_entity"], # Preventing legitimate access
        "Elevation of Privilege": ["process", "user"] # Gaining unauthorized higher privileges
    }

    # Process components (processes, external entities, users)
    for entity_type in ["processes", "external_entities", "users"]:
        if entity_type in dfd_data:
            for entity in dfd_data[entity_type]:
                entity_name = entity.get("name")
                entity_description = entity.get("description", "")
                if not entity_name: continue

                for stride, relevant_types in stride_categories.items():
                    if entity_type.rstrip('s') in relevant_types or (entity_type == "users" and "user" in relevant_types):
                        threats[entity_name][stride].append(f"Potential {stride} threat against {entity_name} ({entity_description}).")

    # Process data stores
    if "data_stores" in dfd_data:
        for store in dfd_data["data_stores"]:
            store_name = store.get("name")
            store_description = store.get("description", "")
            if not store_name: continue

            for stride in ["Tampering", "Information Disclosure"]:
                threats[store_name][stride].append(f"Potential {stride} threat against data store {store_name} ({store_description}).")

    # Process data flows
    if "data_flows" in dfd_data:
        for flow in dfd_data["data_flows"]:
            flow_name = flow.get("name", f"Flow from {flow.get('source')} to {flow.get('destination')}")
            flow_description = flow.get("description", "")
            source = flow.get("source")
            destination = flow.get("destination")

            if not source or not destination: continue

            for stride in ["Tampering", "Information Disclosure"]:
                threats[flow_name][stride].append(
                    f"Potential {stride} threat on data flow '{flow_name}' from {source} to {destination} ({flow_description})."
                )

    return threats

def main():
    parser = argparse.ArgumentParser(
        description="Analyze a Data Flow Diagram (DFD) and suggest potential STRIDE threats.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "dfd_file",
        help="Path to the DFD file (JSON or YAML format)."
    )
    parser.add_argument(
        "-o", "--output",
        help="Optional: Output file to save the suggested threats (JSON format). If not provided, prints to console."
    )

    args = parser.parse_args()

    print(f"Loading DFD from {args.dfd_file}...")
    dfd_data = load_dfd(args.dfd_file)

    print("Applying STRIDE methodology...")
    suggested_threats = apply_stride(dfd_data)

    if args.output:
        try:
            with open(args.output, 'w') as f:
                json.dump(suggested_threats, f, indent=2)
            print(f"Suggested threats saved to {args.output}")
        except IOError as e:
            print(f"Error writing to output file {args.output}: {e}")
            exit(1)
    else:
        print("\n--- Suggested STRIDE Threats ---")
        if not suggested_threats:
            print("No specific threats identified based on the DFD structure. Consider refining your DFD.")
        for component, stride_threats in suggested_threats.items():
            print(f"\nComponent/Flow: {component}")
            for stride_category, threat_list in stride_threats.items():
                print(f"  {stride_category}:")
                for threat in threat_list:
                    print(f"    - {threat}")

if __name__ == "__main__":
    main()
