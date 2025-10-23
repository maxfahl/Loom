#!/bin/bash

# generate-nested-context.sh
#
# Purpose: Generates a boilerplate for a nested context structure, demonstrating how to combine
#          multiple contexts effectively. This helps in organizing related but distinct global states.
#
# Usage: ./generate-nested-context.sh <ParentContextName> <ChildContextName1> [ChildContextName2...]
#   <ParentContextName>: The name of the top-level context (e.g., App, Global).
#   <ChildContextName1>: The name of the first child context (e.g., Auth, Theme).
#   [ChildContextName2...]: Optional additional child context names.
#
# Example:
#   ./generate-nested-context.sh App Auth Theme
#   This will create:
#     - src/contexts/app/index.tsx (combines AuthProvider and ThemeProvider)
#     - src/contexts/auth/index.tsx
#     - src/contexts/theme/index.tsx
#
# Configuration:
#   - CONTEXT_DIR: The base directory where contexts will be created. Defaults to 'src/contexts'.
#
# Error Handling:
#   - Checks if at least two context names are provided (one parent, at least one child).
#   - Provides informative messages for success or failure.

# --- Configuration ---
CONTEXT_DIR="src/contexts"
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

# Function to generate a single context file
generate_single_context() {
  local CONTEXT_NAME_PASCAL=$1
  local CONTEXT_NAME_KEBAB=$(pascal_to_kebab "$CONTEXT_NAME_PASCAL")
  local CONTEXT_PATH="$CONTEXT_DIR/$CONTEXT_NAME_KEBAB"
  local CONTEXT_FILE="$CONTEXT_PATH/index.tsx"

  mkdir -p "$CONTEXT_PATH" || { echo "❌ Error: Failed to create directory '$CONTEXT_PATH'."; return 1; }

  cat << EOF > "$CONTEXT_FILE"
import React, { createContext, useContext, useState, useMemo, useCallback, ReactNode } from 'react';

// 1. Define the Context's Data Shape
interface ${CONTEXT_NAME_PASCAL}ContextType {
  ${CONTEXT_NAME_PASCAL,,}Value: string;
  set${CONTEXT_NAME_PASCAL}Value: (newValue: string) => void;
}

// 2. Create the Context with a default (initial) value
const ${CONTEXT_NAME_PASCAL}Context = createContext<${CONTEXT_NAME_PASCAL}ContextType | undefined>(undefined);

// 3. Create a Provider Component
interface ${CONTEXT_NAME_PASCAL}ProviderProps {
  children: ReactNode;
}

export const ${CONTEXT_NAME_PASCAL}Provider: React.FC<${CONTEXT_NAME_PASCAL}ProviderProps> = ({ children }) => {
  const [${CONTEXT_NAME_PASCAL,,}Value, set${CONTEXT_NAME_PASCAL}Value] = useState<string>('Default ${CONTEXT_NAME_PASCAL} Value');

  const contextValue = useMemo(() => ({
    ${CONTEXT_NAME_PASCAL,,}Value,
    set${CONTEXT_NAME_PASCAL}Value,
  }), [${CONTEXT_NAME_PASCAL,,}Value]);

  return (
    <${CONTEXT_NAME_PASCAL}Context.Provider value={contextValue}>
      {children}
    </${CONTEXT_NAME_PASCAL}Context.Provider>
  );
};

// 4. Create a Custom Hook to consume the Context
export const use${CONTEXT_NAME_PASCAL} = () => {
  const context = useContext(${CONTEXT_NAME_PASCAL}Context);
  if (context === undefined) {
    throw new Error(`use${CONTEXT_NAME_PASCAL} must be used within a ${CONTEXT_NAME_PASCAL}Provider`);
  }
  return context;
};

export default ${CONTEXT_NAME_PASCAL}Context;
EOF
  echo "✅ Created context file: $CONTEXT_FILE"
}

# --- Main Script Logic ---

# Check if at least two arguments are provided (ParentContextName and at least one ChildContextName)
if [ "$#" -lt 2 ]; then
  echo "❌ Error: Please provide at least a ParentContextName and one ChildContextName."
  echo "Usage: ./generate-nested-context.sh <ParentContextName> <ChildContextName1> [ChildContextName2...]"
  exit 1
fi

PARENT_CONTEXT_NAME_PASCAL=$(kebab_to_pascal "$1")
PARENT_CONTEXT_NAME_KEBAB=$(pascal_to_kebab "$PARENT_CONTEXT_NAME_PASCAL")
PARENT_CONTEXT_PATH="$CONTEXT_DIR/$PARENT_CONTEXT_NAME_KEBAB"
PARENT_CONTEXT_FILE="$PARENT_CONTEXT_PATH/index.tsx"

shift # Remove parent context name from arguments

CHILD_CONTEXT_NAMES=("$@")

# Generate individual child contexts
for child_name in "${CHILD_CONTEXT_NAMES[@]}"; do
  generate_single_context "$(kebab_to_pascal "$child_name")" || exit 1
done

# Generate the main parent context file that combines providers
mkdir -p "$PARENT_CONTEXT_PATH" || { echo "❌ Error: Failed to create directory '$PARENT_CONTEXT_PATH'."; exit 1; }

MAIN_FILE_IMPORTS=""
MAIN_FILE_PROVIDERS=""
for child_name in "${CHILD_CONTEXT_NAMES[@]}"; do
  CHILD_NAME_PASCAL=$(kebab_to_pascal "$child_name")
  CHILD_NAME_KEBAB=$(pascal_to_kebab "$CHILD_NAME_PASCAL")
  MAIN_FILE_IMPORTS+="import { ${CHILD_NAME_PASCAL}Provider } from '../${CHILD_NAME_KEBAB}';\n"
  MAIN_FILE_PROVIDERS+="    <${CHILD_NAME_PASCAL}Provider>\n"
done

MAIN_FILE_PROVIDERS_END=""
for child_name in "${CHILD_CONTEXT_NAMES[@]}"; do
  CHILD_NAME_PASCAL=$(kebab_to_pascal "$child_name")
  MAIN_FILE_PROVIDERS_END+="    </${CHILD_NAME_PASCAL}Provider>\n"
done

cat << EOF > "$PARENT_CONTEXT_FILE"
import React, { ReactNode } from 'react';
${MAIN_FILE_IMPORTS}

interface ${PARENT_CONTEXT_NAME_PASCAL}ProviderProps {
  children: ReactNode;
}

export const ${PARENT_CONTEXT_NAME_PASCAL}Provider: React.FC<${PARENT_CONTEXT_NAME_PASCAL}ProviderProps> = ({ children }) => {
  return (
${MAIN_FILE_PROVIDERS}      {children}
${MAIN_FILE_PROVIDERS_END}  );
};

export default ${PARENT_CONTEXT_NAME_PASCAL}Provider;
EOF

echo "✅ Created main nested context file: $PARENT_CONTEXT_FILE"
echo "To use, wrap your application or a part of it with <${PARENT_CONTEXT_NAME_PASCAL}Provider>."
echo "Example: <${PARENT_CONTEXT_NAME_PASCAL}Provider><YourApp /></${PARENT_CONTEXT_NAME_PASCAL}Provider>"
