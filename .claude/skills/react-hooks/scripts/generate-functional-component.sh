#!/bin/bash

# generate-functional-component.sh
#
# Purpose: Automates the creation of a functional React component with optional useState and useEffect boilerplate,
#          and a basic test file. This script streamlines the process of creating new components,
#          ensuring consistency and reducing manual setup.
#
# Usage: ./generate-functional-component.sh <ComponentName> [--state] [--effect] [--memo]
#   <ComponentName>: The name of the component (e.g., MyButton, UserProfile).
#                    The script will convert this to kebab-case for filenames and PascalCase for the component.
#   --state:         (Optional) Include a basic useState hook in the component.
#   --effect:        (Optional) Include a basic useEffect hook in the component.
#   --memo:          (Optional) Wrap the component in React.memo for performance optimization.
#
# Example:
#   ./generate-functional-component.sh MyNewComponent --state --effect
#   This will create:
#     - src/components/my-new-component/index.tsx
#     - src/components/my-new-component/my-new-component.test.tsx
#
# Configuration:
#   - COMPONENT_DIR: The base directory where components will be created. Defaults to 'src/components'.
#   - TEST_DIR:      The base directory where component tests will be created. Defaults to 'src/components'.
#
# Error Handling:
#   - Checks if a component name is provided.
#   - Checks if the component already exists to prevent accidental overwrites.
#   - Provides informative messages for success or failure.

# --- Configuration ---
COMPONENT_DIR="src/components"
TEST_DIR="src/components"
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

# Parse arguments
COMPONENT_NAME=""
INCLUDE_STATE=false
INCLUDE_EFFECT=false
INCLUDE_MEMO=false

for arg in "$@"; do
  case $arg in
    --state)
      INCLUDE_STATE=true
      shift
      ;;
    --effect)
      INCLUDE_EFFECT=true
      shift
      ;;
    --memo)
      INCLUDE_MEMO=true
      shift
      ;;
    -*) 
      echo "❌ Error: Unknown option '$arg'."
      echo "Usage: ./generate-functional-component.sh <ComponentName> [--state] [--effect] [--memo]"
      exit 1
      ;;
    *)
      if [ -z "$COMPONENT_NAME" ]; then
        COMPONENT_NAME="$arg"
      else
        echo "❌ Error: Too many arguments. Component name already provided."
      echo "Usage: ./generate-functional-component.sh <ComponentName> [--state] [--effect] [--memo]"
        exit 1
      fi
      shift
      ;;
  esac
done

# Check if component name is provided
if [ -z "$COMPONENT_NAME" ]; then
  echo "❌ Error: Please provide a name for your component."
  echo "Usage: ./generate-functional-component.sh <ComponentName> [--state] [--effect] [--memo]"
  exit 1
fi

COMPONENT_NAME_PASCAL=$(kebab_to_pascal "$COMPONENT_NAME")
COMPONENT_NAME_KEBAB=$(pascal_to_kebab "$COMPONENT_NAME_PASCAL")

COMPONENT_PATH="$COMPONENT_DIR/$COMPONENT_NAME_KEBAB"
COMPONENT_FILE="$COMPONENT_PATH/index.tsx"
TEST_FILE="$TEST_DIR/$COMPONENT_NAME_KEBAB/$COMPONENT_NAME_KEBAB.test.tsx"

# Check if component already exists
if [ -d "$COMPONENT_PATH" ]; then
  echo "⚠️ Warning: Component '$COMPONENT_NAME_PASCAL' already exists at '$COMPONENT_PATH'."
  read -p "Do you want to overwrite it? (y/N): " OVERWRITE
  if [[ ! "$OVERWRITE" =~ ^[yY]$ ]]; then
    echo "Aborting component generation."
    exit 0
  fi
  echo "Overwriting existing component..."
fi

# Create directories
mkdir -p "$COMPONENT_PATH" || { echo "❌ Error: Failed to create directory '$COMPONENT_PATH'."; exit 1; }
mkdir -p "$(dirname "$TEST_FILE")" || { echo "❌ Error: Failed to create directory for test file."; exit 1; }

# Build component content
COMPONENT_IMPORTS="import React"
COMPONENT_BODY=""

if [ "$INCLUDE_STATE" = true ]; then
  COMPONENT_IMPORTS=", { useState } from 'react'"
  COMPONENT_BODY="  const [count, setCount] = useState(0);

"
fi

if [ "$INCLUDE_EFFECT" = true ]; then
  if [ "$INCLUDE_STATE" = false ]; then
    COMPONENT_IMPORTS=", { useEffect } from 'react'"
  else
    COMPONENT_IMPORTS=", { useState, useEffect } from 'react'"
  fi
  COMPONENT_BODY+="  useEffect(() => {
    // Side effect logic here
    console.log('Component mounted or updated');

    return () => {
      // Cleanup logic here
      console.log('Component unmounted');
    };
  }, []); // Add dependencies here

"
fi

if [ "$INCLUDE_MEMO" = true ]; then
  if [[ ! "$COMPONENT_IMPORTS" =~ "React" ]]; then
    COMPONENT_IMPORTS="import React"
  fi
  COMPONENT_IMPORTS=", { memo } from 'react'"
  COMPONENT_WRAPPER="React.memo("
  COMPONENT_WRAPPER_END=")"
else
  COMPONENT_WRAPPER=""
  COMPONENT_WRAPPER_END=""
fi

# Create component file content
cat << EOF > "$COMPONENT_FILE"
${COMPONENT_IMPORTS};

interface ${COMPONENT_NAME_PASCAL}Props {
  // Define props here
}

const ${COMPONENT_NAME_PASCAL}: React.FC<${COMPONENT_NAME_PASCAL}Props> = ${COMPONENT_WRAPPER}(({ /* props */ }) => {
${COMPONENT_BODY}  return (
    <div>
      <h1>${COMPONENT_NAME_PASCAL} Component</h1>
      {${INCLUDE_STATE} && <p>Count: {count}</p>}
    </div>
  );
})${COMPONENT_WRAPPER_END};

export default ${COMPONENT_NAME_PASCAL};
EOF

# Create test file content
cat << EOF > "$TEST_FILE"
import { render, screen } from '@testing-library/react';
import ${COMPONENT_NAME_PASCAL} from './index';

describe('${COMPONENT_NAME_PASCAL}', () => {
  it('renders without crashing', () => {
    render(<${COMPONENT_NAME_PASCAL} />);
    expect(screen.getByText('${COMPONENT_NAME_PASCAL} Component')).toBeInTheDocument();
  });

  // Add more tests as needed for component logic and interactions
});
EOF

echo "✅ Successfully created component '$COMPONENT_NAME_PASCAL' at '$COMPONENT_FILE'."
echo "✅ Test file created at '$TEST_FILE'."
echo "To run tests, you might need to install '@testing-library/react' and 'jest-dom'."
echo "Example usage:"
echo "  <${COMPONENT_NAME_PASCAL} />"
