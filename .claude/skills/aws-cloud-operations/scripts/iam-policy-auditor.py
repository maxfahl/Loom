#!/usr/bin/env python3

"""
iam-policy-auditor.py

This script audits customer-managed IAM policies in a given AWS region for overly permissive statements.
It identifies policies that grant broad access (e.g., `Action: "*"` or `Resource: "*"` with `Effect: Allow`).

Usage:
    python3 iam-policy-auditor.py --region <aws-region> [--policy-name-filter <filter-string>]

Examples:
    # Audit all customer-managed policies in us-east-1
    python3 iam-policy-auditor.py --region us-east-1

    # Audit policies containing "Admin" in their name in us-west-2
    python3 iam-policy-auditor.py --region us-west-2 --policy-name-filter Admin
"""

import argparse
import boto3
import json
import sys

class Color:
    RED = '\033[91m'
    YELLOW = '\033[93m'
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    END = '\033[0m'

def check_policy_statement(statement):
    """
    Checks an individual IAM policy statement for overly permissive configurations.
    Returns a string describing the issue or None if no issue found.
    """
    if statement.get('Effect') == 'Allow':
        actions = statement.get('Action', [])
        resources = statement.get('Resource', [])

        # Normalize actions and resources to lists for consistent checking
        if isinstance(actions, str): actions = [actions]
        if isinstance(resources, str): resources = [resources]

        # Check for wildcard actions
        if '*' in actions:
            return f"Wildcard action ('Action: \"*\" ') found."
        
        # Check for wildcard resources
        if '*' in resources:
            return f"Wildcard resource ('Resource: \"*\" ') found."

        # Check for actions that are effectively wildcard (e.g., service:*)
        for action in actions:
            if action.endswith(':*'):
                return f"Wildcard action prefix ('{action}') found."

    return None

def audit_iam_policies(iam_client, policy_name_filter=None):
    """
    Audits customer-managed IAM policies for overly permissive statements.
    """
    print(f"{Color.BLUE}Starting IAM policy audit...{Color.END}")
    issues_found = []

    paginator = iam_client.get_paginator('list_policies')
    try:
        for page in paginator.paginate(Scope='Local'): # Local scope for customer-managed policies
            for policy in page['Policies']:
                policy_name = policy['PolicyName']
                policy_arn = policy['Arn']

                if policy_name_filter and policy_name_filter.lower() not in policy_name.lower():
                    continue

                print(f"  {Color.BLUE}Checking policy: {policy_name} ({policy_arn}){Color.END}")

                # Get the default policy version
                default_version_id = policy['DefaultVersionId']
                policy_version = iam_client.get_policy_version(
                    PolicyArn=policy_arn,
                    VersionId=default_version_id
                )
                policy_document = policy_version['PolicyVersion']['Document']

                statements = policy_document.get('Statement', [])
                if not isinstance(statements, list):
                    statements = [statements] # Handle single statement not in a list

                for i, statement in enumerate(statements):
                    issue = check_policy_statement(statement)
                    if issue:
                        issues_found.append({
                            'PolicyName': policy_name,
                            'PolicyArn': policy_arn,
                            'StatementIndex': i,
                            'Issue': issue,
                            'Statement': statement
                        })
    except Exception as e:
        print(f"{Color.RED}Error auditing IAM policies: {e}{Color.END}", file=sys.stderr)
        return []

    return issues_found

def main():
    parser = argparse.ArgumentParser(
        description="Audits customer-managed IAM policies for overly permissive statements.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        '--region',
        required=True,
        help="The AWS region to operate in (e.g., us-east-1)."
    )
    parser.add_argument(
        '--policy-name-filter',
        help="Optional. Filter policies by name (case-insensitive substring match)."
    )

    args = parser.parse_args()

    region = args.region
    policy_name_filter = args.policy_name_filter

    try:
        iam_client = boto3.client('iam', region_name=region)
    except Exception as e:
        print(f"{Color.RED}Failed to create IAM client for region {region}: {e}{Color.END}", file=sys.stderr)
        sys.exit(1)

    issues = audit_iam_policies(iam_client, policy_name_filter)

    print(f"\n{Color.BLUE}--- IAM Policy Audit Results ---{Color.END}")
    if issues:
        print(f"{Color.RED}Found {len(issues)} potential security issues in IAM policies:{Color.END}")
        for issue in issues:
            print(f"\n  {Color.YELLOW}Policy Name: {issue['PolicyName']}{Color.END}")
            print(f"  Policy ARN: {issue['PolicyArn']}")
            print(f"  Issue: {issue['Issue']}")
            print(f"  Problematic Statement (Index {issue['StatementIndex']}):")
            print(f"    {json.dumps(issue['Statement'], indent=2).replace('\n', '\n    ')}")
    else:
        print(f"{Color.GREEN}No overly permissive policies found matching criteria.{Color.END}")

    print(f"\n{Color.BLUE}--- Audit Finished ---{Color.END}")

if __name__ == "__main__":
    main()
