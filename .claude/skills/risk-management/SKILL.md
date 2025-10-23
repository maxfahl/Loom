---
name: risk-management
version: 0.1.0
category: Project Management / Security
tags: risk, mitigation, security, project, agile, devsecops, compliance, threat modeling
description: Guides Claude in identifying, assessing, and mitigating project and technical risks in software development.
---

# Risk Management Skill

## 1. Skill Purpose

This skill enables Claude to effectively identify, assess, prioritize, and mitigate various types of risks (technical, project, security, compliance) throughout the software development lifecycle. It promotes a proactive, integrated, and continuous approach to risk management, aligning with modern Agile and DevSecOps methodologies.

## 2. When to Activate This Skill

Activate this skill when:
- Planning a new project or feature.
- During sprint planning, daily stand-ups, or retrospectives.
- Encountering unexpected issues, bugs, or security vulnerabilities.
- Evaluating third-party dependencies or open-source components.
- Responding to changes in regulatory requirements or project scope.
- Performing code reviews or architectural assessments.
- When asked to "identify risks," "mitigate threats," "assess vulnerabilities," or "ensure compliance."

## 3. Core Knowledge

The fundamental concepts, patterns, and APIs Claude needs to know for effective risk management:

- **Risk Identification Techniques:** Brainstorming, checklists, interviews, SWOT analysis, Delphi technique, root cause analysis, threat modeling (STRIDE, DREAD).
- **Risk Assessment:**
    - **Qualitative:** Probability (Likelihood) x Impact (Severity) matrix.
    - **Quantitative:** Expected Monetary Value (EMV), Decision Tree Analysis.
