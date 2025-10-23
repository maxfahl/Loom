---
Name: api-versioning
Version: 1.0.0
Category: API Development
Tags: API, Versioning, REST, GraphQL, gRPC, Microservices
Description: Strategies and best practices for versioning APIs to ensure backward compatibility and smooth evolution.
---

## Skill Purpose

This skill enables Claude to understand, implement, and advise on various API versioning strategies. It covers the rationale behind API versioning, common approaches (URI, Header, Query Parameter, Media Type), and best practices for managing API evolution, deprecation, and client migration. The goal is to help developers build robust, maintainable, and future-proof APIs.

## When to Activate This Skill

Activate this skill when:
- Designing a new API or extending an existing one.
- Planning for backward-compatible changes or introducing breaking changes.
- Migrating clients to a new API version.
- Documenting API changes or deprecation policies.
- Reviewing API design for versioning consistency and best practices.
- Discussing the impact of API changes on consumers.

## Core Knowledge

The fundamental concepts, patterns, and APIs Claude needs to know:

### 1. Why API Versioning Matters
- **Backward Compatibility**: Allowing older clients to continue functioning while new versions are introduced.
- **Managing Evolving Requirements**: Adapting to new business needs without disrupting existing integrations.
- **Supporting Multiple Client Types**: Catering to diverse client needs simultaneously.
- **Facilitating Controlled Rollouts**: Gradual migration of consumers to new versions, reducing risk.

### 2. Common API Versioning Strategies

#### a. URI Path Versioning
- **Description**: Embeds the version number directly in the URL path.
- **Example**: `/api/v1/users`, `/api/v2/products`
- **Pros**: Simple, clear, easy to implement, good for caching, human-readable.
- **Cons**: Violates REST principle of resource identification (different URIs for the same logical resource), URL proliferation.

#### b. Header Versioning
- **Description**: Includes version information in custom HTTP headers or the `Accept` header.
- **Example**: `X-API-Version: 1`, `Accept: application/vnd.myapi.v2+json`
- **Pros**: Clean URLs, fine-grained control, allows content negotiation.
- **Cons**: Less discoverable, requires client to explicitly send headers, can be complex with content negotiation.

#### c. Query Parameter Versioning
- **Description**: Specifies the version as a query parameter in the URL.
- **Example**: `/api/users?version=1`, `/api/products?api-version=2025-09-01`
- **Pros**: Flexible, easy to test in browsers, supports date-based versions.
- **Cons**: Less canonical for REST, can affect caching, version might be overlooked.

#### d. Media Type Versioning (Content Negotiation)
- **Description**: Uses the `Accept` header to specify the desired media type, including a version.
- **Example**: `Accept: application/vnd.company.resource.v1+json`
- **Pros**: Adheres to REST principles, clean URLs.
- **Cons**: More complex to implement and document, requires good tooling.

#### e. GraphQL and gRPC Versioning
- **GraphQL**: Typically versions schemas by adding new fields/types, deprecating old ones, rather than versioning the entire API endpoint.
- **gRPC**: Uses protocol buffer versioning, often by placing the version in the package name (e.g., `package billing.v1;`).

### 3. Semantic Versioning
- **Concept**: `MAJOR.MINOR.PATCH` (e.g., `1.2.3`)
  - **MAJOR**: Breaking changes (incompatible API changes).
  - **MINOR**: Backward-compatible new features/functionality.
  - **PATCH**: Backward-compatible bug fixes.

### 4. Deprecation and Sunset Policies
- **Importance**: Clear communication and timelines for retiring old API versions.
- **Common Practice**: Support previous major version for 6-12 months.
- **Communication Channels**: Headers, emails, dashboards, documentation.

### 5. API Gateways
- **Role**: Centralized management of API versions, routing, security, and rate limiting.
- **Examples**: Nginx, Kong, AWS API Gateway, Azure API Management.

## Key Guidance for Claude

