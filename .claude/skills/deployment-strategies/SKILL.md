---
name: deployment-strategies
version: 1.0.0
category: DevOps / Deployment
tags: deployment, devops, ci/cd, blue-green, canary, rolling, release, kubernetes, cloud-native
description: Strategies for deploying applications with minimal downtime and risk.
---

## Skill Purpose

This skill enables Claude to understand, evaluate, and recommend appropriate application deployment strategies (e.g., Blue-Green, Canary, Rolling, Recreate) based on specific project requirements, risk tolerance, and infrastructure. It provides guidance on implementing these strategies, particularly in cloud-native environments like Kubernetes, and highlights best practices for automation, monitoring, and rollback.

## When to Activate This Skill

Activate this skill when discussing:
- Application deployment, release management, or continuous delivery.
- Strategies for minimizing downtime during updates.
- Risk mitigation for new software versions.
- CI/CD pipeline design for deployments.
- Kubernetes deployment patterns.
- Rollback procedures and disaster recovery related to deployments.
- Evaluating trade-offs between different deployment approaches.

## Core Knowledge

### 1. Deployment Strategy Overview

*   **Rolling Deployment:** Gradually replaces instances of the old version with the new version.
    *   **Pros:** Simple to implement, minimal infrastructure overhead.
    *   **Cons:** Rollback can be slow, potential for mixed traffic (old and new versions simultaneously), issues can affect all users.
*   **Recreate Deployment:** Terminates all instances of the old version before deploying the new version.
    *   **Pros:** Simplest to implement, guarantees only one version is running at a time.
    *   **Cons:** Significant downtime during the transition.
*   **Blue-Green Deployment:** Runs two identical production environments ("blue" for current, "green" for new). Traffic is switched entirely from blue to green once the green environment is validated.
    *   **Pros:** Zero downtime, instant rollback, new version tested in production-like environment.
    *   **Cons:** Doubles infrastructure costs temporarily, requires careful state management for stateful applications.
*   **Canary Deployment:** Gradually rolls out a new version to a small subset of users, monitors its performance, and then progressively increases traffic if stable.
    *   **Pros:** Minimizes impact of issues, real-world testing, easy rollback for affected users.
    *   **Cons:** More complex to implement, requires robust monitoring and automated analysis, longer deployment cycle.
*   **A/B Testing (related):** Similar to Canary but focuses on testing different features or UI changes with specific user segments for business metrics, rather than just stability. Can be layered on top of canary.
*   **Shadow Deployment:** Routes a copy of live production traffic to a new version without affecting real users. Used for performance testing and validation.

### 2. Key Kubernetes Concepts for Deployment Strategies

*   **Deployments:** Manage the lifecycle of application pods.
*   **Services:** Provide stable network endpoints, abstracting away underlying pods.
*   **Labels and Selectors:** Crucial for associating pods with Deployments and for Services to route traffic.
*   **Ingress/Service Mesh (Istio, Linkerd, Traefik):** For advanced traffic management, weighted routing, and A/B testing.
*   **Argo Rollouts / Flagger:** Kubernetes-native tools for advanced deployment strategies with automated analysis and promotion/rollback.

### 3. Monitoring and Observability

*   **Metrics:** Error rates, latency, throughput, CPU/memory usage, business-specific KPIs.
*   **Tools:** Prometheus, Grafana, Datadog, New Relic, OpenTelemetry.
*   **SLOs (Service Level Objectives):** Define acceptable performance thresholds and rollback criteria.

## Key Guidance for Claude

### Always Recommend (✅ Best Practices)

*   ✅ **Prioritize Automation:** Automate all deployment steps, including testing, monitoring, and rollback, to reduce human error and increase speed.
*   ✅ **Implement Robust Monitoring:** Ensure comprehensive monitoring and alerting for both baseline and new versions during progressive deployments (Canary, Blue-Green).
*   ✅ **Define Clear Rollback Procedures:** Always have a well-tested, automated rollback plan for every deployment strategy.
*   ✅ **Use Version Control for Everything:** Store all deployment configurations, scripts, and application code in version control.
*   ✅ **Start Small with Canaries:** Begin canary releases with a very small percentage of traffic (e.g., 1-5%) and gradually increase.
*   ✅ **Test in Production-like Environments:** Validate new versions in environments that closely mirror production before full rollout.
*   ✅ **Consider Infrastructure as Code (IaC):** Manage infrastructure using tools like Terraform or Pulumi for consistency and repeatability.
*   ✅ **Leverage Feature Flags:** Use feature flags to decouple deployment from release, allowing features to be toggled on/off independently.
*   ✅ **Automate Canary Analysis:** Use tools like Argo Rollouts, Flagger, or Spinnaker with Kayenta for automated metric comparison and decision-making.

