# SKILL.md - Secrets Management

## Metadata Section

- Name: secrets-management
- Version: 1.0.0
- Category: Security / Operations
- Tags: Secrets, Security, Environment Variables, Key Management, Vault, .env, Best Practices, DevOps
- Description: Guides Claude on best practices for securely managing sensitive information (secrets) in applications and infrastructure.

## Skill Purpose

This skill enables Claude to identify, implement, and review secure strategies for handling application secrets. It covers the lifecycle of secrets from generation and storage to access and rotation, emphasizing the use of dedicated secret management solutions over insecure methods, particularly in production environments.

## When to Activate This Skill

Activate this skill when the task involves:
- Designing the security architecture for a new application or service.
- Storing API keys, database credentials, private keys, or other sensitive configuration.
- Migrating from insecure secret storage methods (e.g., hardcoding, plain text files) to secure ones.
- Setting up CI/CD pipelines that require access to secrets.
- Reviewing code or infrastructure configurations for secret exposure risks.
- Implementing secret rotation policies.
- Choosing between environment variables, `.env` files, and dedicated secret managers.
- Addressing compliance requirements related to sensitive data handling.
- Discussing security for microservices or cloud-native applications.

## Core Knowledge

The fundamental concepts, patterns, and APIs Claude needs to know for secrets management:

1.  **What are Secrets?**
    *   Any piece of sensitive information that grants access or control: API keys, database credentials, private keys, certificates, OAuth tokens, passwords, encryption keys, etc.

2.  **Secrets Management Principles:**
    *   **Never hardcode secrets:** Secrets should never be directly embedded in source code.
    *   **Never commit secrets to VCS:** Secrets should not be stored in Git or any version control system.
    *   **Least Privilege:** Grant access to secrets only to entities (users, applications) that absolutely need them, and only for the duration required.
    *   **Separation of Concerns:** Separate secrets from application code and configuration.
    *   **Encryption at Rest and in Transit:** Secrets must be encrypted when stored and when being transmitted.
    *   **Rotation:** Regularly change secrets to minimize the impact of compromise.
    *   **Auditing:** Log all access to secrets for accountability and detection of suspicious activity.
    *   **Dynamic Secrets:** Generate secrets on-demand with short lifespans.

3.  **Common Secret Storage Methods (and their security implications):**
    *   **Hardcoding:** (❌ BAD) Direct embedding in code.
    *   **Plain text files (`.env`, `config.json`):** (❌ BAD for production) Vulnerable to file system access, accidental commits.
    *   **Environment Variables:** (⚠️ CAUTION) Better than hardcoding, but still visible in process lists, inherited by child processes, not encrypted at rest. Acceptable for non-sensitive config or local dev, but not production secrets.
    *   **Dedicated Secret Managers:** (✅ BEST PRACTICE) Centralized, encrypted, access-controlled, auditable, supports rotation and dynamic secrets.

4.  **Dedicated Secret Management Solutions:**
    *   **Cloud-Native:** AWS Secrets Manager, Azure Key Vault, Google Cloud Secret Manager.
    *   **Open-Source/Self-Hosted:** HashiCorp Vault, Infisical, SOPS (Secrets OPerationS).
    *   **Commercial:** Doppler, 1Password Secrets Automation, CyberArk, Keeper Secrets Manager.

5.  **Integration Points:**
    *   **CI/CD Pipelines:** Secure injection of secrets into build and deployment processes.
    *   **Container Orchestration:** Kubernetes Secrets, Docker Swarm Secrets.
    *   **Application Runtime:** Retrieving secrets via SDKs or CLI tools.

6.  **TypeScript/Node.js Specifics:**
    *   `dotenv`: For loading `.env` files in development (but not for production secrets).
    *   Process environment variables (`process.env`).
    *   SDKs for cloud secret managers (e.g., `@aws-sdk/client-secrets-manager`).

## Key Guidance for Claude

### Always Recommend (✅ best practices)

- ✅ **Use a dedicated secret management solution for production environments.** This includes cloud-native services (AWS Secrets Manager, Azure Key Vault, GCP Secret Manager) or tools like HashiCorp Vault.
- ✅ **Implement the principle of least privilege.** Grant only the minimum necessary access to secrets for users and applications.
- ✅ **Encrypt all secrets both at rest and in transit.** Utilize KMS (Key Management Service) for managing encryption keys.
- ✅ **Automate secret rotation.** Configure secret managers to automatically rotate credentials (e.g., database passwords) on a regular schedule.
- ✅ **Integrate secrets management into CI/CD pipelines.** Retrieve secrets dynamically at runtime, never bake them into build artifacts.
- ✅ **Utilize dynamic secrets where possible.** Generate short-lived credentials on demand for services like databases.
- ✅ **Implement comprehensive audit logging and monitoring** for all secret access and modification events.
- ✅ **Store `.env` files only for local development** and ensure they are explicitly excluded from version control (`.gitignore`).
- ✅ **Use environment variables for non-sensitive configuration** or for bootstrap credentials to access a secret manager.
- ✅ **Educate developers** on secure coding practices related to secrets management.
- ✅ **Regularly review and audit** secret access policies and configurations.

