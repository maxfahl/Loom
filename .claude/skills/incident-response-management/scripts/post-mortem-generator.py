#!/usr/bin/env python3

"""
post-mortem-generator.py: Generates a structured Markdown post-mortem template.

This script creates a new Markdown file for a post-mortem report, pre-filling
key incident details based on command-line arguments. It helps ensure consistency
and speeds up the post-incident review process.

Usage:
    python post-mortem-generator.py --incident-id INC-123 --summary "API Latency Spike" \
                                    --date 2025-10-20 --duration "2h 15m" \
                                    [--service "User API"] [--commander "Jane Doe"] \
                                    [--output-dir "./postmortems"]

Configuration:
    - OUTPUT_DIR: Environment variable to specify the default output directory.
                  Defaults to './postmortems' if not set.
"""

import argparse
import os
import datetime
import sys

def main():
    parser = argparse.ArgumentParser(
        description="Generates a structured Markdown post-mortem template.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("--incident-id", required=True,
                        help="Unique identifier for the incident (e.g., INC-123).")
    parser.add_argument("--summary", required=True,
                        help="A concise summary of the incident.")
    parser.add_argument("--date", required=True,
                        help="Date of the incident (YYYY-MM-DD).")
    parser.add_argument("--duration", default="TBD",
                        help="Duration of the incident (e.g., '2h 15m').")
    parser.add_argument("--service", default="Unknown Service",
                        help="Name of the affected service.")
    parser.add_argument("--commander", default="Unassigned",
                        help="Name of the Incident Commander.")
    parser.add_argument("--severity", default="P2", choices=["P0", "P1", "P2", "P3", "P4"],
                        help="Incident severity level (P0-P4).")
    parser.add_argument("--output-dir",
                        default=os.getenv("OUTPUT_DIR", "./postmortems"),
                        help="Directory to save the post-mortem file.")

    args = parser.parse_args()

    # Validate date format
    try:
        incident_date = datetime.datetime.strptime(args.date, "%Y-%m-%d").strftime("%Y-%m-%d")
    except ValueError:
        print(f"Error: Invalid date format. Please use YYYY-MM-DD. Got: {args.date}")
        sys.exit(1)

    # Construct filename
    filename_slug = args.summary.lower().replace(" ", "-").replace("/", "").replace("'", "") # Sanitize for filename
    output_filename = f"post-mortem-{incident_date}-{filename_slug}.md"
    output_path = os.path.join(args.output_dir, output_filename)

    # Ensure output directory exists
    os.makedirs(args.output_dir, exist_ok=True)

    template_content = f"""
# Post-Mortem Report: {args.summary}

## 1. Incident Summary

*   **Incident ID:** {args.incident_id}
*   **Date & Time (UTC):** {incident_date} - TBD
*   **Duration:** {args.duration}
*   **Service(s) Affected:** {args.service}
*   **Severity:** {args.severity}
*   **Impact:** [Concise description of business and customer impact, e.g., "Users unable to log in for 2 hours, resulting in X% revenue loss."]
*   **Incident Commander:** {args.commander}
*   **Key Responders:** [List of individuals/teams involved]

## 2. Detection

*   **How was the incident detected?** [e.g., "Automated alert from Prometheus", "Customer report via support channel"]
*   **Time to Detect (MTTD):** [e.g., 5 minutes]
*   **Was detection effective?** [Yes/No, why/why not]

## 3. Response Timeline

| Timestamp (UTC) | Event                                                              | Owner          |
| :-------------- | :----------------------------------------------------------------- | :------------- |
| {incident_date} HH:MM | Incident detected                                                  | TBD            |
| {incident_date} HH:MM | Incident acknowledged                                              | TBD            |
| {incident_date} HH:MM | Initial investigation started                                      | TBD            |
| {incident_date} HH:MM | Mitigation applied                                                 | TBD            |
| {incident_date} HH:MM | Service restored                                                   | TBD            |
| {incident_date} HH:MM | Incident resolved                                                  | TBD            |

*   **Time to Acknowledge (MTTA):** [e.g., 2 minutes]
*   **Time to Resolve (MTTR):** [e.g., 1 hour 30 minutes]

## 4. Root Cause Analysis

*   **What was the immediate cause?** [e.g., "Deployment of new feature X introduced a memory leak in Service Y."]
*   **What were the contributing factors?** [e.g., "Lack of adequate load testing for feature X", "Monitoring alert threshold was too high."]
*   **5 Whys / Fishbone Diagram (if applicable):** [Brief summary or link to analysis]

## 5. Resolution

*   **How was the incident resolved?** [e.g., "Rolled back deployment of feature X", "Increased database connection pool size."]
*   **Was the resolution effective?** [Yes/No]

## 6. Lessons Learned

*   **What went well?** [e.g., "Team communication was excellent", "Runbook for database issues was accurate."]
*   **What could have gone better?** [e.g., "Detection could have been faster", "Lack of clear ownership for Service Z."]

## 7. Action Items

| ID    | Description                                                              | Owner          | Due Date   | Status    |
| :---- | :----------------------------------------------------------------------- | :------------- | :--------- | :-------- |
| {args.incident_id}-1 | [Action item 1]                                                          | TBD            | YYYY-MM-DD | Open      |
| {args.incident_id}-2 | [Action item 2]                                                          | TBD            | YYYY-MM-DD | Open      |

## 8. Supporting Information

*   [Link to relevant dashboards (Grafana, Datadog)]
*   [Link to relevant logs (Splunk, ELK)]
*   [Link to Jira ticket / Incident Management Platform entry]
*   [Link to communication threads (Slack)]
"""

    try:
        with open(output_path, "w") as f:
            f.write(template_content)
        print(f"✅ Post-mortem template generated successfully: {output_path}")
    except IOError as e:
        print(f"Error writing file {output_path}: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
