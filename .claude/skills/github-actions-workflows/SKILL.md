---
name: github-actions-workflows
version: 1.0.0
category: CI/CD / Automation
tags: github actions, workflows, ci/cd, automation, yaml, best practices
description: Guides Claude on creating, managing, and optimizing GitHub Actions workflows.
---

# SKILL.md for github-actions-workflows

### 2. Skill Purpose

This skill enables Claude to design, implement, and maintain robust, secure, and efficient GitHub Actions workflows. It focuses on automating software development processes, from continuous integration and testing to continuous deployment, while adhering to best practices for security, performance, and maintainability.

### 3. When to Activate This Skill

Activate this skill whenever the task involves:
- Creating new CI/CD pipelines using GitHub Actions.
- Optimizing existing GitHub Actions workflows for performance or cost.
- Enhancing the security posture of GitHub Actions workflows.
- Troubleshooting issues in GitHub Actions runs.
- Refactoring or modularizing GitHub Actions workflows.
- Automating common GitHub Actions development tasks.
- Reviewing GitHub Actions workflow definitions.

Specific triggers/keywords/patterns:
- "create a github action for X"
- "optimize this github workflow"
- "secure my github actions"
- "troubleshoot github actions failure"
- "best practices for github actions"
- "automate deployment with github actions"
- "lint github actions workflow"
- "pin github action versions"

### 4. Core Knowledge

The fundamental concepts, patterns, and APIs Claude needs to know:

- **Workflow Structure**: `name`, `on`, `jobs`, `steps`, `uses`, `run`, `env`, `with`.
- **Events**: `push`, `pull_request`, `workflow_dispatch`, `schedule`, `issue_comment`, etc.
- **Jobs**: `runs-on`, `steps`, `outputs`, `needs`, `if`, `timeout-minutes`.
- **Steps**: `uses` (actions), `run` (shell commands), `name`, `id`, `env`, `with`.
- **Actions**: Marketplace actions, local actions, composite actions.
- **Contexts**: `github`, `env`, `job`, `steps`, `runner`, `secrets`, `strategy`, `matrix`.
- **Expressions**: `if` conditions, `format()`, `toJSON()`, `fromJSON()`.
- **Secrets**: `secrets.GITHUB_TOKEN`, custom repository/environment secrets.
- **Caching**: `actions/cache` for dependencies and build artifacts.
- **Matrix Strategies**: `strategy.matrix` for parallel job execution.
- **Reusable Workflows**: `workflow_call` for modularity.
- **Self-hosted Runners**: Configuration and security considerations.
- **Security Hardening**: Pinning actions to SHAs, OIDC, least privilege.
- **`actionlint`**: Linter for GitHub Actions workflows.

### 5. Key Guidance for Claude

- **Always Recommend** (✅ best practices)
    - ✅ **Pin Actions to Full-Length SHAs**: Always reference actions using their full commit SHA (e.g., `actions/checkout@a81eb75e2b2a0f13038f3d79a26232f9679b33cd`) instead of `vX` or `main` to prevent unexpected changes or supply chain attacks.
    - ✅ **Use GitHub Secrets**: Store all sensitive information (API keys, tokens) in GitHub Secrets, never hardcode them.
    - ✅ **Least Privilege for `GITHUB_TOKEN`**: Restrict the default `GITHUB_TOKEN` permissions to the minimum required for each job.
    - ✅ **Modular Workflows**: Break down complex workflows into smaller, reusable workflows or composite actions.
    - ✅ **Caching Dependencies**: Implement `actions/cache` for build dependencies (e.g., `node_modules`, `pip cache`) to speed up workflow runs.
    - ✅ **Matrix Builds for Parallelism**: Use `strategy.matrix` to run tests or builds across multiple environments concurrently.
    - ✅ **Conditional Job Execution**: Use `if` conditions to skip jobs or steps when they are not relevant (e.g., only deploy on `main` branch pushes).
    - ✅ **Set Timeouts**: Define `timeout-minutes` for jobs to prevent workflows from running indefinitely.
    - ✅ **Versioned Runners**: Specify exact runner versions (e.g., `ubuntu-22.04`) instead of `ubuntu-latest` for consistency.
    - ✅ **Lint Workflows**: Integrate `actionlint` or similar tools to validate workflow syntax and best practices.

- **Never Recommend** (❌ anti-patterns)
    - ❌ **Hardcoding Secrets**: Never embed sensitive data directly in workflow files.
    - ❌ **Using `actions/checkout@main` or `actions/setup-node@v1`**: Avoid using floating tags or branches for actions; always pin to a specific SHA.
    - ❌ **Overly Permissive `GITHUB_TOKEN`**: Do not grant `permissions: write-all` unless absolutely necessary and justified.
    - ❌ **Monolithic Workflows**: Avoid creating single, giant workflow files that handle everything.
    - ❌ **Uncached Dependencies**: Do not repeatedly download and install dependencies in every workflow run.
    - ❌ **Ignoring Error Handling**: Do not assume steps will always succeed. Use `continue-on-error` judiciously and implement proper error reporting.
    - ❌ **Running Untrusted Code**: Be cautious when running code from untrusted sources, especially in self-hosted runners.
    - ❌ **Exposing Sensitive Data in Logs**: Ensure no secrets or sensitive environment variables are printed to workflow logs.

