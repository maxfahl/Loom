import http from 'k6/http';
import { check, sleep } from 'k6';
import { Options } from 'k6/options';

export const options: Options = {
  vus: 10, // 10 virtual users
  duration: '30s', // for 30 seconds
  thresholds: {
    http_req_failed: ['rate<0.01'], // http errors should be less than 1%
    http_req_duration: ['p(95)<200'], // 95% of requests should be below 200ms
  },
};

export default function () {
  const res = http.get('https://test.k6.io');
  check(res, {
    'is status 200': (r) => r.status === 200,
    'body contains "k6.io"': (r) => r.body ? r.body.includes('k6.io') : false,
  });
  sleep(1);
}
