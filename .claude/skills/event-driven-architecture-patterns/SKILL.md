---
name: event-driven-architecture-patterns
version: 1.0.0
category: Architecture / Distributed Systems
tags: EDA, Event-Driven, Microservices, Asynchronous, TypeScript, Patterns
description: Designing and implementing systems that react to events for loose coupling and scalability.
---

# Event-Driven Architecture Patterns

## 1. Skill Purpose

This skill enables Claude to understand, design, and implement systems based on Event-Driven Architecture (EDA). EDA is a software architecture paradigm promoting the production, detection, consumption of, and reaction to events. It's crucial for building scalable, resilient, and loosely coupled systems, especially in microservices and distributed environments.

**Core Concepts:**
*   **Event**: A significant occurrence or change of state in the system. Events are immutable facts.
*   **Event Producer (Publisher)**: A component that generates and publishes events.
*   **Event Consumer (Subscriber)**: A component that listens for and reacts to events.
*   **Event Broker (Message Broker)**: An intermediary that facilitates communication between event producers and consumers (e.g., Kafka, RabbitMQ).

## 2. When to Activate This Skill

Activate this skill when the task involves:
*   Designing new microservices or distributed systems.
*   Refactoring monolithic applications into a more modular structure.
*   Implementing asynchronous communication between services.
*   Handling high-throughput data streams or real-time updates.
*   Ensuring loose coupling and high scalability for system components.
*   Managing distributed transactions with eventual consistency.
*   Keywords: "event-driven", "microservices communication", "asynchronous processing", "scalable system", "real-time updates", "distributed transactions", "event sourcing", "saga pattern".

## 3. Core Knowledge

### Event Definition and Characteristics
*   **Immutability**: Events are facts that have occurred and cannot be changed.
*   **Fact-based**: Events describe *what happened*, not *what should happen*.
*   **Schema**: Events should have a well-defined structure (e.g., using TypeScript interfaces).
*   **Versioning**: Mechanisms to handle changes in event schemas over time.

### Key Event-Driven Patterns

1.  **Publisher-Subscriber (Pub/Sub)**:
    *   **Concept**: Producers publish events to a topic/channel, and multiple consumers can subscribe to and receive these events.
    *   **Use Case**: Broadcasting information, fan-out scenarios.

2.  **Event Sourcing**:
    *   **Concept**: The application state is stored as a sequence of immutable events. The current state is derived by replaying these events.
    *   **Use Case**: Audit trails, historical data analysis, rebuilding state, complex domain models.

3.  **Command Query Responsibility Segregation (CQRS)**:
    *   **Concept**: Separates the read (query) and write (command) models of an application. Often used with Event Sourcing, where events update the read model.
    *   **Use Case**: Optimizing for read/write performance, complex queries, different data representations for reads and writes.

4.  **Saga Pattern**:
    *   **Concept**: Manages distributed transactions that span multiple services, ensuring data consistency through a sequence of local transactions and compensating actions.
    *   **Use Case**: Multi-service business processes (e.g., order fulfillment involving payment, inventory, shipping).

5.  **Outbox Pattern**:
    *   **Concept**: Ensures atomicity between a database transaction and publishing an event. Events are first saved to an "outbox" table within the same transaction as the business logic, then asynchronously published to the event broker.
    *   **Use Case**: Preventing data inconsistencies when publishing events after a database commit.

6.  **Dead Letter Queue (DLQ)**:
    *   **Concept**: A queue where messages are sent if they cannot be processed successfully after a certain number of retries.
    *   **Use Case**: Isolating problematic messages, preventing consumer blocking, enabling manual inspection and reprocessing.

### TypeScript Specifics for EDA

