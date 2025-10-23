#!/bin/bash

# generate-clean-layer.sh
#
# Purpose:
#   Automates the creation of new files within a specified Clean Architecture layer
#   (e.g., domain, application, infrastructure, presentation). It creates the necessary
#   folder structure and boilerplate files (e.g., an interface, a class, a use case)
#   based on the layer and component type. This saves significant time and ensures
#   consistency in project structure.
#
# Usage:
#   ./generate-clean-layer.sh -l <layer> -n <name> -t <type> [-p <project_root>]
#
# Arguments:
#   -l, --layer         Required. The Clean Architecture layer (e.g., domain, application, infrastructure, presentation).
#   -n, --name          Required. The name of the component (e.g., User, ProductRepository, CreateUser).
#   -t, --type          Required. The type of component (e.g., entity, interface, use-case, repository, controller, service, dto).
#   -p, --project-root  Optional. The root directory of your project. Defaults to the current directory.
#
# Examples:
#   ./generate-clean-layer.sh -l domain -n User -t entity
#   ./generate-clean-layer.sh -l application -n IUserRepository -t interface
#   ./generate-clean-layer.sh -l application -n CreateUser -t use-case
#   ./generate-clean-layer.sh -l infrastructure -n PostgreSQLUserRepository -t repository
#   ./generate-clean-layer.sh -l presentation -n UserController -t controller
#   ./generate-clean-layer.sh -l application -n UserDto -t dto
#
# Configuration:
#   None directly in script; relies on command-line arguments.
#
# Error Handling:
#   Provides clear error messages for missing or invalid arguments.
#   Checks if target directory already exists.
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
  echo -e "Usage: $0 -l <layer> -n <name> -t <type> [-p <project_root>]"
  echo -e ""
  echo -e "Arguments:"
  echo -e "  -l, --layer         Required. The Clean Architecture layer (e.g., domain, application, infrastructure, presentation)."
  echo -e "  -n, --name          Required. The name of the component (e.g., User, ProductRepository, CreateUser)."
  echo -e "  -t, --type          Required. The type of component (e.g., entity, interface, use-case, repository, controller, service, dto)."
  echo -e "  -p, --project-root  Optional. The root directory of your project. Defaults to the current directory."
  echo -e ""
  echo -e "Examples:"
  echo -e "  ./generate-clean-layer.sh -l domain -n User -t entity"
  echo -e "  ./generate-clean-layer.sh -l application -n IUserRepository -t interface"
  echo -e "  ./generate-clean-layer.sh -l application -n CreateUser -t use-case"
  echo -e "  ./generate-clean-layer.sh -l infrastructure -n PostgreSQLUserRepository -t repository"
  echo -e "  ./generate-clean-layer.sh -l presentation -n UserController -t controller"
  echo -e "  ./generate-clean-layer.sh -l application -n UserDto -t dto"
  exit 1
}

# --- Parse Arguments ---
while [[ "$#" -gt 0 ]]; do
  case "$1" in
    -l|--layer) LAYER="$2"; shift ;;
    -n|--name) NAME="$2"; shift ;;
    -t|--type) TYPE="$2"; shift ;;
    -p|--project-root) PROJECT_ROOT="$2"; shift ;;
    -h|--help) print_help ;;
    *) echo -e "${RED}Unknown parameter passed: $1${NC}"; print_help ;;
  esac
  shift
done

# --- Validate Arguments ---
if [ -z "$LAYER" ] || [ -z "$NAME" ] || [ -z "$TYPE" ]; then
  echo -e "${RED}Error: Missing required arguments. Layer, Name, and Type are mandatory.${NC}"
  print_help
fi

PROJECT_ROOT=${PROJECT_ROOT:-.}
BASE_DIR="$PROJECT_ROOT/src" # Assuming 'src' as the base for layers

# --- Determine Target Directory and File Content ---
FILE_CONTENT=""
FILE_EXTENSION="ts"
TARGET_SUBDIR=""

case "$LAYER" in
  domain)
    case "$TYPE" in
      entity)
        TARGET_SUBDIR="domain/entities"
        FILE_CONTENT="export class ${NAME} {
  constructor(public id: string, public name: string) {}
}
"
        ;;
      interface)
        TARGET_SUBDIR="domain/interfaces"
        FILE_CONTENT="export interface I${NAME} {
  // Define domain-specific interfaces here
}
"
        ;;
      value-object)
        TARGET_SUBDIR="domain/value-objects"
        FILE_CONTENT="export class ${NAME} {
  constructor(public value: string) {}

  equals(other: ${NAME}): boolean {
    return this.value === other.value;
  }
}
"
        ;;
      *)
        echo -e "${RED}Error: Invalid type '$TYPE' for layer 'domain'. Valid types: entity, interface, value-object.${NC}"
        exit 1
        ;;
    esac
    ;;
  application)
    case "$TYPE" in
      use-case)
        TARGET_SUBDIR="application/use-cases"
        FILE_CONTENT="import { I${NAME}Repository } from '../ports/${NAME,,}-repository';

interface ${NAME}Request {
  // Define request properties
}

interface ${NAME}Response {
  // Define response properties
}

export class ${NAME}UseCase {
  constructor(private readonly ${NAME,,}Repository: I${NAME}Repository) {}

