# Docker Engineering Skill

This package provides Claude with the necessary knowledge and tools to effectively work with Docker, focusing on best practices for image optimization, security, and efficient container management.

## Key Features:

*   **Optimized Dockerfiles**: Guidance on creating lean and secure Docker images using multi-stage builds, minimal base images, and proper `.dockerignore` usage.
*   **Container Orchestration**: Best practices for local development with Docker Compose.
*   **Security**: Emphasizes running as non-root, secure secret management, and vulnerability scanning.
*   **Automation Scripts**: A set of scripts to automate common Docker tasks, including image analysis, Docker Compose setup, and resource cleanup.

## Contents:

*   `SKILL.md`: The main instruction file for Claude, detailing core knowledge, best practices, and anti-patterns.
*   `examples/`: Directory containing example Dockerfiles and Docker Compose configurations.
*   `patterns/`: Directory for common Docker patterns and solutions.
*   `scripts/`: Automation scripts to streamline Docker workflows.
*   `README.md`: This human-readable overview of the skill.

## Automation Scripts Included:

1.  `docker-image-analyzer.sh`: Analyzes Dockerfiles for best practices and suggests optimizations.
2.  `docker-compose-init.py`: Interactively generates `docker-compose.yaml` files for various project types.
3.  `docker-prune-all.sh`: Safely cleans up unused Docker resources.
4.  `docker-secret-template.py`: Generates `.env.template` files from Dockerfiles or Docker Compose configurations.

For detailed instructions and examples, refer to `SKILL.md`.
