# Data Sanitization Skill

This skill provides guidance and tools for implementing robust data sanitization processes in non-production environments. It focuses on protecting sensitive information, ensuring compliance with data privacy regulations (like GDPR, CCPA, HIPAA), and maintaining data utility for effective development and testing.

## Key Concepts:

*   **Data Masking**: Techniques to replace sensitive data with fictitious but realistic alternatives.
*   **Synthetic Data Generation**: Creating artificial data that mimics real data's statistical properties without containing actual sensitive information.
*   **Automation**: Integrating sanitization into CI/CD pipelines for consistency and efficiency.
*   **Security**: Best practices for securing non-production environments.

## Included Scripts:

This skill includes several automation scripts to streamline data sanitization workflows:

*   `generate-synthetic-data.py`: Generate realistic synthetic data based on a schema.
*   `mask-database-dump.sh`: Sanitize sensitive data within a database dump.
*   `validate-sanitization-rules.py`: Validate data masking rules against sample data.
*   `setup-masked-db-env.sh`: Automate the setup of a non-production database with masked data.

For detailed information on how to use this skill and its components, refer to `SKILL.md`.