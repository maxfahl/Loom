---
name: rest-api-design
version: 1.0.0
category: Web Development / API Design
tags: REST, API design, RESTful, HTTP, API best practices, microservices
description: Best practices for designing robust, scalable, and developer-friendly RESTful APIs.
---

# REST API Design Skill

## 1. Skill Purpose

This skill enables Claude to design and evaluate RESTful APIs following industry best practices. It focuses on creating APIs that are intuitive, consistent, scalable, secure, and performant, ensuring a positive developer experience and long-term maintainability.

## 2. When to Activate This Skill

Activate this skill when:
- Designing a new RESTful API from scratch.
- Evaluating or refactoring an existing API for adherence to REST principles.
- Defining API contracts for microservices or external integrations.
- Documenting API endpoints and their behavior.
- Discussing API versioning, authentication, authorization, or error handling strategies.
- Performing code reviews on API implementations.

## 3. Core Knowledge

The fundamental concepts, principles, and best practices Claude needs to know regarding REST API design:

### Core REST Principles:

-   **Resource-Oriented Design**: APIs should expose resources (nouns, preferably plural) that represent data or services, not actions (verbs).
    -   Examples: `/users`, `/products/{id}/orders`.
-   **Statelessness**: Each request from client to server must contain all necessary information. The server should not store any client context between requests.
-   **Uniform Interface**: Use standard HTTP methods (GET, POST, PUT, PATCH, DELETE) for operations on resources.
-   **Cacheability**: Responses should explicitly or implicitly define themselves as cacheable or non-cacheable.
-   **Client-Server Separation**: Client and server evolve independently.
-   **Layered System**: Intermediaries (proxies, load balancers) can be introduced between client and server.

### URI Structure and Naming Conventions:

-   **Use Nouns (Plural)**: For collections (e.g., `/users`, `/products`).
-   **Hierarchical Structure**: Reflect relationships (e.g., `/users/{id}/orders`).
-   **Clear and Consistent**: Use kebab-case for paths (e.g., `/user-accounts`).
-   **Avoid Trailing Slashes**: Maintain consistency.
-   **Avoid Verbs in URIs**: HTTP methods define the action.

### HTTP Methods (Verbs):

-   **`GET`**: Retrieve a resource or collection. (Idempotent, Safe)
-   **`POST`**: Create a new resource. (Not Idempotent, Not Safe)
-   **`PUT`**: Update/replace an existing resource completely. (Idempotent, Not Safe)
-   **`PATCH`**: Partially update an existing resource. (Not Idempotent, Not Safe)
-   **`DELETE`**: Remove a resource. (Idempotent, Not Safe)

### HTTP Status Codes:

-   **`2xx` (Success)**: `200 OK`, `201 Created`, `204 No Content`.
-   **`3xx` (Redirection)**: `301 Moved Permanently`, `304 Not Modified`.
-   **`4xx` (Client Error)**: `400 Bad Request`, `401 Unauthorized`, `403 Forbidden`, `404 Not Found`, `405 Method Not Allowed`, `409 Conflict`, `422 Unprocessable Entity`, `429 Too Many Requests`.
-   **`5xx` (Server Error)**: `500 Internal Server Error`, `503 Service Unavailable`.

### API Versioning:

-   **URL Versioning**: `/api/v1/users` (common, explicit).
-   **Header Versioning**: `Accept: application/vnd.example.v1+json` (cleaner URIs).
-   **Query Parameter Versioning**: `/api/users?version=1` (less RESTful).
-   **Versioning from Day One**: Plan for it early.

### Security:

-   **HTTPS**: Always use TLS/SSL.
-   **Authentication**: Verify client identity (e.g., API Keys, Basic Auth, OAuth 2.0, JWT).
-   **Authorization**: Determine client permissions.
-   **Input Validation & Sanitization**: Prevent injection attacks.
-   **Rate Limiting/Throttling**: Prevent abuse (`429 Too Many Requests`).
-   **Principle of Least Privilege**: Grant minimum necessary access.

### Documentation:

-   **OpenAPI (Swagger)**: Standard for API description, enabling auto-generated docs, SDKs.
-   **Clear Examples**: Provide request/response examples.
-   **Error Details**: Document all possible error responses.

### Performance & Scalability:

