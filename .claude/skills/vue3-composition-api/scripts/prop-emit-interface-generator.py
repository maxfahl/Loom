#!/usr/bin/env python3

# prop-emit-interface-generator.py
# Description: Interactively prompts the user for prop names, types, and default values,
#              as well as emit event names and their payloads, then generates the
#              corresponding TypeScript interfaces for `defineProps` and `defineEmits`
#              within a Vue component.

import argparse
import sys

def generate_props_interface():
    props = []
    print("
--- Generate Props Interface ---")
    print("Enter prop details. Type 'done' when finished.")
    while True:
        prop_name = input("Prop Name (e.g., 'userId', 'isActive', 'item') [type 'done' to finish]: ").strip()
        if prop_name.lower() == 'done':
            break
        if not prop_name:
            print("Prop name cannot be empty. Please try again.")
            continue

        prop_type = input(f"Type for '{prop_name}' (e.g., 'string', 'number', 'boolean', 'User', 'string[]'): ").strip()
        if not prop_type:
            print("Prop type cannot be empty. Please try again.")
            continue

        is_optional = input(f"Is '{prop_name}' optional? (y/N): ").strip().lower() == 'y'
        default_value = input(f"Default value for '{prop_name}' (leave empty if none or handled by `withDefaults`): ").strip()

        props.append({
            'name': prop_name,
            'type': prop_type,
            'optional': is_optional,
            'default': default_value
        })
    return props

def generate_emits_interface():
    emits = []
    print("
--- Generate Emits Interface ---")
    print("Enter emit event details. Type 'done' when finished.")
    while True:
        emit_name = input("Emit Event Name (e.g., 'update:modelValue', 'submit', 'itemSelected') [type 'done' to finish]: ").strip()
        if emit_name.lower() == 'done':
            break
        if not emit_name:
            print("Emit name cannot be empty. Please try again.")
            continue

        payload_type = input(f"Payload type for '{emit_name}' (e.g., 'number', 'string', 'User', 'void', '[string, number]'): ").strip()
        if not payload_type:
            payload_type = 'void' # Default to void if no payload type is given

        emits.append({
            'name': emit_name,
            'payload_type': payload_type
        })
    return emits

def format_props_interface(props_data):
    if not props_data:
        return ""

    interface_lines = []
    with_defaults_lines = []

    interface_lines.append("interface Props {")
    for prop in props_data:
        optional_char = '?' if prop['optional'] else ''
        interface_lines.append(f"  {prop['name']}{optional_char}: {prop['type']};")
        if prop['default']:
            with_defaults_lines.append(f"  {prop['name']}: {prop['default']},")
    interface_lines.append("}")

    output = "
// Props Interface
" + "
".join(interface_lines) + "
const props = withDefaults(defineProps<Props>(), {")
    if with_defaults_lines:
        output += "
".join(with_defaults_lines) + "
});"
    else:
        output += "
});"

    return output

def format_emits_interface(emits_data):
    if not emits_data:
        return ""

    interface_lines = []
    interface_lines.append("interface Emits {")
    for emit in emits_data:
        payload = emit['payload_type']
        if payload == 'void':
            interface_lines.append(f"  (e: '{emit['name']}'): void;")
        else:
            interface_lines.append(f"  (e: '{emit['name']}', value: {payload}): void;")
    interface_lines.append("}")

    output = "
// Emits Interface
" + "
".join(interface_lines) + "
const emit = defineEmits<Emits>();"
    return output

def main():
    parser = argparse.ArgumentParser(
        description="Generate TypeScript interfaces for Vue 3 defineProps and defineEmits.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument('--props', action='store_true', help="Generate props interface.")
    parser.add_argument('--emits', action='store_true', help="Generate emits interface.")
    parser.add_argument('--all', action='store_true', help="Generate both props and emits interfaces (default if no option is given).")

    args = parser.parse_args()

    if not args.props and not args.emits:
        args.all = True

    generated_code = []

    if args.props or args.all:
        props_data = generate_props_interface()
        if props_data:
            generated_code.append(format_props_interface(props_data))

    if args.emits or args.all:
        emits_data = generate_emits_interface()
        if emits_data:
            generated_code.append(format_emits_interface(emits_data))

    if generated_code:
        print("
--- Generated Code ---")
        print("```typescript")
        print("

".join(generated_code))
        print("```")
        print("
Copy and paste this into your Vue 3 <script setup lang="ts"> block.")
    else:
        print("No interfaces generated.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("
Operation cancelled by user.")
        sys.exit(1)
