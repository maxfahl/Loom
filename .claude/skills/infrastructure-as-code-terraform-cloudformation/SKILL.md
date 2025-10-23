---
Name: infrastructure-as-code-terraform-cloudformation
Version: 1.0.0
Category: Cloud Infrastructure / DevOps
Tags: IaC, Terraform, CloudFormation, AWS, Azure, GCP, infrastructure, automation, DevOps
Description: Enables programmatic management and provisioning of cloud infrastructure using Terraform and CloudFormation.
---

# Infrastructure as Code (Terraform, CloudFormation)

## Skill Purpose

This skill empowers Claude to design, implement, and manage cloud infrastructure programmatically using Infrastructure as Code (IaC) principles with both Terraform and AWS CloudFormation. It covers best practices for modularity, version control, security, and automation, enabling efficient, scalable, and repeatable infrastructure deployments across various cloud providers (AWS, Azure, GCP for Terraform; AWS for CloudFormation).

## When to Activate This Skill

Activate this skill when the task involves:
- Provisioning or de-provisioning cloud resources.
- Defining infrastructure in a declarative manner.
- Automating infrastructure deployments via CI/CD.
- Managing infrastructure state and drift.
- Implementing security and compliance policies for infrastructure.
- Refactoring existing infrastructure definitions.
- Troubleshooting infrastructure deployment issues.
- Migrating infrastructure between environments or cloud providers.

Keywords: `Terraform`, `CloudFormation`, `IaC`, `infrastructure`, `AWS`, `Azure`, `GCP`, `resource provisioning`, `stack management`, `module`, `template`, `state file`, `drift detection`, `CI/CD for infrastructure`.

## Core Knowledge

The fundamental concepts, patterns, and APIs Claude needs to know for effective IaC with Terraform and CloudFormation:

### General IaC Principles
- **Declarative vs. Imperative:** Understanding that IaC defines *what* the infrastructure should be, not *how* to build it.
- **Idempotence:** Applying the same configuration multiple times yields the same result.
- **Version Control:** Managing infrastructure definitions in Git for collaboration, history, and auditability.
- **Modularity:** Breaking down infrastructure into reusable components.
- **Testing:** Implementing automated tests for infrastructure code.
- **Secrets Management:** Securely handling sensitive information.
- **Policy as Code:** Enforcing organizational policies and security guardrails.

### Terraform Specifics
- **Terraform Language (HCL):** Syntax, resource blocks, data sources, variables, outputs, locals.
- **Providers:** How Terraform interacts with different cloud providers (AWS, Azure, GCP, etc.).
- **State Management:** Local vs. Remote state (S3, Azure Blob, GCS, HashiCorp Consul/Terraform Cloud), state locking, state file security.
- **Modules:** Creating and consuming reusable Terraform modules.
- **Workspaces:** Managing multiple environments from a single configuration.
- **CLI Commands:** `init`, `plan`, `apply`, `destroy`, `validate`, `fmt`, `import`, `state`.
- **Backend Configuration:** Configuring remote state.
- **Terraform Cloud/Enterprise:** Remote operations, state management, policy enforcement.

### CloudFormation Specifics
- **CloudFormation Template Structure:** YAML/JSON format, Resources, Parameters, Mappings, Conditions, Outputs, Metadata.
- **Intrinsic Functions:** `Fn::GetAtt`, `Fn::Join`, `Fn::Sub`, `Ref`, `Fn::ImportValue`, `Fn::GetAZs`.
- **Stack Management:** Creating, updating, deleting stacks, change sets, nested stacks.
- **Cross-Stack References:** Sharing outputs between stacks.
- **Drift Detection:** Identifying manual changes to resources.
- **Custom Resources:** Extending CloudFormation with Lambda-backed custom resources.
- **CloudFormation Guard/cfn-nag:** Policy enforcement and security checks.
- **AWS CLI/SDK:** Programmatic interaction with CloudFormation.

## Key Guidance for Claude

