/**
 * Memory Store - High-level interface for storing and retrieving memory data
 */

import { FileStorage } from './FileStorage';
import { Pattern, Solution, Decision, Metrics } from '../models';
import { AgentName } from '../types/common';

export interface MemoryData {
  patterns: Pattern[];
  solutions: Solution[];
  decisions: Decision[];
  metrics?: Metrics;
  context?: Record<string, unknown>;
}

export class MemoryStore {
  private storage: FileStorage;

  constructor(basePath: string, compression: boolean = true) {
    this.storage = new FileStorage(basePath, { compression });
  }

  /**
   * Initialize storage directory structure
   */
  async initialize(): Promise<void> {
    await this.storage.initialize();
  }

  /**
   * Load all memory data for an agent
   */
  async loadAgentMemory(agentName: AgentName): Promise<MemoryData> {
    const patterns = (await this.storage.read<Pattern[]>(`${agentName}/patterns.json`)) || [];
    const solutions = (await this.storage.read<Solution[]>(`${agentName}/solutions.json`)) || [];
    const decisions = (await this.storage.read<Decision[]>(`${agentName}/decisions.json`)) || [];
    const metrics = (await this.storage.read<Metrics>(`${agentName}/metrics.json`)) || undefined;
    const context =
      (await this.storage.read<Record<string, unknown>>(`${agentName}/context.json`)) || undefined;

    return {
      patterns,
      solutions,
      decisions,
      metrics,
      context,
    };
  }

  /**
   * Save patterns for an agent
   */
  async savePatterns(agentName: AgentName, patterns: Pattern[]): Promise<void> {
    await this.storage.write(`${agentName}/patterns.json`, patterns);
  }

  /**
   * Save solutions for an agent
   */
  async saveSolutions(agentName: AgentName, solutions: Solution[]): Promise<void> {
    await this.storage.write(`${agentName}/solutions.json`, solutions);
  }

  /**
   * Save decisions for an agent
   */
  async saveDecisions(agentName: AgentName, decisions: Decision[]): Promise<void> {
    await this.storage.write(`${agentName}/decisions.json`, decisions);
  }

  /**
   * Save metrics for an agent
   */
  async saveMetrics(agentName: AgentName, metrics: Metrics): Promise<void> {
    await this.storage.write(`${agentName}/metrics.json`, metrics);
  }

  /**
   * Save context for an agent
   */
  async saveContext(agentName: AgentName, context: Record<string, unknown>): Promise<void> {
    await this.storage.write(`${agentName}/context.json`, context);
  }

  /**
   * Save all memory data for an agent
   */
  async saveAgentMemory(agentName: AgentName, data: MemoryData): Promise<void> {
    await this.savePatterns(agentName, data.patterns);
    await this.saveSolutions(agentName, data.solutions);
    await this.saveDecisions(agentName, data.decisions);

    if (data.metrics) {
      await this.saveMetrics(agentName, data.metrics);
    }

    if (data.context) {
      await this.saveContext(agentName, data.context);
    }
  }

  /**
   * Delete all memory data for an agent
   */
  async deleteAgentMemory(agentName: AgentName): Promise<void> {
    await this.storage.delete(`${agentName}/patterns.json`);
    await this.storage.delete(`${agentName}/solutions.json`);
    await this.storage.delete(`${agentName}/decisions.json`);
    await this.storage.delete(`${agentName}/metrics.json`);
    await this.storage.delete(`${agentName}/context.json`);
    await this.storage.delete(`${agentName}/index.json`);
  }

  /**
   * Check if agent has any memory data
   */
  async agentHasMemory(agentName: AgentName): Promise<boolean> {
    return (
      (await this.storage.exists(`${agentName}/patterns.json`)) ||
      (await this.storage.exists(`${agentName}/solutions.json`)) ||
      (await this.storage.exists(`${agentName}/decisions.json`))
    );
  }

  /**
   * Get memory size for an agent in bytes
   */
  async getAgentMemorySize(agentName: AgentName): Promise<number> {
    return await this.storage.getDirectorySize(agentName);
  }

  /**
   * Get total memory size in bytes
   */
  async getTotalMemorySize(): Promise<number> {
    return await this.storage.getDirectorySize();
  }

  /**
   * List all agents with memory data
   */
  async listAgents(): Promise<AgentName[]> {
    const files = await this.storage.listRecursive();
    const agents = new Set<string>();

    for (const file of files) {
      const parts = file.split('/');
      if (parts.length > 1) {
        agents.add(parts[0]);
      }
    }

    return Array.from(agents);
  }

  /**
   * Create backup of agent memory
   */
  async backupAgentMemory(agentName: AgentName, backupPath?: string): Promise<string[]> {
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    const backupDir = backupPath || `backup/${agentName}-${timestamp}`;
    const backedUpFiles: string[] = [];

    const files = ['patterns.json', 'solutions.json', 'decisions.json', 'metrics.json', 'context.json', 'index.json'];

    for (const file of files) {
      const filePath = `${agentName}/${file}`;
      if (await this.storage.exists(filePath)) {
        const targetPath = `${backupDir}/${file}`;
        await this.storage.backup(filePath, targetPath);
        backedUpFiles.push(targetPath);
      }
    }

    return backedUpFiles;
  }

  /**
   * Restore agent memory from backup
   */
  async restoreAgentMemory(agentName: AgentName, backupPath: string): Promise<void> {
    const files = ['patterns.json', 'solutions.json', 'decisions.json', 'metrics.json', 'context.json', 'index.json'];

    for (const file of files) {
      const sourcePath = `${backupPath}/${file}`;
      if (await this.storage.exists(sourcePath)) {
        const targetPath = `${agentName}/${file}`;
        await this.storage.restore(sourcePath, targetPath);
      }
    }
  }

  /**
   * Load global cross-agent data
   */
  async loadGlobalData<T>(filename: string): Promise<T | null> {
    return await this.storage.read<T>(`global/${filename}`);
  }

  /**
   * Save global cross-agent data
   */
  async saveGlobalData<T>(filename: string, data: T): Promise<void> {
    await this.storage.write(`global/${filename}`, data);
  }

  /**
   * Get storage base path
   */
  getBasePath(): string {
    return this.storage.getBasePath();
  }
}
