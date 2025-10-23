---
Name: threat-modeling
Version: 1.0.0
Category: Security / Application Security
Tags: threat modeling, security, application security, DevSecOps, STRIDE, PASTA, DREAD, AI, automation, shift left
Description: Proactively identifies and addresses security vulnerabilities in systems and applications.
---

# Threat Modeling Skill

## 1. Skill Purpose

This skill enables Claude to understand, perform, and guide users through the process of threat modeling. Threat modeling is a structured approach to identifying potential threats, vulnerabilities, and countermeasures within a system or application. By integrating threat modeling early and continuously into the Software Development Lifecycle (SDLC), this skill helps "shift left" security, ensuring that security is a fundamental aspect of design and development, rather than an afterthought. It aims to reduce the cost and effort of fixing security issues by identifying them proactively.

## 2. When to Activate This Skill

Activate this skill when:
*   A new system or application is being designed.
*   A new feature is being added to an existing system.
*   Significant architectural changes are planned.
*   Before major deployments or releases.
*   During incident response to understand attack vectors.
*   Keywords or phrases like "security review," "vulnerability assessment," "design review," "threat analysis," "risk assessment," or "secure design" are used.

## 3. Core Knowledge

### Methodologies
*   **STRIDE:** (Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege) - A common model for classifying threats.
*   **DREAD:** (Damage, Reproducibility, Exploitability, Affected users, Discoverability) - Used for risk assessment, often in conjunction with STRIDE.
*   **PASTA:** (Process for Attack Simulation and Threat Analysis) - A seven-step, risk-centric methodology.
*   **LINDDUN:** (Linkability, Identifiability, Non-repudiation, Detectability, Disclosure of information, Unawareness, Non-compliance) - Focuses on privacy threats.
*   **OWASP Threat Modeling Methodology v2.0 (2025):** Standardized guidance for analyzing AI system exposure and mapping infrastructure-as-code.
*   **STRIDE-AI:** Enhanced STRIDE for comprehensive AI threat modeling.
*   **MAESTRO (Multi-Agentic System Threat Model):** A 7-layer reference architecture for threat modeling AI agents.

### Concepts
*   **Attack Surface:** The sum of the different points where an unauthorized user can try to enter data to or extract data from an environment.
*   **Trust Boundaries:** Lines in a system diagram where the level of trust changes.
*   **Data Flow Diagrams (DFDs):** Visual representations of how data moves through a system, crucial for identifying trust boundaries and interaction points.
*   **Assets:** What needs to be protected (e.g., data, services, reputation).
*   **Threats:** Potential harmful events that could exploit vulnerabilities.
*   **Vulnerabilities:** Weaknesses in a system that can be exploited by threats.
*   **Countermeasures:** Actions or controls to mitigate identified threats.
*   **Risk Assessment:** Evaluating the likelihood and impact of identified threats.

### Principles
*   **Shift Left:** Integrating security activities earlier in the SDLC.
*   **Security by Design:** Building security into the system from the ground up.
*   **Continuous Threat Modeling:** Regularly reviewing and updating threat models throughout the system's lifecycle.

### Tools (Conceptual)
*   **Threat Modeling Platforms:** Commercial tools like IriusRisk, ThreatModeler, Aristiun's Aribot for automated threat model generation and management.
*   **Threat-as-Code:** Defining threat models in machine-readable formats (e.g., YAML) for version control and automation.

## 4. Key Guidance for Claude

### Always Recommend (✅ Best Practices)
*   **Start Early:** Begin threat modeling during the design phase, before any code is written.
*   **Involve Stakeholders:** Include developers, architects, product owners, and security experts.
*   **Use Data Flow Diagrams (DFDs):** DFDs are fundamental for visualizing data movement, trust boundaries, and interaction points.
*   **Prioritize Based on Business Impact:** Focus on threats that pose the highest risk to business objectives and critical assets.
*   **Iterate and Refine:** Threat modeling is not a one-time event; it should be an ongoing, iterative process.
*   **Integrate with CI/CD:** Automate threat model validation and updates within the continuous integration/continuous delivery pipeline.
*   **Document Thoroughly:** Maintain clear and concise documentation of identified threats, risks, and countermeasures.
*   **Consider AI/ML Specific Threats:** For AI-driven systems, use methodologies like STRIDE-AI or MAESTRO.

### Never Recommend (❌ Anti-Patterns)
*   **One-Time Activity:** Treating threat modeling as a checkbox exercise performed only once.
*   **Solely Relying on Tools:** Tools are aids, not replacements for critical thinking and human expertise.
*   **Ignoring Business Context:** Threat modeling without understanding the business impact of potential threats.
*   **Skipping Documentation:** Failing to document the threat model makes it difficult to track, review, and update.
*   **Generic Threats:** Applying a generic list of threats without tailoring them to the specific system context.
*   **Late-Stage Threat Modeling:** Attempting to threat model a system just before deployment, leading to costly rework.

### Common Questions & Responses (FAQ Format)

*   **Q: When is the best time to perform threat modeling?**
    *   **A:** The ideal time is during the design phase of a new system or feature, and then continuously throughout its lifecycle, especially before major changes or deployments.
*   **Q: Which threat modeling methodology should I use?**
    *   **A:** It depends on your context. STRIDE is excellent for identifying general threats. PASTA is more risk-centric. LINDDUN focuses on privacy. For AI systems, consider STRIDE-AI or MAESTRO.
