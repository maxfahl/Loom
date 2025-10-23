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

export interface BackupMetadata {
  id: string;
  timestamp: Timestamp;
  agents: AgentName[];
  totalSize: number;
  compressed: boolean;
  encrypted: boolean;
  type: 'full' | 'incremental';
  parentBackupId?: string;
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

      // Create backup directory
      const backupDir = path.join(this.backupPath, backupId);
      await fs.mkdir(backupDir, { recursive: true });

      let totalSize = 0;
      const backedUpAgents: AgentName[] = [];

      // Backup each agent
      for (const agent of agents) {
        const agentBackupPath = path.join(backupId, agent);
        const files = await this.store.backupAgentMemory(agent, agentBackupPath);

        if (files.length > 0) {
          backedUpAgents.push(agent);
          // Calculate size
          for (const file of files) {
            const fullPath = path.join(this.store.getBasePath(), file);
            const stats = await fs.stat(fullPath);
            totalSize += stats.size;
          }
        }
      }

      // Backup global data if requested
      if (options.includeGlobal) {
        const globalData = await this.store.loadGlobalData('cross-agent.json');
        if (globalData) {
          const globalPath = path.join(backupDir, 'global.json');
          await fs.writeFile(globalPath, JSON.stringify(globalData, null, 2));
        }
      }

      // Create metadata
      const metadata: BackupMetadata = {
        id: backupId,
        timestamp,
        agents: backedUpAgents,
        totalSize,
        compressed: options.compress || true,
        encrypted: options.encrypt || false,
        type: options.type || 'full',
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

      // Validate integrity if requested
      if (options.validateIntegrity) {
        const valid = await this.validateBackup(options.backupId);
        if (!valid) {
          return { success: false, error: 'Backup integrity check failed' };
        }
      }

      // Determine which agents to restore
      const agentsToRestore = options.agents || metadata.agents;

      // Restore each agent
      for (const agent of agentsToRestore) {
        if (!metadata.agents.includes(agent)) {
          continue; // Skip agents not in backup
        }

        // Check if agent memory exists
        const exists = await this.store.agentHasMemory(agent);

        if (exists && !options.overwrite) {
          // Skip if exists and overwrite not enabled
          continue;
        }

        // Restore agent memory
        const backupPath = path.join(options.backupId, agent);
        await this.store.restoreAgentMemory(agent, backupPath);
      }

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

      // Delete backup directory
      const backupDir = path.join(this.backupPath, backupId);
      await fs.rm(backupDir, { recursive: true, force: true });

      // Delete metadata
      const metadataPath = path.join(this.backupPath, `${backupId}.meta.json`);
      await fs.unlink(metadataPath);

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
   * Validate backup integrity
   */
  async validateBackup(backupId: string): Promise<boolean> {
    try {
      const metadata = this.backups.get(backupId);
      if (!metadata) return false;

      const backupDir = path.join(this.backupPath, backupId);

      // Check if backup directory exists
      await fs.access(backupDir);

      // Check if all agent files exist
      for (const agent of metadata.agents) {
        const agentDir = path.join(backupDir, agent);
        await fs.access(agentDir);
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
