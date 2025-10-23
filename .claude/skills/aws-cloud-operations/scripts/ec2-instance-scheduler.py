#!/usr/bin/env python3

"""
ec2-instance-scheduler.py

This script automatically stops or starts EC2 instances based on a specified tag.
It's useful for cost optimization by scheduling non-production instances to run only during business hours.

Usage:
    python3 ec2-instance-scheduler.py --region <aws-region> --action <start|stop> [--tag-key <key>] [--tag-value <value>] [--dry-run]

Examples:
    # Dry run: Find instances that would be stopped with default tag 'Schedule: off-hours'
    python3 ec2-instance-scheduler.py --region us-east-1 --action stop --dry-run

    # Stop instances tagged 'Environment: dev' and 'Schedule: off-hours' in us-west-2
    python3 ec2-instance-scheduler.py --region us-west-2 --action stop --tag-key Environment --tag-value dev

    # Start instances tagged 'Project: my-app' and 'Schedule: on-hours' in eu-central-1
    python3 ec2-instance-scheduler.py --region eu-central-1 --action start --tag-key Project --tag-value my-app
"""

import argparse
import boto3
import sys

class Color:
    RED = '\033[91m'
    YELLOW = '\033[93m'
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    END = '\033[0m'

def get_instances_by_tag(ec2_client, tag_key, tag_value, current_state):
    """
    Retrieves EC2 instances matching a tag key/value pair and current state.
    """
    filters = [
        {'Name': f'tag:{tag_key}', 'Values': [tag_value]},
        {'Name': 'instance-state-name', 'Values': [current_state]}
    ]
    instances = []
    try:
        response = ec2_client.describe_instances(Filters=filters)
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                instances.append(instance['InstanceId'])
    except Exception as e:
        print(f"{Color.RED}Error describing instances: {e}{Color.END}", file=sys.stderr)
    return instances

def stop_instances(ec2_client, instance_ids, dry_run):
    """
    Stops a list of EC2 instances.
    """
    if not instance_ids:
        print(f"{Color.YELLOW}No instances to stop.{Color.END}")
        return

    if dry_run:
        print(f"{Color.YELLOW}Dry run: Would stop instances: {instance_ids}{Color.END}")
        return

    try:
        print(f"{Color.BLUE}Stopping instances: {instance_ids}{Color.END}")
        ec2_client.stop_instances(InstanceIds=instance_ids)
        print(f"{Color.GREEN}Successfully initiated stop for instances: {instance_ids}{Color.END}")
    except Exception as e:
        print(f"{Color.RED}Error stopping instances {instance_ids}: {e}{Color.END}", file=sys.stderr)

def start_instances(ec2_client, instance_ids, dry_run):
    """
    Starts a list of EC2 instances.
    """
    if not instance_ids:
        print(f"{Color.YELLOW}No instances to start.{Color.END}")
        return

    if dry_run:
        print(f"{Color.YELLOW}Dry run: Would start instances: {instance_ids}{Color.END}")
        return

    try:
        print(f"{Color.BLUE}Starting instances: {instance_ids}{Color.END}")
        ec2_client.start_instances(InstanceIds=instance_ids)
        print(f"{Color.GREEN}Successfully initiated start for instances: {instance_ids}{Color.END}")
    except Exception as e:
        print(f"{Color.RED}Error starting instances {instance_ids}: {e}{Color.END}", file=sys.stderr)

def main():
    parser = argparse.ArgumentParser(
        description="Automatically stops or starts EC2 instances based on a specified tag.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        '--region',
        required=True,
        help="The AWS region to operate in (e.g., us-east-1)."
    )
    parser.add_argument(
        '--action',
        choices=['start', 'stop'],
        required=True,
        help="Action to perform: 'start' or 'stop' instances."
    )
    parser.add_argument(
        '--tag-key',
        default='Schedule',
        help="The tag key to filter instances by. (Default: Schedule)"
    )
    parser.add_argument(
        '--tag-value',
        default='off-hours',
        help="The tag value to filter instances by. (Default: off-hours for stop, on-hours for start)"
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help="If specified, no actions will be performed. Only reports what would happen."
    )

    args = parser.parse_args()

    region = args.region
    action = args.action
    tag_key = args.tag_key
    tag_value = args.tag_value
    dry_run = args.dry_run

    # Adjust default tag_value based on action if not explicitly provided
    if action == 'start' and args.tag_value == 'off-hours':
        tag_value = 'on-hours'
    elif action == 'stop' and args.tag_value == 'on-hours':
        tag_value = 'off-hours'

    print(f"{Color.BLUE}--- EC2 Instance Scheduler in region: {region} ---{Color.END}")
    print(f"{Color.BLUE}Action: {action.upper()}, Tag: {tag_key}={tag_value}{Color.END}")
    if dry_run:
        print(f"{Color.YELLOW}--- DRY RUN MODE: No actions will be performed. ---{Color.END}")
    
    try:
        ec2_client = boto3.client('ec2', region_name=region)
    except Exception as e:
        print(f"{Color.RED}Failed to create EC2 client for region {region}: {e}{Color.END}", file=sys.stderr)
        sys.exit(1)

    if action == 'stop':
        instances_to_process = get_instances_by_tag(ec2_client, tag_key, tag_value, 'running')
        stop_instances(ec2_client, instances_to_process, dry_run)
    elif action == 'start':
        instances_to_process = get_instances_by_tag(ec2_client, tag_key, tag_value, 'stopped')
        start_instances(ec2_client, instances_to_process, dry_run)

    print(f"{Color.BLUE}--- EC2 Instance Scheduling finished. ---{Color.END}")

if __name__ == "__main__":
    main()
