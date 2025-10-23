# Modular Test Script Design

For larger k6 test suites, it's beneficial to organize your code into smaller, reusable modules. This improves readability, maintainability, and allows for easier collaboration.

## Pattern

Break down your k6 test script into logical modules, typically by functionality or API endpoint. Use `export` to expose functions and variables that can be imported and reused across different test files.

### `src/api/auth.ts`

```typescript
import http from 'k6/http';
import { check } from 'k6';

const BASE_URL = __ENV.BASE_URL || 'https://api.example.com';

export function login(username: string, password: string): string | null {
  const res = http.post(`${BASE_URL}/login`, JSON.stringify({
    username,
    password,
  }), {
    headers: { 'Content-Type': 'application/json' },
  });

  check(res, {
    'login successful': (r) => r.status === 200,
    'has token': (r) => r.json('token') !== undefined,
  });

  return res.json('token') as string | null;
}

export function logout(token: string): void {
  const res = http.post(`${BASE_URL}/logout`, null, {
    headers: {
      'Authorization': `Bearer ${token}`,
    },
  });
  check(res, { 'logout successful': (r) => r.status === 200 });
}
```

### `src/api/products.ts`

```typescript
import http from 'k6/http';
import { check } from 'k6';

const BASE_URL = __ENV.BASE_URL || 'https://api.example.com';

export function getProducts(token: string): any[] | null {
  const res = http.get(`${BASE_URL}/products`, {
    headers: {
      'Authorization': `Bearer ${token}`,
    },
  });
  check(res, { 'get products successful': (r) => r.status === 200 });
  return res.json() as any[] | null;
}

export function getProductById(token: string, productId: string): any | null {
  const res = http.get(`${BASE_URL}/products/${productId}`, {
    headers: {
      'Authorization': `Bearer ${token}`,
    },
  });
  check(res, { 'get product by ID successful': (r) => r.status === 200 });
  return res.json() as any | null;
}
```

### `src/tests/full-user-flow.ts`

```typescript
import { sleep } from 'k6';
import { Options } from 'k6/options';
import { login, logout } from '../api/auth';
import { getProducts, getProductById } from '../api/products';

export const options: Options = {
  vus: 5,
  duration: '30s',
  thresholds: {
    http_req_failed: ['rate<0.01'],
    http_req_duration: ['p(95)<500'],
  },
};

export default function () {
  const username = __ENV.TEST_USERNAME || 'testuser';
  const password = __ENV.TEST_PASSWORD || 'testpass';

  const token = login(username, password);
  if (token) {
    sleep(1);
    const products = getProducts(token);
    if (products && products.length > 0) {
      sleep(1);
      getProductById(token, products[0].id);
    }
    sleep(1);
    logout(token);
  }
  sleep(1);
}
```

## Benefits

*   **Reusability**: Functions like `login` or `getProducts` can be reused across multiple test scenarios.
*   **Maintainability**: Changes to an API endpoint only need to be updated in one place.
*   **Readability**: Test scripts become cleaner and easier to understand, focusing on the flow rather than implementation details.
*   **Collaboration**: Different team members can work on different modules simultaneously.
