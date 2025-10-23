---
name: distributed-systems-design
version: 1.0.0
category: System Design / Architecture
tags: distributed systems, microservices, scalability, fault tolerance, consistency, resilience, cloud-native, event-driven, patterns, anti-patterns
description: Enables Claude to design robust, scalable, and fault-tolerant distributed systems.
---

# Distributed Systems Design

## 1. Skill Purpose

This skill empowers Claude to design, evaluate, and troubleshoot distributed systems. It provides the foundational knowledge of principles, architectural styles, design patterns, and best practices necessary to build scalable, resilient, and maintainable applications that operate across multiple interconnected components. Claude will be able to understand the trade-offs involved in distributed environments and make informed decisions to meet specific system requirements.

## 2. When to Activate This Skill

Activate this skill when:
*   Designing new system architectures that require high availability, scalability, or fault tolerance.
*   Evaluating existing systems for performance bottlenecks, reliability issues, or scalability limitations.
*   Refactoring monolithic applications into microservices or other distributed patterns.
*   Discussing cloud-native deployments, container orchestration (Kubernetes), or serverless architectures.
*   Troubleshooting complex issues involving inter-service communication, data consistency, or distributed transactions.
*   Considering data partitioning, replication strategies, or distributed data stores.

## 3. Core Knowledge

Claude should be proficient in the following concepts:

### Principles
*   **CAP Theorem:** Understanding the trade-offs between Consistency, Availability, and Partition Tolerance.
*   **ACID vs. BASE:** Differentiating transactional properties for relational and NoSQL databases.
*   **Scalability:** Horizontal vs. Vertical scaling, elasticity, and auto-scaling.
*   **Fault Tolerance:** Designing systems to continue operating despite component failures.
*   **Resilience:** The ability to recover from failures and maintain an acceptable level of service.
*   **Consistency Models:** Strong, eventual, causal, read-your-writes, session consistency.
*   **Availability:** High availability (HA) and disaster recovery (DR) strategies.
*   **Latency & Throughput:** Key performance indicators and optimization techniques.

### Architectural Styles
*   **Microservices Architecture:** Independent services, bounded contexts, API-driven communication.
*   **Event-Driven Architecture (EDA):** Event producers, consumers, brokers (Kafka, RabbitMQ), asynchronous communication.
*   **Cloud-Native Architecture:** Leveraging cloud services, containers (Docker), orchestration (Kubernetes), serverless.

### Design Patterns
*   **Saga Pattern:** Managing distributed transactions and ensuring data consistency across services.
*   **Event Sourcing + CQRS:** Separating read and write models for scalability, auditability, and complex data flows.
*   **Circuit Breaker Pattern:** Preventing cascading failures by stopping calls to failing services.
*   **Bulkhead Pattern:** Isolating resources to prevent failures in one service from impacting others.
*   **Retry Pattern:** Automatically retrying failed operations, often with exponential backoff.
*   **API Gateway Pattern:** Single entry point for clients, routing, authentication, load balancing.
*   **Service Discovery Pattern:** Dynamically locating and communicating with services.
*   **Sharding/Partitioning:** Distributing data across multiple nodes for scalability.
*   **Replication:** Maintaining multiple copies of data for durability and availability.
*   **Leader-Follower/Master-Slave:** Patterns for distributed coordination and data management.
*   **Publish-Subscribe (Pub/Sub):** Decoupling message producers and consumers.
*   **Sidecar Pattern:** Deploying auxiliary components alongside main services (ee.g., for logging, monitoring).

### Communication Protocols
*   **RESTful APIs:** Stateless, resource-oriented communication over HTTP.
*   **gRPC:** High-performance, contract-based RPC framework.
*   **Message Queues/Brokers:** Kafka, RabbitMQ, AWS SQS/SNS, Azure Service Bus for asynchronous communication.

### Data Management
*   **Distributed Databases:** NoSQL databases (Cassandra, MongoDB, DynamoDB), NewSQL databases.
*   **Distributed Transactions:** 2-Phase Commit (2PC), 3-Phase Commit (3PC) - understanding their limitations.

