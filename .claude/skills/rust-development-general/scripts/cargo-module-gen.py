#!/usr/bin/env python3
# cargo-module-gen.py
#
# Description:
#   Generates a new Rust module with a specified name, creating the necessary
#   file structure (`mod.rs` or `module_name.rs`) and a basic test boilerplate.
#
# Usage:
#   python3 cargo-module-gen.py <module_name> [--path <relative_path>] [--lib]
#
# Arguments:
#   <module_name>   The name of the new module (e.g., `my_feature`).
#   --path <path>   (Optional) Relative path to the directory where the module
#                   should be created (e.g., `src/utils`). Defaults to `src/`.
#   --lib           (Optional) Create a `mod.rs` inside a new directory for
#                   a library-style module. Otherwise, creates `module_name.rs`.
#   --dry-run       (Optional) Show what would be done without actually creating files.
#
# Examples:
#   python3 cargo-module-gen.py network
#   python3 cargo-module-gen.py database --path src/data
#   python3 cargo-module-gen.py models --lib --path src
#
# Error Handling:
#   - Exits if module name is not provided.
#   - Exits if the target directory already contains a module with the same name.
#   - Provides informative messages for each step.

import argparse
import os
import sys

def create_module(module_name, base_path, is_lib_style, dry_run):
    target_dir = os.path.join(base_path, module_name) if is_lib_style else base_path
    module_file_name = "mod.rs" if is_lib_style else f"{module_name}.rs"
    module_file_path = os.path.join(target_dir, module_file_name)

    if not dry_run:
        os.makedirs(target_dir, exist_ok=True)

    if os.path.exists(module_file_path) and not dry_run:
        print(f"Error: Module file already exists at {module_file_path}", file=sys.stderr)
        sys.exit(1)

    content = f"""// {module_file_name}

pub fn {module_name}_function() {{
    println!("Hello from {module_name}!");
}}

#[cfg(test)]
mod tests {{
    use super::*;

    #[test]
    fn test_{module_name}_function() {{
        // Add your test logic here
        assert_eq!(2 + 2, 4);
    }}
}}
"""

    if dry_run:
        print(f"Would create directory: {target_dir}")
        print(f"Would create file: {module_file_path}")
        print("--- Content ---")
        print(content)
        print("---------------")
    else:
        with open(module_file_path, "w") as f:
            f.write(content)
        print(f"✅ Module '{module_name}' created at {module_file_path}")

    # Add `mod module_name;` to the parent module's mod.rs or lib.rs/main.rs
    parent_mod_file = os.path.join(base_path, "mod.rs")
    if not os.path.exists(parent_mod_file):
        parent_mod_file = os.path.join(base_path, "lib.rs")
    if not os.path.exists(parent_mod_file):
        parent_mod_file = os.path.join(base_path, "main.rs")

    if os.path.exists(parent_mod_file):
        mod_declaration = f"pub mod {module_name};"
        if dry_run:
            print(f"Would add '{{mod_declaration}}' to {parent_mod_file}")
        else:
            with open(parent_mod_file, "a") as f:
                f.write(f"\n{mod_declaration}\n")
            print(f"✅ Added '{{mod_declaration}}' to {parent_mod_file}")
    else:
        print(f"Warning: Could not find a parent mod.rs, lib.rs, or main.rs in {base_path} to declare the new module.")

def main():
    parser = argparse.ArgumentParser(
        description="Generates a new Rust module with boilerplate."
    )
    parser.add_argument("module_name", help="The name of the new module.")
    parser.add_argument(
        "--path",
        default="src",
        help="Relative path to the directory where the module should be created. Defaults to 'src/'.",
    )
    parser.add_argument(
        "--lib",
        action="store_true",
        help="Create a 'mod.rs' inside a new directory for a library-style module. Otherwise, creates 'module_name.rs'.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without actually creating files.",
    )

    args = parser.parse_args()

    if not args.module_name:
        parser.print_help()
        sys.exit(1)

    create_module(args.module_name, args.path, args.lib, args.dry_run)

if __name__ == "__main__":
    main()
