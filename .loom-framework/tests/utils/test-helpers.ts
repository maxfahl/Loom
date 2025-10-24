/**
 * Test Helper Utilities
 */

import * as fs from 'fs';
import * as path from 'path';
import { execSync } from 'child_process';

export class TestHelper {
  /**
   * Create a temporary test directory
   */
  static createTempDir(name: string): string {
    const tempDir = path.join(process.cwd(), '.test-temp', name);
    if (fs.existsSync(tempDir)) {
      fs.rmSync(tempDir, { recursive: true, force: true });
    }
    fs.mkdirSync(tempDir, { recursive: true });
    return tempDir;
  }

  /**
   * Create a mock Loom project structure
   */
  static createMockProject(name: string): string {
    const projectDir = TestHelper.createTempDir(name);

    // Create directories
    const dirs = [
      '.claude',
      '.claude/agents',
      '.claude/commands',
      '.claude/skills',
      'prompts',
      'prompts/features',
      'prompts/stories',
    ];

    dirs.forEach((dir) => {
      fs.mkdirSync(path.join(projectDir, dir), { recursive: true });
    });

    // Create status.xml
    const statusXml = `<?xml version="1.0" encoding="UTF-8"?>
<project name="${name}">
  <feature-flags>
    <agent-memory enabled="false"/>
  </feature-flags>
  <current-epic>none</current-epic>
  <current-story>none</current-story>
  <yolo-mode>false</yolo-mode>
</project>`;

    fs.writeFileSync(path.join(projectDir, 'status.xml'), statusXml);

    // Create CLAUDE.md
    const claudeMd = `# Project Instructions

<!-- LOOM_FRAMEWORK_START -->
Loom framework instructions
<!-- LOOM_FRAMEWORK_END -->`;

    fs.writeFileSync(path.join(projectDir, 'CLAUDE.md'), claudeMd);

    // Create package.json
    const packageJson = {
      name,
      version: '1.0.0',
      description: 'Test project',
    };

    fs.writeFileSync(
      path.join(projectDir, 'package.json'),
      JSON.stringify(packageJson, null, 2)
    );

    // Initialize git
    try {
      execSync('git init', { cwd: projectDir, stdio: 'pipe' });
      execSync('git config user.name "Test User"', {
        cwd: projectDir,
        stdio: 'pipe',
      });
      execSync('git config user.email "test@test.com"', {
        cwd: projectDir,
        stdio: 'pipe',
      });
    } catch (error) {
      // Git init may fail, that's okay for tests
    }

    return projectDir;
  }

  /**
   * Read and parse status.xml
   */
  static readStatusXml(projectDir: string): any {
    const statusPath = path.join(projectDir, 'status.xml');
    if (!fs.existsSync(statusPath)) {
      throw new Error('status.xml not found');
    }

    const content = fs.readFileSync(statusPath, 'utf-8');

    // Simple XML parsing for tests
    const epicMatch = content.match(/<current-epic>(.*?)<\/current-epic>/);
    const storyMatch = content.match(/<current-story>(.*?)<\/current-story>/);
    const yoloMatch = content.match(/<yolo-mode>(.*?)<\/yolo-mode>/);

    return {
      currentEpic: epicMatch ? epicMatch[1] : 'none',
      currentStory: storyMatch ? storyMatch[1] : 'none',
      yoloMode: yoloMatch ? yoloMatch[1] === 'true' : false,
    };
  }

  /**
   * Update status.xml
   */
  static updateStatusXml(
    projectDir: string,
    updates: { epic?: string; story?: string; yolo?: boolean }
  ): void {
    const statusPath = path.join(projectDir, 'status.xml');
    let content = fs.readFileSync(statusPath, 'utf-8');

    if (updates.epic) {
      content = content.replace(
        /<current-epic>.*?<\/current-epic>/,
        `<current-epic>${updates.epic}</current-epic>`
      );
    }

    if (updates.story) {
      content = content.replace(
        /<current-story>.*?<\/current-story>/,
        `<current-story>${updates.story}</current-story>`
      );
    }

    if (updates.yolo !== undefined) {
      content = content.replace(
        /<yolo-mode>.*?<\/yolo-mode>/,
        `<yolo-mode>${updates.yolo}</yolo-mode>`
      );
    }

    fs.writeFileSync(statusPath, content);
  }

  /**
   * Create a mock epic
   */
  static createMockEpic(projectDir: string, epicName: string): string {
    const epicDir = path.join(projectDir, 'prompts/features', epicName);
    fs.mkdirSync(epicDir, { recursive: true });

    const epicContent = `# Epic: ${epicName}

## Overview
Test epic for ${epicName}

## Goals
- [ ] Goal 1
- [ ] Goal 2

## Stories
(To be created)
`;

    const epicPath = path.join(epicDir, 'EPIC.md');
    fs.writeFileSync(epicPath, epicContent);

    return epicPath;
  }

  /**
   * Create a mock story
   */
  static createMockStory(
    projectDir: string,
    epicName: string,
    storyName: string
  ): string {
    const storiesDir = path.join(
      projectDir,
      'prompts/features',
      epicName,
      'stories'
    );
    fs.mkdirSync(storiesDir, { recursive: true });

    const storyContent = `# Story: ${storyName}

## Description
Test story for ${storyName}

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2

## Technical Notes
Implementation notes here
`;

    const storyPath = path.join(storiesDir, `${storyName}.md`);
    fs.writeFileSync(storyPath, storyContent);

    return storyPath;
  }

  /**
   * Count files in directory recursively
   */
  static countFiles(dir: string): number {
    let count = 0;

    const walk = (directory: string) => {
      const files = fs.readdirSync(directory);
      for (const file of files) {
        const filePath = path.join(directory, file);
        const stats = fs.statSync(filePath);

        if (stats.isDirectory()) {
          walk(filePath);
        } else {
          count++;
        }
      }
    };

    walk(dir);
    return count;
  }

  /**
   * Simulate file change
   */
  static touchFile(filePath: string): void {
    const now = new Date();
    fs.utimesSync(filePath, now, now);
  }

  /**
   * Wait for specified milliseconds
   */
  static async wait(ms: number): Promise<void> {
    return new Promise((resolve) => setTimeout(resolve, ms));
  }

  /**
   * Generate random test ID
   */
  static generateTestId(): string {
    return `test-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
  }
}

export default TestHelper;
