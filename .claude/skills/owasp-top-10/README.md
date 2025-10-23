# OWASP Top 10 Skill

This skill provides Claude with in-depth knowledge and practical tools for understanding and mitigating the OWASP Top 10 2021 web application security risks.

It covers detailed explanations of each vulnerability, common attack vectors, prevention strategies, and code examples demonstrating both vulnerable and secure implementations. Automation scripts are included to assist developers in identifying and addressing these critical security concerns.

## Contents

- `SKILL.md`: The main instruction file for Claude, detailing core knowledge, guidance, anti-patterns, and a code review checklist for each OWASP Top 10 item.
- `examples/`: Directory containing code examples (TypeScript) illustrating vulnerable and secure coding practices for various OWASP Top 10 categories.
- `patterns/`: Directory for common secure coding patterns (currently empty, can be expanded).
- `scripts/`: Automation scripts to assist with security tasks.
  - `dependency-vulnerability-check.sh`: Script to scan project dependencies for known vulnerabilities.
  - `input-sanitizer-generator.py`: Python script to generate boilerplate TypeScript code for input sanitization and validation.
  - `security-header-check.sh`: Script to check a web application's HTTP security headers.

## Usage

Refer to `SKILL.md` for comprehensive guidance on identifying and mitigating OWASP Top 10 vulnerabilities. The `scripts/` directory contains executable tools to automate common security checks and code generation tasks.