*   **Strong Typing for Events**: Define clear TypeScript interfaces or types for all events, including their payload.
    ```typescript
    // examples/basic-pub-sub/event-types.ts
    export interface UserCreatedEvent {
      type: 'UserCreated';
      payload: {
        userId: string;
        name: string;
        email: string;
        timestamp: string;
      };
    }

    export interface OrderPlacedEvent {
      type: 'OrderPlaced';
      payload: {
        orderId: string;
        userId: string;
        items: Array<{ productId: string; quantity: number }>;
        totalAmount: number;
        timestamp: string;
      };
    }

    export type AppEvent = UserCreatedEvent | OrderPlacedEvent;
    ```
*   **Generics for Event Handlers**: Create reusable event handler types.
    ```typescript
    // patterns/event-handler.ts
    export type EventHandler<TEvent extends { type: string; payload: any }> = (
      event: TEvent
    ) => Promise<void>;

    // Example usage
    const handleUserCreated: EventHandler<UserCreatedEvent> = async (event) => {
      console.log(`User created: ${event.payload.name} (${event.payload.email})`);
      // ... business logic
    };
    ```
*   **Strict Mode**: Always enable `strict: true` in `tsconfig.json` to enforce rigorous type safety.
*   **`unknown` over `any`**: Use `unknown` for truly unknown types and perform runtime type checks.

## 4. Key Guidance for Claude

### Always Recommend (✅ Best Practices)

*   ✅ **Define Clear Event Schemas**: Use TypeScript interfaces to explicitly define the structure and types of all events. This ensures type safety and consistency across producers and consumers.
*   ✅ **Events as Immutable Facts**: Design events to represent past occurrences. They should not be mutable or contain commands.
*   ✅ **Implement Idempotent Consumers**: Consumers should be able to process the same event multiple times without causing unintended side effects. This is crucial for resilience and retry mechanisms.
*   ✅ **Choose the Right Event Broker**: Select an event broker (e.g., Kafka for high throughput, RabbitMQ for traditional messaging, cloud-native options for managed services) that matches the system's requirements for message delivery semantics and scale.
*   ✅ **Prioritize Observability**: Implement comprehensive logging, tracing (e.g., OpenTelemetry), and monitoring for event flows. This is vital for debugging distributed systems.
*   ✅ **Event Versioning Strategy**: Plan for how event schemas will evolve. Use a version field in the event, schema registries, or create new event types for breaking changes to maintain backward compatibility.
*   ✅ **Enable TypeScript Strict Mode**: Ensure `strict: true` is set in `tsconfig.json` to leverage TypeScript's full type-checking capabilities.
*   ✅ **Use `unknown` over `any`**: When dealing with uncertain types, prefer `unknown` and narrow down the type at runtime, rather than using `any`.
*   ✅ **Outbox Pattern for Atomicity**: When publishing events after a database write, use the Outbox Pattern to ensure that the event is published only if the database transaction commits successfully.
*   ✅ **Dead Letter Queues (DLQs)**: Configure DLQs for event consumers to capture and handle messages that fail processing, preventing them from blocking the main queue.

### Never Recommend (❌ Anti-Patterns)

*   ❌ **Direct Service-to-Service Communication for Decoupled Logic**: Avoid direct HTTP calls or RPC between services when the intent is loose coupling and asynchronous processing. Use events instead.
*   ❌ **Using Events for Synchronous Request/Response**: Events are inherently asynchronous. Do not try to force a synchronous request/response model using events, as it introduces unnecessary complexity and latency.
*   ❌ **Mutable Events**: Events should be immutable records of facts. Modifying an event after it has been published violates the core principles of EDA.
*   ❌ **Consumers Relying on Producer's Internal State**: Consumers should only depend on the event's payload and its defined schema, not on the internal implementation details or state of the producer.
*   ❌ **Ignoring Error Handling**: Failing to implement robust error handling, retry mechanisms, and DLQs for event processing will lead to fragile systems.
*   ❌ **Over-engineering Simple Applications**: Do not introduce EDA complexity into small, simple applications where a monolithic or simpler architecture would suffice. The overhead often outweighs the benefits.
*   ❌ **Generic Event Names**: Avoid vague event names like `DataChanged`. Use descriptive names that reflect the business context, e.g., `UserRegistered`, `OrderShipped`.
*   ❌ **Chatty Events**: Publishing too many fine-grained events for every minor state change can lead to an "event storm" and make the system harder to understand and debug. Focus on significant business events.

