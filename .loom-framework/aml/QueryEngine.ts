/**
 * Query Engine - Advanced pattern matching and indexing system
 *
 * Provides fast, indexed queries for patterns, solutions, and decisions.
 * Implements similarity matching, ranking algorithms, and search optimization.
 */

import { Pattern, PatternModel } from './models/Pattern';
import { Solution } from './models/Solution';
import { Decision, DecisionModel } from './models/Decision';
import { Context, AgentName } from './types/common';

export interface SearchIndex {
  byType: Map<string, string[]>; // type -> pattern IDs
  byTag: Map<string, string[]>; // tag -> pattern IDs
  byContext: Map<string, string[]>; // context key-value -> pattern IDs
  byConfidence: Map<number, string[]>; // confidence bucket -> pattern IDs
}

export interface SimilarityScore {
  id: string;
  score: number;
  matches: string[];
}

export interface RankingWeights {
  confidence: number;
  recency: number;
  usage: number;
  similarity: number;
}

/**
 * Query Engine class
 */
export class QueryEngine {
  private patternIndex: Map<AgentName, SearchIndex>;
  private solutionIndex: Map<AgentName, Map<string, string[]>>; // errorType -> solution IDs
  private decisionIndex: Map<AgentName, Map<string, string[]>>; // decisionType -> decision IDs

  constructor() {
    this.patternIndex = new Map();
    this.solutionIndex = new Map();
    this.decisionIndex = new Map();
  }

  // ============================================================================
  // INDEX MANAGEMENT
  // ============================================================================

  /**
   * Build index for patterns
   */
  buildPatternIndex(agent: AgentName, patterns: Pattern[]): void {
    const index: SearchIndex = {
      byType: new Map(),
      byTag: new Map(),
      byContext: new Map(),
      byConfidence: new Map(),
    };

    for (const pattern of patterns) {
      const id = pattern.id;
      const type = pattern.pattern.type;

      // Index by type
      if (!index.byType.has(type)) {
        index.byType.set(type, []);
      }
      index.byType.get(type)!.push(id);

      // Index by tags
      if (pattern.tags) {
        for (const tag of pattern.tags) {
          if (!index.byTag.has(tag)) {
            index.byTag.set(tag, []);
          }
          index.byTag.get(tag)!.push(id);
        }
      }

      // Index by context
      for (const [key, value] of Object.entries(pattern.pattern.context)) {
        const contextKey = `${key}:${value}`;
        if (!index.byContext.has(contextKey)) {
          index.byContext.set(contextKey, []);
        }
        index.byContext.get(contextKey)!.push(id);
      }

      // Index by confidence bucket (0.0-0.1, 0.1-0.2, etc.)
      const confidenceBucket = Math.floor(pattern.evolution.confidenceScore * 10) / 10;
      if (!index.byConfidence.has(confidenceBucket)) {
        index.byConfidence.set(confidenceBucket, []);
      }
      index.byConfidence.get(confidenceBucket)!.push(id);
    }

    this.patternIndex.set(agent, index);
  }

  /**
   * Build index for solutions
   */
  buildSolutionIndex(agent: AgentName, solutions: Solution[]): void {
    const index = new Map<string, string[]>();

    for (const solution of solutions) {
      const errorType = solution.problem.errorType;
      if (!index.has(errorType)) {
        index.set(errorType, []);
      }
      index.get(errorType)!.push(solution.id);
    }

    this.solutionIndex.set(agent, index);
  }

  /**
   * Build index for decisions
   */
  buildDecisionIndex(agent: AgentName, decisions: Decision[]): void {
    const index = new Map<string, string[]>();

    for (const decision of decisions) {
      const type = decision.decision.type;
      if (!index.has(type)) {
        index.set(type, []);
      }
      index.get(type)!.push(decision.id);
    }

    this.decisionIndex.set(agent, index);
  }

  // ============================================================================
  // PATTERN SEARCH
  // ============================================================================

  /**
   * Search patterns by type (using index)
   */
  searchPatternsByType(agent: AgentName, type: string): string[] {
    const index = this.patternIndex.get(agent);
    if (!index) return [];

    return index.byType.get(type) || [];
  }

