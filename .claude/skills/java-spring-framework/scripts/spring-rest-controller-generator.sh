#!/bin/bash

# spring-rest-controller-generator.sh
#
# Purpose: Generates boilerplate code for a new Spring Boot REST Controller.
#          It creates a controller class with basic CRUD (Create, Read, Update, Delete)
#          endpoints, including placeholders for service interactions and DTO mapping.
#
# Usage:
#   ./spring-rest-controller-generator.sh [ControllerName] [BasePath] [PackageName] [OutputDir]
#   Example: ./spring-rest-controller-generator.sh Product /api/products com.example.app src/main/java
#
# Features:
#   - Generates a `@RestController` with common HTTP methods (GET, POST, PUT, DELETE).
#   - Includes placeholders for DTOs and service layer interaction.
#   - Prompts for missing arguments if not provided.
#
# Configuration:
#   - None directly in script; relies on command-line arguments or prompts.
#
# Error Handling:
#   - Checks for valid input and existing directories.
#   - Reports file creation errors.

# --- Colors for better readability ---
RED="\033[0;31m"
GREEN="\033[0;32m"
YELLOW="\033[0;33m"
BLUE="\033[0;34m"
NC="\033[0m" # No Color

# --- Helper Functions ---

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
    exit 1
}

prompt_input() {
    local prompt_text="$1"
    local default_value="$2"
    local result_var="$3"
    read -rp "${BLUE}${prompt_text}${NC} [${default_value}]: " input
    eval "$result_var=\"">${input:-${default_value}}\""
}

# --- Main Script Logic ---

log_info "Starting Spring REST Controller Generator..."

CONTROLLER_NAME="$1"
BASE_PATH="$2"
PACKAGE_NAME="$3"
OUTPUT_DIR="$4"

# Prompt for missing arguments
if [ -z "$CONTROLLER_NAME" ]; then
    prompt_input "Enter Controller Name (e.g., Product)" "Product" CONTROLLER_NAME
fi

if [ -z "$BASE_PATH" ]; then
    prompt_input "Enter Base Path (e.g., /api/products)" "/api/${CONTROLLER_NAME,,}s" BASE_PATH
fi

if [ -z "$PACKAGE_NAME" ]; then
    prompt_input "Enter Base Package Name (e.g., com.example.app)" "com.example.demo" PACKAGE_NAME
fi

if [ -z "$OUTPUT_DIR" ]; then
    prompt_input "Enter Output Directory (e.g., src/main/java)" "src/main/java" OUTPUT_DIR
fi

# Derive DTO and Service names
ENTITY_NAME="${CONTROLLER_NAME}"
DTO_NAME="${ENTITY_NAME}ResponseDto"
REQUEST_DTO_NAME="${ENTITY_NAME}RequestDto"
SERVICE_NAME="${ENTITY_NAME}Service"

# Convert package name to directory path
PACKAGE_PATH=$(echo "$PACKAGE_NAME" | tr '.' '/')
CONTROLLER_DIR="${OUTPUT_DIR}/${PACKAGE_PATH}/controller"

# Create directory if it doesn't exist
mkdir -p "$CONTROLLER_DIR" || log_error "Failed to create directory: ${CONTROLLER_DIR}"

CONTROLLER_FILE="${CONTROLLER_DIR}/${CONTROLLER_NAME}Controller.java"

log_info "Generating ${CONTROLLER_NAME}Controller.java in ${CONTROLLER_DIR}"

cat << EOF > "$CONTROLLER_FILE"
package ${PACKAGE_NAME}.controller;

import ${PACKAGE_NAME}.dto.${DTO_NAME};
import ${PACKAGE_NAME}.dto.${REQUEST_DTO_NAME};
import ${PACKAGE_NAME}.service.${SERVICE_NAME};
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("${BASE_PATH}")
public class ${CONTROLLER_NAME}Controller {

    private final ${SERVICE_NAME} ${ENTITY_NAME.toLowerCase()}Service;

    public ${CONTROLLER_NAME}Controller(${SERVICE_NAME} ${ENTITY_NAME.toLowerCase()}Service) {
        this.${ENTITY_NAME.toLowerCase()}Service = ${ENTITY_NAME.toLowerCase()}Service;
    }

    @GetMapping
    public ResponseEntity<List<${DTO_NAME}>> getAll${CONTROLLER_NAME}s() {
        List<${DTO_NAME}> dtos = ${ENTITY_NAME.toLowerCase()}Service.findAll();
        return ResponseEntity.ok(dtos);
    }

    @GetMapping("/{id}")
    public ResponseEntity<${DTO_NAME}> get${CONTROLLER_NAME}ById(@PathVariable Long id) {
        ${DTO_NAME} dto = ${ENTITY_NAME.toLowerCase()}Service.findById(id);
        return ResponseEntity.ok(dto);
    }

    @PostMapping
    public ResponseEntity<${DTO_NAME}> create${CONTROLLER_NAME}(@RequestBody ${REQUEST_DTO_NAME} requestDto) {
        ${DTO_NAME} createdDto = ${ENTITY_NAME.toLowerCase()}Service.create(requestDto);
        return new ResponseEntity<>(createdDto, HttpStatus.CREATED);
    }

    @PutMapping("/{id}")
    public ResponseEntity<${DTO_NAME}> update${CONTROLLER_NAME}(@PathVariable Long id, @RequestBody ${REQUEST_DTO_NAME} requestDto) {
        ${DTO_NAME} updatedDto = ${ENTITY_NAME.toLowerCase()}Service.update(id, requestDto);
        return ResponseEntity.ok(updatedDto);
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> delete${CONTROLLER_NAME}(@PathVariable Long id) {
        ${ENTITY_NAME.toLowerCase()}Service.delete(id);
        return ResponseEntity.noContent().build();
    }
}
EOF

if [ $? -ne 0 ]; then
    log_error "Failed to write controller file: ${CONTROLLER_FILE}"
fi

log_success "Controller ${CONTROLLER_NAME}Controller.java generated successfully!"
log_info "Remember to create the corresponding ${SERVICE_NAME}, ${DTO_NAME}, and ${REQUEST_DTO_NAME} classes."