- **Risk Categories:** Technical (e.g., scalability, performance, complexity, technical debt), Project (e.g., scope creep, resource availability, schedule delays, budget overruns), Security (e.g., vulnerabilities, data breaches, unauthorized access), Compliance (e.g., GDPR, HIPAA, industry standards), Operational (e.g., infrastructure failure, deployment issues), External (e.g., market changes, supplier issues).
- **Risk Response Strategies (4 T's):**
    - **Terminate (Avoid):** Eliminate the risk by changing plans.
    - **Treat (Mitigate):** Reduce the probability or impact of the risk.
    - **Transfer (Share):** Shift the risk to a third party (e.g., insurance, outsourcing).
    - **Tolerate (Accept):** Acknowledge the risk and its potential impact, and plan for contingencies.
- **Continuous Risk Monitoring:** Regular review of identified risks, tracking mitigation efforts, identifying new risks.
- **Agile Risk Integration:** Embedding risk discussions into sprint planning, stand-ups, and retrospectives. Prioritizing risks in the backlog.
- **DevSecOps Principles:** Shifting security "left," automating security checks in CI/CD, collaboration between Dev, Sec, and Ops.
- **Threat Modeling:** Structured approach to identify potential threats and vulnerabilities in a system design.
- **Software Composition Analysis (SCA) & SBOM:** Managing risks from open-source components, understanding software supply chain.
- **Regulatory Compliance:** Awareness of relevant industry regulations and standards (e.g., DORA, EU AI Act, SEC rules).
- **AI/ML in Risk Management:** Understanding how AI can assist in predictive analytics for risk identification and anomaly detection.

## 4. Key Guidance for Claude

### Always Recommend (✅ best practices)

- ✅ **Proactive Identification:** Encourage early and continuous risk identification throughout the SDLC.
- ✅ **Integrated Approach:** Advocate for integrating risk discussions into existing Agile ceremonies and DevSecOps pipelines.
- ✅ **Prioritization:** Emphasize prioritizing risks based on their likelihood and impact, focusing on high-priority items first.
- ✅ **Clear Ownership:** Ensure every identified risk has a clear owner responsible for its monitoring and mitigation.
- ✅ **Documentation:** Maintain a clear, concise risk register or backlog item for each risk, including its description, impact, likelihood, owner, and mitigation plan.
- ✅ **Automate Security:** Recommend automating security checks (SAST, DAST, SCA) within CI/CD pipelines.
- ✅ **Threat Modeling:** Suggest conducting threat modeling sessions for new features or critical system components.
- ✅ **Contingency Planning:** For accepted risks, always recommend developing contingency plans.
- ✅ **Regular Review:** Advise on regular review and re-assessment of risks, especially during project milestones or significant changes.
- ✅ **Security-First Culture:** Promote a mindset where security is a shared responsibility and a primary consideration.

### Never Recommend (❌ anti-patterns)

- ❌ **Ignoring Risks:** Never ignore identified risks, regardless of perceived low impact or likelihood.
- ❌ **One-Time Assessment:** Avoid treating risk management as a one-time activity; it must be continuous.
- ❌ **Blame Culture:** Do not foster a blame culture; focus on identifying and solving problems collaboratively.
- ❌ **Over-Engineering Mitigation:** Avoid disproportionate mitigation efforts for low-impact, low-likelihood risks.
- ❌ **Lack of Ownership:** Never leave a risk unassigned or without a clear owner.
- ❌ **Manual Security Checks:** Discourage reliance solely on manual security checks; automate where possible.
- ❌ **Undocumented Risks:** Do not allow risks to be discussed and forgotten without proper documentation.

### Common Questions & Responses (FAQ format)

**Q: How do I start identifying risks for a new project?**
A: Begin with a brainstorming session involving key stakeholders. Use a checklist of common project and technical risks. Consider conducting an initial threat modeling session for critical components.

**Q: What's the best way to prioritize risks?**
A: Use a qualitative risk matrix (Likelihood vs. Impact). Assign scores (e.g., 1-5) for each, then multiply to get a risk score. Focus on risks with the highest scores.

**Q: How often should we review our risks?**
A: Regularly. For Agile teams, integrate into sprint reviews and retrospectives. For longer projects, review at major milestones and whenever significant changes occur.

**Q: A new security vulnerability was found in a third-party library. What should I do?**
A: Immediately assess its impact and likelihood. Check if a patch is available. If so, prioritize applying it. If not, explore temporary mitigations (e.g., disabling affected features, WAF rules) and track the vendor's progress on a fix. Update your SBOM.

**Q: How can we make risk management less burdensome for the team?**
A: Integrate it seamlessly into existing workflows (Agile ceremonies, CI/CD). Automate what can be automated. Focus on high-impact risks. Foster a culture of shared responsibility rather than a separate "risk team."

## 5. Anti-Patterns to Flag

**Anti-Pattern 1: Ignoring Technical Debt as a Risk**

**BAD:**
```typescript
// src/legacy-module.ts
// This module is complex and hard to maintain, but it works for now.
function calculateLegacyFeature(data: any): any {
  // ... hundreds of lines of spaghetti code ...
  if (data.type === 'special') {
    // ... more complex logic with side effects ...
  }
  return result;
}
```
*Flag:* This code represents significant technical debt, which is an unacknowledged technical risk. It increases the likelihood of bugs, slows down future development, and makes security patches harder to implement.

**GOOD:**
```typescript
// src/legacy-module.ts
/**
 * @deprecated This module is a known source of technical debt.
 * @risk TechnicalDebt: High complexity, high maintenance cost, potential for critical bugs.
 * @mitigation-plan Refactor into smaller, testable units; consider a phased rewrite.
 * @owner @devteamlead
 * @due Q3 2025
 */
function calculateLegacyFeature(data: any): any {
  // ... existing code ...
}

// docs/risk-register.md (or a dedicated risk management tool)
// Entry: Technical Debt in Legacy Feature Module
// Description: The `calculateLegacyFeature` function is overly complex, lacks proper testing, and is a bottleneck for new development.
// Impact: High (Increased bug rate, slow feature delivery, high onboarding cost for new developers)
// Likelihood: Medium (Already experiencing symptoms)
// Owner: @devteamlead
// Mitigation Plan:
// 1. Q2 2025: Conduct a detailed architectural review and break down into smaller refactoring tasks.
// 2. Q3 2025: Begin phased refactoring, prioritizing critical paths and high-risk areas.
// 3. Continuous: Add comprehensive unit and integration tests during refactoring.
// Status: Active - Mitigation in Progress
```

**Anti-Pattern 2: Neglecting Supply Chain Security**

**BAD:**
```json
// package.json
{
  "dependencies": {
    "lodash": "^4.17.21",
    "left-pad": "^1.3.0" // A very old, potentially unmaintained package
  }
}
```
*Flag:* Using outdated or unmaintained third-party libraries introduces significant supply chain security risks. These packages might contain known vulnerabilities that are not being patched, or they could be hijacked.

**GOOD:**
```json
// package.json
{
  "dependencies": {
    "lodash": "^4.17.21",
    "modern-utility-library": "^2.0.0" // Actively maintained, regularly scanned
  }
}
```
*Guidance:* Regularly audit dependencies using SCA tools. Maintain an up-to-date Software Bill of Materials (SBOM). Prioritize updating or replacing vulnerable dependencies.

## 6. Code Review Checklist

- [ ] **Risk Register Updated:** Are any new risks identified during the review added to the risk register/backlog?
- [ ] **Mitigation Implemented:** If the code is a risk mitigation, is it correctly implemented and tested?
- [ ] **Security Best Practices:** Does the code adhere to security best practices (e.g., input validation, secure coding guidelines, least privilege)?
- [ ] **Dependency Scan:** Have new or updated dependencies been scanned for known vulnerabilities (SCA)?
- [ ] **Error Handling:** Is robust error handling in place to prevent system failures and provide informative messages (reducing operational risk)?
- [ ] **Performance Impact:** Does the change introduce any performance bottlenecks or scalability risks?
- [ ] **Compliance:** Does the change comply with relevant regulatory requirements (e.g., data privacy)?
- [ ] **Test Coverage:** Are there sufficient tests (unit, integration, security) to cover the changes and mitigate regression risks?
- [ ] **Observability:** Are appropriate logging, monitoring, and alerting mechanisms in place for new features to detect operational risks early?

## 7. Related Skills

- **security-auditing:** For deep dives into security vulnerabilities and penetration testing.
- **devsecops-pipeline:** For integrating security and risk checks into CI/CD.
- **agile-methodologies:** For embedding risk management into Agile workflows.
- **incident-response:** For handling and recovering from security incidents or major operational failures.
- **compliance-management:** For specific guidance on regulatory adherence.

## 8. Examples Directory Structure

```
risk-management/
├── examples/
│   ├── threat-model-template.md      # Template for conducting a basic threat model
│   ├── risk-register-entry.md        # Example of a well-documented risk register entry
│   └── security-checklist.md         # Basic security checklist for new features
├── patterns/
│   ├── risk-matrix.md                # Markdown representation of a Likelihood x Impact matrix
│   └── mitigation-strategies.md      # Overview of common mitigation strategies
├── scripts/
│   ├── scan-dependencies.sh          # Shell script to run SCA tool
│   ├── generate-sbom.py              # Python script to generate a basic SBOM
│   ├── risk-report-generator.py      # Python script to generate a summary risk report
│   ├── ci-cd-security-check.sh       # Shell script for basic security checks in CI/CD
│   └── vulnerability-tracker.py      # Python script to track and prioritize vulnerabilities
└── README.md
```

## 9. Custom Scripts Section

For the Risk Management skill, the following 3-5 automation scripts would save significant time and address common pain points:

1.  **`scan-dependencies.sh`**: Automates running a Software Composition Analysis (SCA) tool (e.g., `npm audit`, `pip-audit`, `owasp-dependency-check`) to identify known vulnerabilities in project dependencies.
2.  **`generate-sbom.py`**: Generates a basic Software Bill of Materials (SBOM) for a project, listing all direct and transitive dependencies, their versions, and licenses. This is crucial for supply chain risk management and compliance.
3.  **`risk-report-generator.py`**: Parses a structured risk register (e.g., a Markdown file or CSV) and generates a summary report, highlighting high-priority risks, their owners, and mitigation statuses.
4.  **`ci-cd-security-check.sh`**: A shell script to integrate basic security checks (e.g., linting with security rules, basic SAST scan, secret detection) into a CI/CD pipeline.
5.  **`vulnerability-tracker.py`**: A Python script that can ingest vulnerability reports (e.g., from SCA tools) and help prioritize them based on CVSS score, exploitability, and business impact, potentially integrating with a project management tool.

I will now create the directory structure and then proceed to write the source code for each of these scripts.
