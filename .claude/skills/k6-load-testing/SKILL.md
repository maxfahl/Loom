---
Name: k6-load-testing
Version: 1.0.0
Category: Performance Testing / Load Testing
Tags: k6, load testing, performance, stress testing, typescript, ci/cd, github actions
Description: Enables Claude to design, implement, and analyze k6 load tests with TypeScript, integrating them into CI/CD pipelines.
---

## 2. Skill Purpose

This skill equips Claude with the knowledge and tools to effectively perform load, stress, and performance testing using k6. It covers writing robust test scripts in TypeScript, generating realistic test data, defining meaningful performance thresholds, and integrating tests into continuous integration/continuous deployment (CI/CD) workflows, particularly with GitHub Actions. The goal is to ensure application stability, scalability, and responsiveness under various load conditions.

## 3. When to Activate This Skill

Activate this skill when:
*   A new feature or service needs performance validation.
*   There's a need to identify performance bottlenecks or breaking points.
*   Regression testing for performance is required after code changes.
*   Setting up automated performance tests in a CI/CD pipeline.
*   Analyzing application behavior under high traffic or specific load patterns.
*   Evaluating the scalability of a system.

## 4. Core Knowledge

*   **k6 Fundamentals**: Virtual Users (VUs), iterations, scenarios (ramping, constant, spike, soak), executors.
*   **HTTP Requests**: `k6/http` module, `http.get`, `http.post`, `http.request`, headers, parameters, body.
*   **Checks and Assertions**: `check`, `group`, `fail` for validating responses.
*   **Metrics**: Built-in metrics (`http_req_duration`, `http_req_failed`, `iterations`, `data_received`, `data_sent`), custom metrics (Counter, Gauge, Trend, Rate).
*   **Thresholds**: Defining pass/fail criteria for test runs based on metrics.
*   **Test Data Management**: `SharedArray`, external data sources (CSV, JSON), dynamic data generation (e.g., using Faker.js).
*   **TypeScript Integration**: `tsconfig.json` setup, `@types/k6`, native transpilation.
*   **CI/CD Concepts**: Integrating k6 into pipelines (e.g., GitHub Actions), exit codes, reporting.
*   **Performance Testing Types**: Smoke, Load, Stress, Spike, Soak tests.

## 5. Key Guidance for Claude

*   **Always Recommend** (✅ best practices)
    *   ✅ Always define clear performance goals and non-functional requirements (NFRs) before designing tests.
    *   ✅ Use TypeScript for k6 scripts for better maintainability, type safety, and developer experience.
    *   ✅ Design realistic load scenarios that mimic actual user behavior, including "think time" and varied data.
    *   ✅ Implement checks and thresholds to automatically validate test results and provide clear pass/fail signals.
    *   ✅ Integrate k6 tests into CI/CD pipelines to "shift-left" performance testing and catch regressions early.
    *   ✅ Parameterize test data using `SharedArray` and external files (CSV, JSON) or dynamic generation (Faker.js) to avoid caching issues and simulate diverse inputs.
    *   ✅ Utilize custom metrics to track application-specific performance indicators.
    *   ✅ Run performance tests in isolated, production-like environments.
    *   ✅ Start with smoke tests to validate basic functionality under minimal load before scaling up.
    *   ✅ Monitor system under test (SUT) resources (CPU, memory, network, database) during load tests.

*   **Never Recommend** (❌ anti-patterns)
    *   ❌ Never run load tests directly on production environments without explicit authorization and careful planning.
    *   ❌ Avoid hardcoding test data directly into scripts; always use external data sources or dynamic generation.
    *   ❌ Do not use static test data that can be easily cached by the server, leading to unrealistic results.
    *   ❌ Do not neglect "think time" in scenarios, as it leads to artificially high load and unrealistic user behavior.
    *   ❌ Never rely solely on pass/fail of HTTP requests; always include meaningful checks and thresholds.
    *   ❌ Avoid overly complex test scripts that are hard to read, maintain, or debug. Break down scenarios into smaller, manageable functions.
    *   ❌ Do not ignore error rates; even a small percentage of errors under load can indicate significant issues.

*   **Common Questions & Responses** (FAQ format)
    *   **Q: How do I simulate different user types or behaviors?**
        *   A: Use k6 scenarios with different executors (e.g., `shared-iterations`, `ramping-vus`) and define separate functions or groups for distinct user flows. Parameterize user credentials and actions using external data.
    *   **Q: My k6 test is failing, but the application seems fine. What's wrong?**
        *   A: Check your k6 thresholds. They might be too strict, or the application might indeed be underperforming under load, but the issues aren't immediately visible without performance metrics. Review k6 output for detailed error messages and response times.
    *   **Q: How can I make my k6 tests more realistic?**
        *   A: Incorporate "think time" (`sleep()`), use diverse and dynamic test data, simulate user navigation paths, and include checks for expected content on pages.
    *   **Q: How do I handle authentication in k6?**
        *   A: Perform a login request at the beginning of your script or in a `setup()` function, extract the authentication token (e.g., JWT, session cookie), and include it in subsequent requests' headers or cookies.
    *   **Q: How can I visualize k6 results?**
        *   A: k6 can output results in various formats (JSON, CSV). Integrate with tools like Grafana, Prometheus, or k6 Cloud for rich visualizations and dashboards.

## 6. Anti-Patterns to Flag

