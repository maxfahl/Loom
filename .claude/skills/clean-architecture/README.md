# Clean Architecture Skill

This skill provides comprehensive guidance and tools for implementing Clean Architecture in TypeScript projects. It emphasizes building maintainable, scalable, and testable applications by strictly separating concerns into distinct layers.

## Key Concepts Covered:

*   **Layered Architecture:** Understanding the roles of Entities, Use Cases, Interface Adapters, and Frameworks & Drivers.
*   **Dependency Rule:** Ensuring dependencies always flow inwards.
*   **SOLID Principles:** How Clean Architecture aligns with fundamental design principles.
*   **TypeScript Best Practices:** Leveraging TypeScript for strong typing, interfaces, and modularity to enforce architectural boundaries.
*   **Core Components:** Detailed explanations of Entities, Value Objects, Repositories, Use Cases (Interactors), Ports & Adapters, and more.

## When to Use This Skill:

*   Starting a new project that requires a robust and evolvable architecture.
*   Refactoring existing codebases to improve maintainability and testability.
*   When discussing architectural patterns, dependency management, and separation of concerns.

## Included Tools & Resources:

*   **`SKILL.md`:** Detailed instructions, best practices, anti-patterns, and code review checklists.
*   **`examples/`:** Practical TypeScript code examples demonstrating Clean Architecture principles.
*   **`scripts/`:** Automation scripts to streamline common development tasks (e.g., generating layers, validating dependencies, creating use cases).

## Automation Scripts:

1.  **`generate-clean-layer.sh`:** Quickly scaffold new components within any Clean Architecture layer.
2.  **`validate-dependency-rule.py`:** Automatically check for and report violations of the Clean Architecture dependency rule.
3.  **`generate-use-case.sh`:** Generate boilerplate for new use cases, including DTOs and repository interfaces.

This skill aims to empower developers to build high-quality, adaptable software systems using Clean Architecture principles with TypeScript.
