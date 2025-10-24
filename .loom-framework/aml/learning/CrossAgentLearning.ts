/**
 * Cross-Agent Learning Module - Enables knowledge sharing and pattern adaptation across agents
 *
 * This module implements:
 * - Agent compatibility checking based on capabilities and domains
 * - Pattern adaptation to fit target agent context
 * - Knowledge sharing protocol with conflict resolution
 * - Consensus mechanisms for competing patterns
 * - Cross-pollination tracking and analytics
 */

import { Pattern } from '../models/Pattern';
import { AgentName, Context } from '../types/common';

/**
 * Agent capability profile for compatibility checking
 */
export interface AgentProfile {
  name: AgentName;
  capabilities: string[]; // e.g., ['react', 'typescript', 'testing']
  domains: string[]; // e.g., ['frontend', 'backend', 'mobile']
  focusAreas: string[]; // e.g., ['performance', 'accessibility', 'security']
  complexity: 'simple' | 'moderate' | 'advanced';
  learningRate: number; // 0-1, how quickly agent adapts
}

/**
 * Compatibility assessment result
 */
export interface CompatibilityResult {
  compatible: boolean;
  score: number; // 0-1
  reasons: string[];
  adaptationRequired: 'none' | 'minor' | 'major' | 'extensive';
  recommendedAdjustments?: string[];
}

/**
 * Adapted pattern with metadata
 */
export interface AdaptedPattern {
  originalPattern: Pattern;
  adaptedPattern: Pattern;
  sourceAgent: AgentName;
  targetAgent: AgentName;
  adaptations: string[];
  confidenceAdjustment: number; // How much confidence was reduced due to adaptation
  timestamp: string;
}

/**
 * Knowledge sharing record
 */
export interface SharingRecord {
  id: string;
  sourceAgent: AgentName;
  targetAgent: AgentName;
  patternId: string;
  timestamp: string;
  adaptationLevel: 'none' | 'minor' | 'major' | 'extensive';
  successRate: number;
  usageCount: number;
  lastUsed: string;
}

/**
 * Pattern conflict when multiple agents suggest different approaches
 */
export interface PatternConflict {
  id: string;
  patterns: Pattern[];
  context: Context;
  conflictType: 'approach' | 'implementation' | 'architecture' | 'tooling';
  severity: 'low' | 'medium' | 'high';
  timestamp: string;
}

/**
 * Consensus result for conflict resolution
 */
export interface ConsensusResult {
  selectedPattern: Pattern;
  confidence: number;
  votingBreakdown: Map<string, number>; // patternId -> score
  rationale: string;
  minorityOpinions?: string[];
}

/**
 * Configuration for cross-agent learning
 */
export interface CrossAgentLearningConfig {
  compatibility: {
    minScore: number; // Minimum compatibility score (default: 0.6)
    requireOverlappingDomains: boolean; // Require shared domains (default: true)
    capabilityWeightPercent: number; // Weight of capability matching (default: 40)
    domainWeightPercent: number; // Weight of domain matching (default: 40)
    focusAreaWeightPercent: number; // Weight of focus area matching (default: 20)
  };

  adaptation: {
    maxConfidencePenalty: number; // Max confidence reduction (default: 0.3)
    preserveCore: boolean; // Always preserve core approach (default: true)
    allowArchitecturalChanges: boolean; // Allow changing architecture (default: false)
  };

  sharing: {
    autoShare: boolean; // Automatically share high-success patterns (default: true)
    shareThreshold: number; // Success rate threshold for auto-sharing (default: 0.85)
    maxCrossPollinationDepth: number; // Max sharing chain depth (default: 3)
    trackProvenance: boolean; // Track pattern origin (default: true)
  };

  consensus: {
    votingMethod: 'weighted' | 'democratic' | 'experience-based'; // Default: weighted
    quorumPercent: number; // Minimum participation (default: 50)
    tiebreaker: 'recency' | 'confidence' | 'usage-count'; // Default: confidence
  };
}

/**
 * Default configuration
 */
