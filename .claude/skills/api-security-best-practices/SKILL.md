---
name: api-security-best-practices
version: 1.0.0
category: Security / API
tags: API, Security, Best Practices, OWASP, Authentication, Authorization, Data Protection, Threat Modeling, Zero Trust, Shift Left, AI Security
description: Essential guidelines and practices for securing APIs against common vulnerabilities and emerging threats, incorporating 2025 insights.
---

# API Security Best Practices

## Skill Purpose

This skill enables Claude to guide developers in designing, implementing, and maintaining secure APIs. It covers fundamental security principles, common attack vectors, and advanced strategies to protect APIs against evolving threats, with a focus on current best practices for 2025. By leveraging this skill, Claude can help ensure that APIs are robust, resilient, and compliant with modern security standards, minimizing the risk of data breaches and service disruptions.

## When to Activate This Skill

Activate this skill when the user's query involves:

*   Designing new APIs with security in mind.
*   Reviewing existing API implementations for security vulnerabilities.
*   Implementing authentication and authorization mechanisms for APIs.
*   Protecting sensitive data exposed via APIs.
*   Understanding and mitigating common API security threats (e.g., OWASP API Security Top 10).
*   Integrating security into the API development lifecycle (DevSecOps, Shift-Left).
*   Questions about API gateways, rate limiting, input validation, or secure error handling.
*   Discussions around Zero-Trust architecture for APIs.
*   Considerations for AI agents as API consumers.

Keywords: "API security review", "secure API design", "vulnerability assessment API", "authentication for API", "authorization for API", "data protection API", "OWASP API Top 10", "API gateway security", "rate limiting API", "input validation API", "secure API development", "DevSecOps API", "Zero Trust API".

## Core Knowledge

The fundamental concepts, patterns, and APIs Claude needs to know for API Security Best Practices:

1.  **OWASP API Security Top 10 (Latest Version)**: Deep understanding of the most critical API security risks, including:
    *   API1:2023 Broken Object Level Authorization (BOLA)
    *   API2:2023 Broken Authentication
    *   API3:2023 Broken Object Property Level Authorization
    *   API4:2023 Unrestricted Resource Consumption
    *   API5:2023 Broken Function Level Authorization
    *   API6:2023 Unrestricted Access to Sensitive Business Flows
    *   API7:2023 Server Side Request Forgery (SSRF)
    *   API8:2023 Security Misconfiguration
    *   API9:2023 Improper Inventory Management
    *   API10:2023 Unsafe Consumption of APIs
2.  **Authentication Mechanisms**:
    *   **OAuth 2.0 & OpenID Connect (OIDC)**: Flows (Authorization Code, Client Credentials, Implicit, Hybrid), scopes, claims, token types (Access, Refresh, ID).
    *   **JSON Web Tokens (JWTs)**: Structure (Header, Payload, Signature), signing algorithms (HS256, RS256), common vulnerabilities (e.g., `alg: none`, weak secrets, lack of expiration).
    *   **API Keys**: Limitations, secure handling (transport, storage, rotation).
    *   **Mutual TLS (mTLS)**: Client certificate authentication for service-to-service communication.
    *   **Passwordless Authentication**: WebAuthn, FIDO2.
3.  **Authorization Models**:
    *   **Role-Based Access Control (RBAC)**: Roles, permissions, role assignment.
    *   **Attribute-Based Access Control (ABAC)**: Policies based on user, resource, and environment attributes.
    *   **Granular Permissions**: Fine-grained control over resources and actions.
    *   **Policy Enforcement Points (PEP) & Policy Decision Points (PDP)**.
4.  **Data Validation and Sanitization**:
    *   **Input Validation**: Schema validation (JSON Schema, OpenAPI Schema), type checking, length constraints, format validation (regex).
    *   **Output Encoding**: Preventing XSS by encoding output based on context (HTML, URL, JavaScript).
    *   **Sanitization**: Removing or neutralizing malicious input.
5.  **Rate Limiting and Throttling**:
    *   Strategies (fixed window, sliding window, leaky bucket, token bucket).
    *   Implementation (IP-based, user-based, API key-based).
    *   Protection against DoS/DDoS, brute-force attacks.
