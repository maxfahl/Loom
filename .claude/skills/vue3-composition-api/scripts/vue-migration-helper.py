#!/usr/bin/env python3

# vue-migration-helper.py
# Description: Analyzes a Vue Options API component (.vue file) and provides suggestions
#              for migrating 'data', 'methods', 'computed', and 'watch' options to their
#              Composition API equivalents. It acts as a guide rather than a full automation.

import argparse
import re
import os

class VueMigrationHelper:
    def __init__(self, file_path):
        self.file_path = file_path
        self.content = ""
        self.suggestions = []

    def read_file(self):
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"File not found: {self.file_path}")
        with open(self.file_path, 'r', encoding='utf-8') as f:
            self.content = f.read()

    def analyze_options_api(self):
        self.suggestions.append("--- Migration Suggestions for Composition API ---")
        self.suggestions.append(f"Analyzing: {self.file_path}")
        self.suggestions.append("
")

        # Extract <script> block
        script_match = re.search(r'<script[^>]*>(.*?)</script>', self.content, re.DOTALL)
        if not script_match:
            self.suggestions.append("No <script> block found. Ensure it's a Vue SFC.")
            return

        script_content = script_match.group(1)

        # 1. Data Option
        data_match = re.search(r'data\s*\(\s*\)\s*\{\s*return\s*\{([^}]*)\}
		', script_content, re.DOTALL)
        if data_match:
            data_props = data_match.group(1).strip().split(',\n')
            self.suggestions.append("### Data Option (Options API) -> Reactive State (Composition API)")
            self.suggestions.append("
")
            self.suggestions.append("**Original `data()`:**")
            self.suggestions.append(f"```javascript
{data_match.group(0)}
```")
            self.suggestions.append("
")
            self.suggestions.append("**Suggestion:** Convert each data property to `ref` or `reactive` in `<script setup>`:")
            self.suggestions.append("```typescript
<script setup lang=\"ts\">
import { ref, reactive } from 'vue';
")
            for prop_line in data_props:
                if prop_line.strip():
                    key_value = prop_line.split(':', 1)
                    if len(key_value) == 2:
                        key = key_value[0].strip()
                        value = key_value[1].strip()
                        if value.startswith('{') or value.startswith('['):
                            self.suggestions.append(f"const {key} = reactive({value});")
                        else:
                            self.suggestions.append(f"const {key} = ref({value});")
            self.suggestions.append("
// ... rest of your script
</script>
```")
            self.suggestions.append("
")

        # 2. Methods Option
        methods_match = re.search(r'methods\s*:\s*\{([^}]*)\}', script_content, re.DOTALL)
        if methods_match:
            method_defs = methods_match.group(1).strip().split(',\n')
            self.suggestions.append("### Methods Option (Options API) -> Functions (Composition API)")
            self.suggestions.append("
")
            self.suggestions.append("**Original `methods`:**")
            self.suggestions.append(f"```javascript
{methods_match.group(0)}
```")
            self.suggestions.append("
")
            self.suggestions.append("**Suggestion:** Convert each method to a regular function in `<script setup>`:")
            self.suggestions.append("```typescript
<script setup lang=\"ts\">
")
            for method_line in method_defs:
                if method_line.strip():
                    # Simple regex to extract method name and body
                    method_name_match = re.match(r'^\s*(\w+)\s*\(.*\)\s*\{\s*.*\s*\}', method_line, re.DOTALL)
                    if method_name_match:
                        method_name = method_name_match.group(1)
                        # Attempt to get the full method body, might be imperfect for complex cases
                        method_body = method_line.strip()
                        self.suggestions.append(f"const {method_name} = () => {{ /* ... logic ... */ }};")
            self.suggestions.append("
// ... rest of your script
</script>
```")
            self.suggestions.append("
")

        # 3. Computed Option
        computed_match = re.search(r'computed\s*:\s*\{([^}]*)\}', script_content, re.DOTALL)
        if computed_match:
            computed_defs = computed_match.group(1).strip().split(',\n')
            self.suggestions.append("### Computed Option (Options API) -> `computed` (Composition API)")
            self.suggestions.append("
")
            self.suggestions.append("**Original `computed`:**")
            self.suggestions.append(f"```javascript
{computed_match.group(0)}
```")
            self.suggestions.append("
")
            self.suggestions.append("**Suggestion:** Convert each computed property to `computed` in `<script setup>`:")
            self.suggestions.append("```typescript
<script setup lang=\"ts\">
import { computed } from 'vue';
")
            for computed_line in computed_defs:
                if computed_line.strip():
                    key_value = computed_line.split(':', 1)
                    if len(key_value) == 2:
                        key = key_value[0].strip()
                        # Assuming simple getter for now
                        self.suggestions.append(f"const {key} = computed(() => {{ /* ... logic ... */ }});")
            self.suggestions.append("
// ... rest of your script
</script>
```")
            self.suggestions.append("
")

        # 4. Watch Option
        watch_match = re.search(r'watch\s*:\s*\{([^}]*)\}', script_content, re.DOTALL)
        if watch_match:
            watch_defs = watch_match.group(1).strip().split(',\n')
            self.suggestions.append("### Watch Option (Options API) -> `watch` (Composition API)")
            self.suggestions.append("
")
            self.suggestions.append("**Original `watch`:**")
            self.suggestions.append(f"```javascript
{watch_match.group(0)}
```")
            self.suggestions.append("
")
            self.suggestions.append("**Suggestion:** Convert each watch property to `watch` in `<script setup>`:")
            self.suggestions.append("```typescript
<script setup lang=\"ts\">
import { watch } from 'vue';
")
            for watch_line in watch_defs:
                if watch_line.strip():
                    key_value = watch_line.split(':', 1)
                    if len(key_value) == 2:
                        key = key_value[0].strip()
                        # Assuming simple handler for now
                        self.suggestions.append(f"watch(() => {key}, (newValue, oldValue) => {{ /* ... logic ... */ }});")
            self.suggestions.append("
// ... rest of your script
</script>
```")
            self.suggestions.append("
")

        if not (data_match or methods_match or computed_match or watch_match):
            self.suggestions.append("No `data`, `methods`, `computed`, or `watch` options found in the script.")

    def print_suggestions(self):
        for suggestion in self.suggestions:
            print(suggestion)

def main():
    parser = argparse.ArgumentParser(
        description="Vue Options API to Composition API Migration Helper.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument('file', help="Path to the Vue SFC (.vue) file to analyze.")
    parser.add_argument('--dry-run', action='store_true',
                        help="Analyze and print suggestions without modifying any files (default behavior).")

    args = parser.parse_args()

    try:
        helper = VueMigrationHelper(args.file)
        helper.read_file()
        helper.analyze_options_api()
        helper.print_suggestions()
    except FileNotFoundError as e:
        print(f"Error: {e}")
        exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        exit(1)

if __name__ == "__main__":
    main()
