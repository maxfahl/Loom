---
Name: hashicorp-vault-integration
Version: 1.0.0
Category: Security / Secrets Management
Tags: HashiCorp Vault, secrets management, security, dynamic secrets, TypeScript, Kubernetes, CI/CD, Zero Trust
Description: Securely managing and rotating secrets using HashiCorp Vault.
---

# HashiCorp Vault Integration

## 1. Skill Purpose

This skill enables Claude to understand, design, and implement secure secrets management solutions using HashiCorp Vault. It covers best practices for centralizing, protecting, and dynamically provisioning sensitive data like API keys, database credentials, and certificates, especially within modern cloud-native and CI/CD environments.

## 2. When to Activate This Skill

Activate this skill when:
- Your application requires storing and accessing sensitive data (e.g., API keys, database passwords, private keys).
- You need to implement dynamic, short-lived credentials for enhanced security.
- You are building or deploying applications in Kubernetes or other containerized environments and need to inject secrets securely.
- You are setting up CI/CD pipelines that require access to secrets without hardcoding them.
- You are aiming for a Zero Trust security architecture.
- You need to automate secret rotation and auditing.

## 3. Core Knowledge

### 3.1. What is HashiCorp Vault?
HashiCorp Vault is a tool for securely accessing secrets. A secret is anything that you want to tightly control access to, such as API keys, passwords, certificates, and encryption keys. Vault provides a unified interface to any secret, while providing tight access control and recording a detailed audit log.

Key components:
- **Secrets Engines:** Store, generate, or encrypt data (e.g., KV, AWS, Databases, Transit).
- **Auth Methods:** Authenticate users and machines (e.g., AppRole, Kubernetes, LDAP, OIDC).
- **Policies (ACLs):** Define access rules to paths in Vault.

### 3.2. Dynamic Secrets
Vault can generate secrets on demand for various systems (databases, AWS, etc.). These secrets are short-lived and automatically revoked after a lease period, significantly reducing the risk of compromise and secret sprawl.

### 3.3. Vault Agent and Vault Agent Injector
- **Vault Agent:** A client-side daemon that can automatically authenticate to Vault, manage tokens, and render secrets to files or environment variables.
- **Vault Agent Injector:** A Kubernetes Mutating Admission Webhook that automatically injects Vault Agent sidecar containers into application pods, allowing applications to receive secrets without direct Vault API interaction.

### 3.4. Vault Policies (ACLs)
Vault policies are written in HCL (HashiCorp Configuration Language) or JSON and define what paths a token or identity is allowed to access and what capabilities (read, write, list, delete, sudo) are permitted on those paths.

```hcl
# Example Vault Policy (HCL)
path "secret/data/my-app/*" {
  capabilities = ["read"]
}

path "secret/data/my-app/config" {
  capabilities = ["read", "list"]
}

path "aws/creds/my-role" {
  capabilities = ["read"]
}
```

### 3.5. Transit Secrets Engine
Provides "Encryption as a Service." Applications can send data to Vault for encryption or decryption without ever seeing the encryption key itself. This is ideal for protecting sensitive data at rest in application databases.

### 3.6. Audit Logging
Vault provides comprehensive audit trails, logging every request and response. This is crucial for security monitoring, compliance, and incident response.

### 3.7. Authentication Methods
Choosing the right authentication method is key:
- **AppRole:** For machine-to-machine authentication, ideal for applications running on VMs or bare metal.
- **Kubernetes Auth:** For applications running in Kubernetes, authenticating based on Kubernetes Service Accounts.
- **OIDC/JWT:** For CI/CD pipelines or user-facing applications integrating with identity providers.

### 3.8. TypeScript Client Libraries
Several libraries facilitate Vault interaction in TypeScript applications:
- `hashi-vault-js` (Node.js focused)
- `@hashicorp/vault-client-typescript` (Official/community client)

