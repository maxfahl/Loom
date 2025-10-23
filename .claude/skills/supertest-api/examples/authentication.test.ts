// examples/authentication.test.ts

import request from 'supertest';
import app from '../../src/app'; // Adjust path to your Express app as needed

describe('Authentication API Tests', () => {
  const testUser = { username: 'authuser', password: 'authpassword' };
  let authToken: string;

  beforeAll(async () => {
    // Attempt to register the user first, ignore if already exists
    await request(app).post('/auth/register').send(testUser);

    // Log in to get a token
    const res = await request(app).post('/auth/login').send(testUser);
    expect(res.statusCode).toBe(200);
    expect(res.body).toHaveProperty('access_token');
    authToken = res.body.access_token;
  });

  it('should return 401 for a protected route without a token', async () => {
    const res = await request(app).get('/api/protected');
    expect(res.statusCode).toBe(401); // Unauthorized
    expect(res.body).toHaveProperty('message', 'Unauthorized');
  });

  it('should return 401 for a protected route with an invalid token', async () => {
    const res = await request(app)
      .get('/api/protected')
      .set('Authorization', 'Bearer invalidtoken123');
    expect(res.statusCode).toBe(401); // Unauthorized
    expect(res.body).toHaveProperty('message', 'Invalid token');
  });

  it('should access a protected route with a valid token', async () => {
    const res = await request(app)
      .get('/api/protected')
      .set('Authorization', `Bearer ${authToken}`);
    expect(res.statusCode).toBe(200);
    expect(res.body).toHaveProperty('message', 'Access granted to protected resource');
  });

  it('should allow user to logout', async () => {
    const res = await request(app)
      .post('/auth/logout')
      .set('Authorization', `Bearer ${authToken}`);
    expect(res.statusCode).toBe(200);
    expect(res.body).toHaveProperty('message', 'Logged out successfully');

    // Verify token is invalidated (optional, depends on implementation)
    const protectedRes = await request(app)
      .get('/api/protected')
      .set('Authorization', `Bearer ${authToken}`);
    expect(protectedRes.statusCode).toBe(401);
  });
});