### Always Recommend (✅ best practices)
- ✅ **Use Remote State (Terraform):** Always configure a remote backend (e.g., S3, Azure Blob Storage, GCS) for state management to enable collaboration, state locking, and prevent data loss.
- ✅ **Modularize Your IaC:** Break down infrastructure into small, reusable modules (Terraform) or nested stacks (CloudFormation) based on logical components or team ownership.
- ✅ **Version Control Everything:** Store all IaC configurations in Git. Implement code reviews for all changes.
- ✅ **Implement Automated Testing:** Use tools like Terratest (Terraform) or TaskCat (CloudFormation) to validate infrastructure deployments.
- ✅ **Manage Secrets Securely:** Never hardcode sensitive information. Use dedicated secrets management services (AWS Secrets Manager, HashiCorp Vault, Azure Key Vault, GCP Secret Manager) and reference them dynamically.
- ✅ **Enforce Policy as Code:** Utilize tools like Sentinel, OPA, CloudFormation Guard, or cfn-nag to enforce security, compliance, and cost policies automatically.
- ✅ **Use `terraform plan` / Change Sets:** Always review the execution plan (`terraform plan`) or CloudFormation Change Sets before applying changes to understand the impact.
- ✅ **Pin Provider/Resource Versions:** Explicitly define provider versions (Terraform) or use specific resource types (CloudFormation) to ensure consistent deployments and prevent unexpected breaking changes.
- ✅ **Consistent Naming Conventions:** Establish and adhere to clear, consistent naming conventions for resources, modules, and stacks.
- ✅ **Integrate with CI/CD:** Automate IaC deployments through CI/CD pipelines to ensure consistency, reduce manual errors, and accelerate delivery.
- ✅ **Enable Drift Detection:** Regularly run drift detection (CloudFormation) or compare state with actual infrastructure (Terraform) to identify and reconcile manual changes.
- ✅ **Use Workspaces (Terraform) / Parameterization (CloudFormation):** Leverage Terraform workspaces or CloudFormation parameters to manage different environments (dev, staging, prod) from a single codebase.

### Never Recommend (❌ anti-patterns)
- ❌ **Hardcoding Secrets:** Never embed API keys, passwords, or other sensitive data directly in IaC files.
- ❌ **Manual Infrastructure Changes:** Avoid making manual changes to infrastructure managed by IaC. If changes are necessary, update the IaC code and apply it.
- ❌ **Large, Monolithic Configurations:** Do not create single, giant Terraform configurations or CloudFormation templates that manage an entire application or environment. This leads to complexity and slow deployments.
- ❌ **Ignoring State Files (Terraform):** Never delete or manually edit Terraform state files directly unless absolutely necessary and with extreme caution.
- ❌ **Unversioned IaC:** Deploying infrastructure without version control makes rollbacks, auditing, and collaboration impossible.
- ❌ **Skipping `plan` / Change Set Review:** Applying changes without reviewing the plan can lead to unintended resource modifications or deletions.
- ❌ **Using Latest Provider Versions Without Pinning:** This can introduce breaking changes without warning.
- ❌ **Inconsistent Naming:** Haphazard naming conventions make infrastructure difficult to understand and manage.
- ❌ **Manual Deployments:** Relying on manual steps for IaC deployments is error-prone and inefficient.

### Common Questions & Responses (FAQ format)

**Q: How do I manage different environments (dev, staging, prod) with IaC?**
A: **Terraform:** Use Terraform Workspaces (`terraform workspace new <env>`) or, for more complex scenarios, separate directories with distinct backend configurations and variable files.
A: **CloudFormation:** Use parameters to customize templates for different environments. For larger setups, consider nested stacks or separate templates per environment.

**Q: What's the best way to handle sensitive data like database passwords?**
A: Never hardcode them. Use a dedicated secrets manager (AWS Secrets Manager, HashiCorp Vault, Azure Key Vault, GCP Secret Manager) and reference the secrets in your IaC code. For example, in Terraform, use data sources to retrieve secrets. In CloudFormation, use dynamic references to Systems Manager Parameter Store or Secrets Manager.

