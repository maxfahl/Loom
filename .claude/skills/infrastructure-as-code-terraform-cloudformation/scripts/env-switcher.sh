#!/bin/bash

# env-switcher.sh
#
# Purpose: Simplifies switching between Terraform workspaces or managing environment-specific
#          configurations for CloudFormation deployments.
#
# Usage:
#   ./env-switcher.sh -e <environment> -t <iac_type> [-d <iac_directory>] [-p <aws_profile>] [-r <aws_region>]
#
# Examples:
#   # Switch Terraform to 'dev' workspace in the current directory
#   ./env-switcher.sh -e dev -t terraform
#
#   # Switch Terraform to 'prod' workspace in a specific directory
#   ./env-switcher.sh -e prod -t terraform -d /path/to/terraform/root
#
#   # Set up environment for CloudFormation 'staging' deployment
#   ./env-switcher.sh -e staging -t cloudformation -p my-staging-profile -r us-east-1
#
#   # Get help
#   ./env-switcher.sh --help

set -euo pipefail

# ANSI escape codes for colored output
COLOR_GREEN="\033[92m"
COLOR_RED="\033[91m"
COLOR_YELLOW="\033[93m"
COLOR_BLUE="\033[94m"
COLOR_RESET="\033[0m"

# --- Helper Functions ---

log_info() {
    echo -e "${COLOR_BLUE}[INFO]${COLOR_RESET} $1"
}

log_success() {
    echo -e "${COLOR_GREEN}[SUCCESS]${COLOR_RESET} $1"
}

log_warn() {
    echo -e "${COLOR_YELLOW}[WARN]${COLOR_RESET} $1" >&2
}

log_error() {
    echo -e "${COLOR_RED}[ERROR]${COLOR_RESET} $1" >&2
    exit 1
}

show_help() {
    echo "Usage: $0 -e <environment> -t <iac_type> [-d <iac_directory>] [-p <aws_profile>] [-r <aws_region>]"
    echo ""
    echo "  -e, --environment    Specify the target environment (e.g., dev, staging, prod)."
    echo "  -t, --iac-type       Specify the IaC tool: 'terraform' or 'cloudformation'."
    echo "  -d, --directory      Optional: The root directory of your IaC code. Defaults to current directory."
    echo "  -p, --profile        Optional (CloudFormation): AWS profile to use. Sets AWS_PROFILE env var."
    echo "  -r, --region         Optional (CloudFormation): AWS region to use. Sets AWS_REGION env var."
    echo "  -h, --help           Display this help message."
    echo ""
    echo "Terraform Specifics:"
    echo "  - Switches to or creates a Terraform workspace for the specified environment."
    echo "  - Requires 'terraform' CLI to be installed and available in PATH."
    echo ""
    echo "CloudFormation Specifics:"
    echo "  - Sets AWS_PROFILE and AWS_REGION environment variables if provided."
    echo "  - Suggests common CloudFormation parameter file names for the environment."
    echo "  - Requires 'aws' CLI to be installed and available in PATH for profile/region to be effective."
    echo ""
    echo "Examples:"
    echo "  ./env-switcher.sh -e dev -t terraform"
    echo "  ./env-switcher.sh -e prod -t terraform -d /path/to/terraform/root"
    echo "  ./env-switcher.sh -e staging -t cloudformation -p my-staging-profile -r us-east-1"
    exit 0
}

# --- Main Script Logic ---

ENVIRONMENT=""
IAC_TYPE=""
IAC_DIRECTORY="."
AWS_PROFILE=""
AWS_REGION=""

# Parse command-line arguments
while [[ "$#" -gt 0 ]]; do
    case "$1" in
        -e|--environment)
            ENVIRONMENT="$2"
            shift
            ;;
        -t|--iac-type)
            IAC_TYPE="$2"
            shift
            ;;
        -d|--directory)
            IAC_DIRECTORY="$2"
            shift
            ;;
        -p|--profile)
            AWS_PROFILE="$2"
            shift
            ;;
        -r|--region)
            AWS_REGION="$2"
            shift
            ;;
        -h|--help)
            show_help
            ;;
        *)
            log_error "Unknown parameter: $1. Use -h for help."
            ;;
    esac
    shift
