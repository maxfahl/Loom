---
Name: microservices-architecture
Version: 1.0.0
Category: System Design / Architecture
Tags: microservices, distributed systems, architecture patterns, event-driven, serverless, service mesh, api gateway, ddd, devops, scalability, resilience
Description: Best practices and patterns for designing, implementing, and managing microservices architectures.
---

# Microservices Architecture Skill

## 1. Skill Purpose

This skill enables Claude to design, implement, and manage robust, scalable, and resilient microservices architectures. It covers fundamental principles, essential design patterns, and best practices for building distributed systems that are agile, maintainable, and performant, while addressing the inherent complexities of microservices.

## 2. When to Activate This Skill

Activate this skill when the task involves:
-   Designing a new system using a microservices approach.
-   Migrating a monolithic application to microservices.
-   Evaluating or refactoring an existing microservices landscape.
-   Addressing challenges related to scalability, resilience, data consistency, or inter-service communication in a distributed system.
-   Implementing cross-cutting concerns like authentication, logging, monitoring, or tracing in a microservices environment.
-   Discussing deployment strategies, CI/CD pipelines, or operational aspects of microservices.

## 3. Core Knowledge

Claude should understand the following fundamental concepts, patterns, and best practices related to Microservices Architecture:

### Microservices Principles:

-   **Single Responsibility Principle**: Each service focuses on a single business capability.
-   **Loose Coupling**: Services should be independent and have minimal dependencies on each other.
-   **High Cohesion**: Related functionalities are grouped within a single service.
-   **Independent Deployment**: Services can be deployed, updated, and scaled independently.
-   **Bounded Contexts (from DDD)**: Clearly defined boundaries for each service, encapsulating its data and logic.
-   **Decentralized Data Management**: Each service owns its data.
-   **Resilience**: Services are designed to handle failures gracefully.

### Essential Microservices Patterns:

-   **API Gateway**: Single entry point for clients, handles routing, authentication, rate limiting, and aggregation.
-   **Service Discovery**: Mechanism for services to find and communicate with each other dynamically.
-   **Database per Service**: Each microservice has its own private database, ensuring loose coupling.
-   **Saga Pattern**: Manages distributed transactions and data consistency across multiple services.
-   **CQRS (Command Query Responsibility Segregation)**: Separates read and write models for better scalability and performance.
-   **Event Sourcing**: Stores all changes to application state as a sequence of events.
-   **Circuit Breaker**: Prevents cascading failures by stopping calls to a failing service.
-   **Bulkhead**: Isolates components to prevent failures in one from affecting others.
-   **Sidecar**: Deploys a helper container alongside the main application container for cross-cutting concerns (e.g., logging, monitoring).
-   **Strangler Fig**: Incremental migration from monolith to microservices.
-   **Event-Driven Architecture (EDA)**: Services communicate asynchronously via events.
-   **Service Mesh**: A dedicated infrastructure layer for managing service-to-service communication (e.g., Istio, Linkerd).

### Best Practices for Implementation:

-   **Domain-Driven Design (DDD)**: Crucial for defining service boundaries and contexts.
-   **Containerization (Docker, Kubernetes)**: For packaging, deploying, and orchestrating services.
-   **Centralized Logging & Monitoring**: Aggregating logs and metrics for operational visibility.
-   **Distributed Tracing**: Tracking requests across multiple services for debugging and performance analysis.
-   **Automated Testing**: Unit, integration, contract, and end-to-end tests.
-   **CI/CD Pipelines**: Automating build, test, and deployment processes.
-   **Design for Failure**: Implement retry mechanisms, timeouts, fallbacks.
-   **API-First Development**: Define clear API contracts before implementation.
-   **Zero Trust Security**: Continuous verification for all access, mutual TLS, granular access control.
-   **Observability**: Beyond monitoring, understanding the internal state of services from external outputs.
-   **Idempotent Operations**: Design operations that can be called multiple times without changing the result beyond the initial call.

## 4. Key Guidance for Claude

### Always Recommend (✅ Best Practices)