**Q: My Terraform `apply` failed. How do I debug it?**
A:
1.  **Read the error message carefully:** Terraform usually provides clear error messages.
2.  **Check `terraform plan` output:** Re-run `terraform plan` to see if the plan has changed or if new errors appear.
3.  **Enable detailed logging:** Set `TF_LOG=DEBUG` environment variable before running Terraform commands for verbose output.
4.  **Inspect the state file:** Use `terraform state show <resource_address>` to inspect the current state of resources.
5.  **Check cloud provider console/logs:** Verify resource status and logs directly in the AWS, Azure, or GCP console.

**Q: How can I prevent manual changes to my CloudFormation-managed resources?**
A: While direct prevention is hard, you can use:
1.  **Drift Detection:** Regularly run drift detection to identify manual changes.
2.  **IAM Policies:** Restrict direct console/API access to resources managed by CloudFormation.
3.  **CI/CD Enforcement:** Ensure all changes go through the IaC pipeline.
4.  **CloudFormation Guard/cfn-nag:** Implement policies that flag or prevent certain manual modifications.

**Q: When should I use Terraform vs. CloudFormation?**
A:
- **Terraform:**
    - **Multi-cloud environments:** Excellent for managing infrastructure across AWS, Azure, GCP, VMware, etc.
    - **Complex dependencies:** Handles complex resource dependencies well.
    - **Large ecosystems:** Benefits from a vast provider ecosystem for various services.
    - **Community support:** Strong and active community.
- **CloudFormation:**
    - **AWS-only environments:** Deeply integrated with AWS services, often supporting new services faster.
    - **Simpler deployments:** Good for straightforward AWS infrastructure.
    - **Native AWS features:** Leverages AWS-specific features like Change Sets, StackSets, and Guard.
    - **No external state management:** State is managed natively by AWS.

## Anti-Patterns to Flag

### ❌ Hardcoding Sensitive Data

```typescript
// BAD: Hardcoding database password
resource "aws_db_instance" "mydb" {
  // ...
  password = "MySuperSecretPassword123!"
  // ...
}

// BAD: Hardcoding API key in CloudFormation
Resources:
  MyLambdaFunction:
    Type: AWS::Lambda::Function
    Properties:
      Environment:
        Variables:
          API_KEY: "AKIAIOSFODNN7EXAMPLE"
```

```typescript
// GOOD: Referencing secrets from a secrets manager (Terraform)
data "aws_secretsmanager_secret" "db_password" {
  name = "my-app/db-password"
}

data "aws_secretsmanager_secret_version" "db_password_version" {
  secret_id = data.aws_secretsmanager_secret.db_password.id
}

resource "aws_db_instance" "mydb" {
  // ...
  password = data.aws_secretsmanager_secret_version.db_password_version.secret_string
  // ...
}

// GOOD: Referencing secrets from Systems Manager Parameter Store (CloudFormation)
Resources:
  MyLambdaFunction:
    Type: AWS::Lambda::Function
    Properties:
      Environment:
        Variables:
          API_KEY: "{{resolve:ssm:/my-app/api-key:1}}" # Using dynamic reference
```

### ❌ Monolithic IaC Configurations

```typescript
// BAD: Single, giant Terraform file for entire application
// main.tf contains VPC, EC2, RDS, S3, Lambda, etc.
// This becomes unmanageable, slow to plan/apply, and hard to collaborate on.
```

```typescript
// GOOD: Modular Terraform structure
// root/
// ├── main.tf
// ├── variables.tf
// ├── outputs.tf
// ├── modules/
// │   ├── vpc/
// │   │   ├── main.tf
// │   │   ├── variables.tf
// │   │   └── outputs.tf
// │   ├── ec2-instance/
// │   │   ├── main.tf
// │   │   ├── variables.tf
// │   │   └── outputs.tf
// │   └── rds/
// │       ├── main.tf
// │       ├── variables.tf
// │       └── outputs.tf
```

```typescript
// BAD: Single, giant CloudFormation template for everything
// template.yaml contains all resources for an entire environment.
```

