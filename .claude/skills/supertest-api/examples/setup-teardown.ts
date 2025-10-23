// examples/setup-teardown.ts

// This file demonstrates common setup and teardown patterns for Supertest API tests.
// It's not a test file itself, but rather a collection of reusable functions or patterns.

import mongoose from 'mongoose';
import { MongoMemoryServer } from 'mongodb-memory-server';

let mongo: MongoMemoryServer;

/**
 * Connects to an in-memory MongoDB instance for testing.
 * Call this in `beforeAll` in your test suite.
 */
export const connectToTestDb = async () => {
  mongo = await MongoMemoryServer.create();
  const mongoUri = mongo.getUri();
  await mongoose.connect(mongoUri);
  console.log('Connected to in-memory MongoDB');
};

/**
 * Clears all collections in the connected MongoDB database.
 * Call this in `beforeEach` to ensure a clean state for each test.
 */
export const clearTestDb = async () => {
  if (mongoose.connection.readyState === 1) { // Check if connected
    const collections = mongoose.connection.collections;
    for (const key in collections) {
      const collection = collections[key];
      await collection.deleteMany({});
    }
    console.log('Cleared all collections in test database');
  }
};

/**
 * Disconnects from the in-memory MongoDB instance and stops the server.
 * Call this in `afterAll` in your test suite.
 */
export const disconnectFromTestDb = async () => {
  if (mongoose.connection.readyState === 1) { // Check if connected
    await mongoose.connection.dropDatabase();
    await mongoose.connection.close();
    console.log('Disconnected from in-memory MongoDB');
  }
  if (mongo) {
    await mongo.stop();
    console.log('Stopped MongoMemoryServer');
  }
};

// Example usage in a test file (e.g., users.test.ts):
/*
import { connectToTestDb, clearTestDb, disconnectFromTestDb } from './setup-teardown';

beforeAll(async () => {
  await connectToTestDb();
});

beforeEach(async () => {
  await clearTestDb();
});

afterAll(async () => {
  await disconnectFromTestDb();
});

describe('My API Tests', () => {
  // ... your tests here
});
*/
