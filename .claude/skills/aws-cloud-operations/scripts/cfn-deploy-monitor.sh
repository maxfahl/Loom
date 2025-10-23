#!/bin/bash

# cfn-deploy-monitor.sh
#
# This script deploys or updates an AWS CloudFormation stack and monitors its progress.
# It waits for the stack operation to complete and reports the final status.
#
# Usage:
#   ./cfn-deploy-monitor.sh \
#       --stack-name <your-stack-name> \
#       --template-file <path-to-template.yaml> \
#       --region <aws-region> \
#       [--parameters "ParameterKey=Key1,ParameterValue=Value1 ParameterKey=Key2,ParameterValue=Value2"]
#
# Examples:
#   # Deploy a new stack with parameters
#   ./cfn-deploy-monitor.sh \
#       --stack-name MyWebServerStack \
#       --template-file ./templates/webserver.yaml \
#       --region us-east-1 \
#       --parameters "ParameterKey=InstanceType,ParameterValue=t3.micro ParameterKey=KeyPairName,ParameterValue=my-ssh-key"
#
#   # Update an existing stack without parameters
#   ./cfn-deploy-monitor.sh \
#       --stack-name MyDatabaseStack \
#       --template-file ./templates/database.yaml \
#       --region us-west-2
#
#   # Deploy a stack and capture outputs (requires jq)
#   ./cfn-deploy-monitor.sh --stack-name MyStack --template-file my-template.yaml --region us-east-1
#   if [ $? -eq 0 ]; then
#       echo "Stack deployed successfully. Outputs:"
#       aws cloudformation describe-stacks --stack-name MyStack --region us-east-1 --query "Stacks[0].Outputs" --output json
#   fi

set -e

# --- Configuration Variables ---
STACK_NAME=""
TEMPLATE_FILE=""
REGION=""
PARAMETERS=""

# --- Helper Functions ---
function print_help() {
    echo "Usage: $0 --stack-name <name> --template-file <file> --region <region> [--parameters \"Key=Val Key=Val\"]"
    echo ""
    echo "Options:"
    echo "  --stack-name      Name of the CloudFormation stack."
    echo "  --template-file   Path to the CloudFormation template file (YAML or JSON)."
    echo "  --region          AWS region to deploy the stack to (e.g., us-east-1)."
    echo "  --parameters      Optional. Space-separated list of CloudFormation parameters."
    echo "                    Format: \"ParameterKey=Key1,ParameterValue=Value1 ParameterKey=Key2,ParameterValue=Value2\""
    echo "  --help            Display this help message."
    echo ""
    echo "Examples:"
    echo "  ./cfn-deploy-monitor.sh \"
    echo "      --stack-name MyWebServerStack \"
    echo "      --template-file ./templates/webserver.yaml \"
    echo "      --region us-east-1 \"
    echo "      --parameters \"ParameterKey=InstanceType,ParameterValue=t3.micro\""
    echo ""
    echo "  ./cfn-deploy-monitor.sh \"
    echo "      --stack-name MyDatabaseStack \"
    echo "      --template-file ./templates/database.yaml \"
    echo "      --region us-west-2"
}

function parse_args() {
    while [[ $# -gt 0 ]]; do
        key="$1"
        case $key in
            --stack-name)
                STACK_NAME="$2"
                shift # past argument
                shift # past value
                ;;
            --template-file)
                TEMPLATE_FILE="$2"
                shift # past argument
                shift # value
                ;;
            --region)
                REGION="$2"
                shift # past argument
                shift # past value
                ;;
            --parameters)
                PARAMETERS="$2"
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

    if [[ -z "$STACK_NAME" || -z "$TEMPLATE_FILE" || -z "$REGION" ]]; then
        echo "Error: Missing required arguments." >&2
        print_help
        exit 1
    fi

    if [[ ! -f "$TEMPLATE_FILE" ]]; then
        echo "Error: Template file not found: $TEMPLATE_FILE" >&2
        exit 1
    fi
}

function deploy_stack() {
    echo "Attempting to deploy/update CloudFormation stack: ${STACK_NAME} in region: ${REGION}"
    
    local deploy_command=(
        aws cloudformation deploy \
        --stack-name "${STACK_NAME}" \
        --template-file "${TEMPLATE_FILE}" \
        --region "${REGION}" \
        --capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM CAPABILITY_AUTO_EXPAND
    )

    if [[ -n "$PARAMETERS" ]]; then
        deploy_command+=(--parameter-overrides ${PARAMETERS})
    fi

    # Check if stack exists to decide between create and update
    if aws cloudformation describe-stacks --stack-name "${STACK_NAME}" --region "${REGION}" &> /dev/null; then
        echo "Stack ${STACK_NAME} already exists. Attempting update."
        # For updates, we need to handle NO_CHANGES error gracefully
        if ! "${deploy_command[@]}" 2>&1 | grep -q "No updates are to be performed"; then
            echo "Update initiated for stack ${STACK_NAME}."
            wait_for_stack_completion "${STACK_NAME}" "${REGION}" "UPDATE"
        else
            echo "No changes detected for stack ${STACK_NAME}. Skipping update."
        fi
    else
        echo "Stack ${STACK_NAME} does not exist. Attempting creation."
        "${deploy_command[@]}"
        wait_for_stack_completion "${STACK_NAME}" "${REGION}" "CREATE"
    fi
}

function wait_for_stack_completion() {
    local stack_name="$1"
    local region="$2"
    local operation_type="$3"
    local success_status=""
    local failure_status=""

    case "$operation_type" in
        "CREATE")
            success_status="CREATE_COMPLETE"
            failure_status="CREATE_FAILED"
            ;; 
        "UPDATE")
            success_status="UPDATE_COMPLETE"
            failure_status="UPDATE_FAILED"
            ;; 
        *)
            echo "Invalid operation type: ${operation_type}" >&2
            exit 1
            ;; 
    esac

    echo "Waiting for stack ${stack_name} to reach ${success_status} or ${failure_status}..."
    
    # Use aws cloudformation wait for stack-create-complete or stack-update-complete
    if [[ "$operation_type" == "CREATE" ]]; then
        aws cloudformation wait stack-create-complete --stack-name "${stack_name}" --region "${region}"
    elif [[ "$operation_type" == "UPDATE" ]]; then
        aws cloudformation wait stack-update-complete --stack-name "${stack_name}" --region "${region}"
    fi

    local stack_status=$(aws cloudformation describe-stacks \
        --stack-name "${stack_name}" \
        --region "${region}" \
        --query "Stacks[0].StackStatus" \
        --output text 2>/dev/null)

    if [[ "$stack_status" == "${success_status}" ]]; then
        echo "Stack ${stack_name} ${operation_type} successful! Status: ${stack_status}"
        return 0
    else
        echo "Error: Stack ${stack_name} ${operation_type} failed! Status: ${stack_status}" >&2
        echo "Check CloudFormation console for details: https://${region}.console.aws.amazon.com/cloudformation/home?region=${region}#/stacks/events?stackId=${stack_name}" >&2
        return 1
    fi
}

# --- Main Execution ---
parse_args "$@"
deploy_stack

exit $? # Exit with the status of the last command (deploy_stack) 
