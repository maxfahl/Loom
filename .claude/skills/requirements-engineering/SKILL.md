---
name: requirements-engineering
version: 0.1.0
category: Software Development / Requirements
tags: requirements, elicitation, analysis, specification, validation, management, user stories, functional requirements, non-functional requirements, RTM, agile, AI, ML
description: Guides Claude in defining clear, testable, and well-managed software requirements.
---

# Requirements Engineering Skill

## 1. Skill Purpose

This skill enables Claude to effectively assist in all phases of Requirements Engineering (RE), from elicitation and analysis to specification, validation, and management. The goal is to ensure the definition of clear, unambiguous, testable, and traceable requirements that align with business objectives and user needs, leveraging modern practices including AI/ML integration and Agile methodologies.

## 2. When to Activate This Skill

Activate this skill when:
- A new project or feature is being initiated and requirements need to be defined.
- Existing requirements are unclear, inconsistent, or incomplete.
- There's a need to refine user stories or acceptance criteria.
- Traceability between requirements, design, and tests needs to be established or verified.
- Stakeholder communication regarding project scope and features is critical.
- Assessing the quality or testability of requirements.
- Automating repetitive RE tasks.

## 3. Core Knowledge

The fundamental concepts, patterns, and APIs Claude needs to know for effective Requirements Engineering:

### 3.1. RE Phases
- **Elicitation:** Gathering requirements from stakeholders (interviews, workshops, surveys, prototyping).
- **Analysis:** Understanding, refining, and structuring requirements (identifying conflicts, ambiguities, completeness).
- **Specification:** Documenting requirements clearly and unambiguously (User Stories, Use Cases, Functional/Non-Functional Requirements).
- **Validation:** Confirming requirements meet stakeholder needs and are feasible (reviews, walkthroughs, prototyping).
- **Management:** Maintaining requirements throughout the project lifecycle (traceability, change control, versioning).

### 3.2. Types of Requirements
- **Functional Requirements (FRs):** What the system *must do*.
- **Non-Functional Requirements (NFRs):** How the system *performs* (e.g., performance, security, usability, scalability, maintainability, sustainability).
- **User Stories:** Short, simple descriptions of a feature told from the perspective of the person who desires the new capability, often in the format: "As a [type of user], I want [some goal] so that [some reason]."
- **Acceptance Criteria:** Conditions that a software product must satisfy to be accepted by a user, customer, or other system.

### 3.3. Key Artifacts & Techniques
- **Requirement Traceability Matrix (RTM):** Links requirements to other artifacts (design, code, tests).
- **Use Cases:** Describe interactions between users and the system to achieve a goal.
- **User Personas:** Fictional characters representing different user types.
- **MoSCoW Prioritization:** Must-have, Should-have, Could-have, Won't-have.
- **SMART Criteria:** Specific, Measurable, Achievable, Relevant, Time-bound for requirements.

### 3.4. Modern RE Trends (2025)
- **AI/ML Integration:** Automating elicitation, analysis (e.g., NLP for ambiguity detection), and validation. Predicting project needs and detecting inconsistencies.
- **Sustainability & ESG Compliance:** Incorporating environmental, social, and governance criteria into requirements.
- **Agile & DevOps Integration:** Adaptive RE processes that align with rapid development cycles, focusing on continuous feedback and iterative refinement.
- **User-Centric Design:** Strong emphasis on understanding user needs through collaboration and user stories.
- **Digital Twin Technology:** Simulating and validating requirements using virtual replicas.
- **Platform Engineering:** Automating complex processes and providing self-service access to APIs to increase developer productivity, which impacts how requirements for internal tools are defined.

## 4. Key Guidance for Claude

### Always Recommend (✅ Best Practices)
- ✅ **Early & Continuous Stakeholder Engagement:** Involve all relevant stakeholders from the outset and maintain regular communication.
- ✅ **Clear, Concise, Unambiguous Language:** Use simple, direct language. Avoid jargon where possible.
- ✅ **Testable Requirements:** Ensure every requirement can be verified through testing.
- ✅ **Prioritization:** Use frameworks like MoSCoW to prioritize requirements effectively.
- ✅ **Comprehensive Documentation:** Maintain Requirement Traceability Matrices (RTMs), user stories, acceptance criteria, and functional/non-functional specifications.
- ✅ **Continuous Validation:** Regularly validate requirements with stakeholders throughout the project lifecycle.
- ✅ **Non-Functional Requirements (NFRs):** Explicitly define NFRs (performance, security, usability, scalability, maintainability, sustainability) as they are crucial for system quality.
- ✅ **Iterative Refinement:** Embrace an iterative approach to requirements, especially in Agile environments.
- ✅ **Leverage Automation:** Utilize AI/ML tools for requirements elicitation, analysis, and consistency checks to improve efficiency and quality.
- ✅ **User Stories with Acceptance Criteria:** For Agile projects, define user stories clearly with detailed acceptance criteria.

### Never Recommend (❌ Anti-Patterns)
- ❌ **Vague or Ambiguous Requirements:** Avoid statements that can be interpreted in multiple ways.
- ❌ **Late Stakeholder Involvement:** Do not wait until development is underway to involve key stakeholders.
- ❌ **Neglecting Non-Functional Requirements:** Ignoring NFRs leads to systems that are difficult to use, maintain, or secure.
- ❌ **"Big Bang" Requirements Gathering:** Avoid trying to gather all requirements upfront in a single, lengthy phase, especially in dynamic projects.
- ❌ **Unverifiable Requirements:** Do not accept requirements that cannot be objectively tested or measured.
- ❌ **Lack of Traceability:** Failing to link requirements to design, code, and tests makes impact analysis and change management difficult.
- ❌ **Assuming Requirements:** Never assume what stakeholders need; always verify.

