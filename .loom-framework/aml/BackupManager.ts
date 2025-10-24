/**
 * Backup Manager - Automated backup and restore functionality
 *
 * Handles scheduled backups, incremental backups, and disaster recovery.
 * Ensures data integrity and provides rollback capabilities.
 */

import { MemoryStore } from './storage/MemoryStore';
import { AgentName, Timestamp, OperationResult } from './types/common';
import * as fs from 'fs/promises';
import * as path from 'path';
import * as crypto from 'crypto';
import * as tar from 'tar';

export interface BackupMetadata {
  id: string;
  timestamp: Timestamp;
  agents: AgentName[];
  totalSize: number;
  compressed: boolean;
  encrypted: boolean;
  type: 'full' | 'incremental';
  parentBackupId?: string;
  checksum?: string;
  fileCount?: number;
}

export interface BackupOptions {
  agents?: AgentName[]; // Specific agents or all
  includeGlobal?: boolean;
  compress?: boolean;
  encrypt?: boolean;
  type?: 'full' | 'incremental';
  destination?: string;
}

export interface RestoreOptions {
  backupId: string;
  agents?: AgentName[]; // Specific agents or all from backup
  overwrite?: boolean;
  validateIntegrity?: boolean;
}

/**
 * Backup Manager class
 */
export class BackupManager {
  private store: MemoryStore;
  private backupPath: string;
  private backups: Map<string, BackupMetadata>;
  private schedule: NodeJS.Timeout | null;

  constructor(storagePath: string, backupPath: string = '.loom/memory-backup') {
    this.store = new MemoryStore(storagePath);
    this.backupPath = backupPath;
    this.backups = new Map();
    this.schedule = null;
  }

  /**
   * Initialize backup system
   */
  async initialize(): Promise<void> {
    await fs.mkdir(this.backupPath, { recursive: true });
    await this.loadBackupMetadata();
  }

