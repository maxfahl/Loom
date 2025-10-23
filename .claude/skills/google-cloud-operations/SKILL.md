--- 
name: google-cloud-operations
version: 0.1.0
category: Cloud / Google Cloud Platform
tags: GCP, Cloud Operations, SRE, Security, Cost Optimization, Monitoring, Logging, CI/CD
description: Guides Claude on best practices for managing and operating applications and infrastructure on Google Cloud Platform.
---

## Skill Purpose

This skill enables Claude to provide comprehensive guidance on Google Cloud Operations, focusing on security, reliability (SRE), cost optimization, and efficient architectural patterns. It helps in designing, deploying, monitoring, and maintaining robust and cost-effective solutions on GCP.

## When to Activate This Skill

Activate this skill when the user is:
- Asking about best practices for GCP security, IAM, or network configuration.
- Seeking advice on improving application reliability, setting up monitoring/alerting, or implementing SRE principles on GCP.
- Looking for ways to optimize costs on GCP, including resource right-sizing and managed service utilization.
- Discussing CI/CD pipelines, deployment strategies, or infrastructure as code on GCP.
- Troubleshooting operational issues with GCP services.
- Designing new architectures or migrating existing workloads to GCP.

## Core Knowledge

Claude should be familiar with the following core concepts and GCP services:

- **Security:**
    - **IAM:** Roles, custom roles, service accounts, least privilege principle, Cloud Identity.
    - **Network Security:** VPC, Shared VPC, Firewall Rules, Cloud Armor, Private Google Access, VPN, Interconnect.
    - **Data Protection:** Encryption (CMEK, CSEK), Cloud DLP, Cloud Storage security (uniform bucket-level access).
    - **Security Command Center:** Vulnerability management, threat detection.
- **Reliability (SRE):**
    - **SLIs, SLOs, SLAs, Error Budgets.**
    - **Monitoring & Logging:** Cloud Monitoring, Cloud Logging, Cloud Trace, Cloud Profiler.
    - **Automated Recovery:** Instance groups, auto-healing, disaster recovery strategies.
    - **Fault Tolerance:** Multi-regional deployments, redundancy.
    - **Chaos Engineering** principles.
- **Cost Optimization:**
    - **Resource Right-Sizing:** Identifying and adjusting resource allocations.
    - **Managed Services:** Cloud SQL, BigQuery, Cloud Functions, Cloud Run, App Engine.
    - **Billing & Cost Management:** Budget alerts, cost analysis reports.
    - **Automation:** Autoscaling, scheduled shutdowns.
- **General Operations:**
    - **CI/CD:** Cloud Build, Cloud Deploy, Artifact Registry, Source Repositories.
    - **Infrastructure as Code (IaC):** Terraform, Deployment Manager.
    - **Serverless & Microservices:** Cloud Functions, Cloud Run, GKE, App Engine.
    - **Hybrid & Multi-cloud:** Anthos.
    - **Remote Access:** OS Login, IAP.

## Key Guidance for Claude

- **Always Recommend** (✅ best practices)
    - ✅ **Implement least privilege for IAM:** Grant only the necessary permissions.
    - ✅ **Enable comprehensive logging and monitoring:** Use Cloud Logging and Cloud Monitoring for all resources.
    - ✅ **Encrypt data at rest and in transit:** Utilize Google-managed or customer-managed encryption keys.
    - ✅ **Design for fault tolerance and redundancy:** Use multi-regional deployments and managed instance groups.
    - ✅ **Automate everything possible:** From deployments to recovery processes.
    - ✅ **Regularly review and optimize costs:** Use billing reports and resource right-sizing.
    - ✅ **Adopt SRE principles:** Define SLIs/SLOs and manage error budgets.
    - ✅ **Use managed services where appropriate:** Reduce operational overhead.
    - ✅ **Secure Cloud Storage buckets:** Enable uniform bucket-level access and restrict public access.

- **Never Recommend** (❌ anti-patterns)
    - ❌ **Granting `Owner` or `Editor` roles broadly:** Leads to security vulnerabilities.
    - ❌ **Exposing sensitive services directly to the internet:** Use load balancers, Cloud Armor, and private access.
    - ❌ **Ignoring logs and metrics:** Prevents proactive issue detection.
    - ❌ **Manual deployments for production environments:** Prone to human error and inconsistency.
    - ❌ **Over-provisioning resources without justification:** Leads to unnecessary costs.
    - ❌ **Storing secrets directly in code or configuration files:** Use Secret Manager.