-   ✅ **Start with DDD**: Use Domain-Driven Design to identify clear service boundaries and bounded contexts before writing code.
-   ✅ **Database per Service**: Advocate for each microservice owning its own data store to ensure true independence and polyglot persistence.
-   ✅ **Asynchronous Communication**: Prefer event-driven or message-queue-based communication for loose coupling between services.
-   ✅ **Implement API Gateway**: Use an API Gateway as the single entry point for external clients to handle routing, authentication, and other cross-cutting concerns.
-   ✅ **Design for Failure**: Assume services will fail. Implement Circuit Breakers, Bulkheads, Retries, and Fallbacks to ensure resilience.
-   ✅ **Centralized Observability**: Set up robust centralized logging, monitoring, and distributed tracing from day one.
-   ✅ **Automate Everything**: Leverage CI/CD pipelines for automated testing, building, and deployment of each microservice independently.
-   ✅ **Containerize Services**: Package microservices in Docker containers for consistent deployment across environments.
-   ✅ **Zero Trust Security**: Implement strong authentication and authorization between services (e.g., mTLS, JWT) and at the API Gateway.
-   ✅ **API-First Approach**: Define clear API contracts (e.g., OpenAPI) for each service before implementation to facilitate integration.

### Never Recommend (❌ Anti-Patterns)

-   ❌ **Shared Database**: Never allow multiple microservices to share the same database. This creates tight coupling and defeats the purpose of microservices.
-   ❌ **Tight Coupling**: Avoid direct synchronous calls between services where possible, especially if it creates a dependency chain that impacts independent deployment.
-   ❌ **Distributed Monolith**: Do not break a monolith into microservices without addressing the underlying architectural issues; this often results in a distributed monolith.
-   ❌ **Ignoring Data Consistency**: Do not neglect strategies for maintaining data consistency across services in distributed transactions (e.g., Saga pattern).
-   ❌ **Neglecting Observability**: Never deploy microservices without comprehensive logging, monitoring, and distributed tracing.
-   ❌ **Manual Deployments**: Avoid manual deployment processes for microservices; always automate with CI/CD.
-   ❌ **Chatty Communication**: Avoid designing services that require excessive, fine-grained synchronous communication, which can lead to performance bottlenecks and increased latency.
-   ❌ **Ignoring Security**: Do not overlook security concerns in a distributed environment; implement Zero Trust principles.

### Common Questions & Responses (FAQ format)

**Q: How do I break down a monolithic application into microservices?**
A: Start by identifying bounded contexts using Domain-Driven Design. Use the Strangler Fig pattern to incrementally extract services, routing traffic to new services while the old functionality is gradually replaced. Prioritize extracting services that are frequently changed, independently scalable, or have clear domain boundaries.

**Q: How do microservices communicate with each other?**
A: Communication can be synchronous (e.g., REST, gRPC via API Gateway or direct service discovery) or asynchronous (e.g., message queues like Kafka, RabbitMQ, or event buses). Asynchronous communication is generally preferred for loose coupling and resilience, especially for non-critical interactions.

**Q: How do I handle data consistency across multiple microservices?**
A: Since each service owns its data, traditional ACID transactions across services are not feasible. Use eventual consistency models. The Saga pattern is a common approach for managing distributed transactions, where a sequence of local transactions is coordinated, with compensating actions for failures.

**Q: What are the key challenges in microservices architecture?**
A: Challenges include distributed data management, inter-service communication complexity, distributed tracing and debugging, operational overhead, ensuring data consistency, and managing security in a distributed environment. Proper tooling and adherence to best practices are crucial.

**Q: How do I deploy and manage microservices?**
A: Containerization (Docker) and orchestration (Kubernetes) are standard. Implement robust CI/CD pipelines for automated builds, tests, and deployments. Utilize service meshes (Istio, Linkerd) for advanced traffic management, security, and observability.

## 5. Anti-Patterns to Flag

### Anti-Pattern 1: Shared Database Across Services

