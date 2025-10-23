---
name: terraform-modules
version: 1.0.0
category: Infrastructure as Code / Terraform
tags: terraform, modules, iac, infrastructure, best practices, reusability
description: Guides Claude on creating and using reusable Terraform modules effectively.
---

# SKILL.md for terraform-modules

### 2. Skill Purpose

This skill enables Claude to design, implement, and utilize Terraform modules following industry best practices. It focuses on promoting reusability, maintainability, and consistency across infrastructure deployments, ensuring that generated Terraform configurations are robust, scalable, and easy to understand.

### 3. When to Activate This Skill

Activate this skill whenever the task involves:
- Creating new Terraform configurations that will be reused across multiple environments or projects.
- Refactoring existing Terraform code to improve modularity and reduce duplication.
- Consuming existing Terraform modules from a registry or local source.
- Performing code reviews on Terraform module definitions.
- Troubleshooting issues related to module inputs, outputs, or versioning.
- Automating common Terraform module development tasks.

Specific triggers/keywords/patterns:
- "create a new terraform module for X"
- "refactor this terraform code into modules"
- "how to use terraform module Y"
- "best practices for terraform modules"
- "design a reusable terraform component"
- "review this terraform module"
- "generate terraform module documentation"
- "update terraform module versions"

### 4. Core Knowledge

The fundamental concepts, patterns, and APIs Claude needs to know:

- **Module Definition**: Understanding `main.tf`, `variables.tf`, `outputs.tf`, `versions.tf`.
- **Module Sources**: Local paths, Terraform Registry, Git repositories, S3 buckets.
- **Input Variables**: `variable` blocks, `type`, `description`, `default`, `validation`, `sensitive`.
- **Output Values**: `output` blocks, `description`, `sensitive`.
- **Local Values**: `locals` blocks for intermediate computations.
- **Data Sources**: Fetching information from existing infrastructure.
- **Providers**: Declaring and configuring providers within modules.
- **Versioning**: Semantic versioning for modules, `version` constraint in `module` blocks.
- **Module Composition**: Nesting modules, passing outputs as inputs.
- **`terraform-docs`**: Tool for automated documentation generation.
- **`tflint`**: Linter for Terraform code.
- **CI/CD Integration**: How modules fit into automated pipelines (validate, plan, apply).
- **State Management**: Understanding how module state is managed and isolated.
- **Naming Conventions**: Consistent naming for resources, variables, and modules (e.g., `snake_case`).

### 5. Key Guidance for Claude

- **Always Recommend** (✅ best practices)
    - ✅ **Single Responsibility Principle**: Design modules to do one thing well.
    - ✅ **Clear Interfaces**: Define explicit inputs (`variables.tf`) and outputs (`outputs.tf`) with comprehensive descriptions.
    - ✅ **Sensible Defaults**: Provide default values for optional variables to simplify module usage.
    - ✅ **Input Validation**: Use `validation` blocks for critical inputs to ensure data integrity.
    - ✅ **Automated Documentation**: Integrate `terraform-docs` to keep `README.md` up-to-date.
    - ✅ **Examples Directory**: Include a `examples/` directory with working, minimal configurations demonstrating module usage.
    - ✅ **Version Constraints**: Always specify `required_version` for Terraform and `version` for providers and modules.
    - ✅ **Testing**: Encourage unit and integration testing for modules (e.g., with Terratest or `terraform test`).
    - ✅ **Sensitive Data Handling**: Mark sensitive variables and outputs with `sensitive = true`.
    - ✅ **Consistent Naming**: Adhere to `snake_case` for resource names, variables, and outputs.

- **Never Recommend** (❌ anti-patterns)
    - ❌ **Hardcoding Values**: Avoid hardcoding values that could vary between environments or deployments. Use variables instead.
    - ❌ **"God" Modules**: Do not create overly complex modules that manage too many disparate resources. Break them down.
    - ❌ **Implicit Dependencies**: Avoid relying on implicit dependencies. Use `depends_on` or explicit input/output passing.
    - ❌ **Exposing Internal Details**: Only expose necessary outputs. Internal resource attributes should remain encapsulated.
    - ❌ **Lack of Documentation**: Never publish or use a module without clear, up-to-date documentation.
    - ❌ **Unversioned Modules**: Avoid using modules without version constraints, as this can lead to unexpected changes.
    - ❌ **Ignoring Linters/Formatters**: Do not bypass `terraform fmt` or `tflint`.
    - ❌ **Directly Modifying State**: Never manually edit the Terraform state file.

