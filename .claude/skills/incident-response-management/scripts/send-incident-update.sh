#!/bin/bash

# send-incident-update.sh: Formats and sends pre-defined incident updates to configured communication channels.
#
# This script helps in sending consistent and timely updates during an incident
# to various stakeholders. It supports sending updates to Slack via webhook
# and can be extended for other channels like email or status pages.
#
# Usage:
#   ./send-incident-update.sh --incident-id INC-123 --status "Investigating" \
#                             --message "Team is actively debugging database connection issues." \
#                             [--channel slack] [--dry-run]
#
# Configuration:
#   - SLACK_WEBHOOK_URL: Environment variable for the Slack webhook URL.
#                        (e.g., YOUR_SLACK_WEBHOOK_URL_HERE)
#   - EMAIL_RECIPIENTS: Environment variable for a comma-separated list of email recipients.
#
# In dry-run mode, no actual messages are sent.

# --- Helper Functions ---
log_info() {
  echo "[INFO] $1"
}

log_warn() {
  echo "[WARN] $1"
}

log_error() {
  echo "[ERROR] $1"
  exit 1
}

show_help() {
  echo "Usage: $0 --incident-id <ID> --status <STATUS> --message <MESSAGE> [--channel <CHANNEL>] [--dry-run]"
  echo ""
  echo "Arguments:"
  echo "  --incident-id <ID>      : Unique identifier for the incident (e.g., INC-123)."
  echo "  --status <STATUS>       : Current status of the incident (e.g., Investigating, Identified, Mitigated, Resolved)."
  echo "  --message <MESSAGE>     : A concise update message for stakeholders."
  echo "  --channel <CHANNEL>     : Optional. Specify communication channel (e.g., slack, email). Defaults to all configured."
  echo "  --dry-run               : Optional. If set, no actual messages will be sent, only print actions."
  echo ""
  echo "Configuration:"
  echo "  SLACK_WEBHOOK_URL: Environment variable for Slack webhook URL."
  echo "  EMAIL_RECIPIENTS: Environment variable for comma-separated email recipients."
  exit 0
}

# --- Argument Parsing ---
INCIDENT_ID=""
STATUS=""
MESSAGE=""
CHANNEL="all"
DRY_RUN=false

while [[ $# -gt 0 ]]; do
  key="$1"
  case $key in
    --incident-id)
      INCIDENT_ID="$2"
      shift # past argument
      shift # past value
      ;;
    --status)
      STATUS="$2"
      shift # past argument
      shift # past value
      ;;
    --message)
      MESSAGE="$2"
      shift # past argument
      shift # past value
      ;;
    --channel)
      CHANNEL="$2"
      shift # past argument
      shift # past value
      ;;
    --dry-run)
      DRY_RUN=true
      shift # past argument
      ;;
    -h|--help)
      show_help
      ;;
    *)
      log_error "Unknown option: $1"
      ;;
  esac
done

# --- Validate Arguments ---
if [ -z "$INCIDENT_ID" ] || [ -z "$STATUS" ] || [ -z "$MESSAGE" ]; then
  log_error "Missing required arguments. Incident ID, Status, and Message are mandatory.\nRun with --help for usage."
fi

# --- Main Logic ---
log_info "Preparing incident update for Incident ID: $INCIDENT_ID (Status: $STATUS)"

if $DRY_RUN; then
  log_info "--- DRY RUN MODE --- No actual messages will be sent. ---"
fi

CURRENT_TIME=$(date -u +"%Y-%m-%d %H:%M:%S UTC")

# --- Slack Notification ---
if [[ "$CHANNEL" == "slack" || "$CHANNEL" == "all" ]]; then
  SLACK_WEBHOOK_URL="$SLACK_WEBHOOK_URL"
  if [ -z "$SLACK_WEBHOOK_URL" ]; then
    log_warn "SLACK_WEBHOOK_URL environment variable not set. Skipping Slack notification."
  else
    SLACK_MESSAGE="{\"text\":\"*Incident Update: $INCIDENT_ID - $STATUS*\\n*Time:* $CURRENT_TIME\\n*Message:* $MESSAGE\"}"
    log_info "Sending Slack update..."
    if $DRY_RUN; then
      echo "  [DRY RUN] Would send to Slack: $SLACK_MESSAGE"
    else
      # In a real scenario, ensure curl is installed and handle its exit code
      curl -X POST -H 'Content-type: application/json' --data "$SLACK_MESSAGE" "$SLACK_WEBHOOK_URL" > /dev/null
      if [ $? -eq 0 ]; then
        log_info "✅ Slack update sent successfully."
      else
        log_error "❌ Failed to send Slack update. Check webhook URL and network connectivity."
      fi
    fi
  fi
fi

# --- Email Notification ---
if [[ "$CHANNEL" == "email" || "$CHANNEL" == "all" ]]; then
  EMAIL_RECIPIENTS="$EMAIL_RECIPIENTS"
  if [ -z "$EMAIL_RECIPIENTS" ]; then
    log_warn "EMAIL_RECIPIENTS environment variable not set. Skipping email notification."
  else
    EMAIL_SUBJECT="Incident Update: $INCIDENT_ID - $STATUS"
    EMAIL_BODY="Time: $CURRENT_TIME\nIncident ID: $INCIDENT_ID\nStatus: $STATUS\nMessage: $MESSAGE\n\n---\nThis is an automated incident update."
    log_info "Sending email update to $EMAIL_RECIPIENTS..."
    if $DRY_RUN; then
      echo "  [DRY RUN] Would send email with subject \"$EMAIL_SUBJECT\" and body:\n$EMAIL_BODY"
    else
      # In a real scenario, ensure 'mail' command is configured or use a more robust email client
      echo -e "$EMAIL_BODY" | mail -s "$EMAIL_SUBJECT" "$EMAIL_RECIPIENTS"
      if [ $? -eq 0 ]; then
        log_info "✅ Email update sent successfully."
      else
        log_error "❌ Failed to send email update. Check 'mail' command configuration or recipients."
      fi
    fi
  fi
fi

log_info "Incident update process completed."
