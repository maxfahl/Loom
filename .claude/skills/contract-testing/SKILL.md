--- 
Name: contract-testing
Version: 1.0.0
Category: Testing / Integration
Tags: contract testing, consumer-driven contracts, microservices, API testing, Pact, OpenAPI, TypeScript
Description: Guides Claude on implementing and managing contract tests for robust microservice integrations.
---

# Contract Testing Skill

## 2. Skill Purpose

This skill enables Claude to understand, implement, and troubleshoot contract testing, primarily using a Consumer-Driven Contract (CDC) approach with tools like Pact and OpenAPI in TypeScript environments. It focuses on ensuring seamless integration between services by defining and verifying explicit contracts.

## 3. When to Activate This Skill

*   When discussing integration points between microservices.
*   When a new API endpoint is being developed or consumed.
*   When changes are made to an existing API.
*   When troubleshooting integration issues between services.
*   When setting up CI/CD pipelines for microservices.
*   Keywords: "contract test", "Pact", "CDC", "API integration", "service contract", "provider state", "consumer expectation".

## 4. Core Knowledge

*   **Consumer-Driven Contracts (CDC):** The philosophy where the consumer defines the contract, and the provider verifies it. This ensures that the provider only implements what is actually consumed, leading to leaner APIs and faster feedback loops.
*   **Pact Framework:** A code-first tool for implementing CDC. It works by providing a mock service for consumer tests (recording expectations) and a verifier for provider tests (replaying expectations against the actual provider).
*   **OpenAPI Specification:** A language-agnostic, human-readable, and machine-readable interface description language for REST APIs. It serves as a single source of truth for API structure and data types.
*   **TypeScript Type Generation:** Tools like `openapi-typescript` can generate TypeScript interfaces and types directly from an OpenAPI specification, providing compile-time type safety for API interactions.
*   **Provider States:** Mechanisms within Pact to set up specific data conditions on the provider side before a contract is verified. This allows testing various scenarios (e.g., "user exists", "product out of stock").
*   **Matchers:** Pact's powerful matching rules (e.g., `like`, `eachLike`, `term`, `regex`) allow for flexible assertions on data types and structures rather than exact values, preventing brittle tests that break on non-breaking changes.
*   **CI/CD Integration:** How contract tests are integrated into automated build and deployment pipelines. This typically involves publishing contracts to a Pact Broker and running provider verification as part of the provider's CI.
*   **Pact Broker:** A central repository for storing, sharing, and managing consumer contracts and provider verification results. It facilitates collaboration and provides visibility into the compatibility status of services.

## 5. Key Guidance for Claude

### Always Recommend (✅ best practices)

*   **Start with the consumer:** Always begin by defining the contract from the consumer's perspective. This ensures the API meets actual consumer needs.
*   **Use Pact-JS for TypeScript projects:** Leverage the official Pact-JS library for robust and idiomatic contract testing in TypeScript environments.
*   **Generate TypeScript types from OpenAPI specs:** Utilize `openapi-typescript` to create type definitions from your OpenAPI specification. This provides compile-time validation and improves developer experience.
*   **Define clear provider states:** Explicitly define provider states for each test scenario to ensure the provider can set up the necessary data for verification.
*   **Integrate contract tests into CI/CD with a Pact Broker:** Automate contract test execution and verification within your CI/CD pipelines, using a Pact Broker for contract management and visibility.
*   **Use loose matchers:** Employ Pact's matchers (`like`, `eachLike`, `term`, `regex`) to assert on data types and structures rather than exact values, making tests resilient to non-breaking changes.
*   **Isolate contract tests:** Ensure contract tests run quickly and independently, without requiring the actual provider to be running.

### Never Recommend (❌ anti-patterns)

*   **Writing full integration tests instead of contract tests:** Avoid spinning up entire services for integration testing when contract tests can provide faster, more isolated feedback on API compatibility.
*   **Hardcoding exact values in contracts:** Do not use exact values in contract expectations where a matcher would be more appropriate, as this leads to brittle tests.
*   **Allowing consumers to directly test provider implementations:** Consumers should not directly test the provider's code; they should test against a contract that the provider then verifies.
*   **Ignoring contract test failures in CI/CD:** Treat contract test failures as critical build failures to prevent breaking changes from reaching production.
*   **Manual contract management:** Avoid manually sharing or managing contract files; always use a Pact Broker.