### Observability
*   **Logging:** Structured logging, centralized log aggregation (ELK Stack, Grafana Loki).
*   **Monitoring:** Metrics collection (Prometheus), dashboards (Grafana), alerting.
*   **Tracing:** Distributed tracing (Jaeger, OpenTelemetry) to visualize request flow across services.

### Key Technologies & Tools
*   **Containerization:** Docker
*   **Orchestration:** Kubernetes
*   **Service Mesh:** Istio, Linkerd
*   **Cloud Platforms:** AWS, Azure, GCP
*   **Monitoring & Alerting:** Prometheus, Grafana, Datadog
*   **Tracing:** Jaeger, OpenTelemetry
*   **Message Brokers:** Apache Kafka, RabbitMQ
*   **Infrastructure as Code (IaC):** Terraform, Ansible

## 4. Key Guidance for Claude

### Always Recommend (✅ Best Practices)
*   ✅ **Design for Failure:** Assume components will fail. Implement redundancy, graceful degradation, and automated failover mechanisms.
*   ✅ **Prioritize Observability:** Implement comprehensive logging, metrics, and distributed tracing from the outset. This is crucial for understanding system behavior and debugging.
*   ✅ **Automate Everything:** Use CI/CD for deployments, Infrastructure as Code (IaC) for provisioning, and automated testing to ensure consistency and reduce human error.
*   ✅ **Start Simple, Iterate, and Refactor:** Begin with a simpler architecture (e.g., modular monolith) and evolve towards more distributed patterns as complexity and needs grow. Avoid premature optimization.
*   ✅ **Choose Appropriate Consistency Models:** Understand the trade-offs of the CAP theorem and select the consistency model (strong, eventual, etc.) that best fits the specific data and business requirements.
*   ✅ **Implement Resilience Patterns:** Actively use Circuit Breaker, Bulkhead, Retry, and Timeout patterns to prevent cascading failures and improve system stability.
*   ✅ **Decouple Services:** Design services with clear boundaries and independent deployment capabilities. Avoid shared databases between microservices.
*   ✅ **Secure by Design:** Implement security measures at every layer, including authentication, authorization, encryption (in transit and at rest), and secure communication protocols.
*   ✅ **Document APIs and Architecture:** Maintain up-to-date documentation for APIs (OpenAPI/AsyncAPI) and overall system architecture diagrams.

### Never Recommend (❌ Anti-Patterns)
*   ❌ **Single Point of Failure (SPOF):** Avoid any component whose failure can bring down the entire system without a backup or failover.
*   ❌ **Tight Coupling:** Do not design services that are heavily dependent on each other's internal implementation details. This leads to "Microservices Spaghetti."
*   ❌ **Distributed Monolith:** Avoid deploying logically separated services as a single, tightly coupled unit, negating the benefits of distribution. This often involves shared databases.
*   ❌ **Ignoring Network Latency and Failures:** Do not assume a reliable, zero-latency network. Design for network partitions, message loss, and variable latency.
*   ❌ **Over-engineering or Premature Optimization:** Do not introduce complex distributed patterns (e.g., event sourcing, CQRS) unless there's a clear, demonstrated need.
*   ❌ **Shared Databases Across Microservices:** Each microservice should own its data store to maintain autonomy and avoid tight coupling.
*   ❌ **Ignoring Security:** Never treat security as an afterthought.
*   ❌ **Chattiness (Over-communication):** Avoid excessive fine-grained synchronous communication between services, which can lead to performance bottlenecks.

### Common Questions & Responses

*   **Q: How do I ensure data consistency across multiple services?**
    *   **A:** For strong consistency, consider distributed transactions (like 2PC, but be aware of their performance overhead and blocking nature). More commonly in microservices, use eventual consistency with patterns like the Saga pattern for distributed business transactions, or Event Sourcing to reconstruct state.
