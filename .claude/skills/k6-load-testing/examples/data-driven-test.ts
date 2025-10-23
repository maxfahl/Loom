import http from 'k6/http';
import { SharedArray } from 'k6/data';
import { check, sleep } from 'k6';
import { Options } from 'k6/options';

const BASE_URL = __ENV.BASE_URL || 'https://test-api.k6.io';

// Load data from a JSON file using SharedArray
// This data will be shared across all VUs and iterations
const users = new SharedArray('users', function () {
  // Load JSON file from the current directory
  return JSON.parse(open('./users.json')).users;
});

export const options: Options = {
  scenarios: {
    dataDriven: {
      executor: 'shared-iterations',
      vus: 10,
      iterations: users.length, // One iteration per user in the data file
      maxDuration: '1m',
    },
  },
  thresholds: {
    http_req_failed: ['rate<0.01'],
    http_req_duration: ['p(95)<300'],
  },
};

export default function () {
  // Get a unique user for each iteration
  const user = users[__VU - 1]; // __VU is 1-indexed

  // Simulate a login request with user data
  const loginRes = http.post(`${BASE_URL}/login`, {
    username: user.username,
    password: user.password,
  });

  check(loginRes, {
    'login successful': (r) => r.status === 200,
    'has session token': (r) => r.headers.hasOwnProperty('X-Session-Token'),
  });

  sleep(1);
}
