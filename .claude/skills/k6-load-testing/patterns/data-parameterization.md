# Data Parameterization

Realistic load testing requires diverse and dynamic test data to simulate real-world user interactions and prevent server-side caching from skewing results. k6 offers several ways to parameterize data.

## Pattern: Using `SharedArray` with JSON/CSV

`SharedArray` is the most efficient way to load large datasets into k6. It loads the data once into memory and shares it across all Virtual Users (VUs), avoiding redundant loading.

### `data/users.json` (example data file)

```json
[
  { "username": "user1", "password": "pass1" },
  { "username": "user2", "password": "pass2" },
  { "username": "user3", "password": "pass3" },
  { "username": "user4", "password": "pass4" },
  { "username": "user5", "password": "pass5" }
]
```

### `data-driven-login.ts` (k6 script)

```typescript
import http from 'k6/http';
import { SharedArray } from 'k6/data';
import { check, sleep } from 'k6';
import { Options } from 'k6/options';

const BASE_URL = __ENV.BASE_URL || 'https://api.example.com';

// Load user data from JSON file using SharedArray
const users = new SharedArray('users', function () {
  // Ensure the path to your data file is correct relative to where k6 is run
  return JSON.parse(open('./data/users.json'));
});

export const options: Options = {
  scenarios: {
    dataDrivenLogin: {
      executor: 'shared-iterations',
      vus: 5,
      iterations: users.length, // One iteration per user in the data file
      maxDuration: '1m',
      // Each VU gets a unique iteration, ensuring each user is used once
      // If you need VUs to pick random users, use `per-vu-iterations` and `users[Math.floor(Math.random() * users.length)]`
    },
  },
  thresholds: {
    http_req_failed: ['rate<0.01'],
    http_req_duration: ['p(95)<300'],
  },
};

export default function () {
  // Get a unique user for each iteration (when using shared-iterations)
  const user = users[__VU - 1]; // __VU is 1-indexed, so adjust for 0-indexed array

  // Simulate a login request with user data
  const loginRes = http.post(`${BASE_URL}/login`, JSON.stringify({
    username: user.username,
    password: user.password,
  }), {
    headers: { 'Content-Type': 'application/json' },
  });

  check(loginRes, {
    'login successful': (r) => r.status === 200,
    'has session token': (r) => r.headers.hasOwnProperty('X-Session-Token'),
  });

  sleep(1);
}
```

## Pattern: Dynamic Data Generation with `Faker.js`

For generating unique, realistic data on the fly, especially for fields like names, emails, addresses, etc., `Faker.js` (or similar libraries) can be used. While k6 doesn't directly support Node.js modules, you can use a bundler like Webpack or `esbuild` to bundle `Faker.js` with your k6 script, or generate data beforehand.

### `generate-faker-data.ts` (k6 script - requires bundling if used directly in k6)

```typescript
// This example assumes Faker.js is bundled or data is pre-generated.
// For direct k6 execution, consider pre-generating data with a separate script.

import http from 'k6/http';
import { check, sleep } from 'k6';
import { Options } from 'k6/options';
// import { faker } from '@faker-js/faker'; // Uncomment if bundled

const BASE_URL = __ENV.BASE_URL || 'https://api.example.com';

export const options: Options = {
  vus: 10,
  duration: '30s',
  thresholds: {
    http_req_failed: ['rate<0.01'],
    http_req_duration: ['p(95)<500'],
  },
};

export default function () {
  // Example of generating dynamic data (if faker is available)
  // const firstName = faker.person.firstName();
  // const lastName = faker.person.lastName();
  // const email = faker.internet.email({ firstName, lastName });
  // const password = faker.internet.password();

  // For demonstration, using static data or pre-generated data
  const firstName = `TestUser${__VU}`;
  const lastName = `LastName${__ITER}`;
  const email = `testuser${__VU}-${__ITER}@example.com`;
  const password = `Password${__VU}${__ITER}!`;

  const res = http.post(`${BASE_URL}/register`, JSON.stringify({
    firstName,
    lastName,
    email,
    password,
  }), {
    headers: { 'Content-Type': 'application/json' },
  });

  check(res, {
    'registration successful': (r) => r.status === 201,
  });

  sleep(1);
}
```

## Benefits

*   **Realism**: Simulates diverse user inputs, making tests more representative of real-world usage.
*   **Prevents Caching**: Unique data for each request helps prevent server-side caching from distorting performance metrics.
*   **Scalability**: Easily generate large volumes of data for high-load scenarios.
*   **Flexibility**: Adapt data generation to specific test requirements (e.g., valid vs. invalid inputs).

## Considerations

*   **Data Volume**: For very large datasets, ensure your test environment has enough memory when using `SharedArray`.
*   **Data Uniqueness**: Ensure generated data is unique if required by your application (e.g., unique email addresses for registration).
*   **Pre-generation vs. On-the-fly**: Decide whether to pre-generate data before the test run or generate it dynamically within the script, considering performance implications and complexity.
