---
description: OWASP security scanning with 3-step analysis and FALSE_POSITIVE filtering
allowed-tools: Bash(git:*), Read, Write, Edit, Grep, Task
model: claude-opus-4-1
---

# /security-review - OWASP Security Scanning

**Model**: Opus (claude-opus-4-1)

**Purpose**: Comprehensive OWASP-based security scanning with FALSE_POSITIVE filtering

## Phase 2 Enhancement: 3-Step Analysis Workflow

This command implements a rigorous 3-step security analysis process that filters out false positives while ensuring real vulnerabilities are caught.

## Process

### Step 1: Read Current Context

```bash
# Read status.xml for active feature
cat docs/development/status.xml

# Read current story value
# Read story file for security requirements (if applicable)
# Location: docs/development/features/[feature]/epics/[epic]/stories/[current-story].md
```

### Step 2: Embed Git Diff for Full Context

Gather ALL changes upfront to prevent repeated file reads:

```bash
# Git status
git status

# Files modified
git diff --name-only origin/HEAD...

# Commits
git log --no-decorate origin/HEAD...

# Full diff content
git diff --merge-base origin/HEAD
```

**Why**: Embedding full context upfront improves review quality and prevents context loss.

### Step 3: Spawn security-reviewer Agent

Launch security-reviewer agent (Opus model) with 3-step analysis workflow:

```markdown
Task: Security review for [story/feature name]

**Review using 3-step analysis**:

## Step 1: Identify Vulnerabilities

Scan for OWASP Top 10 vulnerabilities:

### A01: Broken Access Control
- Missing authorization checks
- Insecure direct object references (IDOR)
- Privilege escalation paths
- Cross-tenant data access

### A02: Cryptographic Failures
- Weak encryption algorithms
- Hard-coded secrets or keys
- Insecure random number generation
- Missing encryption for sensitive data

### A03: Injection
- SQL injection vulnerabilities
- XSS (Cross-Site Scripting)
- Command injection
- LDAP/NoSQL injection
- Template injection

### A04: Insecure Design
- Missing security controls in design
- Business logic flaws
- Insecure workflows
- Missing rate limiting

### A05: Security Misconfiguration
- Default credentials
- Unnecessary features enabled
- Verbose error messages
- Missing security headers

### A06: Vulnerable and Outdated Components
- Dependencies with known vulnerabilities
- Unmaintained libraries
- Outdated frameworks

### A07: Identification and Authentication Failures
- Weak password requirements
- Missing multi-factor authentication
- Session fixation
- Credential stuffing vulnerabilities

### A08: Software and Data Integrity Failures
- Unsigned code
- Insecure deserialization
- CI/CD pipeline vulnerabilities
- Missing integrity checks

### A09: Security Logging and Monitoring Failures
- Insufficient logging
- Missing audit trails
- Failure to detect attacks
- Inadequate monitoring

### A10: Server-Side Request Forgery (SSRF)
- Unvalidated URL redirects
- SSRF via external service calls
- Internal network access from web layer

**Also Check**:
- Authentication and authorization logic
- Input validation and sanitization
- Cryptographic implementations
- Data exposure risks
- API security (rate limiting, authentication)
- Session management
- File upload handling
- Third-party integrations

## Step 2: Filter False Positives (IN PARALLEL)

Apply FALSE_POSITIVE filtering rules from SECURITY_REVIEW_CHECKLIST.md:

### 17 HARD EXCLUSIONS

1. **Intentional Debug/Development Code**: Clearly marked as dev-only
2. **Type-Safe Operations**: TypeScript strict mode prevents the issue
3. **Framework-Handled Security**: Next.js/framework handles it automatically
4. **Test/Mock Code**: Issue only exists in test files
5. **Sanitized Input**: Input is properly validated/sanitized before use
6. **Inaccessible Code Paths**: Code path is unreachable in production
7. **Configuration Examples**: Example code, not production code
8. **Documentation/Comments**: Issue is in comments/docs, not code
9. **Third-Party API Design**: Following third-party API requirements
10. **Intentional Design Decision**: Documented trade-off or requirement
11. **False Positive Pattern**: Known pattern that's not exploitable
12. **Already Mitigated**: Issue addressed by other security controls
13. **Out of Scope**: Frontend code can't prevent backend issues
14. **Low-Severity Noise**: Minor issue with no practical exploit path
15. **Build-Time Only**: Issue in build scripts, not runtime code
16. **Deprecated/Dead Code**: Code is scheduled for removal
17. **Compensating Controls**: Alternative security measures in place

### 12 PRECEDENTS (Context-Specific Filtering)

1. **console.log in Production**: Only if contains PII/secrets
2. **eval() Usage**: Only if user input reaches eval
3. **innerHTML Usage**: Only if unsanitized user input
4. **localStorage for Sensitive Data**: Only if contains auth tokens/PII
5. **CORS Wildcards**: Only if backend has no other auth
6. **HTTP (not HTTPS)**: Only if transmitting sensitive data
7. **Missing Rate Limiting**: Only on sensitive endpoints (login, payment)
8. **Weak Randomness**: Only if used for security (tokens, crypto)
9. **Missing Input Length Limits**: Only on write operations
10. **Verbose Error Messages**: Only if exposing stack traces/internals
11. **Hardcoded URLs**: Only if pointing to production/sensitive systems
12. **Missing CSRF Protection**: Only on state-changing operations

### Signal Quality Criteria

For each finding, assess:

- **Concreteness**: Is there a specific line of code to point to?
- **Exploitability**: Can you describe a concrete attack path?
- **Impact**: What's the actual damage if exploited?
- **Context**: Does the codebase architecture prevent this issue?

### Confidence Scoring (1-10 Scale)

- **9-10**: Concrete, exploitable vulnerability with clear attack path
- **8**: Very likely vulnerability, specific code location, actionable
- **7**: Probable vulnerability, needs minor investigation
- **6**: Medium confidence, needs investigation
- **1-5**: Low confidence, likely false positive (DO NOT REPORT)

**CRITICAL RULE**: Only report findings with confidence ≥8/10

## Step 3: Report High-Confidence Findings

Only report findings that meet these criteria:
- Confidence score ≥8/10
- Concrete attack path described
- Specific file:line reference
- Clear remediation suggestion

**Reference**: SECURITY_REVIEW_CHECKLIST.md for complete methodology
```