### Common Questions & Responses (FAQ format)

*   **Q:** What's the difference between contract testing and integration testing?
    *   **A:** Contract testing verifies the *contract* (agreed-upon interface and behavior) between two services in isolation, ensuring they can communicate correctly. Integration testing verifies the *actual interaction* of multiple services running together in a more realistic environment. Contract tests are faster, provide earlier feedback, and are more focused on interface compatibility.
*   **Q:** How do I handle data variations in contract tests?
    *   **A:** For the provider, use "provider states" to define specific data scenarios (e.g., "a user with ID 123 exists"). For the consumer, use Pact's matchers (e.g., `like`, `eachLike`, `term`) to assert on data types and structures rather than exact values, allowing for flexibility in the actual data returned by the provider.
*   **Q:** Should I use OpenAPI or Pact?
    *   **A:** They are complementary. OpenAPI defines the API's schema and structure. Pact verifies the *behavior* and interactions against a consumer-defined contract. You can use `openapi-typescript` to generate types from your OpenAPI spec for compile-time safety, and then use Pact to verify the runtime interactions. Some tools can even generate Pact contracts from OpenAPI definitions.
*   **Q:** How do I version my contracts?
    *   **A:** Pact Broker automatically handles contract versioning based on the consumer's application version. For API versioning, ensure your contracts reflect the specific API version they are testing (e.g., `/api/v1/users`).

## 6. Anti-Patterns to Flag

### Anti-Pattern: Brittle Consumer Test (Exact Value Matching)

**BAD:** This test will break if the provider changes any non-critical field or value, even if the API contract is still met.

```typescript
// examples/consumer/tests/user-service.pact.spec.ts (BAD example)
import { PactV3, MatchersV3 } from '@pact-foundation/pact';
import { resolve } from 'path';
import { UserService } from '../src/user-service'; // Assuming a simple API client

const provider = new PactV3({
  consumer: 'FrontendApp',
  provider: 'UserService',
  port: 8080,
  logLevel: 'debug',
  dir: resolve(process.cwd(), 'pact/interactions'),
});

describe('UserService API', () => {
  describe('getting a user by ID', () => {
    it('should return a specific user', async () => {
      await provider.addInteraction({
        uponReceiving: 'a request for user 1',
        withRequest: {
          method: 'GET',
          path: '/users/1',
          headers: { 'Accept': 'application/json' },
        },
        willRespondWith: {
          status: 200,
          headers: { 'Content-Type': 'application/json' },
          body: { // Exact values, very brittle!
            id: 1,
            name: 'John Doe',
            email: 'john.doe@example.com',
            age: 30,
          },
        },
      });

      await provider.executeTest(async (mockService) => {
        const userService = new UserService(mockService.url);
        const user = await userService.getUser(1);
        expect(user).toEqual({ id: 1, name: 'John Doe', email: 'john.doe@example.com', age: 30 });
      });
    });
  });
});
```

**GOOD:** Using Pact matchers makes the test more robust and focused on the contract, allowing for variations in non-critical data.

```typescript
// examples/consumer/tests/user-service.pact.spec.ts (GOOD example)
import { PactV3, MatchersV3 } from '@pact-foundation/pact';
import { resolve } from 'path';
import { UserService } from '../src/user-service'; // Assuming a simple API client

const { like, eachLike, term } = MatchersV3;

const provider = new PactV3({
  consumer: 'FrontendApp',
  provider: 'UserService',
  port: 8080,
  logLevel: 'debug',
  dir: resolve(process.cwd(), 'pact/interactions'),
});

describe('UserService API', () => {
  describe('getting a user by ID', () => {
    it('should return a user with expected structure', async () => {
      await provider.addInteraction({
        uponReceiving: 'a request for user 1',
        withRequest: {
          method: 'GET',
          path: '/users/1',
          headers: { 'Accept': 'application/json' },
        },
        willRespondWith: {
          status: 200,
          headers: { 'Content-Type': 'application/json' },
          body: like({
            id: like(1), // Expect a number, example value 1
            name: term({
              matcher: '[A-Za-z ]+',
              generate: 'John Doe',
            }),
            email: term({
              matcher: '\\w+@\\w+\\.\\w+',
              generate: 'john.doe@example.com',
            }),
            // age might be optional or have a default, use like() if always present
            age: like(30),
          }),
        },
      });

      await provider.executeTest(async (mockService) => {
        const userService = new UserService(mockService.url);
        const user = await userService.getUser(1);
        // Assertions should also be flexible, checking types/structure
        expect(typeof user.id).toBe('number');
        expect(typeof user.name).toBe('string');
        expect(typeof user.email).toBe('string');
        expect(user.email).toMatch(/\\w+@\\w+\\.\\w+/);
      });
    });
  });
});
```

