#!/bin/bash

# generate-custom-hook.sh
#
# Purpose: Automates the creation of a custom React Hook boilerplate, including a basic test file.
# This script helps developers quickly scaffold new custom hooks, ensuring a consistent structure
# and reducing repetitive setup tasks.
#
# Usage: ./generate-custom-hook.sh <HookName>
#   <HookName>: The name of the custom hook (e.g., useToggle, useLocalStorage).
#               The script will convert this to kebab-case for filenames and PascalCase for the hook function.
#
# Example:
#   ./generate-custom-hook.sh useMyFeature
#   This will create:
#     - src/hooks/useMyFeature/index.ts
#     - src/hooks/useMyFeature/useMyFeature.test.ts
#
# Configuration:
#   - HOOK_DIR: The base directory where custom hooks will be created. Defaults to 'src/hooks'.
#   - TEST_DIR: The base directory where hook tests will be created. Defaults to 'src/hooks'.
#
# Error Handling:
#   - Checks if a hook name is provided.
#   - Checks if the hook already exists to prevent accidental overwrites.
#   - Provides informative messages for success or failure.

# --- Configuration ---
HOOK_DIR="src/hooks"
TEST_DIR="src/hooks"
# --- End Configuration ---

# --- Utility Functions ---

# Function to convert PascalCase to kebab-case
pascal_to_kebab() {
  echo "$1" | sed -r 's/([A-Z])/-\L\1/g' | sed -r 's/^-//'
}

# Function to convert kebab-case to PascalCase
kebab_to_pascal() {
  echo "$1" | sed -r 's/(^|-)([a-z])/\U\2/g'
}

# --- Main Script Logic ---

# Check if hook name is provided
if [ -z "$1" ]; then
  echo "❌ Error: Please provide a name for your custom hook."
  echo "Usage: ./generate-custom-hook.sh <HookName>"
  exit 1
fi

HOOK_NAME_PASCAL=$(kebab_to_pascal "$1")
HOOK_NAME_KEBAB=$(pascal_to_kebab "$HOOK_NAME_PASCAL")

HOOK_PATH="$HOOK_DIR/$HOOK_NAME_KEBAB"
HOOK_FILE="$HOOK_PATH/index.ts"
TEST_FILE="$TEST_DIR/$HOOK_NAME_KEBAB/$HOOK_NAME_KEBAB.test.ts"

# Check if hook already exists
if [ -d "$HOOK_PATH" ]; then
  echo "⚠️ Warning: Custom hook '$HOOK_NAME_PASCAL' already exists at '$HOOK_PATH'."
  read -p "Do you want to overwrite it? (y/N): " OVERWRITE
  if [[ ! "$OVERWRITE" =~ ^[yY]$ ]]; then
    echo "Aborting hook generation."
    exit 0
  fi
  echo "Overwriting existing hook..."
fi

# Create directories
mkdir -p "$HOOK_PATH" || { echo "❌ Error: Failed to create directory '$HOOK_PATH'."; exit 1; }
mkdir -p "$(dirname "$TEST_FILE")" || { echo "❌ Error: Failed to create directory for test file."; exit 1; }

# Create hook file content
cat << EOF > "$HOOK_FILE"
import { useState, useEffect } from 'react';

/**
 * @function ${HOOK_NAME_PASCAL}
 * @description A custom React hook for managing a specific piece of stateful logic.
 * @param {any} initialValue - The initial value for the hook's internal state.
 * @returns {[any, (newValue: any) => void]} A tuple containing the current value and a setter function.
 * @example
 * const [value, setValue] = ${HOOK_NAME_PASCAL}(false);
 * // ...
 */
export function ${HOOK_NAME_PASCAL}<T>(initialValue: T): [T, (newValue: T) => void] {
  const [value, setValue] = useState<T>(initialValue);

  // Example of a side effect within the hook
  useEffect(() => {
    // Perform some side effect when value changes
    console.log('${HOOK_NAME_PASCAL} value changed:', value);
  }, [value]);

  return [value, setValue];
}
EOF

# Create test file content
cat << EOF > "$TEST_FILE"
import { renderHook, act } from '@testing-library/react-hooks';
import { ${HOOK_NAME_PASCAL} } from './index';

describe('${HOOK_NAME_PASCAL}', () => {
  it('should return the initial value', () => {
    const { result } = renderHook(() => ${HOOK_NAME_PASCAL}(false));
    expect(result.current[0]).toBe(false);
  });

  it('should update the value', () => {
    const { result } = renderHook(() => ${HOOK_NAME_PASCAL}(0));
    expect(result.current[0]).toBe(0);

    act(() => {
      result.current[1](1);
    });
    expect(result.current[0]).toBe(1);

    act(() => {
      result.current[1](prev => prev + 1);
    });
    expect(result.current[0]).toBe(2);
  });

  // Add more tests as needed for specific hook logic
});
EOF

echo "✅ Successfully created custom hook '$HOOK_NAME_PASCAL' at '$HOOK_FILE'."
echo "✅ Test file created at '$TEST_FILE'."
echo "To run tests, you might need to install '@testing-library/react-hooks' and 'react-test-renderer'."
echo "Example usage:"
echo "  const [myValue, setMyValue] = ${HOOK_NAME_PASCAL}(initialState);"
echo "  // ... use myValue and setMyValue"
