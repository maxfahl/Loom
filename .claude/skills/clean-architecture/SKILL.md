---
Name: clean-architecture
Version: 1.0.0
Category: Software Architecture / Design Patterns
Tags: clean architecture, hexagonal architecture, onion architecture, domain-driven design, ddd, typescript, software design, architecture
Description: A software design philosophy that separates the elements of a design into ring levels, ensuring maintainability, scalability, and testability.
---

## Skill Purpose

This skill enables Claude to understand, apply, and guide developers in implementing Clean Architecture, a software design philosophy that promotes building robust, maintainable, scalable, and testable applications. It emphasizes the separation of concerns by organizing code into independent layers, with dependencies flowing inwards. This approach ensures that core business logic remains isolated from external factors like UI, databases, or frameworks, making the system highly adaptable to change.

## When to Activate This Skill

Activate this skill when:
*   Designing new applications from scratch, especially those requiring long-term maintainability and adaptability.
*   Refactoring existing monolithic applications to improve modularity, testability, and scalability.
*   The user explicitly mentions terms like "Clean Architecture," "Hexagonal Architecture," "Onion Architecture," "Ports and Adapters," or "Domain-Driven Design (DDD)."
*   The project requirements emphasize high testability, independence from specific frameworks or databases, and clear separation of business logic.
*   Discussing architectural patterns for TypeScript applications.

## Core Knowledge

### Layers of Clean Architecture

Clean Architecture typically defines four main layers, visualized as concentric circles, where dependencies always flow inwards:

1.  **Entities (Domain Layer):**
    *   **Responsibility:** Encapsulate enterprise-wide business rules. These are the core business objects, often containing methods that embody critical business logic.
    *   **Independence:** Most independent layer. Does not depend on any other layer.
    *   **TypeScript:** Defined as interfaces, classes, or type aliases representing core domain concepts (e.g., `User`, `Product`).

2.  **Use Cases (Application Layer):**
    *   **Responsibility:** Contain application-specific business rules. They orchestrate the flow of data to and from the Entities, defining *what* the application does.
    *   **Independence:** Depends only on the Entities layer.
    *   **TypeScript:** Typically classes (Interactors/Services) that take input, interact with entities and repositories (via interfaces/ports), and produce output.

3.  **Interface Adapters (Infrastructure Layer):**
    *   **Responsibility:** Convert data from the Use Case layer into formats required by external systems (e.g., databases, web services, UI). This layer includes controllers, gateways, and presenters.
    *   **Independence:** Depends on Use Cases and Entities.
    *   **TypeScript:** Implementations of interfaces (ports) defined in the Use Case layer (e.g., `PostgreSQLUserRepository` implementing `IUserRepository`). Also includes DTOs (Data Transfer Objects) for data conversion.

4.  **Frameworks and Drivers (Presentation/External Layer):**
    *   **Responsibility:** The outermost layer, consisting of frameworks, tools, and external interfaces like the UI, database, or web servers (e.g., Express.js, React). These are considered "details" that the inner layers should not depend on.
    *   **Independence:** Depends on Interface Adapters, Use Cases, and Entities.
    *   **TypeScript:** Entry points (e.g., `main.ts`), UI components, API routes, database configurations.

### The Dependency Rule

The most crucial rule in Clean Architecture: **Dependencies must always flow inwards.** Inner circles should not know anything about outer circles. This is achieved through **Dependency Inversion**, where higher-level modules (inner layers) do not depend on lower-level modules (outer layers), but both depend on abstractions (interfaces).

### SOLID Principles Alignment

Clean Architecture strongly aligns with the SOLID principles, particularly:
*   **Single Responsibility Principle (SRP):** Each layer and component has a single, well-defined responsibility.
*   **Open/Closed Principle (OCP):** Software entities should be open for extension but closed for modification.
*   **Liskov Substitution Principle (LSP):** Subtypes must be substitutable for their base types.
*   **Interface Segregation Principle (ISP):** Clients should not be forced to depend on interfaces they do not use.
*   **Dependency Inversion Principle (DIP):** High-level modules should not depend on low-level modules. Both should depend on abstractions. Abstractions should not depend on details. Details should depend on abstractions.