**Example: Reading a secret with `hashi-vault-js`**
```typescript
// src/services/vault.service.ts
import Vault from 'hashi-vault-js';

interface AppSecrets {
  DATABASE_URL: string;
  API_KEY: string;
}

export class VaultService {
  private vault: Vault;

  constructor() {
    // Ensure VAULT_ADDR and VAULT_TOKEN (or other auth method env vars) are set
    const vaultAddress = process.env.VAULT_ADDR;
    const vaultToken = process.env.VAULT_TOKEN; // For development/testing, use AppRole or K8s auth in production

    if (!vaultAddress) {
      throw new Error('VAULT_ADDR environment variable is not set.');
    }
    if (!vaultToken) {
        console.warn('VAULT_TOKEN environment variable is not set. Ensure another auth method is configured.');
        // In a real app, you'd use AppRole, Kubernetes auth, etc.
    }

    this.vault = new Vault({
      apiVersion: 'v1',
      endpoint: vaultAddress,
      token: vaultToken, // Only for testing/dev with root token or short-lived token
    });
  }

  async getSecrets<T>(path: string): Promise<T> {
    try {
      const response = await this.vault.read(path);
      if (response && response.data && response.data.data) {
        return response.data.data as T;
      } else {
        throw new Error(`No data found at path: ${path}`);
      }
    } catch (error) {
      console.error(`Error reading secret from Vault at ${path}:`, error);
      throw error;
    }
  }

  // Example of using dynamic secrets (e.g., database credentials)
  async getDatabaseCredentials(role: string): Promise<{ username: string; password: string }> {
    try {
      const response = await this.vault.read(`database/creds/${role}`);
      if (response && response.data) {
        return response.data as { username: string; password: string };
      } else {
        throw new Error(`No database credentials found for role: ${role}`);
      }
    } catch (error) {
      console.error(`Error getting database credentials for role ${role}:`, error);
      throw error;
    }
  }
}

// Usage example (e.g., in app startup)
// const vaultService = new VaultService();
// async function loadConfig() {
//   try {
//     const appSecrets = await vaultService.getSecrets<AppSecrets>('secret/data/my-app/config');
//     process.env.DATABASE_URL = appSecrets.DATABASE_URL;
//     process.env.API_KEY = appSecrets.API_KEY;
//     console.log('Secrets loaded successfully.');
//   } catch (error) {
//     console.error('Failed to load secrets from Vault.', error);
//     process.exit(1);
//   }
// }
// loadConfig();
```

## 4. Key Guidance for Claude

### ✅ Always Recommend
- **Dynamic Secrets First:** Prioritize dynamic secrets for databases, cloud providers, and other services to minimize secret exposure and enable automatic rotation.
- **Least Privilege Policies:** Design Vault policies (ACLs) to grant only the minimum necessary capabilities on specific paths.
- **Automated Secret Rotation:** Configure Vault to automatically rotate secrets where supported, or implement external automation for static secrets.
- **Vault Agent/Injector for Applications:** Use Vault Agent (for VMs) or Vault Agent Injector (for Kubernetes) to securely deliver secrets to applications without direct Vault API calls from the application code.
- **Infrastructure as Code (IaC):** Manage Vault configuration (auth methods, secrets engines, policies) using tools like Terraform for version control, repeatability, and auditability.
- **Comprehensive Audit Trails:** Ensure Vault audit logging is enabled and integrated with a centralized logging solution for security monitoring and compliance.
- **Encryption-as-a-Service:** Leverage the Transit Secrets Engine for cryptographic operations, offloading key management from applications.
- **Secure Authentication:** Choose the most secure and appropriate authentication method for each client (e.g., Kubernetes Auth for K8s pods, AppRole for applications, OIDC for CI/CD).
- **Environment Variables for Vault Connection:** Use environment variables (`VAULT_ADDR`, `VAULT_TOKEN` for dev/testing, or specific auth method variables) to configure the application's connection to Vault.

### ❌ Never Recommend
- **Hardcoding Secrets:** Never embed sensitive credentials directly into application code, configuration files, or version control.
- **Long-Lived Static Secrets:** Avoid using static secrets with indefinite lifespans; prefer dynamic or frequently rotated secrets.
- **Overly Permissive Policies:** Do not grant `sudo` or broad `write` capabilities unless absolutely necessary and tightly controlled.
- **Storing Vault Tokens in Code/Disk:** Vault tokens should be treated as sensitive secrets themselves. Use Vault Agent or secure authentication methods to manage token lifecycle.
- **Frontend Vault Access:** Never allow client-side (browser) applications to directly access Vault.
- **Ignoring Audit Logs:** Audit logs are critical for security; ensure they are collected, stored securely, and regularly reviewed.

### ❓ Common Questions & Responses
- **"How do I get secrets into my application securely?"**
  - **Response:** "For Kubernetes, use the Vault Agent Injector. For VMs, use Vault Agent to render secrets to files or environment variables. For CI/CD, use OIDC authentication to obtain short-lived tokens and fetch secrets. Avoid direct API calls from application code unless absolutely necessary and with short-lived tokens."
- **"How can I rotate my database credentials automatically?"**
  - **Response:** "Configure the Database Secrets Engine in Vault. It can generate dynamic, short-lived credentials for your database and handle their rotation automatically. Your application will then request new credentials from Vault as needed."
- **"Which Vault authentication method is best for my application?"**
  - **Response:** "For applications running in Kubernetes, the Kubernetes Auth method is highly recommended. For applications on VMs or other platforms, AppRole is a robust machine authentication method. For CI/CD pipelines, OIDC/JWT authentication is ideal as it leverages workload identity."