### Common Questions & Responses

*   **Q: When should I use Event-Driven Architecture?**
    *   **A**: EDA is ideal for complex distributed systems, microservices, cloud-native applications, and scenarios requiring high scalability, resilience, real-time responsiveness, or asynchronous integration between disparate systems.
*   **Q: How do I ensure data consistency in an EDA system?**
    *   **A**: Data consistency in EDA often involves eventual consistency. Patterns like the Saga Pattern (for distributed transactions) and the Outbox Pattern (for atomic event publishing) are crucial. Consumers should also be idempotent.
*   **Q: What's the best event broker for my project?**
    *   **A**: The "best" broker depends on your specific needs:
        *   **Apache Kafka**: Excellent for high-throughput, durable event streaming, log aggregation, and real-time analytics.
        *   **RabbitMQ**: A mature message broker suitable for general-purpose messaging, complex routing, and traditional message queuing.
        *   **Cloud-native services (AWS SQS/SNS, Azure Event Hubs/Service Bus, Google Pub/Sub)**: Managed services that offer scalability and ease of use, often integrated with other cloud offerings.
*   **Q: How do I handle event versioning when my event schema changes?**
    *   **A**:
        1.  **Backward-compatible changes**: Add new optional fields. Consumers should be tolerant of unknown fields.
        2.  **Breaking changes**:
            *   Introduce a new event type (e.g., `UserCreatedV2`).
            *   Use a version field within the event payload (e.g., `event.version: 2`). Consumers can then handle different versions.
            *   Utilize a schema registry (e.g., Confluent Schema Registry for Kafka) to manage and enforce schemas.
*   **Q: How do I debug issues in a distributed event-driven system?**
    *   **A**: Robust observability is key. Implement distributed tracing (e.g., OpenTelemetry, Jaeger) to follow an event's journey across multiple services. Centralized logging and monitoring dashboards are also essential.

## 5. Anti-Patterns to Flag (Code Examples)

### Anti-Pattern 1: Chatty Events / Overly Granular Events

**BAD:**
```typescript
// producer.ts - Too many events for minor state changes
class ProductService {
  updateProductPrice(productId: string, newPrice: number) {
    // ... update price in DB
    this.eventBus.publish({ type: 'ProductPriceUpdated', payload: { productId, newPrice } });
  }

  updateProductStock(productId: string, newStock: number) {
    // ... update stock in DB
    this.eventBus.publish({ type: 'ProductStockUpdated', payload: { productId, newStock } });
  }

  updateProductDescription(productId: string, newDescription: string) {
    // ... update description in DB
    this.eventBus.publish({ type: 'ProductDescriptionUpdated', payload: { productId, newDescription } });
  }
}
```

**GOOD:**
```typescript
// producer.ts - Single, meaningful business event
interface ProductUpdatedEvent {
  type: 'ProductUpdated';
  payload: {
    productId: string;
    changes: {
      price?: number;
      stock?: number;
      description?: string;
    };
    timestamp: string;
  };
}

class ProductService {
  updateProduct(productId: string, updates: { price?: number; stock?: number; description?: string }) {
    // ... update product in DB
    this.eventBus.publish({
      type: 'ProductUpdated',
      payload: { productId, changes: updates, timestamp: new Date().toISOString() },
    });
  }
}
```

### Anti-Pattern 2: Event-Driven Request/Response (Synchronous over Async)

