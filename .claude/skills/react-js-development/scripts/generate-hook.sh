#!/bin/bash

# generate-hook.sh
#
# Description:
#   Automates the creation of a new custom React Hook with TypeScript.
#   It generates the hook's .ts file with a basic structure (including generics
#   for flexibility) and a corresponding test file (.test.ts) using React Testing Library.
#
# Usage:
#   ./generate-hook.sh <HookName> [--path <path/to/hooks>]
#
# Examples:
#   ./generate-hook.sh useCounter
#   ./generate-hook.sh useLocalStorage --path src/utils/hooks
#
# Configuration:
#   None directly in script; uses command-line arguments.
#
# Error Handling:
#   Checks for hook name, valid path, and prevents overwriting existing files.
#
# Dry-run:
#   Not applicable for creation scripts.
#
# Colored Output:
#   Uses ANSI escape codes for better readability.

# --- Colors ---
GREEN="\033[0;32m"
YELLOW="\033[0;33m"
RED="\033[0;31m"
BLUE="\033[0;34m"
NC="\033[0m" # No Color

# --- Variables ---
HOOK_NAME=""
HOOK_PATH="src/hooks" # Default path

# --- Functions ---

show_help() {
  echo -e "${BLUE}Usage:${NC} ./generate-hook.sh <HookName> [--path <path/to/hooks>]"
  echo ""
  echo -e "${BLUE}Description:${NC}"
  echo "  Automates the creation of a new custom React Hook with TypeScript."
  echo "  It generates the hook's .ts file with a basic structure (including generics"
  echo "  for flexibility) and a corresponding test file (.test.ts) using React Testing Library."
  echo ""
  echo -e "${BLUE}Options:${NC}"
  echo "  <HookName>            The name of the custom React Hook (e.g., useCounter)."
  echo "  --path <path>         (Optional) Specify the directory where the hook files will be created."
  echo "                        Defaults to 'src/hooks'."
  echo "  -h, --help            Display this help message."
  echo ""
  echo -e "${BLUE}Examples:${NC}"
  echo "  ./generate-hook.sh useCounter"
  echo "  ./generate-hook.sh useLocalStorage --path src/utils/hooks"
  exit 0
}

# --- Parse Arguments ---
while [[ "$#" -gt 0 ]]; do
  case "$1" in
    --path)
      if [ -n "$2" ] && [[ "$2" != -* ]]; then
        HOOK_PATH="$2"
        shift 2
      else
        echo -e "${RED}Error:${NC} --path requires a directory argument." >&2
        exit 1
      fi
      ;;
    -h|--help)
      show_help
      ;;
    *)
      if [ -z "$HOOK_NAME" ]; then
        HOOK_NAME="$1"
        shift
      else
        echo -e "${RED}Error:${NC} Unknown argument: $1" >&2
        show_help
      fi
      ;;
  esac
done

# --- Validation ---
if [ -z "$HOOK_NAME" ]; then
  echo -e "${RED}Error:${NC} Hook name is required." >&2
  show_help
fi

# Ensure hook name starts with 'use'
if [[ ! "$HOOK_NAME" =~ ^use[A-Z] ]]; then
  echo -e "${RED}Warning:${NC} React Hooks should start with 'use'. Consider renaming '${HOOK_NAME}' to 'use${HOOK_NAME}'."
  # Optionally exit here if strict naming is desired
fi

# Convert hook name to PascalCase for directory and file names
PASCAL_CASE_NAME=$(echo "$HOOK_NAME" | sed -r 's/(^|-)([a-z])/\2/g')

TARGET_DIR="${HOOK_PATH}/${PASCAL_CASE_NAME}"

if [ -d "$TARGET_DIR" ]; then
  echo -e "${RED}Error:${NC} Directory '${TARGET_DIR}' already exists. Aborting to prevent overwrite." >&2
  exit 1
fi

# --- Create Directory ---
echo -e "${BLUE}Creating directory:${NC} ${TARGET_DIR}"
mkdir -p "$TARGET_DIR" || { echo -e "${RED}Error:${NC} Failed to create directory '${TARGET_DIR}'."; exit 1; }

# --- Create Hook File (.ts) ---
HOOK_FILE="${TARGET_DIR}/${HOOK_NAME}.ts"
echo -e "${BLUE}Creating hook file:${NC} ${HOOK_FILE}"
cat << EOF > "$HOOK_FILE"
import { useState, useEffect } from 'react';

/**
 * @template T The type of the value managed by the hook.
 * @param {T} initialValue The initial value for the hook.
 * @returns {[T, (value: T) => void]} A tuple containing the current value and a setter function.
 */
function ${HOOK_NAME}<T>(initialValue: T): [T, (value: T) => void] {
  const [value, setValue] = useState<T>(initialValue);

  // Example effect: log value changes
  useEffect(() => {
    console.log('${HOOK_NAME} value changed:', value);
  }, [value]);

  return [value, setValue];
}

export default ${HOOK_NAME};
EOF

# --- Create Test File (.test.ts) ---
TEST_FILE="${TARGET_DIR}/${HOOK_NAME}.test.ts"
echo -e "${BLUE}Creating test file:${NC} ${TEST_FILE}"
cat << EOF > "$TEST_FILE"
import { renderHook, act } from '@testing-library/react-hooks';
import ${HOOK_NAME} from './${HOOK_NAME}';

describe('${HOOK_NAME}', () => {
  it('should return the initial value', () => {
    const { result } = renderHook(() => ${HOOK_NAME}('initial'));
    expect(result.current[0]).toBe('initial');
  });

  it('should update the value', () => {
    const { result } = renderHook(() => ${HOOK_NAME}('initial'));

    act(() => {
      result.current[1]('updated');
    });

    expect(result.current[0]).toBe('updated');
  });

  it('should handle different types with generics', () => {
    const { result } = renderHook(() => ${HOOK_NAME}(0));
    expect(result.current[0]).toBe(0);

    act(() => {
      result.current[1](100);
    });
    expect(result.current[0]).toBe(100);
  });

  // Add more tests for specific hook logic and effects
});
EOF

echo -e "${GREEN}Successfully created ${HOOK_NAME} hook in ${TARGET_DIR}${NC}"
echo -e "${YELLOW}Remember to implement your hook's logic and add more comprehensive tests!${NC}"
