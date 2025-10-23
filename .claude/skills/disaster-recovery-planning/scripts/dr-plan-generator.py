#!/usr/bin/env python3
"""
dr-plan-generator.py: Generates a basic Disaster Recovery Plan (DRP) document template.

This script prompts the user for key DRP parameters like Recovery Time Objective (RTO),
Recovery Point Objective (RPO), and critical systems, then generates a Markdown
document outlining a basic DRP structure. It aims to automate the initial
documentation phase of DRP, ensuring essential considerations are captured.

Usage:
    python3 dr-plan-generator.py [--output FILE]

Options:
    --output FILE   Specify the output Markdown file name. Defaults to 'DRP_Plan_<timestamp>.md'.
    --help          Show this help message and exit.

Example:
    python3 dr-plan-generator.py --output my_project_drp.md
"""

import argparse
import datetime
import os
import sys

def get_user_input(prompt, default=None):
    """Gets input from the user with an optional default value."""
    if default:
        return input(f"{prompt} (default: {default}): ") or default
    return input(f"{prompt}: ")

def generate_drp_content(project_name, rto, rpo, critical_systems, data_sources, recovery_team):
    """Generates the Markdown content for the DRP."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    content = f"""# Disaster Recovery Plan for {project_name}

**Version**: 1.0
**Date**: {timestamp}
**Prepared By**: [Your Name/Team]

## 1. Introduction

This document outlines the Disaster Recovery Plan (DRP) for the **{project_name}** system. Its purpose is to provide a structured approach to recovering critical IT infrastructure and data in the event of a disaster, minimizing downtime and data loss.

## 2. Recovery Objectives

### 2.1. Recovery Time Objective (RTO)

The maximum acceptable duration of time that **{project_name}** can be unavailable after an incident.
**Target RTO**: {rto}

### 2.2. Recovery Point Objective (RPO)

The maximum acceptable amount of data loss measured in time from a disaster event.
**Target RPO**: {rpo}

## 3. Critical Systems and Dependencies

The following systems are critical for the operation of **{project_name}** and are covered by this DRP:

{critical_systems}

## 4. Data Sources and Backup Strategy

### 4.1. Critical Data Sources

The following data sources are essential for **{project_name}** and require robust backup and replication:

{data_sources}

### 4.2. Backup Strategy (3-2-1-1-0 Rule)

Our backup strategy adheres to the 3-2-1-1-0 rule:
- **3 Copies**: At least three copies of all critical data exist.
- **2 Different Media**: Backups are stored on at least two different types of storage media (e.g., disk, cloud object storage).
- **1 Offsite Copy**: At least one copy is stored offsite in a geographically separate location.
- **1 Air-gapped/Immutable Copy**: At least one copy is air-gapped or immutable to protect against ransomware and accidental deletion.
- **0 Errors**: Regular verification and testing ensure zero backup errors.

**Specific Backup Details (to be filled in):**
- **Frequency**: [e.g., Daily full, hourly incremental]
- **Retention**: [e.g., 7 days daily, 4 weeks weekly, 12 months monthly]
- **Location**: [e.g., Primary data center, AWS S3 (us-east-1), Azure Blob Storage (West US 2)]
- **Tools**: [e.g., Veeam, AWS Backup, custom scripts]

## 5. Replication Strategy

For critical systems requiring low RPO, replication is employed:
- **Type**: [e.g., Database streaming replication, block-level storage replication, application-level replication]
- **Target**: [e.g., Standby database in another region, DR site]
- **Monitoring**: [e.g., Replication lag alerts]

## 6. Recovery Procedures

### 6.1. Incident Detection and Declaration

- **Monitoring Systems**: [e.g., Prometheus, CloudWatch alarms]
- **Alerting**: [e.g., PagerDuty, Slack notifications]
- **Declaration Criteria**: [e.g., Prolonged outage, data corruption detected]

### 6.2. Recovery Steps (High-Level)

