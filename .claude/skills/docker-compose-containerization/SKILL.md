---
name: docker-compose-containerization
version: 1.0.0
category: Containerization / Orchestration
tags: docker, docker-compose, container, orchestration, microservices, development, deployment
description: Enables Claude to effectively use Docker Compose for multi-container application development and deployment.
---

# Docker Compose Containerization Skill

## 1. Skill Purpose

This skill enables Claude to understand, generate, and troubleshoot `docker-compose.yml` configurations for defining and running multi-container Docker applications. It covers best practices for local development environments, testing, and preparing applications for deployment.

## 2. When to Activate This Skill

Activate this skill when the user's request involves:
- Setting up a multi-service application using Docker.
- Defining inter-service dependencies and networking.
- Persisting data with volumes.
- Managing environment variables and secrets for Dockerized applications.
- Orchestrating local development environments.
- Troubleshooting Docker Compose configurations.
- Keywords: `docker-compose`, `multi-container`, `orchestration`, `service definition`, `local development environment`, `docker services`, `docker volumes`, `docker networks`.

## 3. Core Knowledge

Claude needs to understand the following fundamental concepts and components of Docker Compose:

### `docker-compose.yml` Structure
- **`version`**: Specifies the Compose file format version (prefer `3.8` or later for modern features).
- **`services`**: Defines the individual containers that make up your application.
  - `build`: Context and Dockerfile path.
  - `image`: Pre-built Docker image.
  - `ports`: Port mapping (host:container).
  - `volumes`: Data persistence and bind mounts.
  - `environment`: Environment variables.
  - `env_file`: Path to environment variable files.
  - `depends_on`: Service startup order (for dependency resolution).
  - `networks`: Custom network assignments.
  - `healthcheck`: Define how to check if a container is healthy.
  - `restart`: Restart policy.
  - `command` / `entrypoint`: Override default commands.
  - `secrets`: Securely manage sensitive data.
  - `configs`: External configuration files.
  - `deploy`: Deployment configuration (for Swarm mode).
  - `resources`: CPU/memory limits.
- **`volumes`**: Defines named volumes for data persistence.
- **`networks`**: Defines custom bridge networks for inter-service communication.
- **`configs`**: Defines external configuration sources.
- **`secrets`**: Defines external secret sources.

### Key Docker Compose Commands
- `docker compose up [-d] [--build]`: Builds, (re)creates, starts, and attaches to containers for a service. `-d` for detached mode, `--build` to force rebuild images.
- `docker compose down [--volumes] [--rmi all]`: Stops and removes containers, networks, and optionally volumes and images.
- `docker compose build`: Builds or rebuilds services.
- `docker compose ps`: Lists containers.
- `docker compose logs [-f]`: Displays log output from services.
- `docker compose exec <service> <command>`: Executes a command in a running container.
- `docker compose config`: Validates and views the Compose file configuration.

## 4. Key Guidance for Claude

### Always Recommend (✅ Best Practices)

- ✅ **Use named volumes for data persistence**: This decouples data from containers, making it easier to manage and backup.
- ✅ **Define custom networks**: Explicitly define bridge networks for better isolation and clearer communication paths between services. Avoid relying on the default network.
- ✅ **Utilize `.env` files for environment variables**: Separate sensitive or environment-specific variables from `docker-compose.yml`. Use `env_file` in your service definitions.
- ✅ **Implement health checks**: Ensure services are truly ready before dependent services start interacting with them. This prevents race conditions.
- ✅ **Separate development and production configurations**: Use multiple Compose files (e.g., `docker-compose.yml` for common, `docker-compose.dev.yml` for development overrides, `docker-compose.prod.yml` for production overrides).
- ✅ **Pin image versions**: Avoid `latest` tag in production to ensure reproducible builds.
- ✅ **Optimize Dockerfile builds**: Leverage build cache, multi-stage builds, and `.dockerignore` to create smaller, more efficient images.
- ✅ **Set resource limits (CPU/Memory)**: Especially important for production environments to prevent resource exhaustion.
- ✅ **Use `depends_on` for service startup order**: While it doesn't wait for health, it ensures services are started in a specific sequence. Combine with health checks for true readiness.
- ✅ **Securely manage secrets**: Use Docker Secrets or external secret management tools (e.g., HashiCorp Vault) instead of environment variables for sensitive data in production.

### Never Recommend (❌ Anti-Patterns)

- ❌ **Hardcoding sensitive information**: Never embed API keys, database passwords, or other secrets directly in `docker-compose.yml` or Dockerfiles.
- ❌ **Exposing unnecessary ports**: Only expose ports that need to be accessible from the host or other external services.
- ❌ **Using `latest` tag in production**: This can lead to unexpected behavior when the `latest` image is updated.
- ❌ **Building large, monolithic images**: Break down applications into smaller, single-responsibility services.
- ❌ **Ignoring build context**: Ensure your `.dockerignore` file is properly configured to exclude unnecessary files from the build context.
- ❌ **Relying solely on `depends_on` for service readiness**: `depends_on` only ensures startup order, not that the service is fully initialized and ready to accept connections. Always combine with health checks.
- ❌ **Using `host` network mode indiscriminately**: While useful in some cases, it breaks network isolation and can lead to port conflicts.

### Common Questions & Responses (FAQ Format)

- **Q: How do I persist data for my database container?**
  - **A:** Use a named volume. Define it in the `volumes` section and mount it to the database container's data directory.
    ```yaml
    # docker-compose.yml
    services:
      db:
        image: postgres:16
        volumes:
          - db_data:/var/lib/postgresql/data
    volumes:
      db_data:
    ```