- **Common Questions & Responses** (FAQ format)
    - **Q: How can I speed up my GitHub Actions workflows?**
        - A: Implement caching for dependencies (`actions/cache`), use matrix builds for parallelization, set appropriate `runs-on` runners, and ensure your steps are optimized.
    - **Q: What's the most secure way to use third-party actions?**
        - A: Pin them to a full-length commit SHA. Review their source code if possible, and consider forking critical actions for internal control. Restrict `GITHUB_TOKEN` permissions.
    - **Q: How do I pass data between jobs in a workflow?**
        - A: Use job `outputs`. A job can define outputs, and a dependent job can access them via `needs.<job_id>.outputs.<output_name>`.
    - **Q: When should I use reusable workflows versus composite actions?**
        - A: Use reusable workflows (`workflow_call`) for sharing entire workflows across repositories or for complex, multi-job sequences. Use composite actions for encapsulating a sequence of `run` and `uses` steps within a single job.
    - **Q: How do I prevent my workflow from running on specific branches or events?**
        - A: Use `if` conditions at the job or step level, or use `on.<event>.branches` / `on.<event>.tags` filters.

### 6. Anti-Patterns to Flag

- **Anti-Pattern 1: Floating Action Versions**
    - **BAD:**
        ```yaml
        steps:
          - uses: actions/checkout@v3
          - uses: actions/setup-node@v3
        ```
    - **GOOD:** (Replace with actual SHAs)
        ```yaml
        steps:
          - uses: actions/checkout@a81eb75e2b2a0f13038f3d79a26232f9679b33cd # Example SHA for v3
          - uses: actions/setup-node@64ed1c7eab4cce3362f2c96964c0867f10b380f8 # Example SHA for v3
        ```

- **Anti-Pattern 2: Hardcoded Secrets**
    - **BAD:**
        ```yaml
        - name: Deploy to Production
          run: |
            echo "Deploying with API_KEY=${{ env.API_KEY }}"
          env:
            API_KEY: "my-super-secret-key" # NEVER DO THIS
        ```
    - **GOOD:**
        ```yaml
        - name: Deploy to Production
          run: |
            echo "Deploying with API_KEY=${{ secrets.PROD_API_KEY }}"
          env:
            PROD_API_KEY: ${{ secrets.PROD_API_KEY }}
        ```

- **Anti-Pattern 3: Missing Caching for Dependencies**
    - **BAD:**
        ```yaml
        - name: Install dependencies
          run: npm ci
        - name: Build
          run: npm run build
        ```
    - **GOOD:**
        ```yaml
        - name: Cache Node.js modules
          uses: actions/cache@v3
          with:
            path: ~/.npm
            key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
            restore-keys: |
              ${{ runner.os }}-node-
        - name: Install dependencies
          run: npm ci
        - name: Build
          run: npm run build
        ```

### 7. Code Review Checklist

- [ ] Are all third-party actions pinned to a full-length commit SHA?
- [ ] Are all sensitive values stored in GitHub Secrets and accessed via `secrets.<SECRET_NAME>`?
- [ ] Is the `GITHUB_TOKEN` permission scope restricted to the minimum necessary?
- [ ] Is caching implemented for build dependencies (e.g., `actions/cache`)?
- [ ] Are jobs parallelized using `strategy.matrix` where appropriate?
- [ ] Are `if` conditions used to skip unnecessary jobs or steps?
- [ ] Are `timeout-minutes` set for long-running jobs?
- [ ] Are specific runner versions used (e.g., `ubuntu-22.04`)?
- [ ] Is the workflow modularized using reusable workflows or composite actions if complex?
- [ ] Is `actionlint` or a similar linter integrated into the workflow?
- [ ] Are there clear `name` and `description` fields for the workflow and jobs?
- [ ] Does the workflow avoid exposing sensitive data in logs?

### 8. Related Skills

- `ci-cd-pipelines`: For general CI/CD concepts and strategies.
- `docker-containers`: For building and pushing Docker images within workflows.
- `javascript-typescript`: For building and testing Node.js/TypeScript applications.
- `python-development`: For building and testing Python applications.
- `terraform-modules`: For deploying infrastructure as part of a CD pipeline.

### 9. Examples Directory Structure

```
examples/
├── nodejs-ci/
│   ├── .github/
│   │   └── workflows/
│   │       └── ci.yml
├── deploy-to-s3/
│   ├── .github/
│   │   └── workflows/
│   │       └── deploy.yml
└── reusable-workflow/
    ├── .github/
    │   └── workflows/
    │       └── callable-build.yml
    └── .github/
        └── workflows/
            └── main-ci.yml
```

### 10. Custom Scripts Section

Here are 3-5 automation scripts that would save significant time for developers working with GitHub Actions workflows:

1.  **`generate-workflow-boilerplate.sh`**: A shell script to quickly scaffold a new GitHub Actions workflow file with common jobs and best practices.
2.  **`pin-action-versions.py`**: A Python script to automatically update GitHub Actions references in a workflow file to use specific commit SHAs.
3.  **`validate-workflow.sh`**: A shell script to run `actionlint` on GitHub Actions workflow files.
4.  **`list-workflow-secrets.sh`**: A shell script to list GitHub repository secrets (requires `gh` CLI).