const DEFAULT_CONFIG: CrossAgentLearningConfig = {
  compatibility: {
    minScore: 0.6,
    requireOverlappingDomains: true,
    capabilityWeightPercent: 40,
    domainWeightPercent: 40,
    focusAreaWeightPercent: 20,
  },
  adaptation: {
    maxConfidencePenalty: 0.3,
    preserveCore: true,
    allowArchitecturalChanges: false,
  },
  sharing: {
    autoShare: true,
    shareThreshold: 0.85,
    maxCrossPollinationDepth: 3,
    trackProvenance: true,
  },
  consensus: {
    votingMethod: 'weighted',
    quorumPercent: 50,
    tiebreaker: 'confidence',
  },
};

/**
 * Cross-Agent Learning System
 *
 * Philosophy:
 * - Agents can learn from each other, but must adapt patterns to their context
 * - Not all patterns are transferable - compatibility matters
 * - Cross-pollination should enhance, not replace, agent specialization
 * - Conflicts are learning opportunities, not failures
 * - Consensus should be evidence-based, not popularity-based
 */
export class CrossAgentLearning {
  private config: CrossAgentLearningConfig;
  private agentProfiles: Map<AgentName, AgentProfile>;
  private sharingHistory: Map<string, SharingRecord>;
  private conflictResolutions: Map<string, ConsensusResult>;
  private crossPollinationGraph: Map<AgentName, Set<AgentName>>; // Tracks sharing relationships

  constructor(config: Partial<CrossAgentLearningConfig> = {}) {
    this.config = this.mergeConfig(config);
    this.agentProfiles = new Map();
    this.sharingHistory = new Map();
    this.conflictResolutions = new Map();
    this.crossPollinationGraph = new Map();
  }

  /**
   * Register an agent profile for compatibility checking
   */
  registerAgent(profile: AgentProfile): void {
    this.agentProfiles.set(profile.name, profile);
    if (!this.crossPollinationGraph.has(profile.name)) {
      this.crossPollinationGraph.set(profile.name, new Set());
    }
  }

  /**
   * Check compatibility between two agents
   *
   * Multi-factor compatibility scoring:
   * - Capability overlap (40%): Shared technical skills
   * - Domain overlap (40%): Shared problem domains
   * - Focus area alignment (20%): Shared priorities
   */
  checkCompatibility(
    sourceAgent: AgentName,
    targetAgent: AgentName
  ): CompatibilityResult {
    const sourceProfile = this.agentProfiles.get(sourceAgent);
    const targetProfile = this.agentProfiles.get(targetAgent);

    if (!sourceProfile || !targetProfile) {
      return {
        compatible: false,
        score: 0,
        reasons: ['Agent profile not found'],
        adaptationRequired: 'extensive',
      };
    }

    // Calculate capability overlap
    const capabilityScore = this.calculateOverlapScore(
      sourceProfile.capabilities,
      targetProfile.capabilities
    );

    // Calculate domain overlap
    const domainScore = this.calculateOverlapScore(
      sourceProfile.domains,
      targetProfile.domains
    );

    // Calculate focus area alignment
    const focusAreaScore = this.calculateOverlapScore(
      sourceProfile.focusAreas,
      targetProfile.focusAreas
    );

    // Weighted total score
    const totalScore =
      (capabilityScore * this.config.compatibility.capabilityWeightPercent +
        domainScore * this.config.compatibility.domainWeightPercent +
        focusAreaScore * this.config.compatibility.focusAreaWeightPercent) /
      100;

    // Determine adaptation requirements
    let adaptationRequired: 'none' | 'minor' | 'major' | 'extensive';
    if (totalScore >= 0.9) adaptationRequired = 'none';
    else if (totalScore >= 0.7) adaptationRequired = 'minor';
    else if (totalScore >= 0.5) adaptationRequired = 'major';
    else adaptationRequired = 'extensive';

    // Generate reasons
    const reasons: string[] = [];
    if (capabilityScore > 0.7) reasons.push('Strong capability overlap');
    else if (capabilityScore < 0.3) reasons.push('Limited capability overlap');

    if (domainScore > 0.7) reasons.push('Shared problem domain');
    else if (domainScore < 0.3) reasons.push('Different problem domains');

    if (focusAreaScore > 0.5) reasons.push('Aligned priorities');

    // Check domain requirement
    const compatible =
      totalScore >= this.config.compatibility.minScore &&
      (!this.config.compatibility.requireOverlappingDomains || domainScore > 0);

    // Generate adaptation recommendations
    const recommendedAdjustments: string[] = [];
    if (capabilityScore < 0.5) {
      recommendedAdjustments.push('Adjust technical terminology');
      recommendedAdjustments.push('Provide additional context for capabilities');
    }
    if (domainScore < 0.5) {
      recommendedAdjustments.push('Translate domain-specific concepts');
      recommendedAdjustments.push('Add explanatory notes for domain differences');
    }

    return {
      compatible,
      score: totalScore,
      reasons,
      adaptationRequired,
      recommendedAdjustments: recommendedAdjustments.length > 0 ? recommendedAdjustments : undefined,
    };
  }

