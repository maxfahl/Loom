---
Name: playwright-e2e
Version: 0.1.0
Category: Testing / E2E
Tags: playwright, e2e testing, end-to-end, typescript, web testing, browser automation, ci/cd
Description: Enables Claude to write, maintain, and debug robust end-to-end tests for web applications using Playwright and TypeScript.
---

## Skill Purpose

This skill enables Claude to effectively write, understand, and debug end-to-end (E2E) tests for modern web applications using the Playwright testing framework in a TypeScript environment. It focuses on best practices for simulating user interactions, asserting UI states, managing test data, handling authentication, and integrating with CI/CD pipelines.

## When to Activate This Skill

Activate this skill when the user is:
- Asking to write new E2E tests for a web application.
- Debugging existing Playwright-based E2E tests.
- Refactoring E2E tests to improve readability, maintainability, or performance.
- Setting up a new web project and needs guidance on E2E testing infrastructure.
- Discussing strategies for testing complex user flows, authentication, or cross-browser compatibility.
- Reviewing pull requests that involve changes to E2E tests.

Specific keywords or patterns that indicate this skill is needed:
- "write E2E tests with Playwright"
- "Playwright end-to-end testing"
- "testing web UI with TypeScript"
- "how to handle authentication in Playwright"
- "Page Object Model Playwright"
- "Playwright CI/CD integration"
- "visual regression testing Playwright"

## Core Knowledge

The fundamental concepts, patterns, and APIs Claude needs to know:

1.  **Playwright Basics**:
    *   `page` object: The primary interface for interacting with a web page.
    *   Locators: `page.locator()`, `page.getByRole()`, `page.getByText()`, `page.getByLabel()`, etc.
    *   Actions: `click()`, `fill()`, `type()`, `press()`, `check()`, `selectOption()`, `navigate()`, `goBack()`, `waitForURL()`, `waitForSelector()`.
    *   Assertions: `expect(locator).toBeVisible()`, `expect(locator).toHaveText()`, `expect(page).toHaveURL()`, `expect(page).toHaveTitle()`, `expect(locator).toHaveAttribute()`, `expect(locator).toHaveClass()`.
    *   Test structure: `test()`, `test.describe()`, `test.beforeEach()`, `test.afterEach()`, `test.beforeAll()`, `test.afterAll()`.
    *   Test fixtures: `page`, `context`, `browser`, `request`.

2.  **TypeScript Specifics**:
    *   Type definitions (`@playwright/test`).
    *   Configuring `tsconfig.json` for Playwright tests.
    *   Strong typing for page objects, test data, and assertions.

3.  **E2E Testing Patterns**:
    *   **Test Isolation**: Each test runs in an isolated browser context.
    *   **Page Object Model (POM)**: Encapsulating page interactions and selectors into reusable classes.
    *   **Data-Driven Testing**: Using test data generators (e.g., Faker.js) for realistic and varied inputs.
    *   **Authentication Handling**: Using `storageState` or API calls for efficient login.
    *   **Network Mocking**: Intercepting and mocking API requests/responses using `page.route()`.
    *   **Visual Regression Testing**: Comparing screenshots against baselines to detect UI changes.
    *   **Accessibility Testing**: Integrating accessibility checks.
    *   **Error Handling**: Testing application behavior under various error conditions.

4.  **Playwright Tooling**:
    *   Playwright Inspector (`npx playwright codegen`).
    *   Trace Viewer (`npx playwright show-report`).
    *   Screenshots and videos.

5.  **CI/CD Integration**:
    *   Running tests in headless mode.
    *   Parallel execution.
    *   Generating test reports.

## Key Guidance for Claude

### Always Recommend (✅ best practices)