6.  **Encryption**:
    *   **HTTPS/TLS**: Enforcing secure communication in transit, certificate management.
    *   **Encryption at Rest**: Encrypting sensitive data in databases and storage.
7.  **API Gateway Security Features**:
    *   Authentication/Authorization enforcement.
    *   Rate limiting.
    *   Traffic filtering and routing.
    *   Threat protection (WAF integration).
    *   Caching.
    *   Logging and monitoring.
8.  **Logging and Monitoring**:
    *   Comprehensive logging of API requests, responses, and security events.
    *   Real-time anomaly detection.
    *   Alerting mechanisms.
    *   Centralized logging solutions.
9.  **Threat Modeling**:
    *   STRIDE (Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege).
    *   DREAD (Damage, Reproducibility, Exploitability, Affected users, Discoverability).
    *   Integrating threat modeling into the design phase.
10. **Shift-Left Security**:
    *   Integrating security practices early in the SDLC.
    *   Automated security testing (SAST, DAST, IAST, SCA).
    *   Security as Code.
11. **Zero-Trust Architecture**:
    *   "Never trust, always verify."
    *   Micro-segmentation, least privilege access.
    *   Continuous authentication and authorization.
12. **AI and Machine Learning in API Security**:
    *   Behavioral analytics for anomaly detection.
    *   Automated threat intelligence.
    *   Predictive security.
13. **API Inventory and Governance**:
    *   Maintaining an up-to-date catalog of all APIs (internal, external, partner).
    *   Detecting and managing Shadow and Zombie APIs.
    *   API versioning strategies.
14. **Secure Secrets Management**:
    *   Using environment variables, secret vaults (e.g., HashiCorp Vault, AWS Secrets Manager, Azure Key Vault).
    *   Automated secret rotation.
    *   Never hardcoding secrets.
15. **Secure Error Handling**:
    *   Generic error messages for external consumers.
    *   Detailed logging for internal debugging.
    *   Avoiding exposure of stack traces, sensitive data, or internal system details.
16. **Business Logic Abuse**:
    *   Understanding how attackers exploit legitimate API functionality.
    *   Implementing robust business logic validation.
    *   Monitoring for unusual sequences of API calls.
17. **API Supply Chain Vulnerabilities**:
    *   Securing third-party API integrations.
    *   Vetting external dependencies.

## Key Guidance for Claude

### Always Recommend (✅ Best Practices)

*   **Implement the OWASP API Security Top 10**: Prioritize addressing these critical risks in all API development.
*   **Enforce Strong Authentication**: Utilize OAuth 2.0 with OIDC, JWTs (properly validated), or mTLS for robust identity verification. Prefer passwordless authentication where feasible.
*   **Implement Granular Authorization**: Apply RBAC or ABAC to ensure users/services only access resources and perform actions they are explicitly permitted to.
*   **Validate and Sanitize All Input**: Strictly validate all incoming data against a defined schema (e.g., OpenAPI schema) and sanitize to prevent injection attacks.
*   **Implement Rate Limiting and Throttling**: Protect against brute-force attacks, DoS, and resource exhaustion by limiting the number of requests an entity can make.
*   **Encrypt All Communication**: Mandate HTTPS/TLS 1.2+ for all API traffic to protect data in transit.
*   **Utilize API Gateways**: Leverage API gateways for centralized policy enforcement, authentication, rate limiting, and traffic management.
*   **Implement Comprehensive Logging and Monitoring**: Log all API requests, responses, and security-relevant events. Use real-time monitoring and anomaly detection to identify suspicious activity.
*   **Adopt a "Shift-Left" Security Approach**: Integrate security testing (SAST, DAST, SCA) and threat modeling early and continuously throughout the SDLC.
*   **Maintain an Up-to-Date API Inventory**: Keep a complete and accurate record of all APIs, actively identifying and deprecating Shadow and Zombie APIs.
*   **Embrace Zero-Trust Principles**: Assume no implicit trust, verify every request, and enforce least privilege access.
*   **Manage Secrets Securely**: Use dedicated secret management solutions (e.g., environment variables, vaults) and avoid hardcoding credentials. Implement automated rotation.
*   **Provide Generic Error Messages**: Return non-descriptive error messages to external clients to avoid leaking sensitive system information. Log detailed errors internally.
*   **Conduct Regular Security Audits and Penetration Testing**: Proactively discover and remediate vulnerabilities before they can be exploited.

