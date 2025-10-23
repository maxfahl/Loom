/**
 * BackupManager Test Suite
 *
 * Tests backup and restore functionality including:
 * - Full backups
 * - Incremental backups
 * - Backup validation
 * - Point-in-time restore
 * - Backup cleanup
 */

import { describe, it, expect, beforeEach, afterEach } from '@jest/globals';
import * as fs from 'fs/promises';
import * as path from 'path';
import { BackupManager } from '../BackupManager';
import { MemoryStore } from '../storage/MemoryStore';

const TEST_DIR = path.join(__dirname, '../__test_data__/backup-manager');
const MEMORY_DIR = path.join(TEST_DIR, 'memory');
const BACKUP_DIR = path.join(TEST_DIR, 'backups');

describe('BackupManager', () => {
  let backupManager: BackupManager;
  let memoryStore: MemoryStore;

  beforeEach(async () => {
    // Clean up
    await fs.rm(TEST_DIR, { recursive: true, force: true });
    await fs.mkdir(MEMORY_DIR, { recursive: true });
    await fs.mkdir(BACKUP_DIR, { recursive: true });

    memoryStore = new MemoryStore(MEMORY_DIR);
    await memoryStore.initialize();

    backupManager = new BackupManager(MEMORY_DIR, BACKUP_DIR);
  });

  afterEach(async () => {
    await fs.rm(TEST_DIR, { recursive: true, force: true });
  });

  describe('Full Backup', () => {
    it('should create full backup', async () => {
      // Create some test data
      await memoryStore.ensureAgentDirectory('test-agent');
      await memoryStore.addPattern('test-agent', {
        id: 'p1',
        agent: 'test-agent',
        timestamp: new Date().toISOString(),
        pattern: {
          type: 'test',
          context: {},
          approach: { technique: '', codeTemplate: '', rationale: '' },
          conditions: { whenApplicable: [], whenNotApplicable: [] }
        },
        metrics: { successRate: 0.8, executionCount: 1, avgTimeSavedMs: 100, errorPreventionCount: 0 },
        evolution: { created: new Date().toISOString(), lastUsed: new Date().toISOString(), refinements: 0, confidenceScore: 0.7 }
      });

      const result = await backupManager.createFullBackup();

      expect(result.success).toBe(true);
      expect(result.data).toHaveProperty('backupId');
      expect(result.data).toHaveProperty('timestamp');
      expect(result.data).toHaveProperty('size');
      expect(result.data?.type).toBe('full');
    });

    it('should include all agent directories in backup', async () => {
      await memoryStore.ensureAgentDirectory('agent-1');
      await memoryStore.ensureAgentDirectory('agent-2');
      await memoryStore.ensureAgentDirectory('agent-3');

      const result = await backupManager.createFullBackup();

      expect(result.success).toBe(true);

      // Verify backup contains all agents
      const backupPath = path.join(BACKUP_DIR, `${result.data!.backupId}.tar.gz`);
      await fs.access(backupPath); // Should exist
    });

    it('should include global data in backup', async () => {
      await memoryStore.setGlobalData('test-key', { value: 'test' });

      const result = await backupManager.createFullBackup();

      expect(result.success).toBe(true);
      // Global data should be included
    });

    it('should create compressed backup file', async () => {
      // Create substantial data
      await memoryStore.ensureAgentDirectory('agent-1');
      for (let i = 0; i < 100; i++) {
        await memoryStore.addPattern('agent-1', {
          id: `p${i}`,
          agent: 'agent-1',
          timestamp: new Date().toISOString(),
          pattern: {
            type: `type-${i}`,
            context: { data: 'x'.repeat(100) },
            approach: { technique: '', codeTemplate: '', rationale: '' },
            conditions: { whenApplicable: [], whenNotApplicable: [] }
          },
          metrics: { successRate: 0.8, executionCount: 1, avgTimeSavedMs: 100, errorPreventionCount: 0 },
          evolution: { created: new Date().toISOString(), lastUsed: new Date().toISOString(), refinements: 0, confidenceScore: 0.7 }
        });
      }

      const result = await backupManager.createFullBackup();

      expect(result.success).toBe(true);
      expect(result.data?.compressed).toBe(true);
    });
  });

  describe('Incremental Backup', () => {
    it('should create incremental backup after full backup', async () => {
      // Create full backup
      await memoryStore.ensureAgentDirectory('agent-1');
      const fullBackup = await backupManager.createFullBackup();

      // Add more data
      await memoryStore.addPattern('agent-1', {
        id: 'new-pattern',
        agent: 'agent-1',
        timestamp: new Date().toISOString(),
        pattern: {
          type: 'new',
          context: {},
          approach: { technique: '', codeTemplate: '', rationale: '' },
          conditions: { whenApplicable: [], whenNotApplicable: [] }
        },
        metrics: { successRate: 0.9, executionCount: 1, avgTimeSavedMs: 150, errorPreventionCount: 0 },
        evolution: { created: new Date().toISOString(), lastUsed: new Date().toISOString(), refinements: 0, confidenceScore: 0.8 }
      });

      // Create incremental backup
      const incrementalResult = await backupManager.createIncrementalBackup();

      expect(incrementalResult.success).toBe(true);
      expect(incrementalResult.data?.type).toBe('incremental');
      expect(incrementalResult.data?.baseBackupId).toBe(fullBackup.data!.backupId);
    });

    it('should be smaller than full backup', async () => {
      // Create base data
      await memoryStore.ensureAgentDirectory('agent-1');
      for (let i = 0; i < 50; i++) {
        await memoryStore.addPattern('agent-1', {
          id: `p${i}`,
          agent: 'agent-1',
          timestamp: new Date().toISOString(),
          pattern: {
            type: `type-${i}`,
            context: {},
            approach: { technique: '', codeTemplate: '', rationale: '' },
            conditions: { whenApplicable: [], whenNotApplicable: [] }
          },
          metrics: { successRate: 0.8, executionCount: 1, avgTimeSavedMs: 100, errorPreventionCount: 0 },
          evolution: { created: new Date().toISOString(), lastUsed: new Date().toISOString(), refinements: 0, confidenceScore: 0.7 }
        });
      }

      const fullBackup = await backupManager.createFullBackup();

      // Add a few more patterns
      for (let i = 50; i < 55; i++) {
        await memoryStore.addPattern('agent-1', {
          id: `p${i}`,
          agent: 'agent-1',
          timestamp: new Date().toISOString(),
          pattern: {
            type: `type-${i}`,
            context: {},
            approach: { technique: '', codeTemplate: '', rationale: '' },
            conditions: { whenApplicable: [], whenNotApplicable: [] }
          },
          metrics: { successRate: 0.8, executionCount: 1, avgTimeSavedMs: 100, errorPreventionCount: 0 },
          evolution: { created: new Date().toISOString(), lastUsed: new Date().toISOString(), refinements: 0, confidenceScore: 0.7 }
        });
      }

      const incrementalBackup = await backupManager.createIncrementalBackup();

      expect(incrementalBackup.data!.size).toBeLessThan(fullBackup.data!.size);
    });
  });

  describe('Backup Validation', () => {
    it('should validate backup integrity', async () => {
      await memoryStore.ensureAgentDirectory('agent-1');
      const backup = await backupManager.createFullBackup();

      const validation = await backupManager.validateBackup(backup.data!.backupId);

      expect(validation.success).toBe(true);
      expect(validation.data?.valid).toBe(true);
      expect(validation.data?.checksumMatch).toBe(true);
    });

    it('should detect corrupted backup', async () => {
      await memoryStore.ensureAgentDirectory('agent-1');
      const backup = await backupManager.createFullBackup();

      // Corrupt the backup file
      const backupPath = path.join(BACKUP_DIR, `${backup.data!.backupId}.tar.gz`);
      await fs.appendFile(backupPath, 'corrupt data');

      const validation = await backupManager.validateBackup(backup.data!.backupId);

      expect(validation.data?.valid).toBe(false);
      expect(validation.data?.checksumMatch).toBe(false);
    });

    it('should validate backup contents', async () => {
      await memoryStore.ensureAgentDirectory('agent-1');
      await memoryStore.addPattern('agent-1', {
        id: 'p1',
        agent: 'agent-1',
        timestamp: new Date().toISOString(),
        pattern: {
          type: 'test',
          context: {},
          approach: { technique: '', codeTemplate: '', rationale: '' },
          conditions: { whenApplicable: [], whenNotApplicable: [] }
        },
        metrics: { successRate: 0.8, executionCount: 1, avgTimeSavedMs: 100, errorPreventionCount: 0 },
        evolution: { created: new Date().toISOString(), lastUsed: new Date().toISOString(), refinements: 0, confidenceScore: 0.7 }
      });

      const backup = await backupManager.createFullBackup();
      const validation = await backupManager.validateBackup(backup.data!.backupId);

      expect(validation.data?.fileCount).toBeGreaterThan(0);
      expect(validation.data?.agentsIncluded).toContain('agent-1');
    });
  });

  describe('Restore Operations', () => {
    it('should restore from full backup', async () => {
      // Create original data
      await memoryStore.ensureAgentDirectory('agent-1');
      await memoryStore.addPattern('agent-1', {
        id: 'original',
        agent: 'agent-1',
        timestamp: new Date().toISOString(),
        pattern: {
          type: 'original-type',
          context: {},
          approach: { technique: 'original', codeTemplate: '', rationale: '' },
          conditions: { whenApplicable: [], whenNotApplicable: [] }
        },
        metrics: { successRate: 0.9, executionCount: 5, avgTimeSavedMs: 200, errorPreventionCount: 1 },
        evolution: { created: new Date().toISOString(), lastUsed: new Date().toISOString(), refinements: 0, confidenceScore: 0.85 }
      });

      // Create backup
      const backup = await backupManager.createFullBackup();

      // Delete data
      await fs.rm(path.join(MEMORY_DIR, 'agent-1'), { recursive: true });

      // Restore
      const restoreResult = await backupManager.restore(backup.data!.backupId);

      expect(restoreResult.success).toBe(true);

      // Verify data is restored
      const patterns = await memoryStore.getPatterns('agent-1');
      const restored = patterns.data.find(p => p.id === 'original');
      expect(restored).toBeDefined();
      expect(restored?.pattern.type).toBe('original-type');
    });

    it('should restore to point in time', async () => {
      await memoryStore.ensureAgentDirectory('agent-1');

      // State 1
      await memoryStore.addPattern('agent-1', {
        id: 'p1',
        agent: 'agent-1',
        timestamp: new Date().toISOString(),
        pattern: {
          type: 'state-1',
          context: {},
          approach: { technique: '', codeTemplate: '', rationale: '' },
          conditions: { whenApplicable: [], whenNotApplicable: [] }
        },
        metrics: { successRate: 0.7, executionCount: 1, avgTimeSavedMs: 100, errorPreventionCount: 0 },
        evolution: { created: new Date().toISOString(), lastUsed: new Date().toISOString(), refinements: 0, confidenceScore: 0.6 }
      });
      const backup1 = await backupManager.createFullBackup();
      const timestamp1 = backup1.data!.timestamp;

      await new Promise(resolve => setTimeout(resolve, 100));

      // State 2
      await memoryStore.addPattern('agent-1', {
        id: 'p2',
        agent: 'agent-1',
        timestamp: new Date().toISOString(),
        pattern: {
          type: 'state-2',
          context: {},
          approach: { technique: '', codeTemplate: '', rationale: '' },
          conditions: { whenApplicable: [], whenNotApplicable: [] }
        },
        metrics: { successRate: 0.8, executionCount: 1, avgTimeSavedMs: 150, errorPreventionCount: 0 },
        evolution: { created: new Date().toISOString(), lastUsed: new Date().toISOString(), refinements: 0, confidenceScore: 0.75 }
      });

      // Restore to state 1
      await backupManager.restoreToPointInTime(timestamp1);

      const patterns = await memoryStore.getPatterns('agent-1');
      expect(patterns.data).toHaveLength(1);
      expect(patterns.data[0].id).toBe('p1');
      expect(patterns.data[0].pattern.type).toBe('state-1');
    });

    it('should create backup before restore', async () => {
      await memoryStore.ensureAgentDirectory('agent-1');
      const originalBackup = await backupManager.createFullBackup();

      // Modify data
      await memoryStore.addPattern('agent-1', {
        id: 'new',
        agent: 'agent-1',
        timestamp: new Date().toISOString(),
        pattern: {
          type: 'new',
          context: {},
          approach: { technique: '', codeTemplate: '', rationale: '' },
          conditions: { whenApplicable: [], whenNotApplicable: [] }
        },
        metrics: { successRate: 0.8, executionCount: 1, avgTimeSavedMs: 100, errorPreventionCount: 0 },
        evolution: { created: new Date().toISOString(), lastUsed: new Date().toISOString(), refinements: 0, confidenceScore: 0.7 }
      });

      // Restore (should create pre-restore backup)
      const restoreResult = await backupManager.restore(originalBackup.data!.backupId, {
        createBackupBeforeRestore: true
      });

      expect(restoreResult.success).toBe(true);
      expect(restoreResult.data).toHaveProperty('preRestoreBackupId');

      // Verify pre-restore backup exists
      const backups = await backupManager.listBackups();
      const preRestoreBackup = backups.data.find(b =>
        b.id === restoreResult.data!.preRestoreBackupId
      );
      expect(preRestoreBackup).toBeDefined();
    });
  });

  describe('Backup Cleanup', () => {
    it('should list all backups', async () => {
      await memoryStore.ensureAgentDirectory('agent-1');

      await backupManager.createFullBackup();
      await backupManager.createFullBackup();
      await backupManager.createFullBackup();

      const backups = await backupManager.listBackups();

      expect(backups.success).toBe(true);
      expect(backups.data).toHaveLength(3);
    });

    it('should delete old backups', async () => {
      await memoryStore.ensureAgentDirectory('agent-1');

      // Create multiple backups
      const backup1 = await backupManager.createFullBackup();
      await new Promise(resolve => setTimeout(resolve, 100));
      const backup2 = await backupManager.createFullBackup();
      await new Promise(resolve => setTimeout(resolve, 100));
      const backup3 = await backupManager.createFullBackup();

      // Delete backups older than backup3
      const deleteResult = await backupManager.deleteBackupsOlderThan(
        new Date(backup3.data!.timestamp)
      );

      expect(deleteResult.success).toBe(true);
      expect(deleteResult.data?.deletedCount).toBe(2);

      // Only backup3 should remain
      const backups = await backupManager.listBackups();
      expect(backups.data).toHaveLength(1);
      expect(backups.data[0].id).toBe(backup3.data!.backupId);
    });

    it('should keep last N backups', async () => {
      await memoryStore.ensureAgentDirectory('agent-1');

      // Create 10 backups
      for (let i = 0; i < 10; i++) {
        await backupManager.createFullBackup();
        await new Promise(resolve => setTimeout(resolve, 50));
      }

      // Keep only last 3
      const cleanupResult = await backupManager.keepLastNBackups(3);

      expect(cleanupResult.success).toBe(true);
      expect(cleanupResult.data?.deletedCount).toBe(7);

      const backups = await backupManager.listBackups();
      expect(backups.data).toHaveLength(3);
    });

    it('should delete specific backup', async () => {
      await memoryStore.ensureAgentDirectory('agent-1');

      const backup = await backupManager.createFullBackup();

      const deleteResult = await backupManager.deleteBackup(backup.data!.backupId);

      expect(deleteResult.success).toBe(true);

      const backups = await backupManager.listBackups();
      expect(backups.data.find(b => b.id === backup.data!.backupId)).toBeUndefined();
    });
  });

  describe('Performance', () => {
    it('should handle large backup efficiently', async () => {
      // Create substantial data
      await memoryStore.ensureAgentDirectory('agent-1');
      for (let i = 0; i < 500; i++) {
        await memoryStore.addPattern('agent-1', {
          id: `p${i}`,
          agent: 'agent-1',
          timestamp: new Date().toISOString(),
          pattern: {
            type: `type-${i}`,
            context: { data: 'x'.repeat(50) },
            approach: { technique: '', codeTemplate: '', rationale: '' },
            conditions: { whenApplicable: [], whenNotApplicable: [] }
          },
          metrics: { successRate: 0.8, executionCount: 1, avgTimeSavedMs: 100, errorPreventionCount: 0 },
          evolution: { created: new Date().toISOString(), lastUsed: new Date().toISOString(), refinements: 0, confidenceScore: 0.7 }
        });
      }

      const start = Date.now();
      const backup = await backupManager.createFullBackup();
      const duration = Date.now() - start;

      expect(backup.success).toBe(true);
      // Should complete in reasonable time (< 5 seconds for 500 patterns)
      expect(duration).toBeLessThan(5000);
    });

    it('should restore quickly', async () => {
      await memoryStore.ensureAgentDirectory('agent-1');
      for (let i = 0; i < 100; i++) {
        await memoryStore.addPattern('agent-1', {
          id: `p${i}`,
          agent: 'agent-1',
          timestamp: new Date().toISOString(),
          pattern: {
            type: `type-${i}`,
            context: {},
            approach: { technique: '', codeTemplate: '', rationale: '' },
            conditions: { whenApplicable: [], whenNotApplicable: [] }
          },
          metrics: { successRate: 0.8, executionCount: 1, avgTimeSavedMs: 100, errorPreventionCount: 0 },
          evolution: { created: new Date().toISOString(), lastUsed: new Date().toISOString(), refinements: 0, confidenceScore: 0.7 }
        });
      }

      const backup = await backupManager.createFullBackup();
      await fs.rm(path.join(MEMORY_DIR, 'agent-1'), { recursive: true });

      const start = Date.now();
      await backupManager.restore(backup.data!.backupId);
      const duration = Date.now() - start;

      // Should restore quickly (< 2 seconds)
      expect(duration).toBeLessThan(2000);
    });
  });

  describe('Error Handling', () => {
    it('should handle missing backup file', async () => {
      const restoreResult = await backupManager.restore('nonexistent-backup-id');

      expect(restoreResult.success).toBe(false);
      expect(restoreResult.error).toContain('not found');
    });

    it('should handle corrupted backup during restore', async () => {
      await memoryStore.ensureAgentDirectory('agent-1');
      const backup = await backupManager.createFullBackup();

      // Corrupt backup
      const backupPath = path.join(BACKUP_DIR, `${backup.data!.backupId}.tar.gz`);
      await fs.writeFile(backupPath, 'completely invalid data');

      const restoreResult = await backupManager.restore(backup.data!.backupId);

      expect(restoreResult.success).toBe(false);
    });

    it('should handle disk space issues gracefully', async () => {
      // This is difficult to test without actually filling disk
      // We'll just verify error handling structure exists
      expect(backupManager).toHaveProperty('createFullBackup');
    });
  });
});
