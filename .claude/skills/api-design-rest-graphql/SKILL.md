### 1. Metadata Section

- Name: api-design-rest-graphql
- Version: 1.0.0
- Category: Web Development / API
- Tags: REST, GraphQL, API design, microservices, security, performance, documentation, versioning
- Description: Designing and implementing robust and scalable RESTful and GraphQL APIs.

### 2. Skill Purpose

This skill enables Claude to guide developers in designing and implementing high-quality, robust, and scalable APIs using both REST and GraphQL architectural styles. It covers best practices for security, performance, documentation, versioning, and developer experience, ensuring APIs are maintainable and future-proof.

### 3. When to Activate This Skill

Activate this skill when:
*   Starting a new API project (REST or GraphQL).
*   Refactoring an existing API.
*   Evaluating the choice between REST and GraphQL for a specific use case.
*   Implementing API security measures (authentication, authorization, rate limiting).
*   Designing API documentation or developer portals.
*   Addressing performance bottlenecks in an API.
*   Planning API versioning strategies.
*   Integrating APIs with microservices architectures.

### 4. Core Knowledge

*   **REST Principles**: Resource-based design, statelessness, HTTP methods (GET, POST, PUT, PATCH, DELETE), HATEOAS, cacheability.
*   **GraphQL Principles**: Schema-first design, single endpoint, precise data fetching (avoiding over/under-fetching), resolvers, queries, mutations, subscriptions.
*   **API Security**: OAuth 2.0, JWTs, HTTPS, rate limiting, throttling, input validation, least privilege.
*   **API Performance**: Pagination, filtering, caching (ETags, CDNs), N+1 problem (GraphQL DataLoader), query depth/complexity limits.
*   **API Documentation**: OpenAPI/Swagger for REST, GraphQL Schema Definition Language (SDL), interactive documentation.
*   **API Versioning**: URI versioning (`/v1/`), custom headers, content negotiation.
*   **Error Handling**: Consistent error payloads, appropriate HTTP status codes (REST), GraphQL error handling.
*   **API-First Development**: Designing APIs before implementation.
*   **Microservices Integration**: Using GraphQL as an API gateway.

### 5. Key Guidance for Claude

*   **Always Recommend**:
    *   Prioritize API-first development for better planning and developer experience.
    *   Implement robust security measures from the outset (HTTPS, AuthN/AuthZ, rate limiting).
    *   Provide comprehensive, interactive, and up-to-date API documentation.
    *   Ensure consistency in naming conventions, URL patterns, and response structures.
    *   Plan for API versioning early in the design phase.
    *   Optimize for performance using pagination, filtering, and caching.
    *   Provide clear and consistent error responses.
    *   Choose between REST and GraphQL based on the specific use case and client requirements.
*   **Never Recommend**:
    *   Exposing sensitive data without proper authentication and authorization.
    *   Using generic error messages that don't provide enough context.
    *   Breaking existing client integrations without a clear versioning strategy.
    *   Over-fetching or under-fetching data, leading to inefficient client-server communication.
    *   Ignoring API performance considerations, especially for high-traffic APIs.
*   **Common Questions & Responses**:
    *   *Q: When should I choose REST over GraphQL?*
        *   A: Choose REST when you have a clear resource model, predictable data requirements, and a simpler client-server interaction. It's often a good fit for public APIs and when caching at the HTTP level is crucial.
    *   *Q: When should I choose GraphQL over REST?*
        *   A: Choose GraphQL when clients have diverse and evolving data requirements, need to fetch data from multiple sources in a single request, or want to avoid over-fetching. It's particularly beneficial for mobile applications and complex UIs.
    *   *Q: How do I secure my API?*
        *   A: Implement HTTPS, use OAuth 2.0 for authorization and JWTs for authentication, apply rate limiting to prevent abuse, validate all input, and follow the principle of least privilege for access control.

### 6. Anti-Patterns to Flag

*   **BAD (REST)**: Using verbs in API endpoints.
    ```typescript
    // Instead of:
    // GET /getAllUsers
    // POST /createUser
    ```
*   **GOOD (REST)**: Using nouns (resources) and appropriate HTTP methods.
    ```typescript
    // GET /users
    // POST /users
    // GET /users/{id}
    // PUT /users/{id}
    // DELETE /users/{id}
    ```
*   **BAD (GraphQL)**: Exposing internal database schema directly in GraphQL schema.
    ```graphql
    type User {
      _id: ID! // Exposing internal database ID
      // ...
    }
    ```
*   **GOOD (GraphQL)**: Designing a schema that reflects the business domain, not the database.
    ```graphql
    type User {
      id: ID! // Publicly exposed ID
      // ...
    }
    ```
*   **BAD (General)**: Lack of consistent error responses.
    ```json
    // First API error
    { "message": "User not found" }

    // Second API error
    { "error": "Invalid input data", "code": 400 }
    ```
*   **GOOD (General)**: Consistent error structure.
    ```json
    {
      "status": "error",
      "code": "NOT_FOUND",
      "message": "User with ID '123' not found.",
      "details": [
        { "field": "id", "issue": "Invalid user ID" }
      ]
    }
    ```

### 7. Code Review Checklist

*   [ ] Are API endpoints resource-oriented (REST) or schema-driven (GraphQL)?
*   [ ] Is authentication and authorization properly implemented for all endpoints?
*   [ ] Is input data validated rigorously to prevent security vulnerabilities?
*   [ ] Are appropriate HTTP status codes used for RESTful APIs?
*   [ ] Is the API versioned, and is the versioning strategy clear?
*   [ ] Are pagination, filtering, and sorting options available for collections?
*   [ ] Is sensitive data protected in transit (HTTPS) and at rest?
*   [ ] Is the API well-documented (OpenAPI/Swagger for REST, SDL for GraphQL)?
*   [ ] For GraphQL, are resolvers optimized to prevent N+1 issues (e.g., DataLoader)?
*   [ ] Are rate limiting and throttling mechanisms in place?

### 8. Related Skills

*   `microservices-architecture`
*   `jwt-authentication`
*   `ci-cd-pipelines`
*   `docker-best-practices`

### 9. Examples Directory Structure

*   `examples/`
    *   `rest-api-spec.yaml` (OpenAPI/Swagger specification for a REST API)
    *   `graphql-schema.graphql` (GraphQL Schema Definition Language example)
    *   `user-service-rest.ts` (TypeScript example of a RESTful user service)
    *   `user-service-graphql.ts` (TypeScript example of a GraphQL user service with resolvers)

### 10. Custom Scripts Section

Here are 4 automation scripts that address common pain points in API design and development:

1.  **`generate-openapi-client.sh`**: A shell script that takes an OpenAPI/Swagger specification and generates client SDKs in various languages (e.g., TypeScript, Python). This automates client integration.
2.  **`validate-graphql-schema.py`**: A Python script to validate a GraphQL schema against best practices (e.g., naming conventions, presence of descriptions, avoiding N+1 patterns).
3.  **`api-load-test.py`**: A Python script using `locust` or `k6` to perform basic load testing on a given API endpoint (REST or GraphQL), reporting performance metrics.
4.  **`api-security-scan.sh`**: A shell script that integrates with open-source security scanners (e.g., `OWASP ZAP` in a headless mode) to perform basic security checks on an API endpoint.
