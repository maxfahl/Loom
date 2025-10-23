# Containerization (Docker/Docker Compose) Skill

This skill provides comprehensive guidance and tools for effectively using Docker and Docker Compose to containerize applications. It covers best practices for image creation, container security, efficient development workflows, and deployment strategies.

## Key Concepts:

*   **Docker Fundamentals**: Dockerfile syntax, image layers, volumes, networks.
*   **Docker Compose**: Multi-service application definition, healthchecks, environment management.
*   **Image Optimization**: Multi-stage builds, lightweight base images, `.dockerignore`.
*   **Container Security**: Non-root users, read-only filesystems, secret management, vulnerability scanning.
*   **Development Workflows**: Local setup, hot-reloading, CI/CD integration.

## Included Scripts:

This skill includes several automation scripts to streamline containerization workflows:

*   `docker-image-analyzer.sh`: Analyze Docker image size, layers, and potential issues.
*   `generate-docker-compose-env.py`: Generate `.env` files for Docker Compose.
*   `docker-cleanup.sh`: Clean up old Docker resources.
*   `docker-healthcheck-tester.py`: Test Docker Compose healthchecks locally.

For detailed information on how to use this skill and its components, refer to `SKILL.md`.