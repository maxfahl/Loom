/**
 * Pruning Service - Memory cleanup and optimization
 *
 * Implements intelligent pruning strategies to keep memory size under control.
 * Removes low-value patterns, outdated solutions, and stale decisions.
 */

import { Pattern, PatternModel } from './models/Pattern';
import { Solution, SolutionModel } from './models/Solution';
import { Decision, DecisionModel } from './models/Decision';
import { AgentName, Timestamp } from './types/common';
import { PruningConfig } from './config/schema';

export interface PruneResult {
  agent: AgentName;
  patternsRemoved: number;
  solutionsRemoved: number;
  decisionsRemoved: number;
  bytesFreed: number;
  duration: number;
}

export interface PruneStrategy {
  timeBased?: {
    maxAgeDays: number;
    minUsageRate: number; // uses per day
  };
  performanceBased?: {
    minConfidence: number;
    minSuccessRate: number;
  };
  spaceBased?: {
    maxPatterns: number;
    maxSolutions: number;
    maxDecisions: number;
  };
}

/**
 * Pruning Service class
 */
export class PruningService {
  private schedule: NodeJS.Timeout | null;
  private config: PruningConfig;

  constructor(config: PruningConfig) {
    this.config = config;
    this.schedule = null;
  }

  /**
   * Prune agent memory
   */
  prune(
    agent: AgentName,
    patterns: Pattern[],
    solutions: Solution[],
    decisions: Decision[],
    strategy?: PruneStrategy
  ): {
    patterns: Pattern[];
    solutions: Solution[];
    decisions: Decision[];
    result: PruneResult;
  } {
    const startTime = Date.now();
    const initialCounts = {
      patterns: patterns.length,
      solutions: solutions.length,
      decisions: decisions.length,
    };

    // Use provided strategy or build from config
    const pruneStrategy = strategy || this.buildStrategyFromConfig();

    // Prune patterns
    const prunedPatterns = this.prunePatterns(patterns, pruneStrategy);

    // Prune solutions
    const prunedSolutions = this.pruneSolutions(solutions, pruneStrategy);

    // Prune decisions
    const prunedDecisions = this.pruneDecisions(decisions, pruneStrategy);

    // Calculate bytes freed (rough estimate: 1KB per item average)
    const bytesFreed =
      (initialCounts.patterns - prunedPatterns.length +
        (initialCounts.solutions - prunedSolutions.length) +
        (initialCounts.decisions - prunedDecisions.length)) *
      1024;

    const result: PruneResult = {
      agent,
      patternsRemoved: initialCounts.patterns - prunedPatterns.length,
      solutionsRemoved: initialCounts.solutions - prunedSolutions.length,
      decisionsRemoved: initialCounts.decisions - prunedDecisions.length,
      bytesFreed,
      duration: Date.now() - startTime,
    };

    return {
      patterns: prunedPatterns,
      solutions: prunedSolutions,
      decisions: prunedDecisions,
      result,
    };
  }

  /**
   * Prune patterns
   */
  private prunePatterns(patterns: Pattern[], strategy: PruneStrategy): Pattern[] {
    let filtered = patterns;

    // Time-based pruning
    if (strategy.timeBased) {
      filtered = this.prunePatternsByTime(filtered, strategy.timeBased);
    }

    // Performance-based pruning
    if (strategy.performanceBased) {
      filtered = this.prunePatternsByPerformance(filtered, strategy.performanceBased);
    }

    // Space-based pruning
    if (strategy.spaceBased && filtered.length > strategy.spaceBased.maxPatterns) {
      filtered = this.prunePatternsBySpace(filtered, strategy.spaceBased.maxPatterns);
    }

    return filtered;
  }

  /**
   * Prune patterns by time criteria
   */
  private prunePatternsByTime(
    patterns: Pattern[],
    criteria: { maxAgeDays: number; minUsageRate: number }
  ): Pattern[] {
    const now = Date.now();
    const maxAgeMs = criteria.maxAgeDays * 24 * 60 * 60 * 1000;

    return patterns.filter((pattern) => {
      const age = now - new Date(pattern.evolution.lastUsed).getTime();
      if (age > maxAgeMs) {
        // Check usage rate
        const ageDays = age / (24 * 60 * 60 * 1000);
        const usageRate = pattern.metrics.executionCount / ageDays;
        return usageRate >= criteria.minUsageRate;
      }
      return true; // Keep if not too old
    });
  }

  /**
   * Prune patterns by performance criteria
   */
  private prunePatternsByPerformance(
    patterns: Pattern[],
    criteria: { minConfidence: number; minSuccessRate: number }
  ): Pattern[] {
    return patterns.filter((pattern) => {
      const model = new PatternModel(pattern);
      return (
        model.confidenceScore >= criteria.minConfidence &&
        model.successRate >= criteria.minSuccessRate
      );
    });
  }

  /**
   * Prune patterns by space constraint (keep top N by weight)
   */
  private prunePatternsBySpace(patterns: Pattern[], maxCount: number): Pattern[] {
    // Sort by weight (combination of confidence, recency, usage)
    const sorted = patterns
      .map((p) => ({
        pattern: p,
        weight: new PatternModel(p).calculateWeight(),
      }))
      .sort((a, b) => b.weight - a.weight);

    return sorted.slice(0, maxCount).map((item) => item.pattern);
  }

