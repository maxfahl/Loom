import http from 'k6/http';
import { check, sleep } from 'k6';
import { Counter, Trend, Rate } from 'k6/metrics';
import { Options } from 'k6/options';

// Custom metrics
const successfulLogins = new Counter('successful_logins');
const failedLogins = new Counter('failed_logins');
const loginDuration = new Trend('login_duration');
const loginSuccessRate = new Rate('login_success_rate');

export const options: Options = {
  vus: 5,
  duration: '10s',
  thresholds: {
    // Built-in metrics
    http_req_failed: ['rate<0.01'],
    http_req_duration: ['p(95)<500'],
    // Custom metrics thresholds
    'successful_logins': ['count>10'], // Expect more than 10 successful logins
    'login_duration': ['p(99)<1000'], // 99% of login durations under 1 second
    'login_success_rate': ['rate>0.95'], // Login success rate should be above 95%
  },
};

export default function () {
  const res = http.post('https://reqres.in/api/login', JSON.stringify({
    email: 'eve.holt@reqres.in',
    password: 'cityslicka',
  }), {
    headers: { 'Content-Type': 'application/json' },
  });

  const isLoginSuccessful = check(res, {
    'login status is 200': (r) => r.status === 200,
  });

  // Record custom metrics
  if (isLoginSuccessful) {
    successfulLogins.add(1);
    loginSuccessRate.add(true);
  } else {
    failedLogins.add(1);
    loginSuccessRate.add(false);
  }
  loginDuration.add(res.timings.duration);

  sleep(1);
}
