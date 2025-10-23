#!/usr/bin/env python3
"""
a11y-audit.py: Automated Accessibility Auditor

This script performs automated accessibility audits on web pages using Playwright and axe-core.
It can audit a live URL or a local HTML file, generating a JSON report of violations
and an optional human-readable summary.

Dependencies:
  - playwright: `pip install playwright`
  - axe-playwright: `pip install axe-playwright`
  - You also need to install browser binaries: `playwright install`

Usage:
  python a11y-audit.py --url <URL> [--output-json <FILE>] [--output-summary] [--rules <RULE1,RULE2>] [--exclude-rules <RULE1,RULE2>]
  python a11y-audit.py --file <PATH_TO_HTML> [--output-json <FILE>] [--output-summary]

Examples:
  # Audit a live URL and print a summary
  python a11y-audit.py --url https://www.google.com --output-summary

  # Audit a local HTML file and save a JSON report
  python a11y-audit.py --file ./index.html --output-json a11y-report.json

  # Audit a URL, save JSON, and exclude specific rules
  python a11y-audit.py --url https://example.com --output-json report.json --exclude-rules color-contrast,aria-hidden-focus

  # Audit a URL, save JSON, and include only specific rules
  python a11y-audit.py --url https://example.com --output-json report.json --rules wcag2a,wcag21a
"""

import argparse
import json
import sys
from playwright.sync_api import sync_playwright
from axe_playwright import Axe

def run_audit(page, axe_options):
    """Runs the axe-core accessibility audit on the given page."""
    axe = Axe()
    results = axe.run(page, options=axe_options)
    return results

def format_summary(violations):
    """Formats a human-readable summary of accessibility violations."""
    if not violations:
        return "No accessibility violations found. Great job!"

    summary = ["Accessibility Violations Found:"]
    for i, violation in enumerate(violations):
        summary.append(f"  {i + 1}. {violation['help']} (ID: {violation['id']})")
        summary.append(f"     Impact: {violation['impact']}")
        summary.append(f"     Description: {violation['description']}")
        summary.append(f"     Help URL: {violation['helpUrl']}")
        if violation['nodes']:
            summary.append("     Affected Elements:")
            for node in violation['nodes']:
                summary.append(f"       - Selector: {node['target'][0]}")
                summary.append(f"         HTML: {node['html']}")
                if node['failureSummary']:
                    summary.append(f"         Failure Summary: {node['failureSummary']}")
        summary.append("-" * 40)
    return "\n".join(summary)

def main():
    parser = argparse.ArgumentParser(
        description="Automated Accessibility Auditor using Playwright and axe-core.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--url", help="URL to audit (e.g., https://example.com)")
    group.add_argument("--file", help="Path to a local HTML file to audit (e.g., ./index.html)")

    parser.add_argument("--output-json", help="Path to save the full JSON report of violations.")
    parser.add_argument("--output-summary", action="store_true",
                        help="Print a human-readable summary of violations to stdout.")
    parser.add_argument("--rules", help="Comma-separated list of axe-core rules to include (e.g., wcag2a,best-practices).")
    parser.add_argument("--exclude-rules", help="Comma-separated list of axe-core rules to exclude (e.g., color-contrast,aria-hidden-focus).")

    args = parser.parse_args()

    axe_options = {}
    if args.rules:
        axe_options["runOnly"] = {"type": "rules", "values": args.rules.split(',')}
    if args.exclude_rules:
        if "runOnly" in axe_options:
            print("Error: Cannot use both --rules and --exclude-rules simultaneously.", file=sys.stderr)
            sys.exit(1)
        axe_options["rules"] = {rule: {"enabled": False} for rule in args.exclude_rules.split(',')}

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        try:
            if args.url:
                print(f"Navigating to URL: {args.url}")
                page.goto(args.url)
            elif args.file:
                file_path = f"file://{args.file}"
                print(f"Navigating to local file: {file_path}")
                page.goto(file_path)

            print("Running accessibility audit...")
            audit_results = run_audit(page, axe_options)
            violations = audit_results["violations"]

            if args.output_json:
                with open(args.output_json, "w", encoding="utf-8") as f:
                    json.dump(audit_results, f, indent=2, ensure_ascii=False)
                print(f"Full JSON report saved to: {args.output_json}")

            if args.output_summary:
                print("\n" + format_summary(violations))

            if violations:
                print(f"Accessibility audit completed with {len(violations)} violations.")
                sys.exit(len(violations)) # Exit with number of violations
            else:
                print("Accessibility audit completed. No violations found.")
                sys.exit(0)

        except Exception as e:
            print(f"An error occurred during the audit: {e}", file=sys.stderr)
            sys.exit(1)
        finally:
            browser.close()

if __name__ == "__main__":
    main()
