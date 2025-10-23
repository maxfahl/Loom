# Java DropWizard Framework Skill

This directory contains the Claude Skill package for the Java DropWizard Framework.
It provides comprehensive guidance, best practices, and automation scripts to assist
in developing, testing, and deploying high-performance RESTful microservices using DropWizard.

## Package Structure:

- `SKILL.md`: The main instruction file detailing the skill's purpose, core knowledge,
  guidance, anti-patterns, and code review checklist.
- `examples/`: (Planned) Directory for code examples demonstrating DropWizard features.
- `patterns/`: (Planned) Directory for common DropWizard design patterns.
- `scripts/`: Automation scripts to streamline common development tasks.
- `README.md`: This human-readable documentation.

## Automation Scripts:

The `scripts/` directory contains the following utility scripts:

1.  **`create-dropwizard-project.sh`**
    - **Description:** Automates the creation of a new DropWizard project using the Maven archetype.
      It prompts for project details (Group ID, Artifact ID, Version, Package) and then executes
      the `mvn archetype:generate` command. This script saves time by providing a guided setup
      and handling the Maven command.
    - **Usage Example:**
      ```bash
      ./scripts/create-dropwizard-project.sh
      ./scripts/create-dropwizard-project.sh --group-id com.mycompany --artifact-id my-new-service
      ```

2.  **`generate-resource.sh`**
    - **Description:** Generates boilerplate code for a new DropWizard JAX-RS resource, its
      corresponding data representation (POJO), and basic test stubs. This automates the
      repetitive task of setting up new API endpoints.
    - **Usage Example:**
      ```bash
      ./scripts/generate-resource.sh --name User --package com.example.my_app
      ```

3.  **`build-and-dockerize.sh`**
    - **Description:** Automates the process of building a DropWizard application into a fat JAR
      and then creating a Docker image for it. This streamlines the build and containerization
      steps for deployment.
    - **Usage Example:**
      ```bash
      ./scripts/build-and-dockerize.sh
      ./scripts/build-and-dockerize.sh --project-dir /path/to/my-dropwizard-service --tag my-registry/my-service:v1.0.0
      ```

4.  **`run-tests-with-containers.sh`**
    - **Description:** Automates the execution of DropWizard tests, particularly focusing on
      integration tests that might leverage Testcontainers. It ensures a consistent way to run
      tests and provides guidance for Testcontainers setup.
    - **Usage Example:**
      ```bash
      ./scripts/run-tests-with-containers.sh
      ./scripts/run-tests-with-containers.sh --skip-unit-tests --clean-containers
      ```

5.  **`deploy-to-kubernetes.py`**
    - **Description:** Generates basic Kubernetes Deployment and Service YAML configurations for a
      DropWizard application. It can optionally apply these configurations to a Kubernetes cluster
      using `kubectl`.
    - **Usage Example:**
      ```bash
      ./scripts/deploy-to-kubernetes.py --app-name my-dropwizard-api --image my-registry/my-dropwizard-api:1.0.0
      ./scripts/deploy-to-kubernetes.py --app-name user-service --image my-registry/user-service:latest --apply
      ```

## How to Use This Skill:

Refer to the `SKILL.md` file for detailed instructions on how Claude can leverage this skill
to assist with DropWizard development tasks. The scripts in the `scripts/` directory are designed
to be run directly from your terminal within a DropWizard project context.