- **Common Questions & Responses** (FAQ format)
    - **Q: How can I secure my GCP project?**
        - A: Start with IAM least privilege, strong network controls (VPC, firewalls, Cloud Armor), data encryption, and comprehensive logging to Security Command Center.
    - **Q: What's the best way to monitor my application on GCP?**
        - A: Use Cloud Monitoring for metrics and alerting, Cloud Logging for centralized log management, and Cloud Trace/Profiler for performance insights. Define clear SLIs/SLOs.
    - **Q: How do I reduce my GCP bill?**
        - A: Right-size your VMs, leverage committed use discounts, use managed services, implement autoscaling, and set up budget alerts. Regularly review your billing reports.
    - **Q: Should I use Cloud Functions or Cloud Run?**
        - A: Cloud Functions are ideal for event-driven, short-lived tasks. Cloud Run is better for stateless containers, web services, and longer-running processes, offering more flexibility.

## Anti-Patterns to Flag

**1. Over-privileged Service Account**

```typescript
// BAD: Granting broad permissions
// This service account has too many permissions, violating the principle of least privilege.
// It can manage all Compute Engine resources, which is rarely necessary for a single application.
gcloud projects add-iam-policy-binding my-gcp-project \
    --member="serviceAccount:my-app-sa@my-gcp-project.iam.gserviceaccount.com" \
    --role="roles/compute.admin"
```

```typescript
// GOOD: Least privilege
// This service account only has permissions to start/stop specific instances,
// which is a more granular and secure approach.
gcloud projects add-iam-policy-binding my-gcp-project \
    --member="serviceAccount:my-app-sa@my-gcp-project.iam.gserviceaccount.com" \
    --role="roles/compute.instanceAdmin.v1"
gcloud compute instances add-iam-policy-binding my-instance \
    --member="serviceAccount:my-app-sa@my-gcp-project.iam.gserviceaccount.com" \
    --role="roles/compute.instanceAdmin.v1"
```

**2. Public Cloud Storage Bucket**

```typescript
// BAD: Publicly accessible bucket
// This bucket is publicly accessible, which can lead to data exposure.
gsutil iam ch allUsers:objectViewer gs://my-sensitive-data-bucket
```

```typescript
// GOOD: Private bucket with uniform access
// This bucket is private, and uniform bucket-level access is enabled for consistent permissions.
gsutil uniformbucketlevelaccess set on gs://my-sensitive-data-bucket
gsutil acl set private gs://my-sensitive-data-bucket
```

## Code Review Checklist

- [ ] Are IAM roles granular and follow the principle of least privilege?
- [ ] Is all sensitive data encrypted at rest and in transit?
- [ ] Are Cloud Storage buckets configured with uniform bucket-level access and restricted public access?
- [ ] Are logging and monitoring enabled for all critical services?
- [ ] Are alerts configured for critical metrics and error rates?
- [ ] Is the solution designed for fault tolerance and automated recovery?
- [ ] Are CI/CD pipelines automated and secure using Cloud Build/Deploy?
- [ ] Is Infrastructure as Code (IaC) used for resource provisioning?
- [ ] Are costs being monitored, and are there strategies for optimization (e.g., autoscaling, right-sizing)?
- [ ] Are secrets managed securely using Secret Manager?

## Related Skills

- `terraform-modules`
- `ci-cd-pipelines-github-actions` (for general CI/CD concepts, though GCP-specific tools are preferred here)
- `containerization-docker-compose` (for containerized workloads on GKE/Cloud Run)
- `microservices-architecture`
- `serverless-architecture` (if a separate skill is created for this)

## Examples Directory Structure

- `examples/iam-custom-role.tf` (Terraform for a custom IAM role)
- `examples/cloud-monitoring-alert.tf` (Terraform for a Cloud Monitoring alert)
- `examples/cloud-build-pipeline.yaml` (Example Cloud Build configuration)
- `examples/cloud-run-service.tf` (Terraform for a Cloud Run service)

## Custom Scripts Section

Here are 3 automation scripts designed to address common pain points in Google Cloud Operations:

1.  **`gcp-resource-inventory.py` (Python)**: Generates an inventory of active GCP resources across specified projects and provides a summary. Helps with auditing and cost awareness.
2.  **`gcp-iam-auditor.py` (Python)**: Audits IAM policies for a given project, identifies overly broad permissions, and suggests least-privilege alternatives. Enhances security.
3.  **`gcp-pipeline-status.sh` (Shell)**: Checks the status of recent Cloud Build and Cloud Deploy runs, providing quick insights into pipeline health and links to logs. Speeds up troubleshooting.
