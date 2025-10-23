import argparse
import re
import os
import sys

def to_camel_case(snake_str):
    components = snake_str.split('-')
    return components[0] + ''.join(x.title() for x in components[1:])

def to_pascal_case(snake_str):
    return ''.join(x.title() for x in snake_str.split('-'))

def extract_reducer_info(file_content):
    initial_state_match = re.search(r'const initialState = ({[^;]*});', file_content, re.DOTALL)
    if not initial_state_match:
        return None, None, None
    initial_state = initial_state_match.group(1).strip()

    reducer_name_match = re.search(r'const (\w+)Reducer = \(state = initialState, action\) => {', file_content)
    if not reducer_name_match:
        return None, None, None
    reducer_name = reducer_name_match.group(1)

    actions = []
    action_pattern = re.compile(r"case '([A-Z_]+)':\s*return {[^}]*};", re.DOTALL)
    for match in action_pattern.finditer(file_content):
        action_type = match.group(1)
        actions.append(action_type)

    return reducer_name, initial_state, actions

def generate_rtk_slice(slice_name, initial_state, actions):
    camel_slice_name = to_camel_case(slice_name)
    pascal_slice_name = to_pascal_case(slice_name)

    reducers_content = []
    for action_type in actions:
        method_name = to_camel_case(action_type.lower().replace(f'{slice_name.upper()}_', ''))
        reducers_content.append(f"    {method_name}: (state, action) => {{")
        reducers_content.append(f"      // TODO: Implement logic for {action_type}")
        reducers_content.append(f"    }},")

    reducers_str = "\n".join(reducers_content)
    action_exports = ', '.join([to_camel_case(a.lower().replace(f'{slice_name.upper()}_', '')) for a in actions])

    return f"""import {{ createSlice, PayloadAction }} from '@reduxjs/toolkit';

// Original initial state:
// {initial_state}

interface {pascal_slice_name}State {{}}
// TODO: Define your actual state interface based on the original initialState

const initialState: {pascal_slice_name}State = {initial_state};

export const {camel_slice_name}Slice = createSlice({{ 
  name: '{camel_slice_name}',
  initialState,
  reducers: {{
{reducers_str}
  }},
}});

export const {{ {action_exports} }} = {camel_slice_name}Slice.actions;

export default {camel_slice_name}Slice.reducer;
"""

def main():
    parser = argparse.ArgumentParser(
        description="Helps migrate a legacy Redux reducer to a Redux Toolkit createSlice format."
    )
    parser.add_argument(
        "input_file",
        help="Path to the legacy Redux reducer file (e.g., 'src/reducers/userReducer.js')."
    )
    parser.add_argument(
        "-s", "--slice-name",
        help="Desired name for the new Redux Toolkit slice (e.g., 'user', 'products')."
    )
    parser.add_argument(
        "-o", "--output-dir",
        default="src/features",
        help="Output directory for the generated slice file. Default is 'src/features'."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the generated slice content to console instead of saving to file."
    )

    args = parser.parse_args()

    if not os.path.exists(args.input_file):
        print(f"Error: Input file '{args.input_file}' not found.", file=sys.stderr)
        sys.exit(1)

    try:
        with open(args.input_file, 'r', encoding='utf-8') as f:
            file_content = f.read()
    except Exception as e:
        print(f"Error reading input file: {e}", file=sys.stderr)
        sys.exit(1)

    reducer_name, initial_state, actions = extract_reducer_info(file_content)

    if not reducer_name or not initial_state:
        print("Error: Could not extract reducer name or initial state from the input file.", file=sys.stderr)
        sys.exit(1)

    slice_name = args.slice_name if args.slice_name else reducer_name.replace('Reducer', '').lower()

    generated_slice_content = generate_rtk_slice(slice_name, initial_state, actions)

    if args.dry_run:
        print(generated_slice_content)
    else:
        output_dir = os.path.join(args.output_dir, slice_name)
        os.makedirs(output_dir, exist_ok=True)
        output_filepath = os.path.join(output_dir, f"{to_camel_case(slice_name)}Slice.ts")
        with open(output_filepath, 'w') as f:
            f.write(generated_slice_content)
        print(f"Successfully generated Redux Toolkit slice to: {output_filepath}")
        print("\nRemember to review the generated file, define the correct TypeScript interface for your state, and implement the reducer logic.")

if __name__ == "__main__":
    main()
