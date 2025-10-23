--- 
name: docker-best-practices
version: 1.0.0
category: DevOps / Containerization
tags: Docker, Dockerfile, Containerization, Security, Optimization, CI/CD
description: Guides on building secure, optimized, and efficient Docker images and managing containers.
---

# Docker Best Practices

## 1. Skill Purpose

This skill provides comprehensive guidance on building secure, optimized, and efficient Docker images, and managing containers effectively. Adhering to these best practices leads to smaller image sizes, faster build times, reduced attack surfaces, and more reliable deployments. It covers strategies for image optimization, security hardening, and efficient Dockerfile authoring, ensuring that containerized applications are robust and production-ready.

## 2. When to Activate This Skill

Activate this skill when the user's request involves:
*   Optimizing Docker image size or build performance.
*   Improving the security posture of Docker containers.
*   Writing or reviewing Dockerfiles.
*   Troubleshooting Docker-related issues concerning size, security, or efficiency.
*   Setting up CI/CD pipelines for Dockerized applications.
*   Keywords: "Docker best practices", "optimize Dockerfile", "secure Docker image", "reduce Docker image size", "container security", "multi-stage build", ".dockerignore", "non-root user Docker", "Docker vulnerability scanning".

## 3. Core Knowledge

Claude needs to understand the following fundamental concepts related to Docker best practices:

*   **Dockerfile Directives**: Deep understanding of `FROM`, `RUN`, `COPY`, `ADD`, `WORKDIR`, `EXPOSE`, `ENV`, `ARG`, `ENTRYPOINT`, `CMD`, `USER`, `HEALTHCHECK`, `LABEL` and their optimal usage.
*   **Image Layers and Caching**: How Docker builds images layer by layer, the impact of each instruction on image size, and how to leverage build cache effectively.
*   **Multi-Stage Builds**: The concept of separating build-time dependencies from runtime dependencies to create lean production images.
*   **Minimal Base Images**: The advantages and appropriate use cases for lightweight base images like `alpine`, `slim` variants, `distroless`, `Wolfi`, or `Chainguard Images`.
*   **Build Context**: Understanding what the build context is and how `.dockerignore` files prevent unnecessary files from being sent to the Docker daemon.
*   **Container Security Principles**: 
    *   **Least Privilege**: Running containers with the minimum necessary permissions, especially as non-root users.
    *   **Secrets Management**: Securely handling sensitive information (API keys, passwords) without embedding them in images or environment variables.
    *   **Vulnerability Scanning**: The importance of regularly scanning images for known vulnerabilities using tools like Trivy, Clair, or Snyk.
    *   **Read-Only Filesystems**: Running containers with `--read-only` to prevent unauthorized writes.
    *   **Network Segmentation**: Restricting container network access.
*   **Reproducibility**: Pinning image versions and ensuring consistent builds across environments.
*   **Container Orchestration Basics**: How Docker images fit into systems like Docker Compose, Kubernetes, etc.

## 4. Key Guidance for Claude

### Always Recommend (✅ Best Practices)

*   **✅ Use Multi-Stage Builds**: Always separate your build environment from your runtime environment. This drastically reduces the final image size and attack surface by only including necessary runtime artifacts.
    ```dockerfile
    # Dockerfile for a Node.js application with multi-stage build

    # Stage 1: Build the application
    FROM node:20-alpine AS builder
    WORKDIR /app
    COPY package.json package-lock.json ./
    RUN npm install --production=false # Install dev dependencies for build
    COPY . .
    RUN npm run build # Or whatever your build command is

    # Stage 2: Create the final, lean runtime image
    FROM node:20-alpine
    WORKDIR /app
    COPY --from=builder /app/node_modules ./
    COPY --from=builder /app/dist . # Copy only the built artifacts
    COPY package.json ./
    CMD ["node", "dist/main.js"]
    EXCMD ["node", "dist/main.js"]
    ```
*   **✅ Choose Minimal Base Images**: Opt for lightweight base images (e.g., `alpine`, `slim` variants, `distroless`). They have smaller footprints, fewer packages, and thus fewer potential vulnerabilities.
    ```dockerfile
    # ✅ Good: Using Alpine for a Python application
    FROM python:3.10-alpine
    # ...

    # ✅ Good: Using a distroless image for a Go application
    FROM gcr.io/distroless/static-debian11
    # ...
    ```
