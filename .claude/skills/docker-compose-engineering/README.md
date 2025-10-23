# Docker Compose Engineering Skill Package

This package provides comprehensive guidance and automation tools for defining and running multi-container Docker applications using Docker Compose.

## Overview

Docker Compose is a powerful tool for defining and running multi-container Docker applications. With a single YAML file, you can configure your application's services, networks, and volumes, and then spin up your entire environment with a single command. This skill package focuses on best practices for building robust, scalable, and maintainable Docker Compose configurations.

## Contents

-   **`SKILL.md`**: The main instruction file for Claude, detailing core knowledge, best practices, anti-patterns, and code review checklists specific to Docker Compose.
-   **`examples/`**: A directory containing practical `docker-compose.yml` and `Dockerfile` examples demonstrating various Docker Compose features and patterns.
-   **`patterns/`**: A directory for common Docker Compose architectural and configuration patterns.
-   **`scripts/`**: A collection of automation scripts to streamline common Docker Compose development tasks, such as project initialization, service addition, and resource cleanup.
-   **`README.md`**: This human-readable documentation.

## Getting Started

Refer to the `SKILL.md` for detailed guidance on Docker Compose engineering. Explore the `examples/` directory for practical implementations and utilize the `scripts/` to automate your workflow.

## Automation Scripts

The `scripts/` directory contains the following utilities:

-   **`init-docker-compose.sh`**: Initializes a new multi-container project with a basic `docker-compose.yml` and `Dockerfile` for common application stacks.
-   **`add-compose-service.py`**: Adds a new service definition to an existing `docker-compose.yml` file.
-   **`docker-cleanup.sh`**: Prunes dangling or unused Docker images, containers, volumes, and networks.
-   **`add-compose-healthcheck.py`**: Adds a health check configuration to a specified service within a `docker-compose.yml` file.

Each script includes detailed usage instructions and examples within its file.
