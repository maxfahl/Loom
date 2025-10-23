#!/usr/bin/env python3
import os
import argparse
import textwrap
import re

# --- Color constants ---
class Color:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# --- Template for the new Custom Error Class ---
ERROR_CLASS_TEMPLATE = """
import { CustomError } from './custom-errors'; // Adjust the import path as needed

/**
 * {description}
 */
export class {class_name} extends CustomError {
  readonly status = {status_code};
  readonly type = '{type_uri}';
  readonly title = '{title}';

  constructor(detail?: string) {
    super(detail || '{title}');
  }
}
"""

# --- Template for the Markdown Documentation ---
DOCS_MD_TEMPLATE = """
# Error Type: {title}

- **Type URI**: `{type_uri}`
- **HTTP Status Code**: `{status_code}`
- **Title**: `{title}`

## Description

{description}

## When is this error returned?

This error is returned when [DESCRIBE TRIGGERING CONDITION HERE].

## How to resolve this error?

[DESCRIBE RESOLUTION STEPS HERE].

## Example Problem Details

```json
{{
  "type": "{type_uri}",
  "title": "{title}",
  "status": {status_code},
  "detail": "A specific, human-readable explanation of what went wrong.",
  "instance": "/path/to/the/resource/that/failed"
}}
```
"""

def to_pascal_case(text):
    """Converts a string to PascalCase."""
    return ''.join(word.capitalize() for word in re.split('[-_ ]', text))

def prompt_for_input(prompt_text, validation_regex=None, default=None):
    """Prompts the user for input and validates it."""
    while True:
        prompt_str = f"{Color.OKCYAN}{prompt_text}{Color.ENDC}"
        if default:
            prompt_str += f" (default: {default})"
        prompt_str += ": "
        
        value = input(prompt_str).strip()
        if not value and default:
            value = default

        if validation_regex and not re.match(validation_regex, value):
            print(f"{Color.FAIL}Invalid input. Please try again.{Color.ENDC}")
        else:
            return value

def main():
    parser = argparse.ArgumentParser(
        description=f"{Color.BOLD}Scaffold a new RFC 9457-compliant error type.{Color.ENDC}",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog=textwrap.dedent(f"""
        {Color.BOLD}Description:{Color.ENDC}
          This script interactively prompts for information about a new error type
          and generates two files:
          
          1.  A TypeScript class extending a `CustomError` base.
          2.  A Markdown file providing documentation for the new error type.

        {Color.BOLD}Usage Examples:{Color.ENDC}
          {Color.OKCYAN}# Run in interactive mode{Color.ENDC}
          python3 {__file__}

          {Color.OKCYAN}# Provide all arguments on the command line{Color.ENDC}
          python3 {__file__} --name \"Payment Required\" --status 402 --docs-dir docs/errors --out-dir src/errors
        """)
    )
    parser.add_argument("--name", help="The title of the error (e.g., 'Payment Required').")
    parser.add_argument("--status", type=int, help="The HTTP status code (e.g., 402).")
    parser.add_argument("--out-dir", default="./src/errors", help="Directory for the generated TypeScript file.")
    parser.add_argument("--docs-dir", default="./docs/errors", help="Directory for the generated Markdown file.")
    parser.add_argument("--dry-run", action="store_true", help="Print file contents instead of writing them.")

    args = parser.parse_args()

    print(f"{Color.HEADER}{Color.BOLD}Creating a New Error Type{Color.ENDC}")

    if args.name and args.status:
        title = args.name
        status_code = str(args.status)
    else:
        print("Running in interactive mode. Please provide the following details:")
        title = prompt_for_input("Enter the error title (e.g., Payment Required)", r".+")
        status_code = prompt_for_input("Enter the HTTP status code (e.g., 402)", r"^[45][0-9]{2}$")

    # Generate derived names
    type_name = title.lower().replace(' ', '-')
    class_name = to_pascal_case(type_name) + "Error"
    type_uri = f"/errors/{type_name}"
    ts_filename = f"{type_name}-error.ts"
    md_filename = f"{type_name}.md"
    description = f"Represents an HTTP {status_code} ({title}) error."

    # --- Generate TypeScript Class ---
    ts_content = textwrap.dedent(ERROR_CLASS_TEMPLATE.format(
        class_name=class_name,
        status_code=status_code,
        type_uri=type_uri,
        title=title,
        description=description
    )).strip()

    # --- Generate Markdown Docs ---
    md_content = textwrap.dedent(DOCS_MD_TEMPLATE.format(
        title=title,
        type_uri=type_uri,
        status_code=status_code,
        description=description
    )).strip()

    ts_path = os.path.join(args.out_dir, ts_filename)
    md_path = os.path.join(args.docs_dir, md_filename)

    print("\n" + "-"*20 + " Generated Files " + "-"*20)
    print(f"{Color.OKGREEN}TypeScript File:{Color.ENDC} {ts_path}")
    print(f"{Color.OKGREEN}Markdown File:{Color.ENDC}   {md_path}")
    print("-"*57 + "\n")

    if args.dry_run:
        print(f"{Color.WARNING}Dry run mode. Displaying file contents instead of writing.{Color.ENDC}")
        print(f"\n--- {ts_path} ---")
        print(ts_content)
        print(f"\n--- {md_path} ---")
        print(md_content)
    else:
        # Write TypeScript file
        os.makedirs(args.out_dir, exist_ok=True)
        with open(ts_path, 'w') as f:
            f.write(ts_content)
        print(f"✅ Successfully created {ts_path}")

        # Write Markdown file
        os.makedirs(args.docs_dir, exist_ok=True)
        with open(md_path, 'w') as f:
            f.write(md_content)
        print(f"✅ Successfully created {md_path}")

    print(f"\n{Color.OKGREEN}{Color.BOLD}Success!{Color.ENDC} Your new error type has been scaffolded.")
    print("Don't forget to add the new error to your main error module and update the documentation.")

if __name__ == "__main__":
    main()