### Never Recommend (❌ Anti-Patterns)

*   ❌ **Manual Deployments to Production:** Avoid manual steps in production deployments to prevent errors and ensure consistency.
*   ❌ **Deploying Without a Rollback Plan:** Never deploy a new version without a clear, tested, and automated way to revert to the previous stable state.
*   ❌ **Ignoring Monitoring During Rollouts:** Deploying without actively monitoring the health and performance of the new version is extremely risky.
*   ❌ **"Big Bang" Deployments (unless Recreate is explicitly chosen for specific reasons):** Avoid deploying a new version to all users at once without any gradual exposure or testing.
*   ❌ **Using Blue-Green for Stateful Applications Without Data Strategy:** Deploying stateful applications with Blue-Green requires a robust data migration and synchronization strategy; otherwise, data consistency issues will arise.
*   ❌ **Over-engineering for Simple Applications:** Don't implement complex Canary or Blue-Green strategies for simple, low-risk applications where a Rolling Update might suffice.

### Common Questions & Responses (FAQ Format)

*   **Q: When should I use Blue-Green vs. Canary?**
    *   **A:** Use Blue-Green for applications where zero downtime and instant rollback are critical, and you can afford the temporary doubling of infrastructure. It's ideal for stateless microservices. Use Canary when you want to minimize the blast radius of potential issues, test new features with real users, and have robust monitoring to make data-driven promotion decisions.
*   **Q: How do I handle database schema changes with Blue-Green deployments?**
    *   **A:** This is complex. Typically, schema changes must be backward-compatible. The "blue" (old) version must be able to work with the new schema, and the "green" (new) version must also work with the old schema during the transition. Often, a multi-step process involving schema evolution and data migration is required.
*   **Q: What metrics are most important to monitor during a Canary release?**
    *   **A:** Key metrics include error rates (e.g., HTTP 5xx errors), latency (response times), throughput, CPU/memory utilization, and application-specific business metrics (e.g., conversion rates, user engagement).
*   **Q: Can I combine deployment strategies?**
    *   **A:** Yes, often. For example, you might use a Canary release to validate a new version, and once it's deemed stable, perform a Blue-Green switch to fully cut over traffic. Feature flags can also be used with any strategy.

## Anti-Patterns to Flag

### ❌ Bad: Manual Traffic Switch in Blue-Green

```bash
# Manual kubectl edit to change service selector
kubectl edit service my-app-service
# User manually changes selector.version from v1 to v2
```
**Why it's bad:** Prone to human error, slow, not repeatable, difficult to audit.

### ✅ Good: Automated Traffic Switch with Script

```bash
#!/bin/bash
# switch-blue-green.sh
SERVICE_NAME="my-app-service"
NEW_VERSION_LABEL="v2"

echo "Switching traffic for service $SERVICE_NAME to version $NEW_VERSION_LABEL..."
kubectl patch service $SERVICE_NAME -p "{"spec":{"selector":{"version":"$NEW_VERSION_LABEL"}}}"

if [ $? -eq 0 ]; then
    echo "Traffic successfully switched to $NEW_VERSION_LABEL."
else
    echo "Error switching traffic."
    exit 1
fi
```
**Why it's good:** Automated, fast, repeatable, auditable, reduces human error.

### ❌ Bad: Deploying Canary without Automated Analysis

```yaml
# Argo Rollout definition without analysis
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: my-app
spec:
  replicas: 5
  strategy:
    canary:
      steps:
      - setWeight: 20
      - pause: {} # Manual intervention required to promote
      - setWeight: 40
      - pause: {}
      # ... and so on
```
**Why it's bad:** Requires manual intervention, slow, subjective decision-making, delays feedback.

### ✅ Good: Deploying Canary with Automated Analysis

