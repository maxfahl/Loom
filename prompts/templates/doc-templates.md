# Documentation Templates

**Part of**: [Project Setup Meta Prompt](../project-setup-meta-prompt.md)

## Purpose

All 12+ documentation templates including INDEX.md, PRD.md, TECHNICAL_SPEC.md, ARCHITECTURE.md, DESIGN_SYSTEM.md, DEVELOPMENT_PLAN.md, HOOKS_REFERENCE.md, TASKS.md, START_HERE.md, PROJECT_OVERVIEW.md (brownfield), YOLO_MODE.md, domain-specific docs.

## Related Files

- [../phases/phase-2-documentation.md](../phases/phase-2-documentation.md) - Doc creation workflow

## Usage

Read this file:
- In Phase 2 when creating documentation
- To get exact templates for each doc type
- To understand doc structure and required sections
- For brownfield PROJECT_OVERVIEW.md template

---

## 📚 Documentation Files to Create

### 1. INDEX.md (Master Navigation)

**Purpose**: Central navigation hub for all documentation

**Contents**:

- Quick reference table (What to find → Which document)
- Document hierarchy and relationships
- Common queries and their locations
- Code implementation references
- File structure overview

**Why Critical**: Claude Code agents reference this file to find information efficiently.

**Template Structure**:

```markdown
# Documentation Index

## Quick Reference

| Need              | Document        | Path   |
| ----------------- | --------------- | ------ |
| [What user needs] | [Document name] | [Path] |

## Document Hierarchy

[Visual tree structure]

## Common Queries

- "How do I X?" → See [Document]
- "Where is Y?" → See [Document]

## Code References

- [Feature]: [File path]
```

### 2. README.md (Root)

**Purpose**: Minimal getting started guide for users

**Contents**:

- Project name and one-line description
- Quick start (3-5 steps maximum)
- Prerequisites
- Installation commands
- Basic usage
- Link to documentation

**Keep It**:

- Extremely concise
- Action-oriented
- Copy-paste friendly
- Under 3KB

### 3. PRD.md (Product Requirements Document)

**Purpose**: Defines WHAT to build and WHY

**Contents**:

- Executive summary
- Problem statement
- Target users
- Core features (prioritized)
- Non-functional requirements
- Success metrics
- Out of scope items
- Timeline and milestones

**Sections**:

```markdown
# Product Requirements Document

## Executive Summary

[1-2 paragraphs]

## Problem Statement

[What problem are we solving?]

## Target Users

[Who is this for?]

## Core Features

### Must Have (P0)

### Should Have (P1)

### Nice to Have (P2)

## Non-Functional Requirements

- Performance
- Security
- Scalability
- Accessibility

## Success Metrics

[How do we measure success?]

## Out of Scope

[What we're NOT building]

## Timeline

[Phases and milestones]
```

### 4. TECHNICAL_SPEC.md

**Purpose**: Defines HOW to build (implementation details)

**Contents**:

- Technology stack (with versions)
- System architecture overview
- API specifications
- Database schema
- Data models
- External integrations
- Security considerations
- Performance requirements
- Error handling strategy

**Sections**:

```markdown
# Technical Specifications

## Tech Stack

- Framework: [Name] [Version]
- Language: [Name] [Version]
- Database: [Name] [Version]
  [Complete stack]

## API Specifications

### Endpoint: [Name]

- Method: [GET/POST/etc]
- Path: [/api/path]
- Request: [Schema]
- Response: [Schema]
- Errors: [Error codes]

## Database Schema

[Tables, relationships, indexes]

## Data Models

[TypeScript interfaces/types]

## External Integrations

[Third-party services]

## Security

[Authentication, authorization, data protection]

## Performance

[Caching, optimization strategies]

## Error Handling

[Strategy and patterns]
```

### 5. ARCHITECTURE.md

**Purpose**: System design and component relationships

**Contents**:

- High-level architecture diagram (Mermaid)
- Component breakdown
- Data flow diagrams
- Deployment architecture
- Technology decisions and rationale
- Scalability considerations
- Design patterns used

**Include**:

