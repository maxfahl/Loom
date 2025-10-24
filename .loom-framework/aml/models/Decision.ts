/**
 * Decision Model - Represents architectural/design decisions made by agents
 */

import { z } from 'zod';
import { AgentName, DecisionId, Context } from '../types/common';

// Zod schemas for validation
export const DecisionContextSchema = z.record(z.union([z.string(), z.number(), z.boolean()]));

export const DecisionFactorsSchema = z.object({
  primary: z.array(z.string()),
  secondary: z.array(z.string()),
});

export const DecisionDefinitionSchema = z.object({
  type: z.string(),
  question: z.string(),
  context: DecisionContextSchema,
  chosenOption: z.string(),
  alternativesConsidered: z.array(z.string()),
  decisionFactors: DecisionFactorsSchema,
  rationale: z.string().optional(),
});

export const SuccessMetricsSchema = z.object({
  developmentSpeed: z.number().min(0).max(2).optional(), // Multiplier (1.0 = baseline)
  apiPerformance: z.number().min(0).max(1).optional(), // 0-1 score
  clientSatisfaction: z.number().min(0).max(1).optional(), // 0-1 score
  maintainability: z.number().min(0).max(1).optional(), // 0-1 score
  customMetrics: z.record(z.number()).optional(),
});

export const OutcomeSchema = z.object({
  successMetrics: SuccessMetricsSchema,
  lessonsLearned: z.array(z.string()),
  wouldRepeat: z.boolean(),
  improvements: z.array(z.string()).optional(),
});

export const DecisionSchema = z.object({
  id: z.string().uuid(),
  agent: z.string(),
  timestamp: z.string(),
  decision: DecisionDefinitionSchema,
  outcome: OutcomeSchema.optional(),
  tags: z.array(z.string()).optional(),
  active: z.boolean().default(true),
  reviewedAt: z.string().optional(),
});

// TypeScript types
export type DecisionContext = z.infer<typeof DecisionContextSchema>;
export type DecisionFactors = z.infer<typeof DecisionFactorsSchema>;
export type DecisionDefinition = z.infer<typeof DecisionDefinitionSchema>;
export type SuccessMetrics = z.infer<typeof SuccessMetricsSchema>;
export type Outcome = z.infer<typeof OutcomeSchema>;
export type Decision = z.infer<typeof DecisionSchema>;

/**
 * Decision class with helper methods
 */
export class DecisionModel {
  private data: Decision;

  constructor(data: Decision) {
    this.data = DecisionSchema.parse(data);
  }

  get id(): DecisionId {
    return this.data.id;
  }

  get agent(): AgentName {
    return this.data.agent;
  }

  get chosenOption(): string {
    return this.data.decision.chosenOption;
  }

  get wouldRepeat(): boolean {
    return this.data.outcome?.wouldRepeat ?? true;
  }

  get isActive(): boolean {
    return this.data.active ?? true;
  }

  get hasOutcome(): boolean {
    return this.data.outcome !== undefined;
  }

  /**
   * Check if this decision is similar to a given context
   */
  matchesContext(decisionType: string, context?: Context): boolean {
    if (this.data.decision.type !== decisionType) {
      return false;
    }

    if (!context) {
      return true;
    }

    const decisionContext = this.data.decision.context;
    const matchingKeys = Object.keys(decisionContext).filter(
      (key) => context[key] === decisionContext[key]
    );

    const similarity = matchingKeys.length / Math.max(Object.keys(decisionContext).length, 1);
    return similarity >= 0.5; // At least 50% context match
  }

  /**
   * Update outcome metrics after implementation
   */
  updateOutcome(outcome: Outcome): void {
    this.data.outcome = outcome;
    this.data.reviewedAt = new Date().toISOString();
  }

  /**
   * Calculate decision confidence based on outcomes
   */
  calculateConfidence(): number {
    if (!this.data.outcome) {
      return 0.5; // Neutral if no outcome data
    }

    const metrics = this.data.outcome.successMetrics;
    const scores: number[] = [];

    if (metrics.developmentSpeed !== undefined) {
      scores.push(Math.min(metrics.developmentSpeed / 1.5, 1.0)); // Normalize to 0-1
    }
    if (metrics.apiPerformance !== undefined) {
      scores.push(metrics.apiPerformance);
    }
    if (metrics.clientSatisfaction !== undefined) {
      scores.push(metrics.clientSatisfaction);
    }
    if (metrics.maintainability !== undefined) {
      scores.push(metrics.maintainability);
    }

    const avgScore = scores.length > 0 ? scores.reduce((a, b) => a + b, 0) / scores.length : 0.5;

    // Factor in whether they would repeat
    const repeatBonus = this.data.outcome.wouldRepeat ? 0.1 : -0.1;

    return Math.max(0.1, Math.min(avgScore + repeatBonus, 1.0));
  }

  /**
   * Calculate decision weight for recommendations
   */
  calculateWeight(): number {
    const confidence = this.calculateConfidence();

    // Recency factor
    const daysOld = (Date.now() - new Date(this.data.timestamp).getTime()) / (1000 * 60 * 60 * 24);
    const recencyFactor = Math.exp(-daysOld / 90); // Decay over 90 days

    // Has outcome bonus
    const outcomeBonus = this.hasOutcome ? 0.2 : 0.0;

    return confidence * 0.5 + recencyFactor * 0.3 + outcomeBonus;
  }

  /**
   * Get summary of decision for display
   */
  getSummary(): string {
    const decision = this.data.decision;
    return `${decision.question} -> ${decision.chosenOption} (over ${decision.alternativesConsidered.join(', ')})`;
  }

  /**
   * Deactivate decision (soft delete)
   */
  deactivate(): void {
    this.data.active = false;
  }

  /**
   * Get raw data
   */
  toJSON(): Decision {
    return { ...this.data };
  }

  /**
   * Create a new decision
   */
  static create(agent: AgentName, decision: DecisionDefinition): DecisionModel {
    const decisionData: Decision = {
      id: crypto.randomUUID(),
      agent,
      timestamp: new Date().toISOString(),
      decision,
      active: true,
    };

    return new DecisionModel(decisionData);
  }

  /**
   * Validate decision data
   */
  static validate(data: unknown): { valid: boolean; errors?: string[] } {
    const result = DecisionSchema.safeParse(data);
    if (result.success) {
      return { valid: true };
    }
    return {
      valid: false,
      errors: result.error.errors.map((e) => `${e.path.join('.')}: ${e.message}`),
    };
  }
}