-   **Pagination**: For large collections (e.g., `?page=2&size=10`).
-   **Filtering**: Allow clients to narrow results (e.g., `?status=active`).
-   **Sorting**: Allow clients to order results (e.g., `?sort=name,-created_at`).
-   **Partial Responses**: Allow clients to select fields (e.g., `?fields=id,name`).
-   **Caching**: Leverage HTTP caching headers (`Cache-Control`, `ETag`, `Last-Modified`).

## 4. Key Guidance for Claude

### Always Recommend (✅ best practices)

-   ✅ Design APIs around resources (nouns, plural) and use standard HTTP methods for actions.
-   ✅ Ensure APIs are stateless; each request should be independent.
-   ✅ Use appropriate HTTP status codes to convey the outcome of a request (e.g., 200 for success, 201 for creation, 400 for bad request, 404 for not found, 500 for server error).
-   ✅ Implement API versioning from the outset, preferably via URL (e.g., `/v1/`) or Accept header.
-   ✅ Enforce HTTPS for all API communication.
-   ✅ Implement robust authentication (e.g., OAuth 2.0, JWT) and fine-grained authorization.
-   ✅ Provide clear, consistent, and machine-readable error responses with specific error codes and messages.
-   ✅ Document the API thoroughly using OpenAPI/Swagger, including examples for requests and responses.
-   ✅ Implement pagination, filtering, and sorting for collection endpoints to improve performance and usability.
-   ✅ Apply rate limiting to protect against abuse and ensure fair usage.

### Never Recommend (❌ anti-patterns)

-   ❌ Never use verbs in API URIs (e.g., `/getUsers`, `/updateProduct`).
-   ❌ Avoid relying on session state on the server side for RESTful APIs.
-   ❌ Do not use generic HTTP status codes (e.g., always 200 OK) for all responses, especially errors.
-   ❌ Avoid exposing sensitive data or internal implementation details in API responses or error messages.
-   ❌ Never hardcode API keys or credentials; use environment variables or secure configuration management.
-   ❌ Do not skip input validation and sanitization; assume all client input is malicious.
-   ❌ Avoid returning large, unpaginated lists of resources.
-   ❌ Do not neglect API documentation; it's crucial for developer adoption and maintainability.
-   ❌ Avoid inconsistent naming conventions or response structures across different endpoints.

### Common Questions & Responses (FAQ format)

**Q: How should I handle API versioning?**
A: The most common and explicit method is URL versioning (e.g., `/v1/users`). It's easy to understand and implement. Alternatively, header versioning (`Accept: application/vnd.example.v1+json`) keeps URIs cleaner but can be less discoverable. Avoid query parameter versioning (`?version=1`) as it's less RESTful. Choose one strategy and stick to it consistently.

**Q: What's the best way to structure URIs for nested resources?**
A: Use a hierarchical structure that reflects the relationship. For example, if an order belongs to a user, use `/users/{user_id}/orders`. If an item belongs to an order, use `/users/{user_id}/orders/{order_id}/items`. This clearly shows the parent-child relationship.

**Q: How do I handle complex search or filtering requirements?**
A: Use query parameters for filtering (e.g., `/products?category=electronics&min_price=100`). For complex searches, consider a dedicated search endpoint or a flexible query language if your API supports it. Ensure filtering parameters are well-documented and indexed for performance.

**Q: When should I use PUT vs PATCH?**
A: Use `PUT` when the client is sending a complete replacement of the resource. If you `PUT` to `/users/{id}`, the request body should contain all fields for that user, and any missing fields will be considered null or default. Use `PATCH` when the client is sending only the fields that need to be updated. `PATCH` is for partial modifications.

## 5. Anti-Patterns to Flag

### Example 1: Using Verbs in URIs

**BAD:**
```
GET /getAllUsers
POST /createNewProduct
PUT /updateUserById/{id}
DELETE /removeOrder/{id}
```
*Problem*: Violates the resource-oriented principle of REST. HTTP methods already define the action.

**GOOD:**
```
GET /users
POST /products
PUT /users/{id}
DELETE /orders/{id}
```
*Solution*: Use plural nouns for resources and let HTTP methods define the operation.

### Example 2: Generic Error Responses