- **"How do I encrypt sensitive data in my application without managing encryption keys?"**
  - **Response:** "Use Vault's Transit Secrets Engine. Your application sends data to Vault for encryption or decryption, and Vault handles the cryptographic keys. This keeps the keys secure within Vault and simplifies cryptographic operations for your application."

## 5. Anti-Patterns to Flag

### Anti-Pattern 1: Hardcoding Secrets in Code/Config
**BAD:** Storing sensitive API keys directly in `config.ts` or environment variables that are committed to Git.
```typescript
// ❌ BAD: src/config.ts
export const config = {
  DATABASE_URL: "postgres://user:password@db:5432/mydb",
  STRIPE_SECRET_KEY: "sk_test_YOUR_HARDCODED_KEY",
};
// Problem: Secrets are exposed in source control, making them vulnerable to compromise.
```

**GOOD:** Fetching secrets from Vault at runtime.
```typescript
// ✅ GOOD: src/config.ts (or similar setup)
// Secrets are loaded from environment variables which are populated by Vault Agent or a secure injection mechanism.
export const config = {
  DATABASE_URL: process.env.DATABASE_URL || '',
  STRIPE_SECRET_KEY: process.env.STRIPE_SECRET_KEY || '',
};

// ✅ GOOD: Application startup logic (simplified)
// In a real application, this would be handled by Vault Agent, K8s Injector, or a dedicated service.
// const vaultService = new VaultService();
// async function initializeApp() {
//   const secrets = await vaultService.getSecrets<AppSecrets>('secret/data/my-app/config');
//   process.env.DATABASE_URL = secrets.DATABASE_URL;
//   process.env.STRIPE_SECRET_KEY = secrets.STRIPE_SECRET_KEY;
//   // ... then start your application
// }
// initializeApp();
```

### Anti-Pattern 2: Overly Permissive Vault Policies
**BAD:** Granting `sudo` or `write` access to broad paths for application tokens.
```hcl
# ❌ BAD: policy.hcl
path "secret/*" {
  capabilities = ["read", "list", "write", "delete", "sudo"]
}
# Problem: If this token is compromised, an attacker has full access to all secrets.
```

**GOOD:** Implementing least privilege policies.
```hcl
# ✅ GOOD: policy.hcl
path "secret/data/my-app/config" {
  capabilities = ["read"]
}

path "database/creds/my-app-role" {
  capabilities = ["read"]
}
# Problem: This policy only allows reading specific secrets needed by the application.
```

## 6. Code Review Checklist

- [ ] **Secret Centralization:** Are all sensitive configurations (API keys, database credentials, etc.) managed by Vault and not hardcoded?
- [ ] **Dynamic Secrets Usage:** Are dynamic secrets utilized for databases, cloud providers, and other services where possible?
- [ ] **Least Privilege Policies:** Are Vault policies (ACLs) applied to application tokens and identities, granting only the minimum necessary permissions?
- [ ] **Secure Secret Injection:** For Kubernetes, is the Vault Agent Injector used? For other environments, is Vault Agent or a secure, short-lived token mechanism employed?
- [ ] **No Direct Token Storage:** Are Vault tokens never stored persistently in application code, configuration files, or on disk?
- [ ] **Error Handling:** Is there robust error handling for Vault API interactions, including connection failures and secret retrieval issues?
- [ ] **Audit Logging:** Is Vault's audit logging enabled and integrated with a centralized logging system?
- [ ] **Secret Rotation:** Are secrets configured for automatic rotation, or is a manual rotation process in place with clear procedures?
- [ ] **Encryption-as-a-Service:** If cryptographic operations are needed, is the Transit Secrets Engine used instead of application-managed keys?

## 7. Related Skills

- **Security Best Practices:** General security principles that underpin secure Vault integration.
- **Kubernetes:** For deploying applications and integrating Vault Agent Injector.
- **CI/CD Pipelines:** For securely injecting secrets into build and deployment processes.
- **Role-Based Access Control (RBAC):** For managing access to Vault itself and defining application policies.
- **Terraform:** For managing Vault infrastructure as code.

## 8. Examples Directory Structure

- `examples/node-vault-client/`
  - `src/index.ts` (Example application using `hashi-vault-js`)
  - `src/services/vault.service.ts` (Vault client wrapper)
  - `package.json`
- `examples/kubernetes-deployment/`
  - `k8s-deployment.yaml` (Example Kubernetes deployment with Vault Agent Injector annotations)
  - `vault-policy.hcl` (Example Vault policy for K8s service account)

## 9. Custom Scripts Section

This section will detail the automation scripts for HashiCorp Vault Integration.