*   **Q: What's the best way to handle service failures in a distributed system?**
    *   **A:** Implement resilience patterns:
        *   **Circuit Breaker:** To prevent repeated calls to a failing service.
        *   **Bulkhead:** To isolate resources and prevent one failing service from consuming all resources.
        *   **Retry with Exponential Backoff:** For transient failures.
        *   **Timeouts:** To prevent services from waiting indefinitely.
        *   Design for graceful degradation, where the system can operate in a reduced capacity during partial failures.
*   **Q: When should I use microservices versus a monolithic architecture?**
    *   **A:** Start with a modular monolith if the team is small or the domain is not well understood. Microservices introduce significant operational complexity. Migrate to microservices when:
        *   The domain is well-understood and can be clearly decomposed into bounded contexts.
        *   Different parts of the application have distinct scaling requirements.
        *   Different technologies are genuinely needed for different components.
        *   Teams need high autonomy and independent deployment cycles.
*   **Q: How can I monitor the health and performance of my distributed system?**
    *   **A:** Implement a robust observability stack:
        *   **Structured Logging:** Centralize logs with tools like ELK Stack or Grafana Loki.
        *   **Metrics:** Collect system and application metrics using Prometheus and visualize them with Grafana.
        *   **Distributed Tracing:** Use Jaeger or OpenTelemetry to trace requests across service boundaries and identify latency issues.
        *   **Alerting:** Set up alerts for critical metrics and error rates.

## 5. Anti-Patterns to Flag

### Anti-Pattern: Distributed Monolith (Shared Database)
**Description:** Services are logically separated but share a single database, leading to tight coupling and hindering independent deployment and scaling.

```typescript
// BAD: Shared database across multiple microservices
// service-a/src/user-service.ts
import { db } from '../shared-db-connection'; // Shared database connection

export async function createUser(userData: any) {
  await db.insertInto('users').values(userData).execute();
  // ...
}

// service-b/src/order-service.ts
import { db } from '../shared-db-connection'; // Shared database connection

export async function createOrder(orderData: any) {
  // Directly accessing 'users' table from another service's domain
  const user = await db.selectFrom('users').where('id', '=', orderData.userId).executeTakeFirst();
  if (!user) throw new Error('User not found');
  await db.insertInto('orders').values(orderData).execute();
  // ...
}
```

```typescript
// GOOD: Each microservice owns its data
// service-a/src/user-service.ts
import { userServiceDb } from './user-db-connection'; // Dedicated database connection

export async function createUser(userData: any) {
  await userServiceDb.insertInto('users').values(userData).execute();
  // ...
}

// service-b/src/order-service.ts
import { orderServiceDb } from './order-db-connection'; // Dedicated database connection
import { fetchUserById } from '../api/user-api'; // Communicate via API

export async function createOrder(orderData: any) {
  // Communicate with user service via its API
  const user = await fetchUserById(orderData.userId);
  if (!user) throw new Error('User not found');
  await orderServiceDb.insertInto('orders').values(orderData).execute();
  // ...
}
```

### Anti-Pattern: Chattiness (Over-communication)
**Description:** Excessive fine-grained synchronous communication between services, leading to high network latency and reduced performance.

```typescript
// BAD: Chattiness - multiple synchronous API calls for a single operation
// order-service/src/order-processor.ts
async function processOrder(orderId: string) {
  const orderDetails = await fetchOrderDetails(orderId); // API call 1
  const customerInfo = await fetchCustomerInfo(orderDetails.customerId); // API call 2
  const productDetails = await fetchProductDetails(orderDetails.productId); // API call 3
  const shippingOptions = await fetchShippingOptions(customerInfo.address); // API call 4

  // ... combine data and proceed
}
```

```typescript
// GOOD: Reduce chattiness - use a single API call or asynchronous events
// Option 1: API Gateway or Backend-for-Frontend (BFF) aggregates data
// order-service/src/order-processor.ts
async function processOrder(orderId: string) {
  // Assume an aggregated API endpoint or a BFF handles fetching combined data
  const aggregatedData = await fetchAggregatedOrderData(orderId); // Single API call

  // ... use aggregatedData and proceed
}

// Option 2: Asynchronous event-driven approach
// order-service/src/order-processor.ts
async function processOrder(orderId: string) {
  // Publish an event, other services react asynchronously
  await eventBus.publish('order.processing.requested', { orderId });
  // ...
}
// Other services (e.g., customer, product, shipping) listen to the event and update their own data or publish follow-up events.
```

