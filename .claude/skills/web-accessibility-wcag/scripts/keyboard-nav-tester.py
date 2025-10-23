# scripts/keyboard-nav-tester.py

import argparse
import json
import sys
from playwright.sync_api import sync_playwright

def run_keyboard_test(url, output_file=None, browser_name="chromium"):
    """
    Simulates keyboard navigation on a given URL and reports focusable elements.

    Args:
        url (str): The URL to test.
        output_file (str, optional): Path to save the JSON report. Defaults to None (prints to stdout).
        browser_name (str, optional): Browser to use ('chromium', 'firefox', 'webkit'). Defaults to 'chromium'.
    """
    print(f"Starting keyboard navigation test for: {url} using {browser_name}...")

    try:
        with sync_playwright() as p:
            browser = getattr(p, browser_name).launch()
            page = browser.new_page()
            page.goto(url)

            focusable_elements = []
            
            # Get all focusable elements initially
            initial_elements = page.evaluate('''() => {
                return Array.from(document.querySelectorAll(
                    'a[href], area[href], input:not([disabled]), select:not([disabled]), textarea:not([disabled]), button:not([disabled]), iframe, object, embed, *[tabindex], *[contenteditable]'
                )).filter(el => el.offsetWidth > 0 || el.offsetHeight > 0 || el.getClientRects().length > 0)
                .map(el => ({
                    tagName: el.tagName,
                    id: el.id,
                    className: el.className,
                    text: el.textContent.trim().substring(0, 100),
                    role: el.getAttribute('role'),
                    tabIndex: el.tabIndex,
                    isInitiallyFocusable: true
                }));
            }''')
            focusable_elements.extend(initial_elements)

            # Simulate Tab key presses
            for i in range(len(initial_elements) * 2): # Tab through elements twice to catch cycles
                page.keyboard.press('Tab')
                focused_element = page.evaluate('''() => {
                    const el = document.activeElement;
                    if (el) {
                        return {
                            tagName: el.tagName,
                            id: el.id,
                            className: el.className,
                            text: el.textContent.trim().substring(0, 100),
                            role: el.getAttribute('role'),
                            tabIndex: el.tabIndex,
                            isInitiallyFocusable: false // Mark as found via tab
                        };
                    }
                    return null;
                }''')
                if focused_element and focused_element not in focusable_elements:
                    focusable_elements.append(focused_element)
                
                # Check if we've looped back to the start or a common element
                if i > len(initial_elements) and focused_element == focusable_elements[0]:
                    print("Detected loop in tab order, stopping.")
                    break


            browser.close()

            report = {
                "url": url,
                "focusable_elements_count": len(focusable_elements),
                "focusable_elements": focusable_elements
            }

            if output_file:
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(report, f, indent=2)
                print(f"Keyboard navigation report saved to: {output_file}")
            else:
                print(json.dumps(report, indent=2))

            print("Keyboard navigation test completed.")

    except Exception as e:
        print(f"An error occurred during the test: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description="Simulate keyboard navigation on a URL and report focusable elements.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("url", help="The URL to test (e.g., 'https://example.com').")
    parser.add_argument("-o", "--output", help="Optional: Path to save the JSON report (e.g., 'keyboard_report.json'). If not provided, prints to stdout.")
    parser.add_argument("-b", "--browser", choices=["chromium", "firefox", "webkit"], default="chromium",
                        help="Optional: Specify browser to use. Defaults to 'chromium'.")
    parser.add_argument("--dry-run", action="store_true",
                        help="Simulate the test process without actually running Playwright.")

    args = parser.parse_args()

    if args.dry_run:
        print("Dry run: Keyboard navigation test simulation.")
        print(f"Would test URL: {args.url}")
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

    run_keyboard_test(args.url, args.output, args.browser)

if __name__ == "__main__":
    main()