  /**
   * Adapt a pattern from source agent to target agent context
   *
   * Adaptation strategy:
   * 1. Preserve core approach and rationale
   * 2. Adjust terminology to match target agent's vocabulary
   * 3. Add/remove steps based on target agent's complexity level
   * 4. Update context to match target agent's domain
   * 5. Reduce confidence proportionally to adaptation level
   */
  adaptPattern(
    pattern: Pattern,
    sourceAgent: AgentName,
    targetAgent: AgentName
  ): AdaptedPattern | null {
    // Check compatibility first
    const compatibility = this.checkCompatibility(sourceAgent, targetAgent);

    if (!compatibility.compatible) {
      return null;
    }

    const targetProfile = this.agentProfiles.get(targetAgent);
    if (!targetProfile) {
      return null;
    }

    // Create adapted copy
    const adapted: Pattern = JSON.parse(JSON.stringify(pattern));
    const adaptations: string[] = [];

    // Adjust pattern type based on target agent's terminology
    const originalType = adapted.pattern.type;
    adapted.pattern.type = this.adaptTerminology(originalType, sourceAgent, targetAgent);
    if (adapted.pattern.type !== originalType) {
      adaptations.push(`Terminology: "${originalType}" -> "${adapted.pattern.type}"`);
    }

    // Adjust complexity based on target agent's level
    if (targetProfile.complexity === 'simple' && adapted.pattern.approach.steps) {
      const originalSteps = adapted.pattern.approach.steps.length;
      adapted.pattern.approach.steps = this.simplifySteps(adapted.pattern.approach.steps);
      if (adapted.pattern.approach.steps.length !== originalSteps) {
        adaptations.push(`Simplified from ${originalSteps} to ${adapted.pattern.approach.steps.length} steps`);
      }
    } else if (targetProfile.complexity === 'advanced' && !adapted.pattern.approach.steps) {
      // Add more detailed steps for advanced agents
      adapted.pattern.approach.steps = this.expandSteps(adapted.pattern.approach.technique);
      adaptations.push('Added detailed implementation steps');
    }

    // Update context to match target domain
    const originalContext = { ...adapted.pattern.context };
    adapted.pattern.context = this.adaptContext(
      adapted.pattern.context,
      targetProfile.domains
    );
    if (JSON.stringify(originalContext) !== JSON.stringify(adapted.pattern.context)) {
      adaptations.push('Updated context for target domain');
    }

    // Adjust conditions based on target focus areas
    this.adjustConditions(adapted, targetProfile.focusAreas);
    adaptations.push('Adjusted applicability conditions');

    // Calculate confidence penalty based on adaptation level
    const confidencePenalty = this.calculateConfidencePenalty(
      compatibility.adaptationRequired,
      adaptations.length
    );

    // Reduce confidence score
    adapted.evolution.confidenceScore = Math.max(
      0.3,
      adapted.evolution.confidenceScore * (1 - confidencePenalty)
    );

    // Update metadata
    adapted.agent = targetAgent;
    adapted.timestamp = new Date().toISOString();
    adapted.evolution.refinements = 0; // Reset for new agent
    adapted.metrics.executionCount = 0; // Will build up usage in target context

    // Add provenance tag if tracking enabled
    if (this.config.sharing.trackProvenance) {
      adapted.tags = [
        ...(adapted.tags || []),
        `adapted-from:${sourceAgent}`,
        `original-id:${pattern.id}`,
      ];
    }

    return {
      originalPattern: pattern,
      adaptedPattern: adapted,
      sourceAgent,
      targetAgent,
      adaptations,
      confidenceAdjustment: confidencePenalty,
      timestamp: new Date().toISOString(),
    };
  }

