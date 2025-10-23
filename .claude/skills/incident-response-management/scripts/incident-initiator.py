#!/usr/bin/env python3

"""
incident-initiator.py: Automates the initial steps of incident declaration.

This script is designed to streamline the incident declaration process by
automating the creation of a dedicated Slack channel, a Jira incident ticket,
and triggering a PagerDuty incident. It also sends an initial communication
to relevant stakeholders.

Usage:
    python incident-initiator.py --severity P1 --summary "Database connection issues affecting API" \
                                 [--commander "Jane Doe"] [--service "User API"] [--dry-run]

Configuration:
    Requires the following environment variables to be set for actual API calls:
    - SLACK_API_TOKEN: Slack Bot User OAuth Token
    - SLACK_INCIDENT_CHANNEL_PREFIX: Prefix for incident channels (e.g., "incident-")
    - JIRA_API_URL: Jira API base URL (e.g., "https://yourcompany.atlassian.net/rest/api/2")
    - JIRA_API_TOKEN: Jira API token
    - JIRA_PROJECT_KEY: Jira project key for incidents (e.g., "INC")
    - PAGERDUTY_API_TOKEN: PagerDuty API token
    - PAGERDUTY_SERVICE_ID: PagerDuty service ID to trigger incidents
    - PAGERDUTY_FROM_EMAIL: Email address of the user making the API request

    In dry-run mode, no actual API calls are made.
"""

import argparse
import os
import sys
import datetime
import json

# Mock API functions - In a real scenario, these would make actual HTTP requests
# to Slack, Jira, and PagerDuty APIs.
class MockSlack:
    def create_channel(self, name, is_private=False):
        print(f"  [MOCK SLACK] Creating channel: #{name} (private: {is_private})")
        return {"ok": True, "channel": {"id": "C12345", "name": name}}

    def post_message(self, channel_id, text):
        print(f"  [MOCK SLACK] Posting message to channel ID {channel_id}:\n    {text}")
        return {"ok": True, "ts": "123.456"}

class MockJira:
    def create_issue(self, project_key, summary, description, issue_type="Incident", severity=None):
        print(f"  [MOCK JIRA] Creating issue in project {project_key}:")
        print(f"    Summary: {summary}")
        print(f"    Description: {description}")
        print(f"    Type: {issue_type}")
        print(f"    Severity: {severity}")
        return {"id": "10000", "key": f"{project_key}-123", "self": "http://mockjira/browse/INC-123"}

class MockPagerDuty:
    def trigger_incident(self, service_id, from_email, summary, severity, details=None):
        print(f"  [MOCK PAGERDUTY] Triggering incident:")
        print(f"    Service ID: {service_id}")
        print(f"    From: {from_email}")
        print(f"    Summary: {summary}")
        print(f"    Severity: {severity}")
        print(f"    Details: {json.dumps(details, indent=2)}")
        return {"incident": {"id": "PD123", "incident_number": 1, "html_url": "http://mockpd/incidents/PD123"}}