### ✅ Always Recommend
- **Version Public APIs**: Always assume public-facing APIs require versioning from day one.
- **Prioritize Backward Compatibility**: Strive to make changes non-breaking whenever possible.
- **Use Semantic Versioning**: Apply `MAJOR.MINOR.PATCH` for clear communication of change impact.
- **Document Thoroughly**: Provide clear documentation, migration guides, and examples for each version.
- **Implement a Deprecation Policy**: Clearly communicate deprecation timelines and support windows.
- **Utilize API Gateways**: For routing and managing multiple API versions in production.
- **Log API Version Usage**: To inform deprecation decisions and understand client adoption.
- **Design for Extensibility**: Allow clients to ignore unknown fields in responses.

### ❌ Never Recommend
- **No Versioning**: Never release a public API without a versioning strategy.
- **Mixing Versions in One Controller/Endpoint**: Avoid logic that handles multiple versions within a single code unit; separate concerns.
- **Implicit Breaking Changes**: Never introduce breaking changes without a major version increment and clear communication.
- **Abrupt Deprecation**: Do not remove old API versions without ample notice and a transition period.
- **Version in Body**: Avoid putting version information solely in the request body, as it's harder for routing and caching.
- **Ignoring Client Needs**: Do not make versioning decisions without considering the impact on API consumers.

### Common Questions & Responses

- **Q: Which versioning strategy is best?**
  - **A:** URI Path versioning is often recommended for its simplicity and discoverability, especially for public APIs. Header versioning offers cleaner URLs and more flexibility for internal/partner APIs. The "best" strategy depends on the API's audience, complexity, and existing infrastructure.
- **Q: How do I handle non-breaking changes?**
  - **A:** For non-breaking changes (e.g., adding new optional fields, new endpoints), you typically increment the MINOR or PATCH version of the *current* API version. Existing clients should continue to work without modification.
- **Q: When should I create a new major version?**
  - **A:** A new major version (`v2`, `v3`, etc.) should be created when introducing **breaking changes** that are incompatible with previous versions and require clients to update their code.
- **Q: What's a good deprecation timeline?**
  - **A:** A common practice is to support the previous major version for 6-12 months after a new major version is released. This gives clients sufficient time to migrate.
- **Q: Can I use different versioning strategies for different parts of my API?**
  - **A:** While technically possible, it's generally discouraged for consistency and to avoid confusion. Stick to one primary strategy across your API.

## Anti-Patterns to Flag

### 1. No Versioning (Implicit v1)
**BAD:**
```typescript
// api/users.ts
export async function GET(request: Request) {
  // Returns user data
}
```
**GOOD:**
```typescript
// api/v1/users.ts
export async function GET(request: Request) {
  // Returns user data for v1
}
```
**Explanation**: Always explicitly version your APIs, even the initial version, to prepare for future changes.

### 2. Mixing Versions in a Single Endpoint
**BAD:**
```typescript
// api/users.ts
export async function GET(request: Request) {
  const version = request.headers.get('X-API-Version') || '1';
  if (version === '2') {
    // v2 logic
  } else {
    // v1 logic
  }
}
```
**GOOD:**
```typescript
// api/v1/users.ts
export async function GET(request: Request) {
  // v1 logic
}

// api/v2/users.ts
export async function GET(request: Request) {
  // v2 logic
}
```
**Explanation**: Separate concerns by having distinct endpoints or code paths for each API version. This improves readability, maintainability, and testability.

### 3. Breaking Changes Without Version Increment
**BAD:**
```typescript
// api/v1/products.ts (original)
interface Product {
  id: string;
  name: string;
  price: number;
}

// api/v1/products.ts (after change - 'price' removed, 'cost' added)
interface Product {
  id: string;
  name: string;
  cost: number; // Breaking change for clients expecting 'price'
}
```
**GOOD:**
```typescript
// api/v1/products.ts (original)
interface ProductV1 {
  id: string;
  name: string;
  price: number;
}

// api/v2/products.ts (new version with breaking change)
interface ProductV2 {
  id: string;
  name: string;
  cost: number;
}
```
**Explanation**: Any change that forces clients to modify their code (e.g., renaming fields, removing fields, changing data types) is a breaking change and requires a new major version.