1.  **Assess Impact**: Determine the scope and nature of the disaster.
2.  **Activate DR Team**: Notify and assemble the designated recovery team.
3.  **Isolate Affected Systems**: Prevent further damage or data corruption.
4.  **Initiate Recovery Environment**: Provision or switch to DR infrastructure.
5.  **Restore Data**: Recover data from backups or activate replicated data.
6.  **Restore Applications**: Deploy and configure applications in the DR environment.
7.  **Verify Functionality**: Conduct thorough testing of all recovered systems.
8.  **Failback (if applicable)**: Plan and execute the return to primary operations.

**Detailed Recovery Runbook (to be filled in):**
- [Link to detailed runbook or section for specific system recovery steps]

## 7. Roles and Responsibilities

The following individuals/teams are responsible for DRP activities:

{recovery_team}

## 8. Testing and Maintenance

- **Frequency of Testing**: [e.g., Quarterly, annually]
- **Types of Tests**: [e.g., Tabletop exercises, simulated failovers, full DR drills]
- **Review and Update**: This DRP will be reviewed and updated [e.g., annually, after major changes, after each test].

## 9. Communication Plan

- **Internal Stakeholders**: [e.g., Executive leadership, department heads]
- **External Stakeholders**: [e.g., Customers, partners, regulators]
- **Communication Channels**: [e.g., Email, status page, emergency contact list]

## 10. Glossary

- **DRP**: Disaster Recovery Plan
- **RTO**: Recovery Time Objective
- **RPO**: Recovery Point Objective
- **PITR**: Point-in-Time Recovery
- **CDP**: Continuous Data Protection
"""
    return content

def main():
    parser = argparse.ArgumentParser(
        description="Generates a basic Disaster Recovery Plan (DRP) document template.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Specify the output Markdown file name. Defaults to 'DRP_Plan_<timestamp>.md'."
    )
    args = parser.parse_args()

    print("--- DRP Plan Generator ---")
    print("Please provide the following information to generate your DRP template.")

    project_name = get_user_input("Enter Project/System Name", "MyCriticalApp")
    rto = get_user_input("Enter Target RTO (e.g., 4 hours, 24 hours)", "4 hours")
    rpo = get_user_input("Enter Target RPO (e.g., 15 minutes, 1 hour)", "15 minutes")

    print("\n--- Critical Systems (enter one per line, type 'DONE' when finished) ---")
    critical_systems_list = []
    while True:
        system = input(f"Critical System {len(critical_systems_list) + 1} (e.g., Web Server, Database, API Gateway) or 'DONE': ")
        if system.upper() == 'DONE':
            break
        if system:
            critical_systems_list.append(f"- {system}")
    critical_systems = "\n".join(critical_systems_list) if critical_systems_list else "- [No critical systems specified]"

    print("\n--- Critical Data Sources (enter one per line, type 'DONE' when finished) ---")
    data_sources_list = []
    while True:
        data_source = input(f"Data Source {len(data_sources_list) + 1} (e.g., PostgreSQL DB, S3 Bucket, EBS Volumes) or 'DONE': ")
        if data_source.upper() == 'DONE':
            break
        if data_source:
            data_sources_list.append(f"- {data_source}")
    data_sources = "\n".join(data_sources_list) if data_sources_list else "- [No data sources specified]"

    print("\n--- Recovery Team Roles (enter one per line, type 'DONE' when finished) ---")
    recovery_team_list = []
    while True:
        role = input(f"Recovery Team Role {len(recovery_team_list) + 1} (e.g., Incident Commander, Database Admin, Network Engineer) or 'DONE': ")
        if role.upper() == 'DONE':
            break
        if role:
            recovery_team_list.append(f"- {role}: [Name/Team]")
    recovery_team = "\n".join(recovery_team_list) if recovery_team_list else "- [No recovery team roles specified]"


    drp_content = generate_drp_content(project_name, rto, rpo, critical_systems, data_sources, recovery_team)

    if args.output:
        output_filename = args.output
    else:
        timestamp_file = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        output_filename = f"DRP_Plan_{timestamp_file}.md"

    try:
        with open(output_filename, "w") as f:
            f.write(drp_content)
        print(f"\nDRP template successfully generated to '{output_filename}'")
        print("Please review and fill in the detailed sections.")
    except IOError as e:
        print(f"Error writing file '{output_filename}': {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
