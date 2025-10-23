// examples/mocking-external.test.ts

import request from 'supertest';
import app from '../../src/app'; // Adjust path to your Express app as needed
import nock from 'nock';

describe('External Service Mocking Tests', () => {
  beforeEach(() => {
    // Clear all active nock mocks before each test to ensure isolation
    nock.cleanAll();
  });

  afterAll(() => {
    // Ensure no pending nock mocks are left after all tests
    nock.restore();
  });

  it('should return mocked data from an external API call', async () => {
    const externalApiBase = 'http://external-service.com';
    const externalApiPath = '/data';
    const mockedResponse = { externalData: 'mocked value', source: 'nock' };

    // Set up nock to intercept the request to the external service
    nock(externalApiBase)
      .get(externalApiPath)
      .reply(200, mockedResponse);

    // Make a request to your API endpoint that calls the external service
    const res = await request(app).get('/api/data-from-external');

    expect(res.statusCode).toBe(200);
    expect(res.body).toEqual(mockedResponse);
    expect(nock.isDone()).toBe(true); // Verify that the nock interceptor was used
  });

  it('should handle external API errors gracefully', async () => {
    const externalApiBase = 'http://external-service.com';
    const externalApiPath = '/data';

    // Set up nock to simulate an error from the external service
    nock(externalApiBase)
      .get(externalApiPath)
      .reply(500, { error: 'External service unavailable' });

    // Make a request to your API endpoint that calls the external service
    const res = await request(app).get('/api/data-from-external');

    expect(res.statusCode).toBe(500); // Or whatever status your API returns for external errors
    expect(res.body).toHaveProperty('message', 'Failed to fetch external data');
    expect(nock.isDone()).toBe(true);
  });

  it('should mock a POST request to an external service', async () => {
    const externalApiBase = 'http://external-service.com';
    const externalApiPath = '/submit';
    const requestPayload = { item: 'new item' };
    const mockedResponse = { status: 'success', received: requestPayload };

    nock(externalApiBase)
      .post(externalApiPath, requestPayload) // Match payload if needed
      .reply(201, mockedResponse);

    const res = await request(app)
      .post('/api/submit-to-external')
      .send(requestPayload);

    expect(res.statusCode).toBe(201);
    expect(res.body).toEqual(mockedResponse);
    expect(nock.isDone()).toBe(true);
  });
});
