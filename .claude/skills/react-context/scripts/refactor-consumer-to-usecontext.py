#!/usr/bin/env python3

import re
import argparse
import os

def refactor_consumer_to_usecontext(file_path):
    """
    Helps refactor React components from using `Context.Consumer` to the `useContext` hook.
    This script acts as a guide and provides instructions for manual conversion.
    Automated refactoring of this nature is complex and typically requires an AST parser.

    Usage: python scripts/refactor-consumer-to-usecontext.py <filePath>
    """
    if not os.path.exists(file_path):
        print(f"❌ Error: File not found at '{file_path}'")
        return

    with open(file_path, 'r') as f:
        content = f.read()

    findings = []

    # Regex to find <Context.Consumer>...</Context.Consumer> blocks
    # This pattern is simplified and might not catch all variations or nested consumers.
    # It looks for: <SomeContext.Consumer>{(value) => { ... }}</SomeContext.Consumer>
    # Group 1: Context Name (e.g., 'SomeContext')
    # Group 2: Value variable name (e.g., 'value')
    # Group 3: Content inside the consumer's render prop function
    consumer_pattern = re.compile(
        r'<(\w+)\.Consumer>\s*{\s*\((\w+)\)\s*=>\s*{([^}]*)}\s*}</\1\.Consumer>',
        re.DOTALL
    )

    for match in consumer_pattern.finditer(content):
        context_name = match.group(1)
        value_var = match.group(2)
        consumer_body = match.group(3)
        line_number = content.count('\n', 0, match.start()) + 1

        findings.append({
            'line': line_number,
            'context_name': context_name,
            'value_var': value_var,
            'consumer_body': consumer_body.strip(),
            'code_snippet': match.group(0).strip()
        })

    if not findings:
        print(f"✅ No `Context.Consumer` usage found in '{file_path}'.")
        return

    print(f"✨ Found {len(findings)} `Context.Consumer` usages in '{file_path}'.")
    print("Generating refactoring instructions to use `useContext`...\n")

    for i, finding in enumerate(findings):
        print(f"--- Refactoring Instruction {i+1} (Line {finding['line']}) ---")
        print(f"**Original Code:**")
        print(f"```tsx\n{finding['code_snippet']}\n```")
        print("\n**Refactoring Steps:**")
        print(f"1.  **Remove the `<{finding['context_name']}.Consumer>` and `</{finding['context_name']}.Consumer>` tags.")
        print(f"2.  **Inside the functional component where this consumer was used, add the `useContext` hook:**")
        print(f"    `const {finding['value_var']} = useContext({finding['context_name']});`")
        print(f"3.  **Ensure `{finding['context_name']}` is imported from its source.**")
        print(f"4.  **Ensure `useContext` is imported from 'react'.**")
        print(f"5.  **The content of the consumer's render prop (`{finding['value_var']}`) can now be used directly in the component's JSX.**")
        print("\n**Example of Refactored Code:**")
        print(f"```tsx")
        print(f"import React, {{ useContext }} from 'react';")
        print(f"import {finding['context_name']} from '...'; // Adjust import path")
        print(f"\nconst MyComponent: React.FC = () => {{")
        print(f"  const {finding['value_var']} = useContext({finding['context_name']});")
        print(f"  // ... other component logic")
        print(f"  return (\n{finding['consumer_body'].replace(/^/gm, '    ')}\n  );")
        print(f"}};\n```")
        print("\n--------------------------------------------------\n")

def main():
    parser = argparse.ArgumentParser(
        description="Helps refactor React components from Context.Consumer to useContext hook."
    )
    parser.add_argument(
        "file_path",
        help="The path to the TypeScript/JavaScript file to analyze and refactor."
    )
    args = parser.parse_args()
    refactor_consumer_to_usecontext(args.file_path)

if __name__ == "__main__":
    main()
