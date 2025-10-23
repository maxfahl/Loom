# Basic Threat Model Template

This template provides a basic structure for conducting a threat model for a software component or system. It follows a simplified STRIDE-like approach.

## 1. System Description

- **Name of System/Component:** [e.g., User Authentication Service, Payment Gateway]
- **Scope:** [Clearly define the boundaries of the system being analyzed. What's in, what's out?]
- **Key Functionality:** [Summarize what the system does.]
- **Architecture Overview:** [Briefly describe the main components, data flows, and trust boundaries. A simple diagram can be helpful.]
- **Data Handled:** [What types of data does this system process, store, or transmit? (e.g., PII, financial data, sensitive business data)]

## 2. Identify Assets

List the valuable assets that need protection within this system.

- **Asset 1:** [e.g., User Credentials Database]
  - **Value:** [High/Medium/Low] (e.g., Critical for business, legal compliance)
- **Asset 2:** [e.g., API Keys]
  - **Value:** [High/Medium/Low]
- **Asset 3:** [e.g., Customer PII]
  - **Value:** [High/Medium/Low]

## 3. Decompose the Application

Break down the system into its constituent parts (data flows, data stores, processes, external interactors).

- **Data Flows:**
  - [e.g., User Login Request (Browser -> Auth Service)]
  - [e.g., Payment Processing (Order Service -> Payment Gateway)]
- **Data Stores:**
  - [e.g., User Database (PostgreSQL)]
  - [e.g., Session Cache (Redis)]
- **Processes:**
  - [e.g., `login_handler()` function]
  - [e.g., `process_payment()` microservice]
- **External Interactors:**
  - [e.g., End User]
  - [e.g., Third-Party Payment Provider]

## 4. Identify Threats (using STRIDE)

For each identified component (data flow, data store, process, external interactor), consider potential threats using the STRIDE model.

- **S**poofing Identity: Impersonating something or someone else.
- **T**ampering with Data: Modifying data.
- **R**epudiation: Claiming not to have performed an action.
- **I**nformation Disclosure: Exposing information to unauthorized individuals.
- **D**enial of Service: Preventing legitimate users from accessing resources.
- **E**levation of Privilege: Gaining capabilities without proper authorization.

| Component | Threat Type | Threat Description | Potential Impact | Mitigation Strategy | Owner | Status |
|---|---|---|---|---|---|---|
| User Login Flow | Spoofing | Attacker impersonates a legitimate user. | Unauthorized access, data breach. | Multi-factor authentication, strong password policies. | @auth-team | Open |
| User Database | Information Disclosure | Sensitive user data exposed. | Data breach, regulatory fines. | Encryption at rest, access controls, least privilege. | @db-admin | Open |
| Payment Gateway API | Tampering | Attacker modifies payment request. | Financial loss, fraud. | API request signing, input validation. | @payment-team | Open |

## 5. Identify Vulnerabilities

Based on the identified threats, what specific weaknesses in the system could allow these threats to materialize?

- **Vulnerability 1:** [e.g., Lack of input validation on user registration form.]
  - **Related Threat:** Tampering, Information Disclosure.
  - **Mitigation:** Implement strict server-side input validation.
- **Vulnerability 2:** [e.g., Weak password hashing algorithm (e.g., MD5).] 
  - **Related Threat:** Spoofing, Information Disclosure.
  - **Mitigation:** Upgrade to a strong, modern hashing algorithm (e.g., bcrypt, Argon2).

## 6. Determine Mitigation Strategies

For each identified threat and vulnerability, propose and prioritize mitigation strategies.

- **Mitigation 1:** [e.g., Implement MFA for all user roles.]
  - **Threats Addressed:** Spoofing.
  - **Priority:** High.
  - **Owner:** @auth-team.
  - **Status:** To Do.
- **Mitigation 2:** [e.g., Encrypt all sensitive data at rest in the database.]
  - **Threats Addressed:** Information Disclosure.
  - **Priority:** High.
  - **Owner:** @db-admin.
  - **Status:** In Progress.

## 7. Validation and Review

- **Reviewers:** [List of individuals who reviewed the threat model.]
- **Date of Review:** [YYYY-MM-DD]
- **Next Review Date:** [YYYY-MM-DD]
- **Changes/Updates:** [Any significant changes or updates made during the review.]

---