  async execute(request: ${NAME}Request): Promise<${NAME}Response> {
    // Implement use case logic here
    return { /* response data */ };
  }
}
"
        ;;
      port|interface)
        TARGET_SUBDIR="application/ports"
        FILE_CONTENT="import { ${NAME} } from '../../domain/entities/${NAME,,}';

export interface I${NAME}Repository {
  findById(id: string): Promise<${NAME} | null>;
  save(${NAME,,}: ${NAME}): Promise<${NAME}>;
}
"
        ;;
      dto)
        TARGET_SUBDIR="application/dtos"
        FILE_CONTENT="export interface ${NAME} {
  // Define DTO properties
}
"
        ;;
      *)
        echo -e "${RED}Error: Invalid type '$TYPE' for layer 'application'. Valid types: use-case, port, interface, dto.${NC}"
        exit 1
        ;;
    esac
    ;;
  infrastructure)
    case "$TYPE" in
      repository)
        TARGET_SUBDIR="infrastructure/persistence"
        FILE_CONTENT="import { I${NAME}Repository } from '../../application/ports/${NAME,,}-repository';
import { ${NAME} } from '../../domain/entities/${NAME,,}';

export class ${NAME}Repository implements I${NAME}Repository {
  // Implement repository methods here (e.g., database interactions)
  async findById(id: string): Promise<${NAME} | null> {
    throw new Error('Method not implemented.');
  }
  async save(${NAME,,}: ${NAME}): Promise<${NAME}> {
    throw new Error('Method not implemented.');
  }
}
"
        ;;
      service)
        TARGET_SUBDIR="infrastructure/services"
        FILE_CONTENT="export class ${NAME}Service {
  // Implement external service interactions here
}
"
        ;;
      config)
        TARGET_SUBDIR="infrastructure/config"
        FILE_CONTENT="export const ${NAME}Config = {
  // Define configuration properties
};
"
        ;;
      *)
        echo -e "${RED}Error: Invalid type '$TYPE' for layer 'infrastructure'. Valid types: repository, service, config.${NC}"
        exit 1
        ;;
    esac
    ;;
  presentation)
    case "$TYPE" in
      controller)
        TARGET_SUBDIR="presentation/controllers"
        FILE_CONTENT="import { ${NAME}UseCase } from '../../application/use-cases/${NAME,,}-use-case';

export class ${NAME}Controller {
  constructor(private readonly ${NAME,,}UseCase: ${NAME}UseCase) {}

  async handleRequest(req: any, res: any): Promise<void> {
    // Handle request, call use case, send response
    res.status(200).send('OK');
  }
}
"
        ;;
      route)
        TARGET_SUBDIR="presentation/routes"
        FILE_CONTENT="import { Router } from 'express';
import { ${NAME}Controller } from '../controllers/${NAME,,}-controller';

const router = Router();
const ${NAME,,}Controller = new ${NAME}Controller(/* inject use case */);

router.get('/${NAME,,}s', ${NAME,,}Controller.handleRequest);

export default router;
"
        ;;
      middleware)
        TARGET_SUBDIR="presentation/middlewares"
        FILE_CONTENT="import { Request, Response, NextFunction } from 'express';

export function ${NAME}Middleware(req: Request, res: Response, next: NextFunction) {
  // Implement middleware logic
  next();
}
"
        ;;
      *)
        echo -e "${RED}Error: Invalid type '$TYPE' for layer 'presentation'. Valid types: controller, route, middleware.${NC}"
        exit 1
        ;;
    esac
    ;;
  *)
    echo -e "${RED}Error: Invalid layer '$LAYER'. Valid layers: domain, application, infrastructure, presentation.${NC}"
    exit 1
    ;;
esac

# --- Create Directory and File ---
FULL_TARGET_DIR="$BASE_DIR/$TARGET_SUBDIR"
FILE_NAME="${NAME,,}.${FILE_EXTENSION}" # Convert name to lowercase for filename
FULL_FILE_PATH="$FULL_TARGET_DIR/$FILE_NAME"

mkdir -p "$FULL_TARGET_DIR"

if [ -f "$FULL_FILE_PATH" ]; then
  echo -e "${YELLOW}Warning: File '$FULL_FILE_PATH' already exists. Skipping creation.${NC}"
else
  echo -e "$FILE_CONTENT" > "$FULL_FILE_PATH"
  echo -e "${GREEN}Successfully created: $FULL_FILE_PATH${NC}"
fi

# --- Update index.ts (if exists or create) ---
INDEX_FILE="$FULL_TARGET_DIR/index.ts"
EXPORT_STATEMENT="export * from './${NAME,,}';"

if [ -f "$INDEX_FILE" ]; then
  if ! grep -q "$EXPORT_STATEMENT" "$INDEX_FILE"; then
    echo "$EXPORT_STATEMENT" >> "$INDEX_FILE"
    echo -e "${GREEN}Added export to $INDEX_FILE${NC}"
  else
    echo -e "${YELLOW}Export for '${NAME,,}' already exists in $INDEX_FILE. Skipping.${NC}"
  fi
else
  echo "$EXPORT_STATEMENT" > "$INDEX_FILE"
  echo -e "${GREEN}Created $INDEX_FILE with export for '${NAME,,}'${NC}"
fi
