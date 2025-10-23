#!/usr/bin/env python3

"""
aws-resource-cleanup.py

This script identifies and optionally deletes unattached EBS volumes and
EBS snapshots older than a specified number of days in a given AWS region.

Usage:
    python3 aws-resource-cleanup.py --region <aws-region> [--dry-run] [--snapshot-age-days <days>]

Examples:
    # Dry run to find unused resources in us-east-1
    python3 aws-resource-cleanup.py --region us-east-1 --dry-run

    # Delete unattached EBS volumes and snapshots older than 30 days in us-west-2
    python3 aws-resource-cleanup.py --region us-west-2 --snapshot-age-days 30

    # Only delete unattached EBS volumes (default snapshot age is 0, so no snapshots will be considered old)
    python3 aws-resource-cleanup.py --region ap-southeast-1
"""

import argparse
import boto3
from datetime import datetime, timedelta, timezone
import sys

def get_current_utc_time():
    """Returns the current UTC time."""
    return datetime.now(timezone.utc)

def find_unattached_ebs_volumes(ec2_client):
    """
    Finds all unattached EBS volumes in the specified region.
    Returns a list of volume IDs.
    """
    print("Searching for unattached EBS volumes...")
    unattached_volumes = []
    try:
        paginator = ec2_client.get_paginator('describe_volumes')
        for page in paginator.paginate(Filters=[{'Name': 'status', 'Values': ['available']}]):
            for volume in page['Volumes']:
                unattached_volumes.append(volume['VolumeId'])
        print(f"Found {len(unattached_volumes)} unattached EBS volumes.")
    except Exception as e:
        print(f"Error finding unattached EBS volumes: {e}", file=sys.stderr)
    return unattached_volumes

def find_old_ebs_snapshots(ec2_client, age_days):
    """
    Finds all EBS snapshots older than the specified number of days.
    Returns a list of snapshot IDs.
    """
    print(f"Searching for EBS snapshots older than {age_days} days...")
    old_snapshots = []
    cutoff_date = get_current_utc_time() - timedelta(days=age_days)
    try:
        paginator = ec2_client.get_paginator('describe_snapshots')
        # Filter by owner-id to only consider snapshots owned by the current account
        for page in paginator.paginate(OwnerIds=['self']):
            for snapshot in page['Snapshots']:
                start_time = snapshot['StartTime']
                if start_time < cutoff_date:
                    old_snapshots.append(snapshot['SnapshotId'])
        print(f"Found {len(old_snapshots)} EBS snapshots older than {age_days} days.")
    except Exception as e:
        print(f"Error finding old EBS snapshots: {e}", file=sys.stderr)
    return old_snapshots

def delete_ebs_volume(ec2_client, volume_id, dry_run):
    """
    Deletes an EBS volume.
    """
    if dry_run:
        print(f"Dry run: Would delete EBS volume: {volume_id}")
        return True
    
    try:
        ec2_client.delete_volume(VolumeId=volume_id)
        print(f"Successfully deleted EBS volume: {volume_id}")
        return True
    except Exception as e:
        print(f"Error deleting EBS volume {volume_id}: {e}", file=sys.stderr)
        return False

def delete_ebs_snapshot(ec2_client, snapshot_id, dry_run):
    """
    Deletes an EBS snapshot.
    """
    if dry_run:
        print(f"Dry run: Would delete EBS snapshot: {snapshot_id}")
        return True
    
    try:
        ec2_client.delete_snapshot(SnapshotId=snapshot_id)
        print(f"Successfully deleted EBS snapshot: {snapshot_id}")
        return True
    except Exception as e:
        print(f"Error deleting EBS snapshot {snapshot_id}: {e}", file=sys.stderr)
        return False

def main():
    parser = argparse.ArgumentParser(
        description="Identifies and optionally deletes unattached EBS volumes and old EBS snapshots.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        '--region',
        required=True,
        help="The AWS region to operate in (e.g., us-east-1)."
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help="If specified, no resources will be deleted. Only reports what would be deleted."
    )
    parser.add_argument(
        '--snapshot-age-days',
        type=int,
        default=0,
        help="Delete EBS snapshots older than this many days. Set to 0 to disable snapshot cleanup. (Default: 0)"
    )

    args = parser.parse_args()

    region = args.region
    dry_run = args.dry_run
    snapshot_age_days = args.snapshot_age_days

    print(f"--- AWS Resource Cleanup in region: {region} ---")
    if dry_run:
        print("--- DRY RUN MODE: No resources will be deleted. ---")
    
    try:
        ec2_client = boto3.client('ec2', region_name=region)
    except Exception as e:
        print(f"Failed to create EC2 client for region {region}: {e}", file=sys.stderr)
        sys.exit(1)

    # --- EBS Volume Cleanup ---
    volumes_to_delete = find_unattached_ebs_volumes(ec2_client)
    if volumes_to_delete:
        print(f"Found {len(volumes_to_delete)} unattached EBS volumes to delete.")
        if not dry_run:
            confirm = input("Proceed with deleting these EBS volumes? (yes/no): ")
            if confirm.lower() == 'yes':
                for volume_id in volumes_to_delete:
                    delete_ebs_volume(ec2_client, volume_id, dry_run)
            else:
                print("EBS volume deletion cancelled.")
    else:
        print("No unattached EBS volumes found.")

    print("-" * 40)

    # --- EBS Snapshot Cleanup ---
    if snapshot_age_days > 0:
        snapshots_to_delete = find_old_ebs_snapshots(ec2_client, snapshot_age_days)
        if snapshots_to_delete:
            print(f"Found {len(snapshots_to_delete)} old EBS snapshots to delete.")
            if not dry_run:
                confirm = input("Proceed with deleting these EBS snapshots? (yes/no): ")
                if confirm.lower() == 'yes':
                    for snapshot_id in snapshots_to_delete:
                        delete_ebs_snapshot(ec2_client, snapshot_id, dry_run)
                else:
                    print("EBS snapshot deletion cancelled.")
        else:
            print("No old EBS snapshots found.")
    else:
        print("EBS snapshot cleanup is disabled (snapshot-age-days is 0).")

    print("--- Cleanup process finished. ---")

if __name__ == "__main__":
    main()
