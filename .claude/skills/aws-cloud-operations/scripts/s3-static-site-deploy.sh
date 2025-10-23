#!/bin/bash

# s3-static-site-deploy.sh
#
# This script synchronizes a local directory to an S3 bucket configured for static website hosting.
# It sets appropriate Cache-Control headers and can optionally invalidate a CloudFront distribution.
#
# Usage:
#   ./s3-static-site-deploy.sh \
#       --bucket-name <your-s3-bucket-name> \
#       --local-path <path-to-local-site-directory> \
#       --region <aws-region> \
#       [--cloudfront-distribution-id <your-cloudfront-id>] \
#       [--exclude <pattern>] \
#       [--include <pattern>]
#
# Examples:
#   # Deploy a local site to an S3 bucket in us-east-1
#   ./s3-static-site-deploy.sh \
#       --bucket-name my-static-website-bucket \
#       --local-path ./dist \
#       --region us-east-1
#
#   # Deploy and invalidate CloudFront cache
#   ./s3-static-site-deploy.sh \
#       --bucket-name my-static-website-bucket \
#       --local-path ./build \
#       --region us-east-1 \
#       --cloudfront-distribution-id E1234567890ABCDEF
#
#   # Deploy, excluding .DS_Store files
#   ./s3-static-site-deploy.sh \
#       --bucket-name my-static-website-bucket \
#       --local-path ./public \
#       --region us-east-1 \
#       --exclude ".DS_Store"

set -e

# --- Configuration Variables ---
BUCKET_NAME=""
LOCAL_PATH=""
REGION=""
CLOUDFRONT_DISTRIBUTION_ID=""
EXCLUDE_PATTERNS=()
INCLUDE_PATTERNS=()

# --- Helper Functions ---
function print_help() {
    echo "Usage: $0 --bucket-name <name> --local-path <path> --region <region> [--cloudfront-distribution-id <id>] [--exclude <pattern>] [--include <pattern>]"
    echo ""
    echo "Options:"
    echo "  --bucket-name               Name of the S3 bucket for the static website."
    echo "  --local-path                Path to the local directory containing the static site files."
    echo "  --region                    AWS region where the S3 bucket is located (e.g., us-east-1)."
    echo "  --cloudfront-distribution-id Optional. ID of the CloudFront distribution to invalidate after deployment."
    echo "  --exclude                   Optional. A pattern to exclude files from sync (can be used multiple times)."
    echo "  --include                   Optional. A pattern to include files in sync (can be used multiple times)."
    echo "  --help                      Display this help message."
    echo ""
    echo "Examples:"
    echo "  # Deploy a local site to an S3 bucket in us-east-1"
    echo "  ./s3-static-site-deploy.sh \"
    echo "      --bucket-name my-static-website-bucket \"
    echo "      --local-path ./dist \"
    echo "      ----region us-east-1"
    echo ""
    echo "  # Deploy and invalidate CloudFront cache"
    echo "  ./s3-static-site-deploy.sh \"
    echo "      --bucket-name my-static-website-bucket \"
    echo "      --local-path ./build \"
    echo "      --region us-east-1 \"
    echo "      --cloudfront-distribution-id E1234567890ABCDEF"
}

function parse_args() {
    while [[ $# -gt 0 ]]; do
        key="$1"
        case $key in
            --bucket-name)
                BUCKET_NAME="$2"
                shift # past argument
                shift # past value
                ;;
            --local-path)
                LOCAL_PATH="$2"
                shift # past argument
                shift # past value
                ;;
            --region)
                REGION="$2"
                shift # past argument
                shift # past value
                ;;
            --cloudfront-distribution-id)
                CLOUDFRONT_DISTRIBUTION_ID="$2"
                shift # past argument
                shift # past value
                ;;
            --exclude)
                EXCLUDE_PATTERNS+=("--exclude \"$2\"")
                shift # past argument
                shift # past value
                ;;
            --include)
                INCLUDE_PATTERNS+=("--include \"$2\"")
                shift # past argument
                shift # past value
                ;;
            --help)
                print_help
                exit 0
                ;;
            *)
                echo "Unknown option: $1"
                print_help
                exit 1
                ;;
        esac