- **Common Questions & Responses** (FAQ format)
    - **Q: How do I make my module reusable?**
        - A: Design it with a focused scope, define clear input variables for customization, and provide comprehensive documentation and examples. Avoid hardcoding environment-specific values.
    - **Q: When should I create a new module?**
        - A: When you find yourself repeating the same block of resources multiple times, or when you want to encapsulate a logical group of resources that are always deployed together.
    - **Q: How do I handle sensitive information in module inputs/outputs?**
        - A: Use `sensitive = true` for variables and outputs. For actual secrets, integrate with a secrets management system (e.g., AWS Secrets Manager, Azure Key Vault, HashiCorp Vault).
    - **Q: What's the best way to version my modules?**
        - A: Use semantic versioning (e.g., `1.0.0`). Store modules in their own Git repositories and reference them by version. Utilize a module registry if available.
    - **Q: How can I ensure my module's `README.md` is always up-to-date?**
        - A: Use `terraform-docs` to automatically generate the input and output sections of your `README.md` as part of your CI/CD pipeline.

### 6. Anti-Patterns to Flag

- **Anti-Pattern 1: Hardcoded Values**
    - **BAD:**
        ```terraform
        resource "aws_s3_bucket" "my_bucket" {
          bucket = "my-app-prod-bucket"
          acl    = "private"
        }
        ```
    - **GOOD:**
        ```terraform
        variable "bucket_name" {
          description = "Name of the S3 bucket"
          type        = string
        }

        resource "aws_s3_bucket" "my_bucket" {
          bucket = var.bucket_name
          acl    = "private"
        }
        ```

- **Anti-Pattern 2: "God" Module (Too many responsibilities)**
    - **BAD:** A single module that creates VPC, EC2 instances, RDS databases, and S3 buckets.
    - **GOOD:** Separate modules for `vpc`, `ec2-instance`, `rds-database`, and `s3-bucket`, composed in a root module.

- **Anti-Pattern 3: Lack of Input Validation**
    - **BAD:**
        ```terraform
        variable "instance_type" {
          description = "EC2 instance type"
          type        = string
        }
        ```
    - **GOOD:**
        ```terraform
        variable "instance_type" {
          description = "EC2 instance type"
          type        = string
          validation {
            condition     = contains(["t2.micro", "t3.small", "m5.large"], var.instance_type)
            error_message = "Invalid EC2 instance type. Must be one of t2.micro, t3.small, or m5.large."
          }
        }
        ```

### 7. Code Review Checklist

- [ ] Does the module have a clear, single responsibility?
- [ ] Are all input variables explicitly defined with `type`, `description`, and sensible `default` values (if optional)?
- [ ] Are sensitive variables and outputs marked with `sensitive = true`?
- [ ] Are all necessary outputs exposed with clear `description`s?
- [ ] Is there a `versions.tf` file specifying Terraform and provider version constraints?
- [ ] Is the `README.md` comprehensive and up-to-date (ideally generated by `terraform-docs`)?
- [ ] Does the `examples/` directory contain working examples of module usage?
- [ ] Are there no hardcoded values that should be variables?
- [ ] Is the naming consistent and descriptive (e.g., `snake_case`)?
- [ ] Are there appropriate input validations for critical variables?
- [ ] Does the module avoid exposing unnecessary internal details via outputs?
- [ ] Is the module free of implicit dependencies?

### 8. Related Skills

- `terraform-core`: For fundamental Terraform concepts and CLI usage.
- `aws-provider`: For AWS-specific resource definitions and best practices.
- `azure-provider`: For Azure-specific resource definitions and best practices.
- `gcp-provider`: For GCP-specific resource definitions and best practices.
- `ci-cd-pipelines`: For integrating Terraform module testing and deployment into CI/CD.

### 9. Examples Directory Structure

```
examples/
├── basic-usage/
│   ├── main.tf
│   ├── variables.tf
│   └── outputs.tf
├── advanced-configuration/
│   ├── main.tf
│   ├── variables.tf
│   └── outputs.tf
└── ... (other specific use cases)
```

### 10. Custom Scripts Section

Here are 3-5 automation scripts that would save significant time for developers working with Terraform modules:

1.  **`generate-module-boilerplate.sh`**: A shell script to quickly scaffold a new Terraform module with the recommended directory structure and basic files.
2.  **`update-module-docs.sh`**: A shell script to automate the generation/update of `README.md` documentation using `terraform-docs`.
3.  **`validate-terraform-module.sh`**: A shell script to run `terraform fmt`, `terraform validate`, and `tflint` across a specified module or the current directory.
4.  **`tf-module-version-updater.py`**: A Python script to find and update module versions in a root Terraform configuration.