### Never Recommend (❌ Anti-Patterns)

*   **Exposing Sensitive Data in Error Messages**: Never return raw stack traces, database errors, or internal system details to API consumers.
*   **Using Weak or Default Credentials**: Avoid easily guessable passwords, default API keys, or hardcoded credentials.
*   **Hardcoding API Keys or Secrets**: Never embed sensitive credentials directly in code or configuration files.
*   **Skipping Input Validation**: Assuming client-side validation is sufficient is a critical security flaw. Always validate on the server-side.
*   **Ignoring Rate Limiting**: Leaving APIs vulnerable to brute-force, DoS, and resource exhaustion attacks.
*   **Using Unencrypted Communication (HTTP)**: Transmitting data over HTTP exposes it to eavesdropping and tampering.
*   **Trusting Client-Side Input**: Client-side controls can be bypassed; all security checks must be performed server-side.
*   **Undocumented or Shadow APIs**: These create blind spots and significant attack surfaces.
*   **Over-Permissive CORS Policies**: Wildcard origins (`*`) or allowing all methods can lead to cross-site request forgery (CSRF) and other attacks.
*   **Ignoring Security Headers**: Neglecting headers like `Content-Security-Policy`, `X-Content-Type-Options`, `Strict-Transport-Security`.
*   **Using Outdated Libraries or Dependencies**: Vulnerabilities in third-party components are a common attack vector.

### Common Questions & Responses (FAQ Format)

*   **Q: How do I secure my API against common attacks?**
    *   **A:** Start by implementing the OWASP API Security Top 10. Focus on strong authentication and granular authorization, rigorous input validation, rate limiting, and using HTTPS. Regularly audit your API for vulnerabilities.
*   **Q: What's the best authentication method for a modern API?**
    *   **A:** For user-facing APIs, OAuth 2.0 with OpenID Connect is highly recommended for its flexibility and security features. For service-to-service communication, mTLS or client credentials flow with OAuth 2.0 are strong choices. JWTs are commonly used for stateless session management but require careful validation.
*   **Q: How can I prevent injection attacks (SQLi, XSS) in my API?**
    *   **A:** Implement strict server-side input validation using schemas. For SQL, use parameterized queries or ORMs. For XSS, ensure all output rendered in HTML contexts is properly encoded. Never concatenate user input directly into queries or HTML.
*   **Q: What is Broken Object Level Authorization (BOLA) and how do I mitigate it?**
    *   **A:** BOLA (API1:2023) occurs when an API allows a user to access resources they are not authorized for by manipulating object IDs. Mitigation involves implementing robust, server-side authorization checks at every API endpoint that accesses a resource, ensuring the requesting user is explicitly permitted to access *that specific instance* of the resource.
*   **Q: How do I handle API keys securely?**
    *   **A:** API keys should be treated as sensitive credentials. Never hardcode them. Store them in environment variables or a dedicated secret management system. Transmit them over HTTPS, ideally in a custom header rather than URL parameters. Implement key rotation and revoke compromised keys immediately.
*   **Q: What role do API Gateways play in API security?**
    *   **A:** API Gateways act as a single entry point for all API requests, allowing you to centralize security policies. They can enforce authentication, authorization, rate limiting, traffic filtering, and integrate with WAFs, significantly reducing the attack surface and simplifying security management.
*   **Q: How can I detect and prevent Shadow and Zombie APIs?**
    *   **A:** Implement a comprehensive API inventory management system. Regularly scan your network for undocumented endpoints (Shadow APIs) and identify deprecated or unused APIs (Zombie APIs) that should be decommissioned. Integrate API discovery tools into your CI/CD pipeline.

## Anti-Patterns to Flag

### 1. Hardcoded Secrets

**BAD (TypeScript):**

```typescript
// src/config.ts
export const API_KEY = "sk_live_xxxxxxxxxxxxxxxxxxxx";
export const DB_PASSWORD = "mySuperSecretPassword123";

// src/service.ts
import { API_KEY } from './config';

async function fetchData() {
  const response = await fetch('https://api.example.com/data', {
    headers: { 'X-API-Key': API_KEY }
  });
  // ...
}
```

**GOOD (TypeScript):**