*   ✅ **Use Playwright Locators**: Prefer `page.getByRole()`, `page.getByText()`, `page.getByLabel()`, etc., over generic CSS selectors for robustness and readability.
*   ✅ **Implement Page Object Model (POM)**: Structure tests using POM to improve maintainability, reduce code duplication, and make tests easier to understand.
*   ✅ **Leverage Automatic Waiting**: Rely on Playwright's built-in auto-waiting mechanisms. Avoid `page.waitForTimeout()` (fixed delays) as they lead to flaky tests.
*   ✅ **Isolate Tests**: Ensure each test is independent and does not rely on the state of previous tests. Use `test.beforeEach()` and `test.afterEach()` for setup and teardown.
*   ✅ **Handle Authentication Efficiently**: Use `storageState` to persist authentication across tests or perform API logins directly to bypass UI login flows for speed.
*   ✅ **Mock External Network Requests**: Intercept and mock API calls to external services using `page.route()` to ensure tests are fast, reliable, and independent of third-party availability.
*   ✅ **Write Descriptive Test Titles**: Use clear and concise `test.describe()` and `test()` titles that explain the user flow being tested.
*   ✅ **Focus on User Flows**: Design tests to mimic real user interactions and verify the application's behavior from the user's perspective.
*   ✅ **Utilize Playwright's Debugging Tools**: Use Playwright Inspector, Trace Viewer, and screenshots to efficiently debug failing tests.
*   ✅ **Integrate with CI/CD**: Configure tests to run in headless mode in CI/CD pipelines for automated feedback.

### Never Recommend (❌ anti-patterns)

*   ❌ **Hard-coded `waitForTimeout`**: Never use fixed delays. They make tests slow and flaky. Always rely on Playwright's auto-waiting or explicit `page.waitForSelector()`, `page.waitForURL()`, etc.
*   ❌ **Fragile Selectors**: Avoid relying on volatile CSS classes or deeply nested DOM structures. Prefer role-based or text-based locators.
*   ❌ **Testing External Services**: Do not make actual calls to third-party APIs or external services within E2E tests. Mock them instead.
*   ❌ **Shared State Between Tests**: Avoid tests that modify global state or rely on side effects from other tests. This leads to unpredictable results.
*   ❌ **Overly Long Tests**: Keep individual test cases focused on a single user flow or a small set of related interactions. Break down complex scenarios.
*   ❌ **Ignoring Error States**: Do not only test happy paths. Explicitly test how the application handles invalid inputs, network errors, and other error conditions.
*   ❌ **Direct DOM Manipulation**: Avoid directly manipulating the DOM in tests. Interact with elements as a user would (click, fill, type).

### Common Questions & Responses (FAQ format)

*   **Q: How do I handle dynamic data in tests?**
    *   **A:** Use a data generation library like `Faker.js` to create realistic but random test data. For data that needs to persist or be consistent, consider seeding your test database before tests run.
*   **Q: My tests are flaky. What should I do?**
    *   **A:**
        1.  **Review selectors**: Ensure you are using robust Playwright locators.
        2.  **Remove `waitForTimeout`**: Replace fixed delays with explicit waits for conditions.
        3.  **Isolate tests**: Verify that tests are not interfering with each other's state.
        4.  **Use `trace: 'on'`**: Analyze traces to understand what happened during a flaky run.
        5.  **Retry failed tests**: Configure Playwright to retry failed tests (`retries` in config).
*   **Q: How can I test file downloads?**
    *   **A:** Use `page.waitForEvent('download')` to capture download events. You can then save the downloaded file and assert its content or properties.
*   **Q: How do I interact with elements inside an iframe?**
    *   **A:** Use `page.frameLocator('iframeSelector').locator('elementInsideIframeSelector')` to target elements within iframes.
*   **Q: How can I run tests across different browsers?**
    *   **A:** Playwright supports Chromium, Firefox, and WebKit. Configure your `playwright.config.ts` to include different projects for each browser, and Playwright will run your tests across them.

## Anti-Patterns to Flag

### BAD: Using `waitForTimeout` and fragile selectors

