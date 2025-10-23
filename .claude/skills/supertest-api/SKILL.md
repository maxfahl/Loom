--- 
name: supertest-api
version: 0.1.0
category: Testing / API
tags: node.js, express, supertest, typescript, jest, mocha, api testing, integration testing
description: Enables Claude to write robust integration tests for Node.js HTTP APIs using Supertest and TypeScript.
---

## Skill Purpose

This skill enables Claude to effectively write, understand, and debug integration tests for Node.js HTTP APIs using the Supertest library in a TypeScript environment. It focuses on best practices for testing various HTTP methods, asserting responses, handling asynchronous operations, managing test databases, and mocking external dependencies.

## When to Activate This Skill

Activate this skill when the user is:
- Asking to write new integration tests for a Node.js API.
- Debugging existing Supertest-based API tests.
- Refactoring API tests to improve readability, maintainability, or performance.
- Setting up a new Node.js project and needs guidance on API testing infrastructure.
- Discussing strategies for testing API authentication, error handling, or database interactions.
- Reviewing pull requests that involve changes to API tests.

Specific keywords or patterns that indicate this skill is needed:
- "write API tests for Node.js"
- "Supertest integration tests"
- "testing Express routes with TypeScript"
- "how to test API authentication"
- "mocking dependencies in Supertest tests"
- "database setup for API tests"
- "asserting HTTP responses"

## Core Knowledge

The fundamental concepts, patterns, and APIs Claude needs to know:

1.  **Supertest Basics**:
    *   `request(app)`: Creating a Supertest agent from an Express application instance.
    *   HTTP methods: `.get()`, `.post()`, `.put()`, `.delete()`, `.patch()`.
    *   Sending data: `.send(data)`, `.field(name, value)`.
    *   Setting headers: `.set(name, value)`.
    *   Query parameters: `.query(object)`.
    *   Assertions: `.expect(statusCode)`, `.expect(headerName, headerValue)`, `.expect(body)`, `.expect(function)`.
    *   Asynchronous nature: Always use `async/await`.

2.  **Testing Framework Integration (Jest/Mocha)**:
    *   `describe`, `it`/`test` blocks for structuring tests.
    *   `beforeAll`, `beforeEach`, `afterEach`, `afterAll` hooks for setup and teardown.
    *   Jest `expect` matchers (`.toBe`, `.toEqual`, `.toHaveProperty`, `.toBeInstanceOf`, `.toMatchObject`, etc.).

3.  **TypeScript Specifics**:
    *   Type definitions (`@types/supertest`, `@types/jest`).
    *   Configuring `tsconfig.json` for test files.
    *   Importing modules correctly.

4.  **API Testing Patterns**:
    *   **Isolation**: Each test should be independent and not affect others.
    *   **Database Management**: Using in-memory databases or separate test databases, clearing data between tests.
    *   **Mocking**: Mocking external services, third-party APIs, or complex internal modules.
    *   **Authentication**: Handling tokens, cookies, and different authentication flows.
    *   **Error Handling**: Testing expected error responses (e.g., 400, 401, 403, 404, 500).
    *   **File Uploads**: Testing endpoints that handle `multipart/form-data`.

5.  **Project Structure**:
    *   Organizing test files (e.g., `src/__tests__`, `tests/`).
    *   Naming conventions for test files (e.g., `*.test.ts`, `*.spec.ts`).

## Key Guidance for Claude

### Always Recommend (✅ best practices)

*   ✅ **Use `async/await`**: Always use `async/await` with Supertest calls to handle asynchronous operations cleanly.
*   ✅ **Isolate Tests**: Ensure each test is independent. Use `beforeEach` and `afterEach` hooks to reset the state (e.g., clear database, reset mocks).
*   ✅ **Use a Dedicated Test Database**: For tests involving a database, use an in-memory database or a separate, isolated test database to prevent data contamination.
*   ✅ **Mock External Dependencies**: Mock any external services or third-party APIs to make tests fast, reliable, and independent of external system availability.
*   ✅ **Test Edge Cases and Error Paths**: Explicitly test invalid inputs, missing authentication, unauthorized access, and server errors to ensure robust error handling.
*   ✅ **Clear Assertions**: Use specific and clear assertions for status codes, response bodies, and headers. Avoid overly broad assertions.
*   ✅ **Organize Tests Logically**: Group related tests using `describe` blocks and name them descriptively.
*   ✅ **Type Safety**: Leverage TypeScript for type safety in test data, request bodies, and response structures.
*   ✅ **Clean Teardown**: Ensure all resources (database connections, mock servers) are properly closed or cleaned up in `afterAll` hooks.

### Never Recommend (❌ anti-patterns)

*   ❌ **Synchronous Supertest Calls**: Never use Supertest calls without `async/await` or proper Promise handling.
*   ❌ **Shared State Between Tests**: Avoid tests that rely on the side effects of other tests. This leads to flaky and hard-to-debug tests.
*   ❌ **Testing Against Production/Development Database**: Never run integration tests against your development or production database.
*   ❌ **Real External API Calls**: Do not make actual calls to external APIs in integration tests; mock them instead.
*   ❌ **Vague Assertions**: Avoid `expect(res.statusCode).toBeDefined()` or `expect(res.body).toBeTruthy()` without more specific checks.
*   ❌ **Over-mocking**: Don't mock every single internal module. Focus on external dependencies or complex, slow internal components.
*   ❌ **Hardcoding Values**: Avoid hardcoding IDs or other dynamic data. Generate them or fetch them dynamically within the test setup.

