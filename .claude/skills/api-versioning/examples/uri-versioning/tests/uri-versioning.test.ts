// examples/uri-versioning/tests/uri-versioning.test.ts

import request from 'supertest';
import express from 'express';
import { getUsersV1, createUserV1 } from '../src/v1/users';
import { getUsersV2, createUserV2 } from '../src/v2/users';

// Mock Express app for testing
const app = express();
app.use(express.json());
app.get('/api/v1/users', getUsersV1);
app.post('/api/v1/users', createUserV1);
app.get('/api/v2/users', getUsersV2);
app.post('/api/v2/users', createUserV2);

describe('URI Versioning API', () => {
  describe('GET /api/v1/users', () => {
    it('should return v1 users with id and name', async () => {
      const res = await request(app).get('/api/v1/users');
      expect(res.statusCode).toEqual(200);
      expect(res.body).toEqual(expect.arrayContaining([
        expect.objectContaining({ id: '1', name: 'Alice' }),
        expect.objectContaining({ id: '2', name: 'Bob' }),
      ]));
      expect(res.body[0]).not.toHaveProperty('email');
    });
  });

  describe('POST /api/v1/users', () => {
    it('should create a new v1 user', async () => {
      const newUser = { id: '3', name: 'Charlie' };
      const res = await request(app).post('/api/v1/users').send(newUser);
      expect(res.statusCode).toEqual(201);
      expect(res.body).toEqual(newUser);
    });
  });

  describe('GET /api/v2/users', () => {
    it('should return v2 users with id, name, and email', async () => {
      const res = await request(app).get('/api/v2/users');
      expect(res.statusCode).toEqual(200);
      expect(res.body).toEqual(expect.arrayContaining([
        expect.objectContaining({ id: '1', name: 'Alice', email: 'alice@example.com' }),
        expect.objectContaining({ id: '2', name: 'Bob', email: 'bob@example.com' }),
      ]));
      expect(res.body[0]).toHaveProperty('email');
    });
  });

  describe('POST /api/v2/users', () => {
    it('should create a new v2 user', async () => {
      const newUser = { id: '3', name: 'Charlie', email: 'charlie@example.com' };
      const res = await request(app).post('/api/v2/users').send(newUser);
      expect(res.statusCode).toEqual(201);
      expect(res.body).toEqual(newUser);
    });
  });
});
