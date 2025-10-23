#!/usr/bin/env python3

# analyze-mutation-report.py
# Description: Parses a Stryker Mutator JSON report and provides actionable insights.
# It highlights files with low mutation scores and lists survived mutants for investigation.

# Usage:
#   python3 analyze-mutation-report.py [path_to_report.json]
#   python3 analyze-mutation-report.py --report-path ./stryker-report/mutation.json --min-score 70

import argparse
import json
import os

# --- Constants for colored output ---
COLOR_RED = "\033[91m"
COLOR_GREEN = "\033[92m"
COLOR_YELLOW = "\033[93m"
COLOR_BLUE = "\033[94m"
COLOR_RESET = "\033[0m"
COLOR_BOLD = "\033[1m"

def log_info(message):
    print(f"{COLOR_BLUE}[INFO]{COLOR_RESET} {message}")

def log_success(message):
    print(f"{COLOR_GREEN}[SUCCESS]{COLOR_RESET} {message}")

def log_warn(message):
    print(f"{COLOR_YELLOW}[WARN]{COLOR_RESET} {message}")

def log_error(message):
    print(f"{COLOR_RED}[ERROR]{COLOR_RESET} {message}")

def parse_report(report_path):
    """Parses the Stryker JSON report."""
    if not os.path.exists(report_path):
        log_error(f"Report file not found: {report_path}")
        return None
    try:
        with open(report_path, 'r') as f:
            report = json.load(f)
        return report
    except json.JSONDecodeError:
        log_error(f"Invalid JSON format in report file: {report_path}")
        return None
    except Exception as e:
        log_error(f"Error reading report file: {e}")
        return None

def analyze_report(report, min_score_threshold):
    """Analyzes the report and prints insights."""
    if not report or 'files' not in report:
        log_error("Invalid report structure. Missing 'files' key.")
        return

    log_info(f"{COLOR_BOLD}--- Mutation Report Analysis ---")

    overall_score = report.get('mutationScore', 0)
    log_info(f"Overall Mutation Score: {COLOR_BOLD}{overall_score:.2f}%%{COLOR_RESET}")

    if overall_score < min_score_threshold:
        log_warn(f"Overall mutation score {overall_score:.2f}%% is below the threshold of {min_score_threshold}%%!")
    else:
        log_success(f"Overall mutation score {overall_score:.2f}%% meets the threshold of {min_score_threshold}%%.")

    low_score_files = []
    survived_mutants_details = []

    for file_path, file_data in report['files'].items():
        file_score = file_data.get('mutationScore', 0)
        if file_score < min_score_threshold:
            low_score_files.append((file_path, file_score))
        
        for mutant in file_data.get('mutants', []):
            if mutant['status'] == 'Survived':
                survived_mutants_details.append({
                    'file': file_path,
                    'location': f"{mutant['location']['start']['line']}:{mutant['location']['start']['column']}",
                    'mutatorName': mutant['mutatorName'],
                    'replacement': mutant['replacement'],
                    'originalLines': mutant['originalLines']
                })
    
    print("\n" + f"{COLOR_BOLD}--- Files with Mutation Score Below {min_score_threshold}% ---{COLOR_RESET}")
    if low_score_files:
        for path, score in sorted(low_score_files, key=lambda x: x[1]):
            log_warn(f"  - {path}: {score:.2f}%%")
        log_info("Consider focusing your test improvement efforts on these files.")
    else:
        log_success("All files meet the minimum mutation score threshold.")

    print("\n" + f"{COLOR_BOLD}--- Survived Mutants for Investigation ---")
    if survived_mutants_details:
        for mutant in survived_mutants_details:
            print(f"{COLOR_YELLOW}  File: {mutant['file']}{COLOR_RESET}")
            print(f"    Location: {mutant['location']}")
            print(f"    Mutator: {mutant['mutatorName']}")
            print(f"    Original: '{mutant['originalLines']}'")
            print(f"    Mutated to: '{mutant['replacement']}'")
            print("    Action: Review corresponding tests. Do they assert against this specific behavior?")
            print("-" * 20)
        log_info("Each survived mutant indicates a potential gap in your test suite. Investigate and improve tests.")
    else:
        log_success("No survived mutants found! Excellent test suite effectiveness.")

    log_info(f"{COLOR_BOLD}--- Analysis Complete ---")

def main():
    parser = argparse.ArgumentParser(
        description="Analyze Stryker Mutator JSON report for actionable insights."
    )
    parser.add_argument(
        "report_path",
        nargs='?',
        default="stryker-report/mutation.json",
        help="Path to the Stryker JSON report file (e.g., stryker-report/mutation.json)."
    )
    parser.add_argument(
        "--min-score",
        type=float,
        default=80.0,
        help="Minimum mutation score threshold for flagging files (default: 80.0).
              Files with scores below this will be highlighted."
    )

    args = parser.parse_args()

    log_info(f"Starting analysis of Stryker report: {args.report_path}")
    report = parse_report(args.report_path)
    if report:
        analyze_report(report, args.min_score)

if __name__ == "__main__":
    main()
