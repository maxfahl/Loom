---
name: incident-response-management
version: 1.0.0
category: Operations / SRE
tags: incident, response, SRE, DevOps, production, outage, post-mortem, runbook, playbook
description: Guides Claude in effective handling of production incidents, from detection to post-mortem.
---

## Skill Purpose

This skill enables Claude to assist in all phases of incident response management, ensuring a structured, efficient, and blameless approach to resolving production issues. It helps in triaging, investigating, communicating, and learning from incidents to improve system reliability.

## When to Activate This Skill

Activate this skill when:
*   A critical alert fires (e.g., PagerDuty, Opsgenie).
*   A user reports a production issue.
*   A system or service is experiencing degraded performance or an outage.
*   A post-mortem needs to be conducted or documented.
*   Runbooks or incident playbooks need to be created, updated, or reviewed.
*   Incident communication to stakeholders is required.

## Core Knowledge

*   **Incident Lifecycle (NIST/SANS inspired):**
    *   **Preparation:** Proactive measures, policies, tools, training, risk assessment, vulnerability management.
    *   **Detection & Analysis:** Monitoring, alerting, log analysis, impact assessment, severity classification.
    *   **Containment, Eradication, Recovery:** Limiting spread, removing threat, restoring systems.
    *   **Post-Incident Activity:** Post-mortem, root cause analysis, lessons learned, continuous improvement.
*   **Incident Command Structure (ICS):** Roles like Incident Commander, Communications Lead, Technical Lead(s).
*   **Severity Levels:** P0/SEV-0 (critical outage) to P4/SEV-4 (minor issue).
*   **Runbooks & Playbooks:** Step-by-step guides for common incidents.
*   **Communication:** Internal (team, leadership) and External (customers, public) strategies.
*   **Blameless Post-Mortems:** Focus on systemic issues, not individual failures.
*   **Key Metrics:** MTTR (Mean Time To Restore), MTTD (Mean Time To Detect), MTTA (Mean Time To Acknowledge).
*   **Tools:**
    *   **Alerting/On-Call:** PagerDuty, Opsgenie, VictorOps.
    *   **Communication:** Slack, Microsoft Teams, Statuspage.
    *   **Incident Management Platforms:** Jira Service Management, Rootly, Incident.io.
    *   **Monitoring/Observability:** Prometheus, Grafana, Datadog, New Relic, Splunk, ELK Stack.
    *   **Version Control:** Git (for runbooks, playbooks).

## Key Guidance for Claude

*   **Always Recommend** (✅ best practices)
    *   ✅ **Prioritize communication:** Keep all stakeholders informed with timely and clear updates.
    *   ✅ **Follow established runbooks/playbooks:** Adhere to documented procedures for consistency and efficiency.
    *   ✅ **Focus on service restoration first:** Prioritize mitigating impact and restoring functionality over deep root cause analysis during an active incident.
    *   ✅ **Document everything:** Log all actions, observations, and decisions during an incident for post-mortem analysis.
    *   ✅ **Conduct blameless post-mortems:** Focus on learning and improving processes, not assigning blame.
    *   ✅ **Automate repetitive tasks:** Use scripts for incident declaration, communication, and post-mortem generation.
    *   ✅ **Define clear roles:** Ensure an Incident Commander and other roles are assigned early.
    *   ✅ **Escalate appropriately:** Know when and how to escalate an incident based on severity and impact.

*   **Never Recommend** (❌ anti-patterns)
    *   ❌ **Panicking or acting impulsively:** Stick to the process and communicate calmly.
    *   ❌ **Ad-hoc communication:** Avoid informal or inconsistent updates; use designated channels and templates.
    *   ❌ **Skipping post-mortems:** Every incident is a learning opportunity; never skip the review.
    *   ❌ **Blaming individuals:** Focus on process and system improvements.
    *   ❌ **Working in isolation:** Incident response is a team effort; collaborate actively.
    *   ❌ **Making assumptions:** Always verify information and data.

