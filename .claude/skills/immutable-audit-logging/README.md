# Immutable Audit Logging Skill

This skill provides guidance and tools for implementing robust, tamper-proof audit logging in applications. It covers best practices for ensuring data integrity, compliance, and security through immutable audit trails.

## Contents

*   `SKILL.md`: The main instruction file detailing the skill's purpose, core knowledge, guidance, anti-patterns, and code review checklist.
*   `examples/`: Contains TypeScript code examples demonstrating how to implement immutable audit logging.
*   `scripts/`: Automation scripts to assist with setup, verification, and testing of audit logging.
*   `patterns/`: Common patterns related to immutable audit logging.

## Getting Started

Refer to `SKILL.md` for a comprehensive understanding of immutable audit logging and how to apply it in your projects.

## Automation Scripts

The `scripts/` directory contains several utility scripts to streamline your workflow:

*   `generate-audit-event-type.py`: Generates TypeScript interfaces for audit events.
*   `verify-audit-chain-integrity.sh`: Verifies the cryptographic integrity of audit log chains.
*   `setup-s3-object-lock.sh`: Automates AWS S3 Object Lock setup for WORM compliance.
*   `redaction-tester.py`: Tests sensitive data redaction rules.

For detailed usage of each script, refer to their respective help documentation (`--help` flag).
