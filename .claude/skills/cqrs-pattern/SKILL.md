---
Name: cqrs-pattern
Version: 1.0.0
Category: Architectural Patterns / Backend
Tags: CQRS, Event Sourcing, TypeScript, Architecture, Domain-Driven Design
Description: Enables robust, scalable, and maintainable applications by separating command and query responsibilities.
---

# CQRS Pattern

## 1. Skill Purpose

The Command Query Responsibility Segregation (CQRS) pattern separates the operations that change data (Commands) from the operations that read data (Queries). This architectural separation allows for independent optimization, scaling, and evolution of the read and write sides of an application. It is particularly beneficial in complex domains where read and write workloads differ significantly, or where auditability and historical data are crucial. By leveraging TypeScript, CQRS implementations gain enhanced maintainability and reduced errors through strong typing.

## 2. When to Activate This Skill

Activate this skill when the user's request involves:
*   Designing a scalable application architecture.
*   Handling complex domain logic with distinct read and write concerns.
*   Implementing Event Sourcing.
*   Optimizing performance for read-heavy or write-heavy workloads independently.
*   The need for a clear audit trail or historical data.
*   Keywords: "CQRS", "Command Query Responsibility Segregation", "scalable architecture", "event sourcing", "complex domain logic", "separate read/write models", "eventual consistency".

## 3. Core Knowledge

Claude needs to understand the following fundamental concepts related to CQRS:

*   **Commands**:
    *   Represent an intent to change the state of the system (e.g., `CreateUserCommand`, `UpdateProductPriceCommand`).
    *   Are imperative, past-tense, and contain all necessary data to perform the action.
    *   Do not return data, only an indication of success or failure.
    *   Should be immutable.
*   **Command Handlers**:
    *   Receive commands, validate them, apply business logic (often by interacting with an Aggregate Root), and update the Write Model.
    *   Should be simple, focused, and typically deal with a single Aggregate.
    *   May publish Domain Events after successful processing.
*   **Queries**:
    *   Represent a request for data (e.g., `GetUserByIdQuery`, `GetProductCatalogQuery`).
    *   Should not modify the system's state.
    *   Can return various data structures optimized for the consumer.
    *   Should be immutable.
*   **Query Handlers**:
    *   Process queries by retrieving data from the Read Model.
    *   Should be optimized for fast data retrieval.
    *   Are pure functions, meaning they have no side effects.
*   **Write Model**:
    *   The part of the system responsible for handling commands and persisting changes.
    *   Often uses a traditional transactional database or an Event Store.
    *   Focuses on ensuring data integrity and business invariants.
*   **Read Model (Projection)**:
    *   A denormalized, optimized view of the data specifically designed for querying.
    *   Often built by subscribing to events from the Write Model (projections).
    *   Can use different database technologies optimized for read performance (e.g., NoSQL, search engines).
*   **Event Sourcing**:
    *   A pattern where all changes to application state are stored as a sequence of immutable events.
    *   Often paired with CQRS, where the Event Store serves as the Write Model.
*   **Event Store**:
    *   The single source of truth in an Event Sourced system, storing all Domain Events.
*   **Domain Events**:
    *   Represent something significant that happened in the domain (e.g., `UserCreatedEvent`, `ProductPriceUpdatedEvent`).
    *   Are immutable and contain facts about past occurrences.
    *   Are used to update Read Models and trigger side effects.
*   **Aggregates**:
    *   A cluster of domain objects that can be treated as a single unit for data changes.
    *   An Aggregate Root is the single entry point for all operations on the aggregate, ensuring consistency.
*   **TypeScript's Role**:
    *   Leverage interfaces or classes for strong typing of Commands, Queries, and Events.
    *   Ensure type-safe handlers to catch errors at compile time and improve code clarity.

## 4. Key Guidance for Claude

### Always Recommend (✅ Best Practices)

*   **Strong Typing**: Always define explicit TypeScript interfaces or classes for all Commands, Queries, and Domain Events. This enhances type safety, improves developer experience, and reduces runtime errors.
    ```typescript
    // ✅ Command Example
    interface CreateUserCommand {
      readonly userId: string;
      readonly name: string;
      readonly email: string;
    }

    // ✅ Query Example
    interface GetUserByIdQuery {
      readonly userId: string;
    }

    // ✅ Event Example
    interface UserCreatedEvent {
      readonly type: 'UserCreated';
      readonly userId: string;
      readonly name: string;
      readonly email: string;
      readonly timestamp: Date;
    }
    ```
