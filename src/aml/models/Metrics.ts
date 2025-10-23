/**
 * Metrics Model - Tracks performance and learning metrics for agents
 */

import { z } from 'zod';
import { AgentName, Timestamp } from '../types/common';

// Zod schemas for validation
export const PerformanceMetricsSchema = z.object({
  avgQueryLatencyMs: z.number().min(0),
  avgWriteLatencyMs: z.number().min(0),
  cacheHitRate: z.number().min(0).max(1),
  totalQueries: z.number().int().min(0),
  totalWrites: z.number().int().min(0),
});

export const LearningMetricsSchema = z.object({
  totalPatterns: z.number().int().min(0),
  activePatterns: z.number().int().min(0),
  totalSolutions: z.number().int().min(0),
  activeSolutions: z.number().int().min(0),
  totalDecisions: z.number().int().min(0),
  activeDecisions: z.number().int().min(0),
  avgPatternConfidence: z.number().min(0).max(1),
  avgSolutionConfidence: z.number().min(0).max(1),
});

export const UsageMetricsSchema = z.object({
  patternUsageCount: z.number().int().min(0),
  solutionUsageCount: z.number().int().min(0),
  decisionReferenceCount: z.number().int().min(0),
  errorPreventionCount: z.number().int().min(0),
  timeSavedMs: z.number().min(0),
});

export const StorageMetricsSchema = z.object({
  totalSizeBytes: z.number().int().min(0),
  patternsSizeBytes: z.number().int().min(0),
  solutionsSizeBytes: z.number().int().min(0),
  decisionsSizeBytes: z.number().int().min(0),
  compressionRatio: z.number().min(0).max(1),
});

export const MetricsSchema = z.object({
  agent: z.string(),
  timestamp: z.string(),
  performance: PerformanceMetricsSchema,
  learning: LearningMetricsSchema,
  usage: UsageMetricsSchema,
  storage: StorageMetricsSchema,
  period: z.enum(['hourly', 'daily', 'weekly', 'monthly']),
});

// TypeScript types
export type PerformanceMetrics = z.infer<typeof PerformanceMetricsSchema>;
export type LearningMetrics = z.infer<typeof LearningMetricsSchema>;
export type UsageMetrics = z.infer<typeof UsageMetricsSchema>;
export type StorageMetrics = z.infer<typeof StorageMetricsSchema>;
export type Metrics = z.infer<typeof MetricsSchema>;

/**
 * Metrics class with helper methods
 */
export class MetricsModel {
  private data: Metrics;

  constructor(data: Metrics) {
    this.data = MetricsSchema.parse(data);
  }

  get agent(): AgentName {
    return this.data.agent;
  }

  get timestamp(): Timestamp {
    return this.data.timestamp;
  }

  /**
   * Check if performance meets SLA requirements
   */
  meetsPerformanceSLA(): boolean {
    const perf = this.data.performance;
    return (
      perf.avgQueryLatencyMs < 50 && perf.avgWriteLatencyMs < 100 && perf.cacheHitRate > 0.8
    );
  }

  /**
   * Calculate overall health score (0-1)
   */
  calculateHealthScore(): number {
    const scores: number[] = [];

    // Performance score
    const perfScore =
      Math.min(50 / this.data.performance.avgQueryLatencyMs, 1.0) * 0.3 +
      Math.min(100 / this.data.performance.avgWriteLatencyMs, 1.0) * 0.2 +
      this.data.performance.cacheHitRate * 0.5;
    scores.push(perfScore);

    // Learning score
    const learningScore =
      this.data.learning.avgPatternConfidence * 0.5 + this.data.learning.avgSolutionConfidence * 0.5;
    scores.push(learningScore);

    // Storage efficiency score
    const storageScore = this.data.storage.compressionRatio;
    scores.push(storageScore);

    return scores.reduce((a, b) => a + b, 0) / scores.length;
  }

  /**
   * Get storage utilization percentage
   */
  getStorageUtilization(limitBytes: number): number {
    return this.data.storage.totalSizeBytes / limitBytes;
  }

  /**
   * Check if storage is approaching limits
   */
  isStorageWarning(limitBytes: number, warningThreshold: number = 0.8): boolean {
    return this.getStorageUtilization(limitBytes) > warningThreshold;
  }

  /**
   * Get formatted summary
   */
  getSummary(): string {
    return `Agent: ${this.data.agent}
Performance: ${this.data.performance.avgQueryLatencyMs.toFixed(1)}ms query, ${this.data.performance.cacheHitRate.toFixed(2)} cache hit rate
Learning: ${this.data.learning.totalPatterns} patterns, ${this.data.learning.totalSolutions} solutions
Storage: ${(this.data.storage.totalSizeBytes / 1024 / 1024).toFixed(2)} MB
Health: ${(this.calculateHealthScore() * 100).toFixed(1)}%`;
  }

  /**
   * Get raw data
   */
  toJSON(): Metrics {
    return { ...this.data };
  }

  /**
   * Create empty metrics for an agent
   */
  static createEmpty(agent: AgentName, period: Metrics['period'] = 'daily'): MetricsModel {
    const metrics: Metrics = {
      agent,
      timestamp: new Date().toISOString(),
      performance: {
        avgQueryLatencyMs: 0,
        avgWriteLatencyMs: 0,
        cacheHitRate: 0,
        totalQueries: 0,
        totalWrites: 0,
      },
      learning: {
        totalPatterns: 0,
        activePatterns: 0,
        totalSolutions: 0,
        activeSolutions: 0,
        totalDecisions: 0,
        activeDecisions: 0,
        avgPatternConfidence: 0,
        avgSolutionConfidence: 0,
      },
      usage: {
        patternUsageCount: 0,
        solutionUsageCount: 0,
        decisionReferenceCount: 0,
        errorPreventionCount: 0,
        timeSavedMs: 0,
      },
      storage: {
        totalSizeBytes: 0,
        patternsSizeBytes: 0,
        solutionsSizeBytes: 0,
        decisionsSizeBytes: 0,
        compressionRatio: 1.0,
      },
      period,
    };

    return new MetricsModel(metrics);
  }

  /**
   * Validate metrics data
   */
  static validate(data: unknown): { valid: boolean; errors?: string[] } {
    const result = MetricsSchema.safeParse(data);
    if (result.success) {
      return { valid: true };
    }
    return {
      valid: false,
      errors: result.error.errors.map((e) => `${e.path.join('.')}: ${e.message}`),
    };
  }
}
