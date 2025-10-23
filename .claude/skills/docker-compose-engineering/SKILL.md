---
name: docker-compose-engineering
version: 1.0.0
category: DevOps / Containerization
tags: Docker, Docker Compose, Containerization, DevOps, Microservices, YAML, Infrastructure as Code
description: Guides Claude on best practices for defining and running multi-container Docker applications with Docker Compose.
---

# Docker Compose Engineering Skill

## 1. Skill Purpose

This skill enables Claude to assist developers in efficiently defining, running, and managing multi-container Docker applications using Docker Compose. It focuses on adhering to best practices for modularity, data persistence, security, resource management, and development workflow optimization.

## 2. When to Activate This Skill

Activate this skill when the user is:
- Working with `docker-compose.yml` files.
- Setting up local development environments with multiple services.
- Orchestrating multiple Docker containers for an application.
- Managing container networks or volumes.
- Discussing containerization strategies for development or testing.
- Troubleshooting Docker Compose related issues.
- Automating Docker-related tasks.

## 3. Core Knowledge

Claude should be proficient in the following Docker Compose concepts and related Docker knowledge:

-   **`docker-compose.yml` Syntax and Structure:** Understanding `services`, `networks`, `volumes`, and top-level configuration.
-   **Docker Compose Versions:** Awareness of different `version` fields and the modern approach of omitting it with newer Docker CLI versions.
-   **Service Configuration:**
    -   `build` vs. `image`: When to build from `Dockerfile` or pull an existing image.
    -   `ports`: Mapping host ports to container ports.
    -   `volumes`: Using named volumes for persistence and bind mounts for development.
    -   `environment`: Passing environment variables to containers.
    -   `env_file`: Loading environment variables from a file.
    -   `depends_on`: Declaring service dependencies (for startup order, not readiness).
    -   `healthcheck`: Defining commands to check container health.
    -   `restart`: Defining container restart policies.
    -   `command`, `entrypoint`: Overriding default commands.
    -   `configs`, `secrets`: Managing configuration and sensitive data.
-   **Network Types and Configuration:** `bridge` (default), `host`, `overlay`, and user-defined networks for isolation and communication.
-   **Volume Types and Management:** Named volumes (preferred for persistence), bind mounts (preferred for development), and anonymous volumes.
-   **Environment Variables and Secrets Management:** Best practices for handling sensitive data using `.env` files (development) and Docker Secrets or external secret managers (production).
-   **Resource Limits:** Configuring `cpu_shares`, `cpus`, `mem_limit`, `mem_reservation` to prevent resource exhaustion.
-   **Dockerfile Best Practices:**
    -   Multi-stage builds for optimized, smaller images.
    -   Using `.dockerignore` to exclude unnecessary files from the build context.
    -   Running containers as non-root users.
    -   Pinning image versions explicitly.
    -   Layer caching optimization.
-   **Common Docker Compose Commands:** `docker compose up`, `docker compose down`, `docker compose build`, `docker compose start`, `docker compose stop`, `docker compose ps`, `docker compose logs`, `docker compose exec`.
-   **Development vs. Production Configurations:** Strategies for managing different configurations using multiple Compose files (`-f`) or profiles.

## 4. Key Guidance for Claude

### Always Recommend (✅ Best Practices)