### Step 4: Output Format

```markdown
## Security Review Summary

- **Verdict**: [PASS | VULNERABILITIES_FOUND]
- **Model Used**: claude-opus-4-1
- **HIGH Severity**: X findings
- **MEDIUM Severity**: Y findings
- **LOW Severity**: Z findings

**Philosophy**: Only reporting high-confidence findings (≥8/10) with concrete attack paths.

---

## Findings

### Vuln 1: [OWASP Category] - [Type] - HIGH (Confidence: 9/10)

**Location**: `file.ts:123`

**Description**: [Concrete vulnerability description with specific details]

**Attack Path**:
1. Attacker does [specific action]
2. This causes [specific effect]
3. Leading to [specific exploit]
4. Resulting in [specific damage]

**OWASP Category**: A0X - [Category Name]

**Impact**: [User-facing damage - data breach, account takeover, etc.]

**Remediation**:
- [Specific, actionable fix]
- [Code example if helpful]
- [Link to security best practice if applicable]

**Code Snippet**:
```typescript
// Vulnerable code
[relevant code snippet]
```

---

### Vuln 2: [OWASP Category] - [Type] - MEDIUM (Confidence: 8/10)

**Location**: `file.ts:456`

**Description**: [Concrete vulnerability description]

**Attack Path**:
1. [Specific attack scenario]
2. [Exploitation steps]
3. [Impact]

**OWASP Category**: A0X - [Category Name]

**Impact**: [Specific damage]

**Remediation**: [How to fix]

---

## OWASP Top 10 Coverage

- [x] A01: Broken Access Control - Reviewed
- [x] A02: Cryptographic Failures - Reviewed
- [x] A03: Injection - Reviewed
- [x] A04: Insecure Design - Reviewed
- [x] A05: Security Misconfiguration - Reviewed
- [x] A06: Vulnerable Components - Reviewed
- [x] A07: Authentication Failures - Reviewed
- [x] A08: Software/Data Integrity Failures - Reviewed
- [x] A09: Security Logging Failures - Reviewed
- [x] A10: Server-Side Request Forgery - Reviewed

---

## FALSE_POSITIVE Filtering Applied

### Hard Exclusions Applied:
- [✓] Rule 1: Intentional debug code (dev environment only)
- [✓] Rule 5: Input sanitized before use
- [✓] Rule 9: Third-party API design requirement

### Precedents Applied:
- [✓] Precedent 3: innerHTML with sanitized input
- [✓] Precedent 8: Randomness not used for security

### Findings Filtered Out:
- Filtered out: N findings with confidence <8/10
- Excluded: M findings due to HARD EXCLUSIONS
- Context-filtered: P findings due to PRECEDENTS

**Total Analyzed**: [X findings before filtering]
**Reported**: [Y findings after filtering (confidence ≥8)]

---

## Console Errors/Warnings

[If applicable - security-related console errors from git diff]

---

## Next Steps

[What to do next based on findings - prioritize HIGH → MEDIUM → LOW]
```

