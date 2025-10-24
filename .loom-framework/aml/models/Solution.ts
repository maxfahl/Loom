/**
 * Solution Model - Represents an error resolution learned by an agent
 */

import { z } from 'zod';
import { AgentName, SolutionId, Context } from '../types/common';

// Zod schemas for validation
export const ProblemContextSchema = z.record(z.union([z.string(), z.number(), z.boolean()]));

export const ProblemSchema = z.object({
  errorType: z.string(),
  errorMessage: z.string(),
  stackTraceHash: z.string().optional(),
  context: ProblemContextSchema,
});

export const SolutionApproachSchema = z.object({
  rootCause: z.string(),
  fixApproach: z.string(),
  codeFix: z.string().optional(),
  prevention: z.string(),
  relatedPatterns: z.array(z.string()).optional(),
});

export const EffectivenessMetricsSchema = z.object({
  worked: z.boolean(),
  timeToFixMinutes: z.number().min(0),
  preventedRecurrence: z.number().int().min(0),
  relatedErrorsFixed: z.number().int().min(0),
});

export const SolutionSchema = z.object({
  id: z.string().uuid(),
  agent: z.string(),
  timestamp: z.string(),
  problem: ProblemSchema,
  solution: SolutionApproachSchema,
  effectiveness: EffectivenessMetricsSchema,
  tags: z.array(z.string()).optional(),
  active: z.boolean().default(true),
  verifiedCount: z.number().int().min(0).default(0),
});

// TypeScript types
export type ProblemContext = z.infer<typeof ProblemContextSchema>;
export type Problem = z.infer<typeof ProblemSchema>;
export type SolutionApproach = z.infer<typeof SolutionApproachSchema>;
export type EffectivenessMetrics = z.infer<typeof EffectivenessMetricsSchema>;
export type Solution = z.infer<typeof SolutionSchema>;

/**
 * Solution class with helper methods
 */
export class SolutionModel {
  private data: Solution;

  constructor(data: Solution) {
    this.data = SolutionSchema.parse(data);
  }

  get id(): SolutionId {
    return this.data.id;
  }

  get agent(): AgentName {
    return this.data.agent;
  }

  get errorType(): string {
    return this.data.problem.errorType;
  }

  get worked(): boolean {
    return this.data.effectiveness.worked;
  }

  get isActive(): boolean {
    return this.data.active ?? true;
  }

  /**
   * Check if this solution matches a given error
   */
  matchesError(errorType: string, errorMessage: string, context?: Context): boolean {
    // Exact error type match
    if (this.data.problem.errorType !== errorType) {
      return false;
    }

    // Check message similarity (simple contains check)
    const normalizedSolutionMsg = this.data.problem.errorMessage.toLowerCase();
    const normalizedErrorMsg = errorMessage.toLowerCase();

    const messageMatch =
      normalizedSolutionMsg.includes(normalizedErrorMsg) ||
      normalizedErrorMsg.includes(normalizedSolutionMsg);

    if (!messageMatch) {
      return false;
    }

    // Check context similarity if provided
    if (context) {
      const problemContext = this.data.problem.context;
      const matchingKeys = Object.keys(problemContext).filter(
        (key) => context[key] === problemContext[key]
      );
      const contextSimilarity = matchingKeys.length / Object.keys(problemContext).length;
      return contextSimilarity >= 0.5; // At least 50% context match
    }

    return true;
  }

  /**
   * Record that this solution was verified/used
   */
  recordVerification(worked: boolean, timeToFixMinutes: number = 0): void {
    this.data.verifiedCount++;
    this.data.effectiveness.worked = worked;

    if (worked) {
      this.data.effectiveness.preventedRecurrence++;
      if (timeToFixMinutes > 0) {
        this.data.effectiveness.timeToFixMinutes = timeToFixMinutes;
      }
    }
  }

  /**
   * Calculate solution confidence score
   */
  calculateConfidence(): number {
    // Base confidence from whether it worked
    const baseConfidence = this.data.effectiveness.worked ? 0.7 : 0.3;

    // Verification bonus (more verifications = higher confidence)
    const verificationBonus = Math.min(this.data.verifiedCount * 0.05, 0.2);

    // Recurrence prevention bonus
    const preventionBonus = Math.min(this.data.effectiveness.preventedRecurrence * 0.02, 0.1);

    return Math.min(baseConfidence + verificationBonus + preventionBonus, 1.0);
  }

  /**
   * Calculate solution weight for ranking
   */
  calculateWeight(): number {
    const confidence = this.calculateConfidence();
    const recencyDays =
      (Date.now() - new Date(this.data.timestamp).getTime()) / (1000 * 60 * 60 * 24);
    const recencyFactor = Math.exp(-recencyDays / 60); // Decay over 60 days

    return confidence * 0.7 + recencyFactor * 0.3;
  }

  /**
   * Deactivate solution (soft delete)
   */
  deactivate(): void {
    this.data.active = false;
  }

  /**
   * Get raw data
   */
  toJSON(): Solution {
    return { ...this.data };
  }

  /**
   * Create a new solution
   */
  static create(
    agent: AgentName,
    problem: Problem,
    solution: SolutionApproach,
    effectiveness: EffectivenessMetrics
  ): SolutionModel {
    const solutionData: Solution = {
      id: crypto.randomUUID(),
      agent,
      timestamp: new Date().toISOString(),
      problem,
      solution,
      effectiveness,
      active: true,
      verifiedCount: 1,
    };

    return new SolutionModel(solutionData);
  }

  /**
   * Validate solution data
   */
  static validate(data: unknown): { valid: boolean; errors?: string[] } {
    const result = SolutionSchema.safeParse(data);
    if (result.success) {
      return { valid: true };
    }
    return {
      valid: false,
      errors: result.error.errors.map((e) => `${e.path.join('.')}: ${e.message}`),
    };
  }
}
