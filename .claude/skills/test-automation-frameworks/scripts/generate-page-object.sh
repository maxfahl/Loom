#!/bin/bash

# generate-page-object.sh
#
# Description:
#   This script scaffolds a new TypeScript Page Object file for Playwright or Selenium.
#   It creates a basic class structure with a constructor and a placeholder for selectors/methods,
#   following the Page Object Model (POM) best practice.
#
# Usage:
#   ./generate-page-object.sh <framework> <page-name> [output-dir]
#
# Arguments:
#   <framework>  : The test automation framework (playwright or selenium).
#   <page-name>  : The name of the page object (e.g., LoginPage, DashboardPage).
#   [output-dir] : Optional. The directory where the page object file will be created.
#                  Defaults to 'playwright-typescript/pages' or 'selenium-typescript/pages'
#                  based on the framework.
#
# Examples:
#   ./generate-page-object.sh playwright LoginPage
#   ./generate-page-object.sh selenium ProductPage ./src/e2e/pages
#
# Features:
#   - Supports Playwright and Selenium frameworks.
#   - Generates a TypeScript class with a constructor.
#   - Includes basic imports and a placeholder for elements and methods.
#   - Provides clear usage instructions and error handling.
#   - Allows specifying an output directory.
#
# Error Handling:
#   - Exits if required arguments are missing.
#   - Warns if the output directory does not exist.
#   - Prevents overwriting existing files unless forced (not implemented for simplicity).

set -euo pipefail

# --- Configuration ---
DEFAULT_PLAYWRIGHT_DIR="playwright-typescript/pages"
DEFAULT_SELENIUM_DIR="selenium-typescript/pages"

# --- Functions ---

# Displays help message
show_help() {
  echo "Usage: $0 <framework> <page-name> [output-dir]"
  echo ""
  echo "Arguments:"
  echo "  <framework>  : The test automation framework (playwright or selenium)."
  echo "  <page-name>  : The name of the page object (e.g., LoginPage, DashboardPage)."
  echo "  [output-dir] : Optional. The directory where the page object file will be created."
  echo "                 Defaults to 'playwright-typescript/pages' or 'selenium-typescript/pages'."
  echo ""
  echo "Examples:"
  echo "  $0 playwright LoginPage"
  echo "  $0 selenium ProductPage ./src/e2e/pages"
  echo ""
  echo "Description:"
  echo "  This script scaffolds a new TypeScript Page Object file for Playwright or Selenium."
  echo "  It creates a basic class structure with a constructor and a placeholder for selectors/methods."
}

# Generates Playwright Page Object content
generate_playwright_content() {
  local page_name=$1
  cat <<EOF
import { Page, Locator } from '@playwright/test';

export class ${page_name} {
  readonly page: Page;

  constructor(page: Page) {
    this.page = page;
  }

  // --- Selectors ---
  // Example:
  // get someElement(): Locator {
  //   return this.page.locator('[data-testid="some-element"]');
  // }

  // --- Actions ---
  // Example:
  // async navigateTo(): Promise<void> {
  //   await this.page.goto('/${page_name.toLowerCase().replace('page', '')}');
  // }
  //
  // async clickSomeElement(): Promise<void> {
  //   await this.someElement.click();
  // }
}
EOF
}

# Generates Selenium Page Object content
generate_selenium_content() {
  local page_name=$1
  cat <<EOF
import { WebDriver, By, WebElement } from 'selenium-webdriver';

export class ${page_name} {
  readonly driver: WebDriver;

  constructor(driver: WebDriver) {
    this.driver = driver;
  }

  // --- Selectors ---
  // Example:
  // async getSomeElement(): Promise<WebElement> {
  //   return this.driver.findElement(By.css('[data-testid="some-element"]'));
  // }

  // --- Actions ---
  // Example:
  // async navigateTo(): Promise<void> {
  //   await this.driver.get('http://localhost:3000/${page_name.toLowerCase().replace('page', '')}');
  // }
  //
  // async clickSomeElement(): Promise<void> {
  //   const element = await this.getSomeElement();
  //   await element.click();
  // }
}
EOF
}

# --- Main Logic ---

# Check for help flag
if [[ "$#" -gt 0 && ("$1" == "-h" || "$1" == "--help") ]]; then
  show_help
  exit 0
fi

# Validate arguments
if [ "$#" -lt 2 ]; then
  echo "Error: Missing required arguments."
  show_help
  exit 1
fi

FRAMEWORK=$1
PAGE_NAME=$2
OUTPUT_DIR=${3:-} # Optional third argument

# Determine default output directory if not provided
if [ -z "$OUTPUT_DIR" ]; then
  case "$FRAMEWORK" in
    playwright)
      OUTPUT_DIR="${DEFAULT_PLAYWRIGHT_DIR}"
      ;;
    selenium)
      OUTPUT_DIR="${DEFAULT_SELENIUM_DIR}"
      ;;
    *)
      echo "Error: Invalid framework specified. Must be 'playwright' or 'selenium'."
      show_help
      exit 1
      ;;
  esac
fi

# Ensure output directory exists
if [ ! -d "$OUTPUT_DIR" ]; then
  echo "Warning: Output directory '$OUTPUT_DIR' does not exist. Creating it."
  mkdir -p "$OUTPUT_DIR"
fi

FILE_NAME="${PAGE_NAME}.page.ts"
FILE_PATH="${OUTPUT_DIR}/${FILE_NAME}"

# Check if file already exists
if [ -f "$FILE_PATH" ]; then
  echo "Error: File '$FILE_PATH' already exists. Aborting to prevent overwrite."
  exit 1
fi

echo "Generating Page Object for ${FRAMEWORK}..."
echo "  Page Name: ${PAGE_NAME}"
echo "  Output Dir: ${OUTPUT_DIR}"
echo "  File Path: ${FILE_PATH}"

# Generate content based on framework
case "$FRAMEWORK" in
  playwright)
    generate_playwright_content "$PAGE_NAME" > "$FILE_PATH"
    ;;
  selenium)
    generate_selenium_content "$PAGE_NAME" > "$FILE_PATH"
    ;;
  *)
    # This case should ideally be caught earlier, but as a fallback
    echo "Error: Invalid framework specified. Must be 'playwright' or 'selenium'."
    show_help
    exit 1
    ;;
esac

echo "Successfully created Page Object: '$FILE_PATH'"
echo "Remember to update the selectors and actions within the file."
