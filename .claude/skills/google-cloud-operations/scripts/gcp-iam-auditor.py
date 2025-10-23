#!/usr/bin/env python3
"""
gcp-iam-auditor.py

This script audits IAM policies for a specified Google Cloud Platform (GCP) project.
It identifies overly broad permissions and suggests more granular, least-privilege alternatives.

Usage:
    python3 gcp-iam-auditor.py --project <YOUR_GCP_PROJECT_ID>
    python3 gcp-iam-auditor.py # Uses currently configured gcloud project

Example:
    python3 gcp-iam-auditor.py --project my-prod-project-456
    # Output will be a report of IAM findings and recommendations.

    # To get help:
    python3 gcp-iam-auditor.py --help
"""

import subprocess
import json
import argparse
import sys

def run_gcloud_command(command, project_id):
    """
    Executes a gcloud command and returns its JSON output.
    Handles errors and prints informative messages.
    """
    full_command = ["gcloud"] + command + ["--project", project_id, "--format=json"]
    try:
        result = subprocess.run(
            full_command,
            capture_output=True,
            text=True,
            check=True
        )
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error executing gcloud command: {' '.join(full_command)}", file=sys.stderr)
        print(f"Stderr: {e.stderr}", file=sys.stderr)
        return None
    except json.JSONDecodeError:
        print(f"Error decoding JSON from gcloud command output: {' '.join(full_command)}", file=sys.stderr)
        print(f"Stdout: {result.stdout}", file=sys.stderr)
        return None

def get_project_id_from_config():
    """
    Retrieves the currently configured gcloud project ID.
    """
    try:
        result = subprocess.run(
            ["gcloud", "config", "get-value", "project"],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return None

def get_iam_policy(project_id):
    """
    Fetches the IAM policy for the specified project.
    """
    print(f"🔍 Fetching IAM policy for project '{project_id}'...")
    policy = run_gcloud_command(["projects", "get-iam-policy", project_id], project_id)
    if policy is None:
        print(f"Error: Could not retrieve IAM policy for project '{project_id}'. Check permissions.", file=sys.stderr)
        sys.exit(1)
    return policy

def analyze_iam_policy(policy):
    """
    Analyzes the IAM policy for overly broad permissions and suggests alternatives.
    """
    findings = []
    broad_roles = {
        "roles/owner": "Owner role grants full access. Consider specific administrative roles like `roles/compute.admin`, `roles/storage.admin`, or `roles/cloudsql.admin`.",
        "roles/editor": "Editor role grants broad write access. Consider specific roles based on resource type, e.g., `roles/compute.instanceAdmin.v1`, `roles/storage.objectAdmin`.",
        "roles/viewer": "Viewer role grants broad read access. Consider specific read-only roles like `roles/compute.viewer`, `roles/storage.objectViewer`.",
        "roles/iam.securityAdmin": "Security Admin is powerful. Ensure it's only granted to security personnel.",
        "roles/admin": "Generic admin role, often too broad. Refine to service-specific admin roles."
    }

    for binding in policy.get("bindings", []):
        role = binding.get("role")
        members = binding.get("members")

        if role in broad_roles:
            for member in members:
                findings.append({
                    "member": member,
                    "role": role,
                    "recommendation": broad_roles[role]
                })
        elif "customRoles" in role: # Basic check for custom roles, more advanced analysis would be needed
            # This is a placeholder. A real auditor would need to inspect custom role definitions.
            for member in members:
                findings.append({
                    "member": member,
                    "role": role,
                    "recommendation": "Custom role detected. Review its permissions carefully to ensure least privilege. Custom roles can be overly permissive if not designed well."
                })

    return findings

def main():
    parser = argparse.ArgumentParser(
        description="Audits IAM policies for a GCP project, identifying broad permissions.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "--project",
        help="The GCP project ID to audit. If not provided, uses the currently configured gcloud project."
    )
    args = parser.parse_args()

    project_id = args.project
    if not project_id:
        project_id = get_project_id_from_config()

    if not project_id:
        print("Error: No GCP project ID provided or configured. Please run 'gcloud config set project PROJECT_ID' or provide --project argument.", file=sys.stderr)
        sys.exit(1)

    print("\n🛡️ Starting IAM Policy Audit for Project: {project_id} 🛡️\n")

    iam_policy = get_iam_policy(project_id)
    findings = analyze_iam_policy(iam_policy)

    if not findings:
        print("✅ No broad IAM policy findings detected. Good job!", file=sys.stderr)
    else:
        print("❌ Broad IAM Policy Findings Detected:")
        for i, finding in enumerate(findings):
            print(f"\n--- Finding {i+1} ---")
            print(f"  Member: {finding['member']}")
            print(f"  Role: {finding['role']}")
            print(f"  Recommendation: {finding['recommendation']}")

    print("\n-----------------------------------")
    print("💡 Note: This audit is a starting point. Always review custom roles and specific resource policies manually.")

if __name__ == "__main__":
    main()