**Why it's bad**: Creates tight coupling, making independent deployment and technology choices difficult. Changes to the database schema affect multiple services, leading to a distributed monolith.

**BAD (Conceptual):**
```
Service A (Orders) ----> Shared Database <---- Service B (Products)
```
*Problem*: Both services directly access and modify the same database tables, leading to strong coupling and potential data integrity issues if not carefully managed.

**GOOD (Conceptual):**
```
Service A (Orders) ----> Database A
Service B (Products) ----> Database B
```
*Solution*: Each service owns its database. If Service A needs product information, it should query Service B's API (or consume events from Service B) rather than directly accessing Service B's database.

### Anti-Pattern 2: Chatty Synchronous Communication

**Why it's bad**: Excessive synchronous calls between services increase latency, reduce resilience (a failure in one service can cascade), and create tight runtime coupling.

**BAD (Conceptual):**
```
Client -> Order Service -> Payment Service -> Inventory Service -> Notification Service
```
*Problem*: A single client request triggers a long chain of synchronous calls. If any service in the chain is slow or fails, the entire request fails or is delayed.

**GOOD (Conceptual - Event-Driven):**
```
Client -> Order Service (publishes OrderCreated event)

OrderCreated event -> Payment Service (processes payment, publishes PaymentProcessed event)
PaymentProcessed event -> Inventory Service (updates stock, publishes StockUpdated event)
StockUpdated event -> Notification Service (sends confirmation)
```
*Solution*: Use asynchronous, event-driven communication for non-critical paths. Services publish events, and other services subscribe to events they are interested in. This decouples services and improves resilience.

### Anti-Pattern 3: Lack of Centralized Observability

**Why it's bad**: In a distributed system, debugging and understanding system behavior without centralized logging, monitoring, and tracing is extremely difficult, leading to long MTTR (Mean Time To Recovery).

**BAD (Conceptual):**
```
Service A logs to local file
Service B logs to local file
Service C logs to local file
```
*Problem*: Logs are scattered, making it impossible to get a holistic view of system health or trace a request across services.

**GOOD (Conceptual):**
```
Service A --(logs)--> Centralized Log Aggregator (e.g., ELK Stack, Grafana Loki)
Service B --(metrics)--> Centralized Monitoring (e.g., Prometheus, Grafana)
Service C --(traces)--> Distributed Tracing System (e.g., Jaeger, Zipkin)
```
*Solution*: Implement a centralized observability stack. All services send their logs, metrics, and traces to a central system for aggregation, analysis, and visualization.

## 6. Code Review Checklist

-   [ ] Does the service adhere to the Single Responsibility Principle and its defined bounded context?
-   [ ] Does the service own its data store, or is it sharing a database with other services?
-   [ ] Is inter-service communication designed for loose coupling (preferring asynchronous where appropriate)?
-   [ ] Are API contracts clearly defined (e.g., using OpenAPI) and versioned?
-   [ ] Are mechanisms for resilience (Circuit Breakers, Retries, Fallbacks) implemented where external dependencies exist?
-   [ ] Is the service properly instrumented for centralized logging, monitoring, and distributed tracing?
-   [ ] Are security considerations (authentication, authorization, Zero Trust) addressed for both internal and external APIs?
-   [ ] Is the service containerized and configured for independent deployment?
-   [ ] Are automated tests (unit, integration, contract) in place?
-   [ ] Are environment variables or configuration management used for service-specific settings?
-   [ ] Are idempotent operations designed to handle retries safely?

## 7. Related Skills

-   [rest-api-design](/docs/skills/rest-api-design)
-   [event-driven-architecture-patterns](/docs/skills/event-driven-architecture-patterns)
-   [containerization-docker-compose](/docs/skills/containerization-docker-compose)
-   [ci-cd-pipelines-github-actions](/docs/skills/ci-cd-pipelines-github-actions)
-   [observability-stack-implementation](/docs/skills/observability-stack-implementation)
-   [api-error-responses](/docs/skills/api-error-responses)
-   [jwt-authentication](/docs/skills/jwt-authentication)

