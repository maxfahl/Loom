---
name: aws-cloud-operations
version: 1.0.0
category: Cloud Operations / AWS
tags: AWS, Cloud, Operations, CLI, Boto3, CloudFormation, CDK, Security, Cost Optimization, Automation, IaC
description: Enables efficient and secure management of AWS cloud resources through CLI and automation.
---

# AWS Cloud Operations Skill

## 1. Skill Purpose

This skill empowers Claude to effectively manage, automate, secure, and optimize resources within the Amazon Web Services (AWS) cloud environment. It covers best practices for using the AWS Command Line Interface (CLI), Python Boto3 SDK, and Infrastructure as Code (IaC) tools like AWS CloudFormation and AWS CDK, ensuring adherence to operational excellence, security, reliability, performance efficiency, and cost optimization.

## 2. When to Activate This Skill

Activate this skill when the task involves:
*   Interacting with AWS services via command-line or programmatic scripts.
*   Automating repetitive AWS operational tasks (e.g., resource provisioning, monitoring, cleanup).
*   Implementing or managing AWS infrastructure using Infrastructure as Code (IaC).
*   Ensuring AWS security, compliance, and governance.
*   Optimizing AWS costs and resource utilization.
*   Troubleshooting, monitoring, or auditing AWS environments.
*   Developing or reviewing AWS-related automation scripts (Bash, Python/Boto3).

## 3. Core Knowledge

Claude should possess fundamental knowledge in the following areas:

### 3.1. AWS CLI
*   **Basic Syntax**: `aws <service> <command> <subcommand> --parameter value`.
*   **Configuration**: Managing named profiles (`~/.aws/config`, `~/.aws/credentials`), default region, and output formats (JSON, YAML, text, table).
*   **Authentication**: Understanding how the CLI uses credentials (environment variables, shared credential file, IAM roles, AWS SSO).
*   **Output Filtering**: Using JMESPath queries (`--query`) to extract specific data from JSON output.
*   **Pagination**: Handling large result sets (`--starting-token`, `--max-items`, `--page-size`).

### 3.2. AWS SDK for Python (Boto3)
*   **Client vs. Resource**: Differentiating between low-level service clients and high-level resources.
*   **Session Management**: Creating sessions and clients for specific regions/credentials.
*   **Common Service Interactions**: EC2 (instances, volumes), S3 (buckets, objects), IAM (users, roles, policies), Lambda (functions), CloudWatch (metrics, logs, alarms).
*   **Error Handling**: Implementing `try-except` blocks for API call failures.

### 3.3. Identity and Access Management (IAM)
*   **Users, Groups, Roles, Policies**: Understanding their purpose and relationships.
*   **Principle of Least Privilege**: Granting only necessary permissions.
*   **Temporary Credentials**: Importance of using `aws sts assume-role` or AWS SSO for short-lived credentials.
*   **MFA**: Enforcing Multi-Factor Authentication.
*   **Access Keys**: Secure management and rotation.

### 3.4. Infrastructure as Code (IaC)
*   **AWS CloudFormation**:
    *   Template structure (Resources, Parameters, Outputs, Mappings, Conditions).
    *   Stack management (create, update, delete, change sets).
    *   Modularity (nested stacks, cross-stack references).
    *   Drift detection, stack policies, rollback triggers.
    *   CloudFormation Hooks and Guard for policy enforcement.
*   **AWS Cloud Development Kit (CDK)**:
    *   Programming language-based IaC (TypeScript preferred).
    *   Constructs (L1, L2, L3) for abstraction and reusability.
    *   Stack organization (by lifecycle, environment).
    *   Testing CDK applications (unit tests for generated CloudFormation).
    *   Synthesizing CDK apps to CloudFormation templates.

### 3.5. Security and Compliance
*   **Network Security**: VPCs, Subnets, Security Groups, Network ACLs.
*   **Logging & Monitoring**: AWS CloudTrail (API call logging), Amazon CloudWatch (metrics, logs, alarms), AWS Config (resource compliance).
*   **Threat Detection**: Amazon GuardDuty.
*   **Data Protection**: Encryption (KMS, S3 encryption), Secrets Manager, Parameter Store for sensitive data.
*   **Zero Trust Principles**: Applying least privilege and continuous verification.