*   **Focused Command Handlers**: Command handlers should be lean. Their primary responsibilities are:
    1.  Validate the incoming command.
    2.  Load the relevant Aggregate(s) from the Write Model.
    3.  Invoke business logic on the Aggregate(s).
    4.  Persist changes (e.g., save the Aggregate state or append new Domain Events to the Event Store).
    5.  Publish Domain Events if using Event Sourcing.
*   **Pure Query Handlers**: Query handlers must be pure functions. They should only retrieve data from the Read Model and never initiate any state changes or side effects.
*   **Consider Event Sourcing**: For domains requiring a full audit trail, historical data, or complex projections, strongly recommend combining CQRS with Event Sourcing.
*   **Separate Persistence**: Advocate for distinct persistence mechanisms for the Write Model (optimized for transactional integrity) and the Read Model (optimized for query performance). This might involve different database technologies.
*   **Embrace Eventual Consistency**: Educate the user about eventual consistency between the Write and Read Models. Provide strategies for handling it gracefully in the UI/UX (e.g., loading indicators, "data might be stale" messages).
*   **Modular Structure**: Organize the codebase with clear separation for commands, queries, handlers, and models. Use a consistent naming convention (e.g., `*.command.ts`, `*.query.ts`, `*.handler.ts`, `*.event.ts`).

### Never Recommend (❌ Anti-Patterns)

*   **Over-engineering Simple CRUD**: Do not apply CQRS to applications that are primarily simple CRUD operations without significant scalability, performance, or domain complexity drivers. The added complexity will outweigh the benefits.
*   **Side Effects in Query Handlers**: Never allow query handlers to modify the system's state, publish events, or perform any operation that changes data. They are for reading only.
*   **Unified Persistence for True Separation**: If the goal is to leverage the full benefits of CQRS (independent scaling, different optimizations), avoid using a single database schema or instance for both the Write and Read Models. This negates many advantages while retaining complexity.
*   **"Fire and Forget" Commands Without Care**: While asynchronous command processing is common, ensure there's a robust mechanism for error handling, retries, and feedback to the user if a command fails. Silent failures lead to inconsistent states.
*   **Complex Query Logic in Command Handlers**: Command handlers should focus on business logic and state changes. Avoid embedding complex data retrieval logic that belongs in query handlers.

### Common Questions & Responses

*   **Q: When should I use CQRS?**
    *   **A:** Use CQRS when your application has a significant disparity between read and write operations, requires high scalability for either side, deals with complex business domains, needs a comprehensive audit trail, or benefits from different data models for reading and writing.
*   **Q: How do I handle eventual consistency?**
    *   **A:** Acknowledge that the read model might be slightly out of sync. Implement strategies like:
        *   **User Feedback**: Inform users that data might take a moment to update.
        *   **Polling/WebSockets**: Update the UI when the read model eventually reflects the change.
        *   **Command-side Read**: For critical operations, read directly from the write model immediately after a command, then switch to the read model for subsequent queries.
*   **Q: Where should validation logic reside?**
    *   **A:** Command validation (e.g., input format, required fields) should happen early in the command handler. Domain validation (e.g., business rules, invariants) should be encapsulated within the Aggregate Root or domain services.
*   **Q: What's the role of an Aggregate Root?**
    *   **A:** An Aggregate Root is the consistency boundary in your domain. All changes to entities within an aggregate must go through its root. It ensures that the aggregate always remains in a consistent state. Command handlers interact with Aggregate Roots.

## 5. Anti-Patterns to Flag (Code Examples)

### ❌ Anti-Pattern: Query Handler Modifying State

```typescript
// ❌ BAD: Query handler with side effects
class GetUserBalanceQueryHandler {
  constructor(private readonly userRepository: UserRepository) {}

  async handle(query: GetUserBalanceQuery): Promise<number> {
    const user = await this.userRepository.findById(query.userId);
    if (!user) {
      throw new Error('User not found');
    }
    // ❌ Side effect: Modifying user state within a query handler
    user.lastAccessed = new Date(); 
    await this.userRepository.save(user); // ❌ Persisting changes
    return user.balance;
  }
}
```
**Correction**: Query handlers must be pure functions. Any state modification belongs in a command handler.