  /**
   * Search patterns by tags (using index)
   */
  searchPatternsByTag(agent: AgentName, tag: string): string[] {
    const index = this.patternIndex.get(agent);
    if (!index) return [];

    return index.byTag.get(tag) || [];
  }

  /**
   * Search patterns by context (using index)
   */
  searchPatternsByContext(agent: AgentName, context: Context): string[] {
    const index = this.patternIndex.get(agent);
    if (!index) return [];

    // Find patterns that match ANY context key-value pair
    const matchingSets: Set<string>[] = [];

    for (const [key, value] of Object.entries(context)) {
      const contextKey = `${key}:${value}`;
      const ids = index.byContext.get(contextKey);
      if (ids) {
        matchingSets.push(new Set(ids));
      }
    }

    if (matchingSets.length === 0) return [];

    // Find intersection (patterns that match ALL context pairs)
    const intersection = matchingSets.reduce((acc, set) => {
      return new Set([...acc].filter((x) => set.has(x)));
    });

    return Array.from(intersection);
  }

  /**
   * Search patterns by minimum confidence (using index)
   */
  searchPatternsByConfidence(agent: AgentName, minConfidence: number): string[] {
    const index = this.patternIndex.get(agent);
    if (!index) return [];

    const results: string[] = [];
    const minBucket = Math.floor(minConfidence * 10) / 10;

    for (const [bucket, ids] of index.byConfidence.entries()) {
      if (bucket >= minBucket) {
        results.push(...ids);
      }
    }

    return results;
  }

  /**
   * Calculate similarity between two patterns
   */
  calculatePatternSimilarity(pattern1: Pattern, pattern2: Pattern): number {
    let score = 0;
    let maxScore = 0;

    // Type similarity (40%)
    maxScore += 0.4;
    if (pattern1.pattern.type === pattern2.pattern.type) {
      score += 0.4;
    }

    // Context similarity (30%)
    maxScore += 0.3;
    const context1 = pattern1.pattern.context;
    const context2 = pattern2.pattern.context;
    const allKeys = new Set([...Object.keys(context1), ...Object.keys(context2)]);
    const matchingKeys = Array.from(allKeys).filter((key) => context1[key] === context2[key]);
    const contextSimilarity = matchingKeys.length / allKeys.size;
    score += contextSimilarity * 0.3;

    // Approach similarity (20%)
    maxScore += 0.2;
    if (pattern1.pattern.approach.technique === pattern2.pattern.approach.technique) {
      score += 0.2;
    }

    // Tag similarity (10%)
    maxScore += 0.1;
    if (pattern1.tags && pattern2.tags) {
      const tags1 = new Set(pattern1.tags);
      const tags2 = new Set(pattern2.tags);
      const commonTags = Array.from(tags1).filter((tag) => tags2.has(tag));
      const tagSimilarity = commonTags.length / Math.max(tags1.size, tags2.size);
      score += tagSimilarity * 0.1;
    }

    return score / maxScore;
  }

  /**
   * Find similar patterns
   */
  findSimilarPatterns(
    _agent: AgentName,
    targetPattern: Pattern,
    allPatterns: Pattern[],
    minSimilarity: number = 0.5,
    limit: number = 10
  ): SimilarityScore[] {
    const scores: SimilarityScore[] = [];

    for (const pattern of allPatterns) {
      if (pattern.id === targetPattern.id) continue; // Skip self

      const similarity = this.calculatePatternSimilarity(targetPattern, pattern);
      if (similarity >= minSimilarity) {
        scores.push({
          id: pattern.id,
          score: similarity,
          matches: this.getMatchingAttributes(targetPattern, pattern),
        });
      }
    }

    // Sort by similarity score (descending)
    scores.sort((a, b) => b.score - a.score);

    return scores.slice(0, limit);
  }

