---
Name: docker-engineering
Version: 1.0.0
Category: DevOps / Containerization
Tags: Docker, Container, DevOps, CI/CD, Image Optimization, Security, Performance, TypeScript
Description: Enables Claude to apply best practices for Docker image creation, container management, and secure deployment.
---

# Docker Engineering Skill

## 1. Skill Purpose

This skill empowers Claude to design, build, and manage Docker containers and images following industry best practices. It focuses on creating efficient, secure, and maintainable containerized applications, with a particular emphasis on TypeScript-based projects. Claude will be able to optimize Dockerfiles, manage multi-container setups with Docker Compose, and implement robust security measures.

## 2. When to Activate This Skill

Activate this skill when:
*   Creating a new Dockerfile for any application, especially TypeScript/Node.js projects.
*   Reviewing or refactoring existing Dockerfiles for optimization or security.
*   Setting up local development environments using Docker Compose.
*   Troubleshooting Docker-related build or runtime issues.
*   Implementing CI/CD pipelines involving Docker image builds and deployments.
*   Advising on container security, performance, or resource management.

## 3. Core Knowledge

Claude's core knowledge for Docker Engineering includes:

### Dockerfile Syntax and Instructions
*   `FROM`: Specifying base images (e.g., `node:20-alpine`).
*   `RUN`: Executing commands during image build.
*   `COPY` / `ADD`: Copying files into the image.
*   `CMD` / `ENTRYPOINT`: Defining the command to run when the container starts.
*   `EXPOSE`: Documenting ports the container listens on.
*   `ENV`: Setting environment variables.
*   `ARG`: Defining build-time variables.
*   `USER`: Setting the user for subsequent commands.
*   `WORKDIR`: Setting the working directory.
*   `HEALTHCHECK`: Defining health checks for containers.

### Image Optimization
*   **Multi-stage Builds**: Separating build-time dependencies from runtime.
*   **Minimal Base Images**: Using `alpine`, `slim`, or `distroless` images.
*   `.dockerignore`: Excluding unnecessary files from the build context.
*   **Layer Caching**: Ordering instructions to maximize cache hits.
*   **Combining `RUN` commands**: Reducing layers and cleaning up temporary files.

### Container Management
*   **Docker Compose**: Defining and running multi-container Docker applications.
*   **Volumes**: Persistent data storage and sharing.
*   **Networks**: Inter-container communication and isolation.
*   **Resource Limits**: Setting CPU and memory constraints.
*   **Restart Policies**: Ensuring container resilience.

### Security Best Practices
*   **Non-root Users**: Running processes as non-root.
*   **Secret Management**: Using Docker Secrets, environment variables (carefully), or external vaults.
*   **Vulnerability Scanning**: Integrating tools like Trivy or Snyk.
*   **Image Signing**: Docker Content Trust.
*   **Least Privilege**: Minimizing permissions.

### Performance Considerations
*   Efficient logging strategies.
*   Optimizing network settings.
*   Monitoring container activity.

## 4. Key Guidance for Claude

### ✅ Always Recommend
*   **Multi-stage builds**: Essential for lean, production-ready images.
*   **Minimal base images**: Prioritize `alpine` or `slim` variants.
*   **`.dockerignore`**: Always use it to exclude irrelevant files (e.g., `.git`, `node_modules` from host, `src/` for compiled apps).
*   **Pin image versions**: Use explicit tags (e.g., `node:20.10.0-alpine`) instead of `latest`.
*   **Run as non-root user**: Create a dedicated user in the Dockerfile and switch to it.
*   **Scan images for vulnerabilities**: Integrate tools like Trivy into the CI/CD pipeline.
*   **Secure secret management**: Never hardcode secrets. Use Docker Secrets or environment variables (for non-sensitive dev configs).
*   **Define resource limits**: Prevent resource exhaustion with CPU and memory limits.
*   **Implement `HEALTHCHECK`**: Ensure containers are truly healthy.
*   **One process per container**: Follow the microservices principle for easier scaling and management.
*   **Docker Compose for local development**: Streamline multi-service setups.
*   **TypeScript compilation in build stage**: Only copy compiled JavaScript to the final image.

### ❌ Never Recommend
*   **Using `latest` tag in production**: Leads to unpredictable deployments.
*   **Running container processes as `root`**: Major security risk.
*   **Hardcoding secrets in Dockerfiles or committing `.env` files with secrets**: Exposes sensitive information.
*   **Building large, bloated images**: Increases attack surface, build times, and resource consumption.
*   **Running multiple distinct services in a single container**: Violates single responsibility principle, complicates scaling and monitoring.
*   **Copying entire build context too early**: Invalidates cache unnecessarily.
*   **Ignoring log management**: Can lead to disk space exhaustion.

### ❓ Common Questions & Responses

*   **Q: How can I reduce my Docker image size?**
    *   **A:** Implement multi-stage builds, use minimal base images (e.g., `alpine`), leverage `.dockerignore`, combine `RUN` commands to reduce layers, and clean up temporary files/caches within the same `RUN` instruction.
*   **Q: What's the best way to handle secrets in Docker?**
    *   **A:** For production, use Docker Secrets (for Swarm) or Kubernetes Secrets. For development, use environment variables loaded from a `.env` file that is *not* committed to version control. Never hardcode secrets in Dockerfiles.