- **Q: My services can't communicate with each other. What's wrong?**
  - **A:** Ensure they are on the same custom network. Define a `networks` section and assign services to it. Services can then refer to each other by their service names.
    ```yaml
    # docker-compose.yml
    services:
      web:
        image: my-web-app
        networks:
          - my_app_network
      api:
        image: my-api
        networks:
          - my_app_network
    networks:
      my_app_network:
        driver: bridge
    ```
- **Q: How do I manage environment variables for different environments (dev, prod)?**
  - **A:** Use multiple Compose files. A base `docker-compose.yml` for common configurations, and `docker-compose.dev.yml` or `docker-compose.prod.yml` for environment-specific overrides. Use `docker compose -f docker-compose.yml -f docker-compose.dev.yml up`.
- **Q: My application starts, but the database isn't ready yet, causing errors.**
  - **A:** Implement a `healthcheck` for your database service. Your application service can then use a wait-for-it script or similar mechanism to ensure the database is healthy before attempting to connect.
    ```yaml
    # docker-compose.yml
    services:
      db:
        image: postgres:16
        healthcheck:
          test: ["CMD-SHELL", "pg_isready -U postgres"]
          interval: 5s
          timeout: 5s
          retries: 5
      app:
        image: my-app
        depends_on:
          db:
            condition: service_healthy # Requires Compose V2.2+
    ```

## 5. Anti-Patterns to Flag

### Anti-Pattern: Hardcoding Secrets

**BAD:**
```yaml
# docker-compose.yml
services:
  db:
    image: postgres:16
    environment:
      POSTGRES_PASSWORD: mysecretpassword123 # ❌ Hardcoded secret
```

**GOOD:**
```yaml
# .env
POSTGRES_PASSWORD=mysecurepassword456

# docker-compose.yml
services:
  db:
    image: postgres:16
    env_file:
      - .env # ✅ Use .env file
```
For production, consider Docker Secrets or external secret management.

### Anti-Pattern: Relying on Default Network and `latest` Tag

**BAD:**
```yaml
# docker-compose.yml
services:
  web:
    image: my-web-app:latest # ❌ Using latest tag
    ports:
      - "80:80"
  api:
    image: my-api:latest # ❌ Using latest tag
    # No explicit network, relies on default bridge network
```

**GOOD:**
```yaml
# docker-compose.yml
services:
  web:
    image: my-web-app:1.2.0 # ✅ Pin specific version
    ports:
      - "80:80"
    networks:
      - app_network # ✅ Custom network
  api:
    image: my-api:2.1.5 # ✅ Pin specific version
    networks:
      - app_network # ✅ Custom network

networks:
  app_network:
    driver: bridge
```

## 6. Code Review Checklist

- [ ] Are all sensitive environment variables loaded from `.env` files or Docker Secrets?
- [ ] Are named volumes used for all persistent data?
- [ ] Are custom networks defined and used for inter-service communication?
- [ ] Are health checks implemented for critical services (e.g., databases, message queues)?
- [ ] Are specific image versions pinned instead of `latest`?
- [ ] Is there a clear separation between development and production configurations (if applicable)?
- [ ] Is the `.dockerignore` file optimized to reduce build context size?
- [ ] Are resource limits (CPU/Memory) defined for production services?
- [ ] Are `depends_on` and health checks used together for robust service startup?
- [ ] Are unnecessary ports exposed?

## 7. Related Skills

- `containerization-docker-compose` (This skill)
- `docker-engineering`
- `microservices-architecture`
- `ci-cd-pipelines-github-actions` (for deploying Docker Compose apps)
- `nodejs-express-nestjs-development` (for Dockerizing Node.js apps)
- `python-django-flask-development` (for Dockerizing Python apps)

## 8. Examples Directory Structure

```
examples/
├── docker-compose.yml             # Base configuration
├── docker-compose.dev.yml         # Development overrides
├── docker-compose.prod.yml        # Production overrides
├── .env.example                   # Example environment variables
├── web-app/
│   ├── Dockerfile
│   ├── package.json
│   └── src/
│       └── index.ts
├── api-service/
│   ├── Dockerfile
│   ├── package.json
│   └── src/
│       └── app.ts
└── db/
    └── init.sql                   # Database initialization script
```

## 9. Custom Scripts Section

Here are 3-5 automation scripts designed to streamline common Docker Compose workflows and address developer pain points.

### Script 1: `compose-init.sh` - Initialize Docker Compose Project

**Purpose:** Quickly sets up a new multi-service Docker Compose project with a basic structure, including a `docker-compose.yml`, `.env`, and example service directories (e.g., a Node.js web app and a PostgreSQL database).

**Pain Point Solved:** Reduces the manual boilerplate setup for new projects, ensuring a consistent starting point.

### Script 2: `compose-env-sync.py` - Synchronize .env with Compose File

**Purpose:** Analyzes a `docker-compose.yml` file to identify all environment variables used and compares them against a `.env` file. It can generate a `.env.example` or report missing variables, ensuring consistency across environments.

**Pain Point Solved:** Prevents issues caused by missing or inconsistent environment variables, especially in team environments or CI/CD pipelines.

### Script 3: `compose-cleanup.sh` - Clean Up Docker Resources

**Purpose:** Provides a convenient way to clean up stopped Docker Compose containers, dangling images, unused volumes, and networks, either for a specific project or globally.

**Pain Point Solved:** Frees up disk space and prevents resource clutter from old or failed Docker Compose runs.

### Script 4: `compose-health-monitor.py` - Monitor Service Health

**Purpose:** Continuously monitors the health status of all services defined in a `docker-compose.yml` file. It reports the status and can optionally display logs for unhealthy services, providing quick insights into application readiness.

**Pain Point Solved:** Simplifies debugging and verification of multi-service applications during development and testing, avoiding manual `docker compose ps` and `docker compose logs` commands.
