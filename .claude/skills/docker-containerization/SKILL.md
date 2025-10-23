---
name: docker-containerization
version: 1.0.0
category: DevOps / Containerization
tags: Docker, Container, DevOps, Microservices, Image Optimization, Security, Orchestration
description: Guides on efficient, secure, and scalable Docker containerization practices.
---

# Docker Containerization Skill

## 1. Skill Purpose

This skill enables Claude to assist developers in building, optimizing, securing, and managing Docker containers effectively. It covers best practices for Dockerfile creation, image optimization, container security, local development workflows, and preparation for orchestration environments.

## 2. When to Activate This Skill

Activate this skill when:
- A developer is creating a new Dockerfile or containerizing an application.
- Optimizing existing Docker images for size, build time, or performance.
- Addressing security concerns related to Docker containers (e.g., vulnerability scanning, secret management).
- Setting up local development environments using Docker Compose.
- Preparing applications for deployment to container orchestration platforms like Kubernetes.
- Troubleshooting Docker-related issues.
- Reviewing Dockerfiles or container configurations for best practices.

## 3. Core Knowledge

Claude should understand the following fundamental concepts, patterns, and APIs:

- **Dockerfile Syntax & Instructions**: `FROM`, `RUN`, `COPY`, `ADD`, `WORKDIR`, `EXPOSE`, `ENV`, `ARG`, `ENTRYPOINT`, `CMD`, `LABEL`, `HEALTHCHECK`, `USER`.
- **Docker Image Layers**: How layers are built, cached, and impact image size.
- **Multi-Stage Builds**: Separating build-time dependencies from runtime.
- **Minimal Base Images**: Alpine, `debian-slim`, language-specific slim images.
- **`.dockerignore`**: Excluding unnecessary files from build context.
- **Container Security Principles**: Least privilege, vulnerability scanning, secret management, read-only filesystems.
- **Docker Compose**: `docker-compose.yml` structure, services, networks, volumes for local development.
- **Container Orchestration Concepts**: Basic understanding of Kubernetes/Docker Swarm roles (though specific orchestration skills would be separate).
- **Networking in Docker**: Bridge networks, host networks, port mapping.
- **Volumes and Bind Mounts**: Data persistence.
- **Health Checks**: Ensuring container readiness and liveness.
- **Resource Limits**: CPU and memory constraints.
- **Registry Interaction**: Pushing and pulling images.

## 4. Key Guidance for Claude

### Always Recommend (✅ Best Practices)

- ✅ **Use Multi-Stage Builds**: Always separate build dependencies from runtime to create smaller, more secure images.
- ✅ **Start with Minimal Base Images**: Prefer `alpine`, `debian-slim`, or official language-specific slim images.
- ✅ **Leverage `.dockerignore`**: Exclude development files, `.git`, `node_modules`, etc., to speed up builds and reduce image size.
- ✅ **Pin Image Versions**: Use explicit tags (e.g., `node:20-alpine`) instead of `latest` for reproducibility.
- ✅ **Run as Non-Root User**: Create a dedicated non-root user in the Dockerfile and switch to it.
- ✅ **Implement Health Checks**: Define `HEALTHCHECK` instructions to ensure containers are truly ready and responsive.
- ✅ **Manage Secrets Securely**: Never hardcode secrets. Use Docker Secrets, environment variables (for non-sensitive dev), or external secret managers.
- ✅ **Scan Images for Vulnerabilities**: Integrate tools like Trivy or Snyk into CI/CD.
- ✅ **Combine `RUN` Commands**: Chain multiple commands with `&&` to reduce the number of layers.
- ✅ **Optimize Layer Caching**: Place frequently changing instructions later in the Dockerfile.
- ✅ **Single Concern Per Container**: Design containers to run a single primary process.
- ✅ **Use Volumes for Persistent Data**: Ensure data survives container restarts.
- ✅ **Define Resource Limits**: Set CPU and memory limits to prevent resource exhaustion.
- ✅ **Automate Builds**: Use CI/CD pipelines to automate image building and scanning.

### Never Recommend (❌ Anti-Patterns)

- ❌ **Running as Root**: Avoid `USER root` or not specifying a `USER` instruction, which defaults to root.
- ❌ **Using `latest` Tag**: Never use `FROM image:latest` in production; it leads to unpredictable builds.
- ❌ **Ignoring `.dockerignore`**: Building without it can lead to bloated images and security risks.
- ❌ **Hardcoding Secrets**: Embedding API keys, passwords, or sensitive data directly in Dockerfiles or images.
- ❌ **Bloated Images**: Including unnecessary tools, build dependencies, or large files in the final image.
- ❌ **Missing Health Checks**: Deploying containers without proper health checks can lead to unresponsive services.
- ❌ **Exposing Unnecessary Ports**: Only expose ports that are absolutely required for the application.
- ❌ **Installing SSH Server**: Avoid installing SSH servers inside application containers; use `docker exec` or orchestration tools for access.

### Common Questions & Responses (FAQ Format)

- **Q: My Docker image is too large. How can I reduce its size?**
  - A: "Consider implementing multi-stage builds, using a minimal base image like Alpine, and ensuring your `.dockerignore` file is comprehensive. Also, combine `RUN` commands to reduce layers."
