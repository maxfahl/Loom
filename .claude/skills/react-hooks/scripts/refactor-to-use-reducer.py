#!/usr/bin/env python3

import re
import argparse
import os

def refactor_to_use_reducer(file_path, component_name):
    """
    Helps refactor a React component that uses multiple `useState` calls into a single `useReducer` call.
    This script acts as a guide and generates boilerplate for the reducer and initial state.
    Full automation of this refactoring is complex and typically requires an AST parser.

    Usage: python scripts/refactor-to-use-reducer.py <filePath> <componentName>
    """
    if not os.path.exists(file_path):
        print(f"❌ Error: File not found at '{file_path}'")
        return

    with open(file_path, 'r') as f:
        content = f.read()

    # Regex to find useState calls: const [value, setValue] = useState(initialValue);
    # Captures:
    # 1: state variable name (e.g., 'value')
    # 2: setter function name (e.g., 'setValue')
    # 3: initial value (e.g., 'false', '0', '{ name: "" }')
    useState_pattern = re.compile(r'const\s*\[(\w+),\s*(\w+)]\s*=\s*useState\((.*?)\);')

    state_variables = []
    for match in useState_pattern.finditer(content):
        state_variables.append({
            'name': match.group(1),
            'setter': match.group(2),
            'initial_value': match.group(3)
        })

    if not state_variables:
        print(f"✅ No useState calls found in '{file_path}'. No refactoring needed for useReducer.")
        return

    print(f"✨ Found {len(state_variables)} useState calls in '{file_path}'.")
    print("Generating useReducer boilerplate and refactoring instructions...\n")

    # Generate initial state
    initial_state_lines = []
    for var in state_variables:
        initial_state_lines.append(f"  {var['name']}: {var['initial_value']},")
    initial_state_str = "{\n" + "\n".join(initial_state_lines) + "\n}"

    # Generate reducer function
    reducer_cases = []
    for var in state_variables:
        # Suggest a generic SET_VAR action type
        action_type = f"SET_{var['name'].upper()}"
        reducer_cases.append(f"    case '{action_type}':
      return {{ ...state, {var['name']}: action.payload }};")
    reducer_str = f"function {component_name}Reducer(state, action) {{
  switch (action.type) {{
{'\n'.join(reducer_cases)}}
    default:
      return state;
  }}
}}"

    print("--- Suggested Initial State ---")
    print(f"const initialState = {initial_state_str}\n")

    print("--- Suggested Reducer Function ---")
    print(reducer_str + "\n")

    print("--- Refactoring Steps ---")
    print("1.  **Replace `useState` calls with `useReducer`:**")
    print(f"    Replace all `const [{state_variables[0]['name']}, {state_variables[0]['setter']}] = useState(...)` (and other useState calls) with:")
    print(f"    `const [state, dispatch] = useReducer({component_name}Reducer, initialState);`")
    print("2.  **Update state access:**")
    print(f"    Change `{state_variables[0]['name']}` to `state.{state_variables[0]['name']}`.")
    print("3.  **Update state setters to dispatch calls:**")
    for var in state_variables:
        action_type = f"SET_{var['name'].upper()}"
        print(f"    Change `{var['setter']}(newValue)` to `dispatch({{ type: '{action_type}', payload: newValue }});`")
        print(f"    Change `{var['setter']}(prevValue => ...)` to `dispatch({{ type: '{action_type}', payload: prevValue => ... }});`")
    print("4.  **Add the `initialState` and `{component_name}Reducer` function to your file (or a separate file).**")
    print("5.  **Import `useReducer` from 'react'.**")
    print("6.  **Review and adjust the reducer logic and action types as needed for complex state transitions.**")
    print("7.  **Run your tests to ensure everything is working correctly.**")

def main():
    parser = argparse.ArgumentParser(
        description="Helps refactor a React component from useState to useReducer."
    )
    parser.add_argument(
        "file_path",
        help="The path to the TypeScript/JavaScript file to refactor."
    )
    parser.add_argument(
        "component_name",
        help="The name of the component (e.g., MyForm) to use for the reducer function name."
    )
    args = parser.parse_args()
    refactor_to_use_reducer(args.file_path, args.component_name)

if __name__ == "__main__":
    main()
