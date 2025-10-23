---
name: owasp-top-10
version: 2021.0.1
category: Security / Web Application
tags: security, web, owasp, vulnerabilities, prevention, secure-coding, application-security
description: The top 10 most critical web application security risks and their mitigations.
---

## Skill Purpose

This skill enables Claude to identify, understand, and provide guidance on mitigating the OWASP Top 10 2021 web application security risks. It covers the nature of each vulnerability, common attack vectors, and practical prevention strategies, including secure coding practices and configuration best practices.

## When to Activate This Skill

Activate this skill when discussing:
- Web application security assessments or audits.
- Secure software development lifecycle (SSDLC).
- Code reviews focusing on security.
- Threat modeling and risk analysis for web applications.
- Training developers on common security vulnerabilities.
- Designing or implementing security controls for web applications.

## Core Knowledge

### OWASP Top 10 2021

#### A01:2021-Broken Access Control
*   **Summary:** Access control policies are not properly enforced, allowing users to act outside of their intended permissions (e.g., accessing unauthorized data, functionality, or escalating privileges).
*   **Impact:** Unauthorized data exposure, modification, or destruction; privilege escalation.
*   **Prevention:**
    *   Implement access control mechanisms consistently throughout the application.
    *   Deny access by default; grant access based on the principle of least privilege.
    *   Enforce record ownership in access control models.
    *   Use role-based access control (RBAC) or attribute-based access control (ABAC).
    *   Avoid exposing sensitive object references (e.g., user IDs in URLs) via Insecure Direct Object References (IDOR).
    *   Rate limit API and controller access.

#### A02:2021-Cryptographic Failures
*   **Summary:** Improper or absent encryption of sensitive data at rest or in transit, leading to sensitive data exposure.
*   **Impact:** Data breaches, compliance violations, loss of trust.
*   **Prevention:**
    *   Use strong, up-to-date encryption algorithms (e.g., AES-256) and protocols (e.g., TLS 1.2+).
    *   Employ secure cryptographic libraries; avoid custom implementations.
    *   For password storage, use strong, salted, adaptive hashing functions (e.g., bcrypt, Argon2, PBKDF2).
    *   Implement proper key management, including secure storage and rotation.
    *   Do not store sensitive data unnecessarily.

#### A03:2021-Injection
*   **Summary:** Untrusted data is sent to an interpreter as part of a command or query, tricking the interpreter into executing unintended commands or accessing unauthorized data. Includes SQL, NoSQL, OS command, LDAP, and Cross-Site Scripting (XSS) injection.
*   **Impact:** Data theft, data corruption, remote code execution, denial of service.
*   **Prevention:**
    *   **Parameterized Queries/Prepared Statements:** Use these for all database interactions.
    *   **Input Validation:** Implement strict server-side input validation (whitelist approach).
    *   **Encoding:** Apply context-sensitive output encoding to prevent XSS.
    *   **Least Privilege:** Run processes with the lowest possible privileges.
    *   **Safe APIs:** Use APIs that avoid the use of an interpreter entirely.

#### A04:2021-Insecure Design
*   **Summary:** Flaws in the design or architecture of an application that lead to security vulnerabilities, rather than implementation bugs. This emphasizes the need for security to be integrated early in the SDLC.
*   **Impact:** Systemic vulnerabilities that are hard to fix later, leading to various security risks.
*   **Prevention:**
    *   Integrate security into all stages of the SDLC, starting with design.
    *   Conduct threat modeling for critical components and features.
    *   Establish and use a library of secure design patterns, components, and frameworks.
    *   Implement security controls based on a well-defined security architecture.
    *   Perform security reviews of design documents.

#### A05:2021-Security Misconfiguration
*   **Summary:** Insecure default configurations, incomplete or ad hoc configurations, open cloud storage, misconfigured HTTP headers, verbose error messages, and unpatched systems.
*   **Impact:** Unauthorized access, information disclosure, system compromise.
*   **Prevention:**
    *   Implement a repeatable hardening process for all environments.
    *   Remove or disable unused features, services, and default accounts.
    *   Ensure error messages are generic and do not reveal sensitive information.
    *   Configure strong HTTP security headers (e.g., CSP, HSTS, X-Content-Type-Options).
    *   Regularly patch and update all software components (OS, web server, database, frameworks).
    *   Use Infrastructure as Code (IaC) to define and manage secure configurations.