  /**
   * Share a successful pattern with compatible agents
   *
   * Returns list of agents that received the pattern
   */
  sharePattern(
    sourceAgent: AgentName,
    pattern: Pattern,
    candidateAgents?: AgentName[]
  ): AdaptedPattern[] {
    // Auto-share check
    if (
      this.config.sharing.autoShare &&
      pattern.metrics.successRate < this.config.sharing.shareThreshold
    ) {
      return []; // Pattern not successful enough for auto-sharing
    }

    // Check cross-pollination depth
    const depth = this.getCrossPollinationDepth(sourceAgent, pattern.id);
    if (depth >= this.config.sharing.maxCrossPollinationDepth) {
      return []; // Prevent infinite sharing chains
    }

    // Determine target agents
    const targets = candidateAgents || Array.from(this.agentProfiles.keys());
    const adaptedPatterns: AdaptedPattern[] = [];

    for (const targetAgent of targets) {
      // Skip self
      if (targetAgent === sourceAgent) continue;

      // Check compatibility
      const compatibility = this.checkCompatibility(sourceAgent, targetAgent);
      if (!compatibility.compatible) continue;

      // Adapt pattern
      const adapted = this.adaptPattern(pattern, sourceAgent, targetAgent);
      if (!adapted) continue;

      // Record sharing
      const record: SharingRecord = {
        id: crypto.randomUUID(),
        sourceAgent,
        targetAgent,
        patternId: pattern.id,
        timestamp: new Date().toISOString(),
        adaptationLevel: compatibility.adaptationRequired,
        successRate: 0, // Will be updated as target agent uses it
        usageCount: 0,
        lastUsed: new Date().toISOString(),
      };

      this.sharingHistory.set(record.id, record);

      // Update cross-pollination graph
      const sourceConnections = this.crossPollinationGraph.get(sourceAgent)!;
      sourceConnections.add(targetAgent);

      adaptedPatterns.push(adapted);
    }

    return adaptedPatterns;
  }

  /**
   * Resolve conflicts when multiple agents suggest different patterns
   *
   * Uses weighted voting based on:
   * - Pattern success rate (40%)
   * - Agent expertise in domain (30%)
   * - Pattern confidence (20%)
   * - Pattern usage count (10%)
   */
  resolveConflict(conflict: PatternConflict): ConsensusResult {
    const { patterns, context } = conflict;

    // Voting breakdown
    const votes = new Map<string, number>();

    for (const pattern of patterns) {
      const agentProfile = this.agentProfiles.get(pattern.agent);

      // Calculate vote weight based on multiple factors
      let voteWeight = 0;

      // Success rate (40%)
      voteWeight += pattern.metrics.successRate * 0.4;

      // Confidence (20%)
      voteWeight += pattern.evolution.confidenceScore * 0.2;

      // Usage count (10%) - normalized
      const maxUsage = Math.max(...patterns.map((p) => p.metrics.executionCount));
      const usageScore = maxUsage > 0 ? pattern.metrics.executionCount / maxUsage : 0;
      voteWeight += usageScore * 0.1;

      // Agent expertise in domain (30%)
      if (agentProfile) {
        const domainExpertise = this.calculateDomainExpertise(agentProfile, context);
        voteWeight += domainExpertise * 0.3;
      }

      votes.set(pattern.id, voteWeight);
    }

    // Find winner
    let selectedPattern = patterns[0];
    let maxVote = votes.get(patterns[0].id)!;

    for (const pattern of patterns) {
      const vote = votes.get(pattern.id)!;
      if (vote > maxVote) {
        maxVote = vote;
        selectedPattern = pattern;
      }
    }

    // Check for ties
    const tiedPatterns = patterns.filter((p) => votes.get(p.id) === maxVote);
    if (tiedPatterns.length > 1) {
      // Apply tiebreaker
      selectedPattern = this.applyTiebreaker(tiedPatterns);
    }

    // Calculate confidence based on vote margin
    const totalVotes = Array.from(votes.values()).reduce((a, b) => a + b, 0);
    const winMargin = maxVote / totalVotes;
    const confidence = Math.min(winMargin * 1.2, 1.0); // Boost for clear winners

    // Collect minority opinions
    const minorityOpinions = patterns
      .filter((p) => p.id !== selectedPattern.id)
      .map(
        (p) =>
          `${p.agent} suggested ${p.pattern.type} (success rate: ${p.metrics.successRate.toFixed(2)})`
      );

    // Generate rationale
    const rationale = this.generateConflictRationale(selectedPattern, votes, patterns);

    // Record resolution
    const result: ConsensusResult = {
      selectedPattern,
      confidence,
      votingBreakdown: votes,
      rationale,
      minorityOpinions: minorityOpinions.length > 0 ? minorityOpinions : undefined,
    };

    this.conflictResolutions.set(conflict.id, result);

    return result;
  }

