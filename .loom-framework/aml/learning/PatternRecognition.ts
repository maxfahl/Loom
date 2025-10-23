/**
 * Pattern Recognition Engine - Extracts and identifies repeatable patterns from agent actions
 *
 * This module implements sophisticated pattern matching algorithms including:
 * - Sequence extraction from action histories
 * - Cosine similarity for pattern matching
 * - Edit distance (Levenshtein) for structural comparison
 * - Multi-factor scoring with statistical significance
 * - Pattern evolution tracking
 */

import { Pattern, PatternModel } from '../models/Pattern';
import { AgentName, Context } from '../types/common';

/**
 * Represents an agent action that can be analyzed for patterns
 */
export interface AgentAction {
  type: string;
  timestamp: string;
  context: Context;
  parameters: Record<string, unknown>;
  outcome: 'success' | 'failure' | 'partial';
  durationMs: number;
  metadata?: Record<string, unknown>;
}

/**
 * Sequence of actions that might form a pattern
 */
export interface ActionSequence {
  actions: AgentAction[];
  startTime: string;
  endTime: string;
  frequency: number;
  avgDuration: number;
}

/**
 * Pattern match result with similarity score
 */
export interface PatternMatch {
  pattern: Pattern;
  similarity: number;
  matchType: 'exact' | 'structural' | 'semantic';
  confidence: number;
}

/**
 * Pattern scoring factors
 */
interface PatternScore {
  frequencyScore: number; // How often this pattern appears
  successScore: number; // Success rate of the pattern
  recencyScore: number; // How recently it was used
  complexityScore: number; // Simpler patterns score higher
  contextFitScore: number; // How well it fits current context
  totalScore: number;
  significanceLevel: number; // Statistical significance (p-value)
}

/**
 * Configuration for pattern recognition
 */
export interface PatternRecognitionConfig {
  minSequenceLength: number; // Minimum actions in a sequence
  maxSequenceLength: number; // Maximum actions to consider
  minFrequency: number; // Minimum occurrences to be considered
  minSimilarity: number; // Minimum similarity threshold (0-1)
  significanceThreshold: number; // p-value threshold for statistical significance
  temporalWindow: number; // Time window in milliseconds to group actions
}

/**
 * Default configuration
 */
const DEFAULT_CONFIG: PatternRecognitionConfig = {
  minSequenceLength: 2,
  maxSequenceLength: 10,
  minFrequency: 3,
  minSimilarity: 0.7,
  significanceThreshold: 0.05,
  temporalWindow: 300000, // 5 minutes
};

/**
 * Pattern Recognition Engine
 *
 * Core algorithm philosophy:
 * 1. Extract sequences using sliding window + temporal grouping
 * 2. Normalize sequences to handle variations
 * 3. Use multiple similarity metrics (cosine, edit distance, semantic)
 * 4. Score using multi-factor weighted system
 * 5. Validate statistical significance before promotion
 */
export class PatternRecognitionEngine {
  private config: PatternRecognitionConfig;
  private sequenceCache: Map<string, ActionSequence[]>;

  constructor(config: Partial<PatternRecognitionConfig> = {}) {
    this.config = { ...DEFAULT_CONFIG, ...config };
    this.sequenceCache = new Map();
  }

  /**
   * Extract action sequences from agent history
   *
   * Uses sliding window algorithm with temporal grouping to identify
   * potentially meaningful action sequences.
   */
  extractSequences(actions: AgentAction[], agentName: AgentName): ActionSequence[] {
    // Check cache first
    const cacheKey = this.generateCacheKey(actions, agentName);
    if (this.sequenceCache.has(cacheKey)) {
      return this.sequenceCache.get(cacheKey)!;
    }

    const sequences: ActionSequence[] = [];
    const { minSequenceLength, maxSequenceLength, temporalWindow } = this.config;

    // Sort by timestamp
    const sortedActions = [...actions].sort(
      (a, b) => new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime()
    );

    // Sliding window extraction
    for (let windowSize = minSequenceLength; windowSize <= maxSequenceLength; windowSize++) {
      for (let i = 0; i <= sortedActions.length - windowSize; i++) {
        const window = sortedActions.slice(i, i + windowSize);

        // Check temporal coherence - actions should be within temporal window
        const startTime = new Date(window[0].timestamp).getTime();
        const endTime = new Date(window[window.length - 1].timestamp).getTime();

        if (endTime - startTime <= temporalWindow) {
          // Calculate average duration
          const totalDuration = window.reduce((sum, action) => sum + action.durationMs, 0);
          const avgDuration = totalDuration / window.length;

          sequences.push({
            actions: window,
            startTime: window[0].timestamp,
            endTime: window[window.length - 1].timestamp,
            frequency: 1, // Will be updated in findCommonSequences
            avgDuration,
          });
        }
      }
    }

    this.sequenceCache.set(cacheKey, sequences);
    return sequences;
  }

