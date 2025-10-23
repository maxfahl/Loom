# Post-Mortem Report: [Incident Title]

## 1. Incident Summary

*   **Incident ID:** [e.g., INC-123, PagerDuty Incident #456]
*   **Date & Time (UTC):** [Start Time] - [End Time]
*   **Duration:** [e.g., 2 hours 15 minutes]
*   **Service(s) Affected:** [e.g., User API, Payment Service, Frontend]
*   **Severity:** [P0, P1, P2]
*   **Impact:** [Concise description of business and customer impact, e.g., "Users unable to log in for 2 hours, resulting in X% revenue loss."]
*   **Incident Commander:** [Name]
*   **Key Responders:** [List of individuals/teams involved]

## 2. Detection

*   **How was the incident detected?** [e.g., "Automated alert from Prometheus", "Customer report via support channel"]
*   **Time to Detect (MTTD):** [e.g., 5 minutes]
*   **Was detection effective?** [Yes/No, why/why not]

## 3. Response Timeline

| Timestamp (UTC) | Event                                                              | Owner          |
| :-------------- | :----------------------------------------------------------------- | :------------- |
| [YYYY-MM-DD HH:MM] | Alert triggered: `ServiceXHighErrorRate`                           | Monitoring     |
| [YYYY-MM-DD HH:MM] | On-call engineer acknowledged alert                                | [Engineer Name]|
| [YYYY-MM-DD HH:MM] | Incident declared P1, Slack channel #incident-xyz created          | [Engineer Name]|
| [YYYY-MM-DD HH:MM] | Initial investigation: checked recent deployments                  | [Engineer Name]|
| [YYYY-MM-DD HH:MM] | Identified database connection pool exhaustion                     | [Engineer Name]|
| [YYYY-MM-DD HH:MM] | Mitigation: Restarted database instances                           | [Engineer Name]|
| [YYYY-MM-DD HH:MM] | Service restored, monitoring for stability                         | [Engineer Name]|
| [YYYY-MM-DD HH:MM] | Incident resolved                                                  | [Engineer Name]|

*   **Time to Acknowledge (MTTA):** [e.g., 2 minutes]
*   **Time to Resolve (MTTR):** [e.g., 1 hour 30 minutes]

## 4. Root Cause Analysis

*   **What was the immediate cause?** [e.g., "Deployment of new feature X introduced a memory leak in Service Y."]
*   **What were the contributing factors?** [e.g., "Lack of adequate load testing for feature X", "Monitoring alert threshold was too high."]
*   **5 Whys / Fishbone Diagram (if applicable):** [Brief summary or link to analysis]

## 5. Resolution

*   **How was the incident resolved?** [e.g., "Rolled back deployment of feature X", "Increased database connection pool size."]
*   **Was the resolution effective?** [Yes/No]

## 6. Lessons Learned

*   **What went well?** [e.g., "Team communication was excellent", "Runbook for database issues was accurate."]
*   **What could have gone better?** [e.g., "Detection could have been faster", "Lack of clear ownership for Service Z."]

## 7. Action Items

| ID    | Description                                                              | Owner          | Due Date   | Status    |
| :---- | :----------------------------------------------------------------------- | :------------- | :--------- | :-------- |
| INC-123-1 | Implement load testing for new features in CI/CD pipeline                | @engineer-lead | YYYY-MM-DD | Open      |
| INC-123-2 | Review and adjust alert thresholds for Service Y memory usage            | @sre-team      | YYYY-MM-DD | Open      |
| INC-123-3 | Create runbook for Service Z common issues                               | @dev-team      | YYYY-MM-DD | Open      |

## 8. Supporting Information

*   [Link to relevant dashboards (Grafana, Datadog)]
*   [Link to relevant logs (Splunk, ELK)]
*   [Link to Jira ticket / Incident Management Platform entry]
*   [Link to communication threads (Slack)]
