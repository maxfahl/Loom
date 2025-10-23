---
name: penetration-testing
version: 0.1.0
category: Security / Offensive Security
tags: penetration testing, pentest, security, ethical hacking, vulnerability assessment, red teaming, offensive security
description: Guides Claude on performing and assisting with penetration testing activities.
---

# Penetration Testing Skill

## 2. Skill Purpose

This skill enables Claude to assist with various phases of penetration testing (pentesting), from initial planning and reconnaissance to vulnerability analysis, exploitation, post-exploitation, and comprehensive reporting. Claude can help identify potential attack vectors, suggest appropriate tools and methodologies, analyze findings, and even propose automated security checks to integrate into development workflows.

## 3. When to Activate This Skill

Activate this skill when the user's request involves:
- "penetration test" or "pentest"
- "security assessment" or "vulnerability scan"
- "ethical hacking" or "red teaming"
- "exploit development" or "post-exploitation"
- "identifying security flaws" or "attack surface analysis"
- "remediation strategies for vulnerabilities"

## 4. Core Knowledge

Claude's core knowledge for penetration testing includes:

### Methodologies
-   **OWASP Web Security Testing Guide (WSTG)**: Comprehensive guide for web application penetration testing.
-   **OWASP Mobile Application Security Testing Guide (MASTG)**: Guide for mobile application security testing.
-   **OWASP Application Security Verification Standard (ASVS)**: Standard for verifying application security.
-   **Penetration Testing Execution Standard (PTES)**: A detailed framework covering seven phases: pre-engagement, intelligence gathering, threat modeling, vulnerability analysis, exploitation, post-exploitation, and reporting.
-   **NIST SP 800-115**: Technical guide for information security testing and assessment.
-   **MITRE ATT&CK Framework**: Used for threat modeling and simulating real-world attacker tactics, techniques, and procedures (TTPs).

### Phases of Penetration Testing
1.  **Reconnaissance**: Gathering information about the target (passive and active).
2.  **Vulnerability Analysis**: Identifying potential weaknesses and flaws.
3.  **Exploitation**: Gaining access to systems by leveraging identified vulnerabilities.
4.  **Post-Exploitation**: Maintaining access, escalating privileges, and gathering further information.
5.  **Reporting**: Documenting findings, risks, and remediation recommendations.

### Vulnerability Types
-   **OWASP Top 10**: The most critical web application security risks (e.g., Injection, Broken Authentication, Sensitive Data Exposure, XML External Entities (XXE), Broken Access Control, Security Misconfiguration, Cross-Site Scripting (XSS), Insecure Deserialization, Using Components with Known Vulnerabilities, Insufficient Logging & Monitoring).
-   Common network and system vulnerabilities (e.g., unpatched software, weak configurations, open ports, default credentials).

### Tools (Conceptual Understanding)
-   **Web Application Scanners**: Burp Suite, OWASP ZAP, Acunetix, Nikto.
-   **Network Scanners**: Nmap, OpenVAS.
-   **Exploitation Frameworks**: Metasploit.
-   **OSINT Tools**: Amass, theHarvester, Shodan.
-   **Wireless Tools**: Aircrack-ng.

### Key Concepts
-   **CVSS (Common Vulnerability Scoring System)**: Standard for assessing the severity of vulnerabilities.
-   **Risk Scoring**: Prioritizing vulnerabilities based on likelihood and impact.
-   **Threat Modeling**: Structured approach to identify potential threats and vulnerabilities.
-   **Attack Surface**: The sum of all points where an unauthorized user can try to enter or extract data from an environment.
-   **Rules of Engagement (RoE)**: Defines the scope, limits, and procedures for a penetration test.

## 5. Key Guidance for Claude

### Always Recommend (✅ Best Practices)
-   ✅ **Define Clear Scope and RoE**: Always start by clarifying the scope, objectives, and rules of engagement with the user. Emphasize the importance of explicit authorization.
-   ✅ **Prioritize Continuous Testing**: Advocate for integrating security testing into CI/CD pipelines and adopting a DevSecOps approach for continuous vulnerability management.
-   ✅ **Hybrid Approach**: Suggest combining automated tools for broad coverage with manual testing for deeper, more complex vulnerability discovery (e.g., business logic flaws).
-   ✅ **Actionable, Risk-Prioritized Findings**: Ensure all findings are clearly documented, include CVSS scores or similar risk ratings, and provide concrete, actionable remediation steps.
-   ✅ **Utilize Cyber Threat Intelligence (CTI)**: Advise on incorporating CTI to understand current threats and adapt testing methodologies to simulate relevant attacker TTPs.
-   ✅ **Follow Established Methodologies**: Guide the user to adhere to recognized frameworks like OWASP WSTG or PTES for structured and comprehensive assessments.
-   ✅ **Emphasize Communication**: Stress the importance of clear and continuous communication with stakeholders throughout the pentest lifecycle.
-   ✅ **Document Everything**: Maintain thorough documentation of all steps, findings, and evidence.

### Never Recommend (❌ Anti-Patterns)
-   ❌ **Testing Without Authorization**: Never proceed with any testing activity without explicit, written permission from the asset owner.
-   ❌ **Ignoring Legal/Ethical Boundaries**: Do not suggest or perform actions that violate laws, ethical guidelines, or the agreed-upon rules of engagement.
-   ❌ **Sole Reliance on Automated Tools**: Avoid presenting automated scan results as a complete penetration test. Automated tools are a starting point, not a replacement for human expertise.
-   ❌ **Vague or Unactionable Reports**: Do not provide reports that lack specific details, evidence, risk ratings, or clear remediation advice.
-   ❌ **Disrupting Production Systems**: Unless explicitly agreed upon in the RoE, avoid actions that could lead to service disruption, data loss, or system instability in production environments.
-   ❌ **Sharing Sensitive Information**: Never expose or share sensitive findings or client information without proper authorization and secure channels.

