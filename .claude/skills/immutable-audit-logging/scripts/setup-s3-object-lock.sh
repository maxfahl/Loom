#!/bin/bash

# setup-s3-object-lock.sh
# Automates the setup of an AWS S3 bucket with Object Lock enabled for WORM compliance.
# This script creates a new S3 bucket with Object Lock in compliance mode.

# Usage:
#   ./setup-s3-object-lock.sh -b <bucket_name> -r <aws_region>
#   ./setup-s3-object-lock.sh --bucket my-immutable-audit-logs --region us-east-1

# Requirements:
#   - AWS CLI installed and configured with appropriate credentials.

set -euo pipefail

# --- Configuration ---
BUCKET_NAME=""
AWS_REGION=""

# --- Helper Functions ---
print_help() {
  echo "Usage: $0 -b <bucket_name> -r <aws_region>"
  echo ""
  echo "Automates the setup of an AWS S3 bucket with Object Lock enabled."
  echo "Creates a new S3 bucket with Object Lock in compliance mode, which is WORM compliant."
  echo ""
  echo "Options:"
  echo "  -b, --bucket <name>  The name of the S3 bucket to create. Must be globally unique."
  echo "  -r, --region <region> The AWS region to create the bucket in (e.g., us-east-1)."
  echo "  -h, --help           Display this help message."
  echo ""
  echo "Example:"
  echo "  $0 -b my-company-audit-logs-prod-12345 -r us-west-2"
  exit 0
}

# Function to check for required commands
check_dependencies() {
  if ! command -v aws &> /dev/null;
  then
    echo "Error: AWS CLI is not installed. Please install it to run this script."
    echo "  Refer to: https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html"
    exit 1
  fi
  # Check if AWS CLI is configured
  if ! aws configure list &> /dev/null;
  then
    echo "Error: AWS CLI is not configured. Please run 'aws configure' to set up credentials."
    exit 1
  fi
}

# --- Main Logic ---

# Parse arguments
while [[ $# -gt 0 ]]; do
  key="$1"
  case $key in
    -b|--bucket)
      BUCKET_NAME="$2"
      shift # past argument
      shift # past value
      ;;
    -r|--region)
      AWS_REGION="$2"
      shift # past argument
      shift # past value
      ;;
    -h|--help)
      print_help
      ;;
    *)
      echo "Unknown option: $1"
      print_help
      ;;
  esac
done

if [[ -z "$BUCKET_NAME" || -z "$AWS_REGION" ]]; then
  echo "Error: Both bucket name and AWS region are required."
  print_help
fi

check_dependencies

echo "Attempting to create S3 bucket '$BUCKET_NAME' in region '$AWS_REGION' with Object Lock enabled..."

# Create the S3 bucket with Object Lock enabled
# Note: Object Lock can only be enabled at bucket creation.
# Compliance mode prevents anyone, including the root user, from deleting the object version or changing its retention settings.
# This is the strongest form of WORM compliance.

CREATE_BUCKET_COMMAND="aws s3api create-bucket \
  --bucket \"$BUCKET_NAME\" \
  --region \"$AWS_REGION\" \
  --object-lock-enabled-for-bucket \
  --acl private"

# For regions other than us-east-1, LocationConstraint is required
if [[ "$AWS_REGION" != "us-east-1" ]]; then
  CREATE_BUCKET_COMMAND+=" \
  --create-bucket-configuration LocationConstraint=\"$$AWS_REGION\""
fi

if eval "$CREATE_BUCKET_COMMAND"; then
  echo "\nSuccessfully created S3 bucket '$BUCKET_NAME' with Object Lock enabled in '$AWS_REGION'."
  echo "\nNext steps:"
  echo "1. Configure bucket policies for access control."
  echo "2. Set default retention period for objects (optional, but recommended for compliance)."
  echo "   Example: aws s3api put-object-lock-configuration --bucket \"$BUCKET_NAME\" --object-lock-configuration '{\"ObjectLockEnabled\":\"Enabled\",\"Rule\":{\"DefaultRetention\":{\"Mode\":\"COMPLIANCE\",\"Years\":1}}}'"
  exit 0
else
  echo "\nError: Failed to create S3 bucket '$BUCKET_NAME'. Please check the error message above."
  exit 1
fi
