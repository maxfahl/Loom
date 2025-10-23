
#!/usr/bin/env python3

"""
web_perf_audit.py

Automates running Google Lighthouse audits for specified URLs and generates a
summary report in Markdown format. This script helps developers quickly assess
web performance metrics, especially Core Web Vitals, across multiple pages.

Usage:
  python3 web_perf_audit.py -u <URL1> <URL2> ... [-o <OUTPUT_DIR>] [--dry-run] [--help]

Examples:
  python3 web_perf_audit.py -u https://example.com https://example.com/about
  python3 web_perf_audit.py -u https://example.com -o reports --dry-run
  python3 web_perf_audit.py -u https://example.com --output-format json # To get raw JSON output

Requirements:
  - Node.js and npm installed.
  - Lighthouse CLI installed globally: `npm install -g lighthouse`
"""

import argparse
import subprocess
import json
import os
import sys
from datetime import datetime

# --- Configuration ---
LIGHTHOUSE_CLI = "lighthouse"
DEFAULT_OUTPUT_DIR = "lighthouse_reports"
REPORT_FILENAME_PREFIX = "lighthouse_report"
SUMMARY_FILENAME = "performance_summary.md"

# --- Helper Functions ---

def run_command(command, dry_run=False, capture_output=True, text=True, check=True):
    """Runs a shell command."""
    if dry_run:
        print(f"DRY RUN: Would execute: {' '.join(command)}")
        return subprocess.CompletedProcess(command, 0, stdout="", stderr="")
    try:
        result = subprocess.run(
            command,
            capture_output=capture_output,
            text=text,
            check=check,
            encoding='utf-8',
            errors='ignore'
        )
        return result
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {' '.join(command)}", file=sys.stderr)
        print(f"Stdout: {e.stdout}", file=sys.stderr)
        print(f"Stderr: {e.stderr}", file=sys.stderr)
        raise
    except FileNotFoundError:
        print(f"Error: Command '{command[0]}' not found. "
              "Please ensure Lighthouse CLI is installed and in your PATH.", file=sys.stderr)
        sys.exit(1)