- Visual diagrams (Mermaid syntax)
- Clear component boundaries
- Communication patterns
- State management approach

### 6. DESIGN_SYSTEM.md

**Purpose**: UI/UX guidelines and component library

**Contents**:

- Component library priority order
- Color system (CSS variables)
- Typography scale
- Spacing system
- Component mapping (feature → component)
- Responsive breakpoints
- Accessibility guidelines
- Dark mode support
- Animation/motion guidelines

**Critical Section**:

```markdown
## Component Library Priority 

1. [Primary Library] ← Check FIRST
   ↓ (if not found)
2. [Secondary Library] ← Check SECOND
   ↓ (if not found)
3. [Tertiary Library] ← Check THIRD
   ↓ (if not found)
4. [Base Library] ← Check FOURTH
   ↓ (if not found)
5. Custom Build ← Last Resort

## Component Mapping

| Feature | Library | Component | Installation |
| ------- | ------- | --------- | ------------ |
```

### 7. TASKS.md

**Purpose**: Development task checklist

**Contents**:

- Phases and milestones
- Individual tasks (specific, actionable)
- Task dependencies
- Acceptance criteria
- Estimated effort
- Current status

**Format**:

```markdown
# Development Tasks

## Phase 1: Foundation

### Week 1: Setup

- [ ] Task 1 (Est: 2h)
  - Acceptance: [What done looks like]
  - Dependencies: None
- [ ] Task 2 (Est: 4h)
  - Acceptance: [Criteria]
  - Dependencies: Task 1

## Phase 2: Core Features

[Continue...]
```

### 8. DEVELOPMENT_PLAN.md

**Purpose**: Development methodology and roadmap

**Contents**:

- Development methodology (TDD, Agile, etc.)
- Red-Green-Refactor explanation (if TDD)
- Code style guide
- Testing strategy
- CI/CD pipeline
- Release process
- 12-week (or appropriate) roadmap

**If TDD**:

```markdown
## Test-Driven Development (MANDATORY)

### Red-Green-Refactor Cycle

1. 🔴 RED: Write failing test first
2. 🟢 GREEN: Write minimal code to pass
3. 🔵 REFACTOR: Clean up code
4. ♻️ REPEAT: Iterate

### TDD Rules

1. Write tests BEFORE implementation
2. Write simplest test first
3. Watch tests fail (RED)
   [etc.]
```

### 9. PROJECT_SUMMARY.md

**Purpose**: Comprehensive project overview

**Contents**:

- Project description
- Goals and objectives
- Key features summary
- Technical highlights
- AI agent workflow structure
- Timeline overview
- Links to all other docs

### 10. EXECUTIVE_SUMMARY.md

**Purpose**: High-level technical summary

**Contents**:

- One-paragraph project description
- Tech stack summary
- Key technical decisions
- Implementation approach
- Current status
- Next steps

### 11. START_HERE.md

**Purpose**: Navigation guide for different roles

**Contents**:

```markdown
# Start Here Guide

## For Developers

1. Read [Document 1]
2. Review [Document 2]
3. Start with [Task]

## For Designers

1. Check [Design System]
2. Review [Mockups]

## For Project Managers

1. Review [PRD]
2. Check [Timeline]

## For QA/Testers

1. Review [Test Strategy]
2. Check [Test Cases]
```

### 12. PROJECT_OVERVIEW.md (Brownfield Only)

**Purpose**: Comprehensive analysis of existing brownfield codebase

**When to Create**: ONLY for brownfield projects, created by research agent BEFORE other docs

**Note**: This is an extensive template (~220 lines) by design. Brownfield analysis requires thoroughness to understand existing codebases. The length is intentional and necessary.

**Contents**:

```markdown
# Project Overview - Existing Codebase Analysis

**Project Name**: [Detected name]
**Analysis Date**: [Date]
**Codebase Location**: [Path]

## Executive Summary

[1-2 paragraph overview of what this project is and does]

## Project Structure
```

[Complete directory tree]

````

**Key Directories**:
- `[dir]/` - [Purpose]
- `[dir]/` - [Purpose]

## Technology Stack