*   **✅ Consolidate `RUN` Commands and Clean Up**: Combine multiple `RUN` instructions using `&&` and ensure you clean up caches and temporary files in the *same* `RUN` command to avoid creating unnecessary layers.
    ```dockerfile
    # ✅ Good: Consolidated RUN command with cleanup
    FROM ubuntu:22.04
    RUN apt-get update && \
        apt-get install -y --no-install-recommends some-package another-package && \
        rm -rf /var/lib/apt/lists/* # Clean up apt cache
    ```
*   **✅ Leverage `.dockerignore`**: Always use a `.dockerignore` file to exclude unnecessary files and directories (e.g., `.git`, `node_modules` in the build context, local IDE configs) from being sent to the Docker daemon. This speeds up builds and reduces image size.
    ```dockerignore
    # .dockerignore example
    .git
    .vscode/
    node_modules/
    npm-debug.log
    Dockerfile
    docker-compose.yml
    *.env
    ```
*   **✅ Run Containers as Non-Root Users**: Create a dedicated non-root user inside your container and switch to it using the `USER` directive. This limits the potential damage if the container is compromised.
    ```dockerfile
    # ✅ Good: Running as a non-root user
    FROM node:20-alpine
    WORKDIR /app
    COPY package.json ./
    RUN npm install --production
    RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser
    USER appuser
    CMD ["node", "src/index.js"]
    ```
*   **✅ Scan Images for Vulnerabilities**: Integrate image scanning tools (e.g., Trivy, Snyk, Clair) into your CI/CD pipeline to detect and remediate known vulnerabilities before deployment.
*   **✅ Pin Image Versions**: Always specify exact image tags (e.g., `node:20.10.0-alpine` instead of `node:latest` or `node:20-alpine`). This ensures reproducible builds and prevents unexpected breaking changes.
*   **✅ Manage Secrets Securely**: Never hardcode secrets in Dockerfiles or pass them directly as environment variables in production. Use Docker Secrets, Kubernetes Secrets, or external secret management solutions (e.g., HashiCorp Vault).

### Never Recommend (❌ Anti-Patterns)

*   **❌ Running as Root**: Avoid running your application inside the container as the `root` user. This is a major security risk as a compromised container could gain root access to the host system.
*   **❌ Embedding Secrets**: Do not hardcode API keys, passwords, or other sensitive information directly into your Dockerfile or commit them to version control. This exposes them to anyone with access to the image or repository.
*   **❌ Using `latest` or Broad Tags**: Never use the `latest` tag or broad tags like `node:20-alpine` (if `20-alpine` can change) for production images. These tags are mutable and can lead to inconsistent builds and unexpected behavior.
*   **❌ Installing Unnecessary Packages**: Avoid installing development tools, debuggers, or other packages that are not required for the application's runtime. Each additional package increases image size and potential attack surface.
*   **❌ Mounting Critical Host Directories**: Do not mount sensitive host directories (e.g., `/`, `/etc`, `/var/run/docker.sock`) into containers unless absolutely necessary and with extreme caution. This can lead to privilege escalation.
*   **❌ Multiple `CMD` or `ENTRYPOINT`**: A Dockerfile should only have one `CMD` and one `ENTRYPOINT` instruction. Multiple instances will only use the last one defined.

### Common Questions & Responses

*   **Q: How can I significantly reduce my Docker image size?**
    *   **A:** Implement multi-stage builds, choose minimal base images (like Alpine or distroless), effectively use `.dockerignore`, consolidate `RUN` commands, and clean up caches/temporary files in the same `RUN` instruction.
*   **Q: What are the most critical security practices for Docker images?**
    *   **A:** Running containers as non-root users, regularly scanning images for vulnerabilities, securely managing secrets (not embedding them), pinning image versions, and limiting container capabilities are paramount.
*   **Q: Should I use `COPY` or `ADD` in my Dockerfile?**
    *   **A:** Generally, prefer `COPY`. `ADD` has additional functionality (tar extraction, URL fetching) that can introduce security risks or unexpected behavior. Use `ADD` only when you specifically need its advanced features, otherwise `COPY` is safer and clearer.
