---
description: OWASP security scanning with 3-step analysis and FALSE_POSITIVE filtering
allowed-tools: Bash(git:*), Read, Task
model: claude-opus-4-1
---

# /security-review - OWASP Security Scanning

**Model**: Opus (claude-opus-4-1)

**Purpose**: Comprehensive OWASP-based security scanning with FALSE_POSITIVE filtering

## Process

### 1. Read Current Context

- Read `status.xml` for active feature
- Read `<current-story>` value
- Read story file for security requirements (if applicable)

### 2. Embed Git Diff for Full Context

Gather ALL changes upfront:

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

**Why**: Embedding full context upfront prevents repeated file reads

### 3. Spawn security-reviewer Agent

Launch security-reviewer agent (Opus model) with 3-step analysis workflow:

```markdown
Task: Security review for [story/feature name]

**Review using 3-step analysis**:

Step 1: Identify Vulnerabilities
- Scan for OWASP Top 10 vulnerabilities
- Check authentication and authorization
- Review input validation and sanitization
- Examine cryptographic implementations
- Assess data exposure risks
- Identify injection vulnerabilities (SQL, XSS, command)

Step 2: Filter False Positives (IN PARALLEL)
- Apply 17 HARD EXCLUSIONS (see SECURITY_REVIEW_CHECKLIST.md)
- Apply 12 PRECEDENTS for context-specific filtering
- Assess signal quality criteria
- Assign confidence score (1-10 scale)

Step 3: Report High-Confidence Findings
- Only report findings with confidence ≥8/10
- Categorize severity: HIGH, MEDIUM, LOW
- Provide concrete attack path for each finding
- Include file:line references
- Suggest remediation

**Reference**: SECURITY_REVIEW_CHECKLIST.md for complete methodology
```

### 4. Output Format

```markdown
## Security Review Summary

- **Verdict**: [PASS | VULNERABILITIES_FOUND]
- **HIGH Severity**: X findings
- **MEDIUM Severity**: Y findings
- **LOW Severity**: Z findings

---

## Findings

### Vuln 1: [Type] - HIGH (Confidence: 9/10)

**Location**: `file.ts:123`

**Description**: [Concrete vulnerability description]

**Attack Path**: [Specific exploitation scenario]

**Remediation**: [How to fix]

---

### Vuln 2: [Type] - MEDIUM (Confidence: 8/10)

**Location**: `file.ts:456`

**Description**: [Concrete vulnerability description]

**Attack Path**: [Specific exploitation scenario]

**Remediation**: [How to fix]

---

## OWASP Top 10 Coverage

- [x] A01: Broken Access Control
- [x] A02: Cryptographic Failures
- [x] A03: Injection
- [x] A04: Insecure Design
- [x] A05: Security Misconfiguration
- [x] A06: Vulnerable Components
- [x] A07: Authentication Failures
- [x] A08: Software/Data Integrity Failures
- [x] A09: Security Logging Failures
- [x] A10: Server-Side Request Forgery

---

## FALSE_POSITIVE Filtering Applied

- 17 Hard Exclusions: [List which were applied]
- 12 Precedents: [List which were applied]
- Filtered out: N findings with confidence <8/10
```

### 5. Confidence Scoring Guide

- **9-10**: Concrete, exploitable vulnerability with clear attack path
- **8**: Very likely vulnerability, specific code location, actionable
- **7**: Probable vulnerability, needs minor investigation
- **6**: Medium confidence, needs investigation
- **1-5**: Low confidence, likely false positive (DO NOT REPORT)

### 6. Update Story File (if security issues found)

If HIGH severity findings:
- Add "## Security Issues" section to story file
- List all HIGH severity findings with file:line
- Update story status to "In Progress" (must fix before merge)

If MEDIUM/LOW severity only:
- Add as optional improvements to story notes
- Do not block merge

## Important Notes

- **Model**: MUST use Opus (claude-opus-4-1) for security review
- **Threshold**: Only report findings with confidence ≥8/10
- **FALSE_POSITIVE Rules**: Apply ALL 17 hard exclusions + 12 precedents
- **Attack Path**: Every finding MUST include concrete attack scenario
- **No Theoretical Issues**: Only report exploitable, practical vulnerabilities
