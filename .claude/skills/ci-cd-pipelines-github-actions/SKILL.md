---
Name: ci-cd-pipelines-github-actions
Version: 1.0.0
Category: DevOps / CI/CD
Tags: github actions, ci/cd, automation, devops, security, typescript
Description: Guides Claude on setting up and managing CI/CD pipelines using GitHub Actions, focusing on best practices for security, efficiency, and maintainability.
---

## Skill Purpose
This skill enables Claude to assist developers in designing, implementing, and optimizing CI/CD pipelines using GitHub Actions. It covers best practices for secure, efficient, and maintainable workflows, helping to automate software delivery from code commit to deployment.

## When to Activate This Skill
*   When a user asks to set up CI/CD for a new project.
*   When a user needs to optimize existing GitHub Actions workflows.
*   When a user is looking for best practices in GitHub Actions security.
*   When a user wants to automate deployment processes.
*   When a user encounters issues with GitHub Actions workflows (e.g., slow builds, security warnings).
*   Keywords: `github actions`, `ci/cd`, `workflow`, `pipeline`, `deploy`, `build`, `test`, `automation`, `security`, `optimize`.

## Core Knowledge
*   **GitHub Actions Fundamentals**: Workflows, events, jobs, steps, actions, runners, secrets, environments.
*   **YAML Syntax**: Proper structuring of workflow files.
*   **Security Best Practices**: Least privilege, secret management, action pinning, OIDC, branch protection.
*   **Performance Optimization**: Caching, parallelization, path filtering, conditional execution.
*   **Maintainability**: Modularity, reusability, versioning.
*   **Common Actions**: `actions/checkout`, `actions/setup-node`, `actions/cache`, `actions/upload-artifact`, `actions/download-artifact`, `actions/github-script`.
*   **Deployment Strategies**: Continuous Deployment (CD), Continuous Delivery (CD), blue/green, canary.
*   **Testing**: Unit, integration, E2E testing within CI.
*   **Code Quality**: Linting, type checking, security scanning (Dependabot, CodeQL).

## Key Guidance for Claude

*   **Always Recommend**
    *   Pin actions to a full commit SHA for security and stability.
    *   Use `GITHUB_TOKEN` with least privilege permissions.
    *   Store sensitive data in GitHub Secrets.
    *   Implement dependency caching to speed up builds.
    *   Use `concurrency` with `cancel-in-progress: true` to prevent stale runs.
    *   Break down complex workflows into reusable components.
    *   Utilize path filtering to trigger workflows only when relevant files change.
    *   Integrate security scanning tools early in the pipeline.
    *   Set job-level timeouts.
    *   Use OIDC for authentication with cloud providers.

*   **Never Recommend**
    *   Hardcoding secrets directly in workflow files.
    *   Using mutable action references (e.g., `@main`, `@latest`).
    *   Granting `GITHUB_TOKEN` excessive permissions.
    *   Ignoring workflow logs or security alerts.
    *   Creating monolithic, hard-to-maintain workflows.
    *   Skipping dependency caching for frequently built projects.

*   **Common Questions & Responses**
    *   **Q: How do I secure my GitHub Actions workflows?**
        *   A: Focus on least privilege for `GITHUB_TOKEN`, pin actions to commit SHAs, use GitHub Secrets, and integrate OIDC for cloud authentication.
    *   **Q: My CI/CD pipeline is slow, how can I speed it up?**
        *   A: Implement dependency caching, parallelize jobs, use path filtering, and ensure efficient test execution.
    *   **Q: How can I reuse parts of my workflow across multiple repositories?**
        *   A: Create reusable workflows or composite actions to encapsulate common steps and logic.
    *   **Q: What's the best way to deploy to AWS/GCP/Azure from GitHub Actions?**
        *   A: Use OIDC for secure, passwordless authentication, and leverage official cloud provider actions or custom scripts for deployment.

## Anti-Patterns to Flag

*   **BAD: Hardcoded Secrets**
    ```yaml
    - name: Deploy to Production
      run: |
        echo "Deploying with API_KEY=${{ secrets.MY_API_KEY_DEV }}" # Incorrectly using dev secret
        # ... deployment logic ...
    ```
    *   **GOOD: Proper Secret Usage**
    ```yaml
    - name: Deploy to Production
      env:
        API_KEY: ${{ secrets.PRODUCTION_API_KEY }}
      run: |
        echo "Deploying with API_KEY=***" # Secrets are masked in logs
        # ... deployment logic using $API_KEY ...
    ```

*   **BAD: Unpinned Action**
    ```yaml
    - uses: actions/checkout@main # Mutable reference, can introduce breaking changes or security risks
    ```
    *   **GOOD: Pinned Action (Commit SHA)**
    ```yaml
    - uses: actions/checkout@b4ffde65f46336ab88eb5afa53bb794d44cc353d # Pinned to a specific commit SHA
    ```

*   **BAD: Overly Permissive GITHUB_TOKEN**
    ```yaml
    permissions:
      contents: write # Grants write access when only read might be needed
      pull-requests: write
    ```
    *   **GOOD: Least Privilege GITHUB_TOKEN**
    ```yaml
    permissions:
      contents: read # Only read access
      pull-requests: write # If the workflow needs to comment on PRs
    ```

## Code Review Checklist
*   Are all third-party actions pinned to a full commit SHA?
*   Are `GITHUB_TOKEN` permissions scoped to the least privilege necessary?
*   Are all sensitive values stored in GitHub Secrets and not hardcoded?
*   Is dependency caching implemented for faster builds?
*   Is `concurrency` used to prevent stale workflow runs?
*   Are workflows modular and reusable?
*   Is path filtering applied to avoid unnecessary runs?
*   Are security scanning tools integrated?
*   Are job timeouts configured?
*   Is OIDC used for cloud authentication?
*   Are there clear comments explaining complex steps?

## Related Skills
*   `typescript-strict-mode`: For ensuring code quality in TypeScript projects.
*   `docker-best-practices`: For building efficient and secure Docker images within CI.
*   `k6-load-testing`: For integrating performance testing into CI/CD.
*   `jest-unit-tests`: For running unit tests in CI.
*   `playwright-e2e`: For running end-to-end tests in CI.

## Examples Directory Structure
*   `examples/basic-ci.yaml`: A simple CI workflow for a TypeScript project.
*   `examples/deploy-to-aws-s3.yaml`: Example of deploying a static site to AWS S3 using OIDC.
*   `examples/reusable-workflow.yaml`: Demonstrates a reusable workflow.
*   `examples/matrix-build.yaml`: Example of using matrix builds for testing.

## Custom Scripts Section