## 8. Examples Directory Structure

```
microservices-architecture/
├── examples/
│   ├── service_boundary_definition.md # Example of defining a bounded context
│   ├── event_driven_flow.md           # Diagram/description of an event-driven flow
│   └── api_gateway_config.yaml        # Example API Gateway configuration snippet
├── patterns/
│   ├── saga_orchestration.md          # Description of Saga orchestration pattern
│   └── circuit_breaker_implementation.md # Conceptual code for circuit breaker
├── scripts/
│   ├── microservice-scaffold.py       # Python script to scaffold a new microservice
│   ├── service-dependency-analyzer.py # Python script to analyze service dependencies
│   ├── deploy-to-k8s.sh               # Shell script for deploying to Kubernetes
│   └── event-schema-validator.py      # Python script to validate event schemas
└── README.md
```

## 9. Custom Scripts Section

This section outlines automation scripts designed to streamline common development tasks related to microservices architecture.

### 9.1. Microservice Scaffold Script

**Description**: Generates a basic project structure for a new microservice, including a simple application (Flask or Express.js), a Dockerfile, and a README. This helps developers quickly set up new services with common best practices.

**Script**: `scripts/microservice-scaffold.sh`

**Usage Examples**:

```bash
# Scaffold a new Python Flask microservice named 'product-catalog'
./scripts/microservice-scaffold.sh --name product-catalog --type python-flask --port 5000

# Scaffold a new Node.js Express microservice named 'order-processor' in a specific directory
./scripts/microservice-scaffold.sh --name order-processor --type node-express --output-dir ./services

# Perform a dry run to see what would be generated
./scripts/microservice-scaffold.sh --name test-service --type python-flask --dry-run
```

### 9.2. Service Dependency Analyzer

**Description**: Scans specified files or directories for patterns indicating inter-service communication (e.g., HTTP/HTTPS calls to other services). It helps visualize and understand the dependency graph within a microservices architecture.

**Script**: `scripts/service-dependency-analyzer.sh`

**Usage Examples**:

```bash
# Analyze services in the './services' directory, identifying calls to user-service and product-service
./scripts/service-dependency-analyzer.sh ./services --service-prefix 'http://user-service' --service-prefix 'http://product-service'

# Analyze the current directory, excluding node_modules, and output as JSON
./scripts/service-dependency-analyzer.sh . --exclude 'node_modules/*' --output-format json

# Perform a dry run
./scripts/service-dependency-analyzer.sh ./src --dry-run
```

### 9.3. Deploy to Kubernetes Script

**Description**: Automates the process of building a Docker image, pushing it to a container registry, and applying Kubernetes manifests to deploy or update a microservice in a Kubernetes cluster.

**Script**: `scripts/deploy-to-k8s.sh`

**Usage Examples**:

```bash
# Deploy a microservice to Kubernetes
./scripts/deploy-to-k8s.sh \
  --service-name user-service \
  --image-tag v1.0.0 \
  --registry myregistry.com/myorg \
  --k8s-manifest k8s/user-service.yaml \
  --namespace production

# Perform a dry run for deployment
./scripts/deploy-to-k8s.sh \
  --service-name product-service \
  --image-tag latest \
  --registry gcr.io/my-project \
  --k8s-manifest k8s/product-service.yaml \
  --dry-run
```

### 9.4. Event Schema Validator

**Description**: Validates a JSON event against a JSON schema. This ensures that event data conforms to its predefined schema, which is critical for maintaining data consistency and interoperability in event-driven microservices architectures.

**Script**: `scripts/event-schema-validator.sh`

**Usage Examples**:

```bash
# Validate an 'order_created' event against its schema
./scripts/event-schema-validator.sh \
  --event-file ./events/order_created.json \
  --schema-file ./schemas/order_created_schema.json

# Validate a 'user_updated' event (dry run)
./scripts/event-schema-validator.sh \
  --event-file ./events/user_updated.json \
  --schema-file ./schemas/user_schema.json \
  --dry-run
```