```typescript
// .env
API_KEY=sk_live_xxxxxxxxxxxxxxxxxxxx
DB_PASSWORD=mySuperSecretPassword123

// src/config.ts
import 'dotenv/config'; // Ensure dotenv is loaded early

export const API_KEY = process.env.API_KEY;
export const DB_PASSWORD = process.env.DB_PASSWORD;

if (!API_KEY || !DB_PASSWORD) {
  console.error("Missing critical environment variables!");
  process.exit(1);
}

// src/service.ts
import { API_KEY } from './config';

async function fetchData() {
  const response = await fetch('https://api.example.com/data', {
    headers: { 'X-API-Key': API_KEY }
  });
  // ...
}
```
*Explanation*: Hardcoding secrets directly in the codebase is a major security risk. Environment variables or dedicated secret management systems (like HashiCorp Vault, AWS Secrets Manager) should be used.

### 2. Insufficient Input Validation

**BAD (TypeScript - Express.js example):**

```typescript
// src/routes/users.ts
app.post('/users', (req, res) => {
  const { name, email, password } = req.body;
  // No validation, directly using user input
  const newUser = { name, email, passwordHash: hash(password) };
  db.saveUser(newUser);
  res.status(201).send('User created');
});
```

**GOOD (TypeScript - Express.js with Zod for validation):**

```typescript
// src/routes/users.ts
import { z } from 'zod'; // Assuming Zod for schema validation

const createUserSchema = z.object({
  name: z.string().min(3).max(50),
  email: z.string().email(),
  password: z.string().min(8).regex(/[A-Z]/, "Password must contain at least one uppercase letter")
                      .regex(/[a-z]/, "Password must contain at least one lowercase letter")
                      .regex(/[0-9]/, "Password must contain at least one number")
                      .regex(/[^a-zA-Z0-9]/, "Password must contain at least one special character"),
});

app.post('/users', (req, res) => {
  try {
    const { name, email, password } = createUserSchema.parse(req.body);
    const newUser = { name, email, passwordHash: hash(password) };
    db.saveUser(newUser);
    res.status(201).send('User created');
  } catch (error) {
    if (error instanceof z.ZodError) {
      return res.status(400).json({ message: 'Validation failed', errors: error.errors });
    }
    console.error('Error creating user:', error);
    res.status(500).send('Internal server error');
  }
});
```
*Explanation*: Lack of server-side input validation can lead to various attacks, including injection, buffer overflows, and unexpected application behavior. Always validate all incoming data against a strict schema.

### 3. Verbose Error Messages

**BAD (TypeScript - Express.js example):**

```typescript
// src/routes/data.ts
app.get('/data/:id', async (req, res) => {
  try {
    const data = await db.getData(req.params.id);
    if (!data) {
      return res.status(404).send('Data not found');
    }
    res.json(data);
  } catch (error) {
    // Exposing internal error details
    console.error('Database error:', error);
    res.status(500).json({ message: 'An internal server error occurred', error: error.message, stack: error.stack });
  }
});
```

**GOOD (TypeScript - Express.js example):**

```typescript
// src/routes/data.ts
app.get('/data/:id', async (req, res) => {
  try {
    const data = await db.getData(req.params.id);
    if (!data) {
      return res.status(404).json({ message: 'Resource not found' });
    }
    res.json(data);
  } catch (error) {
    // Log detailed error internally, return generic message externally
    console.error(`Error fetching data for ID ${req.params.id}:`, error);
    res.status(500).json({ message: 'An unexpected error occurred. Please try again later.' });
  }
});
```
*Explanation*: Verbose error messages can leak sensitive information about the server's internal structure, database schema, or dependencies, aiding attackers in reconnaissance. Always provide generic error messages to clients and log detailed errors internally.

## Code Review Checklist