def get_lighthouse_report(url, output_dir, dry_run=False):
    """Runs Lighthouse for a given URL and returns the JSON report path."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = os.path.join(output_dir, f"{REPORT_FILENAME_PREFIX}_{url.replace('://', '_').replace('/', '_')}_{timestamp}.json")
    
    command = [
        LIGHTHOUSE_CLI,
        url,
        "--output=json",
        f"--output-path={report_path}",
        "--chrome-flags='--headless --no-sandbox'",
        "--quiet"
    ]
    
    print(f"Running Lighthouse for {url}...")
    try:
        run_command(command, dry_run=dry_run)
        if not dry_run and os.path.exists(report_path):
            print(f"Lighthouse report saved to {report_path}")
            return report_path
        elif dry_run:
            print(f"Dry run: Lighthouse report would be saved to {report_path}")
            return None
    except Exception as e:
        print(f"Failed to run Lighthouse for {url}: {e}", file=sys.stderr)
        return None
    return None

def parse_lighthouse_report(report_path):
    """Parses a Lighthouse JSON report and extracts key metrics."""
    if not report_path or not os.path.exists(report_path):
        return None
    
    with open(report_path, 'r', encoding='utf-8') as f:
        report = json.load(f)
    
    audits = report.get('audits', {})
    metrics = {
        "url": report.get('finalUrl', 'N/A'),
        "performance_score": round(report.get('categories', {}).get('performance', {}).get('score', 0) * 100),
        "LCP": audits.get('largest-contentful-paint', {}).get('displayValue', 'N/A'),
        "CLS": audits.get('cumulative-layout-shift', {}).get('displayValue', 'N/A'),
        "INP": audits.get('interaction-to-next-paint', {}).get('displayValue', 'N/A'),
        "FCP": audits.get('first-contentful-paint', {}).get('displayValue', 'N/A'),
        "TBT": audits.get('total-blocking-time', {}).get('displayValue', 'N/A'),
    }
    return metrics

def generate_markdown_summary(all_metrics, output_dir):
    """Generates a Markdown summary of all Lighthouse audits."""
    summary_path = os.path.join(output_dir, SUMMARY_FILENAME)
    
    with open(summary_path, 'w', encoding='utf-8') as f:
        f.write(f"# Web Performance Audit Summary - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

")
        f.write("This report summarizes the Google Lighthouse performance audits for the specified URLs.

")
        f.write("## Key Metrics Explained:
")
        f.write("- **Performance Score:** Overall performance score (0-100).
")
        f.write("- **LCP (Largest Contentful Paint):** Time to render the largest visible content element.
")
        f.write("- **CLS (Cumulative Layout Shift):** Measures visual stability.
")
        f.write("- **INP (Interaction to Next Paint):** Measures page responsiveness to user interactions.
")
        f.write("- **FCP (First Contentful Paint):** Time to render the first pixel of content.
")
        f.write("- **TBT (Total Blocking Time):** Sum of all time periods between FCP and Time to Interactive where the main thread was blocked for long enough to prevent input responsiveness.

")
        
        for metrics in all_metrics:
            f.write(f"## Audit for: [{metrics['url']}]({metrics['url']})

")
            f.write(f"- **Performance Score:** {metrics['performance_score']}
")
            f.write(f"- **Largest Contentful Paint (LCP):** {metrics['LCP']}
")
            f.write(f"- **Cumulative Layout Shift (CLS):** {metrics['CLS']}
")
            f.write(f"- **Interaction to Next Paint (INP):** {metrics['INP']}
")
            f.write(f"- **First Contentful Paint (FCP):** {metrics['FCP']}
")
            f.write(f"- **Total Blocking Time (TBT):** {metrics['TBT']}
")
            f.write(f"
[View Full Lighthouse Report (JSON)]({os.path.basename(metrics['report_path'])})

")
            f.write("---

")
            
    print(f"Performance summary generated at {summary_path}")

# --- Main Execution ---

def main():
    parser = argparse.ArgumentParser(
        description="Automate Google Lighthouse audits for specified URLs and generate a summary report.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "-u", "--urls",
        nargs='+',
        required=True,
        help="List of URLs to audit (e.g., -u https://example.com https://example.com/about)"
    )
    parser.add_argument(
        "-o", "--output-dir",
        default=DEFAULT_OUTPUT_DIR,
        help=f"Directory to save Lighthouse reports and summary. Defaults to '{DEFAULT_OUTPUT_DIR}'."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simulate the execution without actually running Lighthouse or writing files."
    )
    parser.add_argument(
        "--output-format",
        choices=['markdown', 'json'],
        default='markdown',
        help="Specify the output format for the summary. 'markdown' for a human-readable summary, 'json' for raw aggregated JSON."
    )

    args = parser.parse_args()

    if not args.dry_run:
        os.makedirs(args.output_dir, exist_ok=True)

    all_metrics = []
    for url in args.urls:
        report_path = get_lighthouse_report(url, args.output_dir, args.dry_run)
        if report_path:
            metrics = parse_lighthouse_report(report_path)
            if metrics:
                metrics['report_path'] = report_path # Store full path for linking
                all_metrics.append(metrics)
    
    if not all_metrics:
        print("No successful Lighthouse audits to report.", file=sys.stderr)
        sys.exit(1)

    if args.output_format == 'markdown':
        if not args.dry_run:
            generate_markdown_summary(all_metrics, args.output_dir)
        else:
            print("Dry run: Markdown summary would be generated.")
    elif args.output_format == 'json':
        json_output_path = os.path.join(args.output_dir, "performance_summary.json")
        if not args.dry_run:
            with open(json_output_path, 'w', encoding='utf-8') as f:
                json.dump(all_metrics, f, indent=2)
            print(f"JSON summary generated at {json_output_path}")
        else:
            print("Dry run: JSON summary would be generated.")

if __name__ == "__main__":
    main()