### Never Recommend (❌ anti-patterns)

- ❌ **Hardcoding secrets directly in source code.** This is the most egregious anti-pattern and leads to immediate compromise if the code is exposed.
- ❌ **Committing secrets to version control systems (Git, SVN, etc.).** Even in private repositories, this is a high-risk practice.
- ❌ **Storing production secrets in plain text files (e.g., `.env`, `config.json`) on servers.** These are easily discoverable and readable.
- ❌ **Using environment variables for sensitive production secrets without additional protections.** They are visible in process lists and not encrypted at rest.
- ❌ **Disabling or ignoring secret rotation.** Stale secrets are a major security risk.
- ❌ **Granting broad, unrestricted access to secrets.** Violates the principle of least privilege.
- ❌ **Baking secrets into Docker images or other deployment artifacts.** Leads to secret sprawl and makes rotation difficult.
- ❌ **Logging secrets to application logs or standard output.** Can expose sensitive information.
- ❌ **Using weak or default passwords/keys for secrets.**
- ❌ **Ignoring security warnings or static analysis findings related to secret exposure.**

### Common Questions & Responses (FAQ format)

**Q: What's the difference between environment variables and a secret manager?**
A: Environment variables are simple key-value pairs accessible to processes, but they are not encrypted at rest, can be seen in process lists, and lack advanced features like rotation or auditing. Secret managers are dedicated services that provide centralized, encrypted storage, fine-grained access control, automated rotation, and comprehensive auditing, making them the secure choice for production secrets.

**Q: Can I use `.env` files in production?**
A: No, `.env` files are generally not recommended for production secrets. While convenient for local development, they are plain text files, vulnerable to accidental exposure, and lack the security features (encryption, access control, auditing, rotation) of a dedicated secret manager.

**Q: How do I get secrets into my application in a CI/CD pipeline?**
A: Your CI/CD system should integrate with your secret manager. During the build or deployment phase, the pipeline should make an API call to the secret manager to retrieve the necessary secrets and inject them as environment variables into the running application container or process. Never hardcode them in the pipeline script or commit them to the repository.

**Q: How often should I rotate my secrets?**
A: The frequency depends on the secret's sensitivity and exposure. Database passwords, API keys, and certificates should be rotated regularly (e.g., every 30-90 days). Dynamic secrets can be rotated much more frequently, even per request or per session. Automated rotation via a secret manager is highly recommended.

**Q: What is a "bootstrap secret" and how do I manage it?**
A: A bootstrap secret is the initial credential an application uses to authenticate with a secret manager. This secret itself needs to be managed securely, often as a highly restricted environment variable or through instance roles/identities (e.g., AWS IAM roles for EC2 instances) that grant temporary access to the secret manager.

## Anti-Patterns to Flag

### Anti-Pattern 1: Hardcoding Secrets

**BAD (Directly in code):**
```typescript
// src/database.ts
const DB_PASSWORD = "mySuperSecretPassword123"; // ❌ NEVER DO THIS!

// src/api.ts
const STRIPE_API_KEY = "sk_test_********************"; // ❌ NEVER DO THIS!
```

**GOOD (Using environment variables for local dev, secret manager for prod):**
```typescript
// src/database.ts
// For local development, loaded from .env (excluded from VCS)
// For production, loaded from environment or secret manager
const DB_PASSWORD = process.env.DB_PASSWORD;

// src/api.ts
const STRIPE_API_KEY = process.env.STRIPE_API_KEY;

// Ensure these are validated and handled if missing
if (!DB_PASSWORD) {
  throw new Error("DB_PASSWORD environment variable is not set.");
}
```

### Anti-Pattern 2: Committing `.env` files to VCS

**BAD (Exposes secrets to anyone with repo access):**
```
// .gitignore
# (missing .env)

// .env (committed to Git)
DB_USER=admin
DB_PASSWORD=supersecret
API_KEY=xyz123abc
```

**GOOD (Proper `.gitignore` and `.env.example`):**
```
// .gitignore
.env
.env.local
.env.*.local

// .env.example (committed to Git, for documentation)
# Example environment variables
DB_USER=your_db_user
DB_PASSWORD=your_db_password
API_KEY=your_api_key

// .env (local, NOT committed to Git)
DB_USER=local_dev_user
DB_PASSWORD=local_dev_password
API_KEY=dev_api_key
```

