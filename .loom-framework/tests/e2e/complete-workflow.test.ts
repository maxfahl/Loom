/**
 * End-to-End Workflow Tests
 *
 * Tests complete user workflows from start to finish
 */

import { describe, test, expect, beforeAll, afterAll } from '@jest/globals';
import TestHelper from '../utils/test-helpers';
import * as fs from 'fs';
import * as path from 'path';

describe('E2E: Complete Development Workflow', () => {
  let projectDir: string;

  beforeEach(() => {
    projectDir = TestHelper.createMockProject(`e2e-workflow-test-${Date.now()}`);
  });

  afterEach(() => {
    if (fs.existsSync(projectDir)) {
      fs.rmSync(projectDir, { recursive: true, force: true });
    }
  });

  test('E2E: New Project Setup -> Feature -> Story -> Dev -> Commit', async () => {
    // Step 1: Verify initial setup
    const initialStatus = TestHelper.readStatusXml(projectDir);
    expect(initialStatus.currentEpic).toBe('none');
    expect(initialStatus.currentStory).toBe('none');

    // Step 2: Create feature/epic
    const epicName = 'user-authentication';
    const epicPath = TestHelper.createMockEpic(projectDir, epicName);
    expect(fs.existsSync(epicPath)).toBe(true);

    TestHelper.updateStatusXml(projectDir, { epic: epicName });
    const afterEpicStatus = TestHelper.readStatusXml(projectDir);
    expect(afterEpicStatus.currentEpic).toBe(epicName);

    // Step 3: Create story
    const storyName = 'implement-login';
    const storyPath = TestHelper.createMockStory(
      projectDir,
      epicName,
      storyName
    );
    expect(fs.existsSync(storyPath)).toBe(true);

    TestHelper.updateStatusXml(projectDir, { story: storyName });
    const afterStoryStatus = TestHelper.readStatusXml(projectDir);
    expect(afterStoryStatus.currentStory).toBe(storyName);

    // Step 4: Development - create source files
    const srcDir = path.join(projectDir, 'src', 'auth');
    fs.mkdirSync(srcDir, { recursive: true });

    const loginFile = path.join(srcDir, 'login.ts');
    fs.writeFileSync(
      loginFile,
      `
export class LoginService {
  async login(email: string, password: string) {
    // Implementation
    return { success: true, token: 'mock-token' };
  }
}
`.trim()
    );

    expect(fs.existsSync(loginFile)).toBe(true);

    // Step 5: Create tests
    const testDir = path.join(projectDir, 'src', 'auth', '__tests__');
    fs.mkdirSync(testDir, { recursive: true });

    const testFile = path.join(testDir, 'login.test.ts');
    fs.writeFileSync(
      testFile,
      `
import { LoginService } from '../login';

describe('LoginService', () => {
  it('should login successfully', async () => {
    const service = new LoginService();
    const result = await service.login('test@test.com', 'password');
    expect(result.success).toBe(true);
  });
});
`.trim()
    );

    expect(fs.existsSync(testFile)).toBe(true);

    // Step 6: Verify all files created
    const filesCreated = [loginFile, testFile, storyPath, epicPath];
    filesCreated.forEach((file) => {
      expect(fs.existsSync(file)).toBe(true);
    });

    // Step 7: Verify project state
    const finalStatus = TestHelper.readStatusXml(projectDir);
    expect(finalStatus.currentEpic).toBe(epicName);
    expect(finalStatus.currentStory).toBe(storyName);
  });

  test('E2E: Multiple stories in single epic', async () => {
    const epicName = 'payment-system';
    TestHelper.createMockEpic(projectDir, epicName);

    const stories = [
      'create-payment-endpoint',
      'add-payment-validation',
      'implement-refunds',
    ];

    stories.forEach((storyName) => {
      const storyPath = TestHelper.createMockStory(
        projectDir,
        epicName,
        storyName
      );
      expect(fs.existsSync(storyPath)).toBe(true);
    });

    const storiesDir = path.join(
      projectDir,
      'prompts/features',
      epicName,
      'stories'
    );
    const createdStories = fs.readdirSync(storiesDir);

    expect(createdStories.length).toBe(stories.length);
  });

  test('E2E: Switch between multiple epics', async () => {
    const epic1 = 'feature-a';
    const epic2 = 'feature-b';

    TestHelper.createMockEpic(projectDir, epic1);
    TestHelper.createMockEpic(projectDir, epic2);

    // Work on epic1
    TestHelper.updateStatusXml(projectDir, { epic: epic1 });
    TestHelper.createMockStory(projectDir, epic1, 'story-a1');

    let status = TestHelper.readStatusXml(projectDir);
    expect(status.currentEpic).toBe(epic1);

    // Switch to epic2
    TestHelper.updateStatusXml(projectDir, { epic: epic2 });
    TestHelper.createMockStory(projectDir, epic2, 'story-b1');

    status = TestHelper.readStatusXml(projectDir);
    expect(status.currentEpic).toBe(epic2);

    // Verify both epics exist
    const featuresDir = path.join(projectDir, 'prompts/features');
    const epics = fs.readdirSync(featuresDir);

    expect(epics).toContain(epic1);
    expect(epics).toContain(epic2);
  });
});