```yaml
# Argo Rollout definition with automated analysis
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: my-app
spec:
  replicas: 5
  strategy:
    canary:
      steps:
      - setWeight: 20
      - pause: { duration: 1m } # Wait for metrics to stabilize
      - analysis:
          templates:
            - templateName: success-rate-analysis
      - setWeight: 50
      - pause: { duration: 1m }
      - analysis:
          templates:
            - templateName: error-rate-analysis
      # ... more steps and analysis
  # Define analysis templates (e.g., success-rate-analysis, error-rate-analysis)
  # that query Prometheus/Grafana and define pass/fail conditions.
```
**Why it's good:** Automated, objective, faster feedback loop, reduces risk.

## Code Review Checklist

When reviewing code related to deployment strategies, verify the following:

*   **Deployment Manifests:**
    *   Are `readinessProbe` and `livenessProbe` correctly configured?
    *   Are resource limits and requests defined?
    *   Are `PodDisruptionBudgets` in place for high availability?
    *   Are labels and selectors consistent and correctly applied for Blue-Green/Canary?
*   **CI/CD Pipelines:**
    *   Are all deployment steps automated?
    *   Is there a clear trigger for deployments (e.g., Git push to main)?
    *   Are tests (unit, integration, end-to-end) run before deployment?
    *   Is there an automated rollback step in case of failure?
    *   Are environment-specific configurations managed securely (e.g., secrets)?
*   **Monitoring & Alerting:**
    *   Are relevant metrics collected for the application and infrastructure?
    *   Are alerts configured for critical issues during and after deployment?
    *   Are dashboards available to visualize the health of new deployments?
*   **Rollback Mechanism:**
    *   Is the rollback process clearly defined and automated?
    *   Has the rollback process been tested?
*   **Stateful Applications:**
    *   If stateful, is there a robust data migration and backward compatibility strategy?

## Related Skills

*   `ci-cd-pipelines`: For building and automating the deployment process.
*   `kubernetes`: For managing containerized applications and orchestrating deployments.
*   `docker`: For containerizing applications.
*   `feature-flags`: For decoupling deployment from release and enabling A/B testing.
*   `observability`: For comprehensive monitoring, logging, and tracing.

## Examples Directory Structure

```
examples/
├── kubernetes/
│   ├── blue-green-deployment.yaml  # Example K8s manifests for Blue-Green
│   ├── canary-deployment-argo-rollouts.yaml # Example Argo Rollouts for Canary
│   └── rolling-update-deployment.yaml # Standard K8s Rolling Update
├── ci-cd/
│   ├── github-actions-blue-green.yaml # GitHub Actions workflow for Blue-Green
│   └── gitlab-ci-canary.yaml # GitLab CI workflow for Canary
└── scripts/
    ├── blue-green-traffic-switch.sh # Shell script to switch K8s service selector
    └── canary-metrics-analyzer.py # Python script to analyze canary metrics
```

## Custom Scripts Section ⭐ NEW

Here are 3-5 automation scripts that would save significant time for developers working with deployment strategies.

### 1. `blue-green-traffic-switch.sh`

**Purpose:** Automates the traffic switch for a Kubernetes Blue-Green deployment by updating the service selector. This script ensures a quick, consistent, and auditable cutover between the blue and green environments.

**Pain Point:** Manually editing Kubernetes service YAMLs or patching services during a Blue-Green cutover is error-prone and can lead to downtime if not executed precisely.

**Usage Example:**
```bash
./scripts/blue-green-traffic-switch.sh --service my-app-service --version v2
```

### 2. `canary-metrics-analyzer.py`

**Purpose:** A Python script that simulates automated analysis of canary deployment metrics. It checks for predefined success/failure conditions (e.g., error rate thresholds) and recommends whether to promote or roll back the canary. In a real-world scenario, this would integrate with monitoring systems like Prometheus.

**Pain Point:** Manually monitoring dashboards and making subjective decisions about canary promotion or rollback is time-consuming, inconsistent, and can delay releases or increase risk.

**Usage Example:**
```bash
python scripts/canary-metrics-analyzer.py --canary-version v2 --baseline-version v1 --error-threshold 0.01
```

### 3. `deployment-config-generator.py`

**Purpose:** Generates a basic Kubernetes Deployment and Service YAML configuration based on user input, pre-configuring labels and selectors suitable for Blue-Green or Canary strategies.

**Pain Point:** Manually writing Kubernetes YAMLs for new applications, especially ensuring correct labeling for advanced deployment strategies, can be tedious and error-prone.

**Usage Example:**
```bash
python scripts/deployment-config-generator.py
```