### TypeScript's Role

TypeScript is an excellent fit for Clean Architecture due to its features that help enforce boundaries and contracts:
*   **Strong Static Typing:** Catches errors at compile time, improving reliability and acting as living documentation.
*   **Interfaces and Type Aliases:** Crucial for defining clear contracts (ports) between layers, enabling Dependency Inversion.
*   **Generics:** Allows for reusable, type-safe components that work across various types.
*   **Strict Type-Checking:** Features like `strictNullChecks` enhance code reliability.
*   **Modularity:** ES6 modules facilitate organizing code into smaller, reusable units.
*   **Dependency Injection (DI):** Using DI containers (e.g., `tsyringe`) helps manage dependencies and promotes testability.

### Key Concepts

*   **Entities:** Core business objects with enterprise-wide rules.
*   **Value Objects:** Immutable objects representing descriptive aspects of the domain.
*   **Aggregates:** Clusters of domain objects treated as a single unit for data changes.
*   **Repositories:** Abstractions for data persistence, defined as interfaces in the domain/application layer and implemented in the infrastructure layer.
*   **Use Cases (Interactors):** Application-specific business logic orchestrating entities and repositories.
*   **Ports & Adapters:** "Ports" are interfaces defined by inner layers, and "Adapters" are implementations of these interfaces in outer layers.
*   **Presenters:** Prepare data for the UI.
*   **Controllers:** Handle input from the UI/API and delegate to use cases.
*   **Gateways:** Interfaces for external services (e.g., payment gateways, email services).

## Key Guidance for Claude

### Always Recommend (✅ Best Practices)

*   **Prioritize Business Logic Independence:** Ensure that the core business rules (Entities and Use Cases) are completely unaware of external concerns like databases, UI frameworks, or third-party libraries.
*   **Define Clear Interfaces (Ports):** Use TypeScript interfaces to define the contracts for communication between layers. For example, `IUserRepository` in the Application layer, implemented by `PostgreSQLUserRepository` in the Infrastructure layer.
*   **Implement Adapters:** Create concrete implementations (adapters) in the outer layers that conform to the interfaces (ports) defined by the inner layers.
*   **Enforce Layer Boundaries with TypeScript:** Leverage TypeScript's type system, especially interfaces and strict mode, to explicitly define and enforce the boundaries and contracts between layers.
*   **Comprehensive Unit Testing:** Write thorough unit tests for each layer, particularly for Entities and Use Cases. Mock all external dependencies to ensure tests are fast, isolated, and reliable.
*   **Organize Code by Architectural Layers:** Structure the project directory to reflect the Clean Architecture layers (e.g., `src/domain`, `src/application`, `src/infrastructure`, `src/presentation`).
*   **Utilize Dependency Injection:** Employ a Dependency Injection (DI) container or manual DI to manage and provide dependencies, promoting loose coupling and testability.
*   **Use DTOs for Data Transfer:** Define Data Transfer Objects (DTOs) for input and output between layers (especially between Presentation/Infrastructure and Application) to prevent domain objects from leaking into external layers.

### Never Recommend (❌ Anti-Patterns)

*   **Violating the Dependency Rule:** Never allow an inner layer to directly import or depend on a module from an outer layer. This is the most critical anti-pattern.
*   **Mixing Business Logic with Framework Code:** Avoid embedding framework-specific code (e.g., Express.js route handlers, React component logic) directly within your Use Cases or Entities.
*   **Tight Coupling:** Do not create direct concrete dependencies between layers. Always rely on abstractions (interfaces) for inter-layer communication.
*   **Skipping Interface Definitions:** Do not omit defining interfaces (ports) for services or repositories. This undermines Dependency Inversion and testability.
*   **Direct Database/External Service Access:** Use Cases or Entities should never directly interact with a database client, API client, or any other external service. Always go through a repository or gateway interface.
*   **Leaking Domain Objects:** Do not pass domain entities directly to the Presentation or Infrastructure layers. Convert them to DTOs to maintain encapsulation and prevent unintended modifications.

