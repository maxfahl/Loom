/**
 * Pattern Model - Represents a successful implementation pattern learned by an agent
 */

import { z } from 'zod';
import { AgentName, PatternId, Timestamp, Context } from '../types/common';

// Zod schemas for validation
export const PatternConditionsSchema = z.object({
  whenApplicable: z.array(z.string()),
  whenNotApplicable: z.array(z.string()),
});

export const PatternApproachSchema = z.object({
  technique: z.string(),
  codeTemplate: z.string().optional(),
  rationale: z.string(),
  steps: z.array(z.string()).optional(),
});

export const PatternContextSchema = z.record(z.union([z.string(), z.number(), z.boolean()]));

export const PatternDefinitionSchema = z.object({
  type: z.string(),
  context: PatternContextSchema,
  approach: PatternApproachSchema,
  conditions: PatternConditionsSchema,
});

export const PatternMetricsSchema = z.object({
  successRate: z.number().min(0).max(1),
  executionCount: z.number().int().min(0),
  avgTimeSavedMs: z.number().min(0),
  errorPreventionCount: z.number().int().min(0),
});

export const PatternEvolutionSchema = z.object({
  created: z.string(), // ISO 8601 timestamp
  lastUsed: z.string(), // ISO 8601 timestamp
  refinements: z.number().int().min(0),
  confidenceScore: z.number().min(0).max(1),
});

export const PatternSchema = z.object({
  id: z.string().uuid(),
  agent: z.string(),
  timestamp: z.string(),
  pattern: PatternDefinitionSchema,
  metrics: PatternMetricsSchema,
  evolution: PatternEvolutionSchema,
  tags: z.array(z.string()).optional(),
  active: z.boolean().default(true),
});

// TypeScript types derived from schemas
export type PatternConditions = z.infer<typeof PatternConditionsSchema>;
export type PatternApproach = z.infer<typeof PatternApproachSchema>;
export type PatternContext = z.infer<typeof PatternContextSchema>;
export type PatternDefinition = z.infer<typeof PatternDefinitionSchema>;
export type PatternMetrics = z.infer<typeof PatternMetricsSchema>;
export type PatternEvolution = z.infer<typeof PatternEvolutionSchema>;
export type Pattern = z.infer<typeof PatternSchema>;

/**
 * Pattern class with helper methods
 */
export class PatternModel {
  private data: Pattern;

  constructor(data: Pattern) {
    this.data = PatternSchema.parse(data);
  }

  get id(): PatternId {
    return this.data.id;
  }

  get agent(): AgentName {
    return this.data.agent;
  }

  get confidenceScore(): number {
    return this.data.evolution.confidenceScore;
  }

  get successRate(): number {
    return this.data.metrics.successRate;
  }

  get isActive(): boolean {
    return this.data.active ?? true;
  }

  /**
   * Update confidence score based on success/failure
   */
  updateConfidence(success: boolean, learningRate: number = 0.1): void {
    const currentScore = this.data.evolution.confidenceScore;
    if (success) {
      this.data.evolution.confidenceScore = Math.min(currentScore * (1 + learningRate), 1.0);
    } else {
      this.data.evolution.confidenceScore = Math.max(currentScore * (1 - learningRate), 0.1);
    }
  }

  /**
   * Record pattern usage
   */
  recordUsage(success: boolean, timeSavedMs: number = 0): void {
    this.data.metrics.executionCount++;
    this.data.evolution.lastUsed = new Date().toISOString();
    this.data.evolution.refinements++;

    if (success) {
      const totalSuccess =
        this.data.metrics.successRate * (this.data.metrics.executionCount - 1) + 1;
      this.data.metrics.successRate = totalSuccess / this.data.metrics.executionCount;

      if (timeSavedMs > 0) {
        const totalTime =
          this.data.metrics.avgTimeSavedMs * (this.data.metrics.executionCount - 1) + timeSavedMs;
        this.data.metrics.avgTimeSavedMs = totalTime / this.data.metrics.executionCount;
      }
    } else {
      const totalSuccess = this.data.metrics.successRate * (this.data.metrics.executionCount - 1);
      this.data.metrics.successRate = totalSuccess / this.data.metrics.executionCount;
    }
  }

  /**
   * Check if pattern matches given context
   */
  matchesContext(context: Context): boolean {
    const patternContext = this.data.pattern.context;
    return Object.keys(patternContext).every((key) => {
      const patternValue = patternContext[key];
      const contextValue = context[key];
      return contextValue === patternValue;
    });
  }

  /**
   * Calculate pattern weight for decision making
   */
  calculateWeight(recencyFactorDays: number = 30): number {
    // Base weight from success rate
    const baseWeight = this.data.metrics.successRate;

    // Recency factor (more recent = higher weight)
    const daysOld =
      (Date.now() - new Date(this.data.evolution.lastUsed).getTime()) / (1000 * 60 * 60 * 24);
    const recencyFactor = Math.exp(-daysOld / recencyFactorDays);

    // Usage frequency factor
    const usageFrequency = Math.min(this.data.metrics.executionCount / 100, 1.0);

    // Confidence factor
    const confidenceFactor = this.data.evolution.confidenceScore;

    // Combined weight
    return baseWeight * 0.4 + recencyFactor * 0.3 + usageFrequency * 0.15 + confidenceFactor * 0.15;
  }

  /**
   * Deactivate pattern (soft delete)
   */
  deactivate(): void {
    this.data.active = false;
  }

  /**
   * Get raw data
   */
  toJSON(): Pattern {
    return { ...this.data };
  }

  /**
   * Create a new pattern from scratch
   */
  static create(
    agent: AgentName,
    type: string,
    context: PatternContext,
    approach: PatternApproach,
    conditions: PatternConditions
  ): PatternModel {
    const pattern: Pattern = {
      id: crypto.randomUUID(),
      agent,
      timestamp: new Date().toISOString(),
      pattern: {
        type,
        context,
        approach,
        conditions,
      },
      metrics: {
        successRate: 0.5, // Start neutral
        executionCount: 1,
        avgTimeSavedMs: 0,
        errorPreventionCount: 0,
      },
      evolution: {
        created: new Date().toISOString(),
        lastUsed: new Date().toISOString(),
        refinements: 0,
        confidenceScore: 0.3, // Start with low confidence
      },
      active: true,
    };

    return new PatternModel(pattern);
  }

  /**
   * Validate pattern data
   */
  static validate(data: unknown): { valid: boolean; errors?: string[] } {
    const result = PatternSchema.safeParse(data);
    if (result.success) {
      return { valid: true };
    }
    return {
      valid: false,
      errors: result.error.errors.map((e) => `${e.path.join('.')}: ${e.message}`),
    };
  }
}