*   **Q: How can I integrate threat modeling into my DevSecOps pipeline?**
    *   **A:** Automate the generation of DFDs, use "Threat-as-Code" to define and version control threat models, and implement CI/CD checks to validate security controls derived from the threat model.
*   **Q: What are the most important outputs of a threat model?**
    *   **A:** Identified threats, their associated risks, proposed countermeasures, and a clear understanding of the system's attack surface and trust boundaries.
*   **Q: How do I ensure my threat model stays relevant?**
    *   **A:** Make it a living document. Regularly review and update it as the system evolves, new threats emerge, or new components are introduced.

## 5. Anti-Patterns to Flag

### Example: Insecure Data Handling (Information Disclosure)

**BAD (Anti-Pattern):**
```typescript
// user-service.ts
import { Request, Response } from 'express';
import { User } from './types';

// ... (assume user data is fetched from a database)

app.get('/users/:id', (req: Request, res: Response) => {
  const userId = req.params.id;
  const user: User = getUserFromDB(userId); // Fetches user including sensitive fields

  // Directly sending the entire user object without filtering
  res.status(200).json(user);
});

// types.ts
interface User {
  id: string;
  username: string;
  email: string;
  passwordHash: string; // Sensitive
  creditCardInfo: string; // Sensitive
  isAdmin: boolean;
}
```
**Why it's BAD:** This code directly exposes sensitive user information (passwordHash, creditCardInfo) through the API, violating the principle of least privilege and leading to an Information Disclosure threat (STRIDE). A threat model would identify the data flow from the database to the API response crossing a trust boundary and flag the exposure of sensitive attributes.

**GOOD (Recommended Pattern):**
```typescript
// user-service.ts
import { Request, Response } from 'express';
import { User, PublicUser } from './types';

// ... (assume user data is fetched from a database)

app.get('/users/:id', (req: Request, res: Response) => {
  const userId = req.params.id;
  const user: User = getUserFromDB(userId);

  if (!user) {
    return res.status(404).json({ message: 'User not found' });
  }

  // Filter out sensitive information before sending the response
  const publicUser: PublicUser = {
    id: user.id,
    username: user.username,
    email: user.email,
    isAdmin: user.isAdmin,
  };

  res.status(200).json(publicUser);
});

// types.ts
interface User {
  id: string;
  username: string;
  email: string;
  passwordHash: string;
  creditCardInfo: string;
  isAdmin: boolean;
}

interface PublicUser {
  id: string;
  username: string;
  email: string;
  isAdmin: boolean;
}
```
**Why it's GOOD:** By creating a `PublicUser` interface and explicitly mapping only non-sensitive fields, the system prevents accidental exposure of sensitive data. This countermeasure directly addresses the Information Disclosure threat identified during threat modeling.

## 6. Code Review Checklist

*   [ ] **Data Flow & Trust Boundaries:** Are all data flows and trust boundaries clearly defined and understood?
*   [ ] **Input Validation:** Is all external input (user input, API parameters, file uploads) rigorously validated?
*   [ ] **Authentication & Authorization:** Are authentication mechanisms robust, and is authorization implemented correctly (least privilege)?
*   [ ] **Sensitive Data Handling:** Is sensitive data encrypted at rest and in transit? Is access to it strictly controlled?
*   [ ] **Error Handling:** Do error messages avoid leaking sensitive system information? Are errors logged securely?
*   [ ] **Logging & Monitoring:** Are security-relevant events logged, and is there adequate monitoring for suspicious activities?
*   [ ] **Third-Party Components:** Are all third-party libraries and dependencies up-to-date and free from known vulnerabilities?
*   [ ] **Configuration Management:** Is security-related configuration managed securely and consistently?
*   [ ] **Session Management:** Are session tokens generated securely, protected against hijacking, and properly invalidated?
*   [ ] **Denial of Service (DoS) Protection:** Are there mechanisms in place to prevent or mitigate DoS attacks (e.g., rate limiting)?

## 7. Related Skills

*   `DevSecOps`
*   `API Security Best Practices`
*   `Cloud Deployment & Security`
*   `Secure Coding Principles`
*   `Containerization & Orchestration Security`
*   `Network Security (TLS/mTLS)`

## 8. Examples Directory Structure

*   `examples/dfd-example.json`: A JSON representation of a simple Data Flow Diagram.
*   `examples/threat-model-template.yaml`: A YAML template for a basic threat model document.
*   `examples/secure-design-pattern.ts`: TypeScript example demonstrating a secure design pattern (e.g., input validation, output encoding).

## 9. Custom Scripts Section

This section outlines automation scripts designed to streamline and enhance the threat modeling process. These scripts aim to reduce manual effort, improve consistency, and integrate threat modeling more deeply into the development workflow.

### Script Ideas:

1.  **`generate-threat-model-template.py`**: Generates a basic threat model document (Markdown or YAML) from project metadata.
2.  **`dfd-to-stride-threats.py`**: Analyzes a simplified Data Flow Diagram (DFD) in JSON/YAML format and suggests potential STRIDE threats.
3.  **`ci-threat-model-check.sh`**: A shell script for CI/CD pipelines to ensure a threat model exists and meets basic compliance checks for a given component.
4.  **`vulnerability-report-generator.py`**: Takes a list of identified vulnerabilities (e.g., from a CSV or JSON) and generates a formatted report.