- **Q: How do I handle sensitive information like API keys in Docker?**
  - A: "Never hardcode secrets. For production, use Docker Secrets, Kubernetes Secrets, or a dedicated secret management solution like HashiCorp Vault. For local development, environment variables or `.env` files (excluded from Git) can be used."
- **Q: My container starts but then immediately exits. What could be wrong?**
  - A: "Check your `CMD` and `ENTRYPOINT` instructions. Ensure your application is designed to run in the foreground and doesn't exit after starting. Review container logs (`docker logs <container_id>`) for error messages."
- **Q: How can I make my Docker builds faster?**
  - A: "Optimize layer caching by placing stable instructions early in the Dockerfile. Use `.dockerignore` to reduce build context size. Ensure you're using a fast Docker daemon and sufficient build resources."
- **Q: Should I use `ADD` or `COPY` in my Dockerfile?**
  - A: "Prefer `COPY` as it's more transparent and predictable. `ADD` has additional functionality like tar extraction and URL fetching, which can introduce security risks and complexity if not explicitly needed."

## 5. Anti-Patterns to Flag

### BAD: Single-stage build, root user, `latest` tag, no healthcheck

```typescript
// BAD Dockerfile
FROM node:latest
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
EXPOSE 3000
CMD ["npm", "start"]
```

### GOOD: Multi-stage build, non-root user, pinned version, healthcheck, .dockerignore

```typescript
// GOOD Dockerfile
# Stage 1: Build
FROM node:20-alpine AS builder
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build

# Stage 2: Run
FROM node:20-alpine
WORKDIR /app
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/package.json ./package.json
USER node # Run as non-root user
EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 CMD curl --fail http://localhost:3000/health || exit 1
CMD ["node", "dist/main.js"]
```

### BAD: Hardcoded secrets

```typescript
// BAD Dockerfile (hardcoded secret)
FROM alpine
ENV API_KEY="supersecretkey"
CMD ["sh", "-c", "echo $API_KEY"]
```

### GOOD: Using build arguments (for non-sensitive build-time values) or external secrets

```typescript
// GOOD Dockerfile (using build arg for non-sensitive value)
FROM alpine
ARG BUILD_VERSION
ENV APP_VERSION=$BUILD_VERSION
CMD ["sh", "-c", "echo App Version: $APP_VERSION"]

// For sensitive secrets, use Docker Secrets or orchestration secrets at runtime.
// Example with Docker Compose:
// services:
//   myapp:
//     image: myapp:1.0
//     secrets:
//       - my_api_key
// secrets:
//   my_api_key:
//     file: ./my_api_key.txt
```

## 6. Code Review Checklist

- [ ] **Dockerfile Optimization**:
    - [ ] Are multi-stage builds used?
    - [ ] Is a minimal base image selected?
    - [ ] Is `.dockerignore` present and comprehensive?
    - [ ] Are image versions pinned (no `latest`)?
    - [ ] Are `RUN` commands combined to minimize layers?
    - [ ] Is layer caching optimized (stable instructions first)?
- [ ] **Security**:
    - [ ] Does the container run as a non-root user?
    - [ ] Are secrets handled securely (no hardcoding)?
    - [ ] Are only necessary ports exposed?
    - [ ] Is an SSH server avoided inside the application container?
- [ ] **Reliability & Maintainability**:
    - [ ] Is a `HEALTHCHECK` instruction defined?
    - [ ] Are `CMD` and `ENTRYPOINT` correctly configured for foreground execution?
    - [ ] Are volumes used for persistent data?
    - [ ] Are resource limits (CPU/memory) defined?
    - [ ] Is the container designed for a single concern?
- [ ] **Local Development**:
    - [ ] If applicable, is `docker-compose.yml` used for multi-service local setups?

## 7. Related Skills

- [[kubernetes-orchestration]] (Future skill for deployment)
- [[ci-cd-pipelines]] (For automating Docker builds and deployments)
- [[nodejs-express-nestjs-development]] (For containerizing Node.js apps)
- [[python-django-flask-development]] (For containerizing Python apps)

## 8. Examples Directory Structure

```
examples/
├── nodejs-web-app/
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── src/
│   └── package.json
├── python-api/
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── src/
│   └── requirements.txt
└── multi-stage-build-example/
    ├── Dockerfile
    └── src/
```

## 9. Custom Scripts Section

Here are 3-5 automation scripts designed to address common pain points in Docker containerization workflows:

1.  **`docker-image-optimizer.sh`**: Analyzes a Dockerfile and suggests optimizations for image size and build speed.
2.  **`docker-compose-dev-setup.sh`**: Generates a basic `docker-compose.yml` for a given application type (Node.js, Python, etc.) with common services (database, cache).
3.  **`docker-secret-manager.py`**: A Python script to help manage Docker secrets for local development, encrypting/decrypting them and injecting them into `docker-compose.yml` or `Dockerfile` build args securely.
4.  **`docker-healthcheck-validator.sh`**: Validates the `HEALTHCHECK` instruction in a Dockerfile and provides recommendations.
