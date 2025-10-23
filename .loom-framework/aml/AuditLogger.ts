/**
 * Audit Logger - Security and compliance logging
 *
 * Records all significant operations for security auditing and compliance.
 * Supports GDPR, data access tracking, and security event monitoring.
 */

import { AgentName, Timestamp } from './types/common';
import * as fs from 'fs/promises';
import * as path from 'path';

export type AuditEventType =
  | 'pattern_created'
  | 'pattern_updated'
  | 'pattern_deleted'
  | 'pattern_accessed'
  | 'solution_created'
  | 'solution_updated'
  | 'solution_deleted'
  | 'solution_accessed'
  | 'decision_created'
  | 'decision_updated'
  | 'decision_deleted'
  | 'decision_accessed'
  | 'memory_exported'
  | 'memory_imported'
  | 'memory_cleared'
  | 'backup_created'
  | 'backup_restored'
  | 'config_changed'
  | 'sensitive_data_accessed';

export interface AuditEvent {
  id: string;
  timestamp: Timestamp;
  type: AuditEventType;
  agent: AgentName;
  action: string;
  resourceId?: string;
  resourceType?: 'pattern' | 'solution' | 'decision' | 'config' | 'backup';
  success: boolean;
  error?: string;
  metadata?: Record<string, unknown>;
  sensitiveData?: boolean;
  ipAddress?: string;
  userId?: string;
}

export interface AuditQuery {
  agent?: AgentName;
  type?: AuditEventType;
  resourceId?: string;
  startTime?: Timestamp;
  endTime?: Timestamp;
  success?: boolean;
  sensitiveData?: boolean;
  limit?: number;
}

export interface AuditReport {
  totalEvents: number;
  eventsByType: Map<AuditEventType, number>;
  eventsByAgent: Map<AgentName, number>;
  successRate: number;
  sensitiveDataAccesses: number;
  timeRange: { start: Timestamp; end: Timestamp };
}

/**
 * Audit Logger class
 */
export class AuditLogger {
  private logPath: string;
  private events: AuditEvent[];
  private maxEventsInMemory: number;
  private flushInterval: number;
  private flushTimer: NodeJS.Timeout | null;

  constructor(logPath: string = '.loom/memory/audit', maxEventsInMemory: number = 1000) {
    this.logPath = logPath;
    this.events = [];
    this.maxEventsInMemory = maxEventsInMemory;
    this.flushInterval = 60000; // Flush every minute
    this.flushTimer = null;
  }

  /**
   * Initialize audit logger
   */
  async initialize(): Promise<void> {
    await fs.mkdir(this.logPath, { recursive: true });
    this.startAutoFlush();
  }

  /**
   * Log an audit event
   */
  async log(event: Omit<AuditEvent, 'id' | 'timestamp'>): Promise<void> {
    const auditEvent: AuditEvent = {
      id: crypto.randomUUID(),
      timestamp: new Date().toISOString(),
      ...event,
    };

    this.events.push(auditEvent);

    // Auto-flush if buffer is full
    if (this.events.length >= this.maxEventsInMemory) {
      await this.flush();
    }
  }

  /**
   * Log pattern creation
   */
  async logPatternCreated(
    agent: AgentName,
    patternId: string,
    metadata?: Record<string, unknown>
  ): Promise<void> {
    await this.log({
      type: 'pattern_created',
      agent,
      action: 'Pattern created',
      resourceId: patternId,
      resourceType: 'pattern',
      success: true,
      metadata,
    });
  }

  /**
   * Log pattern access
   */
  async logPatternAccessed(agent: AgentName, patternId: string): Promise<void> {
    await this.log({
      type: 'pattern_accessed',
      agent,
      action: 'Pattern accessed',
      resourceId: patternId,
      resourceType: 'pattern',
      success: true,
    });
  }

  /**
   * Log solution creation
   */
  async logSolutionCreated(
    agent: AgentName,
    solutionId: string,
    metadata?: Record<string, unknown>
  ): Promise<void> {
    await this.log({
      type: 'solution_created',
      agent,
      action: 'Solution created',
      resourceId: solutionId,
      resourceType: 'solution',
      success: true,
      metadata,
    });
  }

  /**
   * Log memory export (GDPR data portability)
   */
  async logMemoryExported(agent: AgentName, exportSize: number): Promise<void> {
    await this.log({
      type: 'memory_exported',
      agent,
      action: 'Memory exported',
      success: true,
      metadata: { exportSize },
      sensitiveData: true,
    });
  }

  /**
   * Log memory cleared (GDPR right to deletion)
   */
  async logMemoryCleared(agent: AgentName): Promise<void> {
    await this.log({
      type: 'memory_cleared',
      agent,
      action: 'Memory cleared',
      success: true,
      sensitiveData: true,
    });
  }

  /**
   * Log configuration change
   */
  async logConfigChanged(
    agent: AgentName,
    changes: Record<string, unknown>
  ): Promise<void> {
    await this.log({
      type: 'config_changed',
      agent,
      action: 'Configuration changed',
      resourceType: 'config',
      success: true,
      metadata: changes,
    });
  }