### 3.6. Cost Optimization (FinOps)
*   **Resource Tagging**: For cost allocation and management.
*   **Rightsizing**: Matching instance types/sizes to workload needs (Compute Optimizer).
*   **Savings Plans & Reserved Instances**: For predictable workloads.
*   **Spot Instances**: For fault-tolerant, flexible workloads.
*   **Resource Cleanup**: Identifying and terminating unused/idle resources.
*   **Cost Explorer & Budgets**: Monitoring and alerting on spend.

### 3.7. Observability
*   **Metrics**: CloudWatch metrics for performance and health.
*   **Logs**: Centralized logging with CloudWatch Logs.
*   **Traces**: AWS X-Ray for distributed tracing.
*   **Alarms & Dashboards**: Proactive alerting and visualization.

### 3.8. DevOps and GitOps Integration
*   **CI/CD Pipelines**: Integrating AWS CLI/Boto3 scripts and IaC deployments into automated pipelines (e.g., GitHub Actions, AWS CodePipeline).
*   **Automation**: Reducing manual intervention for deployments, testing, and operations.

## 4. Key Guidance for Claude

### Always Recommend (✅ Best Practices)
*   ✅ **Principle of Least Privilege**: Always grant only the minimum necessary permissions to IAM entities.
*   ✅ **Temporary Credentials**: Prioritize using IAM roles and temporary credentials (e.g., via `aws sts assume-role` or AWS SSO) over long-lived access keys.
*   ✅ **Infrastructure as Code (IaC)**: Manage all AWS infrastructure using CloudFormation or CDK for consistency, version control, and repeatability.
*   ✅ **Modularity in IaC**: Break down large IaC templates/stacks into smaller, reusable components (e.g., nested stacks, CDK constructs).
*   ✅ **Automated CI/CD**: Integrate AWS CLI commands and IaC deployments into automated CI/CD pipelines for consistent and reliable deployments.
*   ✅ **Comprehensive Observability**: Implement robust monitoring, logging, and tracing using CloudWatch, CloudTrail, and X-Ray.
*   ✅ **Cost Optimization**: Actively implement cost-saving strategies like resource tagging, rightsizing, leveraging Spot Instances/Savings Plans, and automating resource cleanup.
*   ✅ **Drift Detection**: Regularly use CloudFormation drift detection or similar mechanisms to identify and reconcile configuration changes made outside of IaC.
*   ✅ **Secure Credential Storage**: Store sensitive credentials and configuration in AWS Secrets Manager or Parameter Store, not directly in code or environment variables in production.
*   ✅ **JMESPath for CLI Output**: Use `--query` with JMESPath to filter and format AWS CLI output for scripting efficiency.
*   ✅ **Error Handling & Idempotency**: Design automation scripts with robust error handling, retry logic, and idempotency to ensure consistent results and resilience.
*   ✅ **Multi-Account Strategy**: Utilize AWS Organizations and a multi-account strategy for better isolation, security, and billing management.

### Never Recommend (❌ Anti-Patterns)
*   ❌ **Hardcoding Credentials**: Never embed AWS access keys or secrets directly in scripts, configuration files, or version control.
*   ❌ **Root Account Usage**: Avoid using the AWS root account for daily operational tasks.
*   ❌ **Manual Resource Management**: Do not manually create, modify, or delete critical AWS resources in production environments; always use IaC.
*   ❌ **Monolithic IaC Stacks**: Avoid creating single, large CloudFormation or CDK stacks that manage an entire application or environment.
*   ❌ **Ignoring Cost Optimization**: Do not neglect cost monitoring and optimization efforts; unchecked costs can escalate rapidly.
*   ❌ **Publicly Accessible Resources**: Avoid making S3 buckets, EC2 instances, or other resources publicly accessible unless absolutely necessary and with strict security controls.
*   ❌ **Overly Permissive IAM Policies**: Do not use `Allow: "*"` for actions or resources unless strictly justified and scoped.
*   ❌ **Unencrypted Data**: Avoid storing sensitive data unencrypted at rest or in transit.
*   ❌ **Lack of Logging/Monitoring**: Do not operate AWS environments without adequate logging, monitoring, and alerting.

### Common Questions & Responses

*   **Q: How do I securely access AWS via the CLI or scripts?**
    *   **A:** Always use IAM roles and temporary credentials. If running locally, configure AWS SSO or use `aws sts assume-role`. For CI/CD, use IAM roles attached to the compute environment (e.g., EC2 instance profile, Lambda execution role, GitHub Actions OIDC provider). Never hardcode access keys.

