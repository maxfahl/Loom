#!/bin/bash

# generate-playwright-page-object.sh
#
# Purpose:
#   Generates a new Playwright Page Object Model (POM) file with boilerplate code.
#   This script helps developers quickly scaffold new page objects, including basic
#   structure, common locators, and interaction methods, promoting maintainability
#   and reducing code duplication in E2E tests.
#
# Usage:
#   ./generate-playwright-page-object.sh <page_name> [output_dir]
#
# Arguments:
#   <page_name>:   The name of the page object (e.g., "LoginPage", "DashboardPage").
#                  This will be used to name the file and the class.
#   [output_dir]:  Optional. The directory where the page object file will be created.
#                  Defaults to "tests/pages" if not provided.
#
# Examples:
#   ./generate-playwright-page-object.sh LoginPage
#   ./generate-playwright-page-object.sh ProductPage e2e/page-objects
#
# Features:
#   - Creates a new TypeScript page object file.
#   - Includes Playwright Page import.
#   - Sets up a basic class structure with a constructor.
#   - Adds example locators and interaction methods.
#   - Provides clear comments and usage instructions.
#   - Handles existing file conflicts.
#   - Configurable output directory.

set -euo pipefail

# --- Configuration ---
DEFAULT_OUTPUT_DIR="tests/pages"
PAGE_FILE_EXTENSION=".ts"

# --- Helper Functions ---

# Function to display script usage
usage() {
  echo "Usage: $0 <page_name> [output_dir]"
  echo ""
  echo "Arguments:"
  echo "  <page_name>:   The name of the page object (e.g., \"LoginPage\", \"DashboardPage\")."
  echo "                 Used to name the file and the class."
  echo "  [output_dir]:  Optional. The directory where the page object file will be created."
  echo "                 Defaults to \"${DEFAULT_OUTPUT_DIR}\" if not provided."
  echo ""
  echo "Examples:"
  echo "  $0 LoginPage"
  echo "  $0 ProductPage e2e/page-objects"
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

PAGE_NAME="$1"
OUTPUT_DIR="${2:-${DEFAULT_OUTPUT_DIR}}"

PAGE_CLASS_NAME="${PAGE_NAME}"
PAGE_FILE_NAME="${PAGE_NAME}${PAGE_FILE_EXTENSION}"
FULL_PATH="${OUTPUT_DIR}/${PAGE_FILE_NAME}"

print_color "blue" "Generating Playwright Page Object: ${PAGE_CLASS_NAME}"
print_color "blue" "Output directory: ${OUTPUT_DIR}"
print_color "blue" "Page object file name: ${PAGE_FILE_NAME}"

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
import { Locator, Page, expect } from '@playwright/test';

export class ${PAGE_CLASS_NAME} {
  readonly page: Page;

  // --- Locators ---
  // Example: page.getByRole('heading', { name: 'Welcome' })
  readonly welcomeHeading: Locator;
  // Example: page.getByLabel('Username')
  readonly usernameInput: Locator;
  // Example: page.getByRole('button', { name: 'Submit' })
  readonly submitButton: Locator;

  constructor(page: Page) {
    this.page = page;
    this.welcomeHeading = page.getByRole('heading', { name: 'Welcome' });
    this.usernameInput = page.getByLabel('Username');
    this.submitButton = page.getByRole('button', { name: 'Submit' });
  }

  // --- Actions ---

  /**
   * Navigates to the ${PAGE_NAME} page.
   */
  async goto() {
    await this.page.goto('/'); // Adjust URL as needed
  }

  /**
   * Fills the username input field.
   * @param username The username to enter.
   */
  async fillUsername(username: string) {
    await this.usernameInput.fill(username);
  }

  /**
   * Clicks the submit button.
   */
  async clickSubmitButton() {
    await this.submitButton.click();
  }

  // --- Assertions (can also be in test files) ---

  /**
   * Asserts that the welcome heading is visible.
   */
  async expectWelcomeHeadingVisible() {
    await expect(this.welcomeHeading).toBeVisible();
  }

  /**
   * Asserts that the current page URL matches the expected URL for this page.
   * @param expectedUrl The expected URL suffix (e.g., '/dashboard').
   */
  async expectOnPage(expectedUrl: string) {
    await expect(this.page).toHaveURL(new RegExp(`${expectedUrl}$`));
  }
}
EOF

print_color "green" "Successfully created Playwright Page Object: '${FULL_PATH}'"
print_color "green" "Remember to adjust locators, methods, and the goto() URL as per your application's structure."