-   **Use the Latest Stable Docker Compose File Format:** While the `version` field is technically deprecated in newer Docker CLI versions, ensure the syntax aligns with modern Docker Compose capabilities.
-   **Keep Services Modular and Single-Purpose:** Each service should ideally encapsulate a single responsibility (e.g., a web server, a database, a cache).
-   **Use Named Volumes for Data Persistence:** For any data that needs to survive container restarts or recreation, use named volumes. Bind mounts are suitable for development (e.g., mounting source code).
-   **Manage Sensitive Data Securely:** Use `.env` files for environment variables in development. For production, leverage Docker Secrets or external secret management solutions (e.g., HashiCorp Vault, AWS Secrets Manager).
-   **Define Custom Networks Explicitly:** Create user-defined networks to control inter-service communication and isolate services, improving security and clarity.
-   **Apply Resource Limits to Services:** Configure `cpu_shares`, `mem_limit`, etc., to prevent any single service from consuming excessive host resources and impacting other services.
-   **Implement Health Checks for All Services:** Define `healthcheck` commands to allow Docker to determine if a container is truly ready and healthy, enabling proper dependency management and automatic restarts.
-   **Run Containers as Non-Root Users:** Always create a non-root user in your `Dockerfile` and switch to it before running your application to mitigate security risks.
-   **Pin Image Versions Explicitly:** Avoid using `latest` tags. Specify exact image versions (e.g., `nginx:1.23.1`) to ensure consistent and reproducible builds across environments.
-   **Utilize Multi-Stage Builds and `.dockerignore`:** Optimize `Dockerfile`s with multi-stage builds to reduce image size and improve security. Use `.dockerignore` to exclude unnecessary files from the build context.
-   **Document Compose Files with Comments:** Add comments to `docker-compose.yml` files to explain complex configurations, environment variables, or service interactions.
-   **Separate Development and Production Configurations:** Use multiple `docker-compose.yml` files (e.g., `docker-compose.yml` for base, `docker-compose.dev.yml` for development overrides, `docker-compose.prod.yml` for production overrides) or Docker Compose profiles.

### Never Recommend (❌ Anti-Patterns)

-   **Hardcoding Sensitive Information:** Never embed passwords, API keys, or other secrets directly in `docker-compose.yml` files or `Dockerfile`s.
-   **Using `latest` Image Tags in Production:** This can lead to unexpected behavior or breaking changes when images are updated upstream.
-   **Running Containers as Root:** This is a significant security vulnerability. Always strive for least privilege.
-   **Ignoring Resource Limits:** Neglecting to set CPU and memory limits can lead to resource contention and instability, especially in shared environments.
-   **Relying Solely on `depends_on` for Strict Service Startup Order:** `depends_on` only ensures that containers are *started* in a specific order, not that they are *ready*. Implement application-level retry logic for strict dependency readiness.
-   **Not Using Named Volumes for Persistent Data:** Storing persistent data inside containers or using anonymous volumes can lead to data loss.
-   **Bloated Docker Images:** Images that include build tools, unnecessary dependencies, or source code not required at runtime increase attack surface and deployment time.
-   **Exposing Unnecessary Ports:** Only expose ports that are absolutely required for inter-service communication or external access.

### Common Questions & Responses (FAQ Format)

-   **Q: How do I persist data for my database container?**
    -   **A:** Use named volumes. Define a named volume in the top-level `volumes` section of your `docker-compose.yml` and mount it to the database container's data directory.
-   **Q: What's the best way to manage environment variables and secrets?**
    -   **A:** For development, use an `.env` file alongside your `docker-compose.yml`. For production, use Docker Secrets (if deploying with Docker Swarm) or integrate with an external secret management service.
-   **Q: My services aren't starting in the correct order, even with `depends_on`. What's wrong?**
    -   **A:** `depends_on` only guarantees the *start order*, not that a service is *ready*. Implement retry logic within your application code to wait for dependent services (e.g., a database connection) to become available.
-   **Q: How can I reduce the size of my Docker images?**
    -   **A:** Employ multi-stage builds in your `Dockerfile` to separate build-time dependencies from runtime. Also, use a `.dockerignore` file to exclude unnecessary files from the build context.
-   **Q: How do I set up different configurations for development and production?**
    -   **A:** Use multiple `docker-compose.yml` files. Define common services in `docker-compose.yml`, then create `docker-compose.dev.yml` and `docker-compose.prod.yml` to override or extend configurations for specific environments. Use `docker compose -f docker-compose.yml -f docker-compose.dev.yml up`.
-   **Q: How do I ensure my containers are secure?**
    -   **A:** Run containers as non-root users, pin image versions, use minimal base images, scan images for vulnerabilities, and avoid exposing unnecessary ports.