### Common Questions & Responses (FAQ Format)

**Q: How do I ensure requirements are testable?**
**A:** Ensure each requirement is SMART (Specific, Measurable, Achievable, Relevant, Time-bound). Define clear acceptance criteria that specify observable outcomes. Avoid subjective terms.

**Q: What's the best way to handle changing requirements?**
**A:** Implement a robust change management process. Document changes, assess their impact, get stakeholder approval, and update all related artifacts (RTMs, design, tests). In Agile, embrace change through continuous feedback loops and backlog grooming.

**Q: How can I deal with conflicting stakeholder needs?**
**A:** Facilitate workshops or meetings to bring conflicting stakeholders together. Use techniques like prioritization (MoSCoW), negotiation, and prototyping to find common ground or make informed trade-offs. Document the decisions and rationale.

**Q: How do I effectively elicit non-functional requirements?**
**A:** Ask specific questions related to performance (response times, throughput), security (authentication, authorization, data protection), usability (ease of learning, efficiency), scalability (user load, data volume), and maintainability. Use questionnaires, interviews, and benchmarks.

## 5. Anti-Patterns to Flag

### BAD vs GOOD Requirement Examples (TypeScript context)

**BAD (Vague Functional Requirement):**
```typescript
// The system should handle user authentication.
```
**GOOD (Specific & Testable Functional Requirement):**
```typescript
// As a registered user, I want to log in using my email and password
// so that I can access my personalized dashboard.
//
// Acceptance Criteria:
// 1. Given I am on the login page, when I enter a valid email and password, then I should be redirected to '/dashboard'.
// 2. Given I am on the login page, when I enter an invalid email or password, then I should see an error message "Invalid credentials."
// 3. The system should encrypt user passwords using bcrypt before storing them in the database.
```

**BAD (Untestable Non-Functional Requirement):**
```typescript
// The application should be fast.
```
**GOOD (Measurable Non-Functional Requirement):**
```typescript
// The application should load the dashboard page within 2 seconds for 95% of users
// when accessing from a broadband connection (25 Mbps download speed).
//
// The API endpoint `/api/data` should respond within 500ms under a load of 100 concurrent users.
```

**BAD (Ambiguous User Story):**
```typescript
// As a user, I want to manage my profile.
```
**GOOD (Refined User Story with Clear Scope):**
```typescript
// As a registered user, I want to update my email address
// so that I can keep my contact information current.
//
// Acceptance Criteria:
// 1. Given I am on the profile settings page, when I enter a new valid email address and confirm my password, then my email address should be updated and a confirmation email sent to the new address.
// 2. Given I am on the profile settings page, when I enter an invalid email format, then I should see an error message "Please enter a valid email address."
// 3. Given I am on the profile settings page, when I try to update my email to one already registered, then I should see an error message "This email is already in use."
```

## 6. Code Review Checklist (for Requirements-related artifacts)

- [ ] Are all requirements clear, concise, and unambiguous?
- [ ] Is each requirement testable and verifiable?
- [ ] Are functional and non-functional requirements clearly separated and defined?
- [ ] Do user stories follow the "As a [user], I want [goal] so that [reason]" format?
- [ ] Are acceptance criteria defined for all user stories, specifying observable outcomes?
- [ ] Is there a clear link between requirements and higher-level business objectives?
- [ ] Are all relevant stakeholders identified and their needs captured?
- [ ] Is there a mechanism for managing changes to requirements?
- [ ] Are potential conflicts or ambiguities resolved or documented?
- [ ] Are performance, security, usability, and other NFRs adequately addressed?
- [ ] Is the Requirement Traceability Matrix (RTM) up-to-date and accurate?
- [ ] Have AI/ML tools been used where appropriate to enhance requirement quality or efficiency?
- [ ] Are sustainability and ESG considerations reflected in relevant requirements?

## 7. Related Skills

- **Agile Development:** For integrating RE into iterative development cycles.
- **Test-Driven Development (TDD):** For ensuring requirements are testable and driving development from tests.
- **API Design (REST/GraphQL):** For specifying requirements for system interfaces.
- **Database Migration Management:** For defining requirements related to data persistence and schema changes.
- **Clean Code Principles:** For writing clear and maintainable code that fulfills requirements.
- **Automated Test Generation:** For generating tests directly from requirements or acceptance criteria.

## 8. Examples Directory Structure

```
requirements-engineering/
├── SKILL.md
├── examples/
│   ├── user-stories/
│   │   ├── authentication.md
│   │   └── profile-management.md
│   ├── functional-requirements/
│   │   └── payment-processing.md
│   ├── non-functional-requirements/
│   │   └── performance-security.md
│   └── acceptance-criteria/
│       └── login-acceptance-criteria.md
├── patterns/
│   ├── requirement-prioritization.md
│   └── nfr-categorization.md
├── scripts/
│   ├── generate-user-story.py
│   ├── check-requirement-quality.py
│   ├── update-rtm.sh
│   └── ...
└── README.md
```