**Framework**: [Name] [Version]
**Language**: [Name] [Version]
**Database**: [Name] [Version]
**Testing**: [Framework] [Version]

**Complete Dependencies**:
[List from package.json, requirements.txt, etc.]

## Setup & Installation

### Prerequisites
- [Requirement 1]
- [Requirement 2]

### Installation Steps
```bash
# Step 1
[command]

# Step 2
[command]
````

### Environment Variables

Required variables (from .env.example or code):

```
VAR_NAME=description
VAR_NAME=description
```

## Running the Project

### Development

```bash
[command to run dev server]
```

### Production

```bash
[command to run production]
```

### Testing

```bash
# Run all tests
[command]

# Run specific test
[command]

# Run with coverage
[command]
```

### Building

```bash
[build command]
```

## Scripts Reference

### NPM/Yarn Scripts (from package.json)

| Script   | Command     | Purpose        |
| -------- | ----------- | -------------- |
| `[name]` | `[command]` | [What it does] |

### Shell Scripts (from scripts/, bin/, etc.)

| Script   | Location | Purpose        | Usage          |
| -------- | -------- | -------------- | -------------- |
| `[name]` | `[path]` | [What it does] | `[how to run]` |

## Configuration Files

| File     | Purpose              | Key Settings         |
| -------- | -------------------- | -------------------- |
| `[file]` | [What it configures] | [Important settings] |

## Architecture

### Entry Point

- Main file: `[path]`
- Startup flow: [Description]

### Key Components

1. **[Component/Module Name]** (`[path]`)
   - Purpose: [What it does]
   - Key functions: [List]

### Data Flow

[Describe how data flows through the application]

### API Endpoints (if applicable)

| Method  | Path          | Purpose        | Handler       |
| ------- | ------------- | -------------- | ------------- |
| `[GET]` | `[/api/path]` | [What it does] | `[file:line]` |

### Database Schema (if applicable)

**Tables**:

- `[table_name]`: [Purpose]
  - Columns: [List]

## Testing Strategy

**Test Location**: `[path]`
**Test Framework**: [Name]
**Coverage**: [X%] (current)

**Test Types**:

- Unit tests: `[pattern]`
- Integration tests: `[pattern]`
- E2E tests: `[pattern]`

**Running Tests**:

```bash
[commands]
```

## Development Workflow

### Branch Strategy

- Main branch: `[name]`
- Development branch: `[name]`
- Feature branches: `[pattern]`

### Commit Patterns

[Analyze recent commits for patterns]

- Convention: [Conventional Commits / Other]
- Examples: [List recent commits]

### Code Review

- PR template: [Location]
- Required checks: [List]

### CI/CD

- Platform: [GitHub Actions / GitLab CI / etc.]
- Config: `[file]`
- Workflows: [List workflows and what they do]

## Existing Documentation

**README.md**: [Summary]
**Other Docs**: [List and summarize]
**Code Comments**: [Coverage level - Good/Moderate/Sparse]
**API Docs**: [Location if exists]

## Dependencies & Integrations

### External Services

- [Service 1]: [Purpose, how integrated]
- [Service 2]: [Purpose, how integrated]

### Third-Party APIs

- [API 1]: [What it's used for]
- [API 2]: [What it's used for]

### Database Connections

- Type: [PostgreSQL/MongoDB/etc.]
- Connection: [How configured]

## Code Quality

**Linting**: [ESLint/Prettier/etc.] - Config: `[file]`
**Type Checking**: [TypeScript/Flow/etc.]
**Formatting**: [Prettier/etc.]
**Pre-commit Hooks**: [Husky/etc.]

## Pain Points & Opportunities

### Identified Issues

- [Issue 1]: [Description]
- [Issue 2]: [Description]

### Improvement Opportunities

- [Opportunity 1]: [Description]
- [Opportunity 2]: [Description]

### Missing Documentation

- [What's not documented]

### Technical Debt

- [Debt item 1]
- [Debt item 2]

## Recommendations

### Immediate Actions

1. [Recommendation 1]
2. [Recommendation 2]

### Long-term Improvements

1. [Improvement 1]
2. [Improvement 2]

---

**Analysis Completed**: [Date]
**Next Steps**: Use this document as foundation for TECHNICAL_SPEC.md, ARCHITECTURE.md, and other planning docs.

````

**CRITICAL IMPORTANCE**:
- This doc must be created FIRST for brownfield projects
- All other docs reference this as source of truth
- Extremely detailed - include file paths, code examples, command examples
- Should be 5-10KB minimum for thorough analysis

### 13. Domain-Specific Docs

Based on project type, add:

**Web Applications**:
- API_REFERENCE.md
- DEPLOYMENT.md
- MONITORING.md

**Data Engineering**:
- DATA_PIPELINE.md
- ETL_SPECIFICATION.md

**Mobile Apps**:
- PLATFORM_SPECIFIC.md (iOS/Android)
- APP_STORE_GUIDELINES.md

**Libraries/SDKs**:
- API_DOCUMENTATION.md
- INTEGRATION_GUIDE.md
- CHANGELOG.md

### 14. YOLO_MODE.md Template

**Purpose**: Complete YOLO mode workflow control documentation

**When to Create**: Always create for all projects

**Complete YOLO_MODE.md Structure**:

_(Template content exists but not shown here for brevity)_

---

### 15. CODE_REVIEW_PRINCIPLES.md Template

**Purpose**: 7-phase hierarchical code review framework with triage matrix

**When to Create**: Always create for all projects (added in Phase 1: Core Review Enhancements)

**Source**: OneRedOak review workflows (`04-REFERENCE-EXTRACTS.md` lines 62-141)

**Complete CODE_REVIEW_PRINCIPLES.md Structure**:

```markdown
# Code Review Principles

