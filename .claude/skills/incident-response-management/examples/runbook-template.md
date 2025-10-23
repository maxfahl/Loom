# Runbook Template: [Service Name] - [Incident Type]

## Metadata
*   **Service:** [Service Name]
*   **Incident Type:** [e.g., High Latency, Service Down, Error Rate Spike]
*   **Severity:** [P0, P1, P2, P3, P4]
*   **Last Updated:** YYYY-MM-DD
*   **Owner:** [Team/Individual]

## Symptoms
*   [List observable symptoms, e.g., "High 5xx error rates on /api/v1/users", "Service X is unreachable"]
*   [Link to relevant dashboards/alerts]

## Detection
*   **Alert Name:** [e.g., `ServiceXHighErrorRate`]
*   **Monitoring System:** [e.g., Prometheus, Datadog]
*   **Trigger Condition:** [e.g., "5xx error rate > 5% for 5 minutes"]

## Impact
*   **Affected Users/Systems:** [e.g., "All users of Service X", "Downstream Service Y"]
*   **Business Impact:** [e.g., "Users unable to log in", "Revenue loss"]

## Troubleshooting Steps

**Phase 1: Initial Triage (5-10 minutes)**
1.  **Verify Incident:**
    *   Check [Service X Dashboard](link-to-dashboard) for current status.
    *   Confirm alert is not a false positive.
2.  **Check Recent Changes:**
    *   Review recent deployments for [Service Name] in [CI/CD System Link].
    *   Check recent configuration changes.
3.  **Basic Health Checks:**
    *   Check service logs for errors: `kubectl logs -f <pod-name> -n <namespace>`
    *   Check resource utilization (CPU, Memory) for [Service Name] pods.

**Phase 2: Investigation & Diagnosis**
1.  **Database Connectivity:**
    *   If applicable, check database connection pool metrics.
    *   Verify database is up and reachable from [Service Name] instances.
2.  **External Dependencies:**
    *   Check status of external services [e.g., Payment Gateway, CDN] that [Service Name] depends on.
3.  **Common Failure Modes:**
    *   [List specific common failure modes for this service and how to check them]

## Mitigation & Resolution

**Short-Term Mitigation (Prioritize service restoration)**
1.  **Restart Service:**
    *   `kubectl rollout restart deployment/<service-name> -n <namespace>`
    *   Monitor service health after restart.
2.  **Rollback Deployment:**
    *   If a recent deployment is suspected, rollback to previous stable version: `kubectl rollout undo deployment/<service-name> -n <namespace>`
3.  **Scale Up/Out:**
    *   If resource exhaustion, temporarily scale up instances: `kubectl scale deployment/<service-name> --replicas=<N> -n <namespace>`

**Long-Term Resolution (After service is restored)**
*   Identify root cause.
*   Implement permanent fix (e.g., code change, infrastructure update).
*   Update runbook if new steps were discovered.

## Communication

*   **Internal:**
    *   Create Slack channel: `#incident-[service-name]-[date]`
    *   Notify relevant teams (e.g., Engineering, Product, Support).
*   **External:**
    *   Update [Status Page](link-to-statuspage).
    *   Draft customer communication (if applicable).

## Escalation

*   If incident is not resolved within [X minutes/hours] or impact escalates:
    *   Escalate to [On-Call Manager/SRE Team Lead].
    *   Trigger PagerDuty escalation policy for [Service Name].

## Post-Mortem

*   Schedule a blameless post-mortem meeting within 24-48 hours.
*   Document findings in a post-mortem report (use `post-mortem-template.md`).
*   Track action items in Jira/Confluence.
