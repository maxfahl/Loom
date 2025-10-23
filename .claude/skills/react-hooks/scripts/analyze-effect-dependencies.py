#!/usr/bin/env python3

import re
import argparse
import os

def analyze_effect_dependencies(file_path):
    """
    Analyzes a TypeScript/JavaScript file for useEffect calls and provides suggestions
    for potential dependency array issues.

    This script uses heuristics and regular expressions, so it may not catch all edge cases
    and might produce false positives/negatives. For more robust analysis, a proper
    AST parser (e.g., using TypeScript's compiler API or Babel) is recommended.
    """
    if not os.path.exists(file_path):
        print(f"❌ Error: File not found at '{file_path}'")
        return

    with open(file_path, 'r') as f:
        content = f.read()

    findings = []

    # Pattern 1: useEffect without a dependency array (infinite loop risk)
    # This pattern looks for `useEffect(` followed by a function and then immediately `);`
    # It's a heuristic and might have false positives if the function itself contains `);`
    no_deps_pattern = re.compile(r'useEffect\(\s*\([^)]*\)\s*=>\s*{[^}]*}\s*\);', re.DOTALL)
    for match in no_deps_pattern.finditer(content):
        line_number = content.count('\n', 0, match.start()) + 1
        findings.append({
            'line': line_number,
            'type': 'Missing Dependency Array',
            'message': "useEffect without a dependency array will run on every render. Consider adding an empty array `[]` for componentDidMount-like behavior, or specify dependencies.",
            'code_snippet': match.group(0).strip()
        })

    # Pattern 2: useEffect with an empty dependency array, but potentially using external variables
    # This is a common source of stale closures.
    empty_deps_pattern = re.compile(r'useEffect\(\s*\([^)]*\)\s*=>\s*{([^}]*)}\s*,\s*\[\s*\]\s*\)', re.DOTALL)
    for match in empty_deps_pattern.finditer(content):
        effect_body = match.group(1)
        line_number = content.count('\n', 0, match.start()) + 1

        # Heuristic: Look for common state setters or props access within the effect body
        # This is a very basic check and will have false positives.
        # It looks for words that are typically props, state variables, or functions
        # that would come from the outer scope.
        if re.search(r'\b(set[A-Z][a-zA-Z0-9]*)\(|props\.[a-zA-Z0-9]+|state\.[a-zA-Z0-9]+', effect_body):
            findings.append({
                'line': line_number,
                'type': 'Potential Stale Closure / Missing Dependency',
                'message': "useEffect with an empty dependency array might be using external variables (e.g., state setters, props, state). Consider adding these to the dependency array or using functional updates for state setters.",
                'code_snippet': match.group(0).strip()
            })

    if not findings:
        print(f"✅ No obvious useEffect dependency issues found in '{file_path}'.")
    else:
        print(f"⚠️ Potential useEffect dependency issues found in '{file_path}':")
        for finding in findings:
            print(f"\n  Line {finding['line']}: {finding['type']}")
            print(f"    Message: {finding['message']}")
            print(f"    Code: ```typescript\n{finding['code_snippet']}\n```")

def main():
    parser = argparse.ArgumentParser(
        description="Analyze useEffect dependencies in a TypeScript/JavaScript file."
    )
    parser.add_argument(
        "file_path",
        help="The path to the TypeScript/JavaScript file to analyze."
    )
    args = parser.parse_args()
    analyze_effect_dependencies(args.file_path)

if __name__ == "__main__":
    main()