  /**
   * Get matching attributes between two patterns
   */
  private getMatchingAttributes(pattern1: Pattern, pattern2: Pattern): string[] {
    const matches: string[] = [];

    if (pattern1.pattern.type === pattern2.pattern.type) {
      matches.push('type');
    }

    if (pattern1.pattern.approach.technique === pattern2.pattern.approach.technique) {
      matches.push('technique');
    }

    const context1 = pattern1.pattern.context;
    const context2 = pattern2.pattern.context;
    for (const key of Object.keys(context1)) {
      if (context1[key] === context2[key]) {
        matches.push(`context.${key}`);
      }
    }

    if (pattern1.tags && pattern2.tags) {
      const commonTags = pattern1.tags.filter((tag) => pattern2.tags!.includes(tag));
      if (commonTags.length > 0) {
        matches.push('tags');
      }
    }

    return matches;
  }

  // ============================================================================
  // RANKING ALGORITHMS
  // ============================================================================

  /**
   * Rank patterns using weighted scoring
   */
  rankPatterns(
    patterns: Pattern[],
    weights: RankingWeights = {
      confidence: 0.4,
      recency: 0.3,
      usage: 0.2,
      similarity: 0.1,
    },
    targetContext?: Context
  ): Pattern[] {
    const scored = patterns.map((pattern) => {
      const _model = new PatternModel(pattern);
      let score = 0;

      // Confidence score
      score += _model.confidenceScore * weights.confidence;

      // Recency score (exponential decay over 30 days)
      const daysOld =
        (Date.now() - new Date(pattern.evolution.lastUsed).getTime()) / (1000 * 60 * 60 * 24);
      const recencyScore = Math.exp(-daysOld / 30);
      score += recencyScore * weights.recency;

      // Usage score (normalized by max 100 uses)
      const usageScore = Math.min(pattern.metrics.executionCount / 100, 1.0);
      score += usageScore * weights.usage;

      // Similarity score (if target context provided)
      if (targetContext && weights.similarity > 0) {
        const contextMatch = _model.matchesContext(targetContext) ? 1.0 : 0.0;
        score += contextMatch * weights.similarity;
      }

      return { pattern, score };
    });

    // Sort by score (descending)
    scored.sort((a, b) => b.score - a.score);

    return scored.map((item) => item.pattern);
  }

  /**
   * Rank solutions using weighted scoring
   */
  rankSolutions(solutions: Solution[]): Solution[] {
    const scored = solutions.map((solution) => {
      let score = 0;

      // Base score from whether it worked
      score += solution.effectiveness.worked ? 0.5 : 0.1;

      // Verification count bonus
      score += Math.min(solution.verifiedCount * 0.05, 0.2);

      // Recurrence prevention bonus
      score += Math.min(solution.effectiveness.preventedRecurrence * 0.03, 0.15);

      // Recency score
      const daysOld = (Date.now() - new Date(solution.timestamp).getTime()) / (1000 * 60 * 60 * 24);
      const recencyScore = Math.exp(-daysOld / 60);
      score += recencyScore * 0.15;

      return { solution, score };
    });

    // Sort by score (descending)
    scored.sort((a, b) => b.score - a.score);

    return scored.map((item) => item.solution);
  }

  /**
   * Rank decisions using weighted scoring
   */
  rankDecisions(decisions: Decision[]): Decision[] {
    const scored = decisions.map((decision) => {
      const _model = new DecisionModel(decision);
      let score = _model.calculateWeight();

      return { decision, score };
    });

    // Sort by score (descending)
    scored.sort((a, b) => b.score - a.score);

    return scored.map((item) => item.decision);
  }

  // ============================================================================
  // FUZZY SEARCH
  // ============================================================================