#### A06:2021-Vulnerable and Outdated Components
*   **Summary:** Using libraries, frameworks, and other software components with known security flaws, or components that are outdated and unmaintained.
*   **Impact:** Exploitation of known vulnerabilities, leading to various attacks (e.g., remote code execution, data breaches).
*   **Prevention:**
    *   Maintain an inventory of all client-side and server-side components and their versions.
    *   Regularly scan for vulnerabilities in dependencies using automated tools (e.g., `npm audit`, Snyk, Dependabot, Trivy).
    *   Subscribe to security advisories for all used components.
    *   Update components to their latest secure versions promptly.
    *   Remove unused dependencies.

#### A07:2021-Identification and Authentication Failures
*   **Summary:** Weaknesses in user identification, authentication, and session management functions, allowing attackers to compromise user accounts or assume identities.
*   **Impact:** Account takeover, identity theft, unauthorized access.
*   **Prevention:**
    *   Implement strong, multi-factor authentication (MFA).
    *   Enforce strong password policies (length, complexity, uniqueness).
    *   Implement secure session management (e.g., secure, HTTP-only, short-lived session tokens).
    *   Rate limit failed login attempts to prevent brute-force attacks.
    *   Avoid exposing session IDs in URLs.
    *   Secure credential recovery processes.

#### A08:2021-Software and Data Integrity Failures
*   **Summary:** Making assumptions about software updates, critical data, and CI/CD pipelines without verifying their integrity. This includes issues like insecure deserialization.
*   **Impact:** Supply chain attacks, unauthorized data manipulation, remote code execution.
*   **Prevention:**
    *   Verify the integrity of software updates, critical data, and CI/CD artifacts using digital signatures or checksums.
    *   Ensure secure deserialization practices; avoid deserializing untrusted data.
    *   Implement strong access controls for CI/CD pipelines and code repositories.
    *   Scan code and dependencies for integrity issues.

#### A09:2021-Security Logging and Monitoring Failures
*   **Summary:** Insufficient logging and monitoring, or ineffective incident response, allowing attackers to persist and expand their reach undetected.
*   **Impact:** Delayed detection of breaches, increased damage, difficulty in forensic analysis.
*   **Prevention:**
    *   Implement comprehensive logging of all security-relevant events (e.g., failed logins, access control failures, data modifications).
    *   Ensure logs are immutable, protected from tampering, and stored securely.
    *   Establish effective monitoring and alerting for suspicious activities.
    *   Develop and test an incident response plan.
    *   Centralize log management and analysis.

#### A10:2021-Server-Side Request Forgery (SSRF)
*   **Summary:** An application fetches a remote resource without validating the user-supplied URL, allowing an attacker to manipulate the application into sending requests to an unintended location (e.g., internal systems, cloud metadata services).
*   **Impact:** Access to internal services, sensitive data exposure, port scanning of internal networks.
*   **Prevention:**
    *   Validate all user-supplied input for URLs using a whitelist approach.
    *   Sanitize and encode user input before using it in requests.
    *   Disable HTTP redirections.
    *   Use network segmentation and firewall rules to restrict outbound connections from application servers.
    *   Do not send raw responses from remote servers to clients.

## Key Guidance for Claude

### Always Recommend (✅ Best Practices)

*   ✅ **Security by Design:** Integrate security considerations from the very beginning of the software development lifecycle.
*   ✅ **Input Validation:** Always validate all untrusted input on the server-side using a whitelist approach.
*   ✅ **Output Encoding:** Always encode output based on the context (HTML, JavaScript, URL, CSS) to prevent XSS.
*   ✅ **Least Privilege:** Grant only the necessary permissions to users, processes, and services.
*   ✅ **Secure Defaults:** Configure all systems and applications with security-hardened defaults.
*   ✅ **Patch Management:** Keep all software (OS, libraries, frameworks, applications) up-to-date with the latest security patches.
*   ✅ **Strong Authentication:** Implement multi-factor authentication and strong password policies.
*   ✅ **Comprehensive Logging & Monitoring:** Log all security-relevant events and monitor them for suspicious activity.
*   ✅ **Automated Security Testing:** Integrate SAST, DAST, and SCA tools into CI/CD pipelines.
*   ✅ **Threat Modeling:** Conduct regular threat modeling for critical application components.

### Never Recommend (❌ Anti-Patterns)

