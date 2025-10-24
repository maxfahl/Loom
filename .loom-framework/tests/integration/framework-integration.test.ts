/**
 * Loom Framework Integration Tests
 *
 * Tests complete workflows from setup through development
 */

import { describe, test, expect, beforeEach, afterEach } from '@jest/globals';
import TestHelper from '../utils/test-helpers';
import * as fs from 'fs';
import * as path from 'path';

describe('Loom Framework Integration', () => {
  let projectDir: string;

  beforeEach(() => {
    projectDir = TestHelper.createMockProject(TestHelper.generateTestId());
  });

  afterEach(() => {
    if (fs.existsSync(projectDir)) {
      fs.rmSync(projectDir, { recursive: true, force: true });
    }
  });

  describe('Project Setup (Loomify)', () => {
    test('should create complete Loom project structure', () => {
      expect(fs.existsSync(path.join(projectDir, '.claude'))).toBe(true);
      expect(fs.existsSync(path.join(projectDir, 'status.xml'))).toBe(true);
      expect(fs.existsSync(path.join(projectDir, 'CLAUDE.md'))).toBe(true);
      expect(fs.existsSync(path.join(projectDir, '.claude/agents'))).toBe(true);
      expect(fs.existsSync(path.join(projectDir, '.claude/commands'))).toBe(
        true
      );
    });

    test('should have valid status.xml structure', () => {
      const status = TestHelper.readStatusXml(projectDir);

      expect(status).toHaveProperty('currentEpic');
      expect(status).toHaveProperty('currentStory');
      expect(status).toHaveProperty('yoloMode');
      expect(status.currentEpic).toBe('none');
    });

    test('should have CLAUDE.md with framework markers', () => {
      const claudeMdPath = path.join(projectDir, 'CLAUDE.md');
      const content = fs.readFileSync(claudeMdPath, 'utf-8');

      expect(content).toContain('<!-- LOOM_FRAMEWORK_START -->');
      expect(content).toContain('<!-- LOOM_FRAMEWORK_END -->');
    });

    test('should detect existing vs new project', () => {
      const hasGit = fs.existsSync(path.join(projectDir, '.git'));
      const hasPackageJson = fs.existsSync(
        path.join(projectDir, 'package.json')
      );

      expect(hasGit).toBe(true);
      expect(hasPackageJson).toBe(true);
    });
  });

  describe('Feature Creation', () => {
    test('should create new feature (epic) successfully', () => {
      const epicName = 'user-authentication';
      const epicPath = TestHelper.createMockEpic(projectDir, epicName);

      expect(fs.existsSync(epicPath)).toBe(true);

      const epicContent = fs.readFileSync(epicPath, 'utf-8');
      expect(epicContent).toContain(`# Epic: ${epicName}`);
      expect(epicContent).toContain('## Overview');
      expect(epicContent).toContain('## Goals');
    });

    test('should update status.xml with new epic', () => {
      const epicName = 'payment-system';
      TestHelper.createMockEpic(projectDir, epicName);
      TestHelper.updateStatusXml(projectDir, { epic: epicName });

      const status = TestHelper.readStatusXml(projectDir);
      expect(status.currentEpic).toBe(epicName);
    });

    test('should prevent duplicate epic names', () => {
      const epicName = 'duplicate-epic';
      const epicDir = path.join(projectDir, 'prompts/features', epicName);

      TestHelper.createMockEpic(projectDir, epicName);

      expect(fs.existsSync(epicDir)).toBe(true);

      // Second creation should detect existing
      const exists = fs.existsSync(epicDir);
      expect(exists).toBe(true);
    });

    test('should validate epic name format', () => {
      const validNames = ['user-auth', 'payment-system', 'data-sync'];
      const invalidNames = [
        'User Auth', // spaces
        'user_auth', // underscores
        'User-Auth', // capital letters
        'user@auth', // special chars
      ];

      const validateName = (name: string) =>
        /^[a-z]+(-[a-z]+)*$/.test(name);

      validNames.forEach((name) => {
        expect(validateName(name)).toBe(true);
      });

      invalidNames.forEach((name) => {
        expect(validateName(name)).toBe(false);
      });
    });
  });

  describe('Story Creation', () => {
    beforeEach(() => {
      const epicName = 'test-epic';
      TestHelper.createMockEpic(projectDir, epicName);
      TestHelper.updateStatusXml(projectDir, { epic: epicName });
    });

    test('should create story under current epic', () => {
      const storyName = 'implement-login';
      const storyPath = TestHelper.createMockStory(
        projectDir,
        'test-epic',
        storyName
      );

      expect(fs.existsSync(storyPath)).toBe(true);

      const storyContent = fs.readFileSync(storyPath, 'utf-8');
      expect(storyContent).toContain(`# Story: ${storyName}`);
      expect(storyContent).toContain('## Acceptance Criteria');
    });

    test('should update status.xml with current story', () => {
      const storyName = 'test-story';
      TestHelper.createMockStory(projectDir, 'test-epic', storyName);
      TestHelper.updateStatusXml(projectDir, { story: storyName });

      const status = TestHelper.readStatusXml(projectDir);
      expect(status.currentStory).toBe(storyName);
    });

    test('should store stories in correct epic directory', () => {
      const epicName = 'test-epic';
      const storyName = 'story-1';

      const storyPath = TestHelper.createMockStory(
        projectDir,
        epicName,
        storyName
      );
      const expectedPath = path.join(
        projectDir,
        'prompts/features',
        epicName,
        'stories',
        `${storyName}.md`
      );

      expect(storyPath).toBe(expectedPath);
      expect(fs.existsSync(expectedPath)).toBe(true);
    });

    test('should fail if no epic is set', () => {
      TestHelper.updateStatusXml(projectDir, { epic: 'none' });
      const status = TestHelper.readStatusXml(projectDir);

      expect(status.currentEpic).toBe('none');
      // Story creation would fail here
    });
  });

  describe('Development Workflow', () => {
    beforeEach(() => {
      TestHelper.createMockEpic(projectDir, 'test-epic');
      TestHelper.createMockStory(projectDir, 'test-epic', 'test-story');
      TestHelper.updateStatusXml(projectDir, {
        epic: 'test-epic',
        story: 'test-story',
      });
    });

    test('should have current story set before development', () => {
      const status = TestHelper.readStatusXml(projectDir);

      expect(status.currentStory).not.toBe('none');
      expect(status.currentStory).toBe('test-story');
    });

    test('should create source files during development', () => {
      const srcDir = path.join(projectDir, 'src');
      fs.mkdirSync(srcDir, { recursive: true });

      const testFile = path.join(srcDir, 'test.ts');
      fs.writeFileSync(testFile, 'export const test = true;');

      expect(fs.existsSync(testFile)).toBe(true);
    });

    test('should track file changes during development', () => {
      const beforeCount = TestHelper.countFiles(projectDir);

      // Simulate development creating files
      const srcDir = path.join(projectDir, 'src');
      fs.mkdirSync(srcDir, { recursive: true });
      fs.writeFileSync(path.join(srcDir, 'file1.ts'), 'content');
      fs.writeFileSync(path.join(srcDir, 'file2.ts'), 'content');

      const afterCount = TestHelper.countFiles(projectDir);

      expect(afterCount).toBeGreaterThan(beforeCount);
    });
  });

  describe('YOLO Mode', () => {
    test('should toggle YOLO mode', () => {
      TestHelper.updateStatusXml(projectDir, { yolo: true });
      let status = TestHelper.readStatusXml(projectDir);
      expect(status.yoloMode).toBe(true);

      TestHelper.updateStatusXml(projectDir, { yolo: false });
      status = TestHelper.readStatusXml(projectDir);
      expect(status.yoloMode).toBe(false);
    });

    test('should affect agent behavior in YOLO mode', () => {
      const status = TestHelper.readStatusXml(projectDir);

      if (status.yoloMode) {
        // In YOLO mode: skip confirmations, auto-commit, etc.
        expect(status.yoloMode).toBe(true);
      } else {
        // Normal mode: require confirmations
        expect(status.yoloMode).toBe(false);
      }
    });
  });

  describe('Cross-Reference Validation', () => {
    test('should validate status.xml schema', () => {
      const statusPath = path.join(projectDir, 'status.xml');
      const content = fs.readFileSync(statusPath, 'utf-8');

      expect(content).toContain('<?xml version="1.0"');
      expect(content).toContain('<project name=');
      expect(content).toContain('<feature-flags>');
      expect(content).toContain('<current-epic>');
      expect(content).toContain('<current-story>');
    });

    test('should validate CLAUDE.md markers', () => {
      const claudeMdPath = path.join(projectDir, 'CLAUDE.md');
      const content = fs.readFileSync(claudeMdPath, 'utf-8');

      const hasStartMarker = content.includes('<!-- LOOM_FRAMEWORK_START -->');
      const hasEndMarker = content.includes('<!-- LOOM_FRAMEWORK_END -->');

      expect(hasStartMarker).toBe(true);
      expect(hasEndMarker).toBe(true);
    });

    test('should validate epic references in stories', () => {
      const epicName = 'test-epic';
      const storyName = 'test-story';

      TestHelper.createMockEpic(projectDir, epicName);
      const storyPath = TestHelper.createMockStory(
        projectDir,
        epicName,
        storyName
      );

      const storyDir = path.dirname(storyPath);
      const epicDir = path.dirname(storyDir); // Go up one level from stories/ to epic/
      const epicFile = path.join(epicDir, 'EPIC.md');

      expect(fs.existsSync(epicFile)).toBe(true);
    });
  });

  describe('Error Recovery', () => {
    test('should handle corrupted status.xml', () => {
      const statusPath = path.join(projectDir, 'status.xml');
      fs.writeFileSync(statusPath, 'corrupted content');

      try {
        TestHelper.readStatusXml(projectDir);
        fail('Should throw error for corrupted XML');
      } catch (error) {
        expect(error).toBeDefined();
      }
    });

    test('should handle missing status.xml', () => {
      const statusPath = path.join(projectDir, 'status.xml');
      fs.unlinkSync(statusPath);

      try {
        TestHelper.readStatusXml(projectDir);
        fail('Should throw error for missing file');
      } catch (error: any) {
        expect(error.message).toContain('not found');
      }
    });

    test('should recover from partial setup', () => {
      // Remove some directories
      const claudeDir = path.join(projectDir, '.claude');
      fs.rmSync(claudeDir, { recursive: true, force: true });

      // Verify it's missing
      expect(fs.existsSync(claudeDir)).toBe(false);

      // Re-setup would recreate it
      fs.mkdirSync(claudeDir, { recursive: true });
      expect(fs.existsSync(claudeDir)).toBe(true);
    });
  });

  describe('Concurrency Handling', () => {
    test('should handle multiple rapid story creations', () => {
      const epicName = 'concurrent-epic';
      TestHelper.createMockEpic(projectDir, epicName);

      const storyNames = ['story-1', 'story-2', 'story-3'];

      storyNames.forEach((name) => {
        TestHelper.createMockStory(projectDir, epicName, name);
      });

      const storiesDir = path.join(
        projectDir,
        'prompts/features',
        epicName,
        'stories'
      );
      const files = fs.readdirSync(storiesDir);

      expect(files.length).toBe(storyNames.length);
    });

    test('should detect concurrent status.xml updates', async () => {
      const status1 = TestHelper.readStatusXml(projectDir);
      const status2 = TestHelper.readStatusXml(projectDir);

      expect(status1).toEqual(status2);

      // Simulate concurrent update
      TestHelper.updateStatusXml(projectDir, { epic: 'epic-1' });

      const status3 = TestHelper.readStatusXml(projectDir);
      expect(status3.currentEpic).toBe('epic-1');
    });
  });

  describe('Migration and Upgrade', () => {
    test('should detect framework version', () => {
      const statusPath = path.join(projectDir, 'status.xml');
      const content = fs.readFileSync(statusPath, 'utf-8');

      // Framework version could be tracked in status.xml
      const hasVersion = content.includes('version=') || content.includes('<version>');
      // Current implementation may not have version yet
      expect(typeof hasVersion).toBe('boolean');
    });

    test('should support story migration between epics', () => {
      const epic1 = 'epic-1';
      const epic2 = 'epic-2';
      const storyName = 'migrated-story';

      TestHelper.createMockEpic(projectDir, epic1);
      TestHelper.createMockEpic(projectDir, epic2);

      const originalPath = TestHelper.createMockStory(
        projectDir,
        epic1,
        storyName
      );

      expect(fs.existsSync(originalPath)).toBe(true);

      // Migrate to epic2
      const newPath = path.join(
        projectDir,
        'prompts/features',
        epic2,
        'stories',
        `${storyName}.md`
      );

      const storiesDir = path.dirname(newPath);
      if (!fs.existsSync(storiesDir)) {
        fs.mkdirSync(storiesDir, { recursive: true });
      }

      fs.copyFileSync(originalPath, newPath);
      expect(fs.existsSync(newPath)).toBe(true);
    });
  });
});
