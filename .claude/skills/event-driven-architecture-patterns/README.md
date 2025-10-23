# Event-Driven Architecture Patterns Skill

This directory contains a Claude skill package focused on Event-Driven Architecture (EDA) patterns. It provides Claude with the knowledge, best practices, anti-patterns, and automation scripts necessary to design, implement, and maintain scalable and resilient event-driven systems, particularly using TypeScript.

## What is Event-Driven Architecture?

Event-Driven Architecture is a software design paradigm where components communicate asynchronously by producing and consuming events. This approach promotes loose coupling, enhanced scalability, and improved resilience, making it ideal for modern distributed systems and microservices.

## Key Features of this Skill:

*   **Core Concepts**: Understanding of events, producers, consumers, and event brokers.
*   **Key Patterns**: Detailed guidance on Publisher-Subscriber, Event Sourcing, CQRS, Saga Pattern, Outbox Pattern, and Dead Letter Queues.
*   **TypeScript Best Practices**: Specific recommendations for implementing EDA with TypeScript, including strong typing, strict mode, and generics.
*   **Anti-Patterns**: Identification and examples of common pitfalls to avoid in EDA.
*   **Code Review Checklist**: A comprehensive list to ensure high-quality EDA implementations.
*   **Automation Scripts**: Practical scripts to streamline common development tasks related to event schema generation, consumer boilerplate creation, event replaying, and DLQ processing.

## Directory Structure:

*   `SKILL.md`: The main instruction file for Claude, containing detailed knowledge and guidance.
*   `examples/`: Contains concrete TypeScript code examples demonstrating various EDA patterns.
*   `patterns/`: Stores reusable code patterns or utility types relevant to EDA.
*   `scripts/`: Houses automation scripts to assist with EDA development workflows.
*   `README.md` (this file): A human-readable overview of the skill package.

## Getting Started with the Scripts:

The `scripts/` directory contains several utilities to help you with EDA development. Refer to the `SKILL.md` for detailed descriptions and usage instructions for each script.

## Contributing:

Contributions to enhance this skill package are welcome. Please refer to the `SKILL.md` for guidelines on adding new patterns, examples, or improving existing content.
