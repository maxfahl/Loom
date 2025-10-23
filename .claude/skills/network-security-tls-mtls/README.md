# Network Security (TLS/mTLS) Skill

This skill provides comprehensive guidance and tools for implementing and managing secure network communications using Transport Layer Security (TLS) and mutual TLS (mTLS). It focuses on establishing robust security postures for client-server and service-to-service interactions, adhering to modern best practices and mitigating common vulnerabilities.

## What this Skill Covers

*   **TLS/mTLS Fundamentals**: Understanding the handshake process, certificates, CAs, and the distinction between one-way (TLS) and mutual (mTLS) authentication.
*   **Certificate Lifecycle Management**: Best practices for automated issuance, renewal, and revocation of certificates using public and private CAs.
*   **Zero Trust Architectures**: How mTLS is a cornerstone for securing microservices in zero-trust environments.
*   **Modern TLS Standards**: Guidance on adopting TLS 1.3 and strong cipher suites.
*   **Key Technologies**: Leveraging tools like OpenSSL, Certbot, and service meshes (Istio, Linkerd) for TLS/mTLS implementation.
*   **Common Pitfalls**: Identifying and avoiding issues like certificate expiry, weak configurations, and validation errors.
*   **Automation Scripts**: A set of utility scripts to assist with certificate management and TLS configuration auditing.

## Getting Started

To leverage this skill, refer to the `SKILL.md` for detailed knowledge and guidance. Explore the `examples/` directory for practical configurations and utilize the `scripts/` for automating various TLS/mTLS tasks.

## Directory Structure

*   `SKILL.md`: The main instruction file for Claude, detailing core knowledge, best practices, and anti-patterns.
*   `examples/`: Contains example configurations and scripts demonstrating various TLS/mTLS patterns.
*   `patterns/`: (Currently empty, but reserved for future common TLS/mTLS patterns or reusable components).
*   `scripts/`: Automation scripts to assist with TLS/mTLS development and maintenance.
*   `README.md`: This human-readable overview of the skill.

## Automation Scripts

The `scripts/` directory contains the following utilities:

*   `cert_expiry_notifier.py`: A Python script to scan certificates for expiry and send notifications.
*   `generate_cert.sh`: A Bash script to generate private keys, CSRs, and self-signed certificates using OpenSSL.
*   `tls_auditor.py`: A Python script to audit the TLS configuration of an HTTPS endpoint.

## Contribution

Contributions are welcome! If you have additional best practices, examples, or automation scripts related to Network Security (TLS/mTLS), please consider contributing to this skill.