**BAD:**
```typescript
// order-service.ts - Trying to get immediate response via events
class OrderService {
  async placeOrder(orderData: any): Promise<any> {
    const orderPlacedEvent = { type: 'OrderPlaced', payload: { orderData, correlationId: '...' } };
    this.eventBus.publish(orderPlacedEvent);

    // This is an anti-pattern: waiting for a response event
    const paymentProcessedEvent = await this.eventBus.waitForEvent('PaymentProcessed', orderPlacedEvent.payload.correlationId);

    if (paymentProcessedEvent.payload.status === 'SUCCESS') {
      // ... proceed
    } else {
      // ... handle failure
    }
    return paymentProcessedEvent.payload;
  }
}
```

**GOOD:**
```typescript
// order-service.ts - Embrace asynchronicity, use callbacks or webhooks for eventual response
class OrderService {
  async placeOrder(orderData: any): Promise<{ orderId: string }> {
    const orderId = generateOrderId();
    const orderPlacedEvent = {
      type: 'OrderPlaced',
      payload: { orderId, orderData, timestamp: new Date().toISOString() },
    };
    await this.eventBus.publish(orderPlacedEvent);
    console.log(`Order ${orderId} placed. Payment will be processed asynchronously.`);
    return { orderId }; // Return immediately, response will come later
  }
}

// payment-service.ts - Processes payment and publishes result
class PaymentService {
  constructor(eventBus: EventBus) {
    eventBus.subscribe('OrderPlaced', this.handleOrderPlaced.bind(this));
  }

  async handleOrderPlaced(event: OrderPlacedEvent) {
    const { orderId, totalAmount } = event.payload;
    try {
      // ... process payment
      const paymentResult = await processPayment(orderId, totalAmount);
      await this.eventBus.publish({
        type: 'PaymentProcessed',
        payload: { orderId, status: 'SUCCESS', transactionId: paymentResult.id, timestamp: new Date().toISOString() },
      });
    } catch (error) {
      await this.eventBus.publish({
        type: 'PaymentFailed',
        payload: { orderId, reason: error.message, timestamp: new Date().toISOString() },
      });
    }
  }
}
```

### Anti-Pattern 3: Lack of Idempotency in Consumers

**BAD:**
```typescript
// inventory-service.ts - Decrements stock without checking if already processed
class InventoryService {
  constructor(eventBus: EventBus) {
    eventBus.subscribe('OrderPlaced', this.handleOrderPlaced.bind(this));
  }

  async handleOrderPlaced(event: OrderPlacedEvent) {
    const { orderId, items } = event.payload;
    // If this event is processed twice, stock will be decremented twice!
    for (const item of items) {
      await decrementStock(item.productId, item.quantity);
    }
    console.log(`Stock decremented for order ${orderId}`);
  }
}
```

**GOOD:**
```typescript
// inventory-service.ts - Idempotent consumer using a unique message ID or transaction ID
class InventoryService {
  private processedEvents: Set<string> = new Set(); // In a real app, use a persistent store

  constructor(eventBus: EventBus) {
    eventBus.subscribe('OrderPlaced', this.handleOrderPlaced.bind(this));
  }

  async handleOrderPlaced(event: OrderPlacedEvent) {
    const { orderId, items } = event.payload;
    const eventId = event.id; // Assume event has a unique ID

    if (this.processedEvents.has(eventId)) {
      console.log(`Event ${eventId} for order ${orderId} already processed. Skipping.`);
      return; // Already processed, do nothing
    }

    // Perform the operation
    for (const item of items) {
      await decrementStock(item.productId, item.quantity);
    }

    // Mark as processed
    this.processedEvents.add(eventId); // In a real app, this would be part of a transaction
    console.log(`Stock decremented for order ${orderId}`);
  }
}

// A more robust idempotent approach often involves a database transaction:
// The consumer attempts to record the event ID and perform its action within a single transaction.
// If the event ID is already recorded, the transaction fails or is skipped.
```

## 6. Code Review Checklist