## 6. Code Review Checklist

*   **Resilience:**
    *   Are Circuit Breakers implemented for external service calls?
    *   Are Retry mechanisms with exponential backoff in place for transient errors?
    *   Are appropriate timeouts configured for all network operations?
    *   Is there a strategy for graceful degradation during partial outages?
    *   Are Bulkhead patterns used to isolate critical resources?
*   **Observability:**
    *   Is structured logging used consistently across all services?
    *   Are logs aggregated centrally and easily searchable?
    *   Are key business and system metrics being collected and visualized?
    *   Is distributed tracing implemented to track requests across service boundaries?
    *   Are alerts configured for critical errors, performance deviations, and service unavailability?
*   **Decoupling & Autonomy:**
    *   Does each service own its data store?
    *   Are services communicating via well-defined APIs (REST, gRPC) or message queues?
    *   Is there minimal shared code or tight coupling between services?
    *   Can services be deployed and scaled independently?
*   **Data Consistency:**
    *   Is the chosen consistency model appropriate for the data and business requirements?
    *   If eventual consistency is used, are mechanisms in place to handle potential inconsistencies (e.g., Sagas, reconciliation)?
*   **API Design:**
    *   Are APIs well-defined, consistent, and versioned?
    *   Is API documentation (e.g., OpenAPI) up-to-date?
*   **Scalability:**
    *   Are services stateless where possible?
    *   Is there a clear strategy for horizontal scaling of services and data stores?
*   **Security:**
    *   Are authentication and authorization mechanisms properly implemented?
    *   Is data encrypted in transit and at rest?
    *   Are secrets managed securely (e.g., HashiCorp Vault, AWS Secrets Manager)?

## 7. Related Skills

*   `microservices-architecture`
*   `event-driven-architecture-patterns`
*   `cloud-deployment-kubernetes-vps`
*   `api-design-rest-graphql`
*   `containerization-docker-compose`
*   `ci-cd-pipeline-implementation`
*   `observability-stack-implementation`
*   `data-sanitization`
*   `network-security-tls-mtls`

## 8. Examples Directory Structure

```
examples/
├── typescript/
│   ├── microservice-template/
│   │   ├── src/
│   │   │   ├── app.ts
│   │   │   ├── controllers/
│   │   │   ├── services/
│   │   │   └── models/
│   │   ├── Dockerfile
│   │   ├── docker-compose.yml
│   │   ├── package.json
│   │   └── tsconfig.json
│   ├── event-driven-saga/
│   │   ├── src/
│   │   │   ├── order-service/
│   │   │   ├── payment-service/
│   │   │   └── inventory-service/
│   │   ├── kafka-setup/
│   │   └── README.md
│   └── circuit-breaker-implementation/
│       ├── src/
│       │   └── external-service-client.ts
│       └── README.md
```

## 9. Custom Scripts Section

Here are 3-5 automation scripts that would save significant time for developers working with distributed systems:

1.  **`service-scaffold.sh` (Shell Script):** Automates the creation of a new microservice project with a basic structure, Dockerfile, and `docker-compose.yml` for local development.
2.  **`chaos-injector.py` (Python Script):** A simple fault injection script to simulate network latency or service unavailability for a given service, aiding in resilience testing.
3.  **`api-contract-validator.ts` (TypeScript/Node.js Script):** Validates API contracts (e.g., OpenAPI/Swagger) against actual service responses to prevent breaking changes and ensure backward compatibility.
4.  **`distributed-trace-analyzer.py` (Python Script):** Parses distributed trace logs (e.g., OpenTelemetry JSON exports) to identify bottlenecks or errors across services, providing a summary of critical paths.