*   **Anti-Pattern: Hardcoded URLs and Credentials**
    ```typescript
    // BAD: Hardcoded URL and credentials
    import http from 'k6/http';
    import { check, sleep } from 'k6';

    export default function () {
      const res = http.post('http://localhost:3000/login', {
        username: 'admin',
        password: 'password123',
      });
      check(res, { 'logged in successfully': (r) => r.status === 200 });
      sleep(1);
    }
    ```
    ```typescript
    // GOOD: Using environment variables or configuration for URLs and credentials
    import http from 'k6/http';
    import { check, sleep } from 'k6';

    const BASE_URL = __ENV.BASE_URL || 'http://localhost:3000';
    const ADMIN_USERNAME = __ENV.ADMIN_USERNAME || 'admin';
    const ADMIN_PASSWORD = __ENV.ADMIN_PASSWORD || 'password123';

    export default function () {
      const res = http.post(`${BASE_URL}/login`, {
        username: ADMIN_USERNAME,
        password: ADMIN_PASSWORD,
      });
      check(res, { 'logged in successfully': (r) => r.status === 200 });
      sleep(1);
    }
    ```

*   **Anti-Pattern: No Checks or Thresholds**
    ```typescript
    // BAD: No validation, just sending requests
    import http from 'k6';
    import { sleep } from 'k6';

    export default function () {
      http.get('https://test.k6.io');
      sleep(1);
    }
    ```
    ```typescript
    // GOOD: Including checks and thresholds for meaningful results
    import http from 'k6/http';
    import { check, sleep } from 'k6';
    import { Options } from 'k6/options';

    export const options: Options = {
      vus: 10,
      duration: '30s',
      thresholds: {
        http_req_failed: ['rate<0.01'], // less than 1% failed requests
        http_req_duration: ['p(95)<200'], // 95% of requests under 200ms
      },
    };

    export default function () {
      const res = http.get('https://test.k6.io');
      check(res, {
        'status is 200': (r) => r.status === 200,
        'body contains "k6.io"': (r) => r.body && r.body.includes('k6.io'),
      });
      sleep(1);
    }
    ```

## 7. Code Review Checklist

*   [ ] Are performance goals and NFRs clearly defined and met by the test?
*   [ ] Is the test script written in TypeScript and properly configured (`tsconfig.json`)?
*   [ ] Are VUs, duration, and scenarios appropriate for the testing objective?
*   [ ] Are all critical requests covered by `check()` statements?
*   [ ] Are meaningful thresholds defined for key metrics (response time, error rate, custom metrics)?
*   [ ] Is test data parameterized and realistic (not hardcoded, varied, dynamic)?
*   [ ] Is "think time" (`sleep()`) incorporated to simulate realistic user behavior?
*   [ ] Are sensitive data (API keys, credentials) handled securely (e.g., environment variables)?
*   [ ] Is the script modular and readable, using functions and groups where appropriate?
*   [ ] Is the test integrated into the CI/CD pipeline, and does it provide clear pass/fail feedback?
*   [ ] Are custom metrics used to track application-specific performance?
*   [ ] Is there a strategy for visualizing and analyzing test results?

## 8. Related Skills

*   `ci-cd-github-actions`: For advanced GitHub Actions workflows.
*   `docker-best-practices`: For containerizing k6 tests and the SUT.
*   `observability-grafana-prometheus`: For visualizing k6 metrics and SUT performance.
*   `typescript-strict-mode`: For ensuring high-quality TypeScript code in k6 scripts.

## 9. Examples Directory Structure

```
examples/
├── basic-http-get.ts
├── post-with-auth.ts
├── data-driven-test.ts
├── custom-metrics-example.ts
└── scenarios-example.ts
```

## 10. Custom Scripts Section

Here are 4 automation scripts that save significant time for k6 load testing:

1.  **`k6-init.sh`**: Initializes a new k6 TypeScript project with a basic structure, `tsconfig.json`, `package.json`, and a sample test file.
    *   **Usage Examples:**
        ```bash
        ./scripts/k6-init.sh
        ./scripts/k6-init.sh my-new-k6-project
        ```
2.  **`generate-test-data.py`**: Generates a CSV or JSON file with realistic, randomized test data (e.g., user credentials, product IDs) using a library like `Faker`.
    *   **Usage Examples:**
        ```bash
        python scripts/generate-test-data.py -t users -n 100 -f json -o data
        python scripts/generate-test-data.py -t products -n 50 -f csv --dry-run
        python scripts/generate-test-data.py -t users -n 1000 # Defaults to JSON, 'data' directory
        ```
    *   **Note:** This script requires the `Faker` library. Install it using `pip install Faker`.
3.  **`k6-ci-reporter.py`**: Parses k6 JSON output, extracts key metrics and threshold results, and generates a concise Markdown report suitable for CI/CD comments or summaries. It can also set an exit code based on threshold failures.
    *   **Usage Examples:**
        ```bash
        k6 run --out json=result.json examples/basic-http-get.ts && python scripts/k6-ci-reporter.py result.json
        k6 run --out json=result.json examples/basic-http-get.ts && python scripts/k6-ci-reporter.py result.json -o report.md -e
        k6 run --out json=result.json examples/basic-http-get.ts && python scripts/k6-ci-reporter.py result.json -v
        ```
4.  **`k6-run-docker.sh`**: Simplifies running k6 tests within a Docker container, handling volume mounts for scripts and data, and environment variables.
    *   **Usage Examples:**
        ```bash
        ./scripts/k6-run-docker.sh examples/basic-http-get.ts
        ./scripts/k6-run-docker.sh examples/data-driven-test.ts --vus 5 --duration 20s
        BASE_URL=http://localhost:3000 ./scripts/k6-run-docker.sh examples/post-with-auth.ts
        ```