  /**
   * Build consensus mechanism for pattern recommendation
   *
   * Used when multiple agents have patterns that could apply
   */
  buildConsensus(
    patterns: Pattern[],
    context: Context,
    minQuorum: number = this.config.consensus.quorumPercent
  ): ConsensusResult | null {
    if (patterns.length === 0) {
      return null;
    }

    // Check quorum
    const totalAgents = this.agentProfiles.size;
    const participatingAgents = new Set(patterns.map((p) => p.agent)).size;
    const quorumMet = (participatingAgents / totalAgents) * 100 >= minQuorum;

    if (!quorumMet && patterns.length > 1) {
      return null; // Need more participation
    }

    // Create pseudo-conflict and resolve
    const conflict: PatternConflict = {
      id: crypto.randomUUID(),
      patterns,
      context,
      conflictType: 'approach',
      severity: 'medium',
      timestamp: new Date().toISOString(),
    };

    return this.resolveConflict(conflict);
  }

  /**
   * Get cross-pollination analytics
   */
  getCrossPollinationStats(): {
    totalShares: number;
    mostGenerousAgent: AgentName | null;
    mostReceptiveAgent: AgentName | null;
    avgAdaptationLevel: string;
    successRate: number;
  } {
    const shares = Array.from(this.sharingHistory.values());

    if (shares.length === 0) {
      return {
        totalShares: 0,
        mostGenerousAgent: null,
        mostReceptiveAgent: null,
        avgAdaptationLevel: 'none',
        successRate: 0,
      };
    }

    // Count shares per agent
    const sourceCount = new Map<AgentName, number>();
    const targetCount = new Map<AgentName, number>();

    for (const share of shares) {
      sourceCount.set(share.sourceAgent, (sourceCount.get(share.sourceAgent) || 0) + 1);
      targetCount.set(share.targetAgent, (targetCount.get(share.targetAgent) || 0) + 1);
    }

    const mostGenerousAgent =
      Array.from(sourceCount.entries()).sort((a, b) => b[1] - a[1])[0]?.[0] || null;

    const mostReceptiveAgent =
      Array.from(targetCount.entries()).sort((a, b) => b[1] - a[1])[0]?.[0] || null;

    // Calculate average adaptation level
    const adaptationLevels = shares.map((s) => s.adaptationLevel);
    const avgAdaptation =
      adaptationLevels.reduce((sum, level) => {
        const weights = { none: 0, minor: 1, major: 2, extensive: 3 };
        return sum + weights[level];
      }, 0) / shares.length;

    const avgAdaptationLevel =
      avgAdaptation < 0.5
        ? 'none'
        : avgAdaptation < 1.5
          ? 'minor'
          : avgAdaptation < 2.5
            ? 'major'
            : 'extensive';

    // Calculate success rate
    const successRate =
      shares.reduce((sum, s) => sum + s.successRate, 0) / shares.length;

    return {
      totalShares: shares.length,
      mostGenerousAgent,
      mostReceptiveAgent,
      avgAdaptationLevel,
      successRate,
    };
  }

  // ============================================================================
  // Private Helper Methods
  // ============================================================================