*   **Common Questions & Responses** (FAQ format)
    *   **Q: How do I declare a P1 incident?**
        *   A: "Initiate the `incident-initiator.py` script with the `--severity P1` flag, providing a concise summary. This will trigger alerts, create a communication channel, and a tracking ticket."
    *   **Q: What should be in a post-mortem?**
        *   A: "A post-mortem should include: Incident Summary, Impact, Detection, Response Timeline, Root Cause, Resolution, Lessons Learned, and Action Items. Use the `post-mortem-generator.py` script to get a structured template."
    *   **Q: How often should I update stakeholders during an incident?**
        *   A: "For critical incidents (P0/P1), aim for updates every 15-30 minutes, even if it's just to say 'still investigating'. For lower severity, every 1-2 hours. Use the `send-incident-update.sh` script with a pre-approved template."
    *   **Q: Where can I find the runbook for service X?**
        *   A: "Runbooks are typically stored in the `docs/runbooks/` directory or a dedicated knowledge base. You can use the `runbook-linter.py` script to verify its quality."

## Anti-Patterns to Flag

*   **Bad Communication:**
    ```typescript
    // BAD: Vague, informal, and lacks critical information
    console.log("Something's broken, looking into it.");
    ```
    ```typescript
    // GOOD: Structured, informative, and uses designated channels
    // Incident Commander: "Incident declared P1. Service X is down. Initial investigation points to DB connection issues. Opening #incident-service-x and Jira INC-123. Updates every 15 mins."
    ```
*   **Unstructured Investigation:**
    ```typescript
    // BAD: Randomly checking logs without a hypothesis
    tail -f /var/log/syslog | grep error
    ```
    ```typescript
    // GOOD: Following a structured diagnostic path based on runbook
    // Technical Lead: "Checking DB connection pool metrics as per runbook step 3. Confirming network connectivity to DB. Reviewing recent deployments for service X."
    ```
*   **Blaming:**
    ```typescript
    // BAD: Assigning fault to an individual
    // Post-mortem: "John deployed the faulty code, causing the outage."
    ```
    ```typescript
    // GOOD: Focusing on process and system improvements
    // Post-mortem: "The deployment process lacked sufficient pre-release testing for database schema changes, allowing a breaking change to reach production."
    ```

## Code Review Checklist (for Runbooks/Playbooks/Alerts)

*   [ ] Is the runbook clear, concise, and actionable?
*   [ ] Are all commands and procedures up-to-date and verified?
*   [ ] Does the runbook include clear escalation paths and communication guidelines?
*   [ ] Are all monitoring and alerting configurations aligned with best practices (e.g., appropriate thresholds, clear alert messages, actionable playbooks)?
*   [ ] Is the post-mortem template consistently used and filled out completely?
*   [ ] Are action items from previous incidents tracked and completed?

## Related Skills

*   `monitoring-and-alerting`: For setting up effective detection mechanisms.
*   `observability-stack-implementation`: For deep insights into system behavior during incidents.
*   `post-mortem-analysis`: For structured learning after incidents.
*   `communication-strategies`: For effective stakeholder management.

## Examples Directory Structure

*   `examples/runbook-template.md`
*   `examples/communication-template.md`
*   `examples/post-mortem-template.md`
*   `examples/alert-config.yaml` (e.g., Prometheus alert rule)

## Custom Scripts Section ⭐ NEW

Here are the automation scripts for Incident Response Management:

1.  **`incident-initiator.py` (Python):**
    *   **Description:** Automates the initial steps of incident declaration by creating a dedicated Slack channel, a Jira incident ticket, and triggering a PagerDuty incident.
    *   **Usage:** `python incident-initiator.py --severity P1 --summary "Database connection issues affecting API"`

2.  **`post-mortem-generator.py` (Python):**
    *   **Description:** Generates a structured Markdown post-mortem template pre-filled with incident details.
    *   **Usage:** `python post-mortem-generator.py --incident-id INC-123 --summary "API Latency Spike" --date 2025-10-20`

3.  **`runbook-linter.py` (Python):**
    *   **Description:** Validates Markdown runbook files for common issues like missing sections, broken links, and outdated commands.
    *   **Usage:** `python runbook-linter.py --path docs/runbooks/api-service-runbook.md`

4.  **`send-incident-update.sh` (Shell):**
    *   **Description:** Formats and sends pre-defined incident updates to configured communication channels (e.g., Slack, email).
    *   **Usage:** `./send-incident-update.sh --incident-id INC-123 --status "Investigating" --message "Team is actively debugging database connection issues."`