```typescript
// bad-login.test.ts
import { test, expect } from '@playwright/test';

test('should log in a user (BAD)', async ({ page }) => {
  await page.goto('http://localhost:3000/login');
  await page.waitForTimeout(2000); // BAD: Fixed wait
  await page.fill('.username-input', 'testuser'); // BAD: Fragile class selector
  await page.fill('#passwordField', 'testpassword');
  await page.click('button.submit-btn'); // BAD: Fragile class selector
  await page.waitForTimeout(3000); // BAD: Fixed wait
  await expect(page.locator('h1.welcome-message')).toHaveText('Welcome, testuser!');
});
```

### GOOD: Leveraging Playwright locators and auto-waiting

```typescript
// good-login.test.ts
import { test, expect } from '@playwright/test';

test('should log in a user (GOOD)', async ({ page }) => {
  await page.goto('http://localhost:3000/login');
  // GOOD: Playwright auto-waits for elements to be actionable
  await page.getByLabel('Username').fill('testuser');
  await page.getByLabel('Password').fill('testpassword');
  await page.getByRole('button', { name: 'Log In' }).click();
  // GOOD: Wait for navigation or specific element to appear
  await expect(page.getByRole('heading', { name: 'Welcome, testuser!' })).toBeVisible();
});
```

## Code Review Checklist

*   [ ] Are Playwright's built-in locators (e.g., `getByRole`, `getByText`) used predominantly?
*   [ ] Is the Page Object Model (POM) implemented for complex pages/components?
*   [ ] Are there any instances of `page.waitForTimeout()`? If so, can they be replaced with explicit waits or auto-waiting?
*   [ ] Is each test isolated and independent of other tests?
*   [ ] Is authentication handled efficiently (e.g., `storageState`, API login)?
*   [ ] Are external network requests mocked using `page.route()`?
*   [ ] Are test titles clear, concise, and descriptive of the user flow?
*   [ ] Are assertions specific and verify user-visible behavior?
*   [ ] Is TypeScript used effectively for type safety?
*   [ ] Are tests configured for headless execution in CI/CD?
*   [ ] Are screenshots/videos captured on failure for debugging?

## Related Skills

*   `react-hooks`: For understanding React component interactions.
*   `nextjs-app-router`: For testing Next.js applications.
*   `typescript-strict-mode`: For best practices in TypeScript usage.
*   `docker-compose-testing`: For setting up isolated test environments with Docker.

## Examples Directory Structure

```
examples/
├── basic-navigation.spec.ts    # Basic page navigation and element interaction
├── login-flow.spec.ts          # User login/logout flow with authentication handling
├── form-submission.spec.ts     # Testing form filling and submission
├── data-grid-interaction.spec.ts # Interacting with dynamic data grids/tables
├── network-mocking.spec.ts     # Mocking API responses for specific tests
├── visual-regression.spec.ts   # Example of visual regression testing
└── pom-example/                # Directory for Page Object Model examples
    ├── pages/                  # Page object classes
    │   ├── LoginPage.ts
    │   └── DashboardPage.ts
    └── pom.spec.ts             # Tests using Page Object Model
```

## Custom Scripts Section

For `playwright-e2e`, the following automation scripts would save significant time:

1.  **`generate-playwright-page-object.sh`**: A shell script to scaffold a new Playwright Page Object Model (POM) file, including basic structure, locators, and common interaction methods.
2.  **`run-visual-regression-tests.sh`**: A shell script to execute Playwright tests specifically tagged for visual regression, potentially generating or updating baselines.
3.  **`clean-playwright-artifacts.sh`**: A shell script to remove Playwright test artifacts (screenshots, videos, traces, test reports) to keep the project clean and manage disk space.
4.  **`playwright-auth-setup.py`**: A Python script to perform a login via Playwright and save the `storageState` to a file, which can then be used by other tests to bypass the login UI. This is useful for setting up authenticated contexts efficiently.
