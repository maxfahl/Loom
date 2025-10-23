# scripts/audit-a11y.py

import argparse
import json
import os
import sys
from playwright.sync_api import sync_playwright

def run_audit(url, output_file=None, browser_name="chromium"):
    """
    Runs an accessibility audit on a given URL using axe-core via Playwright.

    Args:
        url (str): The URL to audit.
        output_file (str, optional): Path to save the JSON report. Defaults to None (prints to stdout).
        browser_name (str, optional): Browser to use ('chromium', 'firefox', 'webkit'). Defaults to 'chromium'.
    """
    print(f"Starting accessibility audit for: {url} using {browser_name}...")

    try:
        with sync_playwright() as p:
            browser = getattr(p, browser_name).launch()
            page = browser.new_page()
            page.goto(url)

            # Inject axe-core
            page.add_script_tag(url="https://unpkg.com/axe-core@4.8.4/axe.min.js")

            # Run axe-core audit
            # Documentation for axe.run(): https://www.deque.com/axe/core-documentation/api-reference/#api-name-axerun
            results = page.evaluate("() => axe.run()")

            browser.close()

            if output_file:
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(results, f, indent=2)
                print(f"Audit results saved to: {output_file}")
            else:
                print(json.dumps(results, indent=2))

            print("Accessibility audit completed.")

    except Exception as e:
        print(f"An error occurred during the audit: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description="Run an accessibility audit on a URL using axe-core via Playwright.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("url", help="The URL to audit (e.g., 'https://example.com').")
    parser.add_argument("-o", "--output", help="Optional: Path to save the JSON report (e.g., 'report.json'). If not provided, prints to stdout.")
    parser.add_argument("-b", "--browser", choices=["chromium", "firefox", "webkit"], default="chromium",
                        help="Optional: Specify browser to use. Defaults to 'chromium'.")
    parser.add_argument("--dry-run", action="store_true",
                        help="Simulate the audit process without actually running Playwright or axe-core.")

    args = parser.parse_args()

    if args.dry_run:
        print("Dry run: Accessibility audit simulation.")
        print(f"Would audit URL: {args.url}")
        print(f"Would use browser: {args.browser}")
        if args.output:
            print(f"Would save report to: {args.output}")
        sys.exit(0)

    # Check for Playwright installation
    try:
        import playwright
    except ImportError:
        print("Error: Playwright is not installed.", file=sys.stderr)
        print("Please install it using: pip install playwright", file=sys.stderr)
        print("Then install browser binaries: playwright install", file=sys.stderr)
        sys.exit(1)

    run_audit(args.url, args.output, args.browser)

if __name__ == "__main__":
    main()