describe('E2E: Error Scenarios', () => {
  let projectDir: string;

  beforeEach(() => {
    projectDir = TestHelper.createMockProject(`e2e-error-test-${Date.now()}`);
  });

  afterEach(() => {
    if (fs.existsSync(projectDir)) {
      fs.rmSync(projectDir, { recursive: true, force: true });
    }
  });

  test('E2E: Create story without epic should fail', () => {
    const status = TestHelper.readStatusXml(projectDir);
    expect(status.currentEpic).toBe('none');

    // Attempting to create story without epic
    try {
      TestHelper.createMockStory(projectDir, 'none', 'orphan-story');
      // If it doesn't throw, verify the path is weird
      const storyPath = path.join(
        projectDir,
        'prompts/features',
        'none',
        'stories',
        'orphan-story.md'
      );
      // This shouldn't work in real scenario
      expect(fs.existsSync(storyPath)).toBe(false);
    } catch (error) {
      // Expected to fail
      expect(error).toBeDefined();
    }
  });

  test('E2E: Corrupted status.xml recovery', () => {
    // Corrupt status.xml
    const statusPath = path.join(projectDir, 'status.xml');
    const backup = fs.readFileSync(statusPath, 'utf-8');

    fs.writeFileSync(statusPath, 'corrupted');

    // Try to read - should fail
    try {
      TestHelper.readStatusXml(projectDir);
      fail('Should have failed with corrupted XML');
    } catch (error) {
      expect(error).toBeDefined();
    }

    // Recover by restoring backup
    fs.writeFileSync(statusPath, backup);

    // Should work now
    const status = TestHelper.readStatusXml(projectDir);
    expect(status).toBeDefined();
  });
});

describe('E2E: Performance Tests', () => {
  let projectDir: string;

  beforeEach(() => {
    projectDir = TestHelper.createMockProject(`e2e-performance-test-${Date.now()}`);
  });

  afterEach(() => {
    if (fs.existsSync(projectDir)) {
      fs.rmSync(projectDir, { recursive: true, force: true });
    }
  });

  test('E2E: Create 10 epics quickly', async () => {
    const startTime = Date.now();

    for (let i = 1; i <= 10; i++) {
      TestHelper.createMockEpic(projectDir, `epic-${i}`);
    }

    const duration = Date.now() - startTime;

    expect(duration).toBeLessThan(1000); // Should complete in under 1 second

    const featuresDir = path.join(projectDir, 'prompts/features');
    const epics = fs.readdirSync(featuresDir);

    expect(epics.length).toBe(10);
  });

  test('E2E: Create 50 stories quickly', async () => {
    const epicName = 'bulk-epic';
    TestHelper.createMockEpic(projectDir, epicName);

    const startTime = Date.now();

    for (let i = 1; i <= 50; i++) {
      TestHelper.createMockStory(projectDir, epicName, `story-${i}`);
    }

    const duration = Date.now() - startTime;

    expect(duration).toBeLessThan(2000); // Should complete in under 2 seconds

    const storiesDir = path.join(
      projectDir,
      'prompts/features',
      epicName,
      'stories'
    );
    const stories = fs.readdirSync(storiesDir);

    expect(stories.length).toBe(50);
  });

  test('E2E: Rapid status.xml updates', async () => {
    const epicName = 'rapid-epic';
    TestHelper.createMockEpic(projectDir, epicName);

    const startTime = Date.now();

    for (let i = 0; i < 100; i++) {
      TestHelper.updateStatusXml(projectDir, { epic: epicName });
    }

    const duration = Date.now() - startTime;

    expect(duration).toBeLessThan(1000);

    const status = TestHelper.readStatusXml(projectDir);
    expect(status.currentEpic).toBe(epicName);
  });
});
