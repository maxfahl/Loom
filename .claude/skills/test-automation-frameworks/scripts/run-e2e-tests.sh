#!/bin/bash

# run-e2e-tests.sh
#
# Description:
#   This script executes end-to-end (E2E) tests using Playwright or Selenium WebDriver.
#   It provides options for selecting the framework, browser, parallelization, and reporting.
#   Designed to be flexible for both local development and CI/CD environments.
#
# Usage:
#   ./run-e2e-tests.sh [options]
#
# Options:
#   -f, --framework <name> : Specify the test framework (playwright or selenium). Default: playwright.
#   -b, --browser <name>   : Specify the browser to run tests on (e.g., chromium, firefox, webkit for Playwright;
#                            chrome, firefox for Selenium). Default: chromium/chrome.
#   -p, --parallel <num>   : Number of parallel workers/threads. Default: 1 (Playwright) or sequential (Selenium).
#   -t, --tag <tag_name>   : Run tests with a specific tag (Playwright only, e.g., @smoke, @regression).
#   -r, --reporter <type>  : Specify the reporter (e.g., html, list, json for Playwright; spec, allure for Selenium).
#   -h, --help             : Show this help message and exit.
#
# Environment Variables:
#   BASE_URL               : The base URL for the application under test (e.g., http://localhost:3000).
#                            If not set, tests might use a default from their config or fail.
#   CI                     : Set to 'true' in CI environments to enable CI-specific configurations.
#
# Examples:
#   ./run-e2e-tests.sh
#   ./run-e2e-tests.sh --framework playwright --browser firefox --parallel 3
#   ./run-e2e-tests.sh -f selenium -b chrome -r allure
#   BASE_URL=https://staging.example.com ./run-e2e-tests.sh -f playwright -t @smoke
#
# Dependencies:
#   - Node.js and Playwright (for Playwright framework)
#   - Node.js/Python/Java and Selenium WebDriver (for Selenium framework)
#   - Appropriate browser drivers (e.g., chromedriver for Selenium Chrome)

set -euo pipefail

# --- Configuration Defaults ---
FRAMEWORK="playwright"
BROWSER=""
PARALLEL_WORKERS=""
TAG=""
REPORTER=""

# --- Functions ---

# Displays help message
show_help() {
  echo "Usage: $0 [options]"
  echo ""
  echo "Options:"
  echo "  -f, --framework <name> : Specify the test framework (playwright or selenium). Default: ${FRAMEWORK}."
  echo "  -b, --browser <name>   : Specify the browser to run tests on (e.g., chromium, firefox, webkit for Playwright;"
  echo "                           chrome, firefox for Selenium). Default: chromium/chrome."
  echo "  -p, --parallel <num>   : Number of parallel workers/threads. Default: 1 (Playwright) or sequential (Selenium)."
  echo "  -t, --tag <tag_name>   : Run tests with a specific tag (Playwright only, e.g., @smoke, @regression)."
  echo "  -r, --reporter <type>  : Specify the reporter (e.g., html, list, json for Playwright; spec, allure for Selenium)."
  echo "  -h, --help             : Show this help message and exit."
  echo ""
  echo "Environment Variables:"
  echo "  BASE_URL               : The base URL for the application under test (e.g., http://localhost:3000)."
  echo "                           If not set, tests might use a default from their config or fail."
  echo "  CI                     : Set to 'true' in CI environments to enable CI-specific configurations."
}

# --- Argument Parsing ---
while [[ $# -gt 0 ]]; do
  key="$1"
  case $key in
    -f|--framework)
      FRAMEWORK="$2"
      shift # past argument
      shift # past value
      ;;
    -b|--browser)
      BROWSER="$2"
      shift # past argument
      shift # past value
      ;;
    -p|--parallel)
      PARALLEL_WORKERS="$2"
      shift # past argument
      shift # past value
      ;;
    -t|--tag)
      TAG="$2"
      shift # past argument
      shift # past value
      ;;
    -r|--reporter)
      REPORTER="$2"
      shift # past argument
      shift # past value
      ;;
    -h|--help)
      show_help
      exit 0
      ;;
    *)
      echo "Unknown option: $1"
      show_help
      exit 1
      ;;
  esac
done

# --- Execute Tests ---

echo "Running E2E tests with ${FRAMEWORK} framework..."

if [ -n "${BASE_URL}" ]; then
  echo "  Base URL: ${BASE_URL}"
fi

case "${FRAMEWORK}" in
  playwright)
    # Default browser for Playwright if not specified
    if [ -z "${BROWSER}" ]; then
      BROWSER="chromium"
    fi

    PLAYWRIGHT_CMD="npx playwright test"

    PLAYWRIGHT_CMD+=" --project=${BROWSER}"

    if [ -n "${PARALLEL_WORKERS}" ]; then
      PLAYWRIGHT_CMD+=" -j ${PARALLEL_WORKERS}"
    fi

    if [ -n "${TAG}" ]; then
      PLAYWRIGHT_CMD+=" --grep \"@${TAG}\""
    fi

    if [ -n "${REPORTER}" ]; then
      PLAYWRIGHT_CMD+=" --reporter=${REPORTER}"
    fi

    echo "Executing: ${PLAYWRIGHT_CMD}"
    eval "${PLAYWRIGHT_CMD}"
    ;;
  selenium)
    # Default browser for Selenium if not specified
    if [ -z "${BROWSER}" ]; then
      BROWSER="chrome"
    fi

    # Note: Selenium test execution is highly dependent on the project setup (e.g., Java, Python, JS with Mocha/Jest)
    # This example assumes a Node.js/TypeScript setup using a test runner like Mocha or Jest
    # and a custom script to handle Selenium WebDriver initialization and test execution.
    # You would typically have a `selenium-tests.js` or `selenium-tests.ts` that uses `selenium-webdriver`.
    # For simplicity, we'll assume a generic `npm run test:selenium` command that can be configured.

    SELENIUM_CMD="npm run test:selenium --"

    # Pass browser and reporter as environment variables or arguments if the underlying script supports it
    if [ -n "${BROWSER}" ]; then
      SELENIUM_CMD+=" --browser=${BROWSER}"
    fi

    if [ -n "${REPORTER}" ]; then
      SELENIUM_CMD+=" --reporter=${REPORTER}"
    fi

    # Parallel execution for Selenium is more complex and depends on the test runner and grid setup.
    # This script won't directly manage Selenium Grid, but the underlying `npm run test:selenium` could.
    if [ -n "${PARALLEL_WORKERS}" ]; then
      echo "Warning: Parallel execution for Selenium is highly dependent on your test runner and grid setup."
      echo "         The '--parallel' option might not be directly supported by this generic Selenium command."
      SELENIUM_CMD+=" --parallel=${PARALLEL_WORKERS}" # Pass it through, but might not be used
    fi

    echo "Executing: ${SELENIUM_CMD}"
    eval "${SELENIUM_CMD}"
    ;;
  *)
    echo "Error: Invalid framework specified. Must be 'playwright' or 'selenium'."
    show_help
    exit 1
    ;;
esac

echo "E2E test execution completed."
