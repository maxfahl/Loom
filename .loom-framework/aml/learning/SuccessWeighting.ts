/**
 * Success Weighting System - Calculates dynamic weights for patterns based on multiple factors
 *
 * This module implements a sophisticated multi-factor weighting system that:
 * - Balances base success rate with contextual factors
 * - Applies exponential recency decay
 * - Considers pattern complexity and project fit
 * - Dynamically adjusts thresholds based on performance
 * - Calculates confidence intervals for reliability assessment
 */

import { Pattern } from '../models/Pattern';
import { Solution } from '../models/Solution';
import { Decision } from '../models/Decision';
import { Context } from '../types/common';

/**
 * Weight calculation result with detailed breakdown
 */
export interface WeightResult {
  totalWeight: number;
  factors: {
    baseSuccessRate: number; // 40% contribution
    recencyFactor: number; // 30% contribution
    complexityFactor: number; // 10% contribution
    projectFitFactor: number; // 20% contribution
  };
  confidence: number;
  confidenceInterval: {
    lower: number;
    upper: number;
  };
  recommendationStrength: 'weak' | 'moderate' | 'strong' | 'very-strong';
}

/**
 * Threshold adjustment parameters
 */
interface DynamicThresholds {
  minWeight: number; // Minimum weight to consider pattern
  confidenceLevel: number; // Required confidence level (0-1)
  sampleSizeMultiplier: number; // Adjust based on sample size
}

/**
 * Historical performance metrics for threshold adjustment
 */
interface PerformanceHistory {
  totalUsages: number;
  successfulUsages: number;
  avgWeight: number;
  stdDevWeight: number;
  recentTrend: 'improving' | 'stable' | 'declining';
}

/**
 * Configuration for success weighting
 */
export interface SuccessWeightingConfig {
  // Weight distribution (must sum to 1.0)
  weights: {
    baseSuccessRate: number; // Default: 0.4
    recencyFactor: number; // Default: 0.3
    complexityFactor: number; // Default: 0.1
    projectFitFactor: number; // Default: 0.2
  };

  // Recency decay parameters
  recency: {
    halfLifeDays: number; // Days until weight halves (default: 30)
    maxAgeDays: number; // Maximum age before weight reaches floor (default: 180)
    floorWeight: number; // Minimum weight from recency (default: 0.1)
  };

  // Complexity parameters
  complexity: {
    maxSteps: number; // Maximum steps before diminishing returns (default: 10)
    penaltyFactor: number; // Penalty for each additional step (default: 0.1)
  };

  // Confidence calculation
  confidence: {
    minSampleSize: number; // Minimum samples for high confidence (default: 10)
    confidenceLevel: number; // Z-score confidence level (default: 0.95)
  };

  // Dynamic threshold adjustment
  thresholds: {
    enabled: boolean; // Enable dynamic adjustment (default: true)
    adjustmentRate: number; // Rate of threshold adjustment (default: 0.05)
    minWeight: number; // Absolute minimum weight (default: 0.3)
    maxWeight: number; // Threshold for very strong recommendations (default: 0.85)
  };
}

/**
 * Default configuration optimized for balanced performance
 */
const DEFAULT_CONFIG: SuccessWeightingConfig = {
  weights: {
    baseSuccessRate: 0.4,
    recencyFactor: 0.3,
    complexityFactor: 0.1,
    projectFitFactor: 0.2,
  },
  recency: {
    halfLifeDays: 30,
    maxAgeDays: 180,
    floorWeight: 0.1,
  },
  complexity: {
    maxSteps: 10,
    penaltyFactor: 0.1,
  },
  confidence: {
    minSampleSize: 10,
    confidenceLevel: 0.95,
  },
  thresholds: {
    enabled: true,
    adjustmentRate: 0.05,
    minWeight: 0.3,
    maxWeight: 0.85,
  },
};

/**
 * Success Weighting System
 *
 * Philosophy:
 * - High success rate alone isn't enough - context matters
 * - Recent patterns are more relevant than old ones (exponential decay)
 * - Simpler patterns are preferred (Occam's Razor)
 * - Patterns that fit the current project context should be weighted higher
 * - Statistical confidence is essential for reliable recommendations
 */
export class SuccessWeightingSystem {
  private config: SuccessWeightingConfig;
  private performanceHistory: Map<string, PerformanceHistory>;
  private dynamicThresholds: DynamicThresholds;

  constructor(config: Partial<SuccessWeightingConfig> = {}) {
    this.config = this.mergeConfig(config);
    this.performanceHistory = new Map();
    this.dynamicThresholds = {
      minWeight: this.config.thresholds.minWeight,
      confidenceLevel: this.config.confidence.confidenceLevel,
      sampleSizeMultiplier: 1.0,
    };
  }