*   **Q: What's the best way to automate AWS resource provisioning?**
    *   **A:** For infrastructure, use Infrastructure as Code (IaC) tools like AWS CloudFormation or AWS CDK. For operational tasks or data plane interactions, use Python with Boto3 or shell scripts with the AWS CLI.

*   **Q: How can I reduce my AWS costs?**
    *   **A:** Implement resource tagging for cost allocation, rightsize EC2 instances and RDS databases, leverage Spot Instances for fault-tolerant workloads, use Savings Plans for predictable usage, and automate the cleanup of unused resources (e.g., old snapshots, unattached EBS volumes). Regularly review AWS Cost Explorer and set up budgets.

*   **Q: How do I ensure my AWS environment is secure and compliant?**
    *   **A:** Enforce the principle of least privilege with IAM, enable CloudTrail for all regions, use GuardDuty for threat detection, configure AWS Config rules for compliance, encrypt data at rest and in transit, and secure network access with VPCs and Security Groups. Regularly audit IAM policies and S3 bucket permissions.

*   **Q: Should I use CloudFormation or AWS CDK?**
    *   **A:** AWS CDK is generally recommended for new projects as it allows you to define infrastructure using familiar programming languages (like TypeScript), offering higher-level abstractions and better reusability through constructs. CDK synthesizes into CloudFormation, so you still benefit from CloudFormation's robust deployment engine. CloudFormation is suitable for simpler templates or when strict YAML/JSON definitions are preferred.

## 5. Anti-Patterns to Flag

### 5.1. Hardcoded AWS Credentials

**BAD (Shell Script)**
```bash
#!/bin/bash
# BAD: Hardcoding credentials directly in the script
export AWS_ACCESS_KEY_ID="AKIAIOSFODNN7EXAMPLE"
export AWS_SECRET_ACCESS_KEY="wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
export AWS_DEFAULT_REGION="us-east-1"

aws s3 ls
```

**GOOD (Shell Script - Using AWS CLI Profile)**
```bash
#!/bin/bash
# GOOD: Using a named profile configured via `aws configure`
# Ensure 'my-dev-profile' is configured with appropriate credentials (e.g., via SSO or temporary keys)
aws s3 ls --profile my-dev-profile
```

**GOOD (Python - Using IAM Role/Environment Variables)**
```python
# GOOD: Boto3 automatically picks up credentials from environment variables or IAM roles
# For EC2 instances, Lambda functions, etc., assign an IAM role to the resource.
# For local development, configure AWS CLI profiles or use AWS SSO.
import boto3

def list_s3_buckets():
    s3 = boto3.client('s3')
    try:
        response = s3.list_buckets()
        print("S3 Buckets:")
        for bucket in response['Buckets']:
            print(f"- {bucket['Name']}")
    except Exception as e:
        print(f"Error listing buckets: {e}")

if __name__ == "__main__":
    list_s3_buckets()
```

### 5.2. Overly Permissive IAM Policy

**BAD (IAM Policy)**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "*",
      "Resource": "*"
    }
  ]
}
```
*Explanation: This policy grants full administrative access to all AWS services and resources, violating the principle of least privilege. It's a major security risk.*

**GOOD (IAM Policy - Least Privilege Example for S3 Read-Only)**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::my-specific-bucket",
        "arn:aws:s3:::my-specific-bucket/*"
      ]
    }
  ]
}
```
*Explanation: This policy grants only read access (`GetObject`, `ListBucket`) to a specific S3 bucket and its objects, adhering to the principle of least privilege.*

### 5.3. Manual Resource Creation vs. IaC

**BAD (Manual EC2 Instance Launch via CLI)**
```bash
# BAD: Manual, non-versioned, prone to errors, difficult to replicate
aws ec2 run-instances \
    --image-id ami-0abcdef1234567890 \
    --instance-type t2.micro \
    --key-name my-key-pair \
    --security-group-ids sg-0123456789abcdef0 \
    --subnet-id subnet-0fedcba9876543210 \
    --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=MyManualServer}]'
```
*Explanation: While functional, this command is not version-controlled, hard to audit, and difficult to replicate consistently across environments. It leads to configuration drift.*