  /**
   * Create a backup
   */
  async createBackup(options: BackupOptions = {}): Promise<OperationResult<BackupMetadata>> {
    try {
      const backupId = `backup-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
      const timestamp = new Date().toISOString();

      // Determine which agents to backup
      let agents = options.agents || (await this.store.listAgents());

      // Create temporary staging directory
      const stagingDir = path.join(this.backupPath, `${backupId}-staging`);
      await fs.mkdir(stagingDir, { recursive: true });

      const backedUpAgents: AgentName[] = [];
      let fileCount = 0;

      // For incremental backups, find the base backup timestamp
      let baseTimestamp: number | null = null;
      if (options.type === 'incremental') {
        const backupsArray = Array.from(this.backups.values())
          .sort((a, b) => new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime());
        if (backupsArray.length > 0) {
          baseTimestamp = new Date(backupsArray[0].timestamp).getTime();
        }
      }

      // Backup each agent
      for (const agent of agents) {
        const agentSourcePath = path.join(this.store.getBasePath(), agent);
        const agentBackupPath = path.join(stagingDir, agent);

        try {
          await fs.access(agentSourcePath);
        } catch {
          continue; // Agent directory doesn't exist
        }

        await fs.mkdir(agentBackupPath, { recursive: true });

        const files = await fs.readdir(agentSourcePath);
        let agentHasFiles = false;

        for (const file of files) {
          const sourceFile = path.join(agentSourcePath, file);
          const stats = await fs.stat(sourceFile);

          // For incremental backups, only include files modified after base backup
          if (baseTimestamp && stats.mtimeMs < baseTimestamp) {
            continue;
          }

          const destFile = path.join(agentBackupPath, file);
          await fs.copyFile(sourceFile, destFile);
          fileCount++;
          agentHasFiles = true;
        }

        if (agentHasFiles) {
          backedUpAgents.push(agent);
        }
      }

      // Backup global data (always include in full backups, or if includeGlobal is set)
      if (options.type === 'full' || options.includeGlobal) {
        const globalSourcePath = path.join(this.store.getBasePath(), 'global');
        try {
          await fs.access(globalSourcePath);
          const globalBackupPath = path.join(stagingDir, 'global');
          await fs.mkdir(globalBackupPath, { recursive: true });

          const globalFiles = await fs.readdir(globalSourcePath);
          for (const file of globalFiles) {
            const sourceFile = path.join(globalSourcePath, file);
            const destFile = path.join(globalBackupPath, file);
            await fs.copyFile(sourceFile, destFile);
            fileCount++;
          }
        } catch {
          // Global directory doesn't exist, that's okay
        }
      }

      // Create tar.gz archive
      const tarPath = path.join(this.backupPath, `${backupId}.tar.gz`);
      await tar.create(
        {
          gzip: true,
          file: tarPath,
          cwd: stagingDir,
        },
        await fs.readdir(stagingDir)
      );

      // Calculate checksum
      const fileBuffer = await fs.readFile(tarPath);
      const hash = crypto.createHash('sha256');
      hash.update(fileBuffer);
      const checksum = hash.digest('hex');

      // Get final size
      const stats = await fs.stat(tarPath);
      const totalSize = stats.size;

      // Clean up staging directory
      await fs.rm(stagingDir, { recursive: true, force: true });

      // Create metadata
      const metadata: BackupMetadata = {
        id: backupId,
        timestamp,
        agents: backedUpAgents,
        totalSize,
        compressed: true,
        encrypted: options.encrypt || false,
        type: options.type || 'full',
        checksum,
        fileCount,
      };

      // Save metadata
      await this.saveBackupMetadata(metadata);
      this.backups.set(backupId, metadata);

      return { success: true, data: metadata };
    } catch (error) {
      return {
        success: false,
        error: `Failed to create backup: ${(error as Error).message}`,
      };
    }
  }

  /**
   * Restore from backup
   */
  async restoreBackup(options: RestoreOptions): Promise<OperationResult> {
    try {
      const metadata = this.backups.get(options.backupId);
      if (!metadata) {
        return { success: false, error: 'Backup not found' };
      }

      const tarPath = path.join(this.backupPath, `${options.backupId}.tar.gz`);

      // Check if backup file exists
      try {
        await fs.access(tarPath);
      } catch {
        return { success: false, error: 'Backup file not found' };
      }

      // Validate integrity if requested
      if (options.validateIntegrity) {
        const validation = await this.validateBackup(options.backupId);
        if (!validation.success || !validation.data?.valid) {
          return { success: false, error: 'Backup integrity check failed' };
        }
      }

      // Create temporary extraction directory
      const extractDir = path.join(this.backupPath, `${options.backupId}-restore`);
      await fs.mkdir(extractDir, { recursive: true });

      // Extract tar.gz
      await tar.extract({
        file: tarPath,
        cwd: extractDir,
      });

      // Determine which agents to restore
      const agentsToRestore = options.agents || metadata.agents;

      // Restore each agent
      for (const agent of agentsToRestore) {
        if (!metadata.agents.includes(agent)) {
          continue; // Skip agents not in backup
        }

        const agentBackupPath = path.join(extractDir, agent);
        const agentDestPath = path.join(this.store.getBasePath(), agent);

        // Check if agent backup exists
        try {
          await fs.access(agentBackupPath);
        } catch {
          continue; // Agent not in backup
        }

        // Check if agent memory exists
        const exists = await this.store.agentHasMemory(agent);

        if (exists && !options.overwrite) {
          // Skip if exists and overwrite not enabled
          continue;
        }

        // Remove existing agent data if overwriting
        if (exists) {
          await fs.rm(agentDestPath, { recursive: true, force: true });
        }

        // Create agent directory
        await fs.mkdir(agentDestPath, { recursive: true });

        // Copy files
        const files = await fs.readdir(agentBackupPath);
        for (const file of files) {
          const sourceFile = path.join(agentBackupPath, file);
          const destFile = path.join(agentDestPath, file);
          await fs.copyFile(sourceFile, destFile);
        }
      }

      // Restore global data if present
      const globalBackupPath = path.join(extractDir, 'global');
      try {
        await fs.access(globalBackupPath);
        const globalDestPath = path.join(this.store.getBasePath(), 'global');
        await fs.mkdir(globalDestPath, { recursive: true });

        const globalFiles = await fs.readdir(globalBackupPath);
        for (const file of globalFiles) {
          const sourceFile = path.join(globalBackupPath, file);
          const destFile = path.join(globalDestPath, file);
          await fs.copyFile(sourceFile, destFile);
        }
      } catch {
        // Global data not in backup, that's okay
      }

      // Clean up extraction directory
      await fs.rm(extractDir, { recursive: true, force: true });

      return { success: true };
    } catch (error) {
      return {
        success: false,
        error: `Failed to restore backup: ${(error as Error).message}`,
      };
    }
  }

  /**
   * List all backups
   */
  listBackups(): BackupMetadata[] {
    return Array.from(this.backups.values()).sort(
      (a, b) => new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime()
    );
  }

  /**
   * Get backup details
   */
  getBackup(backupId: string): BackupMetadata | null {
    return this.backups.get(backupId) || null;
  }

  /**
   * Delete a backup
   */
  async deleteBackup(backupId: string): Promise<OperationResult> {
    try {
      const metadata = this.backups.get(backupId);
      if (!metadata) {
        return { success: false, error: 'Backup not found' };
      }

      // Delete backup tar.gz file
      const tarPath = path.join(this.backupPath, `${backupId}.tar.gz`);
      await fs.unlink(tarPath).catch(() => {}); // Ignore if doesn't exist

      // Delete metadata
      const metadataPath = path.join(this.backupPath, `${backupId}.meta.json`);
      await fs.unlink(metadataPath).catch(() => {}); // Ignore if doesn't exist

      this.backups.delete(backupId);

      return { success: true };
    } catch (error) {
      return {
        success: false,
        error: `Failed to delete backup: ${(error as Error).message}`,
      };
    }
  }

  /**
   * Validate backup integrity (private version that returns boolean)
   */
  private async validateBackupIntegrity(backupId: string): Promise<boolean> {
    try {
      const metadata = this.backups.get(backupId);
      if (!metadata) return false;

      const tarPath = path.join(this.backupPath, `${backupId}.tar.gz`);

      // Check if backup file exists
      await fs.access(tarPath);

      // Verify checksum if available
      if (metadata.checksum) {
        const fileBuffer = await fs.readFile(tarPath);
        const hash = crypto.createHash('sha256');
        hash.update(fileBuffer);
        const checksum = hash.digest('hex');

        if (checksum !== metadata.checksum) {
          return false;
        }
      }

      return true;
    } catch {
      return false;
    }
  }

  /**
   * Schedule automatic backups
   */
  scheduleBackups(
    schedule: 'hourly' | 'daily' | 'weekly',
    options: BackupOptions = {}
  ): void {
    // Clear existing schedule
    if (this.schedule) {
      clearInterval(this.schedule);
    }

    // Calculate interval
    let intervalMs: number;
    switch (schedule) {
      case 'hourly':
        intervalMs = 60 * 60 * 1000;
        break;
      case 'daily':
        intervalMs = 24 * 60 * 60 * 1000;
        break;
      case 'weekly':
        intervalMs = 7 * 24 * 60 * 60 * 1000;
        break;
    }

    // Schedule backups
    this.schedule = setInterval(async () => {
      await this.createBackup(options);
      await this.cleanupOldBackups();
    }, intervalMs);
  }

  /**
   * Stop scheduled backups
   */
  stopScheduledBackups(): void {
    if (this.schedule) {
      clearInterval(this.schedule);
      this.schedule = null;
    }
  }

  /**
   * Clean up old backups (keep last 10)
   */
  async cleanupOldBackups(keepCount: number = 10): Promise<number> {
    const backups = this.listBackups();

    if (backups.length <= keepCount) {
      return 0;
    }

    const toDelete = backups.slice(keepCount);
    let deleted = 0;

    for (const backup of toDelete) {
      const result = await this.deleteBackup(backup.id);
      if (result.success) {
        deleted++;
      }
    }

    return deleted;
  }

  /**
   * Get total backup size
   */
  getTotalBackupSize(): number {
    return Array.from(this.backups.values()).reduce((sum, backup) => sum + backup.totalSize, 0);
  }

  // ============================================================================
  // NEW PUBLIC METHODS (for test compatibility)
  // ============================================================================

  /**
   * Create full backup (test-compatible signature)
   */
  async createFullBackup(): Promise<OperationResult<{ backupId: string; timestamp: string; sizeBytes: number; size: number; compressed: boolean; type: 'full' | 'incremental' }>> {
    const result = await this.createBackup({ type: 'full' });
    if (result.success && result.data) {
      return {
        success: true,
        data: {
          backupId: result.data.id,
          timestamp: result.data.timestamp,
          sizeBytes: result.data.totalSize,
          size: result.data.totalSize,
          compressed: result.data.compressed,
          type: result.data.type
        }
      };
    }
    return { success: false, error: result.error };
  }

  /**
   * Create incremental backup (test-compatible signature)
   */
  async createIncrementalBackup(baseBackupId?: string): Promise<OperationResult<{ backupId: string; timestamp: string; sizeBytes: number; size: number; type: 'full' | 'incremental'; baseBackupId?: string }>> {
    // Find base backup if not specified
    let actualBaseId = baseBackupId;
    if (!actualBaseId) {
      const backupsArray = Array.from(this.backups.values())
        .sort((a, b) => new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime());
      if (backupsArray.length > 0) {
        actualBaseId = backupsArray[0].id;
      }
    }

    const result = await this.createBackup({ type: 'incremental' });
    if (result.success && result.data) {
      return {
        success: true,
        data: {
          backupId: result.data.id,
          timestamp: result.data.timestamp,
          sizeBytes: result.data.totalSize,
          size: result.data.totalSize,
          type: result.data.type,
          baseBackupId: actualBaseId
        }
      };
    }
    return { success: false, error: result.error };
  }

  /**
   * Validate backup integrity (test-compatible signature)
   */
  async validateBackup(backupId: string): Promise<OperationResult<{ valid: boolean; checksum?: string; checksumMatch?: boolean; fileCount?: number; agentsIncluded?: string[] }>> {
    try {
      const metadata = this.backups.get(backupId);
      if (!metadata) {
        return { success: true, data: { valid: false } };
      }

      const tarPath = path.join(this.backupPath, `${backupId}.tar.gz`);

      // Check if backup file exists
      try {
        await fs.access(tarPath);
      } catch {
        return { success: true, data: { valid: false } };
      }

      // Calculate current checksum
      const fileBuffer = await fs.readFile(tarPath);
      const hash = crypto.createHash('sha256');
      hash.update(fileBuffer);
      const currentChecksum = hash.digest('hex');

      // Verify checksum matches
      const checksumMatch = metadata.checksum ? currentChecksum === metadata.checksum : true;

      // Extract to temporary directory to count files
      const tempDir = path.join(this.backupPath, `${backupId}-validate`);
      await fs.mkdir(tempDir, { recursive: true });

      try {
        await tar.extract({
          file: tarPath,
          cwd: tempDir,
        });

        // Count files
        let fileCount = 0;
        const countFiles = async (dir: string): Promise<void> => {
          const entries = await fs.readdir(dir, { withFileTypes: true });
          for (const entry of entries) {
            if (entry.isFile()) {
              fileCount++;
            } else if (entry.isDirectory()) {
              await countFiles(path.join(dir, entry.name));
            }
          }
        };

        await countFiles(tempDir);

        // Clean up
        await fs.rm(tempDir, { recursive: true, force: true });

        return {
          success: true,
          data: {
            valid: checksumMatch,
            checksum: currentChecksum,
            checksumMatch,
            fileCount,
            agentsIncluded: metadata.agents
          }
        };
      } catch (extractError) {
        // Failed to extract - corrupted archive
        await fs.rm(tempDir, { recursive: true, force: true }).catch(() => {});
        return {
          success: true,
          data: {
            valid: false,
            checksum: currentChecksum,
            checksumMatch: false,
            fileCount: 0,
            agentsIncluded: metadata.agents
          }
        };
      }
    } catch (error) {
      return { success: false, error: (error as Error).message };
    }
  }

  /**
   * Restore from backup (test-compatible signature)
   */
  async restore(backupId: string, options?: { agents?: string[]; createBackupBeforeRestore?: boolean }): Promise<OperationResult<{ preRestoreBackupId?: string }>> {
    try {
      // Check if backup exists
      const metadata = this.backups.get(backupId);
      if (!metadata) {
        return { success: false, error: 'Backup not found' };
      }

      // Validate backup first
      const validation = await this.validateBackup(backupId);
      if (!validation.success || !validation.data?.valid) {
        return { success: false, error: 'Backup validation failed' };
      }

      // Create pre-restore backup if requested
      let preRestoreBackupId: string | undefined;
      if (options?.createBackupBeforeRestore) {
        const preBackup = await this.createFullBackup();
        if (preBackup.success && preBackup.data) {
          preRestoreBackupId = preBackup.data.backupId;
        }
      }

      // Perform restore
      const restoreResult = await this.restoreBackup({
        backupId,
        agents: options?.agents,
        overwrite: true,
        validateIntegrity: false // Already validated above
      });

      if (!restoreResult.success) {
        return { success: false, error: restoreResult.error };
      }

      return {
        success: true,
        data: preRestoreBackupId ? { preRestoreBackupId } : {}
      };
    } catch (error) {
      return { success: false, error: (error as Error).message };
    }
  }

  /**
   * Restore to point in time
   */
  async restoreToPointInTime(timestamp: string): Promise<OperationResult> {
    try {
      const targetTime = new Date(timestamp).getTime();
      const backupsArray = Array.from(this.backups.values());

      // Find backup closest to target time
      let closestBackup: BackupMetadata | null = null;
      let smallestDiff = Infinity;

      for (const backup of backupsArray) {
        const backupTime = new Date(backup.timestamp).getTime();
        const diff = Math.abs(targetTime - backupTime);
        if (diff < smallestDiff) {
          smallestDiff = diff;
          closestBackup = backup;
        }
      }

      if (!closestBackup) {
        return { success: false, error: 'No backup found near target time' };
      }

      return await this.restore(closestBackup.id);
    } catch (error) {
      return { success: false, error: (error as Error).message };
    }
  }

  /**
   * List all backups (test-compatible signature)
   */
  async listBackups(): Promise<OperationResult<Array<{ id: string; timestamp: string; type: 'full' | 'incremental'; sizeBytes: number; agents: string[] }>>> {
    try {
      const backups = Array.from(this.backups.values())
        .sort((a, b) => new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime())
        .map(b => ({
          id: b.id,
          timestamp: b.timestamp,
          type: b.type,
          sizeBytes: b.totalSize,
          agents: b.agents
        }));

      return { success: true, data: backups };
    } catch (error) {
      return { success: false, error: (error as Error).message };
    }
  }

  /**
   * Delete backups older than a date
   */
  async deleteBackupsOlderThan(date: Date): Promise<OperationResult<{ deletedCount: number }>> {
    try {
      const targetTime = date.getTime();
      const backups = Array.from(this.backups.values());
      let deletedCount = 0;

      for (const backup of backups) {
        const backupTime = new Date(backup.timestamp).getTime();
        if (backupTime < targetTime) {
          const deleteResult = await this.deleteBackup(backup.id);
          if (deleteResult.success) {
            deletedCount++;
          }
        }
      }

      return { success: true, data: { deletedCount } };
    } catch (error) {
      return { success: false, error: (error as Error).message };
    }
  }

  /**
   * Keep only last N backups
   */
  async keepLastNBackups(n: number): Promise<OperationResult<{ deletedCount: number }>> {
    try {
      const backups = Array.from(this.backups.values())
        .sort((a, b) => new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime());

      let deletedCount = 0;

      // Delete all backups beyond the first N
      for (let i = n; i < backups.length; i++) {
        const deleteResult = await this.deleteBackup(backups[i].id);
        if (deleteResult.success) {
          deletedCount++;
        }
      }

      return { success: true, data: { deletedCount } };
    } catch (error) {
      return { success: false, error: (error as Error).message };
    }
  }

  /**
   * Get backup info
   */
  async getBackupInfo(backupId: string): Promise<OperationResult<{ id: string; timestamp: string; type: 'full' | 'incremental'; sizeBytes: number; agents: string[] }>> {
    try {
      const metadata = this.backups.get(backupId);
      if (!metadata) {
        return { success: false, error: 'Backup not found' };
      }

      return {
        success: true,
        data: {
          id: metadata.id,
          timestamp: metadata.timestamp,
          type: metadata.type,
          sizeBytes: metadata.totalSize,
          agents: metadata.agents
        }
      };
    } catch (error) {
      return { success: false, error: (error as Error).message };
    }
  }

  // ============================================================================
  // PRIVATE METHODS
  // ============================================================================

  /**
   * Load backup metadata from disk
   */
  private async loadBackupMetadata(): Promise<void> {
    try {
      const files = await fs.readdir(this.backupPath);
      const metaFiles = files.filter((f) => f.endsWith('.meta.json'));

      for (const file of metaFiles) {
        const filePath = path.join(this.backupPath, file);
        const content = await fs.readFile(filePath, 'utf-8');
        const metadata: BackupMetadata = JSON.parse(content);
        this.backups.set(metadata.id, metadata);
      }
    } catch (error) {
      // Backup path doesn't exist yet, ignore
    }
  }

  /**
   * Save backup metadata to disk
   */
  private async saveBackupMetadata(metadata: BackupMetadata): Promise<void> {
    const metadataPath = path.join(this.backupPath, `${metadata.id}.meta.json`);
    await fs.writeFile(metadataPath, JSON.stringify(metadata, null, 2));
  }
}