*   [ ] **Authentication**: Is every endpoint protected by appropriate authentication? Is it strong (e.g., OAuth 2.0/OIDC, mTLS)? Are JWTs validated correctly (signature, expiration, audience)?
*   [ ] **Authorization**: Are granular authorization checks performed at the object/resource level for every request (preventing BOLA)? Is function-level authorization correctly implemented?
*   [ ] **Input Validation**: Is all incoming data (headers, query parameters, body, path parameters) strictly validated against a schema on the server-side? Are data types, lengths, and formats enforced?
*   [ ] **Output Sanitization/Encoding**: Is all data returned to clients properly encoded/sanitized to prevent XSS or other client-side vulnerabilities?
*   [ ] **Rate Limiting/Throttling**: Are rate limits in place for all critical endpoints to prevent brute-force attacks and resource exhaustion?
*   [ ] **HTTPS Enforcement**: Is HTTPS enforced for all API communication? Are insecure HTTP requests redirected or rejected?
*   [ ] **Secrets Management**: Are API keys, database credentials, and other sensitive secrets stored securely (e.g., environment variables, secret vaults) and never hardcoded? Is there a rotation policy?
*   [ ] **Error Handling**: Do error responses avoid leaking sensitive information (stack traces, internal details)? Are generic error messages returned to clients?
*   [ ] **Logging & Monitoring**: Are security-relevant events (failed logins, authorization failures, suspicious requests) logged comprehensively? Is there an alerting mechanism for anomalies?
*   [ ] **CORS Policy**: Is the CORS policy configured securely, avoiding overly permissive settings (e.g., `Access-Control-Allow-Origin: *`)?
*   [ ] **Dependency Security**: Are all third-party libraries and dependencies regularly scanned for known vulnerabilities and kept up-to-date?
*   [ ] **Security Headers**: Are appropriate security headers (e.g., `Content-Security-Policy`, `X-Content-Type-Options`, `Strict-Transport-Security`) configured for API responses?
*   [ ] **Business Logic Abuse**: Are there checks to prevent abuse of legitimate business logic (e.g., excessive purchases, coupon code manipulation)?
*   [ ] **API Inventory**: Is the API documented and part of a managed inventory? Are there processes to detect and decommission Shadow/Zombie APIs?

## Related Skills

*   `authentication`: For detailed guidance on various authentication protocols and implementations.
*   `authorization`: For in-depth knowledge on access control models (RBAC, ABAC) and policy enforcement.
*   `data-validation`: For comprehensive strategies and tools for validating and sanitizing data.
*   `threat-modeling`: For structured approaches to identifying and mitigating security threats early in the design phase.
*   `ci-cd-security`: For integrating security practices and automated testing into continuous integration and deployment pipelines.
*   `secure-coding-principles`: For general secure coding guidelines applicable across all development.

## Examples Directory Structure

```
api-security-best-practices/
├── examples/
│   └── typescript/
│       ├── auth-middleware.ts         # Example of JWT validation middleware
│       ├── input-validation.ts        # Example of schema-based input validation
│       ├── rate-limiter.ts            # Example of a basic rate limiting implementation
│       └── secure-error-handling.ts   # Example of generic error handling middleware
```

## Custom Scripts Section

Here are 3 automation scripts designed to address common pain points in API security development and auditing.

### 1. `api-security-audit.py` (Python)

*   **Description**: This script performs a basic security audit of an API defined by an OpenAPI (Swagger) specification. It checks for common misconfigurations such as missing authentication schemes, the use of insecure HTTP, and potential exposure of sensitive data in example responses. It helps developers "shift-left" by identifying security issues early in the design or development phase.
*   **Pain Point Addressed**: Manually reviewing large OpenAPI specifications for security best practices is tedious, time-consuming, and prone to human error. This script automates initial checks.

### 2. `detect-hardcoded-secrets.sh` (Shell)

*   **Description**: This shell script scans a specified directory (typically a codebase) for patterns that commonly indicate hardcoded secrets like API keys, passwords, and tokens. It uses `grep` with a set of predefined regular expressions to identify potential leaks, helping prevent accidental exposure of sensitive credentials.
*   **Pain Point Addressed**: Developers often accidentally commit secrets to version control, leading to severe security vulnerabilities. This script provides a quick way to detect such issues before or after a commit.

### 3. `rate-limit-tester.py` (Python)

*   **Description**: This Python script tests the effectiveness of an API endpoint's rate limiting mechanism. It sends a configurable number of requests to a target URL within a short period and analyzes the responses to determine if rate limits are being enforced as expected. This helps verify that APIs are protected against brute-force attacks and resource exhaustion.
*   **Pain Point Addressed**: Manually testing rate limiting can be difficult to simulate accurately and verify consistently. This script automates the process, providing clear feedback on rate limit enforcement.
