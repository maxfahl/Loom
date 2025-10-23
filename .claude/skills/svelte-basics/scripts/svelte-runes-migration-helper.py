#!/usr/bin/env python3

# svelte-runes-migration-helper.py
# Description: Analyzes a Svelte component (.svelte file) and provides suggestions
#              for migrating older reactive declarations (`$:`) to Svelte 5's 
#              "Runes" syntax (`$state`, `$derived`), aiding in the transition
#              to the new reactivity model.

import argparse
import re
import os

class SvelteRunesMigrationHelper:
    def __init__(self, file_path):
        self.file_path = file_path
        self.content = ""
        self.suggestions = []

    def read_file(self):
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"File not found: {self.file_path}")
        with open(self.file_path, 'r', encoding='utf-8') as f:
            self.content = f.read()

    def analyze_svelte_script(self):
        self.suggestions.append("--- Svelte 5 Runes Migration Suggestions ---")
        self.suggestions.append(f"Analyzing: {self.file_path}")
        self.suggestions.append("
")

        script_match = re.search(r'<script[^>]*lang="(ts|javascript)"[^>]*>(.*?)</script>', self.content, re.DOTALL | re.IGNORECASE)
        if not script_match:
            self.suggestions.append("No <script lang="ts"> or <script lang="javascript"> block found. Ensure it's a Svelte SFC with a script block.")
            return

        script_content = script_match.group(2)

        # Find reactive declarations ($: variable = expression)
        reactive_declarations = re.findall(r'^\s*\$:\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*(.*?);\s*$', script_content, re.MULTILINE)

        if not reactive_declarations:
            self.suggestions.append("No traditional reactive declarations (`$:`) found in the script.")
            self.suggestions.append("Consider using `$state()` for mutable state and `$derived()` for computed values in Svelte 5.")
            return

        self.suggestions.append("### Reactive Declarations (`$:`) -> Svelte 5 Runes (`$state`, `$derived`)")
        self.suggestions.append("
")
        self.suggestions.append("**Original Reactive Declarations:**")
        self.suggestions.append("```svelte")
        for var_name, expr in reactive_declarations:
            # Find the full line for better context
            full_line_match = re.search(f'^\s*\$:\s*{re.escape(var_name)}\s*=\s*{re.escape(expr)};\s*$', script_content, re.MULTILINE)
            if full_line_match:
                self.suggestions.append(full_line_match.group(0).strip())
        self.suggestions.append("```")
        self.suggestions.append("
")

        self.suggestions.append("**Suggestions for Svelte 5 Runes:**")
        self.suggestions.append("```typescript")
        self.suggestions.append("import { $state, $derived } from 'svelte/compiler'; // Or 'svelte' in future versions")
        self.suggestions.append("")

        for var_name, expr in reactive_declarations:
            # Simple heuristic: if the expression is a simple assignment or a function call, it might be $state.
            # If it clearly depends on other reactive variables, it's likely $derived.
            # This is a basic heuristic and might need manual adjustment.
            if re.search(r'\b(ref|reactive|computed|writable|readable|derived)\b', expr) or 
               re.search(r'\b(this\.)', expr) or 
               re.search(r'\b(get|set)\b', expr): # More complex logic often implies derived
                self.suggestions.append(f'let {var_name} = $derived(() => {expr});')
            else:
                # If it's a simple value or a direct computation, it could be $state or $derived depending on mutability
                # For simplicity, we'll suggest $derived for now if it's not a direct assignment of a literal/simple var
                # A more advanced tool would ask for user input or analyze usage for mutability.
                if re.match(r'^\s*(\".*\"|\".*\"|\d+|true|false|null|undefined|\w+)\s*$', expr): # Simple literal or variable
                    self.suggestions.append(f'let {var_name} = $state({expr}); // Consider if this should be $derived if it depends on other state')
                else:
                    self.suggestions.append(f'let {var_name} = $derived(() => {expr});')

        self.suggestions.append("```")
        self.suggestions.append("
Note: This is an automated suggestion. You may need to manually adjust `$state` vs `$derived` based on whether the variable is directly mutable or derived from other state.")
        self.suggestions.append("Also, ensure you import `$state` and `$derived` from the correct Svelte 5 module (e.g., `svelte/compiler` or `svelte`).")

    def print_suggestions(self):
        for suggestion in self.suggestions:
            print(suggestion)

def main():
    parser = argparse.ArgumentParser(
        description="Svelte Reactive Declarations (`$:`) to Svelte 5 Runes Migration Helper.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument('file', help="Path to the Svelte component (.svelte) file to analyze.")
    parser.add_argument('--dry-run', action='store_true',
                        help="Analyze and print suggestions without modifying any files (default behavior).")

    args = parser.parse_args()

    try:
        helper = SvelteRunesMigrationHelper(args.file)
        helper.read_file()
        helper.analyze_svelte_script()
        helper.print_suggestions()
    except FileNotFoundError as e:
        print(f"Error: {e}")
        exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        exit(1)

if __name__ == "__main__":
    main()
