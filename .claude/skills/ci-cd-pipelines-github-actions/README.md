# CI/CD Pipelines (GitHub Actions) Skill

This skill provides comprehensive guidance and tools for implementing and managing Continuous Integration (CI) and Continuous Deployment (CD) pipelines using GitHub Actions. It focuses on best practices for security, efficiency, and maintainability, enabling developers to automate their software delivery processes effectively.

## What this Skill Covers

*   **Fundamentals of GitHub Actions**: Understanding workflows, events, jobs, steps, and actions.
*   **Security Best Practices**: How to secure your CI/CD pipelines against common vulnerabilities, including proper secret management, least privilege principles, and action pinning.
*   **Performance Optimization**: Strategies to speed up your workflows, such as dependency caching, parallel job execution, and path filtering.
*   **Maintainability**: Guidance on creating modular, reusable, and easy-to-manage workflows.
*   **TypeScript Integration**: Specific examples and patterns for building and testing TypeScript projects.
*   **Automation Scripts**: A set of utility scripts to streamline common GitHub Actions tasks.

## Getting Started

To leverage this skill, refer to the `SKILL.md` for detailed knowledge and guidance. Explore the `examples/` directory for practical workflow configurations and utilize the `scripts/` for automating various CI/CD tasks.

## Directory Structure

*   `SKILL.md`: The main instruction file for Claude, detailing core knowledge, best practices, and anti-patterns.
*   `examples/`: Contains example GitHub Actions workflow files (`.yaml`) demonstrating various CI/CD patterns.
*   `patterns/`: (Currently empty, but reserved for future common workflow patterns or reusable components).
*   `scripts/`: Automation scripts to assist with GitHub Actions development and maintenance.
*   `README.md`: This human-readable overview of the skill.

## Automation Scripts

The `scripts/` directory contains the following utilities:

*   `generate_ci_workflow.py`: A Python script to generate a basic CI workflow for a TypeScript project.
*   `rotate_secret.py`: A Python script to securely rotate GitHub repository secrets.
*   `validate_workflow.sh`: A Bash script to locally validate GitHub Actions workflow files using `act`.

## Contribution

Contributions are welcome! If you have additional best practices, examples, or automation scripts related to GitHub Actions CI/CD, please consider contributing to this skill.
