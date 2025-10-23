import argparse
import os
import re
import sys
from datetime import datetime

# ANSI escape codes for colored output
COLOR_RED = "\033[91m"
COLOR_GREEN = "\033[92m"
COLOR_YELLOW = "\033[93m"
COLOR_BLUE = "\033[94m"
COLOR_RESET = "\033[0m"

def print_color(color, message):
    print(f"{color}{message}{COLOR_RESET}")

class Risk:
    def __init__(self, name, impact, likelihood, owner, mitigation_plan, status):
        self.name = name
        self.impact = impact
        self.likelihood = likelihood
        self.owner = owner
        self.mitigation_plan = mitigation_plan
        self.status = status
        self.priority = self._calculate_priority()

    def _calculate_priority(self):
        impact_map = {'High': 3, 'Medium': 2, 'Low': 1}
        likelihood_map = {'High': 3, 'Medium': 2, 'Low': 1}
        return impact_map.get(self.impact, 0) * likelihood_map.get(self.likelihood, 0)

    def __repr__(self):
        return f"Risk(Name={self.name}, Priority={self.priority}, Status={self.status})"

def parse_risk_register_markdown(file_path):
    """Parses a Markdown file to extract risk information."""
    risks = []
    current_risk_data = {}
    try:
        with open(file_path, 'r') as f:
            content = f.read()

        # Split content by risk headings
        risk_entries = re.split(r'(?m)^### Risk: (.+)$', content)

        # The first element will be empty or pre-amble, skip it
        for i in range(1, len(risk_entries), 2):
            name = risk_entries[i].strip()
            details = risk_entries[i+1]

            impact = re.search(r'^- \*\*Impact:\*\* (.+)$' , details, re.MULTILINE)
            likelihood = re.search(r'^- \*\*Likelihood:\*\* (.+)$' , details, re.MULTILINE)
            owner = re.search(r'^- \*\*Owner:\*\* (.+)$' , details, re.MULTILINE)
            mitigation_plan = re.search(r'^- \*\*Mitigation Plan:\*\* (.+)$' , details, re.MULTILINE)
            status = re.search(r'^- \*\*Status:\*\* (.+)$' , details, re.MULTILINE)

            risks.append(Risk(
                name=name,
                impact=impact.group(1).strip() if impact else "Unknown",
                likelihood=likelihood.group(1).strip() if likelihood else "Unknown",
                owner=owner.group(1).strip() if owner else "Unassigned",
                mitigation_plan=mitigation_plan.group(1).strip() if mitigation_plan else "N/A",
                status=status.group(1).strip() if status else "Open"
            ))

    except FileNotFoundError:
        print_color(COLOR_RED, f"Error: Risk register file not found at {file_path}")
        sys.exit(1)
    except Exception as e:
        print_color(COLOR_RED, f"Error parsing risk register {file_path}: {e}")
        sys.exit(1)
    return risks

def generate_risk_report(risk_file, output_file, min_priority, dry_run):
    """Generates a summary risk report."""
    print_color(COLOR_YELLOW, f"Generating risk report from: {risk_file}")

    risks = parse_risk_register_markdown(risk_file)

    if not risks:
        print_color(COLOR_YELLOW, "No risks found in the register.")
        return

    # Filter and sort risks
    filtered_risks = [r for r in risks if r.priority >= min_priority and r.status != "Mitigated"]
    sorted_risks = sorted(filtered_risks, key=lambda x: x.priority, reverse=True)

    report_content = []
    report_content.append(f"# Risk Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    report_content.append(f"Generated from: {risk_file}\n")
    report_content.append(f"Minimum Priority for Inclusion: {min_priority} (Impact x Likelihood)\n")
    report_content.append(f"Total Risks Identified: {len(risks)}\n")
    report_content.append(f"High Priority / Open Risks in Report: {len(sorted_risks)}\n")
    report_content.append("---\n\n")

    if not sorted_risks:
        report_content.append("No high-priority or open risks to report.\n")
    else:
        for risk in sorted_risks:
            report_content.append(f"## Risk: {risk.name}\n")
            report_content.append(f"- **Priority:** {risk.priority} (Impact: {risk.impact}, Likelihood: {risk.likelihood})\n")
            report_content.append(f"- **Status:** {risk.status}\n")
            report_content.append(f"- **Owner:** {risk.owner}\n")
            report_content.append(f"- **Mitigation Plan:** {risk.mitigation_plan}\n")
            report_content.append("\n")

    final_report = "".join(report_content)

    if dry_run:
        print_color(COLOR_YELLOW, "\n--- Dry Run Risk Report Output ---")
        print(final_report)
        print_color(COLOR_YELLOW, "--- End Dry Run ---")
    else:
        if output_file:
            try:
                with open(output_file, 'w') as f:
                    f.write(final_report)
                print_color(COLOR_GREEN, f"Risk report successfully written to {output_file}")
            except Exception as e:
                print_color(COLOR_RED, f"Error writing risk report to {output_file}: {e}")
                sys.exit(1)
        else:
            print_color(COLOR_GREEN, "\n--- Generated Risk Report ---")
            print(final_report)
            print_color(COLOR_GREEN, "--- End Risk Report ---")

    print_color(COLOR_GREEN, "Risk report generation complete.")

def main():
    parser = argparse.ArgumentParser(
        description="Generate a summary risk report from a Markdown risk register.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "-f", "--file",
        required=True,
        help="Path to the Markdown risk register file."
    )
    parser.add_argument(
        "-o", "--output",
        help="Output file path for the report (e.g., risk_report.md). If not specified, prints to stdout."
    )
    parser.add_argument(
        "-p", "--min-priority",
        type=int,
        default=4,
        help="Minimum calculated priority (Impact x Likelihood) for a risk to be included in the report (default: 4)."
    )
    parser.add_argument(
        "-d", "--dry-run",
        action="store_true",
        help="Show the report output without writing to a file."
    )

    args = parser.parse_args()

    generate_risk_report(args.file, args.output, args.min_priority, args.dry_run)

if __name__ == "__main__":
    main()
