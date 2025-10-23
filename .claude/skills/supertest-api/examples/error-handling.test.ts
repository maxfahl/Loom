// examples/error-handling.test.ts

import request from 'supertest';
import app from '../../src/app'; // Adjust path to your Express app as needed

describe('Error Handling API Tests', () => {
  it('should return 400 Bad Request for invalid input', async () => {
    const res = await request(app)
      .post('/api/items')
      .send({ invalidField: 'value' }); // Assuming 'invalidField' is not expected

    expect(res.statusCode).toBe(400);
    expect(res.body).toHaveProperty('message');
    expect(res.body.message).toContain('Validation failed'); // Or similar error message
  });

  it('should return 404 Not Found for a non-existent route', async () => {
    const res = await request(app).get('/api/non-existent-route');
    expect(res.statusCode).toBe(404);
    expect(res.body).toHaveProperty('message', 'Not Found');
  });

  it('should return 405 Method Not Allowed for unsupported HTTP method', async () => {
    // Assuming /api/items only supports GET/POST, not PUT without an ID
    const res = await request(app).put('/api/items');
    expect(res.statusCode).toBe(405);
    expect(res.body).toHaveProperty('message', 'Method Not Allowed');
  });

  it('should return 500 Internal Server Error for an unhandled exception', async () => {
    // Assuming there's an endpoint that intentionally throws an error
    const res = await request(app).get('/api/trigger-error');
    expect(res.statusCode).toBe(500);
    expect(res.body).toHaveProperty('message', 'Internal Server Error');
  });

  it('should return 403 Forbidden for unauthorized access', async () => {
    // Assuming /api/admin requires an admin role, and we send a regular user token
    const regularUserToken = 'YOUR_REGULAR_USER_TOKEN'; // Obtain from login
    const res = await request(app)
      .get('/api/admin')
      .set('Authorization', `Bearer ${regularUserToken}`);
    expect(res.statusCode).toBe(403);
    expect(res.body).toHaveProperty('message', 'Forbidden');
  });
});
