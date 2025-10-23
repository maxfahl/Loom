import argparse
import os
import sys

# ANSI escape codes for colored output
COLOR_GREEN = "\033[92m"
COLOR_RED = "\033[91m"
COLOR_YELLOW = "\033[93m"
COLOR_BLUE = "\033[94m"
COLOR_RESET = "\033[0m"

def log_info(message):
    print(f"{COLOR_BLUE}[INFO]{COLOR_RESET} {message}")

def log_success(message):
    print(f"{COLOR_GREEN}[SUCCESS]{COLOR_RESET} {message}")

def log_error(message):
    print(f"{COLOR_RED}[ERROR]{COLOR_RESET} {message}")
    sys.exit(1)

def create_terraform_module(module_name, output_dir):
    """Creates boilerplate files for a Terraform module."""
    module_path = os.path.join(output_dir, module_name)
    os.makedirs(module_path, exist_ok=True)

    log_info(f"Creating Terraform module '{module_name}' in {module_path}")

    # main.tf
    with open(os.path.join(module_path, "main.tf"), "w") as f:
        f.write(f"""# {module_name}/main.tf
#
# This file defines the resources managed by the '{module_name}' module.

# Example: AWS S3 Bucket
# resource "aws_s3_bucket" "example" {{
#   bucket = var.bucket_name
#   acl    = "private"
#
#   tags = {{
#     Name        = var.bucket_name
#     Environment = var.environment
#   }}
# }}
"""")
    log_info(f"Created {module_name}/main.tf")

    # variables.tf
    with open(os.path.join(module_path, "variables.tf"), "w") as f:
        f.write(f"""# {module_name}/variables.tf
#
# This file defines the input variables for the '{module_name}' module.

# Example: S3 Bucket Name
# variable "bucket_name" {{
#   description = "The name of the S3 bucket to create."
#   type        = string
# }}

# Example: Environment Tag
# variable "environment" {{
#   description = "The environment name (e.g., dev, staging, prod)."
#   type        = string
#   default     = "dev"
# }}
"""")
    log_info(f"Created {module_name}/variables.tf")

    # outputs.tf
    with open(os.path.join(module_path, "outputs.tf"), "w") as f:
        f.write(f"""# {module_name}/outputs.tf
#
# This file defines the output values exposed by the '{module_name}' module.

# Example: S3 Bucket ARN
# output "bucket_arn" {{
#   description = "The ARN of the S3 bucket."
#   value       = aws_s3_bucket.example.arn
# }}
"""")
    log_info(f"Created {module_name}/outputs.tf")

    # README.md
    with open(os.path.join(module_path, "README.md"), "w") as f:
        f.write(f"""# Terraform Module: {module_name}

This module provisions a {module_name} resource.

## Usage

```terraform
module "{module_name}" {{
  source = "./modules/{module_name}"

  # Example variables
  # bucket_name = "my-unique-{module_name}-bucket"
  # environment = "dev"
}}
```

## Requirements

| Name | Version |
|------|---------|
| terraform | >= 1.0 |
| aws | >= 4.0 |

## Providers

| Name | Version |
|------|---------|
| aws | >= 4.0 |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| # Example: bucket_name | The name of the S3 bucket to create. | `string` | n/a | yes |
| # Example: environment | The environment name (e.g., dev, staging, prod). | `string` | `"dev"` | no |

## Outputs

| Name | Description |
|------|-------------|
| # Example: bucket_arn | The ARN of the S3 bucket. |
"""")
    log_info(f"Created {module_name}/README.md")
    log_success(f"Terraform module '{module_name}' generated successfully!")

def create_cloudformation_stack(stack_name, output_dir):
    """Creates boilerplate files for a CloudFormation nested stack."""
    stack_path = os.path.join(output_dir, stack_name)
    os.makedirs(stack_path, exist_ok=True)

    log_info(f"Creating CloudFormation stack '{stack_name}' in {stack_path}")

    # template.yaml
    with open(os.path.join(stack_path, "template.yaml"), "w") as f:
        f.write(f"""AWSTemplateFormatVersion: '2010-09-09'
Description: CloudFormation template for {stack_name}

Parameters:
  # Example: EnvironmentName:
  #   Type: String
  #   Description: Name of the environment (e.g., dev, staging, prod)
  #   Default: dev

Resources:
  # Example: MyS3Bucket:
  #   Type: AWS::S3::Bucket
  #   Properties:
  #     BucketName: !Sub "${{EnvironmentName}}-{stack_name}-bucket"
  #     Tags:
  #       - Key: Environment
  #         Value: !Ref EnvironmentName

Outputs:
  # Example: S3BucketName:
  #   Description: Name of the S3 bucket created by this stack
  #   Value: !Ref MyS3Bucket
  #   Export:
  #     Name: !Sub "${{AWS::StackName}}-S3BucketName"
"""")
    log_info(f"Created {stack_name}/template.yaml")

    # parameters.yaml
    with open(os.path.join(stack_path, "parameters.yaml"), "w") as f:
        f.write(f"""# {stack_name}/parameters.yaml
#
# This file defines example parameters for the '{stack_name}' CloudFormation stack.

# Example:
# EnvironmentName: dev
"""")
    log_info(f"Created {stack_name}/parameters.yaml")

    # outputs.yaml (optional, but good for consistency with Terraform)
    with open(os.path.join(stack_path, "outputs.yaml"), "w") as f:
        f.write(f"""# {stack_name}/outputs.yaml
#
# This file can be used to document expected outputs from the '{stack_name}' CloudFormation stack.
# The actual outputs are defined in template.yaml.
"""")
    log_info(f"Created {stack_name}/outputs.yaml")

    # README.md
    with open(os.path.join(stack_path, "README.md"), "w") as f:
        f.write(f"""# CloudFormation Stack: {stack_name}

This stack provisions a {stack_name} resource.

## Deployment

To deploy this stack, use the AWS CLI:

```bash
aws cloudformation deploy \
  --template-file template.yaml \
  --stack-name {stack_name}-dev \
  --parameter-overrides file://parameters.yaml \
  --capabilities CAPABILITY_IAM
```

## Parameters

| Name | Description | Type | Default |
|------|-------------|------|---------|
| # Example: EnvironmentName | Name of the environment (e.g., dev, staging, prod) | `String` | `dev` |

## Outputs

| Name | Description |
|------|-------------|
| # Example: S3BucketName | Name of the S3 bucket created by this stack |
"""")
    log_info(f"Created {stack_name}/README.md")
    log_success(f"CloudFormation stack '{stack_name}' generated successfully!")


def main():
    parser = argparse.ArgumentParser(
        description="""
        Generates boilerplate for new Terraform modules or CloudFormation nested stacks.
        """,
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "iac_type",
        choices=["terraform", "cloudformation"],
        help="Type of IaC to generate: 'terraform' or 'cloudformation'."
    )
    parser.add_argument(
        "module_name",
        help="The name of the module or stack to create (e.g., 'vpc', 'ec2-instance')."
    )
    parser.add_argument(
        "-o", "--output-directory",
        default=".",
        help="""
        The directory where the new module/stack folder will be created.
        Defaults to the current directory ('.').
        """
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be created without actually creating files."
    )

    args = parser.parse_args()

    target_output_dir = os.path.abspath(args.output_directory)
    if not os.path.isdir(target_output_dir):
        log_error(f"Output directory '{target_output_dir}' does not exist.")

    if args.dry_run:
        log_info(f"Dry run: Would create {args.iac_type} '{args.module_name}' in {target_output_dir}")
        if args.iac_type == "terraform":
            log_info(f"  Files: {args.module_name}/main.tf, {args.module_name}/variables.tf, {args.module_name}/outputs.tf, {args.module_name}/README.md")
        else: # cloudformation
            log_info(f"  Files: {args.module_name}/template.yaml, {args.module_name}/parameters.yaml, {args.module_name}/outputs.yaml, {args.module_name}/README.md")
        sys.exit(0)

    if args.iac_type == "terraform":
        create_terraform_module(args.module_name, target_output_dir)
    elif args.iac_type == "cloudformation":
        create_cloudformation_stack(args.module_name, target_output_dir)

if __name__ == "__main__":
    main()