  /**
   * Prune solutions
   */
  private pruneSolutions(solutions: Solution[], strategy: PruneStrategy): Solution[] {
    let filtered = solutions;

    // Time-based pruning
    if (strategy.timeBased) {
      filtered = this.pruneSolutionsByTime(filtered, strategy.timeBased.maxAgeDays);
    }

    // Performance-based pruning (remove solutions that didn't work)
    if (strategy.performanceBased) {
      filtered = this.pruneSolutionsByPerformance(filtered, strategy.performanceBased.minConfidence);
    }

    // Space-based pruning
    if (strategy.spaceBased && filtered.length > strategy.spaceBased.maxSolutions) {
      filtered = this.pruneSolutionsBySpace(filtered, strategy.spaceBased.maxSolutions);
    }

    return filtered;
  }

  /**
   * Prune solutions by time
   */
  private pruneSolutionsByTime(solutions: Solution[], maxAgeDays: number): Solution[] {
    const now = Date.now();
    const maxAgeMs = maxAgeDays * 24 * 60 * 60 * 1000;

    return solutions.filter((solution) => {
      const age = now - new Date(solution.timestamp).getTime();
      return age <= maxAgeMs || solution.effectiveness.worked; // Keep if recent or worked
    });
  }

  /**
   * Prune solutions by performance
   */
  private pruneSolutionsByPerformance(solutions: Solution[], minConfidence: number): Solution[] {
    return solutions.filter((solution) => {
      const model = new SolutionModel(solution);
      return model.calculateConfidence() >= minConfidence;
    });
  }

  /**
   * Prune solutions by space (keep top N by weight)
   */
  private pruneSolutionsBySpace(solutions: Solution[], maxCount: number): Solution[] {
    const sorted = solutions
      .map((s) => ({
        solution: s,
        weight: new SolutionModel(s).calculateWeight(),
      }))
      .sort((a, b) => b.weight - a.weight);

    return sorted.slice(0, maxCount).map((item) => item.solution);
  }

  /**
   * Prune decisions
   */
  private pruneDecisions(decisions: Decision[], strategy: PruneStrategy): Decision[] {
    let filtered = decisions;

    // Time-based pruning
    if (strategy.timeBased) {
      filtered = this.pruneDecisionsByTime(filtered, strategy.timeBased.maxAgeDays);
    }

    // Performance-based pruning (keep successful decisions)
    if (strategy.performanceBased) {
      filtered = this.pruneDecisionsByPerformance(filtered);
    }

    // Space-based pruning
    if (strategy.spaceBased && filtered.length > strategy.spaceBased.maxDecisions) {
      filtered = this.pruneDecisionsBySpace(filtered, strategy.spaceBased.maxDecisions);
    }

    return filtered;
  }

  /**
   * Prune decisions by time
   */
  private pruneDecisionsByTime(decisions: Decision[], maxAgeDays: number): Decision[] {
    const now = Date.now();
    const maxAgeMs = maxAgeDays * 24 * 60 * 60 * 1000;

    return decisions.filter((decision) => {
      const age = now - new Date(decision.timestamp).getTime();
      const hasOutcome = decision.outcome !== undefined;
      return age <= maxAgeMs || (hasOutcome && decision.outcome.wouldRepeat); // Keep recent or successful
    });
  }

  /**
   * Prune decisions by performance (keep those that would be repeated)
   */
  private pruneDecisionsByPerformance(decisions: Decision[]): Decision[] {
    return decisions.filter((decision) => {
      const model = new DecisionModel(decision);
      return !model.hasOutcome || model.wouldRepeat;
    });
  }

  /**
   * Prune decisions by space (keep top N by weight)
   */
  private pruneDecisionsBySpace(decisions: Decision[], maxCount: number): Decision[] {
    const sorted = decisions
      .map((d) => ({
        decision: d,
        weight: new DecisionModel(d).calculateWeight(),
      }))
      .sort((a, b) => b.weight - a.weight);

    return sorted.slice(0, maxCount).map((item) => item.decision);
  }

  /**
   * Build strategy from config
   */
  private buildStrategyFromConfig(): PruneStrategy {
    return {
      timeBased: {
        maxAgeDays: this.config.maxAgeDays,
        minUsageRate: this.config.minUsageRate,
      },
      performanceBased: {
        minConfidence: this.config.minConfidence,
        minSuccessRate: 0.5, // Default 50% success rate
      },
    };
  }

  /**
   * Start scheduled pruning
   */
  startScheduledPruning(callback: () => Promise<void>): void {
    if (this.schedule) return;

    let intervalMs: number;
    switch (this.config.schedule) {
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

    this.schedule = setInterval(async () => {
      if (this.config.enabled) {
        await callback();
      }
    }, intervalMs);
  }

  /**
   * Stop scheduled pruning
   */
  stopScheduledPruning(): void {
    if (this.schedule) {
      clearInterval(this.schedule);
      this.schedule = null;
    }
  }

  /**
   * Update pruning configuration
   */
  updateConfig(config: Partial<PruningConfig>): void {
    this.config = { ...this.config, ...config };
  }
}