done

# Validate required arguments
if [[ -z "$ENVIRONMENT" ]]; then
    log_error "Environment (-e) is required."
fi
if [[ -z "$IAC_TYPE" ]]; then
    log_error "IaC type (-t) is required."
fi

# Resolve absolute path for IAC_DIRECTORY
IAC_DIRECTORY=$(realpath "$IAC_DIRECTORY")
if [[ ! -d "$IAC_DIRECTORY" ]]; then
    log_error "Specified IaC directory '$IAC_DIRECTORY' does not exist."
fi

log_info "Setting up environment for: ${ENVIRONMENT} (Type: ${IAC_TYPE})"
log_info "Working directory: ${IAC_DIRECTORY}"

case "$IAC_TYPE" in
    terraform)
        if ! command -v terraform &> /dev/null; then
            log_error "Terraform CLI not found. Please install Terraform to use this feature."
        fi

        log_info "Navigating to Terraform directory: ${IAC_DIRECTORY}"
        pushd "$IAC_DIRECTORY" > /dev/null || log_error "Failed to change directory to ${IAC_DIRECTORY}"

        log_info "Initializing Terraform..."
        if ! terraform init -backend-config="environment=${ENVIRONMENT}" &> /dev/null; then
            log_warn "Terraform init failed or already initialized. Attempting to continue."
            # Re-run init without backend-config if it failed, in case backend is not environment-specific
            if ! terraform init &> /dev/null; then
                log_error "Terraform init failed. Please check your configuration."
            fi
        fi
        log_success "Terraform initialized."

        log_info "Checking for workspace '${ENVIRONMENT}'...";
        if ! terraform workspace select "${ENVIRONMENT}" &> /dev/null; then
            log_warn "Workspace '${ENVIRONMENT}' not found. Creating it..."
            if ! terraform workspace new "${ENVIRONMENT}"; then
                log_error "Failed to create Terraform workspace '${ENVIRONMENT}'."
            fi
            log_success "Workspace '${ENVIRONMENT}' created and selected."
        else
            log_success "Workspace '${ENVIRONMENT}' selected."
        fi

        popd > /dev/null || true # Return to original directory
        log_success "Terraform environment '${ENVIRONMENT}' is ready."
        ;;

    cloudformation)
        log_info "Setting up CloudFormation environment variables."

        if [[ -n "$AWS_PROFILE" ]]; then
            export AWS_PROFILE="$AWS_PROFILE"
            log_info "AWS_PROFILE set to: ${AWS_PROFILE}"
            if ! command -v aws &> /dev/null; then
                log_warn "AWS CLI not found. AWS_PROFILE might not be effective without it."
            fi
        fi

        if [[ -n "$AWS_REGION" ]]; then
            export AWS_REGION="$AWS_REGION"
            log_info "AWS_REGION set to: ${AWS_REGION}"
            if ! command -v aws &> /dev/null; then
                log_warn "AWS CLI not found. AWS_REGION might not be effective without it."
            fi
        fi

        log_info "For CloudFormation deployments in '${ENVIRONMENT}', consider using parameter files like:"
        echo "  - ${IAC_DIRECTORY}/parameters-${ENVIRONMENT}.json"
        echo "  - ${IAC_DIRECTORY}/parameters-${ENVIRONMENT}.yaml"
        echo "  - ${IAC_DIRECTORY}/${ENVIRONMENT}.parameters.json"
        echo "  - ${IAC_DIRECTORY}/${ENVIRONMENT}.parameters.yaml"
        log_success "CloudFormation environment '${ENVIRONMENT}' is ready. Remember to specify your template and parameter files."
        ;;

    *)
        log_error "Invalid IaC type: ${IAC_TYPE}. Must be 'terraform' or 'cloudformation'."
        ;;
esac