def main():
    parser = argparse.ArgumentParser(
        description="Automates the initial steps of incident declaration.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("--severity", required=True, choices=["P0", "P1", "P2", "P3", "P4"],
                        help="Incident severity level (P0-P4).")
    parser.add_argument("--summary", required=True,
                        help="A concise summary of the incident.")
    parser.add_argument("--commander", default="Unassigned",
                        help="Name of the Incident Commander.")
    parser.add_argument("--service", default="Unknown Service",
                        help="Name of the affected service.")
    parser.add_argument("--dry-run", action="store_true",
                        help="If set, no actual API calls will be made, only print actions.")

    args = parser.parse_args()

    print(f"🚀 Initiating Incident: {args.summary} (Severity: {args.severity})")
    if args.dry_run:
        print("--- DRY RUN MODE --- No actual changes will be made. ---")

    # --- Configuration from Environment Variables ---
    # In a real script, you'd load these and check for their existence.
    # For this mock, we'll just acknowledge them.
    slack_api_token = os.getenv("SLACK_API_TOKEN", "MOCK_SLACK_TOKEN")
    slack_channel_prefix = os.getenv("SLACK_INCIDENT_CHANNEL_PREFIX", "incident-")
    jira_api_url = os.getenv("JIRA_API_URL", "https://mockjira.atlassian.net/rest/api/2")
    jira_api_token = os.getenv("JIRA_API_TOKEN", "MOCK_JIRA_TOKEN")
    jira_project_key = os.getenv("JIRA_PROJECT_KEY", "INC")
    pagerduty_api_token = os.getenv("PAGERDUTY_API_TOKEN", "MOCK_PAGERDUTY_TOKEN")
    pagerduty_service_id = os.getenv("PAGERDUTY_SERVICE_ID", "MOCK_SERVICE_ID")
    pagerduty_from_email = os.getenv("PAGERDUTY_FROM_EMAIL", "incident-bot@example.com")

    if not args.dry_run:
        print("Note: For actual execution, ensure environment variables like SLACK_API_TOKEN, JIRA_API_TOKEN, etc., are set.")

    # --- Prepare Incident Details ---
    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    incident_id_slug = args.summary.lower().replace(" ", "-")[:30] # Shorten for channel name
    incident_channel_name = f"{slack_channel_prefix}{incident_id_slug}-{timestamp}".replace("_", "-")
    incident_title = f"[{args.severity}] {args.summary}"
    incident_description = f"""
    * **Severity:** {args.severity}
    * **Summary:** {args.summary}
    * **Affected Service:** {args.service}
    * **Incident Commander:** {args.commander}
    * **Time Declared (UTC):** {datetime.datetime.utcnow().isoformat()}Z
    """

    # --- Step 1: Create Slack Channel ---
    print("\n--- Creating Slack Channel ---")
    slack = MockSlack()
    slack_channel_info = None
    if not args.dry_run:
        # In a real scenario, you'd use a Slack client library here
        # from slack_sdk import WebClient
        # client = WebClient(token=slack_api_token)
        # try:
        #     slack_channel_info = client.conversations_create(name=incident_channel_name, is_private=False)
        # except Exception as e:
        #     print(f"ERROR creating Slack channel: {e}")
        #     sys.exit(1)
        pass # Mocked above
    slack_channel_info = slack.create_channel(incident_channel_name) # Always call mock for dry-run output

    if slack_channel_info and slack_channel_info["ok"]:
        channel_id = slack_channel_info["channel"]["id"]
        print(f"✅ Slack channel '#{incident_channel_name}' created (ID: {channel_id}).")
    else:
        print(f"❌ Failed to create Slack channel. Check logs for details.")
        if not args.dry_run: sys.exit(1)

    # --- Step 2: Create Jira Ticket ---
    print("\n--- Creating Jira Ticket ---")
    jira = MockJira()
    jira_issue_info = None
    if not args.dry_run:
        # In a real scenario, you'd use a Jira client library here
        # from jira import JIRA
        # jira_client = JIRA(server=jira_api_url, token_auth=jira_api_token)
        # try:
        #     jira_issue_info = jira_client.create_issue(
        #         project={'key': jira_project_key},
        #         summary=incident_title,
        #         description=incident_description,
        #         issuetype={'name': 'Incident'},
        #         priority={'name': args.severity} # Map P0-P4 to Jira priorities
        #     )
        # except Exception as e:
        #     print(f"ERROR creating Jira issue: {e}")
        #     sys.exit(1)
        pass # Mocked above
    jira_issue_info = jira.create_issue(jira_project_key, incident_title, incident_description, severity=args.severity) # Always call mock for dry-run output

    if jira_issue_info:
        print(f"✅ Jira ticket '{jira_issue_info['key']}' created: {jira_issue_info['self']}")
    else:
        print(f"❌ Failed to create Jira ticket. Check logs for details.")
        if not args.dry_run: sys.exit(1)

    # --- Step 3: Trigger PagerDuty Incident ---
    print("\n--- Triggering PagerDuty Incident ---")
    pagerduty = MockPagerDuty()
    pd_incident_info = None
    if not args.dry-run:
        # In a real scenario, you'd use a PagerDuty client library or direct HTTP call
        # import requests
        # headers = {
        #     "Accept": "application/vnd.pagerduty+json;version=2",
        #     "Authorization": f"Token token={pagerduty_api_token}",
        #     "From": pagerduty_from_email
        # }
        # payload = {
        #     "incident": {
        #         "type": "incident",
        #         "title": incident_title,
        #         "service": {"id": pagerduty_service_id, "type": "service_reference"},
        #         "body": {"type": "incident_body", "details": incident_description},
        #         "urgency": "high" if args.severity in ["P0", "P1"] else "low"
        #     }
        # }
        # try:
        #     response = requests.post("https://api.pagerduty.com/incidents", headers=headers, json=payload)
        #     response.raise_for_status()
        #     pd_incident_info = response.json()
        # except Exception as e:
        #     print(f"ERROR triggering PagerDuty incident: {e}")
        #     sys.exit(1)
        pass # Mocked above
    pd_incident_info = pagerduty.trigger_incident(
        pagerduty_service_id,
        pagerduty_from_email,
        incident_title,
        args.severity,
        details={"summary": args.summary, "service": args.service, "commander": args.commander}
    ) # Always call mock for dry-run output

    if pd_incident_info:
        print(f"✅ PagerDuty incident '{pd_incident_info['incident']['incident_number']}' triggered: {pd_incident_info['incident']['html_url']}")
    else:
        print(f"❌ Failed to trigger PagerDuty incident. Check logs for details.")
        if not args.dry_run: sys.exit(1)

    # --- Step 4: Post Initial Communication to Slack ---
    print("\n--- Posting Initial Communication to Slack ---")
    initial_message = f"""
    <!here> *INCIDENT DECLARED: {incident_title}*
    *Severity:* {args.severity}
    *Affected Service:* {args.service}
    *Summary:* {args.summary}
    *Incident Commander:* {args.commander}
    *Jira Ticket:* {jira_issue_info['self'] if jira_issue_info else 'N/A'}
    *PagerDuty Incident:* {pd_incident_info['incident']['html_url'] if pd_incident_info else 'N/A'}
    *Next Update:* As soon as more information is available, or within 15-30 minutes.
    """
    if not args.dry_run:
        # client.chat_postMessage(channel=channel_id, text=initial_message)
        pass # Mocked above
    slack.post_message(channel_id, initial_message) # Always call mock for dry-run output
    print(f"✅ Initial incident message posted to Slack channel '#{incident_channel_name}'.")

    print("\n🎉 Incident initiation complete!")
    print(f"Slack Channel: #{incident_channel_name}")
    print(f"Jira Ticket: {jira_issue_info['self'] if jira_issue_info else 'N/A'}")
    print(f"PagerDuty Incident: {pd_incident_info['incident']['html_url'] if pd_incident_info else 'N/A'}")

if __name__ == "__main__":
    main()