  /**
   * Calculate comprehensive weight for a pattern
   *
   * Multi-factor weighting algorithm:
   * 1. Base Success Rate (40%): Historical performance
   * 2. Recency Factor (30%): Exponential decay based on last use
   * 3. Complexity Factor (10%): Inverse complexity penalty
   * 4. Project Fit (20%): Context similarity scoring
   */
  calculatePatternWeight(
    pattern: Pattern,
    currentContext?: Context,
    projectMetadata?: Record<string, unknown>
  ): WeightResult {
    // 1. Base Success Rate (40%)
    const baseSuccessRate = this.calculateBaseSuccessRate(pattern);

    // 2. Recency Factor (30%)
    const recencyFactor = this.calculateRecencyFactor(pattern.evolution.lastUsed);

    // 3. Complexity Factor (10%)
    const complexityFactor = this.calculateComplexityFactor(pattern);

    // 4. Project Fit Factor (20%)
    const projectFitFactor = this.calculateProjectFit(
      pattern,
      currentContext,
      projectMetadata
    );

    // Calculate weighted total
    const totalWeight =
      baseSuccessRate * this.config.weights.baseSuccessRate +
      recencyFactor * this.config.weights.recencyFactor +
      complexityFactor * this.config.weights.complexityFactor +
      projectFitFactor * this.config.weights.projectFitFactor;

    // Calculate confidence and confidence interval
    const confidence = this.calculateConfidence(pattern.metrics.executionCount);
    const confidenceInterval = this.calculateConfidenceInterval(
      totalWeight,
      pattern.metrics.executionCount,
      pattern.metrics.successRate
    );

    // Determine recommendation strength
    const recommendationStrength = this.determineRecommendationStrength(
      totalWeight,
      confidence
    );

    // Update performance history
    this.updatePerformanceHistory(pattern.id, totalWeight, pattern.metrics.successRate);

    return {
      totalWeight,
      factors: {
        baseSuccessRate,
        recencyFactor,
        complexityFactor,
        projectFitFactor,
      },
      confidence,
      confidenceInterval,
      recommendationStrength,
    };
  }

  /**
   * Calculate weight for a solution (error resolution)
   */
  calculateSolutionWeight(
    solution: Solution,
    currentContext?: Context
  ): WeightResult {
    // Convert solution to pattern-like structure for weight calculation
    const pseudoPattern: Partial<Pattern> = {
      id: solution.id,
      metrics: {
        successRate: solution.effectiveness.worked ? 1.0 : 0.0,
        executionCount: solution.effectiveness.preventedRecurrence + 1,
        avgTimeSavedMs: solution.effectiveness.timeToFixMinutes * 60 * 1000,
        errorPreventionCount: solution.effectiveness.preventedRecurrence,
      },
      evolution: {
        created: solution.timestamp,
        lastUsed: solution.timestamp,
        refinements: 0,
        confidenceScore: solution.effectiveness.worked ? 0.9 : 0.3,
      },
      pattern: {
        type: solution.problem.errorType,
        context: solution.problem.context,
        approach: {
          technique: solution.solution.fixApproach,
          rationale: solution.solution.rootCause,
        },
        conditions: {
          whenApplicable: [solution.problem.errorMessage],
          whenNotApplicable: [],
        },
      },
    };

    return this.calculatePatternWeight(pseudoPattern as Pattern, currentContext);
  }

  /**
   * Calculate weight for a decision (architectural choice)
   */
  calculateDecisionWeight(decision: Decision): WeightResult {
    // Convert decision to pattern-like structure
    const avgSuccessMetric =
      (decision.outcome.successMetrics.developmentSpeed +
        decision.outcome.successMetrics.apiPerformance +
        decision.outcome.successMetrics.clientSatisfaction) /
      3;

    const pseudoPattern: Partial<Pattern> = {
      id: decision.id,
      metrics: {
        successRate: avgSuccessMetric,
        executionCount: 1,
        avgTimeSavedMs: 0,
        errorPreventionCount: 0,
      },
      evolution: {
        created: decision.timestamp,
        lastUsed: decision.timestamp,
        refinements: 0,
        confidenceScore: decision.outcome.wouldRepeat ? 0.85 : 0.4,
      },
      pattern: {
        type: decision.decision.type,
        context: decision.decision.context,
        approach: {
          technique: decision.decision.chosenOption,
          rationale: decision.decision.decisionFactors.primary.join(', '),
        },
        conditions: {
          whenApplicable: decision.decision.decisionFactors.primary,
          whenNotApplicable: [],
        },
      },
    };

    return this.calculatePatternWeight(pseudoPattern as Pattern);
  }