### Anti-Pattern: Provider Not Verifying Consumer Contracts

**BAD:** A provider team makes changes to their API without verifying that these changes are compatible with existing consumer contracts. This leads to runtime errors for consumers.

**Solution:** Implement a provider verification step in the provider's CI/CD pipeline. This step fetches all relevant consumer contracts from a Pact Broker and runs them against the actual provider service. If any contract is broken, the build fails.

## 7. Code Review Checklist

*   **Contract Coverage:** Are all critical API interactions between services covered by contract tests?
*   **Matcher Usage:** Are consumer tests using appropriate Pact matchers (`like`, `eachLike`, `term`, `regex`) to ensure flexibility and prevent brittleness?
*   **Provider States:** Are provider states clearly defined and correctly implemented on the provider side to simulate various scenarios?
*   **CI/CD Integration:** Is the contract testing workflow (consumer contract generation, publishing, provider verification) integrated into the CI/CD pipeline?
*   **Pact Broker:** Is a Pact Broker being used to manage and share contracts between consumer and provider teams?
*   **Type Safety:** If applicable, are TypeScript types generated from OpenAPI specifications being used in API clients to catch contract violations at compile time?
*   **Isolation:** Do consumer contract tests run in isolation against a mock service, without requiring the actual provider to be running?
*   **Meaningful Descriptions:** Are contract test descriptions clear and descriptive, explaining the consumer's intent?

## 8. Related Skills

*   `api-versioning`: For managing changes to API contracts over time.
*   `microservices-architecture`: Contract testing is crucial for maintaining stability in distributed systems.
*   `ci-cd-pipelines`: For automating the execution and verification of contract tests.
*   `typescript-strict-mode`: Enhances type safety, complementing the use of generated types from OpenAPI.
*   `rest-api-design`: Good API design facilitates easier contract testing.

## 9. Examples Directory Structure

```
examples/
├── consumer/
│   ├── src/
│   │   └── user-service.ts         # Example consumer API client
│   └── tests/
│   │       └── user-service.pact.spec.ts # Consumer-side Pact test
├── provider/
│   ├── src/
│   │   └── user-api.ts             # Example provider API implementation
│   └── pact-provider-verification.spec.ts # Provider-side Pact verification
└── openapi/
    └── user-api.yaml               # OpenAPI specification for the User API
```

## 10. Custom Scripts Section

Here are 4 automation scripts designed to streamline common contract testing workflows.

### 1. `generate-pact-consumer-test.py` (Python)

*   **Description:** Generates a boilerplate Pact consumer test file (`.pact.spec.ts`) for a given service, including basic interaction setup.
*   **Usage:** `python scripts/generate-pact-consumer-test.py --consumer MyFrontend --provider MyBackend --service UserService`

### 2. `update-openapi-types.sh` (Shell)

*   **Description:** Automates the generation/update of TypeScript types from an OpenAPI specification using `openapi-typescript`.
*   **Usage:** `scripts/update-openapi-types.sh -s ./examples/openapi/user-api.yaml -o ./examples/consumer/src/api-types.ts`

### 3. `run-pact-provider-verification.sh` (Shell)

*   **Description:** Executes the Pact provider verification process against a running provider service, fetching contracts from a Pact Broker.
*   **Usage:** `scripts/run-pact-provider-verification.sh --provider-name UserService --provider-base-url http://localhost:3000 --pact-broker-url https://your-pact-broker.example.com`

### 4. `publish-pact-contract.sh` (Shell)

*   **Description:** Publishes a generated consumer contract to a Pact Broker.
*   **Usage:** `scripts/publish-pact-contract.sh --consumer-name FrontendApp --provider-name UserService --consumer-version 1.0.0 --contract-file ./pact/interactions/frontendapp-userservice.json`