  /**
   * Calculate overlap score between two arrays (Jaccard similarity)
   */
  private calculateOverlapScore(set1: string[], set2: string[]): number {
    const s1 = new Set(set1.map((s) => s.toLowerCase()));
    const s2 = new Set(set2.map((s) => s.toLowerCase()));

    const intersection = new Set([...s1].filter((x) => s2.has(x)));
    const union = new Set([...s1, ...s2]);

    return union.size === 0 ? 0 : intersection.size / union.size;
  }

  /**
   * Adapt terminology from source to target agent
   */
  private adaptTerminology(
    term: string,
    _sourceAgent: AgentName,
    targetAgent: AgentName
  ): string {
    // Terminology mapping (could be extended with a full dictionary)
    const mappings: Record<string, Record<string, string>> = {
      'component-optimization': {
        'frontend-developer': 'react-component-optimization',
        'mobile-developer': 'mobile-component-optimization',
        'backend-architect': 'service-optimization',
      },
      'data-fetching': {
        'frontend-developer': 'api-client-pattern',
        'backend-architect': 'data-access-layer',
        'mobile-developer': 'network-request-pattern',
      },
    };

    const mapping = mappings[term.toLowerCase()];
    return mapping?.[targetAgent] || term;
  }

  /**
   * Simplify steps for less complex agents
   */
  private simplifySteps(steps: string[]): string[] {
    // Combine related steps, remove overly detailed ones
    const simplified: string[] = [];
    let currentGroup = '';

    for (const step of steps) {
      if (step.length < 50) {
        // Short steps stay as-is
        if (currentGroup) {
          simplified.push(currentGroup);
          currentGroup = '';
        }
        simplified.push(step);
      } else {
        // Long steps get combined
        currentGroup = currentGroup
          ? `${currentGroup}; ${step.substring(0, 30)}...`
          : step.substring(0, 50);
      }
    }

    if (currentGroup) {
      simplified.push(currentGroup);
    }

    return simplified.slice(0, 5); // Max 5 steps for simple agents
  }

  /**
   * Expand technique into detailed steps
   */
  private expandSteps(technique: string): string[] {
    // Generic expansion (could be made more sophisticated)
    return [
      `Analyze requirements for ${technique}`,
      `Prepare implementation environment`,
      `Implement ${technique}`,
      `Validate implementation`,
      `Test and optimize`,
      'Document approach',
    ];
  }

  /**
   * Adapt context to match target domains
   */
  private adaptContext(
    context: Record<string, string | number | boolean>,
    targetDomains: string[]
  ): Record<string, string | number | boolean> {
    const adapted = { ...context };

    // Add domain-specific context if missing
    if (targetDomains.includes('frontend') && !adapted.framework) {
      adapted.framework = 'React';
    }
    if (targetDomains.includes('backend') && !adapted.server) {
      adapted.server = 'Node.js';
    }
    if (targetDomains.includes('mobile') && !adapted.platform) {
      adapted.platform = 'cross-platform';
    }

    return adapted;
  }

  /**
   * Adjust conditions based on focus areas
   */
  private adjustConditions(pattern: Pattern, focusAreas: string[]): void {
    const conditions = pattern.pattern.conditions;

    // Add focus-area-specific conditions
    for (const area of focusAreas) {
      if (area === 'performance' && !conditions.whenApplicable.includes('performance-critical')) {
        conditions.whenApplicable.push('performance-critical');
      }
      if (area === 'security' && !conditions.whenApplicable.includes('security-sensitive')) {
        conditions.whenApplicable.push('security-sensitive');
      }
      if (area === 'accessibility' && !conditions.whenApplicable.includes('user-facing')) {
        conditions.whenApplicable.push('user-facing');
      }
    }
  }

  /**
   * Calculate confidence penalty based on adaptation
   */
  private calculateConfidencePenalty(
    adaptationLevel: 'none' | 'minor' | 'major' | 'extensive',
    adaptationCount: number
  ): number {
    const basePenalty = {
      none: 0,
      minor: 0.1,
      major: 0.2,
      extensive: 0.3,
    }[adaptationLevel];

    // Additional penalty for high number of adaptations
    const countPenalty = Math.min(adaptationCount * 0.02, 0.1);

    return Math.min(basePenalty + countPenalty, this.config.adaptation.maxConfidencePenalty);
  }

