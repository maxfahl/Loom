import http from 'k6/http';
import { check, sleep } from 'k6';
import { Options } from 'k6/options';

export const options: Options = {
  scenarios: {
    // Scenario 1: Smoke test - quickly verify system is up
    smoke: {
      executor: 'constant-vus',
      vus: 1,
      duration: '10s',
      tags: { test_type: 'smoke' },
      exec: 'smokeTest', // function to execute
    },
    // Scenario 2: Load test - simulate typical user load
    load: {
      executor: 'ramping-vus',
      startVUs: 0,
      stages: [
        { duration: '30s', target: 10 }, // ramp up to 10 VUs over 30s
        { duration: '1m', target: 10 },  // stay at 10 VUs for 1 minute
        { duration: '30s', target: 0 },  // ramp down to 0 VUs over 30s
      ],
      tags: { test_type: 'load' },
      exec: 'loadTest', // function to execute
    },
    // Scenario 3: Spike test - sudden increase in load
    spike: {
      executor: 'spike',
      vus: 50, // Max VUs during spike
      duration: '1m',
      timeUnit: '1s',
      stages: [
        { duration: '10s', target: 0 }, // initial calm
        { duration: '5s', target: 50 }, // spike up to 50 VUs
        { duration: '45s', target: 0 }, // ramp down
      ],
      tags: { test_type: 'spike' },
      exec: 'loadTest', // function to execute
    },
  },
  thresholds: {
    // Apply thresholds globally or per scenario using tags
    'http_req_failed{test_type:smoke}': ['rate<0.05'],
    'http_req_duration{test_type:smoke}': ['p(99)<500'],
    'http_req_failed{test_type:load}': ['rate<0.01'],
    'http_req_duration{test_type:load}': ['p(95)<200'],
    'http_req_failed{test_type:spike}': ['rate<0.10'], // Higher error rate tolerated for spike
    'http_req_duration{test_type:spike}': ['p(90)<1000'], // Higher duration tolerated for spike
  },
};

export function smokeTest() {
  http.get('https://test.k6.io/contacts.php');
  sleep(0.5);
}

export function loadTest() {
  http.get('https://test.k6.io');
  sleep(1);
  http.get('https://test.k6.io/news.php');
  sleep(1);
}
