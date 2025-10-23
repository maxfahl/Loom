#!/bin/bash

# generate-use-case.sh
#
# Purpose:
#   Streamlines the creation of a new use case (interactor) within the application layer.
#   It generates the use case class, its corresponding input/output DTOs, and an interface
#   for its dependencies (e.g., a repository port). This automates the repetitive setup
#   involved in adding new application features, ensuring consistency and adherence to
#   Clean Architecture principles.
#
# Usage:
#   ./generate-use-case.sh -n <use_case_name> [-e <entity_name>] [-p <project_root>]
#
# Arguments:
#   -n, --name          Required. The name of the use case (e.g., CreateUser, GetProductDetails).
#   -e, --entity        Optional. The primary entity name associated with this use case (e.g., User, Product).
#                       Used for generating repository interfaces and imports. If not provided, a generic
#                       repository interface will be suggested.
#   -p, --project-root  Optional. The root directory of your project. Defaults to the current directory.
#
# Examples:
#   ./generate-use-case.sh -n CreateUser -e User
#   ./generate-use-case.sh -n GetProductDetails -e Product -p /path/to/my/project
#   ./generate-use-case.sh -n SendWelcomeEmail # For a use case not directly tied to a single entity
#
# Configuration:
#   None directly in script; relies on command-line arguments.
#
# Error Handling:
#   Provides clear error messages for missing or invalid arguments.
#   Checks if target files already exist.
#
# Dry-run Mode:
#   Not applicable for this script as it creates files.
#
# Colored Output:
#   Uses ANSI escape codes for colored output (green for success, red for error, yellow for warnings).

# --- Colors ---
GREEN="\033[0;32m"
RED="\033[0;31m"
YELLOW="\033[0;33m"
NC="\033[0m" # No Color

# --- Helper Functions ---
print_help() {
  echo -e "Usage: $0 -n <use_case_name> [-e <entity_name>] [-p <project_root>]"
  echo -e ""
  echo -e "Arguments:"
  echo -e "  -n, --name          Required. The name of the use case (e.g., CreateUser, GetProductDetails)."
  echo -e "  -e, --entity        Optional. The primary entity name associated with this use case (e.g., User, Product)."
  echo -e "                      Used for generating repository interfaces and imports."
  echo -e "  -p, --project-root  Optional. The root directory of your project. Defaults to the current directory."
  echo -e ""
  echo -e "Examples:"
  echo -e "  ./generate-use-case.sh -n CreateUser -e User"
  echo -e "  ./generate-use-case.sh -n GetProductDetails -e Product"
  echo -e "  ./generate-use-case.sh -n SendWelcomeEmail"
  exit 1
}

# --- Parse Arguments ---
while [[ "$#" -gt 0 ]]; do
  case "$1" in
    -n|--name) USE_CASE_NAME="$2"; shift ;;
    -e|--entity) ENTITY_NAME="$2"; shift ;;
    -p|--project-root) PROJECT_ROOT="$2"; shift ;;
    -h|--help) print_help ;;
    *) echo -e "${RED}Unknown parameter passed: $1${NC}"; print_help ;;
  esac
  shift
done

# --- Validate Arguments ---
if [ -z "$USE_CASE_NAME" ]; then
  echo -e "${RED}Error: Use case name is required.${NC}"
  print_help
fi

PROJECT_ROOT=${PROJECT_ROOT:-.}
BASE_DIR="$PROJECT_ROOT/src"

USE_CASE_KEBAB=$(echo "$USE_CASE_NAME" | sed -r 's/([A-Z])/-\L\1/g' | sed 's/^-//')
ENTITY_KEBAB=$(echo "$ENTITY_NAME" | sed -r 's/([A-Z])/-\L\1/g' | sed 's/^-//')

# --- Define Paths ---
USE_CASES_DIR="$BASE_DIR/application/use-cases"
PORTS_DIR="$BASE_DIR/application/ports"
DTOS_DIR="$BASE_DIR/application/dtos"
DOMAIN_ENTITIES_DIR="$BASE_DIR/domain/entities"

mkdir -p "$USE_CASES_DIR"
mkdir -p "$PORTS_DIR"
mkdir -p "$DTOS_DIR"

# --- Generate Request DTO ---
REQUEST_DTO_FILE="$DTOS_DIR/${USE_CASE_KEBAB}-request.ts"
if [ -f "$REQUEST_DTO_FILE" ]; then
  echo -e "${YELLOW}Warning: Request DTO file '$REQUEST_DTO_FILE' already exists. Skipping creation.${NC}"
else
  echo -e "export interface ${USE_CASE_NAME}Request {
  // Define input properties for the use case
  // Example: userId: string;
}
" > "$REQUEST_DTO_FILE"
  echo -e "${GREEN}Generated: $REQUEST_DTO_FILE${NC}"
fi

# --- Generate Response DTO ---
RESPONSE_DTO_FILE="$DTOS_DIR/${USE_CASE_KEBAB}-response.ts"
if [ -f "$RESPONSE_DTO_FILE" ]; then
  echo -e "${YELLOW}Warning: Response DTO file '$RESPONSE_DTO_FILE' already exists. Skipping creation.${NC}"
else
  echo -e "export interface ${USE_CASE_NAME}Response {
  // Define output properties for the use case
  // Example: success: boolean;
  // Example: user: { id: string; name: string; email: string; };
}
" > "$RESPONSE_DTO_FILE"
  echo -e "${GREEN}Generated: $RESPONSE_DTO_FILE${NC}"
