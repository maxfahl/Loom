#!/usr/bin/env python3

import argparse
import json
import os
from datetime import datetime

# --- Configuration ---
OUTPUT_DIR = "pentest_reports"

# --- Helper Functions ---
def print_colored(text, color):
    colors = {
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "magenta": "\033[95m",
        "cyan": "\033[96m",
        "white": "\033[97m",
        "reset": "\033[0m"
    }
    print(f"{colors.get(color, colors['reset'])}{text}{colors['reset']}")

def generate_report_content(findings, report_title="Penetration Test Report", target_info="N/A"):
    """Generates Markdown content for the penetration test report."""
    report_content = f"# {report_title}\n\n"
    report_content += f"**Target Information**: {target_info}\n"
    report_content += f"**Report Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    report_content += "## Executive Summary\n\n"
    report_content += "This report summarizes the findings of a penetration test conducted on the specified target. " \
                      "The objective was to identify security vulnerabilities that could be exploited by malicious actors. " \
                      "A total of {len(findings)} vulnerabilities were identified, categorized by severity and impact. " \
                      "Detailed findings and remediation recommendations are provided below.\n\n"

    if not findings:
        report_content += "No vulnerabilities were identified during this assessment. This indicates a strong security posture for the tested scope.\n\n"
        return report_content

    # Group findings by severity
    severity_order = {"Critical": 1, "High": 2, "Medium": 3, "Low": 4, "Informational": 5}
    sorted_findings = sorted(findings, key=lambda x: severity_order.get(x.get("severity", "Informational"), 5))

    # Summary by severity
    severity_counts = {}
    for finding in findings:
        severity = finding.get("severity", "Informational")
        severity_counts[severity] = severity_counts.get(severity, 0) + 1

    report_content += "### Vulnerability Summary by Severity\n\n"
    for severity, count in sorted(severity_counts.items(), key=lambda item: severity_order.get(item[0], 5)):
        report_content += f"- **{severity}**: {count}\n"
    report_content += "\n"

    report_content += "## Detailed Findings\n\n"

    for i, finding in enumerate(sorted_findings):
        report_content += f"### {i+1}. {finding.get("name", "Unnamed Vulnerability")} ({finding.get("severity", "Informational")})\n\n"
        report_content += f"**Severity**: {finding.get("severity", "Informational")}\n"
        if finding.get("cvss_score"):
            report_content += f"**CVSS Score**: {finding["cvss_score"]}\n"
        if finding.get("cve_id"):
            report_content += f"**CVE ID**: {finding["cve_id"]}\n"
        if finding.get("location"):
            report_content += f"**Location**: {finding["location"]}\n"
        if finding.get("affected_asset"):
            report_content += f"**Affected Asset**: {finding["affected_asset"]}\n"
        report_content += "\n"

        report_content += "#### Description\n\n"
        report_content += f"{finding.get("description", "No description provided.")}\n\n"

        report_content += "#### Steps to Reproduce\n\n"
        report_content += f"```\n{finding.get("reproduce_steps", "No reproduction steps provided.")}\n```\n\n"

        report_content += "#### Impact\n\n"
        report_content += f"{finding.get("impact", "No impact statement provided.")}\n\n"

        report_content += "#### Recommendation\n\n"
        report_content += f"{finding.get("recommendation", "No recommendation provided.")}\n\n"

        if finding.get("references"):
            report_content += "#### References\n\n"
            for ref in finding["references"]:
                report_content += f"- {ref}\n"
            report_content += "\n"

    report_content += "## Conclusion\n\n"
    report_content += "This report provides a snapshot of the security posture at the time of the assessment. " \
                      "It is crucial to address the identified vulnerabilities promptly and implement continuous security practices. " \
                      "Regular penetration testing and security audits are recommended to maintain a strong security posture.\n\n"

    return report_content

# --- Main Logic ---
def main():
    parser = argparse.ArgumentParser(
        description="Generates a Markdown penetration test report from a JSON file of findings.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("input_json", help="Path to the JSON file containing vulnerability findings.")
    parser.add_argument("--title", default="Penetration Test Report",
                        help="Title of the report (default: 'Penetration Test Report').")
    parser.add_argument("--target-info", default="N/A",
                        help="Information about the target (e.g., 'Web Application v1.0', 'Internal Network').")
    parser.add_argument("--output", "-o", action="store_true", help="Save the report to a Markdown file.")
    parser.add_argument("--dry-run", action="store_true", help="Print the generated report to stdout without saving to a file.")

    args = parser.parse_args()

    if not os.path.exists(args.input_json):
        print_colored(f"[-] Error: Input JSON file not found at '{args.input_json}'.", "red")
        sys.exit(1)

    try:
        with open(args.input_json, 'r') as f:
            findings_data = json.load(f)
    except json.JSONDecodeError:
        print_colored(f"[-] Error: Invalid JSON format in '{args.input_json}'.", "red")
        sys.exit(1)
    except Exception as e:
        print_colored(f"[-] An unexpected error occurred while reading JSON: {e}", "red")
        sys.exit(1)

    # Basic validation of findings structure
    if not isinstance(findings_data, list):
        print_colored("[-] Error: JSON input should be a list of vulnerability findings.", "red")
        sys.exit(1)

    report_content = generate_report_content(findings_data, args.title, args.target_info)

    if args.dry_run:
        print_colored("\n--- DRY RUN REPORT CONTENT ---", "yellow")
        print(report_content)
        print_colored("\n--- END DRY RUN ---", "yellow")
    elif args.output:
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        report_filename = f"{args.title.replace(' ', '_').lower()}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        output_path = os.path.join(OUTPUT_DIR, report_filename)
        with open(output_path, 'w') as f:
            f.write(report_content)
        print_colored(f"[+] Penetration test report successfully generated and saved to: {output_path}", "green")
    else:
        print_colored("\n--- GENERATED REPORT CONTENT (not saved) ---", "yellow")
        print(report_content)
        print_colored("\n--- END REPORT CONTENT ---", "yellow")

    print_colored("\n[+] Report generation complete!", "green")

if __name__ == "__main__":
    main()