  /**
   * Find common subsequences across extracted sequences
   *
   * Uses normalized comparison to identify similar sequences even with
   * minor variations in parameters or context.
   */
  findCommonSubsequences(sequences: ActionSequence[]): ActionSequence[] {
    const sequenceMap = new Map<string, ActionSequence[]>();

    // Group similar sequences
    for (const seq of sequences) {
      const normalized = this.normalizeSequence(seq);
      const signature = this.generateSequenceSignature(normalized);

      if (!sequenceMap.has(signature)) {
        sequenceMap.set(signature, []);
      }
      sequenceMap.get(signature)!.push(seq);
    }

    // Filter by minimum frequency and aggregate
    const commonSequences: ActionSequence[] = [];

    for (const [signature, seqGroup] of sequenceMap.entries()) {
      if (seqGroup.length >= this.config.minFrequency) {
        // Create representative sequence with aggregated metrics
        const representative = seqGroup[0];
        const avgDuration =
          seqGroup.reduce((sum, s) => sum + s.avgDuration, 0) / seqGroup.length;

        commonSequences.push({
          ...representative,
          frequency: seqGroup.length,
          avgDuration,
        });
      }
    }

    return commonSequences.sort((a, b) => b.frequency - a.frequency);
  }

  /**
   * Score pattern effectiveness using multiple factors
   *
   * Multi-factor scoring system:
   * - Frequency (30%): How often the pattern appears
   * - Success Rate (30%): Percentage of successful executions
   * - Recency (20%): More recent patterns weighted higher
   * - Complexity (10%): Simpler patterns preferred
   * - Context Fit (10%): How well it matches current context
   */
  scorePattern(
    sequence: ActionSequence,
    existingPatterns: Pattern[],
    currentContext?: Context
  ): PatternScore {
    // Calculate frequency score (normalized by max frequency)
    const maxFrequency = Math.max(...existingPatterns.map((p) => p.metrics.executionCount), 10);
    const frequencyScore = Math.min(sequence.frequency / maxFrequency, 1.0);

    // Calculate success score from sequence outcomes
    const successfulActions = sequence.actions.filter((a) => a.outcome === 'success').length;
    const successScore = successfulActions / sequence.actions.length;

    // Calculate recency score (exponential decay over 30 days)
    const daysOld =
      (Date.now() - new Date(sequence.endTime).getTime()) / (1000 * 60 * 60 * 24);
    const recencyScore = Math.exp(-daysOld / 30);

    // Calculate complexity score (inverse of sequence length)
    const complexityScore = 1 / Math.log(sequence.actions.length + Math.E);

    // Calculate context fit score
    const contextFitScore = currentContext
      ? this.calculateContextFit(sequence, currentContext)
      : 0.5;

    // Weighted total score
    const totalScore =
      frequencyScore * 0.3 +
      successScore * 0.3 +
      recencyScore * 0.2 +
      complexityScore * 0.1 +
      contextFitScore * 0.1;

    // Calculate statistical significance (chi-square test approximation)
    const significanceLevel = this.calculateSignificance(sequence, existingPatterns);

    return {
      frequencyScore,
      successScore,
      recencyScore,
      complexityScore,
      contextFitScore,
      totalScore,
      significanceLevel,
    };
  }