### Step 5: Update Story File (if security issues found)

**If HIGH severity findings**:
```markdown
## Security Issues (HIGH Priority - Must Fix Before Merge)

Created by: /security-review command
Date: [YYYY-MM-DD]

### High-Severity Vulnerabilities

- [ ] **Vuln 1**: [Brief description] (`file.ts:123`)
  - OWASP: A03 - Injection
  - Attack Path: [Brief attack scenario]
  - Fix: [Brief remediation]

- [ ] **Vuln 2**: [Brief description] (`file.ts:456`)
  - OWASP: A01 - Broken Access Control
  - Attack Path: [Brief attack scenario]
  - Fix: [Brief remediation]

**Status**: Story moved back to "In Progress" - must address HIGH severity findings.
```

**If MEDIUM/LOW severity only**:
```markdown
## Security Suggestions (Optional Improvements)

Created by: /security-review command
Date: [YYYY-MM-DD]

### Medium-Priority Suggestions

- [ ] **Suggestion 1**: [Brief description] (`file.ts:789`)
  - OWASP: A05 - Security Misconfiguration
  - Improvement: [Brief suggestion]

**Status**: These are optional improvements and do not block merge.
```

## Confidence Scoring Guide

### 9-10: REPORT (High Confidence)
- Concrete, exploitable vulnerability
- Clear attack path with step-by-step exploitation
- Specific code location (file:line)
- Observable damage scenario
- Actionable remediation

**Example**: Unsanitized user input directly used in SQL query
```typescript
db.query(`SELECT * FROM users WHERE id = ${userId}`)
```

### 8: REPORT (Very Likely)
- Very likely vulnerability
- Attack path needs only minor investigation
- Specific code location
- Clear remediation
- Principle violation (OWASP Top 10)

**Example**: Missing authorization check on sensitive endpoint
```typescript
app.delete('/api/users/:id', async (req, res) => {
  // No check if current user can delete this user
  await db.users.delete(req.params.id)
})
```

### 7: DO NOT REPORT (Probable)
- Probable vulnerability
- Needs investigation to confirm exploitability
- May have mitigating factors
- Unclear attack path

### 6: DO NOT REPORT (Medium Confidence)
- Medium confidence
- Needs significant investigation
- May be mitigated by other controls
- Unclear remediation

### 1-5: DO NOT REPORT (Low Confidence)
- Low confidence
- Likely false positive
- Theoretical issue without practical exploit
- Mitigated by framework/architecture

## Usage Examples

```bash
# Review current changes
/security-review

# Review will:
# 1. Read status.xml for context
# 2. Gather git diff for all changes
# 3. Spawn security-reviewer agent with Opus model
# 4. Apply 3-step analysis with FALSE_POSITIVE filtering
# 5. Report only high-confidence findings (≥8/10)
# 6. Update story file if HIGH severity issues found
```

## When to Use

- Before merging security-sensitive changes
- After implementing authentication/authorization
- When handling user input or sensitive data
- Before deploying to production
- When integrating third-party services
- After adding new API endpoints

## When NOT to Use

- For every small change (use regular `/review` instead)
- For non-security-related changes
- For documentation-only changes
- When no code changes are present

## Important Notes

### Model Requirement
**MUST use Opus (claude-opus-4-1)** for security review. This command is configured to use Opus specifically for its superior security analysis capabilities.

### Reporting Threshold
**Only report findings with confidence ≥8/10**. This prevents overwhelming developers with theoretical issues and false positives.

### FALSE_POSITIVE Rules
**Apply ALL 17 hard exclusions + 12 precedents**. The goal is to find real vulnerabilities, not theoretical problems.

### Attack Path Requirement
**Every finding MUST include a concrete attack scenario**. If you can't describe step-by-step exploitation, it's not a valid finding.

### No Theoretical Issues
**Only report exploitable, practical vulnerabilities**. Academic security concerns without real-world exploit paths should be filtered out.

### Context Matters
**Consider the full application architecture**. Frontend code can't prevent backend issues. Framework security features may mitigate concerns.

## Reference Documents

- **SECURITY_REVIEW_CHECKLIST.md**: Complete FALSE_POSITIVE filtering rules
- **OWASP Top 10 2021**: https://owasp.org/Top10/
- **Story File**: Current story for context and requirements

## Philosophy

**"High Signal, Low Noise"**

Security reviews should:
- Focus on real, exploitable vulnerabilities
- Provide concrete attack paths
- Give actionable remediation steps
- Filter out theoretical concerns
- Respect developer time

A good security review catches real issues while avoiding false positive fatigue.