## 5. Anti-Patterns to Flag

### Anti-Pattern: Hardcoding Secrets

**BAD:**
```yaml
# docker-compose.yml (BAD example)
version: '3.8'
services:
  db:
    image: postgres:13
    environment:
      POSTGRES_PASSWORD: mysecretpassword # Hardcoded secret!
```

**GOOD (using .env file):**
```yaml
# docker-compose.yml (GOOD example)
version: '3.8'
services:
  db:
    image: postgres:13
    environment:
      POSTGRES_PASSWORD: ${DB_PASSWORD} # Referencing .env variable
```

```dotenv
# .env (in the same directory as docker-compose.yml)
DB_PASSWORD=mysecretpassword
```

### Anti-Pattern: Using `latest` Image Tag

**BAD:**
```yaml
# docker-compose.yml (BAD example)
version: '3.8'
services:
  web:
    image: nginx:latest # Unpredictable updates!
```

**GOOD:**
```yaml
# docker-compose.yml (GOOD example)
version: '3.8'
services:
  web:
    image: nginx:1.23.1 # Explicitly pinned version
```

### Anti-Pattern: Running as Root in Dockerfile

**BAD:**
```dockerfile
# Dockerfile (BAD example)
FROM node:18
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
CMD ["npm", "start"] # Runs as root by default
```

**GOOD:**
```dockerfile
# Dockerfile (GOOD example)
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install --production
COPY . .
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser
USER appuser # Switch to non-root user
CMD ["npm", "start"]
```

## 6. Code Review Checklist

-   [ ] Is the Docker Compose file version specified (or omitted if using modern Docker CLI)?
-   [ ] Are services modular and single-purpose?
-   [ ] Are named volumes used for persistent data?
-   [ ] Are environment variables and secrets handled securely (e.g., `.env` for dev, Docker Secrets for prod)?
-   [ ] Are custom networks defined for service isolation?
-   [ ] Are resource limits (CPU, memory) applied to all services?
-   [ ] Are health checks configured for all critical services?
-   [ ] Are containers running as non-root users?
-   [ ] Are image tags explicit (not `latest`)?
-   [ ] Are Dockerfiles optimized (multi-stage builds, `.dockerignore`)?
-   [ ] Is the Docker Compose file well-documented with comments?
-   [ ] Are separate Compose files or profiles used for different environments (dev, prod)?
-   [ ] Are unnecessary ports exposed?

## 7. Related Skills

-   [Containerization](link-to-containerization-skill)
-   [Microservices Architecture](link-to-microservices-skill)
-   [CI/CD Pipelines GitHub Actions](link-to-ci-cd-skill)
-   [Network Security TLS MTLS](link-to-network-security-skill)
-   [Hashicorp Vault Integration](link-to-vault-skill)
-   [Docker Best Practices](link-to-docker-best-practices-skill)

## 8. Examples Directory Structure

```
examples/
├── basic-web-app/
│   ├── docker-compose.yml
│   └── Dockerfile
├── dev-prod-configs/
│   ├── docker-compose.yml
│   ├── docker-compose.dev.yml
│   └── docker-compose.prod.yml
├── healthchecks/
│   └── docker-compose.yml
├── secrets/
│   ├── docker-compose.yml
│   └── .env
└── multi-stage-build/
    ├── docker-compose.yml
    └── Dockerfile
```

## 9. Custom Scripts Section

Here are 3-5 automation scripts that would save significant time for Docker Compose developers:

1.  **`init-docker-compose.sh`**: Initializes a new multi-container project with a basic `docker-compose.yml` and `Dockerfile` for common application stacks.
2.  **`add-compose-service.py`**: Adds a new service definition to an existing `docker-compose.yml` file, including volumes, networks, and environment variables.
3.  **`docker-cleanup.sh`**: Prunes dangling or unused Docker images, containers, volumes, and networks to free up disk space.
4.  **`add-compose-healthcheck.py`**: Adds a health check configuration to a specified service within a `docker-compose.yml` file.