*   ❌ **Trusting User Input:** Never trust any input received from the client-side; always validate on the server-side.
*   ❌ **Concatenating User Input Directly into Queries:** This is a primary cause of injection vulnerabilities.
*   ❌ **Storing Sensitive Data in Plaintext:** Passwords, API keys, and other sensitive data must always be encrypted or hashed securely.
*   ❌ **Using Outdated/Vulnerable Libraries:** Avoid using components with known security flaws or those that are no longer maintained.
*   ❌ **Ignoring Security Warnings/Alerts:** Treat security alerts seriously and investigate them promptly.
*   ❌ **Default Configurations in Production:** Never deploy systems with default passwords or insecure default settings to production.
*   ❌ **Rolling Your Own Cryptography:** Always use well-vetted, standard cryptographic libraries and algorithms.
*   ❌ **Verbose Error Messages:** Do not expose stack traces, database errors, or other sensitive system information in error messages to users.

### Common Questions & Responses (FAQ Format)

*   **Q: How can I prevent SQL Injection?**
    *   **A:** Use parameterized queries or prepared statements for all database interactions. Avoid dynamic SQL query construction by concatenating user input. Implement strict input validation.
*   **Q: What's the best way to handle user passwords?**
    *   **A:** Never store passwords in plaintext. Hash them using a strong, salted, adaptive hashing function like bcrypt, Argon2, or PBKDF2. Do not roll your own hashing algorithm. Implement strong password policies and multi-factor authentication.
*   **Q: How do I protect against Cross-Site Scripting (XSS)?**
    *   **A:** Implement context-sensitive output encoding for all untrusted data before rendering it in HTML, JavaScript, CSS, or URL contexts. Use a robust templating engine that automatically escapes output. Implement a Content Security Policy (CSP).
*   **Q: My application uses many third-party libraries. How do I manage their security?**
    *   **A:** Maintain an up-to-date inventory of all dependencies. Use Software Composition Analysis (SCA) tools (e.g., `npm audit`, Snyk, Dependabot) to scan for known vulnerabilities. Regularly update dependencies to their latest secure versions.
*   **Q: What should I log for security purposes?**
    *   **A:** Log all failed authentication attempts, successful logins, access control failures, data modifications, administrative actions, and any suspicious application behavior. Ensure logs include timestamps, user IDs, and relevant context. Protect logs from tampering.

## Anti-Patterns to Flag

### ❌ Bad: SQL Injection Vulnerability (Node.js/TypeScript)

```typescript
// BAD: Directly concatenating user input into SQL query
import { Request, Response } from 'express';
import { Pool } from 'pg'; // Assuming PostgreSQL

const pool = new Pool();

export const getUserById = async (req: Request, res: Response) => {
  const userId = req.params.id;
  // Vulnerable to SQL Injection
  const query = `SELECT * FROM users WHERE id = ${userId}`;
  try {
    const result = await pool.query(query);
    res.json(result.rows);
  } catch (error) {
    console.error('Database error:', error);
    res.status(500).send('Server error');
  }
};
```
**Why it's bad:** An attacker can inject malicious SQL (e.g., `1 OR 1=1`) to bypass authentication or retrieve unauthorized data.

### ✅ Good: SQL Injection Prevention (Node.js/TypeScript)

```typescript
// GOOD: Using parameterized queries (prepared statements)
import { Request, Response } from 'express';
import { Pool } from 'pg';

const pool = new Pool();

export const getUserById = async (req: Request, res: Response) => {
  const userId = req.params.id;
  // Secure: Using parameterized query
  const query = 'SELECT * FROM users WHERE id = $1';
  try {
    const result = await pool.query(query, [userId]);
    res.json(result.rows);
  } catch (error) {
    console.error('Database error:', error);
    res.status(500).send('Server error');
  }
};
```
**Why it's good:** The database driver separates the query structure from the user-supplied data, preventing malicious input from being interpreted as SQL commands.

### ❌ Bad: Cross-Site Scripting (XSS) Vulnerability (React/TypeScript)

```typescript
// BAD: Directly rendering user-supplied HTML
import React from 'react';

interface Props {
  userInput: string;
}

const DisplayContent: React.FC<Props> = ({ userInput }) => {
  // Vulnerable to XSS if userInput contains <script> tags or malicious HTML
  return (
    <div dangerouslySetInnerHTML={{ __html: userInput }} />
  );
};

export default DisplayContent;
```
**Why it's bad:** If `userInput` contains `<script>alert('XSS')</script>`, the script will execute in the user's browser, potentially stealing cookies or defacing the page.

### ✅ Good: Cross-Site Scripting (XSS) Prevention (React/TypeScript)

