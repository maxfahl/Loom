---
name: test-automation-frameworks
version: 1.0.0
category: Quality Assurance / Testing
tags: Playwright, Selenium, TypeScript, E2E, UI Testing, Automation, QA
description: Guides Claude on implementing robust end-to-end test automation using Playwright and Selenium with TypeScript.
---

# Test Automation Frameworks (Playwright, Selenium)

## 1. Skill Purpose

This skill enables Claude to design, implement, and maintain robust and scalable end-to-end (E2E) test automation suites using modern frameworks like Playwright and Selenium, with a strong emphasis on TypeScript for type safety and maintainability. It covers best practices for writing stable, readable, and efficient tests that integrate seamlessly into CI/CD pipelines.

## 2. When to Activate This Skill

Activate this skill when:
*   A new E2E test suite needs to be set up for a web application.
*   Existing E2E tests are flaky, slow, or hard to maintain.
*   There's a need to refactor or improve the structure of an automation framework.
*   Cross-browser compatibility testing is required.
*   Performance or reliability issues are identified in the current test automation.
*   Integrating E2E tests into a CI/CD pipeline.
*   Debugging complex E2E test failures.

## 3. Core Knowledge

### Frameworks: Playwright vs. Selenium

*   **Playwright**: A modern automation framework from Microsoft, offering fast, reliable, and capable E2E testing across Chromium, Firefox, and WebKit with a single API. It includes auto-wait, test isolation, and powerful debugging tools. Preferred for new projects due to its modern architecture and performance.
*   **Selenium WebDriver**: A widely adopted, older framework that automates browsers. While powerful, it often requires more boilerplate and external libraries for features like auto-wait and reporting. Still relevant for legacy projects or specific browser requirements not fully met by Playwright.

### Key Concepts

