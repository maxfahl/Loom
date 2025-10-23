#!/usr/bin/env python3

"""
generate-svelte-component.py

Purpose:
  Generates boilerplate files for a new Svelte component, including:
  - A .svelte file (the component template and script)
  - A .ts file (for component-specific logic, if needed)
  - A .test.ts file (for unit tests using Vitest and Testing Library Svelte)

This script streamlines component creation, ensuring consistency and saving development time.

Usage:
  python3 generate-svelte-component.py <component_name> [--path <path/to/components>] [--no-logic] [--no-test]

Arguments:
  <component_name> : The name of the component (e.g., MyButton, UserProfileCard).
                     Will be converted to PascalCase for component name and kebab-case for filenames.
  --path           : (Optional) The directory where the component files should be created.
                     Defaults to 'src/lib/components'.
  --no-logic       : (Optional) Do not generate the separate .ts logic file.
  --no-test        : (Optional) Do not generate the .test.ts file.
  --help           : Show this help message and exit.

Examples:
  python3 generate-svelte-component.py MyButton
  python3 generate-svelte-component.py UserCard --path src/components/users
  python3 generate-svelte-component.py Icon --no-logic --no-test

Features:
  - Automatic PascalCase conversion for component names.
  - Automatic kebab-case conversion for filenames.
  - Generates .svelte, .ts, and .test.ts files with basic structure.
  - Customizable output path.
  - Options to skip logic or test file generation.
  - Includes basic error handling and verbose output.

Dependencies:
  - Python 3.x
"""

import argparse
import os
import re
import sys

def to_pascal_case(name):
    return ''.join(word.capitalize() for word in re.split(r'[-_]', name))

def to_kebab_case(name):
    name = re.sub(r'([a-z0-9]|(?=[A-Z]))([A-Z])', r'\1-\2', name).lower()
    return re.sub(r'[_-]+', '-', name).strip('-')

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
        description="Generate boilerplate for a new Svelte component.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "component_name",
        help="The name of the component (e.g., MyButton, UserProfileCard)."
    )
    parser.add_argument(
        "--path",
        default="src/lib/components",
        help="The directory where the component files should be created. Defaults to 'src/lib/components'."
    )
    parser.add_argument(
        "--no-logic",
        action="store_true",
        help="Do not generate the separate .ts logic file."
    )
    parser.add_argument(
        "--no-test",
        action="store_true",
        help="Do not generate the .test.ts file."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Perform a dry run without creating any files."
    )

    args = parser.parse_args()

    component_name_pascal = to_pascal_case(args.component_name)
    component_name_kebab = to_kebab_case(args.component_name)
    component_dir = os.path.join(args.path, component_name_kebab)

    print(f"Generating Svelte component: {component_name_pascal} in {component_dir}")

    # .svelte file content
    svelte_content = f"""
<script lang=\"ts\">
  // import type {{ SomeType }} from './{component_name_kebab}.ts'; // Uncomment if using separate logic file
  export let prop1: string = 'default';
  export let prop2: number = 0;

  // Reactive declarations
  $: doubledProp2 = prop2 * 2;
</script>

<div class=\"{component_name_kebab}\">
  <h1>{component_name_pascal}</h1>
  <p>Prop 1: {prop1}</p>
  <p>Prop 2: {prop2}</p>
  <p>Doubled Prop 2: {doubledProp2}</p>
  <slot></slot>
</div>

<style>
  .{component_name_kebab} {{
    /* Add component-specific styles here */
  }}
</style>
"""
    create_file(os.path.join(component_dir, f'{component_name_kebab}.svelte'), svelte_content, args.dry_run)

    # .ts logic file content
    if not args.no_logic:
        ts_content = f"""
// {component_name_kebab}.ts
// This file can contain component-specific types, interfaces, or utility functions.

export interface {component_name_pascal}Props {{
  prop1?: string;
  prop2?: number;
}}

export function someUtilityFunction(value: number): number {{
  return value * 10;
}}
"""
        create_file(os.path.join(component_dir, f'{component_name_kebab}.ts'), ts_content, args.dry_run)

    # .test.ts file content
    if not args.no_test:
        test_content = f"""
import {{ render, screen }} from '@testing-library/svelte';
import {{ describe, it, expect }} from 'vitest';
import {component_name_pascal} from './{component_name_kebab}.svelte';

describe('{component_name_pascal}', () => {{
  it('should render the component with default props', () => {{
    render({component_name_pascal});
    expect(screen.getByText('{component_name_pascal}')).toBeInTheDocument();
    expect(screen.getByText('Prop 1: default')).toBeInTheDocument();
    expect(screen.getByText('Prop 2: 0')).toBeInTheDocument();
    expect(screen.getByText('Doubled Prop 2: 0')).toBeInTheDocument();
  }});

  it('should render the component with custom props', () => {{
    render({component_name_pascal}, {{ prop1: 'custom', prop2: 5 }});
    expect(screen.getByText('Prop 1: custom')).toBeInTheDocument();
    expect(screen.getByText('Prop 2: 5')).toBeInTheDocument();
    expect(screen.getByText('Doubled Prop 2: 10')).toBeInTheDocument();
  }});

  // Add more tests here as needed
}});
"""
        create_file(os.path.join(component_dir, f'{component_name_kebab}.test.ts'), test_content, args.dry_run)

    print(f"\nComponent {component_name_pascal} boilerplate generation complete.")
    if args.dry_run:
        print("This was a DRY RUN. No files were actually created.")

if __name__ == "__main__":
    main()
