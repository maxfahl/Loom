# Contract Testing Skill

This directory contains the Claude Skill package for **Contract Testing**.

Contract testing is a technique for testing an integration point between two separate services (e.g., a client and an API) by checking that each service in isolation adheres to a shared understanding of the interaction (a contract).

This skill provides Claude with the knowledge, best practices, and tools to effectively implement and manage contract tests, primarily focusing on Consumer-Driven Contracts (CDC) using Pact and OpenAPI in TypeScript environments.

## Contents:

*   `SKILL.md`: The main instruction file for Claude, detailing the purpose, core knowledge, guidance, anti-patterns, and more.
*   `examples/`: Contains practical code examples demonstrating consumer-side Pact tests, provider-side verification, and OpenAPI specifications.
*   `patterns/`: Directory for common contract testing patterns and strategies.
*   `scripts/`: Automation scripts to streamline common contract testing workflows.
*   `README.md`: This human-readable documentation.

## Key Features:

*   **Consumer-Driven Contracts (CDC):** Emphasizes the consumer's perspective in defining API interactions.
*   **Pact Framework:** Guidance on using Pact-JS for robust contract testing in TypeScript.
*   **OpenAPI Integration:** Leveraging OpenAPI for API definition and TypeScript type generation.
*   **CI/CD Best Practices:** Integrating contract tests into automated pipelines with Pact Broker.
*   **Practical Examples:** Real-world code snippets and project structure.
*   **Automation Scripts:** Time-saving scripts for generating tests, updating types, and managing verification/publishing.

## Getting Started (for humans):

To understand how Claude will utilize this skill, refer to the `SKILL.md` file. For practical examples and automation, explore the `examples/` and `scripts/` directories.
