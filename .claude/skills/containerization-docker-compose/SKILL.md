### 1. Metadata Section

- Name: containerization-docker-compose
- Version: 1.0.0
- Category: DevOps / Infrastructure
- Tags: Docker, Docker Compose, containerization, microservices, CI/CD, security, deployment
- Description: Managing containerized applications using Docker and Docker Compose.

### 2. Skill Purpose

This skill enables Claude to guide developers in effectively using Docker and Docker Compose for containerizing applications. It covers best practices for image creation, container security, efficient development workflows, and deployment strategies, ensuring applications are portable, scalable, and maintainable.

### 3. When to Activate This Skill

Activate this skill when:
*   Starting a new project that requires containerization.
*   Optimizing existing Dockerfiles or Docker Compose configurations.
*   Implementing container security best practices.
*   Setting up local development environments with multiple services.
*   Integrating Docker into CI/CD pipelines.
*   Troubleshooting container-related issues.
*   Migrating applications to a containerized environment.

### 4. Core Knowledge

*   **Docker Fundamentals**: Dockerfile syntax, image layers, volumes, networks, container lifecycle.
*   **Docker Compose**: `docker-compose.yml` structure, services, networks, volumes, environment variables, healthchecks.
*   **Image Optimization**: Multi-stage builds, lightweight base images (Alpine, slim), `.dockerignore`, command combining, cache cleanup.
*   **Container Security**: Non-root users, read-only filesystems, resource limits, secret management (Docker Secrets, external vaults), vulnerability scanning.
*   **Development Workflows**: `docker compose watch`, hot-reloading, bind mounts.
*   **Deployment Strategies**: Orchestration (Kubernetes, Docker Swarm), CI/CD integration.
*   **Logging and Monitoring**: Container-aware logging, Prometheus, ELK Stack.
*   **Networking**: Custom bridge networks, host networking, port mapping.

### 5. Key Guidance for Claude

*   **Always Recommend**:
    *   Use multi-stage builds to minimize image size and attack surface.
    *   Pin image versions in Dockerfiles for reproducibility.
    *   Run containers as non-root users to enhance security.
    *   Utilize `.dockerignore` to exclude unnecessary files from build context.
    *   Define healthchecks for all services in Docker Compose.
    *   Manage secrets securely using Docker Secrets or external solutions, never hardcode.
    *   Integrate image vulnerability scanning into CI/CD pipelines.
    *   Use named volumes for data persistence and custom networks for service isolation.
*   **Never Recommend**:
    *   Using `latest` tag for production images.
    *   Running containers as `root` user.
    *   Storing sensitive information directly in Dockerfiles or images.
    *   Ignoring image size optimization.
    *   Using the default bridge network for complex multi-service applications.
    *   Modifying running containers; always rebuild images for changes (immutable infrastructure).
*   **Common Questions & Responses**:
    *   *Q: How can I reduce my Docker image size?*
        *   A: Employ multi-stage builds, use minimal base images (e.g., Alpine), leverage `.dockerignore`, combine `RUN` commands, and clean up caches within the same layer.
    *   *Q: What are the best practices for securing Docker containers?*
        *   A: Run containers as non-root users, use read-only filesystems, set resource limits, manage secrets securely, scan images for vulnerabilities, and restrict network access.
    *   *Q: How do I manage environment variables and secrets in Docker Compose?*
        *   A: Use `.env` files for non-sensitive environment variables and Docker Secrets for sensitive information. Avoid hardcoding them directly in `docker-compose.yml`.

### 6. Anti-Patterns to Flag

*   **BAD**: Single-stage Dockerfile with unnecessary build tools and `latest` tag.
    ```dockerfile
    FROM node:latest
    WORKDIR /app
    COPY package*.json ./
    RUN npm install
    COPY . .
    CMD ["npm", "start"]
    ```
*   **GOOD**: Multi-stage Dockerfile with a specific version and minimal runtime image.
    ```dockerfile
    # Build stage
    FROM node:20-alpine as builder
    WORKDIR /app
    COPY package*.json ./
    RUN npm install --production
    COPY . .
    RUN npm run build

    # Production stage
    FROM node:20-alpine
    WORKDIR /app
    COPY --from=builder /app/node_modules ./node_modules
    COPY --from=builder /app/dist ./dist
    CMD ["node", "dist/main.js"]
    ```
*   **BAD**: Hardcoding sensitive environment variables in `docker-compose.yml`.
    ```yaml
    services:
      app:
        environment:
          - DB_PASSWORD=mysecretpassword
    ```
*   **GOOD**: Using `.env` file for environment variables.
    ```yaml
    # docker-compose.yml
    services:
      app:
        env_file:
          - .env
    # .env file
    # DB_PASSWORD=mysecretpassword
    ```
    Or using Docker Secrets for production.

### 7. Code Review Checklist

*   [ ] Is a `.dockerignore` file present and effectively excluding unnecessary files?
*   [ ] Are multi-stage builds used to minimize image size?
*   [ ] Are specific, immutable image tags used (e.g., `node:20-alpine`) instead of `latest`?
*   [ ] Does the Dockerfile run the application as a non-root user?
*   [ ] Are sensitive environment variables and secrets handled securely (not hardcoded)?
*   [ ] Are healthchecks defined for all services in `docker-compose.yml`?
*   [ ] Are resource limits (CPU, memory) defined for containers in Docker Compose?
*   [ ] Are named volumes used for persistent data?
*   [ ] Are custom networks used for service isolation and communication?
*   [ ] Is the Dockerfile optimized for caching layers during builds?

### 8. Related Skills

*   `ci-cd-pipelines-github-actions`
*   `microservices-architecture`
*   `secrets-management`
*   `cloud-deployment-kubernetes-vps`

### 9. Examples Directory Structure

*   `examples/`
    *   `Dockerfile.optimized` (Example of an optimized multi-stage Dockerfile)
    *   `docker-compose.dev.yml` (Example Docker Compose for local development)
    *   `docker-compose.prod.yml` (Example Docker Compose for production deployment)
    *   `app/` (A simple Node.js application to demonstrate containerization)
        *   `index.ts`
        *   `package.json`

### 10. Custom Scripts Section

Here are 4 automation scripts that address common pain points in containerization:

1.  **`docker-image-analyzer.sh`**: A shell script that analyzes a Docker image for size, layers, and potential security issues (e.g., using `dive` or `docker history`).
2.  **`generate-docker-compose-env.py`**: A Python script to generate a `.env` file for Docker Compose based on a template or interactive prompts, helping manage environment variables.
3.  **`docker-cleanup.sh`**: A shell script to clean up old Docker images, containers, and volumes, freeing up disk space and maintaining a tidy environment.
4.  **`docker-healthcheck-tester.py`**: A Python script to test Docker Compose healthchecks locally, ensuring they correctly reflect service status.