*   [ ] **Event Schema Clarity**: Are all event types and their payloads clearly defined using TypeScript interfaces?
*   [ ] **Immutability**: Do events represent immutable facts? Are there any attempts to modify events after creation?
*   [ ] **Idempotency**: Are all event consumers designed to be idempotent, handling duplicate events gracefully?
*   [ ] **Error Handling & Retries**: Is there a robust strategy for handling consumer failures, including retry mechanisms and Dead Letter Queues (DLQs)?
*   [ ] **Observability**: Is logging, tracing (e.g., OpenTelemetry), and monitoring configured to track event flow across services?
*   [ ] **Event Versioning**: Is there a clear strategy for evolving event schemas while maintaining backward compatibility?
*   [ ] **Loose Coupling**: Do consumers avoid making assumptions about the internal implementation details of producers?
*   [ ] **Asynchronous Nature**: Are events used appropriately for asynchronous communication, avoiding synchronous request/response patterns?
*   [ ] **Business Significance**: Do events represent meaningful business occurrences rather than low-level technical changes?
*   [ ] **TypeScript Best Practices**: Is `strict: true` enabled? Is `any` avoided in favor of `unknown` with runtime checks? Are generics used effectively?

## 7. Related Skills

*   **Microservices Architecture**: EDA is a foundational pattern for microservices communication.
*   **CQRS Pattern**: Often combined with Event Sourcing to optimize read and write models.
*   **Database Migration Management**: Relevant for managing schema changes in event stores or read models.
*   **Observability Stack Implementation**: Essential for monitoring and debugging distributed event-driven systems.
*   **Distributed Tracing**: A specific aspect of observability critical for EDA.

## 8. Examples Directory Structure

```
examples/
├── basic-pub-sub/
│   ├── producer.ts
│   ├── consumer.ts
│   └── event-types.ts
├── event-sourcing-cqrs/
│   ├── commands.ts
│   ├── events.ts
│   ├── aggregates.ts
│   ├── read-model.ts
│   └── event-store.ts
├── saga-pattern/
│   ├── order-saga.ts
│   ├── payment-service.ts
│   ├── inventory-service.ts
│   └── shipping-service.ts
└── outbox-pattern/
    ├── order-service.ts
    ├── event-publisher.ts
    └── database-transaction.ts
```

## 9. Custom Scripts Section

Here are 4 automation scripts designed to streamline common tasks in Event-Driven Architecture development:

### Script 1: `generate-event-schema.py` (Python)
*   **Description**: Automates the creation of TypeScript interfaces for events based on a simple YAML definition. This ensures consistent event schema definitions and reduces manual boilerplate.
*   **Usage**: `python scripts/generate-event-schema.py -i event-definitions.yaml -o src/events/`

### Script 2: `create-consumer-boilerplate.sh` (Shell)
*   **Description**: Generates a basic TypeScript event consumer service boilerplate, including a listener setup, basic error handling, and a placeholder for business logic. Speeds up the creation of new event-consuming services.
*   **Usage**: `scripts/create-consumer-boilerplate.sh MyNewConsumer UserCreatedEvent`

### Script 3: `replay-events.py` (Python)
*   **Description**: A utility to replay events from a specified source (e.g., a Kafka topic, a file containing event logs) to a target event broker or consumer. Useful for testing, debugging, or rebuilding read models in Event Sourcing.
*   **Usage**: `python scripts/replay-events.py --source-topic my-events --target-topic my-events-replay --from-offset 123 --limit 100`

### Script 4: `dlq-processor.py` (Python)
*   **Description**: A script to monitor and process messages from a Dead Letter Queue (DLQ). It logs failed messages, allows for manual inspection, and provides options to re-queue them to their original topic or a different one after resolution.
*   **Usage**: `python scripts/dlq-processor.py --dlq-topic my-dlq --requeue-topic my-original-topic --max-messages 10`
