---
name: data-sanitization
version: 1.0.0
category: Data Management / Security
tags: data privacy, anonymization, masking, synthetic data, GDPR, CCPA, HIPAA
description: Implementing processes to sanitize sensitive data for non-production environments.
---

### 2. Skill Purpose

This skill enables Claude to guide developers in implementing robust data sanitization techniques for non-production environments. It covers methods to protect sensitive information, ensure compliance with data privacy regulations, and maintain data utility for effective development and testing.

### 3. When to Activate This Skill

Activate this skill when:
*   Discussing data privacy concerns in development or testing.
*   Designing or reviewing data pipelines that involve sensitive information.
*   Implementing new features that handle PII or confidential data.
*   Setting up new development, staging, or QA environments.
*   Addressing compliance requirements (GDPR, CCPA, HIPAA) related to non-production data.
*   Troubleshooting issues related to sensitive data exposure in non-production.

### 4. Core Knowledge

*   **Data Masking Techniques**: Static vs. Dynamic, Substitution, Shuffling, Encryption/Tokenization, Nulling Out, Generalization, Deterministic Masking.
*   **Synthetic Data Generation**: Rule-based vs. ML-driven (GANs).
*   **Data Privacy Regulations**: GDPR, CCPA, HIPAA, and their implications for non-production data.
*   **Security Principles**: Least privilege, RBAC, environment segregation.
*   **Data Utility**: Balancing data protection with the need for realistic test data.
*   **Referential Integrity**: Maintaining relationships between masked data points.

### 5. Key Guidance for Claude

*   **Always Recommend**:
    *   Prioritize data privacy and compliance in all non-production environments.
    *   Automate data sanitization processes within CI/CD pipelines.
    *   Implement a "privacy by design" approach.
    *   Use deterministic masking for consistent test results across environments.
    *   Generate synthetic data when real data poses significant privacy risks.
    *   Secure non-production environments with strong access controls.
*   **Never Recommend**:
    *   Using unmasked production data in any non-production environment.
    *   Relying solely on manual sanitization processes.
    *   Ignoring data privacy regulations for non-production data.
    *   Compromising data utility to the point where testing becomes ineffective.
*   **Common Questions & Responses**:
    *   *Q: How do I choose between data masking and synthetic data generation?*
        *   A: Data masking is suitable when you need to retain the structure and some statistical properties of real data. Synthetic data generation is ideal when real data is scarce, highly sensitive, or you need to test edge cases not present in real data.
    *   *Q: What are the key considerations for maintaining referential integrity with masked data?*
        *   A: Use deterministic masking techniques where the same original value always maps to the same masked value across related datasets. This ensures relationships between tables or services are preserved.
    *   *Q: How can I integrate data sanitization into my CI/CD pipeline?*
        *   A: Implement automated scripts that trigger data masking or synthetic data generation as part of your deployment process to non-production environments. Ensure these scripts are version-controlled and regularly tested.

### 6. Anti-Patterns to Flag

*   **BAD**: Copying production database directly to staging without any sanitization.
    ```typescript
    // In a CI/CD script
    exec('pg_dump production_db > staging_db_backup.sql');
    exec('psql staging_db < staging_db_backup.sql');
    ```
*   **GOOD**: Using a data masking tool or script to sanitize sensitive columns during the data transfer.
    ```typescript
    // In a CI/CD script, assuming a data masking tool 'mask_data.sh'
    exec('pg_dump production_db | mask_data.sh --config masking_rules.json | psql staging_db');
    ```
*   **BAD**: Hardcoding sensitive test data in application code.
    ```typescript
    const user = {
      name: "John Doe",
      email: "john.doe@example.com", // Real email
      ssn: "XXX-XX-1234" // Partially real SSN
    };
    ```
*   **GOOD**: Generating synthetic test data or using masked data from a secure source.
    ```typescript
    // Using a synthetic data generator
    import { generateSyntheticUser } from './synthetic-data-generator';
    const user = generateSyntheticUser();
    ```

### 7. Code Review Checklist

*   [ ] Are all PII and sensitive data fields adequately masked or anonymized?
*   [ ] Is referential integrity maintained across masked datasets?
*   [ ] Are data sanitization processes automated and integrated into CI/CD?
*   [ ] Is synthetic data used where appropriate to avoid real data exposure?
*   [ ] Are non-production environments secured with appropriate access controls?
*   [ ] Is there clear documentation of the data sanitization rules and processes?
*   [ ] Does the sanitized data still allow for effective testing and development?

### 8. Related Skills

*   `data-privacy-compliance`
*   `ci-cd-pipelines`
*   `database-security`

### 9. Examples Directory Structure

*   `examples/`
    *   `masking-rules.json` (Example configuration for data masking)
    *   `synthetic-data-generator.ts` (TypeScript example of a synthetic data generator)
    *   `anonymize-user-data.ts` (TypeScript function for anonymizing user data)

### 10. Custom Scripts Section

Here are 4 automation scripts that address common pain points in data sanitization:

1.  **`generate-synthetic-data.py`**: A Python script to generate synthetic data based on a configuration file (e.g., JSON schema). This addresses the pain point of manually creating diverse and realistic test data.
2.  **`mask-database-dump.sh`**: A shell script that takes a database dump, applies masking rules (e.g., using `sed`, `awk`, or a custom tool), and outputs a sanitized dump. This automates the process of sanitizing existing data.
3.  **`validate-sanitization-rules.py`**: A Python script to validate data masking rules against a sample dataset, ensuring that sensitive data is indeed masked and referential integrity is maintained. This helps prevent accidental data leakage.
4.  **`setup-masked-db-env.sh`**: A shell script to automate the setup of a non-production database environment with masked data, integrating the `mask-database-dump.sh` script.
