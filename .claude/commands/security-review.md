---
description: OWASP security scanning with 3-step analysis and FALSE_POSITIVE filtering
model: opus
---

# /security-review - Security Review

## What This Command Does

OWASP-based security scanning with 3-step analysis workflow and intelligent FALSE_POSITIVE filtering.

## Process

1. **Read Current Context**:
   - Read status.xml for active feature
   - Read current story file
   - Understand what code is being reviewed

2. **Gather Code for Review**:
   ```bash
   # All modified files
   git diff --name-only origin/HEAD...

   # Full diff
   git diff origin/HEAD...
   ```

3. **Delegate to Security Reviewer Agent**:

   ```markdown
   Task(
     subagent_type="security-reviewer",
     description="OWASP security scan of uncommitted changes",
     prompt="Execute comprehensive security review using 3-step analysis workflow:

     STEP 1: Identify potential vulnerabilities (OWASP Top 10)
     STEP 2: Apply FALSE_POSITIVE filters (17 hard exclusions + 12 precedents)
     STEP 3: Score remaining findings (report only ≥8/10 confidence)

     For each finding, provide:
     - Vulnerability type (OWASP category)
     - Concrete attack path
     - Code location (file:line)
     - Severity rating
     - Remediation steps

     Focus on exploitable vulnerabilities only. Filter out theoretical risks."
   )
   ```

4. **Security Reviewer Will Execute**:
   - **Step 1**: Scan for OWASP Top 10 vulnerabilities
   - **Step 2**: Apply FALSE_POSITIVE filtering
   - **Step 3**: Score and report high-confidence findings (≥8/10)

5. **Report Format**:
   ```markdown
   # Security Review Results

   **Review Date**: [Date]
   **Methodology**: OWASP Top 10 + 3-Step Analysis
   **Model**: Claude Opus 4 (high confidence analysis)

   ## Summary
   - Total Findings: [X]
   - Critical: [X]
   - High: [X]
   - Medium: [X]
   - Low: [X]

   ## Critical Findings

   ### 1. [Vulnerability Type] - [Brief Description]
   **Location**: `file.js:123`
   **Severity**: Critical (10/10)
   **OWASP Category**: [A01:2021-Broken Access Control]

   **Attack Path**:
   1. Attacker sends request with [specific payload]
   2. Application processes without [validation]
   3. Results in [specific impact]

   **Remediation**:
   - Step 1: [Specific action]
   - Step 2: [Specific action]

   **Code**:
   ```javascript
   // Vulnerable code
   [snippet]
   ```

   ## Recommendations
   [Overall security recommendations]

   ## FALSE_POSITIVE Exclusions Applied
   [List of patterns filtered out]
   ```

## Agent Delegation

```markdown
Task(
  subagent_type="security-reviewer",
  description="OWASP security scan",
  prompt="Execute 3-step security analysis: (1) Identify OWASP Top 10 vulnerabilities, (2) Apply FALSE_POSITIVE filters, (3) Score and report high-confidence findings ≥8/10. Provide concrete attack paths for all findings."
)
```

## Recommended Skills

<!-- TODO: Add relevant skills from .claude/skills/ -->

- `owasp-top-10` - For vulnerability categories
- `api-security-best-practices` - For API-specific security
- `penetration-testing` - For attack path analysis

Use these skills heavily throughout execution to ensure best practices.

**Skill Troubleshooting Authority**: If any referenced skill does not work or any script within the skill does not work, Claude Code has the authority to fix them.

## Arguments

This command takes no arguments. Reviews all uncommitted changes.

## Examples

```
/security-review
```

Executes comprehensive OWASP security review.

## Important Notes

- Uses **Opus model** for highest quality security analysis
- Only reports high-confidence findings (≥8/10)
- Filters out theoretical/low-probability risks
- Focuses on exploitable vulnerabilities with concrete attack paths