  /**
   * Calculate domain expertise of agent for given context
   */
  private calculateDomainExpertise(profile: AgentProfile, context: Context): number {
    let expertiseScore = 0;
    let checks = 0;

    // Check if agent's domains match context
    for (const [key, value] of Object.entries(context)) {
      checks++;
      const contextStr = `${key}:${value}`.toLowerCase();

      for (const domain of profile.domains) {
        if (contextStr.includes(domain.toLowerCase())) {
          expertiseScore++;
          break;
        }
      }

      for (const capability of profile.capabilities) {
        if (contextStr.includes(capability.toLowerCase())) {
          expertiseScore += 0.5;
          break;
        }
      }
    }

    return checks === 0 ? 0.5 : expertiseScore / checks;
  }

  /**
   * Apply tiebreaker when votes are equal
   */
  private applyTiebreaker(patterns: Pattern[]): Pattern {
    switch (this.config.consensus.tiebreaker) {
      case 'recency':
        return patterns.sort(
          (a, b) =>
            new Date(b.evolution.lastUsed).getTime() - new Date(a.evolution.lastUsed).getTime()
        )[0];

      case 'confidence':
        return patterns.sort(
          (a, b) => b.evolution.confidenceScore - a.evolution.confidenceScore
        )[0];

      case 'usage-count':
        return patterns.sort((a, b) => b.metrics.executionCount - a.metrics.executionCount)[0];

      default:
        return patterns[0];
    }
  }

  /**
   * Generate human-readable rationale for conflict resolution
   */
  private generateConflictRationale(
    winner: Pattern,
    votes: Map<string, number>,
    _allPatterns: Pattern[]
  ): string {
    const winnerVote = votes.get(winner.id)!;
    const totalVotes = Array.from(votes.values()).reduce((a, b) => a + b, 0);
    const winPercentage = ((winnerVote / totalVotes) * 100).toFixed(1);

    return `Selected ${winner.agent}'s approach "${winner.pattern.type}" with ${winPercentage}% of weighted votes. ` +
      `Success rate: ${(winner.metrics.successRate * 100).toFixed(1)}%, ` +
      `Confidence: ${(winner.evolution.confidenceScore * 100).toFixed(1)}%, ` +
      `Used ${winner.metrics.executionCount} times.`;
  }

  /**
   * Get cross-pollination depth for a pattern
   */
  private getCrossPollinationDepth(_sourceAgent: AgentName, patternId: string): number {
    // Check sharing history for chain depth
    const shares = Array.from(this.sharingHistory.values()).filter(
      (s) => s.patternId === patternId
    );

    let maxDepth = 0;
    for (const share of shares) {
      // Recursively check if this was shared further
      const depth = this.getDepthRecursive(share.targetAgent, patternId, 0);
      maxDepth = Math.max(maxDepth, depth);
    }

    return maxDepth;
  }

  /**
   * Recursive helper for depth calculation
   */
  private getDepthRecursive(agent: AgentName, patternId: string, currentDepth: number): number {
    const furtherShares = Array.from(this.sharingHistory.values()).filter(
      (s) => s.sourceAgent === agent && s.patternId === patternId
    );

    if (furtherShares.length === 0) {
      return currentDepth;
    }

    let maxDepth = currentDepth;
    for (const share of furtherShares) {
      const depth = this.getDepthRecursive(share.targetAgent, patternId, currentDepth + 1);
      maxDepth = Math.max(maxDepth, depth);
    }

    return maxDepth;
  }

  /**
   * Merge user config with defaults
   */
  private mergeConfig(userConfig: Partial<CrossAgentLearningConfig>): CrossAgentLearningConfig {
    return {
      compatibility: { ...DEFAULT_CONFIG.compatibility, ...userConfig.compatibility },
      adaptation: { ...DEFAULT_CONFIG.adaptation, ...userConfig.adaptation },
      sharing: { ...DEFAULT_CONFIG.sharing, ...userConfig.sharing },
      consensus: { ...DEFAULT_CONFIG.consensus, ...userConfig.consensus },
    };
  }
}