```typescript
// GOOD: Rendering user-supplied text safely (React automatically escapes)
import React from 'react';

interface Props {
  userInput: string;
}

const DisplayContent: React.FC<Props> = ({ userInput }) => {
  // Secure: React automatically escapes string children, preventing XSS
  return (
    <div>{userInput}</div>
  );
};

export default DisplayContent;
```
**Why it's good:** React automatically escapes string content rendered within JSX, converting characters like `<` to `&lt;`, thus preventing them from being interpreted as HTML tags.

## Code Review Checklist

When reviewing code for OWASP Top 10 vulnerabilities, verify the following:

*   **Input Validation:** Is all untrusted input (from users, APIs, files) validated on the server-side using a whitelist approach?
*   **Output Encoding:** Is all untrusted data properly encoded before being rendered in HTML, JavaScript, CSS, or URL contexts?
*   **Database Interactions:** Are parameterized queries or prepared statements used for all database operations? Is ORM configured securely?
*   **Authentication & Session Management:** Are strong, adaptive hashing algorithms used for passwords? Is MFA implemented? Are session tokens secure (HTTP-only, secure flags, short-lived)? Is rate limiting applied to login attempts?
*   **Access Control:** Is access denied by default? Are authorization checks performed on every request to sensitive resources/functions? Are IDORs prevented?
*   **Error Handling:** Are error messages generic and free of sensitive information (stack traces, system details)?
*   **Dependency Management:** Are all third-party libraries and frameworks up-to-date and free of known vulnerabilities? Are SCA tools integrated?
*   **Security Configuration:** Are all application and server configurations hardened? Are unnecessary features/services disabled? Are security headers configured?
*   **Logging & Monitoring:** Are security-relevant events logged? Are logs protected and monitored for suspicious activity?
*   **Sensitive Data Handling:** Is sensitive data encrypted at rest and in transit? Is proper key management in place? Is sensitive data stored only when necessary?
*   **SSRF Prevention:** Are user-supplied URLs validated and sanitized before fetching remote resources?

## Related Skills

*   `secure-coding-practices`: General principles for writing secure code.
*   `api-security`: Specific security considerations for API design and implementation.
*   `authentication-authorization`: Deep dive into identity management and access control.
*   `dependency-management`: Best practices for managing project dependencies securely.

## Examples Directory Structure

```
examples/
├── injection/
│   ├── sql-injection-bad.ts
│   └── sql-injection-good.ts
├── xss/
│   ├── xss-bad-react.tsx
│   └── xss-good-react.tsx
├── access-control/
│   ├── idor-bad.ts
│   └── idor-good.ts
└── scripts/
    ├── dependency-vulnerability-check.sh
    ├── input-sanitizer-generator.py
    └── security-header-check.sh
```

## Custom Scripts Section ⭐ NEW

Here are 3-5 automation scripts that would save significant time for developers working with OWASP Top 10 security.

### 1. `dependency-vulnerability-check.sh`

**Purpose:** Automates the scanning of project dependencies for known vulnerabilities using common package managers (`npm`, `pip`). This helps address A06:2021-Vulnerable and Outdated Components by providing a quick way to identify and report security issues in third-party libraries.

**Pain Point:** Manually checking each dependency for vulnerabilities is tedious and error-prone. Developers often forget to run these checks regularly.

**Usage Example:**
```bash
./scripts/dependency-vulnerability-check.sh --path ./my-nodejs-app
./scripts/dependency-vulnerability-check.sh --path ./my-python-app --package-manager pip
```

### 2. `input-sanitizer-generator.py`

**Purpose:** Generates boilerplate TypeScript code for basic input sanitization and validation functions. This helps developers quickly implement secure handling of common input types, mitigating risks like A03:2021-Injection and A07:2021-Cross-Site Scripting (XSS).

**Pain Point:** Writing robust input validation and sanitization logic from scratch for every input field is repetitive and can lead to inconsistencies or missed edge cases.

**Usage Example:**
```bash
python scripts/input-sanitizer-generator.py --type email --output-file src/utils/validation.ts
python scripts/input-sanitizer-generator.py --type string --max-length 255
```

### 3. `security-header-check.sh`

**Purpose:** Checks a given URL for the presence and correct configuration of common HTTP security headers (e.g., `Content-Security-Policy`, `Strict-Transport-Security`, `X-Content-Type-Options`). This helps identify and remediate A05:2021-Security Misconfiguration related to web server and application headers.

**Pain Point:** Manually inspecting HTTP response headers for security best practices is time-consuming and can be overlooked. Misconfigured headers can leave applications vulnerable.

**Usage Example:**
```bash
./scripts/security-header-check.sh --url https://www.example.com
./scripts/security-header-check.sh --url http://localhost:3000 --verbose
```