```typescript
// GOOD: Nested CloudFormation stacks
// root-stack.yaml (deploys network, then app)
// ├── network-stack.yaml (VPC, subnets, security groups)
// └── application-stack.yaml (EC2, RDS, Lambda, referencing network outputs)
```

## Code Review Checklist

- [ ] Is remote state configured and secured (Terraform)?
- [ ] Are all sensitive values managed via a secrets manager, not hardcoded?
- [ ] Is the IaC modular and reusable (Terraform modules, CloudFormation nested stacks)?
- [ ] Are provider/resource versions explicitly pinned?
- [ ] Are naming conventions consistent and clear?
- [ ] Is the code formatted correctly (`terraform fmt`, `cfn-lint`)?
- [ ] Are there appropriate comments for complex logic or decisions?
- [ ] Are outputs clearly defined and minimal?
- [ ] Are IAM policies following the principle of least privilege?
- [ ] Is there a plan for automated testing of this IaC?
- [ ] Are there any potential drift issues if manual changes occur?
- [ ] Does the `terraform plan` / CloudFormation Change Set output match expectations?

## Related Skills

- `ci-cd-pipeline-implementation`: For automating IaC deployments.
- `secrets-management`: For secure handling of sensitive data.
- `cloud-deployment-kubernetes-vps`: For deploying applications onto the provisioned infrastructure.
- `aws-cloud-operations`: For specific AWS operational knowledge relevant to CloudFormation.
- `azure-cloud-operations`: For specific Azure operational knowledge relevant to Terraform on Azure.
- `google-cloud-operations`: For specific GCP operational knowledge relevant to Terraform on GCP.

## Examples Directory Structure

```
examples/
├── terraform-aws-vpc/
│   ├── main.tf
│   ├── variables.tf
│   └── outputs.tf
├── terraform-azure-vm/
│   ├── main.tf
│   ├── variables.tf
│   └── outputs.tf
├── cloudformation-s3-bucket/
│   └── s3-bucket.yaml
└── cloudformation-lambda-api/
    └── lambda-api.yaml
```

## Custom Scripts Section

Here are 3-5 automation scripts that would save significant time for developers working with Infrastructure as Code using Terraform and CloudFormation.

### 1. `iac-validator.py` (Python)
**Purpose:** Automates the validation and formatting of both Terraform and CloudFormation code. It runs `terraform fmt`, `terraform validate`, `cfn-lint`, and `cfn-guard` (if configured) across specified directories, providing a unified report.
**Pain Point:** Manually running multiple validation tools across different IaC types and directories is tedious and error-prone.
**Script Types:** Quality Checks, Development Helpers

### 2. `env-switcher.sh` (Shell)
**Purpose:** Simplifies switching between Terraform workspaces or CloudFormation parameter files for different environments. It helps manage environment-specific configurations.
**Pain Point:** Managing environment variables, `terraform workspace select`, or manually specifying CloudFormation parameter files for each deployment.
**Script Types:** Development Helpers, Setup/Bootstrap

### 3. `module-generator.py` (Python)
**Purpose:** Generates boilerplate for new Terraform modules or CloudFormation nested stacks, including `main.tf`/`template.yaml`, `variables.tf`/`parameters.yaml`, `outputs.tf`/`outputs.yaml`, and a basic `README.md`.
**Pain Point:** Repetitive creation of standard file structures for new modules/stacks, ensuring consistency.
**Script Types:** Code Generation, Setup/Bootstrap

### 4. `drift-detector.py` (Python)
**Purpose:** Automates drift detection for CloudFormation stacks and provides a summary. For Terraform, it runs `terraform plan -detailed-exitcode` and reports any detected differences.
**Pain Point:** Manually checking for infrastructure drift across many stacks/configurations.
**Script Types:** Quality Checks, Maintenance

### 5. `secrets-injector.py` (Python)
**Purpose:** A utility to securely inject secrets from a specified secrets manager (e.g., AWS Secrets Manager) into IaC deployments, either as environment variables for CI/CD or directly into a temporary configuration file.
**Pain Point:** Securely passing secrets to IaC deployments without hardcoding or exposing them in logs.
**Script Types:** Security, Development Helpers