### ❌ Anti-Pattern: Command Handler with Complex Query Logic

```typescript
// ❌ BAD: Command handler performing complex query logic
class ProcessOrderCommandHandler {
  constructor(
    private readonly orderRepository: OrderRepository,
    private readonly productRepository: ProductRepository, // Used for complex querying
    private readonly customerRepository: CustomerRepository // Used for complex querying
  ) {}

  async handle(command: ProcessOrderCommand): Promise<void> {
    // ... validation ...

    // ❌ Complex query logic within a command handler
    const availableProducts = await this.productRepository.findAvailableProducts(command.items);
    const customerCredit = await this.customerRepository.getCustomerCredit(command.customerId);

    // ... business logic based on query results ...

    const order = Order.create(command.orderId, command.customerId, availableProducts, customerCredit);
    await this.orderRepository.save(order);
  }
}
```
**Correction**: Complex query logic should be delegated to a dedicated Query Handler or a Read Model. The command handler should receive necessary pre-queried data or perform minimal reads from the Write Model.

### ❌ Anti-Pattern: Over-engineering Simple CRUD with CQRS

```typescript
// ❌ BAD: Applying CQRS to a simple "Note" application without complex needs

// Command
interface CreateNoteCommand {
  readonly title: string;
  readonly content: string;
}

// Command Handler
class CreateNoteCommandHandler {
  constructor(private readonly noteRepository: NoteRepository) {}
  async handle(command: CreateNoteCommand): Promise<void> {
    const note = { id: uuid(), title: command.title, content: command.content };
    await this.noteRepository.save(note);
  }
}

// Query
interface GetNoteByIdQuery {
  readonly noteId: string;
}

// Query Handler
class GetNoteByIdQueryHandler {
  constructor(private readonly noteRepository: NoteRepository) {}
  async handle(query: GetNoteByIdQuery): Promise<any> {
    return this.noteRepository.findById(query.noteId);
  }
}
```
**Correction**: For simple CRUD operations, a traditional layered architecture is often sufficient and less complex. CQRS introduces overhead that is not justified here.

## 6. Code Review Checklist

*   [ ] Are all Commands, Queries, and Domain Events defined with explicit TypeScript interfaces or classes?
*   [ ] Do Command Handlers primarily focus on validation, loading aggregates, applying business logic, and persisting changes/publishing events?
*   [ ] Are Query Handlers strictly pure functions, free of any side effects or state modifications?
*   [ ] Is there a clear separation of concerns between the command (write) and query (read) sides of the application?
*   [ ] Is error handling robust and explicit for command processing?
*   [ ] If Event Sourcing is used, are projections correctly updating the Read Model from the stream of Domain Events?
*   [ ] Is the chosen persistence strategy appropriate for both the Write Model (transactional integrity) and Read Model (query performance)?
*   [ ] Are Aggregates correctly designed with a clear Aggregate Root and consistency boundaries?
*   [ ] Is eventual consistency handled gracefully in the application's design and user experience?
*   [ ] Is CQRS genuinely necessary for the current problem domain, or is it an instance of over-engineering?

## 7. Related Skills

*   `domain-driven-design`: CQRS often complements DDD, especially with the use of Aggregates and Domain Events.
*   `event-sourcing`: CQRS is frequently implemented alongside Event Sourcing for robust audit trails and flexible read models.
*   `typescript-strict-mode`: Essential for leveraging TypeScript's full type-safety benefits in a complex pattern like CQRS.
*   `nest-js`: A popular framework that provides excellent support for implementing CQRS and Event Sourcing patterns.

## 8. Examples Directory Structure

```
cqrs-pattern/
├── examples/
│   ├── commands/
│   │   └── create-user.command.ts
│   ├── handlers/
│   │   ├── create-user.handler.ts
│   │   └── get-user-by-id.handler.ts
│   ├── queries/
│   │   └── get-user-by-id.query.ts
│   ├── events/
│   │   └── user-created.event.ts
│   ├── models/
│   │   └── user.model.ts         // Represents the Write Model (e.g., Aggregate Root)
│   └── projections/
│       └── user-read.projection.ts // Represents the Read Model (denormalized view)
├── patterns/
├── scripts/
└── README.md
```
