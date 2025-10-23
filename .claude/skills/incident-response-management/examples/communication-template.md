# Incident Communication Template

## Internal Communication Template

**Subject:** Incident Update: [INCIDENT_ID] - [SERVICE_NAME] - [CURRENT_STATUS]

**To:** #incident-[service-name], @on-call-engineers, @engineering-leadership

**Body:**

**Incident ID:** [INCIDENT_ID]
**Service Affected:** [SERVICE_NAME]
**Current Status:** [e.g., Investigating, Identified, Mitigated, Resolved]
**Severity:** [P0, P1, P2]
**Impact:** [Brief description of current impact, e.g., "Users experiencing intermittent login failures."]
**What we know:** [Concise summary of current understanding, e.g., "Database connection pool exhaustion."]
**Actions taken/Next Steps:** [List actions, e.g., "Restarted database instances. Monitoring for recovery."]
**Next Update:** [Time, e.g., "Within 15 minutes" or "Once status changes"]

**Incident Commander:** [Name]

---

## External Communication Template (Customer-Facing)

**Subject:** [SERVICE_NAME] - [STATUS: Investigating / Monitoring / Resolved]

**To:** Affected Customers (via Status Page / Email List)

**Body:**

**[Date] [Time] UTC - [STATUS]**

We are currently [investigating / monitoring / have resolved] an issue affecting [SERVICE_NAME].

**Impact:** [Brief, customer-friendly description of impact, e.g., "Users may be experiencing intermittent difficulties logging in or accessing certain features."]

**What we're doing:** Our engineering team is actively [investigating the root cause / monitoring the recovery of the service / has implemented a fix and is monitoring stability].

We apologize for any inconvenience this may cause and appreciate your patience.

**Next Update:** We will provide another update [in approximately X minutes / as soon as more information is available / once the issue is fully resolved].

---

**[Date] [Time] UTC - Resolved**

This incident has been resolved. [SERVICE_NAME] is now operating normally. We will conduct a full post-mortem to understand the root cause and implement preventative measures. We thank you for your patience.
