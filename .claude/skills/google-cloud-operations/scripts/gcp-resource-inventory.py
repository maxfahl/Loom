#!/usr/bin/env python3
"""
gcp-resource-inventory.py

This script generates an inventory of active Google Cloud Platform (GCP) resources
across a specified project. It provides a summary of Compute Engine instances,
Cloud Storage buckets, and Cloud SQL instances.

Usage:
    python3 gcp-resource-inventory.py --project <YOUR_GCP_PROJECT_ID>
    python3 gcp-resource-inventory.py # Uses currently configured gcloud project

Example:
    python3 gcp-resource-inventory.py --project my-dev-project-123
    # Output will be a summary of resources found in 'my-dev-project-123'

    # To get help:
    python3 gcp-resource-inventory.py --help
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
    except subprocess.CalledProcessError as e:
        print("Error: No GCP project configured in gcloud CLI. Please run 'gcloud config set project PROJECT_ID' or provide --project argument.", file=sys.stderr)
        sys.exit(1)

def get_compute_instances(project_id):
    """
    Lists Compute Engine instances in the specified project.
    """
    print(f"🔍 Listing Compute Engine instances in project '{project_id}'...")
    instances = run_gcloud_command(["compute", "instances", "list"], project_id)
    if instances is None:
        return []
    return instances

def get_cloud_storage_buckets(project_id):
    """
    Lists Cloud Storage buckets in the specified project.
    """
    print(f"🔍 Listing Cloud Storage buckets in project '{project_id}'...")
    # gsutil does not have a --project flag for listing, it uses the active project.
    # We need to ensure gcloud is configured for the correct project or handle it.
    # For simplicity, we'll assume gcloud config is set correctly or the user provides it.
    # A more robust solution would involve setting the project for gsutil temporarily.
    try:
        # Temporarily set the project for gsutil if it's different from the current config
        current_gcloud_project = get_project_id_from_config()
        if current_gcloud_project != project_id:
            print(f"⚠️ gcloud config project is '{current_gcloud_project}', temporarily setting to '{project_id}' for gsutil.", file=sys.stderr)
            subprocess.run(["gcloud", "config", "set", "project", project_id], check=True, capture_output=True)

        result = subprocess.run(
            ["gsutil", "ls", "-p", project_id], # -p flag for project
            capture_output=True,
            text=True,
            check=True
        )
        buckets = [line.strip().replace('gs://', '') for line in result.stdout.splitlines() if line.strip()]
        return [{"name": b} for b in buckets] # Return in a similar format for consistency
    except subprocess.CalledProcessError as e:
        print(f"Error executing gsutil command: {e.cmd}", file=sys.stderr)
        print(f"Stderr: {e.stderr}", file=sys.stderr)
        return []
    finally:
        # Restore original gcloud project if it was changed
        if current_gcloud_project != project_id:
            subprocess.run(["gcloud", "config", "set", "project", current_gcloud_project], check=True, capture_output=True)


def get_cloud_sql_instances(project_id):
    """
    Lists Cloud SQL instances in the specified project.
    """
    print(f"🔍 Listing Cloud SQL instances in project '{project_id}'...")
    sql_instances = run_gcloud_command(["sql", "instances", "list"], project_id)
    if sql_instances is None:
        return []
    return sql_instances

def main():
    parser = argparse.ArgumentParser(
        description="Generate an inventory of active GCP resources.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "--project",
        help="The GCP project ID to scan. If not provided, uses the currently configured gcloud project."
    )
    args = parser.parse_args()

    project_id = args.project
    if not project_id:
        project_id = get_project_id_from_config()

    if not project_id:
        print("Error: No GCP project ID provided or configured.", file=sys.stderr)
        sys.exit(1)

    print(f"
✨ Generating GCP Resource Inventory for Project: {project_id} ✨
")

    instances = get_compute_instances(project_id)
    buckets = get_cloud_storage_buckets(project_id)
    sql_instances = get_cloud_sql_instances(project_id)

    print("
--- Inventory Summary ---")
    print(f"Compute Engine Instances: {len(instances)}")
    for instance in instances:
        print(f"  - {instance.get('name')} ({instance.get('zone')}, {instance.get('status')})")

    print(f"
Cloud Storage Buckets: {len(buckets)}")
    for bucket in buckets:
        print(f"  - {bucket.get('name')}")

    print(f"
Cloud SQL Instances: {len(sql_instances)}")
    for sql_instance in sql_instances:
        print(f"  - {sql_instance.get('name')} ({sql_instance.get('databaseVersion')}, {sql_instance.get('state')})")

    print("
-------------------------
")
    print("💡 Note: This is a basic inventory. For detailed information, use specific gcloud commands.")

if __name__ == "__main__":
    main()