### Common Questions & Responses

*   **Q: "How should I structure my project directories for Clean Architecture?"**
    *   **A:** A common structure is `src/domain`, `src/application`, `src/infrastructure`, `src/presentation`. Each folder corresponds to a layer, containing its specific components (e.g., `domain/entities`, `application/use-cases`, `infrastructure/persistence`, `presentation/controllers`).
*   **Q: "Where does my database code go?"**
    *   **A:** Database *implementations* (e.g., `PostgreSQLUserRepository`) belong in the `infrastructure/persistence` (or `interface-adapters/persistence`) layer. The *interfaces* (e.g., `IUserRepository`) that these implementations adhere to should be defined in the `domain` or `application` layer.
*   **Q: "How do I handle UI or framework-specific logic (e.g., Express.js routes, React components)?"**
    *   **A:** These belong in the `presentation` (or `frameworks-and-drivers`) layer. They should interact with the `application` layer through controllers or presenters, which in turn call use cases. The UI/framework code should adapt to the application's interfaces, not the other way around.
*   **Q: "What about shared models or DTOs?"**
    *   **A:** Core domain entities should reside in the `domain` layer. DTOs (Data Transfer Objects) used for input/output between layers can be defined within the `application` layer (for use case inputs/outputs) or `interface-adapters` layer (for API request/response bodies).
*   **Q: "How do I handle cross-cutting concerns like logging or authentication?"**
    *   **A:** These are typically handled as "aspects" or "middleware" in the outer layers (e.g., Presentation or Infrastructure). They should wrap the calls to the inner layers without the inner layers being aware of them. Interfaces for logging or authentication services can be defined in inner layers and implemented in outer layers.

## Anti-Patterns to Flag

### Anti-Pattern: Direct Infrastructure Dependency in Application Layer

**BAD Example:**
```typescript
// src/application/use-cases/create-user.ts
import { User } from '../../domain/entities/user';
import { UserRepository } from '../../infrastructure/persistence/user-repository'; // ❌ Direct dependency on infrastructure

export class CreateUserUseCase {
  constructor(private userRepository: UserRepository) {} // ❌ Concrete dependency

  async execute(name: string, email: string): Promise<User> {
    const user = new User(name, email);
    await this.userRepository.save(user);
    return user;
  }
}
```

**GOOD Example:**
```typescript
// src/application/ports/user-repository.ts
import { User } from '../../domain/entities/user';

export interface IUserRepository {
  save(user: User): Promise<User>;
  findByEmail(email: string): Promise<User | null>;
}

// src/application/use-cases/create-user.ts
import { User } from '../../domain/entities/user';
import { IUserRepository } from '../ports/user-repository'; // ✅ Dependency on abstraction

export class CreateUserUseCase {
  constructor(private userRepository: IUserRepository) {} // ✅ Dependency on interface

  async execute(name: string, email: string): Promise<User> {
    const user = new User(name, email);
    await this.userRepository.save(user);
    return user;
  }
}

// src/infrastructure/persistence/postgresql-user-repository.ts
import { Pool } from 'pg'; // Example database client
import { User } from '../../domain/entities/user';
import { IUserRepository } from '../../application/ports/user-repository'; // ✅ Implements interface from inner layer

export class PostgreSQLUserRepository implements IUserRepository {
  constructor(private pool: Pool) {}

  async save(user: User): Promise<User> {
    // ... database logic ...
    return user;
  }

  async findByEmail(email: string): Promise<User | null> {
    // ... database logic ...
    return null;
  }
}
```