  /**
   * Dynamically adjust thresholds based on performance history
   *
   * Algorithm:
   * - If patterns consistently perform well, lower threshold (encourage exploration)
   * - If patterns underperform, raise threshold (increase selectivity)
   * - Adjust based on recent trend (improving/declining)
   */
  adjustThresholds(patternId: string): DynamicThresholds {
    if (!this.config.thresholds.enabled) {
      return this.dynamicThresholds;
    }

    const history = this.performanceHistory.get(patternId);
    if (!history || history.totalUsages < this.config.confidence.minSampleSize) {
      return this.dynamicThresholds;
    }

    const successRate = history.successfulUsages / history.totalUsages;
    const adjustmentRate = this.config.thresholds.adjustmentRate;

    // Adjust minimum weight threshold
    if (history.recentTrend === 'improving') {
      // Lower threshold to encourage more usage
      this.dynamicThresholds.minWeight = Math.max(
        this.config.thresholds.minWeight,
        this.dynamicThresholds.minWeight * (1 - adjustmentRate)
      );
    } else if (history.recentTrend === 'declining') {
      // Raise threshold to be more selective
      this.dynamicThresholds.minWeight = Math.min(
        this.config.thresholds.maxWeight,
        this.dynamicThresholds.minWeight * (1 + adjustmentRate)
      );
    }

    // Adjust based on sample size (higher confidence with more samples)
    if (history.totalUsages > this.config.confidence.minSampleSize * 2) {
      this.dynamicThresholds.sampleSizeMultiplier = 1.1;
    }

    return this.dynamicThresholds;
  }

  /**
   * Calculate confidence interval using normal approximation
   *
   * Returns Wilson score interval for binomial proportion
   */
  calculateConfidenceInterval(
    weight: number,
    sampleSize: number,
    successRate: number
  ): { lower: number; upper: number } {
    if (sampleSize < 3) {
      // Too few samples for meaningful interval
      return { lower: 0, upper: 1 };
    }

    // Z-score for 95% confidence
    const z = 1.96;
    const n = sampleSize;
    const p = successRate;

    // Wilson score interval
    const denominator = 1 + (z * z) / n;
    const center = (p + (z * z) / (2 * n)) / denominator;
    const margin = (z * Math.sqrt((p * (1 - p)) / n + (z * z) / (4 * n * n))) / denominator;

    const lower = Math.max(0, center - margin);
    const upper = Math.min(1, center + margin);

    // Scale by weight
    return {
      lower: lower * weight,
      upper: upper * weight,
    };
  }

  /**
   * Get current dynamic thresholds
   */
  getThresholds(): DynamicThresholds {
    return { ...this.dynamicThresholds };
  }

  /**
   * Reset thresholds to defaults
   */
  resetThresholds(): void {
    this.dynamicThresholds = {
      minWeight: this.config.thresholds.minWeight,
      confidenceLevel: this.config.confidence.confidenceLevel,
      sampleSizeMultiplier: 1.0,
    };
  }

  /**
   * Get performance history for a pattern
   */
  getPerformanceHistory(patternId: string): PerformanceHistory | undefined {
    return this.performanceHistory.get(patternId);
  }

  /**
   * Clear performance history (for testing or reset)
   */
  clearHistory(): void {
    this.performanceHistory.clear();
  }

  // ============================================================================
  // Private Helper Methods
  // ============================================================================

  /**
   * Calculate base success rate with smoothing
   */
  private calculateBaseSuccessRate(pattern: Pattern): number {
    // Laplace smoothing to avoid overconfidence with small samples
    const alpha = 2; // Pseudocount
    const successes = pattern.metrics.successRate * pattern.metrics.executionCount;
    const total = pattern.metrics.executionCount;

    return (successes + alpha) / (total + 2 * alpha);
  }

  /**
   * Calculate recency factor with exponential decay
   *
   * Uses exponential decay: weight = e^(-t / τ)
   * where τ is the half-life parameter
   */
  private calculateRecencyFactor(lastUsed: string): number {
    const now = Date.now();
    const lastUsedTime = new Date(lastUsed).getTime();
    const ageMs = now - lastUsedTime;
    const ageDays = ageMs / (1000 * 60 * 60 * 24);

    // Exponential decay
    const tau = this.config.recency.halfLifeDays / Math.LN2;
    const decayFactor = Math.exp(-ageDays / tau);

    // Apply floor to prevent complete obsolescence
    const recencyFactor = Math.max(this.config.recency.floorWeight, decayFactor);

    // Hard cutoff at max age
    return ageDays > this.config.recency.maxAgeDays
      ? this.config.recency.floorWeight
      : recencyFactor;
  }

