#!/bin/bash

# generate-component.sh
#
# Description:
#   Automates the creation of a new React functional component with TypeScript,
#   including its .tsx file, a corresponding test file (.test.tsx), and an
#   optional CSS module file (.module.css). It sets up basic boilerplate,
#   props interface, and a simple test using React Testing Library.
#
# Usage:
#   ./generate-component.sh <ComponentName> [--css] [--path <path/to/components>]
#
# Examples:
#   ./generate-component.sh MyButton
#   ./generate-component.sh UserProfile --css
#   ./generate-component.sh Header --path src/layout
#
# Configuration:
#   None directly in script; uses command-line arguments.
#
# Error Handling:
#   Checks for component name, valid path, and prevents overwriting existing files.
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
COMPONENT_NAME=""
USE_CSS=false
COMPONENT_PATH="src/components" # Default path

# --- Functions ---

show_help() {
  echo -e "${BLUE}Usage:${NC} ./generate-component.sh <ComponentName> [--css] [--path <path/to/components>]"
  echo ""
  echo -e "${BLUE}Description:${NC}"
  echo "  Automates the creation of a new React functional component with TypeScript,"
  echo "  including its .tsx file, a corresponding test file (.test.tsx), and an"
  echo "  optional CSS module file (.module.css). It sets up basic boilerplate,"
  echo "  props interface, and a simple test using React Testing Library."
  echo ""
  echo -e "${BLUE}Options:${NC}"
  echo "  <ComponentName>       The name of the React component (e.g., MyButton)."
  echo "  --css                 (Optional) Include a CSS module file (.module.css) for the component."
  echo "  --path <path>         (Optional) Specify the directory where the component files will be created."
  echo "                        Defaults to 'src/components'."
  echo "  -h, --help            Display this help message."
  echo ""
  echo -e "${BLUE}Examples:${NC}"
  echo "  ./generate-component.sh MyButton"
  echo "  ./generate-component.sh UserProfile --css"
  echo "  ./generate-component.sh Header --path src/layout"
  exit 0
}

# --- Parse Arguments ---
while [[ "$#" -gt 0 ]]; do
  case "$1" in
    --css)
      USE_CSS=true
      shift
      ;;
    --path)
      if [ -n "$2" ] && [[ "$2" != -* ]]; then
        COMPONENT_PATH="$2"
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
      if [ -z "$COMPONENT_NAME" ]; then
        COMPONENT_NAME="$1"
        shift
      else
        echo -e "${RED}Error:${NC} Unknown argument: $1" >&2
        show_help
      fi
      ;;
  esac
done

# --- Validation ---
if [ -z "$COMPONENT_NAME" ]; then
  echo -e "${RED}Error:${NC} Component name is required." >&2
  show_help
fi

# Convert component name to PascalCase for file names and component export
PASCAL_CASE_NAME=$(echo "$COMPONENT_NAME" | sed -r 's/(^|-)([a-z])/​\2/g')
KEBAB_CASE_NAME=$(echo "$COMPONENT_NAME" | tr '[:upper:]' '[:lower:]' | sed 's/ /-/g')

TARGET_DIR="${COMPONENT_PATH}/${PASCAL_CASE_NAME}"

if [ -d "$TARGET_DIR" ]; then
  echo -e "${RED}Error:${NC} Directory '${TARGET_DIR}' already exists. Aborting to prevent overwrite." >&2
  exit 1
fi

# --- Create Directory ---
echo -e "${BLUE}Creating directory:${NC} ${TARGET_DIR}"
mkdir -p "$TARGET_DIR" || { echo -e "${RED}Error:${NC} Failed to create directory '${TARGET_DIR}'."; exit 1; }

# --- Create Component File (.tsx) ---
COMPONENT_FILE="${TARGET_DIR}/${PASCAL_CASE_NAME}.tsx"
echo -e "${BLUE}Creating component file:${NC} ${COMPONENT_FILE}"
cat << EOF > "$COMPONENT_FILE"
import React from 'react';
${USE_CSS == true ? "import styles from './${PASCAL_CASE_NAME}.module.css';" : ""}

interface ${PASCAL_CASE_NAME}Props {
  // Define your props here
  message: string;
}

const ${PASCAL_CASE_NAME}: React.FC<${PASCAL_CASE_NAME}Props> = ({ message }) => {
  return (
    <div${USE_CSS == true ? " className={styles.container}" : ""}> 
      <h1>{message}</h1>
      <p>This is the ${PASCAL_CASE_NAME} component.</p>
    </div>
  );
};

export default ${PASCAL_CASE_NAME};
EOF

# --- Create Test File (.test.tsx) ---
TEST_FILE="${TARGET_DIR}/${PASCAL_CASE_NAME}.test.tsx"
echo -e "${BLUE}Creating test file:${NC} ${TEST_FILE}"
cat << EOF > "$TEST_FILE"
import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import ${PASCAL_CASE_NAME} from './${PASCAL_CASE_NAME}';

describe('${PASCAL_CASE_NAME}', () => {
  it('renders the component with the provided message', () => {
    const testMessage = 'Hello from Test!';
    render(<${PASCAL_CASE_NAME} message={testMessage} />);

    // Check if the message is rendered
    expect(screen.getByText(testMessage)).toBeInTheDocument();

    // Check if the component text is rendered
    expect(screen.getByText(/This is the ${PASCAL_CASE_NAME} component./i)).toBeInTheDocument();
  });

  // Add more tests here as needed
});
EOF

# --- Create CSS Module File (.module.css) ---
if [ "$USE_CSS" = true ]; then
  CSS_FILE="${TARGET_DIR}/${PASCAL_CASE_NAME}.module.css"
  echo -e "${BLUE}Creating CSS module file:${NC} ${CSS_FILE}"
  cat << EOF > "$CSS_FILE"
.container {
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 8px;
  background-color: #f9f9f9;
}

.container h1 {
  color: #333;
}

.container p {
  color: #666;
}
EOF
fi

echo -e "${GREEN}Successfully created ${PASCAL_CASE_NAME} component in ${TARGET_DIR}${NC}"
echo -e "${YELLOW}Remember to update the props interface and add more comprehensive tests!${NC}"