#!/bin/bash

# generate-context.sh
#
# Purpose: Automates the creation of a React Context boilerplate, including createContext,
#          a Provider component, and a custom useContext hook.
#          This script streamlines the process of setting up new contexts, ensuring consistency
#          and reducing repetitive setup tasks.
#
# Usage: ./generate-context.sh <ContextName>
#   <ContextName>: The name of the context (e.g., Theme, Auth, UserSettings).
#                  The script will convert this to kebab-case for filenames and PascalCase for components/hooks.
#
# Example:
#   ./generate-context.sh Auth
#   This will create:
#     - src/contexts/auth/index.tsx
#     - src/contexts/auth/auth.test.tsx
#
# Configuration:
#   - CONTEXT_DIR: The base directory where contexts will be created. Defaults to 'src/contexts'.
#   - TEST_DIR:    The base directory where context tests will be created. Defaults to 'src/contexts'.
#
# Error Handling:
#   - Checks if a context name is provided.
#   - Checks if the context already exists to prevent accidental overwrites.
#   - Provides informative messages for success or failure.

# --- Configuration ---
CONTEXT_DIR="src/contexts"
TEST_DIR="src/contexts"
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

# Check if context name is provided
if [ -z "$1" ]; then
  echo "❌ Error: Please provide a name for your context."
  echo "Usage: ./generate-context.sh <ContextName>"
  exit 1
fi

CONTEXT_NAME_PASCAL=$(kebab_to_pascal "$1")
CONTEXT_NAME_KEBAB=$(pascal_to_kebab "$CONTEXT_NAME_PASCAL")

CONTEXT_PATH="$CONTEXT_DIR/$CONTEXT_NAME_KEBAB"
CONTEXT_FILE="$CONTEXT_PATH/index.tsx"
TEST_FILE="$TEST_DIR/$CONTEXT_NAME_KEBAB/$CONTEXT_NAME_KEBAB.test.tsx"

# Check if context already exists
if [ -d "$CONTEXT_PATH" ]; then
  echo "⚠️ Warning: Context '$CONTEXT_NAME_PASCAL' already exists at '$CONTEXT_PATH'."
  read -p "Do you want to overwrite it? (y/N): " OVERWRITE
  if [[ ! "$OVERWRITE" =~ ^[yY]$ ]]; then
    echo "Aborting context generation."
    exit 0
  fi
  echo "Overwriting existing context..."
fi

# Create directories
mkdir -p "$CONTEXT_PATH" || { echo "❌ Error: Failed to create directory '$CONTEXT_PATH'."; exit 1; }
mkdir -p "$(dirname "$TEST_FILE")" || { echo "❌ Error: Failed to create directory for test file."; exit 1; }

# Create context file content
cat << EOF > "$CONTEXT_FILE"
import React, { createContext, useContext, useState, useMemo, useCallback, ReactNode } from 'react';

// 1. Define the Context's Data Shape
interface ${CONTEXT_NAME_PASCAL}ContextType {
  value: string;
  setValue: (newValue: string) => void;
  // Add other context-specific data and functions here
}

// 2. Create the Context with a default (initial) value
// The default value is used when a component consumes the context without a matching Provider above it.
const ${CONTEXT_NAME_PASCAL}Context = createContext<${CONTEXT_NAME_PASCAL}ContextType | undefined>(undefined);

// 3. Create a Provider Component
interface ${CONTEXT_NAME_PASCAL}ProviderProps {
  children: ReactNode;
}

export const ${CONTEXT_NAME_PASCAL}Provider: React.FC<${CONTEXT_NAME_PASCAL}ProviderProps> = ({ children }) => {
  const [value, setValue] = useState<string>('Default ${CONTEXT_NAME_PASCAL} Value');

  // Memoize the context value to prevent unnecessary re-renders of consumers
  // The value object will only be re-created if 'value' or 'setValue' (which is stable) changes.
  const contextValue = useMemo(() => ({
    value,
    setValue,
    // Include other memoized functions or values here
  }), [value]);

  return (
    <${CONTEXT_NAME_PASCAL}Context.Provider value={contextValue}>
      {children}
    </${CONTEXT_NAME_PASCAL}Context.Provider>
  );
};

// 4. Create a Custom Hook to consume the Context
// This hook provides a convenient and type-safe way to access the context value.
export const use${CONTEXT_NAME_PASCAL} = () => {
  const context = useContext(${CONTEXT_NAME_PASCAL}Context);
  if (context === undefined) {
    throw new Error(`use${CONTEXT_NAME_PASCAL} must be used within a ${CONTEXT_NAME_PASCAL}Provider`);
  }
  return context;
};

// Optional: Export the context itself if needed for advanced scenarios (e.g., testing)
export default ${CONTEXT_NAME_PASCAL}Context;
EOF

# Create test file content
cat << EOF > "$TEST_FILE"
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import React from 'react';
import { ${CONTEXT_NAME_PASCAL}Provider, use${CONTEXT_NAME_PASCAL} } from './index';

// A test component that consumes the context
const TestComponent: React.FC = () => {
  const { value, setValue } = use${CONTEXT_NAME_PASCAL}();
  return (
    <div>
      <span data-testid="context-value">{value}</span>
      <button onClick={() => setValue('New Value')}>Update Value</button>
    </div>
  );
};

describe('${CONTEXT_NAME_PASCAL} Context', () => {
  it('provides the default value', () => {
    render(
      <${CONTEXT_NAME_PASCAL}Provider>
        <TestComponent />
      </${CONTEXT_NAME_PASCAL}Provider>
    );
    expect(screen.getByTestId('context-value')).toHaveTextContent('Default ${CONTEXT_NAME_PASCAL} Value');
  });

  it('updates the context value', async () => {
    render(
      <${CONTEXT_NAME_PASCAL}Provider>
        <TestComponent />
      </${CONTEXT_NAME_PASCAL}Provider>
    );

    const updateButton = screen.getByRole('button', { name: /Update Value/i });
    await userEvent.click(updateButton);

    expect(screen.getByTestId('context-value')).toHaveTextContent('New Value');
  });

  it('throws an error if used outside of a provider', () => {
    // Suppress console error for this specific test
    const consoleError = jest.spyOn(console, 'error').mockImplementation(() => {});

    expect(() => render(<TestComponent />)).toThrow(
      `use${CONTEXT_NAME_PASCAL} must be used within a ${CONTEXT_NAME_PASCAL}Provider`
    );

    consoleError.mockRestore();
  });
});
EOF

echo "✅ Successfully created context '$CONTEXT_NAME_PASCAL' at '$CONTEXT_FILE'."
echo "✅ Test file created at '$TEST_FILE'."
echo "To run tests, you might need to install '@testing-library/react', '@testing-library/user-event', and 'jest-environment-jsdom'."
echo "Example usage:"
echo "  // In your App.tsx or parent component:
  // <${CONTEXT_NAME_PASCAL}Provider>
  //   <YourComponent />
  // </${CONTEXT_NAME_PASCAL}Provider>
  //
  // // In YourComponent or any child component:
  // const { value, setValue } = use${CONTEXT_NAME_PASCAL}();"
