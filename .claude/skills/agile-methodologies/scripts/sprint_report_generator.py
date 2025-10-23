#!/usr/bin/env python3

import argparse
import pandas as pd
import os
from datetime import datetime

def generate_sprint_report(csv_file: str, sprint_name: str, output_file: str,
                           id_col: str = 'Issue key', summary_col: str = 'Summary',
                           status_col: str = 'Status', story_points_col: str = 'Story points',
                           assignee_col: str = 'Assignee', verbose: bool = False):
    """
    Generates a markdown-formatted sprint report from a CSV export of a task management tool.

    Args:
        csv_file (str): Path to the input CSV file.
        sprint_name (str): The name of the sprint for the report.
        output_file (str): Path to the output markdown file.
        id_col (str): Name of the column containing issue IDs.
        summary_col (str): Name of the column containing issue summaries.
        status_col (str): Name of the column containing issue statuses.
        story_points_col (str): Name of the column containing story points.
        assignee_col (str): Name of the column containing assignee names.
        verbose (bool): If True, print detailed processing messages.
    """
    if verbose:
        print(f"Generating sprint report for '{sprint_name}' from '{csv_file}'...")

    if not os.path.exists(csv_file):
        print(f"Error: CSV file not found at '{csv_file}'")
        return

    try:
        df = pd.read_csv(csv_file)
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return

    required_cols = [id_col, summary_col, status_col]
    if story_points_col:
        required_cols.append(story_points_col)
    if assignee_col:
        required_cols.append(assignee_col)

    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        print(f"Error: Missing required columns in CSV: {', '.join(missing_cols)}")
        print(f"Available columns: {', '.join(df.columns)}")
        return

    # Fill NaN story points with 0 for calculations
    if story_points_col in df.columns:
        df[story_points_col] = pd.to_numeric(df[story_points_col], errors='coerce').fillna(0)

    total_issues = len(df)
    completed_issues = df[df[status_col].isin(['Done', 'Closed', 'Resolved'])]
    in_progress_issues = df[df[status_col].isin(['In Progress', 'In Review', 'Testing', 'Open'])]
    blocked_issues = df[df[status_col].str.contains('Blocked', case=False, na=False)]

    completed_count = len(completed_issues)
    in_progress_count = len(in_progress_issues)
    blocked_count = len(blocked_issues)
    remaining_count = total_issues - completed_count - in_progress_count - blocked_count

    velocity = completed_issues[story_points_col].sum() if story_points_col else 'N/A'

    report_content = f"# Sprint Report: {sprint_name}

"
    report_content += f"**Generated On:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

"
    report_content += "## Summary

"
    report_content += f"- Total Issues: **{total_issues}**
"
    report_content += f"- Completed Issues: **{completed_count}**
"
    report_content += f"- In Progress Issues: **{in_progress_count}**
"
    report_content += f"- Blocked Issues: **{blocked_count}**
"
    report_content += f"- Remaining Issues: **{remaining_count}**
"
    if story_points_col:
        report_content += f"- Achieved Velocity (Story Points): **{velocity}**

"
    else:
        report_content += "
"

    if not completed_issues.empty:
        report_content += "## Completed Issues

"
        for _, row in completed_issues.iterrows():
            sp = f" ({int(row[story_points_col])} SP)" if story_points_col else ""
            assignee = f" - {row[assignee_col]}" if assignee_col and pd.notna(row[assignee_col]) else ""
            report_content += f"- [{row[id_col]}] {row[summary_col]}{sp}{assignee}
"
        report_content += "
"

    if not in_progress_issues.empty:
        report_content += "## In Progress Issues

"
        for _, row in in_progress_issues.iterrows():
            sp = f" ({int(row[story_points_col])} SP)" if story_points_col else ""
            assignee = f" - {row[assignee_col]}" if assignee_col and pd.notna(row[assignee_col]) else ""
            report_content += f"- [{row[id_col]}] {row[summary_col]} (Status: {row[status_col]}){sp}{assignee}
"
        report_content += "
"

    if not blocked_issues.empty:
        report_content += "## Blocked Issues

"
        for _, row in blocked_issues.iterrows():
            sp = f" ({int(row[story_points_col])} SP)" if story_points_col else ""
            assignee = f" - {row[assignee_col]}" if assignee_col and pd.notna(row[assignee_col]) else ""
            report_content += f"- [{row[id_col]}] {row[summary_col]}{sp}{assignee}
"
        report_content += "
"

    if remaining_count > 0:
        # Assuming remaining issues are those not completed, in progress, or blocked
        remaining_issues_df = df[~df[status_col].isin(['Done', 'Closed', 'Resolved', 'In Progress', 'In Review', 'Testing', 'Open']) &
                                 ~df[status_col].str.contains('Blocked', case=False, na=False)]
        if not remaining_issues_df.empty:
            report_content += "## Remaining Issues (Not Started / Backlog)

"
            for _, row in remaining_issues_df.iterrows():
                sp = f" ({int(row[story_points_col])} SP)" if story_points_col else ""
                assignee = f" - {row[assignee_col]}" if assignee_col and pd.notna(row[assignee_col]) else ""
                report_content += f"- [{row[id_col]}] {row[summary_col]}{sp}{assignee}
"
            report_content += "
"


    try:
        with open(output_file, 'w') as f:
            f.write(report_content)
        print(f"Sprint report successfully generated to '{output_file}'")
    except Exception as e:
        print(f"Error writing report to file: {e}")

def main():
    parser = argparse.ArgumentParser(
        description='Generate a markdown-formatted sprint report from a CSV export.',
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument('csv_file', help='Path to the input CSV file (e.g., Jira export).')
    parser.add_argument('-s', '--sprint-name', default='Current Sprint',
                        help='Name of the sprint for the report (default: "Current Sprint").')
    parser.add_argument('-o', '--output-file', default='sprint_report.md',
                        help='Path to the output markdown file (default: "sprint_report.md").')
    parser.add_argument('--id-col', default='Issue key',
                        help='Name of the column containing issue IDs (default: "Issue key").')
    parser.add_argument('--summary-col', default='Summary',
                        help='Name of the column containing issue summaries (default: "Summary").')
    parser.add_argument('--status-col', default='Status',
                        help='Name of the column containing issue statuses (default: "Status").')
    parser.add_argument('--story-points-col', default='Story points',
                        help='Name of the column containing story points (default: "Story points"). '
                             'Set to empty string "" to exclude story points from calculations and report.')
    parser.add_argument('--assignee-col', default='Assignee',
                        help='Name of the column containing assignee names (default: "Assignee"). '
                             'Set to empty string "" to exclude assignees from the report.')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Enable verbose output.')

    args = parser.parse_args()

    # Check for pandas installation
    try:
        import pandas as pd
    except ImportError:
        print("Error: pandas library not found.")
        print("Please install it using: pip install pandas")
        return

    generate_sprint_report(
        csv_file=args.csv_file,
        sprint_name=args.sprint_name,
        output_file=args.output_file,
        id_col=args.id_col,
        summary_col=args.summary_col,
        status_col=args.status_col,
        story_points_col=args.story_points_col if args.story_points_col else None,
        assignee_col=args.assignee_col if args.assignee_col else None,
        verbose=args.verbose
    )

if __name__ == '__main__':
    main()