**BAD:**
```json
HTTP/1.1 500 Internal Server Error
{
  "message": "An unexpected error occurred."
}
```
*Problem*: Provides insufficient information for clients to understand or resolve the error. A 500 error should be reserved for unhandled server-side exceptions.

**GOOD (for client-side validation error):**
```json
HTTP/1.1 400 Bad Request
{
  "code": "INVALID_INPUT",
  "message": "Validation failed for request payload.",
  "details": [
    {
      "field": "email",
      "message": "'test' is not a valid email address."
    },
    {
      "field": "password",
      "message": "Password must be at least 8 characters long."
    }
  ]
}
```
*Solution*: Use specific HTTP status codes and provide a consistent, detailed error payload with error codes, human-readable messages, and specific field-level details where applicable.

### Example 3: Lack of Pagination for Collections

**BAD:**
```
GET /products
```
*Problem*: If the `/products` endpoint returns all products, it can lead to very large responses, slow load times, and excessive server resource consumption, especially with a growing dataset.

**GOOD:**
```
GET /products?page=1&size=20
GET /products?offset=0&limit=20
GET /products?cursor=eyJpZCI6MTIzNDV9
```
*Solution*: Implement pagination (page-based, offset-limit, or cursor-based) to allow clients to retrieve data in manageable chunks.

## 6. Code Review Checklist

-   [ ] Are URIs resource-oriented (nouns, plural) and free of verbs?
-   [ ] Are HTTP methods used appropriately for CRUD operations (GET, POST, PUT, PATCH, DELETE)?
-   [ ] Are HTTP status codes correctly reflecting the outcome of the request?
-   [ ] Is the API stateless?
-   [ ] Is API versioning implemented and consistently applied?
-   [ ] Is HTTPS enforced for all API communication?
-   [ ] Are authentication and authorization mechanisms robust and correctly implemented?
-   [ ] Are error responses consistent, informative, and machine-readable?
-   [ ] Is pagination implemented for all collection endpoints?
-   [ ] Are filtering and sorting options available for collections?
-   [ ] Is the API documented using OpenAPI/Swagger?
-   [ ] Is input validation and sanitization performed on all incoming data?
-   [ ] Is rate limiting implemented to prevent abuse?

## 7. Related Skills

-   `api-error-responses`: Detailed guidance on standardized error handling.
-   `django-rest-framework`: Practical implementation of REST principles in Python.
-   `clean-code-principles`: Applies to API design for clarity and maintainability.
-   `api-security-best-practices`: Deeper dive into securing APIs.

## 8. Examples Directory Structure

```
rest-api-design/
├── examples/
│   ├── user_resource_uris.md       # Examples of good/bad URI design for users
│   ├── http_method_usage.md        # Demonstrates correct HTTP method usage
│   ├── api_versioning_strategies.md # Different approaches to API versioning
│   └── pagination_filtering_sorting.md # Examples of query parameters for collections
├── patterns/
│   ├── consistent_error_response.json # Standardized JSON error response structure
│   └── hateoas_example.json         # Conceptual HATEOAS example
├── scripts/
│   ├── api-spec-generator.py       # Python script to generate basic OpenAPI spec
│   ├── api-endpoint-linter.py      # Python script to check endpoint naming conventions
│   ├── api-version-migrator.sh     # Shell script to assist with API versioning tasks
│   └── api-resource-generator.py   # Python script to generate boilerplate for new API resources
└── README.md
```

## 9. Custom Scripts Section

Here are 4 automation scripts designed to save significant time when designing and implementing REST APIs:

1.  **`api-spec-generator.py`**: A Python script that generates a basic OpenAPI (Swagger) specification YAML file from a simplified input (e.g., resource name, fields), helping to kickstart API documentation and design.
2.  **`api-endpoint-linter.py`**: A Python script that analyzes a project's API endpoint definitions (e.g., from `urls.py` in Django, or route files in Node.js) and flags violations of RESTful naming conventions (e.g., verbs in URIs, inconsistent plurals).
3.  **`api-version-migrator.sh`**: A shell script to assist with API versioning tasks, such as creating new version directories, copying base files, and updating routing configurations.
4.  **`api-resource-generator.py`**: A Python script to generate boilerplate code for a new API resource, including a basic model/schema, controller/handler, and routing entry, based on resource name and fields.
