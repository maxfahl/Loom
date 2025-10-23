import http from 'k6/http';
import { check, sleep } from 'k6';
import { Options } from 'k6/options';

const BASE_URL = __ENV.BASE_URL || 'https://reqres.in/api'; // Example API

export const options: Options = {
  vus: 5,
  duration: '10s',
  thresholds: {
    http_req_failed: ['rate<0.01'],
    http_req_duration: ['p(95)<500'],
  },
};

export default function () {
  // 1. Login to get a token
  const loginRes = http.post(`${BASE_URL}/login`, JSON.stringify({
    email: 'eve.holt@reqres.in',
    password: 'cityslicka',
  }), {
    headers: { 'Content-Type': 'application/json' },
  });

  check(loginRes, {
    'login successful': (r) => r.status === 200,
    'has token': (r) => r.json('token') !== undefined,
  });

  const token = loginRes.json('token');

  if (token) {
    // 2. Use the token to access a protected resource
    const usersRes = http.get(`${BASE_URL}/users?page=2`, {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
    });

    check(usersRes, {
      'get users successful': (r) => r.status === 200,
      'contains users data': (r) => r.json('data') !== undefined,
    });
  }

  sleep(1);
}