*   **Page Object Model (POM)**: A design pattern that treats web pages as classes, encapsulating elements and interactions. Enhances reusability, readability, and maintainability.
*   **Selectors**: Strategies for locating elements on a web page (e.g., CSS selectors, XPath, text, role, test IDs). Prioritize stable and resilient selectors.
*   **Waiting Strategies**: Mechanisms to synchronize test execution with dynamic web content. Explicit waits (waiting for specific conditions) are crucial; implicit waits are less reliable. Playwright's auto-wait is a significant advantage.
*   **Assertions**: Verifying expected outcomes. Use framework-specific assertion libraries (e.g., Playwright's `expect`, Chai with Selenium).
*   **Test Isolation**: Ensuring each test runs in a clean, independent environment to prevent side effects. Playwright provides this by default with isolated browser contexts.
*   **TypeScript Integration**: Leveraging static typing for early error detection, improved code readability, and better refactoring capabilities.

## 4. Key Guidance for Claude

### Always Recommend (✅ Best Practices)

*   **✅ Adopt Page Object Model (POM)**: Structure tests using POM for better organization, reusability, and maintainability. Each page or component should have its own class.
*   **✅ Use Stable and Resilient Selectors**: Prioritize `data-testid` attributes, unique IDs, or semantic locators (e.g., `getByRole` in Playwright) over fragile CSS classes or XPath that might change frequently.
*   **✅ Implement Explicit Waits**: Always wait for elements to be visible, clickable, or present before interacting with them. Avoid arbitrary `sleep()` or `setTimeout()` calls. Playwright's auto-wait handles many common scenarios.
*   **✅ Leverage TypeScript for Type Safety**: Define interfaces and types for page objects, test data, and utility functions. Avoid `any` where possible to catch errors at compile time.
*   **✅ Design for Test Isolation**: Ensure tests are independent and can run in any order without affecting each other. Playwright's `browserContext` provides this by default.
*   **✅ Integrate with CI/CD**: Automate test execution in CI/CD pipelines to catch regressions early.
*   **✅ Enable Cross-Browser Testing**: Configure tests to run across multiple browsers (Chromium, Firefox, WebKit for Playwright; various WebDriver implementations for Selenium).
*   **✅ Use `async/await` for Asynchronous Operations**: Write asynchronous test code in a synchronous-looking manner for better readability and error handling.
*   **✅ Generate Comprehensive Reports**: Utilize built-in or third-party reporters (e.g., Playwright HTML Reporter, Allure) for clear test results and debugging information.
*   **✅ Capture Screenshots/Videos on Failure**: Automatically capture visual evidence for failed tests to aid in debugging.

### Never Recommend (❌ Anti-Patterns)

*   **❌ Hardcoding `sleep()` or `setTimeout()`**: These lead to flaky tests and slow execution. Always use explicit waits.
*   **❌ Fragile Selectors**: Avoid relying solely on dynamically generated CSS classes or deeply nested XPath expressions that are prone to breaking with minor UI changes.
*   **❌ Testing Third-Party Integrations**: Do not include external APIs or services that are outside the application's control in E2E tests. Mock or stub these dependencies.
*   **❌ Excessive Use of `any` in TypeScript**: This defeats the purpose of TypeScript. Strive for strong typing to improve code quality and catch errors early.
*   **❌ Mixing Assertions with Page Object Logic**: Page Objects should only contain element locators and interactions. Assertions belong in the test files.
*   **❌ Ignoring Test Failures**: Every failed test indicates a potential bug or a flaw in the test itself. Investigate and fix promptly.

### Common Questions & Responses

*   **Q: My tests are flaky. What should I do?**
    *   **A:** Flakiness often stems from improper waiting strategies or unstable selectors. Review your waits to ensure explicit conditions are met before interactions. Refactor selectors to use `data-testid` or more robust attributes. Consider Playwright's auto-wait capabilities.
*   **Q: How do I handle dynamic content or AJAX calls?**
    *   **A:** Use explicit waits that target the dynamic content. For example, wait for a specific element to appear, disappear, or for a network request to complete. Playwright's `waitForLoadState`, `waitForSelector`, and network interception features are very useful here.
*   **Q: Should I use Playwright or Selenium?**
    *   **A:** For new projects, Playwright is generally recommended due to its modern architecture, faster execution, built-in auto-wait, and better debugging experience. Selenium is a mature choice for existing projects or when specific browser/driver support is critical.
*   **Q: How can I make my tests run faster?**
    *   **A:** Optimize selectors, reduce unnecessary waits, run tests in parallel (both Playwright and Selenium support this), and ensure your test environment is performant. Consider mocking external dependencies.
*   **Q: How do I manage test data?**
    *   **A:** Avoid hardcoding. Use test data factories, fixtures, or external data sources (e.g., JSON files, databases, APIs) to generate or retrieve data. Parameterize tests where possible.

## 5. Anti-Patterns to Flag

### Anti-Pattern 1: Hardcoded Waits

**BAD:**
```typescript
// tests/bad-login.spec.ts
import { test, expect } from '@playwright/test';

test('should log in a user - BAD', async ({ page }) => {
  await page.goto('http://localhost:3000/login');
  await page.fill('#username', 'testuser');
  await page.fill('#password', 'password123');
  await page.click('button[type="submit"]');
  // ❌ Hardcoded wait - prone to flakiness and slows down tests
  await page.waitForTimeout(5000);
  await expect(page.locator('.welcome-message')).toContainText('Welcome, testuser!');
});
```

**GOOD:**
```typescript
// tests/good-login.spec.ts
import { test, expect } from '@playwright/test';

test('should log in a user - GOOD', async ({ page }) => {
  await page.goto('http://localhost:3000/login');
  await page.fill('#username', 'testuser');
  await page.fill('#password', 'password123');
  await page.click('button[type="submit"]');
  // ✅ Explicit wait for an element to appear after login
  await expect(page.locator('.welcome-message')).toContainText('Welcome, testuser!');
  // Playwright's auto-wait handles waiting for the element to be visible and stable
});
```

### Anti-Pattern 2: Fragile Selectors

**BAD:**
```typescript
// pages/bad-home.page.ts
import { Page } from '@playwright/test';

export class BadHomePage {
  constructor(public page: Page) {}

  // ❌ Fragile selector based on deep nesting and generic classes
  get productTitle() {
    return this.page.locator('div.container > div:nth-child(2) > div.card > h2.product-name');
  }

  async navigateToProductDetails() {
    await this.page.click('div.container > div:nth-child(2) > div.card > button.view-details');
  }
}
```

**GOOD:**
```typescript
// pages/good-home.page.ts
import { Page } from '@playwright/test';

export class GoodHomePage {
  constructor(public page: Page) {}

  // ✅ Robust selector using data-testid attribute
  get productTitle() {
    return this.page.locator('[data-testid="product-name"]');
  }

  async navigateToProductDetails(productName: string) {
    // ✅ Using a more semantic and stable way to locate the button
    await this.page.locator(`[data-testid="product-card-${productName}"] button[data-testid="view-details-button"]`).click();
  }
}
```

### Anti-Pattern 3: Mixing Assertions in Page Objects

**BAD:**
```typescript
// pages/bad-dashboard.page.ts
import { Page, expect } from '@playwright/test';

export class BadDashboardPage {
  constructor(public page: Page) {}

  get welcomeMessage() {
    return this.page.locator('#welcomeMessage');
  }

  // ❌ Assertion within a Page Object method
  async verifyWelcomeMessage(expectedText: string) {
    await expect(this.welcomeMessage).toContainText(expectedText);
  }
}

// tests/bad-dashboard.spec.ts
import { test } from '@playwright/test';
import { BadDashboardPage } from '../pages/bad-dashboard.page';

test('should display welcome message - BAD', async ({ page }) => {
  const dashboardPage = new BadDashboardPage(page);
  await page.goto('/dashboard');
  await dashboardPage.verifyWelcomeMessage('Welcome, Admin!'); // Test logic is hidden
});
```

**GOOD:**
```typescript
// pages/good-dashboard.page.ts
import { Page } from '@playwright/test';

export class GoodDashboardPage {
  constructor(public page: Page) {}

  get welcomeMessage() {
    return this.page.locator('#welcomeMessage');
  }

  // ✅ Page Object only exposes elements and actions, no assertions
  async getWelcomeMessageText(): Promise<string> {
    return await this.welcomeMessage.textContent() || '';
  }
}

// tests/good-dashboard.spec.ts
import { test, expect } from '@playwright/test';
import { GoodDashboardPage } from '../pages/good-dashboard.page';

test('should display welcome message - GOOD', async ({ page }) => {
  const dashboardPage = new GoodDashboardPage(page);
  await page.goto('/dashboard');
  // ✅ Assertion is in the test file, making test intent clear
  await expect(dashboardPage.welcomeMessage).toContainText('Welcome, Admin!');
});
```

## 6. Code Review Checklist

*   [ ] **Page Object Model (POM)**: Are all page interactions and element locators encapsulated within Page Objects?
*   [ ] **Selector Strategy**: Are selectors stable, resilient, and prioritized by `data-testid`, ID, or semantic roles?
*   [ ] **Waiting Strategy**: Are explicit waits used instead of hardcoded `sleep()`? Is Playwright's auto-wait leveraged effectively?
*   [ ] **Type Safety**: Is TypeScript used effectively to define types and interfaces? Is the use of `any` minimized?
*   [ ] **Test Isolation**: Does each test run independently without side effects from other tests?
*   [ ] **Readability**: Are test names and steps clear and descriptive? Is the code clean and easy to understand?
*   [ ] **Assertions**: Are assertions placed in test files, not within Page Objects? Are they clear and specific?
*   [ ] **Error Handling**: Are potential errors (e.g., element not found) handled gracefully, and are screenshots/videos captured on failure?
*   [ ] **Configuration**: Is the test configuration (e.g., `playwright.config.ts`, `tsconfig.json`) optimized and well-documented?
*   [ ] **CI/CD Readiness**: Can the tests be easily integrated and run in a CI/CD pipeline?

## 7. Related Skills

*   `typescript-strict-mode`: For advanced TypeScript configuration and usage.
*   `ci-cd-pipeline-implementation`: For integrating test automation into CI/CD.
*   `docker-containerization`: For running tests in isolated Docker environments.
*   `jest-unit-tests`: For understanding unit testing principles that complement E2E testing.

## 8. Examples Directory Structure

```
examples/
├── playwright-typescript/
│   ├── pages/
│   │   ├── base.page.ts
│   │   ├── login.page.ts
│   │   └── dashboard.page.ts
│   ├── tests/
│   │   ├── login.spec.ts
│   │   └── dashboard.spec.ts
│   ├── playwright.config.ts
│   └── tsconfig.json
└── selenium-typescript/
    ├── pages/
    │   ├── base.page.ts
    │   ├── login.page.ts
    │   └── dashboard.page.ts
    ├── tests/
    │   ├── login.spec.ts
    │   └── dashboard.spec.ts
    ├── selenium.config.ts
    └── tsconfig.json
```

## 9. Custom Scripts Section

This section outlines automation scripts designed to streamline common tasks in test automation frameworks, saving significant developer time.

*   **`generate-page-object.sh`**: A shell script to quickly scaffold a new Page Object file with basic structure.
*   **`test-data-generator.py`**: A Python script to generate realistic, randomized test data for various scenarios.
*   **`run-e2e-tests.sh`**: A shell script to execute E2E tests with configurable options for browser, parallelization, and reporting.
*   **`selector-analyzer.py`**: A Python script to analyze existing selectors for fragility and suggest improvements.
*   **`ci-test-reporter.sh`**: A shell script to process test results and generate a summary report suitable for CI/CD pipelines.