*   **Q: My Docker builds are slow. How can I speed them up?**
    *   **A:** Optimize layer caching by placing frequently changing instructions (like `COPY . .`) later in the Dockerfile. Ensure `package.json`/`package-lock.json` are copied and dependencies installed before the main application code. Use BuildKit.
*   **Q: How do I ensure my Docker containers are secure?**
    *   **A:** Run containers as non-root users, scan images for vulnerabilities, manage secrets securely, pin image versions, restrict network access, and apply resource limits.

## 5. Anti-Patterns to Flag

### Anti-Pattern: Bloated Image, Root User, Unpinned Tag
```dockerfile
# BAD: Large base image, root user, unpinned tag, no .dockerignore implied
FROM ubuntu:latest
WORKDIR /app
COPY . .
RUN apt-get update && apt-get install -y curl git build-essential && rm -rf /var/lib/apt/lists/*
RUN npm install # Installs dev dependencies
EXPOSE 3000
CMD ["npm", "start"]
```

### Good Practice: Lean Image, Non-Root, Pinned Tag, Multi-Stage
```dockerfile
# GOOD: Multi-stage build for a TypeScript Node.js app
# Stage 1: Build environment
FROM node:20-alpine AS builder
WORKDIR /app
COPY package.json yarn.lock ./
RUN yarn install --frozen-lockfile
COPY . .
RUN yarn build # Compiles TypeScript to JavaScript

# Stage 2: Production environment
FROM node:20-alpine
WORKDIR /app
# Create a non-root user
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser
USER appuser
# Copy only necessary production artifacts
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
COPY package.json ./package.json # For production scripts if needed

# Expose port and define healthcheck
EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 CMD curl --fail http://localhost:3000/health || exit 1

CMD ["node", "dist/index.js"]
```

## 6. Code Review Checklist

*   [ ] Is a multi-stage build implemented for production images?
*   [ ] Is a minimal, appropriate base image used (e.g., `alpine`, `slim`)?
*   [ ] Is a `.dockerignore` file present and effectively excluding unnecessary files?
*   [ ] Are all base image versions explicitly pinned (e.g., `node:20.10.0-alpine`)?
*   [ ] Does the container run as a non-root user?
*   [ ] Are secrets handled securely (no hardcoded values, no `.env` files with secrets committed)?
*   [ ] Are CPU and memory resource limits defined in Docker Compose or orchestration?
*   [ ] Is a `HEALTHCHECK` instruction present and correctly configured?
*   [ ] Does each container run only one primary process?
*   [ ] Are `RUN` commands combined and cleaned up to minimize layers?
*   [ ] Is the build cache optimized by ordering instructions from least to most frequently changing?
*   [ ] For TypeScript/Node.js, is only compiled JavaScript copied to the final stage?

## 7. Related Skills

*   `ci-cd-pipelines-github-actions`: For automating Docker builds and deployments.
*   `containerization-docker-compose`: For orchestrating multi-container applications.
*   `microservices-architecture`: For designing containerized services.
*   `typescript-strict-mode`: For writing robust TypeScript applications to be containerized.

## 8. Examples Directory Structure

```
examples/
├── typescript-node-app/
│   ├── Dockerfile             # Example Dockerfile for a TS Node.js app
│   ├── src/
│   │   └── index.ts
│   ├── package.json
│   └── tsconfig.json
└── docker-compose-dev.yaml    # Example Docker Compose for local development
```

## 9. Custom Scripts Section

Here are 3-5 automation scripts that address common pain points in Docker Engineering:

### Script 1: `docker-image-analyzer.sh`
*   **Description**: Analyzes a Dockerfile for common best practices (multi-stage, non-root, .dockerignore, pinned versions) and suggests optimizations. Can optionally run a vulnerability scan using Trivy.
*   **Pain Point**: Manually reviewing Dockerfiles for adherence to best practices and identifying potential security issues.
*   **Type**: Quality Check / Build Helper (Shell Script)

### Script 2: `docker-compose-init.py`
*   **Description**: A Python script to interactively generate a basic `docker-compose.yaml` file for common project types (Node.js, Python, etc.), including services like databases (PostgreSQL, MongoDB) and caching (Redis), with development-friendly configurations.
*   **Pain Point**: Setting up `docker-compose.yaml` from scratch for new projects, ensuring consistency and best practices.
*   **Type**: Setup/Bootstrap / Code Generation (Python Script)

### Script 3: `docker-prune-all.sh`
*   **Description**: A robust shell script to safely clean up all unused Docker resources (stopped containers, dangling images, unused volumes, networks) with a dry-run option.
*   **Pain Point**: Docker consuming excessive disk space due to accumulated unused resources, requiring manual cleanup.
*   **Type**: Maintenance (Shell Script)

### Script 4: `docker-secret-template.py`
*   **Description**: A Python script that generates a `.env.template` file from a given Dockerfile or `docker-compose.yaml` by extracting `ENV` variables and `ARG`s, prompting the user for descriptions, and ensuring no sensitive defaults are exposed.
*   **Pain Point**: Manually creating `.env` templates, ensuring all necessary environment variables are documented, and preventing accidental exposure of sensitive information.
*   **Type**: Development Helper / Security (Python Script)
