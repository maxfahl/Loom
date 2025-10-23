# Google Cloud Operations Skill

This skill provides comprehensive guidance and automation for managing and operating applications and infrastructure on Google Cloud Platform (GCP). It focuses on best practices across security, reliability (Site Reliability Engineering - SRE), cost optimization, and efficient architectural patterns.

## Key Features

- **GCP Best Practices:** Learn about recommended approaches for security, IAM, networking, data protection, monitoring, logging, and CI/CD on GCP.
- **SRE Principles:** Guidance on implementing Service Level Indicators (SLIs), Service Level Objectives (SLOs), Service Level Agreements (SLAs), and error budgets.
- **Cost Optimization Strategies:** Techniques for resource right-sizing, leveraging managed services, and managing GCP spending.
- **Anti-Pattern Identification:** Examples of common mistakes and how to avoid them in GCP operations.
- **Automation Scripts:** A collection of scripts to automate repetitive tasks, improve efficiency, and enforce best practices.

## Included Automation Scripts

- **`gcp-resource-inventory.py`**: Generates an inventory of active GCP resources and provides a summary.
- **`gcp-iam-auditor.py`**: Audits IAM policies for a given project and suggests least-privilege alternatives.
- **`gcp-pipeline-status.sh`**: Checks the status of recent Cloud Build and Cloud Deploy runs.

## Usage

Refer to `SKILL.md` for detailed instructions on how Claude can leverage this skill. The automation scripts can be found in the `scripts/` directory.
