#!/usr/bin/env python3

import re
import argparse
import os

def analyze_context_re_renders(file_path):
    """
    Analyzes a TypeScript/JavaScript file for `Context.Provider` usages and identifies
    potential re-render issues if the `value` prop is not memoized.

    This script uses heuristics and regular expressions, so it may not catch all edge cases
    and might produce false positives/negatives. For more robust analysis, a proper
    AST parser is recommended.

    Usage: python scripts/analyze-context-re-renders.py <filePath>
    """
    if not os.path.exists(file_path):
        print(f"❌ Error: File not found at '{file_path}'")
        return

    with open(file_path, 'r') as f:
        content = f.read()

    findings = []

    # Regex to find <SomeContext.Provider value={...}>
    # Group 1: Context Name (e.g., 'SomeContext')
    # Group 2: The content of the value prop (e.g., '{ count, setCount }', '{...}')
    provider_pattern = re.compile(
        r'<(\w+)\.Provider\s+value={([^}]+)}',
        re.DOTALL
    )

    for match in provider_pattern.finditer(content):
        context_name = match.group(1)
        value_content = match.group(2).strip()
        line_number = content.count('\n', 0, match.start()) + 1

        # Heuristic: Check if the value content looks like a direct object literal
        # without an obvious `useMemo` call wrapping it.
        # This is a very basic check. It will flag any object literal.
        # It won't detect if the object literal is inside a `useMemo` call.
        # A simple check for `useMemo` in the same line or nearby is possible but still heuristic.
        line_content = content.splitlines()[line_number - 1]
        if value_content.startswith('{') and value_content.endswith('}') and "useMemo" not in line_content:
            findings.append({
                'line': line_number,
                'context_name': context_name,
                'message': f"The `value` prop of `{context_name}.Provider` is a direct object literal and might not be memoized. This can cause unnecessary re-renders of consuming components. Consider wrapping the `value` in `useMemo`.",
                'code_snippet': line_content.strip()
            })

    if not findings:
        print(f"✅ No obvious `Context.Provider` re-render issues found in '{file_path}'.")
        return

    print(f"⚠️ Potential `Context.Provider` re-render issues found in '{file_path}':")
    for finding in findings:
        print(f"\n  Line {finding['line']}: Potential Re-render Issue in {finding['context_name']}.Provider")
        print(f"    Message: {finding['message']}")
        print(f"    Code: ```tsx\n{finding['code_snippet']}\n```")

def main():
    parser = argparse.ArgumentParser(
        description="Analyze Context.Provider usages for potential re-render issues."
    )
    parser.add_argument(
        "file_path",
        help="The path to the TypeScript/JavaScript file to analyze."
    )
    args = parser.parse_args()
    analyze_context_re_renders(args.file_path)

if __name__ == "__main__":
    main()
