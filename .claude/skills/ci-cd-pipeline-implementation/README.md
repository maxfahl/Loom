# CI/CD Pipeline Implementation Skill

This directory contains the Claude skill package for **CI/CD Pipeline Implementation**.
It provides comprehensive guidance, best practices, anti-patterns, and automation scripts
to help design, implement, and optimize Continuous Integration and Continuous Delivery/Deployment pipelines.

## Directory Structure

```
ci-cd-pipeline-implementation/
├── SKILL.md                  # Main instruction file for Claude
├── examples/                 # Code examples for various CI/CD platforms
│   ├── github-actions/
│   │   ├── ci.yml
│   │   └── deploy.yml
│   ├── gitlab-ci/
│   │   └── .gitlab-ci.yml
│   ├── jenkins/
│   │   └── Jenkinsfile
│   ├── circleci/
│   │   └── config.yml
│   ├── docker/
│   │   └── Dockerfile.optimized
│   └── terraform/
│       └── main.tf
├── patterns/                 # Common CI/CD patterns and templates
├── scripts/                  # Automation scripts to aid CI/CD workflows
│   ├── pipeline-config-validator.sh
│   ├── secrets-sync.py
│   ├── deployment-rollback.sh
│   └── docker-image-optimizer.py
└── README.md                 # This human-readable documentation
```

## SKILL.md

The `SKILL.md` file is the core of this package, providing Claude with detailed instructions on:

*   **Skill Purpose**: What this skill enables Claude to do.
*   **When to Activate This Skill**: Specific triggers for using this skill.
*   **Core Knowledge**: Fundamental CI/CD concepts, tools, and principles.
*   **Key Guidance for Claude**: Best practices (Always Recommend), anti-patterns (Never Recommend), and common Q&A.
*   **Anti-Patterns to Flag**: Code examples demonstrating bad vs. good practices.
*   **Code Review Checklist**: Items to verify during CI/CD pipeline reviews.
*   **Related Skills**: Links to other relevant Claude skills.
*   **Examples Directory Structure**: Overview of provided code examples.
*   **Custom Scripts Section**: Details on the automation scripts included.

## Automation Scripts

The `scripts/` directory contains valuable automation tools to streamline CI/CD development and operations.

### 1. `pipeline-config-validator.sh`

**Purpose:** Validates CI/CD configuration files (e.g., GitHub Actions YAML, GitLab CI YAML) for syntax errors and adherence to basic best practices *before* committing. This prevents pipeline failures due to simple typos or structural issues.

**Usage Examples:**

```bash
# Validate all common CI/CD files in the current directory and subdirectories
./scripts/pipeline-config-validator.sh

# Validate a specific GitHub Actions workflow file
./scripts/pipeline-config-validator.sh .github/workflows/ci.yml

# Validate a GitLab CI file and a directory containing GitHub Actions workflows
./scripts/pipeline-config-validator.sh .gitlab-ci.yml .github/workflows/

# Validate with a custom yamllint configuration
YAMLLINT_CONFIG=./my-yamllint.yml ./scripts/pipeline-config-validator.sh
```

### 2. `secrets-sync.py`

**Purpose:** Securely synchronizes environment variables from a local `.env` file to CI/CD platform secrets (e.g., GitHub Secrets). This automates the tedious and error-prone manual process of updating secrets.

**Usage Examples:**

```bash
# Sync secrets to a GitHub repository (assuming GITHUB_TOKEN is set as an environment variable)
python3 ./scripts/secrets-sync.py --owner my-org --repo my-repo

# Sync secrets from a custom .env file path
python3 ./scripts/secrets-sync.py --owner my-org --repo my-repo --env-file ./config/.env.prod

# Perform a dry run to see what changes would be made
python3 ./scripts/secrets-sync.py --owner my-org --repo my-repo --dry-run

# Sync secrets using a token passed directly (less secure, use env var if possible)
python3 ./scripts/secrets-sync.py --owner my-org --repo my-repo --github-token ghp_YOUR_TOKEN_HERE
```

### 3. `deployment-rollback.sh`

**Purpose:** Automates the rollback of a deployed application to a specified previous version. This script interacts with common deployment tools (e.g., `kubectl`, cloud provider CLIs) to quickly revert to a stable state, minimizing downtime.

**Usage Examples:**

```bash
# Kubernetes: Rollback 'my-app' in 'production' namespace to the previous revision
./scripts/deployment-rollback.sh --type kubernetes --name my-app --namespace production

# Kubernetes: Rollback 'my-app' to a specific revision (e.g., revision 3)
./scripts/deployment-rollback.sh --type kubernetes --name my-app --revision 3

# AWS ECS: Rollback 'my-service' in 'my-cluster' (forces a new deployment of current task definition)
./scripts/deployment-rollback.sh --type ecs --name my-service --cluster my-cluster --region us-east-1

# Google Cloud Run: Rollback 'my-service' in 'my-project' to the previous revision
./scripts/deployment-rollback.sh --type gcloud --name my-service --project my-project --region us-central1

# Perform a dry run for a Kubernetes rollback
./scripts/deployment-rollback.sh --type kubernetes --name my-app --dry-run
```

### 4. `docker-image-optimizer.py`

**Purpose:** Analyzes a Dockerfile and suggests optimizations (e.g., multi-stage builds, reducing layers, using smaller base images) to create leaner and more secure Docker images.

**Usage Examples:**

```bash
# Analyze a Dockerfile in the current directory
python3 ./scripts/docker-image-optimizer.py ./Dockerfile

# Analyze a Dockerfile located in a specific path
python3 ./scripts/docker-image-optimizer.py /path/to/my/project/Dockerfile

# Perform a dry run (all runs are effectively dry runs as it only suggests)
python3 ./scripts/docker-image-optimizer.py ./Dockerfile --dry-run
```