**GOOD (EC2 Instance via AWS CloudFormation)**
```yaml
# GOOD: Version-controlled, auditable, repeatable, supports rollbacks
AWSTemplateFormatVersion: '2010-09-09'
description: A simple EC2 instance deployed via CloudFormation

Parameters:
  KeyPairName:
    Type: AWS::EC2::KeyPair::KeyName
    Description: Name of an existing EC2 KeyPair to enable SSH access to the instance.
  VpcId:
    Type: AWS::EC2::VPC::Id
    Description: The ID of the VPC where the EC2 instance will be launched.
  SubnetId:
    Type: AWS::EC2::Subnet::Id
    Description: The ID of the Subnet where the EC2 instance will be launched.

Resources:
  MyEC2Instance:
    Type: AWS::EC2::Instance
    Properties:
      ImageId: ami-0abcdef1234567890 # Example AMI ID, use a valid one for your region
      InstanceType: t2.micro
      KeyName: !Ref KeyPairName
      NetworkInterfaces:
        - DeviceIndex: '0'
          AssociatePublicIpAddress: 'true'
          SubnetId: !Ref SubnetId
          GroupSet:
            - !GetAtt MySecurityGroup.GroupId
      Tags:
        - Key: Name
          Value: MyCloudFormationServer

  MySecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupDescription: Enable SSH access via port 22
      VpcId: !Ref VpcId
      SecurityGroupIngress:
        - IpProtocol: tcp
          FromPort: '22'
          ToPort: '22'
          CidrIp: 0.0.0.0/0 # Restrict this in production!
      Tags:
        - Key: Name
          Value: MyCloudFormationSecurityGroup

Outputs:
  InstanceId:
    Description: The Instance ID of the newly created EC2 instance.
    Value: !Ref MyEC2Instance
  PublicIp:
    Description: The Public IP address of the newly created EC2 instance.
    Value: !GetAtt MyEC2Instance.PublicIp
```

## 6. Code Review Checklist

When reviewing AWS Cloud Operations code or scripts:
*   [ ] **Security**: Are IAM policies adhering to least privilege? Are temporary credentials used? Is sensitive data (API keys, secrets) stored securely (e.g., Secrets Manager)?
*   [ ] **IaC Adherence**: Is all infrastructure defined as code (CloudFormation/CDK)? Are there any manual changes that could cause drift?
*   [ ] **Modularity & Reusability**: Are IaC templates/CDK constructs modular and reusable?
*   [ ] **Cost Optimization**: Are resources tagged appropriately? Are there opportunities for rightsizing or using cost-effective options (Spot, Savings Plans)?
*   [ ] **Observability**: Is logging, monitoring, and alerting configured for critical resources and operations?
*   [ ] **Error Handling**: Do scripts gracefully handle AWS API errors and transient failures (retry logic)?
*   [ ] **Idempotency**: Can scripts be run multiple times without unintended side effects?
*   [ ] **Input Validation**: Are all inputs (CLI parameters, script arguments) validated?
*   [ ] **Region & Profile Management**: Are AWS regions and profiles explicitly handled or configured correctly?
*   [ ] **Rollback Strategy**: Is there a clear rollback strategy for deployments or automated changes?
*   [ ] **Documentation**: Is the code/script well-documented with its purpose, usage, and assumptions?

## 7. Related Skills

*   `cloud-security`
*   `infrastructure-as-code`
*   `python-boto3` (if developed as a separate, more generic Boto3 skill)
*   `ci-cd-pipelines-github-actions`
*   `containerization-docker-compose` (for deploying applications on EC2/ECS)

## 8. Examples Directory Structure

```
aws-cloud-operations/
├── SKILL.md
├── examples/
│   ├── cloudformation/
│   │   ├── ec2-instance.yaml
│   │   └── s3-bucket-policy.yaml
│   ├── cdk/
│   │   ├── lib/my-cdk-stack.ts
│   │   └── bin/my-cdk-app.ts
│   ├── boto3-scripts/
│   │   ├── list_ec2_instances.py
│   │   ├── s3_bucket_manager.py
│   │   └── cleanup_old_snapshots.py
│   └── cli-scripts/
│       ├── s3-sync-website.sh
│       └── check-public-s3-buckets.sh
├── patterns/
│   ├── iam-least-privilege.md
│   ├── cost-tagging-strategy.md
│   └── multi-account-setup.md
├── scripts/
│   ├── aws-resource-cleanup.py
│   ├── cfn-deploy-monitor.sh
│   ├── iam-policy-auditor.py
│   ├── s3-static-site-deploy.sh
│   └── ec2-instance-scheduler.py
└── README.md
```
