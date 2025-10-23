import argparse
import asyncio
import os
import json
from playwright.async_api import async_playwright

# playwright-auth-setup.py
#
# Purpose:
#   Automates the login process for a web application using Playwright and saves
#   the authenticated session's `storageState` to a JSON file. This file can then
#   be used by subsequent Playwright tests to start with an authenticated session,
#   bypassing the need to log in repeatedly in each test and significantly speeding
#   up test execution.
#
# Usage:
#   python playwright-auth-setup.py [--base-url <url>] [--username <user>] \
#                                   [--password <pass>] [--output <file>] \
#                                   [--headless] [--dry-run]
#
# Arguments:
#   --base-url <url>:      The base URL of the application's login page.
#                          Defaults to 'http://localhost:3000/login'.
#   --username <user>:     The username to use for login.
#                          Defaults to 'testuser'.
#   --password <pass>:     The password to use for login.
#                          Defaults to 'testpassword'.
#   --output <file>:       The path to save the storageState.json file.
#                          Defaults to 'playwright/.auth/user.json'.
#   --headless:            Run Playwright in headless mode (no browser UI).
#                          Defaults to true. Use --no-headless for headful.
#   --dry-run:             If set, the script will only show what would be done
#                          without actually launching a browser or saving state.
#
# Examples:
#   python playwright-auth-setup.py
#   python playwright-auth-setup.py --base-url https://myapp.com/login --username admin --password securepass
#   PLAYWRIGHT_AUTH_URL="http://localhost:8080/login" python playwright-auth-setup.py --output custom-auth.json --no-headless
#   python playwright-auth-setup.py --dry-run
#
# Features:
#   - Configurable login URL, credentials, and output file.
#   - Supports headless and headful browser modes.
#   - Provides clear console output with color.
#   - Includes a dry-run mode for safety.
#   - Automatically creates output directory if it doesn't exist.
#
# Prerequisites:
#   - Playwright must be installed (`pip install playwright`).
#   - Playwright browsers must be installed (`playwright install`).

class Color:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def print_color(color, message):
    print(f"{color}{message}{Color.END}")

async def main():
    parser = argparse.ArgumentParser(
        description="Automates Playwright login and saves storageState."
    )
    parser.add_argument(
        "--base-url",
        default=os.environ.get("PLAYWRIGHT_AUTH_URL", "http://localhost:3000/login"),
        help="Base URL of the application's login page (default: http://localhost:3000/login)."
    )
    parser.add_argument(
        "--username",
        default=os.environ.get("PLAYWRIGHT_AUTH_USERNAME", "testuser"),
        help="Username for login (default: testuser)."
    )
    parser.add_argument(
        "--password",
        default=os.environ.get("PLAYWRIGHT_AUTH_PASSWORD", "testpassword"),
        help="Password for login (default: testpassword)."
    )
    parser.add_argument(
        "--output",
        default=os.environ.get("PLAYWRIGHT_AUTH_OUTPUT", "playwright/.auth/user.json"),
        help="Path to save the storageState.json file (default: playwright/.auth/user.json)."
    )
    parser.add_argument(
        "--headless",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Run Playwright in headless mode (default: true). Use --no-headless for headful."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="If set, only show what would be done without actual browser interaction."
    )

    args = parser.parse_args()

    base_url = args.base_url
    username = args.username
    password = args.password
    output_file = args.output
    headless = args.headless
    dry_run = args.dry_run

    print_color(Color.BLUE, f"Starting Playwright authentication setup for: {base_url}")
    if dry_run:
        print_color(Color.YELLOW, "DRY RUN: No browser will be launched, and no state will be saved.")

    if dry_run:
        print_color(Color.YELLOW, f"Dry run: Would navigate to {base_url}")
        print_color(Color.YELLOW, f"Dry run: Would fill username '{username}' and password.")
        print_color(Color.YELLOW, "Dry run: Would click login button.")
        print_color(Color.YELLOW, f"Dry run: Would save storage state to '{output_file}'.")
        print_color(Color.BLUE, "Dry run complete.")
        return

    output_dir = os.path.dirname(output_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print_color(Color.BLUE, f"Created output directory: {output_dir}")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=headless)
        context = await browser.new_context()
        page = await context.new_page()

        try:
            print_color(Color.BLUE, f"Navigating to login page: {base_url}")
            await page.goto(base_url)

            print_color(Color.BLUE, f"Filling username: {username}")
            await page.fill('input[name="username"], input[id="username"], input[type="email"]', username)

            print_color(Color.BLUE, "Filling password...")
            await page.fill('input[name="password"], input[id="password"], input[type="password"]', password)

            print_color(Color.BLUE, "Clicking login button...")
            # Attempt to click a common login button selector
            await page.click('button[type="submit"], button:has-text("Log In"), button:has-text("Sign In")')

            # Wait for navigation after login, or for a specific element on the dashboard
            await page.wait_for_url(lambda url: url != base_url, timeout=10000) # Wait for URL change
            # Alternatively, wait for a dashboard element:
            # await page.wait_for_selector('#dashboard-welcome', timeout=10000)

            print_color(Color.GREEN, "Login successful. Saving storage state...")
            await context.storage_state(path=output_file)
            print_color(Color.GREEN, f"Storage state saved to: {output_file}")

        except Exception as e:
            print_color(Color.RED, f"An error occurred during login or state saving: {e}")
            # Optionally save a screenshot on failure
            await page.screenshot(path="playwright-auth-failure.png")
            print_color(Color.RED, "Screenshot 'playwright-auth-failure.png' saved for debugging.")
            import sys
            sys.exit(1)
        finally:
            await browser.close()
            print_color(Color.BLUE, "Browser closed.")

if __name__ == "__main__":
    asyncio.run(main())