### Common Questions & Responses (FAQ format)

*   **Q: How do I test authenticated routes?**
    *   **A:** First, perform a login request to obtain an authentication token (e.g., JWT). Then, include this token in the `Authorization` header of subsequent requests using `.set('Authorization', `Bearer ${token}`)`.
*   **Q: My tests are slow. How can I speed them up?**
    *   **A:**
        1.  **Use an in-memory database:** Significantly faster than disk-based databases.
        2.  **Mock external services:** Avoid network latency.
        3.  **Optimize database cleanup:** Clear only necessary collections between tests, or drop the entire database once in `afterAll`.
        4.  **Run tests in parallel:** If your test runner supports it and tests are isolated.
*   **Q: How do I test file uploads?**
    *   **A:** Use `.attach(fieldName, filePath)` for file attachments and `.field(fieldName, value)` for other form fields when sending `multipart/form-data` requests.
*   **Q: How can I ensure my Express app is ready before tests run?**
    *   **A:** Export your Express `app` instance directly from its module. Supertest will automatically start and stop the server for you when `request(app)` is called. For more complex setups, you might need to explicitly start and stop the server in `beforeAll` and `afterAll` hooks.

## Anti-Patterns to Flag

### BAD: Relying on global state or previous test side-effects

```typescript
// users.test.ts
let createdUserId: string;

describe('User API', () => {
  it('should create a user', async () => {
    const res = await request(app).post('/users').send({ name: 'Test User' });
    expect(res.statusCode).toBe(201);
    createdUserId = res.body.id; // BAD: Storing state globally
  });

  it('should get the created user', async () => {
    // BAD: This test depends on the previous test creating a user
    const res = await request(app).get(`/users/${createdUserId}`);
    expect(res.statusCode).toBe(200);
    expect(res.body.name).toBe('Test User');
  });
});
```

### GOOD: Isolated tests with proper setup

```typescript
// users.test.ts
import request from 'supertest';
import app from '../src/app'; // Your Express app
import User from '../src/models/User'; // Your Mongoose/Sequelize model

describe('User API', () => {
  beforeEach(async () => {
    // Clear users collection before each test
    await User.deleteMany({});
  });

  it('should create a user', async () => {
    const newUser = { name: 'Test User', email: 'test@example.com' };
    const res = await request(app).post('/users').send(newUser);
    expect(res.statusCode).toBe(201);
    expect(res.body.name).toBe(newUser.name);
    expect(res.body).toHaveProperty('id');
  });

  it('should get a specific user', async () => {
    // GOOD: Create user within the test's setup
    const user = await User.create({ name: 'Existing User', email: 'existing@example.com' });
    const res = await request(app).get(`/users/${user._id}`);
    expect(res.statusCode).toBe(200);
    expect(res.body.name).toBe('Existing User');
  });
});
```

## Code Review Checklist

*   [ ] Are all Supertest calls `await`ed?
*   [ ] Is test data isolated and cleaned up between tests (e.g., `beforeEach`, `afterEach`)?
*   [ ] Are external dependencies mocked, or is a dedicated test environment used?
*   [ ] Are status codes, response bodies, and headers asserted clearly and specifically?
*   [ ] Are error conditions and edge cases covered by tests?
*   [ ] Is authentication handled correctly for protected routes?
*   [ ] Are test files and descriptions clear and descriptive?
*   [ ] Is TypeScript used effectively for type safety in test data and responses?
*   [ ] Are all necessary imports present and correct?
*   [ ] Is the test setup and teardown efficient (e.g., database connections, server start/stop)?

## Related Skills

*   `node-express-api`: For understanding Node.js/Express API development.
*   `jest-unit-tests`: For general Jest testing patterns and assertions.
*   `typescript-strict-mode`: For best practices in TypeScript usage.
*   `docker-compose-testing`: For setting up isolated test environments with Docker.

## Examples Directory Structure

```
examples/
├── basic-crud.test.ts          # Basic GET, POST, PUT, DELETE tests
├── authentication.test.ts      # Testing authenticated routes
├── error-handling.test.ts      # Testing various error scenarios
├── file-upload.test.ts         # Example of testing file uploads
├── mocking-external.test.ts    # Demonstrates mocking external services
└── setup-teardown.ts           # Database setup and teardown examples
```

## Custom Scripts Section

For `supertest-api`, the following automation scripts would save significant time:

1.  **`generate-api-test-boilerplate.sh`**: A shell script to quickly scaffold a new Supertest API test file with common imports, `describe` block, and a basic `GET` endpoint test.
2.  **`clear-test-db.py`**: A Python script to connect to a specified test database (e.g., MongoDB, PostgreSQL) and clear all collections/tables. Useful for ensuring a clean state before running tests, especially in CI/CD.
3.  **`update-api-schema-snapshots.sh`**: A shell script to run tests that generate API response snapshots and update them. This is crucial for maintaining up-to-date snapshots when API responses legitimately change.
4.  **`test-auth-flow.py`**: A Python script that simulates a full authentication flow (e.g., register, login, get token) and then makes a request to a protected endpoint, verifying the token's validity. Useful for quick smoke tests of the auth system.
