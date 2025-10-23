#!/usr/bin/env python3

"""
generate-svelte-store.py

Purpose:
  Generates boilerplate for a new Svelte store (writable, readable, or derived)
  with TypeScript, based on user-provided details.

This script helps in quickly setting up consistent and type-safe Svelte stores.

Usage:
  python3 generate-svelte-store.py <store_name> <store_type> [--initial_value <value>] [--path <path/to/stores>]

Arguments:
  <store_name>    : The name of the store (e.g., counter, authStatus).
                    Will be converted to kebab-case for filename and camelCase for variable.
  <store_type>    : The type of store to generate (writable, readable, derived).
  --initial_value : (Optional) The initial value for writable/readable stores.
                    Defaults to a sensible empty value based on type (e.g., 0, '', []).
  --path          : (Optional) The directory where the store file should be created.
                    Defaults to 'src/lib/stores'.
  --help          : Show this help message and exit.

Examples:
  python3 generate-svelte-store.py counter writable --initial_value 0
  python3 generate-svelte-store.py user readable --initial_value "{ name: 'Guest' }" --path src/stores
  python3 generate-svelte-store.py doubledCounter derived

Features:
  - Generates writable, readable, or derived Svelte stores.
  - Automatic naming conventions (kebab-case for file, camelCase for variable).
  - Customizable initial value for writable/readable stores.
  - Customizable output path.
  - Includes basic error handling and verbose output.
  - Provides type hints for TypeScript.

Dependencies:
  - Python 3.x
"""

import argparse
import os
import re
import sys

def to_camel_case(name):
    s = re.sub(r'(_|-)+', ' ', name).title().replace(' ', '')
    return s[0].lower() + s[1:] if s else ''

def to_kebab_case(name):
    name = re.sub(r'([a-z0-9]|(?=[A-Z]))([A-Z])', r'\1-\2', name).lower()
    return re.sub(r'[_-]+', '-', name).strip('-')

def get_default_initial_value(store_name):
    if "count" in store_name.lower():
        return "0"
    elif "is" in store_name.lower() or "has" in store_name.lower():
        return "false"
    elif "list" in store_name.lower() or "array" in store_name.lower():
        return "[]"
    elif "object" in store_name.lower() or "data" in store_name.lower():
        return "{}"
    return "''"

def create_file(filepath, content, dry_run=False):
    if dry_run:
        print(f"[DRY RUN] Would create file: {filepath}")
        return
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Created: {filepath}")
    except IOError as e:
        print(f"Error creating file {filepath}: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description="Generate boilerplate for a new Svelte store.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "store_name",
        help="The name of the store (e.g., counter, authStatus)."
    )
    parser.add_argument(
        "store_type",
        choices=["writable", "readable", "derived"],
        help="The type of store to generate (writable, readable, derived)."
    )
    parser.add_argument(
        "--initial_value",
        help="The initial value for writable/readable stores. Defaults to a sensible empty value."
    )
    parser.add_argument(
        "--path",
        default="src/lib/stores",
        help="The directory where the store file should be created. Defaults to 'src/lib/stores'."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Perform a dry run without creating any files."
    )

    args = parser.parse_args()

    store_name_camel = to_camel_case(args.store_name)
    store_name_kebab = to_kebab_case(args.store_name)
    store_filepath = os.path.join(args.path, f'{store_name_kebab}.ts')

    print(f"Generating Svelte {args.store_type} store: {store_name_camel} in {store_filepath}")

    store_content = ""
    if args.store_type == "writable":
        initial_value = args.initial_value if args.initial_value is not None else get_default_initial_value(args.store_name)
        store_content = f"""
import {{ writable }} from 'svelte/store';

# Define the type for the store's value
type {store_name_camel.capitalize()}Store = any; // TODO: Replace 'any' with actual type

export const {store_name_camel} = writable<{store_name_camel.capitalize()}Store>({initial_value});

# Example of how to update the store:
# {store_name_camel}.set(newValue);
# {store_name_camel}.update(currentValue => {{ /* ... */ return newValue; }});
"""
    elif args.store_type == "readable":
        initial_value = args.initial_value if args.initial_value is not None else get_default_initial_value(args.store_name)
        store_content = f"""
import {{ readable }} from 'svelte/store';

# Define the type for the store's value
type {store_name_camel.capitalize()}Store = any; // TODO: Replace 'any' with actual type

export const {store_name_camel} = readable<{store_name_camel.capitalize()}Store>({initial_value}, (set) => {{
  # This function runs when the first subscriber subscribes.
  # Use 'set' to update the store's value.
  # Example: set(someInitialValue);

  # Return a cleanup function that runs when the last subscriber unsubscribes.
  return () => {{}};
});
"""
    elif args.store_type == "derived":
        store_content = f"""
import {{ derived }} from 'svelte/store';
# import {{ someOtherStore }} from './some-other-store'; // Example: import a store to derive from

# Define the type for the derived store's value
type {store_name_camel.capitalize()}Store = any; // TODO: Replace 'any' with actual type

# Example: Derive from an existing store
# export const {store_name_camel} = derived(someOtherStore, ($someOtherStore) => {{
#   return $someOtherStore.value * 2; // Example derivation logic
# }});

# Placeholder derived store
export const {store_name_camel} = derived(null, (set) => {{
  set('Derived value placeholder'); // TODO: Implement actual derivation logic
}}); // TODO: Replace null with actual dependency store(s)
"""

    create_file(store_filepath, store_content, args.dry_run)

    print(f"\nStore {store_name_camel} boilerplate generation complete.")
    if args.dry_run:
        print("This was a DRY RUN. No files were actually created.")

if __name__ == "__main__":
    main()