## Code Review Checklist

*   [ ] **Dependency Rule Adherence:** Verify that no inner layer directly imports or depends on an outer layer. All dependencies should flow inwards.
*   [ ] **Interface-Based Communication:** Check if all interactions between layers (especially from Application to Infrastructure) are done through interfaces (ports) defined in the inner layers.
*   [ ] **Business Logic Purity:** Ensure that the `domain` and `application` layers contain pure business logic, free from any framework-specific code, database queries, or UI concerns.
*   [ ] **Testability:** Can entities and use cases be unit tested in isolation without requiring a database or web server? Are dependencies mocked effectively?
*   [ ] **TypeScript Enforcement:** Is TypeScript used to define clear types and interfaces for all data structures and contracts between layers? Is strict mode enabled and adhered to?
*   [ ] **Separation of Concerns:** Is each file and module focused on a single responsibility? Are concerns clearly separated across layers?
*   [ ] **DTO Usage:** Are DTOs used appropriately for data transfer between layers, preventing domain objects from being exposed unnecessarily?
*   [ ] **Dependency Injection:** Is dependency injection used consistently to provide concrete implementations to higher-level modules?

## Related Skills

*   `typescript-strict-mode`: For enforcing strong typing and code quality.
*   `tdd-red-green-refactor`: For developing test-driven components within each layer.
*   `rest-api-design`: For designing the presentation layer (controllers, DTOs).
*   `jest-unit-tests`: For writing effective unit and integration tests for each layer.
*   `python-type-hints`: (If working with Python) for similar type enforcement.

## Examples Directory Structure

```
.devdev/skills/clean-architecture/examples/
├── user-management/
│   ├── domain/
│   │   ├── entities/
│   │   │   └── user.ts
│   │   └── value-objects/
│   │       └── email.ts
│   ├── application/
│   │   ├── use-cases/
│   │   │   ├── create-user.ts
│   │   │   └── get-user-by-email.ts
│   │   ├── ports/
│   │   │   └── user-repository.ts
│   │   └── dtos/
│   │       ├── create-user-dto.ts
│   │       └── user-response-dto.ts
│   ├── infrastructure/
│   │   ├── persistence/
│   │   │   ├── postgresql-user-repository.ts
│   │   │   └── in-memory-user-repository.ts
│   │   ├── services/
│   │   │   └── email-service.ts
│   │   └── config/
│   │       └── database.ts
│   └── presentation/
│       ├── controllers/
│       │   └── user-controller.ts
│       ├── routes/
│       │   └── user-routes.ts
│       └── middlewares/
│           └── auth-middleware.ts
└── product-catalog/
    ├── domain/
    │   └── entities/
    │       └── product.ts
    └── application/
        └── use-cases/
            └── create-product.ts
```

## Custom Scripts Section ⭐ NEW

Here are 3 automation scripts designed to address common pain points when working with Clean Architecture in TypeScript projects.

### 1. `generate-clean-layer.sh`

**Description:** This script automates the creation of new files within a specified Clean Architecture layer (e.g., `domain`, `application`, `infrastructure`, `presentation`). It creates the necessary folder structure and boilerplate files (e.g., an interface, a class, a use case) based on the layer and component type. This saves significant time and ensures consistency.

### 2. `validate-dependency-rule.py`

**Description:** This Python script scans the codebase to ensure that the Clean Architecture dependency rule is not violated. It identifies instances where an inner layer directly imports or depends on a module from an outer layer, which is a critical anti-pattern. This helps maintain architectural integrity over time.

### 3. `generate-use-case.sh`

**Description:** This script streamlines the creation of a new use case (interactor) within the application layer. It generates the use case class, its corresponding input/output DTOs, and an interface for its dependencies (e.g., a repository port). This automates the repetitive setup involved in adding new application features.
