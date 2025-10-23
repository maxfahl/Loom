#!/usr/bin/env python3

import re
import argparse
import os

def analyze_component_type(file_path):
    """
    Analyzes a TypeScript/JavaScript file and suggests whether it should be a Server or Client Component
    based on the presence of `useState`, `useEffect`, browser APIs, or `async` functions/`fetch` calls.

    This script uses heuristics and regular expressions, so it may not catch all edge cases
    and might produce false positives/negatives. For more robust analysis, a proper
    AST parser is recommended.

    Usage: python scripts/analyze-component-type.py <filePath>
    """
    if not os.path.exists(file_path):
        print(f"❌ Error: File not found at '{file_path}'")
        return

    with open(file_path, 'r') as f:
        content = f.read()

    is_client_component_directive = re.search(r'^"use client";', content, re.MULTILINE)
    
    # Heuristics for Client Component indicators
    uses_useState = re.search(r'useState\(', content) or re.search(r'import\s*{[^}]*useState[^}]*}\s*from\s*["|"]react["|"]', content)
    uses_useEffect = re.search(r'useEffect\(', content) or re.search(r'import\s*{[^}]*useEffect[^}]*}\s*from\s*["|"]react["|"]', content)
    uses_browser_api = re.search(r'\b(window|document|localStorage|sessionStorage)\b', content)

    # Heuristics for Server Component indicators
    is_async_component = re.search(r'export\s+default\s+async\s+function\s+\w+\(', content)
    uses_fetch_in_component = re.search(r'fetch\(', content) and not is_client_component_directive # fetch can be used in client components too, but if it's in a server component, it's a strong indicator

    suggestions = []

    if is_client_component_directive:
        suggestions.append("This is explicitly marked as a Client Component with '"use client"'.")
    else:
        if uses_useState or uses_useEffect or uses_browser_api:
            suggestions.append("This component appears to use React Hooks (useState, useEffect) or browser-specific APIs (window, document). It should likely be a **Client Component** (add '"use client"' at the top of the file).")
        elif is_async_component or uses_fetch_in_component:
            suggestions.append("This component appears to be an `async` function or uses `fetch` directly. It should likely be a **Server Component** (no '"use client"' directive needed).")
        else:
            suggestions.append("This component does not show obvious signs of being a Client or Server Component. By default, it will be treated as a **Server Component**.")

    print(f"--- Component Type Analysis for '{file_path}' ---")
    for suggestion in suggestions:
        print(f"  - {suggestion}")
    print("--------------------------------------------------")

def main():
    parser = argparse.ArgumentParser(
        description="Analyzes a component file to suggest if it should be a Server or Client Component in Next.js App Router."
    )
    parser.add_argument(
        "file_path",
        help="The path to the TypeScript/JavaScript component file to analyze."
    )
    args = parser.parse_args()
    analyze_component_type(args.file_path)

if __name__ == "__main__":
    main()