## Code Review Checklist

- [ ] Is the API explicitly versioned (e.g., `/v1/`, `X-API-Version: 1`)?
- [ ] Does the versioning strategy align with the API's audience and use case?
- [ ] Are breaking changes introduced only in new major versions?
- [ ] Are non-breaking changes handled gracefully within the current version (minor/patch increment)?
- [ ] Is there clear documentation for all API versions, including migration guides?
- [ ] Is a deprecation policy defined and communicated for older versions?
- [ ] Are API Gateway rules configured correctly to route requests to the appropriate versions?
- [ ] Is the code separated by version (e.g., `v1` and `v2` directories/modules)?
- [ ] Are new fields added as optional to maintain backward compatibility?
- [ ] Is semantic versioning applied consistently?

## Related Skills

- `rest-api-design`: For general principles of RESTful API design.
- `openapi-specification`: For documenting API contracts and versions.
- `microservices-architecture`: For understanding how versioning fits into distributed systems.
- `typescript-strict-mode`: For ensuring type safety in API contracts.

## Examples Directory Structure

```
api-versioning/
├── examples/
│   ├── uri-versioning/
│   │   ├── src/
│   │   │   ├── v1/
│   │   │   │   └── users.ts
│   │   │   └── v2/
│   │   │   │   └── users.ts
│   │   │   └── index.ts (router/gateway setup)
│   │   └── tests/
│   │       └── uri-versioning.test.ts
│   ├── header-versioning/
│   │   ├── src/
│   │   │   ├── api.ts (logic for header parsing)
│   │   │   └── users.ts
│   │   └── tests/
│   │       └── header-versioning.test.ts
│   └── media-type-versioning/
│       ├── src/
│       │   ├── api.ts (logic for media type parsing)
│       │   └── products.ts
│       └── tests/
│           └── media-type-versioning.test.ts
```

## Custom Scripts Section

This section outlines automation scripts designed to streamline common tasks associated with API versioning. Each script aims to reduce manual effort, enforce best practices, and improve consistency across API development workflows.

### 1. `generate-api-version-boilerplate.sh` (Shell Script)
- **Purpose**: Scaffolds a new API version directory and basic endpoint files based on a chosen versioning strategy (URI or Header).
- **Pain Point**: Manually creating new folders, files, and basic routing for each new API version is repetitive and error-prone.
- **Usage**: `generate-api-version-boilerplate.sh --strategy uri --version v2 --resource users`

### 2. `check-api-deprecation.py` (Python Script)
- **Purpose**: Scans API codebase (e.g., OpenAPI spec, route files) for deprecated endpoints and flags them based on a defined deprecation policy.
- **Pain Point**: Forgetting to deprecate old endpoints or not communicating deprecation effectively.
- **Usage**: `check-api-deprecation.py --api-spec ./openapi.yaml --policy 6_months`

### 3. `update-api-gateway-routes.sh` (Shell Script)
- **Purpose**: Automates the update of API Gateway routing configurations (e.g., Nginx, Kong, AWS API Gateway) to include new API versions or deprecate old ones.
- **Pain Point**: Manually updating API Gateway configurations is complex, error-prone, and time-consuming.
- **Usage**: `update-api-gateway-routes.sh --gateway nginx --config ./nginx.conf --action add --version v2 --target /api/v2`

### 4. `compare-api-versions.py` (Python Script)
- **Purpose**: Compares two versions of an API definition (e.g., OpenAPI/Swagger spec files) to identify breaking changes, new features, and deprecated elements.
- **Pain Point**: Manually identifying all changes between API versions for migration guides or semantic versioning decisions.
- **Usage**: `compare-api-versions.py --old-spec ./openapi-v1.yaml --new-spec ./openapi-v2.yaml --output report.md`
