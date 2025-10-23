---
Name: network-security-tls-mtls
Version: 1.0.0
Category: Security / Networking
Tags: tls, mtls, network security, certificates, PKI, zero trust, service mesh, automation
Description: Guides Claude on implementing secure network communications using TLS and mTLS, focusing on best practices for certificate management, zero trust architectures, and common pitfalls.
---

## Skill Purpose
This skill enables Claude to assist developers and security professionals in designing, implementing, and managing secure network communications using Transport Layer Security (TLS) and mutual TLS (mTLS). It covers best practices for certificate lifecycle management, securing microservices in zero-trust environments, and avoiding common configuration and operational pitfalls.

## When to Activate This Skill
*   When a user asks to secure network communication between services or clients and servers.
*   When a user needs to implement mTLS for microservices or a Zero Trust architecture.
*   When a user is dealing with certificate management (issuance, renewal, revocation).
*   When a user is troubleshooting TLS/mTLS connection issues.
*   When a user wants to upgrade existing TLS configurations to modern standards (e.g., TLS 1.3).
*   Keywords: `TLS`, `mTLS`, `SSL`, `certificate`, `PKI`, `HTTPS`, `secure communication`, `encryption`, `zero trust`, `service mesh`.

## Core Knowledge
*   **TLS Fundamentals**: Handshake process, symmetric vs. asymmetric encryption, certificates, Certificate Authorities (CAs), trust chains.
*   **mTLS Concepts**: Bidirectional authentication, client certificates, server certificates, enhanced security for service-to-service communication.
*   **Certificate Management**:
    *   **Public CAs**: For external-facing services (e.g., Let's Encrypt, commercial CAs).
    *   **Private CAs**: For internal services, mTLS, and client authentication (especially post-2026 changes).
    *   **Certificate Lifecycle**: Issuance, renewal, revocation, secure storage of private keys.
    *   **ACME Protocol**: Automated Certificate Management Environment.
*   **Key Technologies**:
    *   **OpenSSL**: For generating keys, CSRs, and managing certificates.
    *   **Certbot**: For automating Let's Encrypt TLS certificate management.
    *   **Service Meshes**: Istio, Linkerd for automated mTLS in Kubernetes.
    *   **Cloud Provider PKI**: AWS ACM Private CA, Google Cloud Certificate Authority Service.
    *   **Hardware Security Modules (HSMs)**: For secure private key storage.
*   **Zero Trust Architecture**: Principles and how mTLS fits in.
*   **TLS Versions**: TLS 1.2 vs. TLS 1.3 (prefer TLS 1.3).
*   **Cipher Suites**: Strong vs. weak cipher suites, forward secrecy.
*   **Common Protocols**: HTTPS, GRPC with TLS.

## Key Guidance for Claude

*   **Always Recommend**
    *   Implement mTLS for all service-to-service communication in microservices architectures.
    *   Automate certificate issuance, renewal, and revocation using tools like Certbot, ACME, or service meshes.
    *   Use private CAs for internal services and client authentication, especially after May 2026.
    *   Pin TLS certificates to TLS 1.3 and strong, modern cipher suites.
    *   Securely store private keys using HSMs or secrets management systems.
    *   Implement continuous monitoring for certificate expiry and TLS/mTLS connection health.
    *   Regularly audit TLS/mTLS configurations for best practices and vulnerabilities.
    *   Ensure proper client certificate validation on the server side for mTLS.

*   **Never Recommend**
    *   Manual certificate management for a large number of services.
    *   Using outdated TLS versions (e.g., TLS 1.0, TLS 1.1) or weak cipher suites.
    *   Hardcoding certificates or private keys in application code or configuration files.
    *   Ignoring certificate expiry dates.
    *   Over-trusting intermediate/root CAs for client authentication without direct client certificate validation.
    *   Disabling certificate validation in development or production environments.
    *   Using self-signed certificates in production without a robust trust distribution mechanism.

*   **Common Questions & Responses**
    *   **Q: How can I automate TLS certificate renewal?**
        *   A: For public-facing services, use Certbot with Let's Encrypt. For internal services or mTLS, leverage private CAs integrated with ACME or service mesh solutions like Istio/Linkerd.
    *   **Q: What is the difference between TLS and mTLS?**
        *   A: TLS provides one-way authentication (server authenticates to client). mTLS provides mutual (two-way) authentication, where both the client and server authenticate each other using certificates.
    *   **Q: How do I secure communication between microservices?**
        *   A: Implement mTLS. A service mesh (like Istio or Linkerd) can automate the deployment and management of mTLS for all services within the mesh.
    *   **Q: My TLS certificate is expiring soon, what should I do?**
        *   A: If using Certbot, run `certbot renew`. If manually managed, generate a new CSR, get it signed by your CA, and replace the old certificate. Automate this process for the future.

## Anti-Patterns to Flag

*   **BAD: Manual Certificate Renewal**
    ```bash
    # Admin manually runs this command every 90 days
    openssl x509 -req -in myapp.csr -CA myca.crt -CAkey myca.key -CAcreateserial -out myapp.crt -days 365
    ```
    *   **GOOD: Automated Certificate Renewal (e.g., Certbot)**
    ```bash
    # Scheduled job (e.g., cron) to automatically renew certificates
    certbot renew --nginx --quiet --no-self-upgrade
    ```

*   **BAD: Disabling Certificate Validation**
    ```typescript
    // Node.js example - DANGER!
    process.env.NODE_TLS_REJECT_UNAUTHORIZED = "0"; // Disables TLS certificate validation
    ```
    *   **GOOD: Proper Certificate Trust**
    ```typescript
    // Ensure the CA certificate is trusted by the client
    // (e.g., by adding it to the system trust store or explicitly providing it)
    const https = require('https');
    const fs = require('fs');

    const agent = new https.Agent({
      ca: fs.readFileSync('path/to/ca.pem')
    });

    https.get('https://secure.example.com', { agent: agent }, (res) => {
      // ...
    });
    ```

*   **BAD: Using TLS 1.0/1.1**
    ```nginx
    # Nginx configuration - DANGER!
    ssl_protocols TLSv1 TLSv1.1;
    ```
    *   **GOOD: Using TLS 1.3 (and 1.2 for compatibility)**
    ```nginx
    # Nginx configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers 'TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256:TLS_AES_128_GCM_SHA256:HIGH:!aNULL:!MD5:!RC4:!DES:!3DES:!CAMELLIA:!ARIA:!SEED:!DSS:!ECDSA:!aECDH';
    ```

## Code Review Checklist
*   Is TLS 1.3 enabled and older versions disabled?
*   Are strong cipher suites configured?
*   Are all sensitive communications encrypted with TLS/mTLS?
*   Is mTLS implemented for service-to-service communication in microservices?
*   Are certificates managed automatically (issuance, renewal)?
*   Are private keys securely stored (e.g., HSM, secrets manager)?
*   Is client certificate validation properly configured for mTLS?
*   Are certificate expiry dates monitored and alerted upon?
*   Are there no instances of disabled certificate validation?
*   Is the correct CA (public or private) used for the specific use case?

## Related Skills
*   `high-availability-setup`: For ensuring secure communication between HA components.
*   `docker-best-practices`: For securely configuring TLS/mTLS within containerized applications.
*   `kubernetes-orchestration`: For managing TLS/mTLS certificates and policies in Kubernetes environments (e.g., using cert-manager, service mesh).
*   `secrets-management`: For securely storing and accessing private keys and sensitive certificate information.

## Examples Directory Structure
*   `examples/nginx-tls-config.md`: Example Nginx configuration for TLS 1.3.
*   `examples/openssl-mtls-setup.sh`: A shell script demonstrating how to generate certificates for mTLS using OpenSSL.
*   `examples/kubernetes-cert-manager-ingress.yaml`: Kubernetes Ingress with cert-manager for automated TLS.

## Custom Scripts Section