done

    if [[ -z "$BUCKET_NAME" || -z "$LOCAL_PATH" || -z "$REGION" ]]; then
        echo "Error: Missing required arguments." >&2
        print_help
        exit 1
    fi

    if [[ ! -d "$LOCAL_PATH" ]]; then
        echo "Error: Local path not found or is not a directory: $LOCAL_PATH" >&2
        exit 1
    fi
}

function sync_to_s3() {
    echo "Synchronizing local path '${LOCAL_PATH}' to s3://${BUCKET_NAME} in region ${REGION}..."

    local s3_sync_command=(
        aws s3 sync "${LOCAL_PATH}" "s3://${BUCKET_NAME}" \
        --region "${REGION}" \
        --delete \
        --cache-control "max-age=31536000, public, immutable" \
        --exclude "*.html" \
        --exclude "*.json" \
        --exclude "*.xml" \
        --exclude "*.txt" \
        --exclude "*.css" \
        --exclude "*.js"
    )

    # Add user-defined exclude/include patterns
    for pattern in "${EXCLUDE_PATTERNS[@]}"; do
        s3_sync_command+=("$pattern")
    done
    for pattern in "${INCLUDE_PATTERNS[@]}"; do
        s3_sync_command+=("$pattern")
    done

    # Execute the main sync command for long-lived assets
    echo "Running: ${s3_sync_command[@]}"
    "${s3_sync_command[@]}"
    if [ $? -ne 0 ]; then
        echo "Error: S3 sync failed for long-lived assets." >&2
        exit 1
    fi

    # Sync HTML, JSON, XML, TXT, CSS, JS files with shorter or no-cache control
    echo "Synchronizing HTML, JSON, XML, TXT, CSS, JS files with specific cache control..."
    local s3_sync_short_cache_command=(
        aws s3 sync "${LOCAL_PATH}" "s3://${BUCKET_NAME}" \
        --region "${REGION}" \
        --delete \
        --cache-control "no-cache, no-store, must-revalidate" \
        --exclude "*" \
        --include "*.html" \
        --include "*.json" \
        --include "*.xml" \
        --include "*.txt" \
        --include "*.css" \
        --include "*.js"
    )

    # Add user-defined exclude/include patterns (if they override the defaults)
    for pattern in "${EXCLUDE_PATTERNS[@]}"; do
        s3_sync_short_cache_command+=("$pattern")
    done
    for pattern in "${INCLUDE_PATTERNS[@]}"; do
        s3_sync_short_cache_command+=("$pattern")
    done

    echo "Running: ${s3_sync_short_cache_command[@]}"
    "${s3_sync_short_cache_command[@]}"
    if [ $? -ne 0 ]; then
        echo "Error: S3 sync failed for short-lived assets." >&2
        exit 1
    fi

    echo "S3 synchronization complete."
}

function invalidate_cloudfront_cache() {
    if [[ -n "$CLOUDFRONT_DISTRIBUTION_ID" ]]; then
        echo "Creating CloudFront invalidation for distribution ${CLOUDFRONT_DISTRIBUTION_ID}..."
        local invalidation_id=$(aws cloudfront create-invalidation \
            --distribution-id "${CLOUDFRONT_DISTRIBUTION_ID}" \
            --paths "/*" \
            --query "Invalidation.Id" \
            --output text \
            --region "${REGION}")

        if [ $? -eq 0 ]; then
            echo "CloudFront invalidation started. Invalidation ID: ${invalidation_id}"
            echo "Waiting for invalidation to complete... (This may take several minutes)"
            aws cloudfront wait invalidation-completed \
                --distribution-id "${CLOUDFRONT_DISTRIBUTION_ID}" \
                --id "${invalidation_id}" \
                --region "${REGION}"
            echo "CloudFront invalidation completed."
        else
            echo "Error: Failed to create CloudFront invalidation." >&2
            exit 1
        fi
    else
        echo "No CloudFront distribution ID provided. Skipping CloudFront invalidation."
    fi
}

# --- Main Execution ---
parse_args "$@"
sync_to_s3
invalidate_cloudfront_cache

echo "Deployment process finished successfully!"