**Version**: 1.0
**Last Updated**: [YYYY-MM-DD]
**Framework**: 7-Phase Hierarchical Review

---

## Overview

This document defines the code review methodology for [Project Name]. All code reviews follow a hierarchical 7-phase framework that prioritizes critical architectural and security concerns before moving to optimization and polish.

### Philosophy: "Net Positive > Perfection"

**Merge Criteria**:
- Does this change improve the codebase health overall?
- Are critical issues (Blockers) addressed?
- Is the implementation reasonably maintainable?

**If YES to all three → APPROVE**, even if not perfect.

**Why**: Shipping improved code is better than blocking good-enough code. Perfection is the enemy of progress.

---

## Hierarchical Review Framework

All code reviews follow this prioritized checklist:

### 1. Architectural Design & Integrity (Critical)

**Priority**: Critical - Must address before merge if issues found

**Review Checklist**:
- Evaluate if the design aligns with existing architectural patterns and system boundaries
- Assess modularity and adherence to Single Responsibility Principle
- Identify unnecessary complexity - could a simpler solution achieve the same goal?
- Verify the change is atomic (single, cohesive purpose) not bundling unrelated changes
- Check for appropriate abstraction levels and separation of concerns

**Project-Specific References**:
- Review against ARCHITECTURE.md for system design alignment
- Check TECHNICAL_SPEC.md for implementation patterns
- Verify INDEX.md for project context

---

### 2. Functionality & Correctness (Critical)

**Priority**: Critical - Must address before merge if issues found

**Review Checklist**:
- Verify the code correctly implements the intended business logic
- Identify handling of edge cases, error conditions, and unexpected inputs
- Detect potential logical flaws, race conditions, or concurrency issues
- Validate state management and data flow correctness
- Ensure idempotency where appropriate

**Project-Specific References**:
- Verify against PRD.md for requirements compliance
- Check acceptance criteria in current story file

---

### 3. Security (Non-Negotiable)

**Priority**: Blocker - MUST fix before merge

**Review Checklist**:
- Verify all user input is validated, sanitized, and escaped (XSS, SQLi, command injection prevention)
- Confirm authentication and authorization checks on all protected resources
- Check for hardcoded secrets, API keys, or credentials
- Assess data exposure in logs, error messages, or API responses
- Validate CORS, CSP, and other security headers where applicable
- Review cryptographic implementations for standard library usage

**Related Documentation**:
- See SECURITY_REVIEW_CHECKLIST.md for OWASP-based security scanning (if available)

---