  /**
   * Calculate cosine similarity between two sequences
   *
   * Treats action sequences as vectors in feature space and computes
   * the cosine of the angle between them.
   */
  calculateCosineSimilarity(seq1: ActionSequence, seq2: ActionSequence): number {
    const features1 = this.extractFeatureVector(seq1);
    const features2 = this.extractFeatureVector(seq2);

    // Ensure same dimensionality
    const allKeys = new Set([...Object.keys(features1), ...Object.keys(features2)]);
    const vec1: number[] = [];
    const vec2: number[] = [];

    for (const key of allKeys) {
      vec1.push(features1[key] || 0);
      vec2.push(features2[key] || 0);
    }

    // Compute dot product
    let dotProduct = 0;
    let norm1 = 0;
    let norm2 = 0;

    for (let i = 0; i < vec1.length; i++) {
      dotProduct += vec1[i] * vec2[i];
      norm1 += vec1[i] * vec1[i];
      norm2 += vec2[i] * vec2[i];
    }

    // Avoid division by zero
    if (norm1 === 0 || norm2 === 0) {
      return 0;
    }

    return dotProduct / (Math.sqrt(norm1) * Math.sqrt(norm2));
  }

  /**
   * Calculate edit distance (Levenshtein distance) between sequences
   *
   * Measures structural similarity by counting minimum edits needed
   * to transform one sequence into another.
   */
  calculateEditDistance(seq1: ActionSequence, seq2: ActionSequence): number {
    const actions1 = seq1.actions.map((a) => a.type);
    const actions2 = seq2.actions.map((a) => a.type);

    const m = actions1.length;
    const n = actions2.length;

    // Create DP table
    const dp: number[][] = Array(m + 1)
      .fill(null)
      .map(() => Array(n + 1).fill(0));

    // Initialize base cases
    for (let i = 0; i <= m; i++) dp[i][0] = i;
    for (let j = 0; j <= n; j++) dp[0][j] = j;

    // Fill DP table
    for (let i = 1; i <= m; i++) {
      for (let j = 1; j <= n; j++) {
        if (actions1[i - 1] === actions2[j - 1]) {
          dp[i][j] = dp[i - 1][j - 1];
        } else {
          dp[i][j] = 1 + Math.min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1]);
        }
      }
    }

    // Normalize to 0-1 range (1 = identical, 0 = completely different)
    const maxLen = Math.max(m, n);
    return maxLen === 0 ? 1 : 1 - dp[m][n] / maxLen;
  }

  /**
   * Find matching patterns for a given action sequence
   *
   * Uses ensemble approach combining multiple similarity metrics
   */
  findMatchingPatterns(
    sequence: ActionSequence,
    existingPatterns: Pattern[],
    minSimilarity: number = this.config.minSimilarity
  ): PatternMatch[] {
    const matches: PatternMatch[] = [];

    for (const pattern of existingPatterns) {
      // Convert pattern to pseudo-sequence for comparison
      const patternSequence = this.patternToSequence(pattern);

      // Calculate multiple similarity metrics
      const cosineSim = this.calculateCosineSimilarity(sequence, patternSequence);
      const editSim = this.calculateEditDistance(sequence, patternSequence);
      const semanticSim = this.calculateSemanticSimilarity(sequence, patternSequence);

      // Ensemble similarity (weighted average)
      const similarity = cosineSim * 0.4 + editSim * 0.3 + semanticSim * 0.3;

      if (similarity >= minSimilarity) {
        // Determine match type
        let matchType: 'exact' | 'structural' | 'semantic';
        if (editSim > 0.95) {
          matchType = 'exact';
        } else if (editSim > 0.7) {
          matchType = 'structural';
        } else {
          matchType = 'semantic';
        }

        matches.push({
          pattern,
          similarity,
          matchType,
          confidence: similarity * pattern.evolution.confidenceScore,
        });
      }
    }

    return matches.sort((a, b) => b.confidence - a.confidence);
  }

  /**
   * Validate pattern with statistical significance testing
   *
   * Uses chi-square test to determine if pattern success rate is
   * significantly different from random chance.
   */
  validatePattern(
    sequence: ActionSequence,
    existingPatterns: Pattern[]
  ): { valid: boolean; pValue: number; reason?: string } {
    // Check minimum frequency
    if (sequence.frequency < this.config.minFrequency) {
      return {
        valid: false,
        pValue: 1.0,
        reason: `Insufficient frequency: ${sequence.frequency} < ${this.config.minFrequency}`,
      };
    }

    // Calculate success rate
    const successCount = sequence.actions.filter((a) => a.outcome === 'success').length;
    const successRate = successCount / sequence.actions.length;

    // Pattern must have positive success rate
    if (successRate <= 0.5) {
      return {
        valid: false,
        pValue: 1.0,
        reason: `Low success rate: ${successRate.toFixed(2)}`,
      };
    }

    // Calculate statistical significance
    const pValue = this.calculateSignificance(sequence, existingPatterns);

    if (pValue > this.config.significanceThreshold) {
      return {
        valid: false,
        pValue,
        reason: `Not statistically significant: p=${pValue.toFixed(4)} > ${this.config.significanceThreshold}`,
      };
    }

    return { valid: true, pValue };
  }

  /**
   * Track pattern evolution over time
   */
  trackEvolution(pattern: Pattern, newUsage: { success: boolean; timestamp: string }): void {
    const model = new PatternModel(pattern);
    model.recordUsage(newUsage.success);

    // Update evolution metrics
    pattern.evolution.lastUsed = newUsage.timestamp;
    pattern.evolution.refinements++;

    // Adjust confidence based on recent performance
    const recentSuccessRate = pattern.metrics.successRate;
    if (recentSuccessRate > 0.8) {
      pattern.evolution.confidenceScore = Math.min(pattern.evolution.confidenceScore * 1.05, 1.0);
    } else if (recentSuccessRate < 0.5) {
      pattern.evolution.confidenceScore = Math.max(pattern.evolution.confidenceScore * 0.95, 0.1);
    }
  }

  // ============================================================================
  // Private Helper Methods
  // ============================================================================

  /**
   * Normalize sequence to handle minor variations
   */
  private normalizeSequence(sequence: ActionSequence): ActionSequence {
    return {
      ...sequence,
      actions: sequence.actions.map((action) => ({
        ...action,
        // Normalize timestamps to relative offsets
        timestamp: '0',
        // Keep only essential parameters (remove noise)
        parameters: this.normalizeParameters(action.parameters),
      })),
    };
  }

  /**
   * Generate unique signature for sequence
   */
  private generateSequenceSignature(sequence: ActionSequence): string {
    const actionTypes = sequence.actions.map((a) => a.type).join('->');
    const contextKeys = sequence.actions
      .flatMap((a) => Object.keys(a.context))
      .filter((key, idx, arr) => arr.indexOf(key) === idx)
      .sort()
      .join(',');

    return `${actionTypes}|${contextKeys}`;
  }

  /**
   * Generate cache key for sequence extraction
   */
  private generateCacheKey(actions: AgentAction[], agentName: AgentName): string {
    const actionHash = actions
      .map((a) => `${a.type}:${a.timestamp}`)
      .join('|')
      .split('')
      .reduce((hash, char) => {
        const chr = char.charCodeAt(0);
        hash = (hash << 5) - hash + chr;
        return hash | 0;
      }, 0);

    return `${agentName}:${actionHash}`;
  }

  /**
   * Extract feature vector from sequence for similarity comparison
   */
  private extractFeatureVector(sequence: ActionSequence): Record<string, number> {
    const features: Record<string, number> = {};

    // Action type frequencies
    for (const action of sequence.actions) {
      const key = `type:${action.type}`;
      features[key] = (features[key] || 0) + 1;
    }

    // Outcome distribution
    for (const action of sequence.actions) {
      const key = `outcome:${action.outcome}`;
      features[key] = (features[key] || 0) + 1;
    }

    // Context features
    for (const action of sequence.actions) {
      for (const [key, value] of Object.entries(action.context)) {
        const featureKey = `context:${key}:${value}`;
        features[featureKey] = (features[featureKey] || 0) + 1;
      }
    }

    // Duration bucket
    const avgDuration = sequence.avgDuration;
    const durationBucket =
      avgDuration < 100 ? 'fast' : avgDuration < 1000 ? 'medium' : 'slow';
    features[`duration:${durationBucket}`] = 1;

    // Normalize by sequence length
    for (const key in features) {
      features[key] /= sequence.actions.length;
    }

    return features;
  }

  /**
   * Calculate semantic similarity based on action types and outcomes
   */
  private calculateSemanticSimilarity(seq1: ActionSequence, seq2: ActionSequence): number {
    const types1 = new Set(seq1.actions.map((a) => a.type));
    const types2 = new Set(seq2.actions.map((a) => a.type));

    // Jaccard similarity for action types
    const intersection = new Set([...types1].filter((x) => types2.has(x)));
    const union = new Set([...types1, ...types2]);

    const jaccardSim = union.size === 0 ? 0 : intersection.size / union.size;

    // Outcome similarity
    const outcomes1 = seq1.actions.map((a) => a.outcome);
    const outcomes2 = seq2.actions.map((a) => a.outcome);
    const outcomeSim =
      outcomes1.filter((o, i) => o === outcomes2[i]).length / Math.max(outcomes1.length, 1);

    return jaccardSim * 0.6 + outcomeSim * 0.4;
  }

  /**
   * Calculate context fit score
   */
  private calculateContextFit(sequence: ActionSequence, targetContext: Context): number {
    let totalFit = 0;
    let contextChecks = 0;

    for (const action of sequence.actions) {
      for (const [key, value] of Object.entries(action.context)) {
        contextChecks++;
        if (targetContext[key] === value) {
          totalFit++;
        }
      }
    }

    return contextChecks === 0 ? 0.5 : totalFit / contextChecks;
  }

  /**
   * Calculate statistical significance using chi-square approximation
   */
  private calculateSignificance(
    sequence: ActionSequence,
    existingPatterns: Pattern[]
  ): number {
    const successCount = sequence.actions.filter((a) => a.outcome === 'success').length;
    const totalCount = sequence.actions.length;
    const successRate = successCount / totalCount;

    // Calculate expected success rate from existing patterns
    const avgSuccessRate =
      existingPatterns.length > 0
        ? existingPatterns.reduce((sum, p) => sum + p.metrics.successRate, 0) /
          existingPatterns.length
        : 0.5;

    const expectedSuccess = totalCount * avgSuccessRate;
    const expectedFailure = totalCount * (1 - avgSuccessRate);

    // Chi-square statistic
    const chiSquare =
      Math.pow(successCount - expectedSuccess, 2) / expectedSuccess +
      Math.pow(totalCount - successCount - expectedFailure, 2) / expectedFailure;

    // Approximate p-value (1 degree of freedom)
    // Using simplified approximation: p ≈ exp(-chiSquare/2)
    const pValue = Math.exp(-chiSquare / 2);

    return pValue;
  }

  /**
   * Normalize parameters to reduce noise
   */
  private normalizeParameters(params: Record<string, unknown>): Record<string, unknown> {
    const normalized: Record<string, unknown> = {};

    for (const [key, value] of Object.entries(params)) {
      // Keep only primitive types and ignore IDs/timestamps
      if (
        typeof value === 'string' ||
        typeof value === 'number' ||
        typeof value === 'boolean'
      ) {
        if (!key.toLowerCase().includes('id') && !key.toLowerCase().includes('timestamp')) {
          normalized[key] = value;
        }
      }
    }

    return normalized;
  }

  /**
   * Convert pattern to pseudo-sequence for comparison
   */
  private patternToSequence(pattern: Pattern): ActionSequence {
    // Create a representative sequence from pattern definition
    const action: AgentAction = {
      type: pattern.pattern.type,
      timestamp: pattern.timestamp,
      context: pattern.pattern.context,
      parameters: {},
      outcome: pattern.metrics.successRate > 0.5 ? 'success' : 'failure',
      durationMs: pattern.metrics.avgTimeSavedMs,
    };

    return {
      actions: [action],
      startTime: pattern.timestamp,
      endTime: pattern.evolution.lastUsed,
      frequency: pattern.metrics.executionCount,
      avgDuration: pattern.metrics.avgTimeSavedMs,
    };
  }

  /**
   * Clear sequence cache (for memory management)
   */
  clearCache(): void {
    this.sequenceCache.clear();
  }
}
