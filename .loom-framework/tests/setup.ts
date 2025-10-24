/**
 * Test Setup and Global Configuration
 */

import { beforeAll, afterAll, beforeEach, afterEach } from '@jest/globals';
import * as fs from 'fs';
import * as path from 'path';

// Global test timeout
jest.setTimeout(30000);

// Test directories
export const TEST_DIRS = {
  root: path.join(process.cwd(), 'tests'),
  fixtures: path.join(process.cwd(), 'fixtures'),
  mocks: path.join(process.cwd(), 'mocks'),
  reports: path.join(process.cwd(), 'reports'),
  temp: path.join(process.cwd(), '.test-temp'),
};

// Ensure directories exist
beforeAll(() => {
  Object.values(TEST_DIRS).forEach((dir) => {
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }
  });
});

// Set up test fixtures before each test
beforeEach(async () => {
  // Ensure temp directory exists
  if (!fs.existsSync(TEST_DIRS.temp)) {
    fs.mkdirSync(TEST_DIRS.temp, { recursive: true });
  }

  // Copy status.xml fixture if it exists
  const fixtureStatusPath = path.join(TEST_DIRS.root, 'fixtures', 'status.xml');
  if (fs.existsSync(fixtureStatusPath)) {
    const targetStatusPath = path.join(TEST_DIRS.temp, 'status.xml');
    await fs.promises.copyFile(fixtureStatusPath, targetStatusPath);
  }
});

// Clean up temp directories after each test
afterEach(async () => {
  // Let any pending async operations complete
  await new Promise(resolve => setTimeout(resolve, 100));

  if (fs.existsSync(TEST_DIRS.temp)) {
    // Remove lock files first
    try {
      const files = fs.readdirSync(TEST_DIRS.temp, { recursive: true, withFileTypes: true });
      for (const file of files) {
        if (file.isFile() && file.name.endsWith('.lock')) {
          const lockPath = path.join(file.path || file.parentPath || '', file.name);
          await fs.promises.unlink(lockPath).catch(() => {});
        }
      }
    } catch (err) {
      // Ignore errors during lock file cleanup
    }

    // Then remove directory with async method
    await fs.promises.rm(TEST_DIRS.temp, { recursive: true, force: true });
  }
});

// Global cleanup
afterAll(async () => {
  // Let any pending async operations complete
  await new Promise(resolve => setTimeout(resolve, 100));

  if (fs.existsSync(TEST_DIRS.temp)) {
    // Remove lock files first
    try {
      const files = fs.readdirSync(TEST_DIRS.temp, { recursive: true, withFileTypes: true });
      for (const file of files) {
        if (file.isFile() && file.name.endsWith('.lock')) {
          const lockPath = path.join(file.path || file.parentPath || '', file.name);
          await fs.promises.unlink(lockPath).catch(() => {});
        }
      }
    } catch (err) {
      // Ignore errors during lock file cleanup
    }

    // Then remove directory with async method
    await fs.promises.rm(TEST_DIRS.temp, { recursive: true, force: true });
  }
});

// Custom matchers
expect.extend({
  toBeValidXML(received: string) {
    const isValid = received.includes('<?xml') && received.includes('</');
    return {
      message: () => `expected ${received} to be valid XML`,
      pass: isValid,
    };
  },
  toHaveLoomStructure(received: string) {
    const required = ['.claude', 'status.xml', 'CLAUDE.md'];
    const hasStructure = required.every((item) =>
      fs.existsSync(path.join(received, item))
    );
    return {
      message: () => `expected ${received} to have Loom structure`,
      pass: hasStructure,
    };
  },
});

// Suppress console noise in tests unless DEBUG is set
if (!process.env.DEBUG) {
  global.console = {
    ...console,
    log: jest.fn(),
    debug: jest.fn(),
    info: jest.fn(),
    warn: jest.fn(),
    error: jest.fn(),
  };
}

export default {};