  /**
   * Calculate complexity factor (simpler = better)
   *
   * Uses logarithmic penalty for complex patterns
   */
  private calculateComplexityFactor(pattern: Pattern): number {
    // Estimate complexity from pattern structure
    const steps = pattern.pattern.approach.steps?.length || 1;
    const conditionsCount = pattern.pattern.conditions.whenApplicable.length;
    const contextSize = Object.keys(pattern.pattern.context).length;

    const totalComplexity = steps + conditionsCount * 0.5 + contextSize * 0.3;

    // Logarithmic penalty (diminishing returns)
    const normalizedComplexity = totalComplexity / this.config.complexity.maxSteps;
    const complexityPenalty = Math.log(1 + normalizedComplexity) / Math.log(2);

    // Invert so simpler patterns score higher
    return Math.max(0.1, 1 - complexityPenalty * this.config.complexity.penaltyFactor);
  }

  /**
   * Calculate project fit factor
   *
   * Measures how well the pattern fits the current project context
   */
  private calculateProjectFit(
    pattern: Pattern,
    currentContext?: Context,
    projectMetadata?: Record<string, unknown>
  ): number {
    if (!currentContext && !projectMetadata) {
      return 0.5; // Neutral if no context available
    }

    let fitScore = 0;
    let totalChecks = 0;

    // Check context match
    if (currentContext) {
      const patternContext = pattern.pattern.context;
      for (const key in patternContext) {
        totalChecks++;
        if (currentContext[key] === patternContext[key]) {
          fitScore++;
        } else if (currentContext[key] !== undefined) {
          // Partial credit for related but different values
          fitScore += 0.3;
        }
      }
    }

    // Check project metadata match
    if (projectMetadata) {
      const patternContext = pattern.pattern.context;
      for (const key in patternContext) {
        if (projectMetadata[key] !== undefined) {
          totalChecks++;
          if (projectMetadata[key] === patternContext[key]) {
            fitScore++;
          }
        }
      }
    }

    return totalChecks === 0 ? 0.5 : fitScore / totalChecks;
  }

  /**
   * Calculate confidence based on sample size
   *
   * Uses sigmoid function for smooth transition
   */
  private calculateConfidence(sampleSize: number): number {
    const minSamples = this.config.confidence.minSampleSize;

    // Sigmoid function: confidence = 1 / (1 + e^(-k(x - x0)))
    const k = 0.3; // Steepness
    const x0 = minSamples; // Inflection point

    return 1 / (1 + Math.exp(-k * (sampleSize - x0)));
  }

  /**
   * Determine recommendation strength based on weight and confidence
   */
  private determineRecommendationStrength(
    weight: number,
    confidence: number
  ): 'weak' | 'moderate' | 'strong' | 'very-strong' {
    const combinedScore = weight * confidence;

    if (combinedScore >= 0.8) return 'very-strong';
    if (combinedScore >= 0.6) return 'strong';
    if (combinedScore >= 0.4) return 'moderate';
    return 'weak';
  }

  /**
   * Update performance history for a pattern
   */
  private updatePerformanceHistory(
    patternId: string,
    weight: number,
    successRate: number
  ): void {
    const history = this.performanceHistory.get(patternId) || {
      totalUsages: 0,
      successfulUsages: 0,
      avgWeight: 0,
      stdDevWeight: 0,
      recentTrend: 'stable' as const,
    };

    // Update counts
    history.totalUsages++;
    history.successfulUsages += successRate >= 0.7 ? 1 : 0;

    // Update average weight (exponential moving average)
    const alpha = 0.2; // Smoothing factor
    history.avgWeight = alpha * weight + (1 - alpha) * history.avgWeight;

    // Update standard deviation (simplified)
    const deviation = Math.abs(weight - history.avgWeight);
    history.stdDevWeight = alpha * deviation + (1 - alpha) * history.stdDevWeight;

    // Determine trend (compare recent performance to average)
    if (weight > history.avgWeight + history.stdDevWeight) {
      history.recentTrend = 'improving';
    } else if (weight < history.avgWeight - history.stdDevWeight) {
      history.recentTrend = 'declining';
    } else {
      history.recentTrend = 'stable';
    }

    this.performanceHistory.set(patternId, history);
  }

  /**
   * Merge user config with defaults
   */
  private mergeConfig(userConfig: Partial<SuccessWeightingConfig>): SuccessWeightingConfig {
    return {
      weights: { ...DEFAULT_CONFIG.weights, ...userConfig.weights },
      recency: { ...DEFAULT_CONFIG.recency, ...userConfig.recency },
      complexity: { ...DEFAULT_CONFIG.complexity, ...userConfig.complexity },
      confidence: { ...DEFAULT_CONFIG.confidence, ...userConfig.confidence },
      thresholds: { ...DEFAULT_CONFIG.thresholds, ...userConfig.thresholds },
    };
  }
}