*   **Q: How do I handle environment variables in Docker?**
    *   **A:** For non-sensitive configuration, `ENV` is fine. For sensitive data (secrets), use Docker Secrets, Kubernetes Secrets, or external secret management tools. Avoid passing secrets via `ENV` in production.

## 5. Anti-Patterns to Flag (Code Examples)

### ❌ Anti-Pattern: Single-Stage Build with Bloat and Root User

```dockerfile
# ❌ BAD: Single-stage build, running as root, installing dev tools
FROM node:18 # Large base image, often includes build tools

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm install # Installs dev dependencies unnecessarily

COPY . .

EXPOSE 3000
CMD ["npm", "start"] # Runs as root by default
```
**Correction**: Use a multi-stage build to separate build-time dependencies from runtime. Create a non-root user for the final stage.

### ❌ Anti-Pattern: Hardcoding Secrets and Using `latest` Tag

```dockerfile
# ❌ BAD: Hardcoding API key, using 'latest' tag
FROM python:latest # Mutable 'latest' tag

ENV API_KEY="super-secret-key-123" # ❌ Hardcoded secret

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

CMD ["python", "app.py"]
```
**Correction**: Pin image versions (e.g., `python:3.9-slim-buster`). Use Docker Secrets or a secrets management solution instead of `ENV` for sensitive data.

### ❌ Anti-Pattern: Unoptimized `RUN` Commands and No Cleanup

```dockerfile
# ❌ BAD: Multiple RUN commands, no cleanup, creating extra layers
FROM ubuntu:20.04

RUN apt-get update # Creates a layer
RUN apt-get install -y curl wget # Creates another layer
RUN rm -rf /var/lib/apt/lists/* # Cleanup in a separate layer, not effective

# ...
```
**Correction**: Combine `apt-get update` and `apt-get install` into a single `RUN` command using `&&`, and perform cleanup (`rm -rf /var/lib/apt/lists/*`) in the *same* command to ensure the cleanup is part of the same layer that added the packages.

## 6. Code Review Checklist

*   [ ] Is a multi-stage build implemented to separate build and runtime environments?
*   [ ] Is a minimal and appropriate base image (e.g., Alpine, slim, distroless) used for the final stage?
*   [ ] Are `RUN` commands consolidated using `&&` to minimize layers?
*   [ ] Is `rm -rf /var/lib/apt/lists/*` (or equivalent for other package managers) performed in the same `RUN` command as package installation?
*   [ ] Is a `.dockerignore` file present and effectively excluding unnecessary files from the build context?
*   [ ] Does the container run as a non-root user (`USER` directive) in the final stage?
*   [ ] Are all image versions explicitly pinned (e.g., `node:20.10.0-alpine`) instead of using `latest` or broad tags?
*   [ ] Are secrets handled securely (e.g., Docker Secrets, external vault) and NOT hardcoded in the Dockerfile or passed via `ENV` for sensitive data?
*   [ ] Are only essential packages and dependencies installed for the application's runtime?
*   [ ] Is the `HEALTHCHECK` instruction used for critical services?
*   [ ] Are `EXPOSE` instructions used correctly to document intended ports?
*   [ ] Is the `WORKDIR` directive used to set the working directory consistently?
*   [ ] Is the `CMD` or `ENTRYPOINT` instruction correctly defined for the application's startup?

## 7. Related Skills

*   `docker-compose-services`: For defining and running multi-container Docker applications.
*   `ci-cd-pipelines`: For automating the build, test, and deployment of Docker images.
*   `kubernetes-deployments`: For orchestrating and managing containerized applications at scale.
*   `linux-fundamentals`: Understanding underlying OS concepts for efficient containerization.

## 8. Examples Directory Structure

```
docker-best-practices/
├── examples/
│   ├── nodejs-app/
│   │   └── Dockerfile
│   ├── python-app/
│   │   └── Dockerfile
│   ├── multi-stage-build/
│   │   └── Dockerfile
│   └── dockerignore-example/
│       ├── .dockerignore
│       └── src/
│           └── app.js
├── patterns/
├── scripts/
└── README.md
```