  /**
   * Log backup creation
   */
  async logBackupCreated(backupId: string, metadata?: Record<string, unknown>): Promise<void> {
    await this.log({
      type: 'backup_created',
      agent: 'system',
      action: 'Backup created',
      resourceId: backupId,
      resourceType: 'backup',
      success: true,
      metadata,
    });
  }

  /**
   * Log error event
   */
  async logError(
    type: AuditEventType,
    agent: AgentName,
    action: string,
    error: string
  ): Promise<void> {
    await this.log({
      type,
      agent,
      action,
      success: false,
      error,
    });
  }

  /**
   * Query audit logs
   */
  async query(query: AuditQuery): Promise<AuditEvent[]> {
    // Load recent logs from disk if needed
    await this.loadRecentLogs();

    let filtered = this.events;

    // Filter by agent
    if (query.agent) {
      filtered = filtered.filter((e) => e.agent === query.agent);
    }

    // Filter by type
    if (query.type) {
      filtered = filtered.filter((e) => e.type === query.type);
    }

    // Filter by resource ID
    if (query.resourceId) {
      filtered = filtered.filter((e) => e.resourceId === query.resourceId);
    }

    // Filter by time range
    if (query.startTime) {
      filtered = filtered.filter((e) => e.timestamp >= query.startTime!);
    }
    if (query.endTime) {
      filtered = filtered.filter((e) => e.timestamp <= query.endTime!);
    }

    // Filter by success
    if (query.success !== undefined) {
      filtered = filtered.filter((e) => e.success === query.success);
    }

    // Filter by sensitive data
    if (query.sensitiveData !== undefined) {
      filtered = filtered.filter((e) => e.sensitiveData === query.sensitiveData);
    }

    // Limit results
    if (query.limit) {
      filtered = filtered.slice(-query.limit); // Get most recent N events
    }

    return filtered;
  }

  /**
   * Generate audit report
   */
  async generateReport(startTime: Timestamp, endTime: Timestamp): Promise<AuditReport> {
    const events = await this.query({ startTime, endTime });

    const eventsByType = new Map<AuditEventType, number>();
    const eventsByAgent = new Map<AgentName, number>();
    let successCount = 0;
    let sensitiveDataAccesses = 0;

    for (const event of events) {
      // Count by type
      eventsByType.set(event.type, (eventsByType.get(event.type) || 0) + 1);

      // Count by agent
      eventsByAgent.set(event.agent, (eventsByAgent.get(event.agent) || 0) + 1);

      // Count successes
      if (event.success) successCount++;

      // Count sensitive data accesses
      if (event.sensitiveData) sensitiveDataAccesses++;
    }

    return {
      totalEvents: events.length,
      eventsByType,
      eventsByAgent,
      successRate: events.length > 0 ? successCount / events.length : 1.0,
      sensitiveDataAccesses,
      timeRange: { start: startTime, end: endTime },
    };
  }

  /**
   * Flush events to disk
   */
  async flush(): Promise<void> {
    if (this.events.length === 0) return;

    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    const logFile = path.join(this.logPath, `audit-${timestamp}.json`);

    try {
      await fs.writeFile(logFile, JSON.stringify(this.events, null, 2));
      this.events = []; // Clear buffer after successful write
    } catch (error) {
      console.error('Failed to flush audit logs:', error);
    }
  }

  /**
   * Start auto-flush
   */
  private startAutoFlush(): void {
    if (this.flushTimer) return;

    this.flushTimer = setInterval(async () => {
      await this.flush();
    }, this.flushInterval);
  }

  /**
   * Stop auto-flush
   */
  stop(): void {
    if (this.flushTimer) {
      clearInterval(this.flushTimer);
      this.flushTimer = null;
    }
    // Final flush
    this.flush();
  }

  /**
   * Load recent logs from disk
   */
  private async loadRecentLogs(): Promise<void> {
    try {
      const files = await fs.readdir(this.logPath);
      const logFiles = files.filter((f) => f.startsWith('audit-') && f.endsWith('.json'));

      // Load only the most recent log file to avoid memory issues
      if (logFiles.length > 0) {
        logFiles.sort().reverse();
        const recentFile = logFiles[0];
        const filePath = path.join(this.logPath, recentFile);
        const content = await fs.readFile(filePath, 'utf-8');
        const events: AuditEvent[] = JSON.parse(content);

        // Merge with current events (avoid duplicates)
        const existingIds = new Set(this.events.map((e) => e.id));
        for (const event of events) {
          if (!existingIds.has(event.id)) {
            this.events.push(event);
          }
        }
      }
    } catch (error) {
      // Ignore errors (logs might not exist yet)
    }
  }

  /**
   * Delete old audit logs (retention policy)
   */
  async deleteOldLogs(retentionDays: number): Promise<number> {
    try {
      const files = await fs.readdir(this.logPath);
      const logFiles = files.filter((f) => f.startsWith('audit-') && f.endsWith('.json'));

      const now = Date.now();
      const maxAgeMs = retentionDays * 24 * 60 * 60 * 1000;
      let deleted = 0;

      for (const file of logFiles) {
        const filePath = path.join(this.logPath, file);
        const stats = await fs.stat(filePath);
        const age = now - stats.mtimeMs;

        if (age > maxAgeMs) {
          await fs.unlink(filePath);
          deleted++;
        }
      }

      return deleted;
    } catch (error) {
      return 0;
    }
  }
}