### Anti-Pattern 3: Storing Secrets in Logs

**BAD (Sensitive data in plain sight):**
```typescript
// src/auth.service.ts
async function login(username: string, password: string) {
  console.log(`Attempting login for user: ${username} with password: ${password}`); // ❌ NEVER LOG SECRETS!
  // ... authentication logic
}

// In a shell script, accidentally echoing a secret:
# export DB_PASSWORD="mysecret"
# echo "Database password is: $DB_PASSWORD" # ❌ NEVER ECHO SECRETS!
```

**GOOD (Logging only non-sensitive information):**
```typescript
// src/auth.service.ts
async function login(username: string, password: string) {
  console.log(`Attempting login for user: ${username}`); // ✅ Only log non-sensitive info
  // ... authentication logic
}

// In a shell script, avoid echoing secrets:
# export DB_PASSWORD="mysecret"
# echo "Database password has been set." # ✅ Confirm without revealing
```

## Code Review Checklist

- [ ] Are all sensitive values (API keys, passwords, etc.) externalized from the codebase?
- [ ] Are secrets never hardcoded or committed to version control?
- [ ] Is a dedicated secret management solution used for production environments?
- [ ] Is the principle of least privilege applied to secret access?
- [ ] Are secrets encrypted at rest and in transit?
- [ ] Is automated secret rotation implemented where appropriate?
- [ ] Are secrets injected securely into CI/CD pipelines at runtime, not baked into artifacts?
- [ ] Is there comprehensive audit logging for all secret access?
- [ ] Are `.env` files used only for local development and properly `.gitignore`d?
- [ ] Are environment variables used cautiously for secrets, and never for highly sensitive production data?
- [ ] Is there a clear strategy for managing "bootstrap secrets" for the secret manager itself?
- [ ] Are secrets never logged to stdout, stderr, or application logs?
- [ ] Are default or weak credentials avoided?
- [ ] Is input validation performed on retrieved secrets if they are expected to conform to a specific format?

## Related Skills

- `jwt-authentication`: For securely managing JWT secret keys and other authentication-related secrets.
- `api-security`: General API security principles, including protecting API keys and endpoints.
- `docker-best-practices`: For securely handling secrets in containerized environments (e.g., Docker Secrets, Kubernetes Secrets).
- `github-actions-workflows`: For securely injecting secrets into GitHub Actions workflows.
- `terraform-modules`: For provisioning infrastructure that integrates with secret managers.

## Examples Directory Structure

```
examples/
├── local-dev/
│   ├── .env.example
│   ├── .env
│   ├── app.ts
│   └── package.json
├── cloud-native/
│   ├── aws-secrets-manager-example.ts
│   ├── azure-key-vault-example.ts
│   ├── gcp-secret-manager-example.ts
│   └── package.json
├── ci-cd/
│   ├── .github/
│   │   └── workflows/
│   │       └── deploy.yml
│   └── README.md
└── README.md
```

## Custom Scripts Section

Here are 3 automation scripts designed to streamline common tasks related to secrets management:

1.  **`generate_secret.py` (Python): Secure Secret Generator**
    *   **Purpose:** Generates cryptographically secure random strings suitable for various types of secrets (e.g., API keys, database passwords, encryption keys). It allows specifying length and character sets.
    *   **Pain Point Solved:** Manually generating strong, random secrets is often done insecurely or with insufficient entropy. This script provides a reliable way to create high-quality secrets.
    *   **Usage:** `python scripts/generate_secret.py --length 64 --type password`

2.  **`env_validator.py` (Python): .env File Validator**
    *   **Purpose:** Lints and validates `.env` files against common best practices and an optional `.env.example` template. It checks for missing variables, incorrect formatting, and potential security issues.
    *   **Pain Point Solved:** Inconsistent or malformed `.env` files can lead to runtime errors or accidental secret exposure. This script helps maintain `.env` file quality and consistency.
    *   **Usage:** `python scripts/env_validator.py --env-file .env --template .env.example`

3.  **`secure_env_loader.sh` (Shell): Secure Environment Loader**
    *   **Purpose:** A shell script to securely load environment variables from a `.env` file into the current shell session. It includes checks for file permissions and provides warnings about best practices, offering a safer alternative to directly `source`ing `.env` files.
    *   **Pain Point Solved:** Directly sourcing `.env` files can expose secrets in shell history or if file permissions are too lax. This script mitigates these risks for local development.
    *   **Usage:** `source scripts/secure_env_loader.sh .env`
