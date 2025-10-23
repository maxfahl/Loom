
#!/bin/bash

# stripe-webhook-forwarder.sh
#
# Description:
# This script simplifies local Stripe webhook testing by wrapping the Stripe CLI.
# It automatically starts `stripe listen` and forwards events to a specified local endpoint.
# It handles common setup, ensures the Stripe CLI is available, and provides clear usage.
#
# Usage:
#   ./stripe-webhook-forwarder.sh --endpoint http://localhost:3000/api/webhook
#   ./stripe-webhook-forwarder.sh -e http://localhost:8080/stripe/webhooks --events payment_intent.succeeded,customer.subscription.updated
#   ./stripe-webhook-forwarder.sh --help
#
# Dependencies:
#   - Stripe CLI: https://stripe.com/docs/stripe-cli
#
# Configuration:
#   - Ensure your Stripe API keys are configured with the Stripe CLI (`stripe login`).
#   - Ensure your local server is running and listening on the specified endpoint.

# --- Configuration Variables ---
DEFAULT_ENDPOINT="http://localhost:3000/api/webhook"
DEFAULT_EVENTS="*" # Listen to all events by default

# --- Helper Functions ---
function show_help() {
    echo "Usage: $0 --endpoint <url> [--events <event_list>] [--help]"
    echo ""
    echo "Options:"
    echo "  -e, --endpoint <url>     : Your local webhook endpoint URL (default: $DEFAULT_ENDPOINT)."
    echo "  -v, --events <event_list>: Comma-separated list of specific events to listen for (default: $DEFAULT_EVENTS)."
    echo "                             Example: payment_intent.succeeded,customer.subscription.created"
    echo "  --help                   : Display this help message."
    echo ""
    echo "Examples:"
    echo "  $0 -e http://localhost:3000/api/webhook"
    echo "  $0 --endpoint http://localhost:8080/stripe/webhooks --events invoice.payment_succeeded,customer.created"
    echo "  $0 -e https://my-ngrok-tunnel.ngrok.io/stripe/webhooks # If using ngrok"
}

function log_info() {
    echo -e "\033[0;34m[INFO]\033[0m $1"
}

function log_success() {
    echo -e "\033[0;32m[SUCCESS]\033[0m $1"
}

function log_error() {
    echo -e "\033[0;31m[ERROR]\033[0m $1"
}

function check_stripe_cli() {
    if ! command -v stripe &> /dev/null;
    then
        log_error "Stripe CLI not found. Please install it: https://stripe.com/docs/stripe-cli"
        exit 1
    fi
    log_success "Stripe CLI found."
}

# --- Main Logic ---

ENDPOINT=""
EVENTS="$DEFAULT_EVENTS"

# Parse arguments
while [[ $# -gt 0 ]]; do
    key="$1"
    case $key in
        -e|--endpoint)
        ENDPOINT="$2"
        shift # past argument
        shift # past value
        ;;
        -v|--events)
        EVENTS="$2"
        shift # past argument
        shift # past value
        ;;
        --help)
        show_help
        exit 0
        ;;
        *)
        log_error "Unknown option: $1"
        show_help
        exit 1
        ;;
    esac
done

if [ -z "$ENDPOINT" ]; then
    log_warning "No endpoint specified. Using default: $DEFAULT_ENDPOINT"
    ENDPOINT="$DEFAULT_ENDPOINT"
fi

log_info "Checking for Stripe CLI..."
check_stripe_cli

log_info "Starting Stripe webhook listener..."
log_info "Forwarding events to: $ENDPOINT"
log_info "Listening for events: $EVENTS"

# Execute stripe listen command
# The --skip-verify flag is often useful for local development with self-signed certs or HTTP endpoints
stripe listen --forward-to "$ENDPOINT" --events "$EVENTS" --skip-verify

log_info "Stripe webhook listener stopped."
