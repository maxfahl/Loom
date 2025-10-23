#!/bin/bash

# generate-api-test-boilerplate.sh
#
# Purpose:
#   Generates a new Supertest API test file with boilerplate code for a given API endpoint.
#   This script helps developers quickly scaffold new integration tests, saving time
#   on repetitive setup tasks like imports, describe blocks, and a basic GET test.
#
# Usage:
#   ./generate-api-test-boilerplate.sh <endpoint_path> [output_dir]
#
# Arguments:
#   <endpoint_path>: The API endpoint path (e.g., "/users", "/products/:id").
#                    This will be used to name the test file and generate basic test descriptions.
#   [output_dir]:    Optional. The directory where the test file will be created.
#                    Defaults to "src/__tests__/api" if not provided.
#
# Examples:
#   ./generate-api-test-boilerplate.sh /users
#   ./generate-api-test-boilerplate.sh /products/:id tests/integration
#
# Features:
#   - Creates a new TypeScript test file.
#   - Includes Supertest and Jest imports.
#   - Sets up a basic 'describe' block.
#   - Adds a placeholder GET test case.
#   - Provides clear comments and usage instructions.
#   - Handles existing file conflicts.
#   - Configurable output directory.

set -euo pipefail

# --- Configuration ---
DEFAULT_OUTPUT_DIR="src/__tests__/api"
TEST_FILE_EXTENSION=".test.ts"

# --- Helper Functions ---

# Function to display script usage
usage() {
  echo "Usage: $0 <endpoint_path> [output_dir]"
  echo ""
  echo "Arguments:"
  echo "  <endpoint_path>: The API endpoint path (e.g., \"/users\", \"/products/:id\")."
  echo "                   Used to name the test file and generate basic test descriptions."
  echo "  [output_dir]:    Optional. The directory where the test file will be created."
  echo "                   Defaults to \"${DEFAULT_OUTPUT_DIR}\" if not provided."
  echo ""
  echo "Examples:"
  echo "  $0 /users"
  echo "  $0 /products/:id tests/integration"
  exit 1
}

# Function to print messages in color
print_color() {
  local color="$1"
  local message="$2"
  case "$color" in
    "red")    echo -e "\033[0;31m${message}\033[0m" ;;
    "green")  echo -e "\033[0;32m${message}\033[0m" ;;
    "yellow") echo -e "\033[0;33m${message}\033[0m" ;;
    "blue")   echo -e "\033[0;34m${message}\033[0m" ;;
    *)        echo "${message}" ;;
  esac
}

# --- Main Script Logic ---

# Check for required arguments
if [[ $# -lt 1 ]]; then
  usage
fi

ENDPOINT_PATH="$1"
OUTPUT_DIR="${2:-${DEFAULT_OUTPUT_DIR}}"

# Sanitize endpoint path for filename
FILENAME_BASE=$(echo "${ENDPOINT_PATH}" | sed -e 's/^\///' -e 's/:id//' -e 's/\//-/g' -e 's/--/-/g' -e 's/^-//' -e 's/-$//')
if [[ -z "${FILENAME_BASE}" ]]; then
  FILENAME_BASE="root"
fi
TEST_FILE_NAME="${FILENAME_BASE}${TEST_FILE_EXTENSION}"
FULL_PATH="${OUTPUT_DIR}/${TEST_FILE_NAME}"

print_color "blue" "Generating boilerplate for endpoint: ${ENDPOINT_PATH}"
print_color "blue" "Output directory: ${OUTPUT_DIR}"
print_color "blue" "Test file name: ${TEST_FILE_NAME}"

# Create output directory if it doesn't exist
mkdir -p "${OUTPUT_DIR}" || { print_color "red" "Error: Could not create directory ${OUTPUT_DIR}"; exit 1; }

# Check if file already exists
if [[ -f "${FULL_PATH}" ]]; then
  print_color "yellow" "Warning: File '${FULL_PATH}' already exists."
  read -rp "Do you want to overwrite it? (y/N): " OVERWRITE_CHOICE
  if [[ ! "${OVERWRITE_CHOICE}" =~ ^[Yy]$ ]]; then
    print_color "blue" "Operation cancelled."
    exit 0
  fi
fi

# Generate file content
cat << EOF > "${FULL_PATH}"
import request from 'supertest';
import app from '../../src/app'; // Adjust path to your Express app as needed

describe('API - ${ENDPOINT_PATH}', () => {
  // --- Setup/Teardown Hooks ---
  // Example: Clear database before each test if using an ORM like Mongoose
  // beforeEach(async () => {
  //   await mongoose.connection.dropDatabase();
  //   await mongoose.connection.createCollection('users'); // Recreate necessary collections
  // });

  // Example: Connect to test database once before all tests
  // beforeAll(async () => {
  //   await connectToTestDb();
  // });

  // Example: Disconnect from test database once after all tests
  // afterAll(async () => {
  //   await disconnectFromTestDb();
  // });

  // --- Test Cases ---

  it('should return 200 OK for GET ${ENDPOINT_PATH}', async () => {
    const res = await request(app).get('${ENDPOINT_PATH}');
    expect(res.statusCode).toBe(200);
    // Add more specific assertions here, e.g.:
    // expect(res.body).toBeInstanceOf(Array);
    // expect(res.body.length).toBeGreaterThan(0);
  });

  // Example: Test POST request
  // it('should create a new resource via POST ${ENDPOINT_PATH}', async () => {
  //   const newResource = { name: 'Test Item', value: 123 };
  //   const res = await request(app)
  //     .post('${ENDPOINT_PATH}')
  //     .send(newResource)
  //     .set('Accept', 'application/json');
  //
  //   expect(res.statusCode).toBe(201); // Created
  //   expect(res.body.name).toBe(newResource.name);
  //   expect(res.body).toHaveProperty('id');
  // });

  // Example: Test authenticated GET request
  // it('should return 200 OK for authenticated GET ${ENDPOINT_PATH}', async () => {
  //   const authToken = 'YOUR_AUTH_TOKEN'; // Obtain this from a login test or mock
  //   const res = await request(app)
  //     .get('${ENDPOINT_PATH}')
  //     .set('Authorization', `Bearer ${authToken}`);
  //
  //   expect(res.statusCode).toBe(200);
  // });

  // Example: Test error handling (e.g., 404 Not Found)
  // it('should return 404 Not Found for a non-existent resource', async () => {
  //   const nonExistentId = 'nonexistent123';
  //   const res = await request(app).get('${ENDPOINT_PATH}/${nonExistentId}');
  //   expect(res.statusCode).toBe(404);
  //   expect(res.body).toHaveProperty('message', 'Resource not found');
  // });
});
EOF

print_color "green" "Successfully created test file: '${FULL_PATH}'"
print_color "green" "Remember to adjust the path to your Express app (e.g., '../../src/app') and add specific assertions."
print_color "green" "Don't forget to configure your test environment (e.g., database setup/teardown)."