  /**
   * Calculate Levenshtein distance between two strings
   */
  private levenshteinDistance(str1: string, str2: string): number {
    const m = str1.length;
    const n = str2.length;
    const dp: number[][] = Array(m + 1)
      .fill(null)
      .map(() => Array(n + 1).fill(0));

    for (let i = 0; i <= m; i++) dp[i][0] = i;
    for (let j = 0; j <= n; j++) dp[0][j] = j;

    for (let i = 1; i <= m; i++) {
      for (let j = 1; j <= n; j++) {
        if (str1[i - 1] === str2[j - 1]) {
          dp[i][j] = dp[i - 1][j - 1];
        } else {
          dp[i][j] = Math.min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1]) + 1;
        }
      }
    }

    return dp[m][n];
  }

  /**
   * Calculate string similarity (0-1)
   */
  calculateStringSimilarity(str1: string, str2: string): number {
    const maxLen = Math.max(str1.length, str2.length);
    if (maxLen === 0) return 1.0;

    const distance = this.levenshteinDistance(str1.toLowerCase(), str2.toLowerCase());
    return 1 - distance / maxLen;
  }

  /**
   * Fuzzy search patterns by description/rationale
   */
  fuzzySearchPatterns(
    patterns: Pattern[],
    query: string,
    minSimilarity: number = 0.5
  ): Pattern[] {
    const queryLower = query.toLowerCase();
    const results: { pattern: Pattern; score: number }[] = [];

    for (const pattern of patterns) {
      const rationale = pattern.pattern.approach.rationale.toLowerCase();
      const type = pattern.pattern.type.toLowerCase();

      // Check for exact substring match first
      if (rationale.includes(queryLower) || type.includes(queryLower)) {
        results.push({ pattern, score: 1.0 });
        continue;
      }

      // Calculate fuzzy match score
      const rationaleScore = this.calculateStringSimilarity(query, rationale);
      const typeScore = this.calculateStringSimilarity(query, type);
      const maxScore = Math.max(rationaleScore, typeScore);

      if (maxScore >= minSimilarity) {
        results.push({ pattern, score: maxScore });
      }
    }

    // Sort by similarity score
    results.sort((a, b) => b.score - a.score);

    return results.map((r) => r.pattern);
  }

  /**
   * Fuzzy search solutions by error message
   */
  fuzzySearchSolutions(
    solutions: Solution[],
    errorMessage: string,
    minSimilarity: number = 0.5
  ): Solution[] {
    const results: { solution: Solution; score: number }[] = [];

    for (const solution of solutions) {
      const solMessage = solution.problem.errorMessage;

      // Check for exact substring match first
      if (
        solMessage.toLowerCase().includes(errorMessage.toLowerCase()) ||
        errorMessage.toLowerCase().includes(solMessage.toLowerCase())
      ) {
        results.push({ solution, score: 1.0 });
        continue;
      }

      // Calculate fuzzy match score
      const score = this.calculateStringSimilarity(errorMessage, solMessage);

      if (score >= minSimilarity) {
        results.push({ solution, score });
      }
    }

    // Sort by similarity score
    results.sort((a, b) => b.score - a.score);

    return results.map((r) => r.solution);
  }

  // ============================================================================
  // ANALYTICS
  // ============================================================================

  /**
   * Get pattern statistics
   */
  getPatternStats(patterns: Pattern[]): {
    total: number;
    active: number;
    avgConfidence: number;
    avgSuccessRate: number;
    avgExecutionCount: number;
    topTypes: Array<{ type: string; count: number }>;
  } {
    const active = patterns.filter((p) => p.active !== false);
    const avgConfidence =
      patterns.reduce((sum, p) => sum + p.evolution.confidenceScore, 0) / patterns.length || 0;
    const avgSuccessRate =
      patterns.reduce((sum, p) => sum + p.metrics.successRate, 0) / patterns.length || 0;
    const avgExecutionCount =
      patterns.reduce((sum, p) => sum + p.metrics.executionCount, 0) / patterns.length || 0;

    // Count by type
    const typeCounts = new Map<string, number>();
    for (const pattern of patterns) {
      const type = pattern.pattern.type;
      typeCounts.set(type, (typeCounts.get(type) || 0) + 1);
    }

    const topTypes = Array.from(typeCounts.entries())
      .map(([type, count]) => ({ type, count }))
      .sort((a, b) => b.count - a.count)
      .slice(0, 10);

    return {
      total: patterns.length,
      active: active.length,
      avgConfidence,
      avgSuccessRate,
      avgExecutionCount,
      topTypes,
    };
  }

  /**
   * Clear all indices
   */
  clearIndices(): void {
    this.patternIndex.clear();
    this.solutionIndex.clear();
    this.decisionIndex.clear();
  }

  /**
   * Clear indices for specific agent
   */
  clearAgentIndices(agent: AgentName): void {
    this.patternIndex.delete(agent);
    this.solutionIndex.delete(agent);
    this.decisionIndex.delete(agent);
  }
}