### 4. Maintainability & Readability (High Priority)

**Priority**: High - Strong recommendation to fix

**Review Checklist**:
- Assess code clarity for future developers
- Evaluate naming conventions for descriptiveness and consistency
- Analyze control flow complexity and nesting depth
- Verify comments explain 'why' (intent/trade-offs) not 'what' (mechanics)
- Check for appropriate error messages that aid debugging
- Identify code duplication that should be refactored

**Engineering Principles**:
- **DRY** (Don't Repeat Yourself): Eliminate duplication
- **KISS** (Keep It Simple, Stupid): Prefer simple solutions
- **YAGNI** (You Aren't Gonna Need It): Don't add unused features

---

### 5. Testing Strategy & Robustness (High Priority)

**Priority**: High - Strong recommendation to fix

**TDD Requirements** (Project-Specific):
- **CRITICAL**: Verify tests were written FIRST (Red-Green-Refactor cycle)
- Check test coverage is ≥80% (MANDATORY per project TDD policy from DEVELOPMENT_PLAN.md)
- Confirm tests follow project testing conventions
- Validate test file naming and organization matches project structure

**General Testing Review**:
- Evaluate test coverage relative to code complexity and criticality
- Verify tests cover failure modes, security edge cases, and error paths
- Assess test maintainability and clarity
- Check for appropriate test isolation and mock usage
- Identify missing integration or end-to-end tests for critical paths

**Project-Specific References**:
- Check DEVELOPMENT_PLAN.md for TDD methodology
- Verify test requirements in current story file

---

### 6. Performance & Scalability (Important)

**Priority**: Important - Recommend fixing if performance-critical

**Review Checklist**:
- **Backend**: Identify N+1 queries, missing indexes, inefficient algorithms
- **Frontend**: Assess bundle size impact, rendering performance, Core Web Vitals
- **API Design**: Evaluate consistency, backwards compatibility, pagination strategy
- Review caching strategies and cache invalidation logic
- Identify potential memory leaks or resource exhaustion

---

### 7. Dependencies & Documentation (Important)

**Priority**: Important - Recommend updating

**Component Library Priority Order** (Project-Specific):

For UI components, verify library priority order from DESIGN_SYSTEM.md:
1. **Kibo UI** (dev tools, specialized components) - CHECK FIRST
2. **Blocks.so** (layouts, dashboard patterns) - CHECK SECOND
3. **ReUI** (animations, motion) - CHECK THIRD
4. **shadcn/ui** (base primitives) - CHECK FOURTH
5. **Custom** (last resort only) - ONLY IF NOTHING EXISTS

**Flag if**: Custom component created when library option exists

**General Dependencies Review**:
- Question necessity of new third-party dependencies
- Assess dependency security, maintenance status, and license compatibility
- Verify API documentation updates for contract changes
- Check for updated configuration or deployment documentation

**Project Documentation References**:
- Review code against INDEX.md for project context
- Check compliance with PRD.md requirements
- Verify technical implementation matches TECHNICAL_SPEC.md
- Confirm UI follows DESIGN_SYSTEM.md guidelines
- Check TDD compliance with DEVELOPMENT_PLAN.md

---

## Triage Matrix

All review findings must be categorized using this triage matrix:

### [Blocker]

**Definition**: Must be fixed before merge

**Examples**:
- Security vulnerability (Phase 3)
- Architectural regression (Phase 1)
- TDD non-compliance (tests not written first, <80% coverage) (Phase 5)
- Breaks existing functionality (Phase 2)
- Hardcoded secrets/credentials (Phase 3)

**Action**: Block merge until fixed

---

### [Improvement]

**Definition**: Strong recommendation for improving implementation

**Examples**:
- Unnecessary complexity (Phase 1)
- Missing edge case handling (Phase 2)
- Poor naming conventions (Phase 4)
- Low test coverage on critical path (Phase 5)
- Performance bottleneck (Phase 6)
- Missing documentation (Phase 7)

**Action**: Request changes with explanation

---

### [Nit]

**Definition**: Minor polish, optional

**Examples**:
- Typo in comment
- Inconsistent whitespace
- Suggestion for alternative approach (not clearly better)
- Preference for different code style (already meets standards)

**Action**: Suggest but don't block merge

---

## Communication Principles

When providing code review feedback:

1. **Actionable Feedback**: Provide specific, actionable suggestions with `file:line` references
2. **Explain the "Why"**: When suggesting changes, explain the underlying engineering principle that motivates the suggestion
3. **Apply Triage Matrix**: Categorize significant issues to help the author prioritize
4. **Be Constructive**: Maintain objectivity and assume good intent
5. **Provide Examples**: When possible, show code examples of recommended approach
6. **Link to Standards**: Reference project documentation (ARCHITECTURE.md, DESIGN_SYSTEM.md, etc.)

---

## Review Output Format

Code reviews should follow this structure:

```markdown
## Review Summary

- **Verdict**: [APPROVE | REQUEST_CHANGES | NEEDS_DISCUSSION]
- **Blockers**: X issues
- **Improvements**: Y recommendations
- **Nits**: Z minor suggestions

---

## Phase 1: Architectural Design & Integrity

[Blocker/Improvement/Nit findings for architecture...]

## Phase 2: Functionality & Correctness

[Blocker/Improvement/Nit findings for functionality...]

## Phase 3: Security

[Blocker/Improvement/Nit findings for security...]

## Phase 4: Maintainability & Readability

[Blocker/Improvement/Nit findings for maintainability...]

## Phase 5: Testing Strategy & Robustness

[Blocker/Improvement/Nit findings for testing...]

## Phase 6: Performance & Scalability

[Blocker/Improvement/Nit findings for performance...]

## Phase 7: Dependencies & Documentation

[Blocker/Improvement/Nit findings for dependencies...]

---

## Net Positive Assessment

- Does this change improve the codebase health overall? [YES/NO]
- Are all Blockers addressed? [YES/NO]
- Is the implementation reasonably maintainable? [YES/NO]

**Recommendation**: [APPROVE | REQUEST_CHANGES]
```

---

## Related Documentation

- **/review** command - Triggers code review using this framework
- **code-reviewer** agent - Implements this 7-phase review methodology
- **SECURITY_REVIEW_CHECKLIST.md** - Security-specific review (Phase 3 deep-dive)
- **DESIGN_PRINCIPLES.md** - Design review methodology (UI/UX focus)
- **DEVELOPMENT_PLAN.md** - TDD requirements and testing standards

---

_Last updated: [YYYY-MM-DD]_
_For updates to this file, use the `#` key during Claude Code sessions_
```

**Customization Notes**:
- Replace `[Project Name]` with actual project name
- Update `[YYYY-MM-DD]` with current date
- Adjust TDD requirements based on project enforcement level (STRICT vs RECOMMENDED)
- Update component library priority order if project uses different libraries
- Add project-specific architectural patterns or security requirements

---

### 16. SECURITY_REVIEW_CHECKLIST.md Template

**Purpose**: OWASP-based security scanning methodology with FALSE_POSITIVE filtering

**When to Create**: Always create for all projects (added in Phase 2: Security Review)

**Source**: OneRedOak security review workflows (`04-REFERENCE-EXTRACTS.md` lines 155-232)

**Complete SECURITY_REVIEW_CHECKLIST.md Structure**:

```markdown
# Security Review Checklist

**Version**: 1.0
**Last Updated**: [YYYY-MM-DD]
**Framework**: OWASP Top 10 with FALSE_POSITIVE Filtering

---

## Overview

This document defines the security review methodology for [Project Name]. All security reviews follow OWASP Top 10 guidelines with battle-tested FALSE_POSITIVE filtering rules from Anthropic.

### 3-Step Analysis Workflow

1. **Step 1**: Identify Vulnerabilities (scan for OWASP Top 10)
2. **Step 2**: Filter False Positives (apply 17 hard exclusions + 12 precedents)
3. **Step 3**: Confidence Scoring (only report findings ≥8/10)

### Model Requirement

**CRITICAL**: Security reviews MUST use **Opus model** (claude-opus-4-1) for maximum accuracy.

---

## OWASP Top 10 Vulnerabilities

### A01: Broken Access Control

**Check for**:
- Missing authentication/authorization checks on protected endpoints
- Insecure direct object references (IDOR) - user can access other users' data
- Privilege escalation opportunities (user can elevate to admin)
- Path traversal vulnerabilities (`../../../etc/passwd`)

**Example Vulnerable Code**:
```typescript
// BAD: No auth check
app.get('/api/user/:id', (req, res) => {
  const user = db.getUser(req.params.id); // Any user can access any ID
  res.json(user);
});

// GOOD: Auth check
app.get('/api/user/:id', authenticate, (req, res) => {
  if (req.user.id !== req.params.id && !req.user.isAdmin) {
    return res.status(403).json({ error: 'Forbidden' });
  }
  const user = db.getUser(req.params.id);
  res.json(user);
});
```

---

### A02: Cryptographic Failures

**Check for**:
- Hardcoded secrets, API keys, or credentials in code
- Weak encryption algorithms (MD5, SHA1, DES - use AES-256, SHA-256+)
- Insecure random number generation (`Math.random()` for security tokens)
- Missing encryption for sensitive data (passwords, PII, tokens)

**Example Vulnerable Code**:
```typescript
// BAD: Hardcoded secret
const API_KEY = "sk-1234567890abcdef";

// GOOD: Environment variable
const API_KEY = process.env.API_KEY;
```

---

### A03: Injection

**Check for**:
- SQL injection (user input in SQL queries without sanitization)
- XSS (user input rendered in HTML without escaping)
- Command injection (user input in shell commands)
- LDAP/XML/NoSQL injection

**Example Vulnerable Code**:
```typescript
// BAD: SQL injection
db.query(`SELECT * FROM users WHERE id = ${req.params.id}`);

// GOOD: Parameterized query
db.query('SELECT * FROM users WHERE id = ?', [req.params.id]);
```

---

### A04-A10: [Include remaining OWASP categories]

_(Condense for token efficiency - full template would include all 10 categories)_

---

## FALSE_POSITIVE Filtering Rules

**CRITICAL**: Apply these rules VERBATIM. Battle-tested by Anthropic.

### HARD EXCLUSIONS (17 Rules)

Automatically exclude findings matching these patterns:

1. **Denial of Service (DOS)** - Resource exhaustion attacks
2. **Secrets on disk** - If otherwise secured
3. **Rate limiting** - Service overload scenarios
4. **Memory/CPU exhaustion** - Resource consumption issues
5. **Input validation** - Non-security-critical fields without proven impact
6. **GitHub Actions** - Input sanitization unless clearly exploitable
7. **Lack of hardening** - Best practices vs concrete vulnerabilities
8. **Theoretical race conditions** - Only report if concretely problematic
9. **Outdated libraries** - Managed separately
10. **Memory safety** - Impossible in Rust/memory-safe languages
11. **Unit test files** - Test-only code
12. **Log spoofing** - Unsanitized user input in logs
13. **SSRF path-only** - Only host/protocol control is SSRF
14. **AI prompt injection** - User content in AI prompts
15. **Regex injection** - Untrusted content in regex
16. **Regex DOS** - Regex performance issues
17. **Documentation** - Markdown files
18. **Missing audit logs** - Not a vulnerability

### PRECEDENTS (12 Rules)

Context-specific filtering:

1. **Logging secrets**: High-value secrets in plaintext IS a vuln. URLs are safe
2. **UUIDs**: Unguessable, no validation needed
3. **Env vars/CLI flags**: Trusted in secure environments
4. **Resource leaks**: Memory/file descriptor leaks not valid
5. **Subtle web vulns**: Tabnabbing, XS-Leaks, etc. - only if extremely high confidence
6. **React/Angular XSS**: Secure unless using `dangerouslySetInnerHTML`
7. **GitHub Actions**: Most not exploitable, require concrete attack path
8. **Client-side auth**: Server handles validation
9. **MEDIUM findings**: Only if obvious and concrete
10. **Jupyter notebooks**: Most not exploitable
11. **Logging non-PII**: Only secrets/passwords/PII are vulns
12. **Shell script injection**: Require concrete attack path

---

## Confidence Scoring (1-10 Scale)

**CRITICAL**: Only report findings with confidence ≥8/10

### Scoring Guidelines

- **9-10**: Concrete, exploitable vulnerability. Clear attack path. REPORT.
- **8**: Very likely vulnerability. Specific location. Actionable. REPORT.
- **7**: Probable vulnerability. Needs investigation. DO NOT REPORT.
- **6**: Medium confidence. Needs investigation. DO NOT REPORT.
- **1-5**: Low confidence. Likely false positive. DO NOT REPORT.

### Signal Quality Criteria

For each finding, assess:
1. Is there a concrete, exploitable vulnerability with clear attack path?
2. Does this represent a real security risk vs theoretical best practice?
3. Are there specific code locations and reproduction steps?
4. Would this finding be actionable for a security team?

If NO to any question → Reduce confidence score

---

## Severity Classification

### HIGH Severity

**Criteria**:
- Exploitable vulnerability with direct security impact
- Data breach, code execution, or privilege escalation possible
- Immediate remediation required

**Examples**:
- SQL injection on production database
- Hardcoded admin credentials
- Authentication bypass
- Unvalidated file upload leading to code execution

---

### MEDIUM Severity

**Criteria**:
- Security weakness requiring additional conditions to exploit
- Limited impact or requires user interaction
- Should be fixed but not immediately blocking

**Examples**:
- Missing rate limiting on non-critical endpoints
- Weak password requirements
- Lack of CSRF tokens on low-impact forms

---

### LOW Severity

**Criteria**:
- Minor security improvement
- Theoretical concern with unclear attack path
- Optional enhancement

**Examples**:
- Missing security headers on static assets
- Verbose error messages (non-sensitive info)
- Minor information disclosure

---

## Output Format

Security reviews must follow this structure:

```markdown
## Security Review Summary

- **Verdict**: [PASS | VULNERABILITIES_FOUND]
- **HIGH Severity**: X findings (must fix before merge)
- **MEDIUM Severity**: Y findings (should fix)
- **LOW Severity**: Z findings (optional)

---

## Findings

### Vuln 1: [OWASP Category] - HIGH (Confidence: 9/10)

**Location**: `file.ts:123`

**Description**:
[Concrete vulnerability description]

**Attack Path**:
1. Attacker performs action X
2. System responds with Y
3. Attacker exploits Z to achieve [impact]

**Impact**: [Data breach / Code execution / Privilege escalation]

**Remediation**:
```typescript
// FIX: Use parameterized query
db.query('SELECT * FROM users WHERE id = ?', [req.params.id]);
```

---

## OWASP Top 10 Coverage Checklist

- [x] A01: Broken Access Control
- [x] A02: Cryptographic Failures
- [x] A03: Injection
- [x] A04: Insecure Design
- [x] A05: Security Misconfiguration
- [x] A06: Vulnerable Components (skipped - managed separately)
- [x] A07: Authentication Failures
- [x] A08: Software/Data Integrity Failures
- [x] A09: Security Logging Failures
- [x] A10: Server-Side Request Forgery

---

## FALSE_POSITIVE Filtering Applied

- **Hard Exclusions Applied**: [List which of 17]
- **Precedents Applied**: [List which of 12]
- **Findings Filtered**: N findings with confidence <8/10
```

---

## Related Documentation

- **/security-review** command - Triggers security review using this checklist
- **security-reviewer** agent - Implements OWASP methodology with Opus model
- **CODE_REVIEW_PRINCIPLES.md** - General code review (includes security in Phase 3)
- **TECHNICAL_SPEC.md** - API security requirements
- **ARCHITECTURE.md** - Security boundaries and trust zones

---

_Last updated: [YYYY-MM-DD]_
_For updates to this file, use the `#` key during Claude Code sessions_
```

**Customization Notes**:
- Replace `[Project Name]` with actual project name
- Update `[YYYY-MM-DD]` with current date
- Add project-specific security requirements (e.g., PCI-DSS, HIPAA, SOC2)
- Expand A04-A10 OWASP categories with project-relevant examples
- Update severity thresholds based on project risk tolerance