### Common Questions & Responses (FAQ Format)

-   **Q: What's the first step in a penetration test?**
    -   **A:** The absolute first step is to define the scope, objectives, and rules of engagement with the client/stakeholders, ensuring explicit authorization. Following that, reconnaissance (information gathering) begins.
-   **Q: How do I prioritize the vulnerabilities found?**
    -   **A:** Prioritize vulnerabilities based on their CVSS score, potential business impact, and exploitability. High-impact, easily exploitable vulnerabilities should be addressed first.
-   **Q: What tools should I use for web application penetration testing?**
    -   **A:** For web applications, essential tools include Burp Suite (for proxying, scanning, and manual testing), OWASP ZAP (an open-source alternative), and specialized scanners like Acunetix for automated vulnerability detection.
-   **Q: Can automated scanners replace manual penetration testing?**
    -   **A:** No. Automated scanners are excellent for identifying known vulnerabilities at scale and providing a baseline. However, they often miss complex business logic flaws, chained exploits, and subtle security issues that require human intelligence and creativity. A hybrid approach is best.
-   **Q: How do I ensure my findings are actionable?**
    -   **A:** For each finding, include a clear description, steps to reproduce, evidence (screenshots, logs), the impact of the vulnerability, and specific, detailed remediation recommendations. Assign a risk rating (e.g., CVSS).

## 6. Anti-Patterns to Flag

### Anti-Pattern: Uncontrolled Network Scanning
-   **BAD Example (Conceptual)**:
    ```typescript
    // User asks: "Scan the entire corporate network for open ports."
    // Claude's internal thought: "I should just run Nmap on the whole subnet."
    // This is bad because it lacks scope, authorization, and could disrupt services.
    ```
-   **GOOD Example (Conceptual)**:
    ```typescript
    // User asks: "Scan the staging web server (192.168.1.100) for common web ports (80, 443, 8080)."
    // Claude's internal thought: "This is a clearly defined scope and target. I can use Nmap with specific port flags."
    // This adheres to defined scope and minimizes risk.
    ```

### Anti-Pattern: Superficial Vulnerability Assessment
-   **BAD Example (Conceptual)**:
    ```typescript
    // User asks: "Perform a quick security check on our new API."
    // Claude's internal thought: "I'll just run an automated API scanner and report its findings."
    // This is bad because it misses business logic flaws, authentication bypasses, and other complex issues.
    ```
-   **GOOD Example (Conceptual)**:
    ```typescript
    // User asks: "Perform a quick security check on our new API."
    // Claude's internal thought: "I will run an automated API scanner for initial findings, then manually review authentication flows, authorization checks, input validation, and potential business logic bypasses."
    // This combines automation with human-like critical thinking.
    ```

## 7. Code Review Checklist

When reviewing code for security vulnerabilities, consider the following:

-   [ ] **Input Validation & Sanitization**: Are all user inputs (from web forms, APIs, file uploads, etc.) properly validated and sanitized to prevent injection attacks (SQLi, XSS, Command Injection)?
-   [ ] **Authentication & Session Management**: Is authentication robust (strong passwords, multi-factor authentication)? Are session tokens securely generated, stored, and invalidated?
-   [ ] **Authorization & Access Control**: Are access controls correctly implemented at all layers (function, object, record)? Is the principle of least privilege followed?
-   [ ] **Sensitive Data Handling**: Is sensitive data encrypted at rest and in transit? Are secrets (API keys, credentials) stored securely and not hardcoded?
-   [ ] **Error Handling & Logging**: Do error messages avoid leaking sensitive information? Is sufficient logging in place for security monitoring and incident response?
-   [ ] **Security Misconfiguration**: Are default configurations hardened? Are unnecessary services disabled? Are security headers properly set?
-   [ ] **Dependency Management**: Are all third-party libraries and frameworks up-to-date and free from known vulnerabilities?
-   [ ] **API Security**: Are API endpoints protected against common attacks (e.g., rate limiting, proper authentication, input schema validation)?
-   [ ] **Server-Side Request Forgery (SSRF)**: Are external requests from the server properly validated to prevent SSRF?
-   [ ] **Cross-Site Request Forgery (CSRF)**: Are CSRF tokens implemented for state-changing requests?

## 8. Related Skills

-   **Web Development**: For understanding web application architecture and common vulnerabilities.
-   **Cloud Security**: For assessing cloud-native applications and infrastructure.
-   **Network Security**: For understanding network protocols, firewalls, and network-based attacks.
-   **API Design**: For evaluating API security and identifying vulnerabilities in API implementations.
-   **DevSecOps**: For integrating security practices into the development pipeline.

## 9. Examples Directory Structure

The `examples/` directory within this skill package should contain practical code snippets and configurations demonstrating various penetration testing concepts.

-   `examples/web-app/`
    -   `xss-payload.ts`: Example TypeScript code demonstrating a reflected XSS payload.
    -   `sql-injection-example.ts`: TypeScript snippet showing a vulnerable SQL query and a parameterized query fix.
    -   `csrf-poc.html`: A simple HTML proof-of-concept for CSRF.
-   `examples/network/`
    -   `nmap-scan-script.sh`: A basic shell script for targeted Nmap scans.
    -   `port-banner-grab.sh`: Shell script to grab banners from open ports.
-   `examples/cloud/`
    -   `aws-s3-misconfig.ts`: Conceptual TypeScript code illustrating how to identify a misconfigured public S3 bucket.
-   `examples/exploit-templates/`
    -   `basic-buffer-overflow.c`: A simple C example of a vulnerable program and a basic exploit.
    -   `reverse-shell.py`: A Python script for a basic reverse shell.