fi

# --- Generate Repository Interface (Port) ---
if [ -n "$ENTITY_NAME" ]; then
  REPO_INTERFACE_NAME="I${ENTITY_NAME}Repository"
  REPO_FILE_NAME="${ENTITY_KEBAB}-repository.ts"
  REPO_INTERFACE_FILE="$PORTS_DIR/$REPO_FILE_NAME"

  if [ -f "$REPO_INTERFACE_FILE" ]; then
    echo -e "${YELLOW}Warning: Repository interface file '$REPO_INTERFACE_FILE' already exists. Skipping creation.${NC}"
  else
    ENTITY_IMPORT="import { ${ENTITY_NAME} } from '../../domain/entities/${ENTITY_KEBAB}';"
    echo -e "${ENTITY_IMPORT}

export interface ${REPO_INTERFACE_NAME} {
  // Define methods for interacting with ${ENTITY_NAME} data storage
  // Example: findById(id: string): Promise<${ENTITY_NAME} | null>;
  // Example: save(${ENTITY_KEBAB}: ${ENTITY_NAME}): Promise<${ENTITY_NAME}>;
}
" > "$REPO_INTERFACE_FILE"
    echo -e "${GREEN}Generated: $REPO_INTERFACE_FILE${NC}"
  fi
  REPO_IMPORT_STATEMENT="import { ${REPO_INTERFACE_NAME} } from '../ports/${ENTITY_KEBAB}-repository';"
  REPO_CONSTRUCTOR_PARAM="private readonly ${ENTITY_KEBAB}Repository: ${REPO_INTERFACE_NAME}"
else
  REPO_IMPORT_STATEMENT="// Consider defining a repository interface if this use case interacts with data."
  REPO_CONSTRUCTOR_PARAM="// private readonly someRepository: ISomeRepository"
fi

# --- Generate Use Case Class ---
USE_CASE_FILE="$USE_CASES_DIR/${USE_CASE_KEBAB}.ts"
if [ -f "$USE_CASE_FILE" ]; then
  echo -e "${YELLOW}Warning: Use case file '$USE_CASE_FILE' already exists. Skipping creation.${NC}"
else
  echo -e "import { ${USE_CASE_NAME}Request } from '../dtos/${USE_CASE_KEBAB}-request';
import { ${USE_CASE_NAME}Response } from '../dtos/${USE_CASE_KEBAB}-response';
${REPO_IMPORT_STATEMENT}

export class ${USE_CASE_NAME}UseCase {
  constructor(${REPO_CONSTRUCTOR_PARAM}) {}

  async execute(request: ${USE_CASE_NAME}Request): Promise<${USE_CASE_NAME}Response> {
    // Implement the core business logic for ${USE_CASE_NAME}
    console.log('Executing ${USE_CASE_NAME} with request:', request);
    return { /* populate with actual response data */ };
  }
}
" > "$USE_CASE_FILE"
  echo -e "${GREEN}Generated: $USE_CASE_FILE${NC}"
fi

# --- Update index.ts for use-cases, ports, dtos ---
for DIR in "$USE_CASES_DIR" "$PORTS_DIR" "$DTOS_DIR"; do
  INDEX_FILE="$DIR/index.ts"
  COMPONENT_NAME=""
  if [ "$DIR" == "$USE_CASES_DIR" ]; then
    COMPONENT_NAME="${USE_CASE_KEBAB}"
  elif [ "$DIR" == "$PORTS_DIR" ] && [ -n "$ENTITY_NAME" ]; then
    COMPONENT_NAME="${ENTITY_KEBAB}-repository"
  elif [ "$DIR" == "$DTOS_DIR" ]; then
    COMPONENT_NAME="${USE_CASE_KEBAB}-request"
    # Also add response DTO
    RESPONSE_EXPORT_STATEMENT="export * from './${USE_CASE_KEBAB}-response';"
    if [ -f "$INDEX_FILE" ]; then
      if ! grep -q "$RESPONSE_EXPORT_STATEMENT" "$INDEX_FILE"; then
        echo "$RESPONSE_EXPORT_STATEMENT" >> "$INDEX_FILE"
        echo -e "${GREEN}Added export for ${USE_CASE_KEBAB}-response to $INDEX_FILE${NC}"
      fi
    else
      echo "$RESPONSE_EXPORT_STATEMENT" > "$INDEX_FILE"
      echo -e "${GREEN}Created $INDEX_FILE with export for ${USE_CASE_KEBAB}-response${NC}"
    fi
  fi

  if [ -n "$COMPONENT_NAME" ]; then
    EXPORT_STATEMENT="export * from './${COMPONENT_NAME}';"
    if [ -f "$INDEX_FILE" ]; then
      if ! grep -q "$EXPORT_STATEMENT" "$INDEX_FILE"; then
        echo "$EXPORT_STATEMENT" >> "$INDEX_FILE"
        echo -e "${GREEN}Added export for ${COMPONENT_NAME} to $INDEX_FILE${NC}"
      else
        echo -e "${YELLOW}Export for '${COMPONENT_NAME}' already exists in $INDEX_FILE. Skipping.${NC}"
      fi
    else
      echo "$EXPORT_STATEMENT" > "$INDEX_FILE"
      echo -e "${GREEN}Created $INDEX_FILE with export for ${COMPONENT_NAME}${NC}"
    fi
  fi
done
