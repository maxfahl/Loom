/**
 * Memory Service - Core service for Agent Memory & Learning System
 *
 * This is the main interface for agents to interact with the AML system.
 * Provides CRUD operations, querying, and learning capabilities.
 */

import * as path from 'path';
import { MemoryStore, MemoryData } from './storage/MemoryStore';
import { PatternModel, Pattern } from './models/Pattern';
import { SolutionModel, Solution } from './models/Solution';
import { DecisionModel, Decision } from './models/Decision';
import { ConfigManager } from './config/ConfigManager';
import { AgentName, Context, OperationResult } from './types/common';
import { AMLConfig } from './config/schema';

export interface QueryPatternOptions {
  type?: string;
  context?: Context;
  minConfidence?: number;
  limit?: number;
  sortBy?: 'confidence' | 'weight' | 'recency' | 'successRate';
  includeInactive?: boolean;
}

export interface QuerySolutionOptions {
  errorType?: string;
  errorMessage?: string;
  context?: Context;
  minConfidence?: number;
  limit?: number;
  includeInactive?: boolean;
}

export interface QueryDecisionOptions {
  type?: string;
  context?: Context;
  includeWithoutOutcome?: boolean;
  limit?: number;
  includeInactive?: boolean;
}

export interface RecordPatternData {
  type: string;
  context: Record<string, string | number | boolean>;
  approach: {
    technique: string;
    codeTemplate?: string;
    rationale: string;
    steps?: string[];
  };
  conditions: {
    whenApplicable: string[];
    whenNotApplicable: string[];
  };
  tags?: string[];
}

export interface RecordSolutionData {
  errorType: string;
  errorMessage: string;
  stackTraceHash?: string;
  context: Record<string, string | number | boolean>;
  rootCause: string;
  fixApproach: string;
  codeFix?: string;
  prevention: string;
  worked: boolean;
  timeToFixMinutes: number;
  tags?: string[];
}

export interface RecordDecisionData {
  type: string;
  question: string;
  context: Record<string, string | number | boolean>;
  chosenOption: string;
  alternativesConsidered: string[];
  decisionFactors: {
    primary: string[];
    secondary: string[];
  };
  rationale?: string;
  tags?: string[];
}

export interface PatternUsageResult {
  patternId: string;
  success: boolean;
  timeSavedMs?: number;
  errorsPrevented?: number;
}

export interface MetricsReport {
  agent: AgentName;
  totalPatterns: number;
  activePatterns: number;
  totalSolutions: number;
  activeSolutions: number;
  totalDecisions: number;
  activeDecisions: number;
  avgConfidence: number;
  memoryUsageBytes: number;
  healthScore: number;
}

/**
 * Main Memory Service class
 */
export class MemoryService {
  private store: MemoryStore;
  private configManager: ConfigManager;
  private memoryCache: Map<AgentName, MemoryData>;
  private cacheTimestamps: Map<AgentName, number>;
  private cacheTTL: number;

  constructor(storagePath: string = '.loom/memory', config?: Partial<AMLConfig>) {
    this.store = new MemoryStore(storagePath, true);
    // ConfigManager expects a file path, not a directory
    this.configManager = new ConfigManager(path.join(storagePath, 'config.json'));
    this.memoryCache = new Map();
    this.cacheTimestamps = new Map();
    this.cacheTTL = 3600000; // 1 hour default

    if (config) {
      this.configManager.updateConfig(config);
    }
  }

  /**
   * Initialize the memory service
   */
  async initialize(): Promise<void> {
    await this.store.initialize();
    await this.configManager.load();
  }

  /**
   * Check if AML is enabled globally
   */
  isEnabled(): boolean {
    return this.configManager.getConfig().enabled;
  }

  /**
   * Check if AML is enabled for a specific agent
   * Only returns true if agent is explicitly configured in agentOverrides
   */
  isEnabledForAgent(agent: AgentName): boolean {
    if (!this.isEnabled()) return false;
    const config = this.configManager.getConfig();
    // Whitelist approach: agent must be explicitly configured
    const override = config.agentOverrides?.[agent];
    if (!override) return false;
    return override.enabled ?? true;
  }

  // ============================================================================
  // PATTERN OPERATIONS
  // ============================================================================

  /**
   * Query patterns for an agent
   */
  async queryPatterns(
    agent: AgentName,
    options: QueryPatternOptions = {}
  ): Promise<Pattern[]> {
    if (!this.isEnabledForAgent(agent)) {
      return [];
    }

    const startTime = Date.now();
    const memory = await this.getMemory(agent);
    let patterns = memory.patterns.map((p) => new PatternModel(p));

    // Filter by active status
    if (!options.includeInactive) {
      patterns = patterns.filter((p) => p.isActive);
    }

    // Filter by type
    if (options.type) {
      patterns = patterns.filter((p) => p.toJSON().pattern.type === options.type);
    }

    // Filter by context match
    if (options.context) {
      patterns = patterns.filter((p) => p.matchesContext(options.context!));
    }

    // Filter by minimum confidence
    if (options.minConfidence !== undefined) {
      patterns = patterns.filter((p) => p.confidenceScore >= options.minConfidence!);
    }

    // Sort patterns
    const sortBy = options.sortBy || 'weight';
    patterns.sort((a, b) => {
      switch (sortBy) {
        case 'confidence':
          return b.confidenceScore - a.confidenceScore;
        case 'weight':
          return b.calculateWeight() - a.calculateWeight();
        case 'recency':
          return (
            new Date(b.toJSON().evolution.lastUsed).getTime() -
            new Date(a.toJSON().evolution.lastUsed).getTime()
          );
        case 'successRate':
          return b.successRate - a.successRate;
        default:
          return 0;
      }
    });

    // Limit results
    if (options.limit) {
      patterns = patterns.slice(0, options.limit);
    }

    const queryTime = Date.now() - startTime;
    await this.recordQueryMetric(agent, queryTime);

    return patterns.map((p) => p.toJSON());
  }

  /**
   * Get a specific pattern by ID
   */
  async getPattern(agent: AgentName, patternId: string): Promise<Pattern | null> {
    const memory = await this.getMemory(agent);
    const pattern = memory.patterns.find((p) => p.id === patternId);
    return pattern || null;
  }

  /**
   * Record a new pattern
   */
  async recordPattern(
    agent: AgentName,
    data: RecordPatternData
  ): Promise<OperationResult<Pattern>> {
    if (!this.isEnabledForAgent(agent)) {
      return { success: false, error: 'AML not enabled for agent' };
    }

    try {
      const startTime = Date.now();
      const memory = await this.getMemory(agent);

      // Create new pattern
      const pattern = PatternModel.create(
        agent,
        data.type,
        data.context,
        data.approach,
        data.conditions
      );

      if (data.tags) {
        pattern.toJSON().tags = data.tags;
      }

      // Add to memory
      memory.patterns.push(pattern.toJSON());

      // Check size limits
      const agentConfig = this.configManager.getAgentConfig(agent);
      if (memory.patterns.length > agentConfig.maxPatternCount) {
        // Remove lowest confidence inactive patterns
        memory.patterns = memory.patterns
          .sort((a, b) => {
            const aModel = new PatternModel(a);
            const bModel = new PatternModel(b);
            return bModel.confidenceScore - aModel.confidenceScore;
          })
          .slice(0, agentConfig.maxPatternCount);
      }

      // Save to storage
      await this.saveMemory(agent, memory);

      const writeTime = Date.now() - startTime;
      await this.recordWriteMetric(agent, writeTime);

      return { success: true, data: pattern.toJSON() };
    } catch (error) {
      return {
        success: false,
        error: `Failed to record pattern: ${(error as Error).message}`,
      };
    }
  }

  /**
   * Record pattern usage and outcome
   */
  async recordPatternUsage(
    agent: AgentName,
    usage: PatternUsageResult
  ): Promise<OperationResult> {
    try {
      const memory = await this.getMemory(agent);
      const pattern = memory.patterns.find((p) => p.id === usage.patternId);

      if (!pattern) {
        return { success: false, error: 'Pattern not found' };
      }

      const patternModel = new PatternModel(pattern);
      patternModel.recordUsage(usage.success, usage.timeSavedMs);
      patternModel.updateConfidence(
        usage.success,
        this.configManager.getConfig().learning.learningRate
      );

      // Update in memory
      const index = memory.patterns.findIndex((p) => p.id === usage.patternId);
      memory.patterns[index] = patternModel.toJSON();

      await this.saveMemory(agent, memory);

      return { success: true };
    } catch (error) {
      return {
        success: false,
        error: `Failed to record pattern usage: ${(error as Error).message}`,
      };
    }
  }

  // ============================================================================
  // SOLUTION OPERATIONS
  // ============================================================================

  /**
   * Query solutions for an agent
   */
  async querySolutions(
    agent: AgentName,
    options: QuerySolutionOptions = {}
  ): Promise<Solution[]> {
    if (!this.isEnabledForAgent(agent)) {
      return [];
    }

    const startTime = Date.now();
    const memory = await this.getMemory(agent);
    let solutions = memory.solutions.map((s) => new SolutionModel(s));

    // Filter by active status
    if (!options.includeInactive) {
      solutions = solutions.filter((s) => s.isActive);
    }

    // Filter by error type
    if (options.errorType) {
      solutions = solutions.filter((s) => s.errorType === options.errorType);
    }

    // Filter by error message match
    if (options.errorMessage) {
      solutions = solutions.filter((s) =>
        s.toJSON().problem.errorMessage.toLowerCase().includes(options.errorMessage!.toLowerCase())
      );
    }

    // Filter by context
    if (options.context && options.errorType && options.errorMessage) {
      solutions = solutions.filter((s) =>
        s.matchesError(options.errorType!, options.errorMessage!, options.context)
      );
    }

    // Filter by minimum confidence
    if (options.minConfidence !== undefined) {
      solutions = solutions.filter((s) => s.calculateConfidence() >= options.minConfidence!);
    }

    // Sort by weight (confidence + recency)
    solutions.sort((a, b) => b.calculateWeight() - a.calculateWeight());

    // Limit results
    if (options.limit) {
      solutions = solutions.slice(0, options.limit);
    }

    const queryTime = Date.now() - startTime;
    await this.recordQueryMetric(agent, queryTime);

    return solutions.map((s) => s.toJSON());
  }

  /**
   * Record a new solution
   */
  async recordSolution(
    agent: AgentName,
    data: RecordSolutionData
  ): Promise<OperationResult<Solution>> {
    if (!this.isEnabledForAgent(agent)) {
      return { success: false, error: 'AML not enabled for agent' };
    }

    try {
      const startTime = Date.now();
      const memory = await this.getMemory(agent);

      // Create new solution
      const solution = SolutionModel.create(
        agent,
        {
          errorType: data.errorType,
          errorMessage: data.errorMessage,
          stackTraceHash: data.stackTraceHash,
          context: data.context,
        },
        {
          rootCause: data.rootCause,
          fixApproach: data.fixApproach,
          codeFix: data.codeFix,
          prevention: data.prevention,
        },
        {
          worked: data.worked,
          timeToFixMinutes: data.timeToFixMinutes,
          preventedRecurrence: 0,
          relatedErrorsFixed: 0,
        }
      );

      if (data.tags) {
        solution.toJSON().tags = data.tags;
      }

      // Add to memory
      memory.solutions.push(solution.toJSON());

      // Check size limits
      const agentConfig = this.configManager.getAgentConfig(agent);
      if (memory.solutions.length > agentConfig.maxSolutionCount) {
        // Remove lowest confidence inactive solutions
        memory.solutions = memory.solutions
          .sort((a, b) => {
            const aModel = new SolutionModel(a);
            const bModel = new SolutionModel(b);
            return bModel.calculateConfidence() - aModel.calculateConfidence();
          })
          .slice(0, agentConfig.maxSolutionCount);
      }

      // Save to storage
      await this.saveMemory(agent, memory);

      const writeTime = Date.now() - startTime;
      await this.recordWriteMetric(agent, writeTime);

      return { success: true, data: solution.toJSON() };
    } catch (error) {
      return {
        success: false,
        error: `Failed to record solution: ${(error as Error).message}`,
      };
    }
  }

  // ============================================================================
  // DECISION OPERATIONS
  // ============================================================================

  /**
   * Query decisions for an agent
   */
  async queryDecisions(
    agent: AgentName,
    options: QueryDecisionOptions = {}
  ): Promise<Decision[]> {
    if (!this.isEnabledForAgent(agent)) {
      return [];
    }

    const startTime = Date.now();
    const memory = await this.getMemory(agent);
    let decisions = memory.decisions.map((d) => new DecisionModel(d));

    // Filter by active status
    if (!options.includeInactive) {
      decisions = decisions.filter((d) => d.isActive);
    }

    // Filter by type
    if (options.type) {
      decisions = decisions.filter((d) => d.toJSON().decision.type === options.type);
    }

    // Filter by context
    if (options.context && options.type) {
      decisions = decisions.filter((d) => d.matchesContext(options.type!, options.context));
    }

    // Filter by outcome presence
    if (!options.includeWithoutOutcome) {
      decisions = decisions.filter((d) => d.hasOutcome);
    }

    // Sort by weight
    decisions.sort((a, b) => b.calculateWeight() - a.calculateWeight());

    // Limit results
    if (options.limit) {
      decisions = decisions.slice(0, options.limit);
    }

    const queryTime = Date.now() - startTime;
    await this.recordQueryMetric(agent, queryTime);

    return decisions.map((d) => d.toJSON());
  }

  /**
   * Record a new decision
   */
  async recordDecision(
    agent: AgentName,
    data: RecordDecisionData
  ): Promise<OperationResult<Decision>> {
    if (!this.isEnabledForAgent(agent)) {
      return { success: false, error: 'AML not enabled for agent' };
    }

    try {
      const startTime = Date.now();
      const memory = await this.getMemory(agent);

      // Create new decision
      const decision = DecisionModel.create(agent, {
        type: data.type,
        question: data.question,
        context: data.context,
        chosenOption: data.chosenOption,
        alternativesConsidered: data.alternativesConsidered,
        decisionFactors: data.decisionFactors,
        rationale: data.rationale,
      });

      if (data.tags) {
        decision.toJSON().tags = data.tags;
      }

      // Add to memory
      memory.decisions.push(decision.toJSON());

      // Check size limits
      const agentConfig = this.configManager.getAgentConfig(agent);
      if (memory.decisions.length > agentConfig.maxDecisionCount) {
        // Remove oldest inactive decisions
        memory.decisions = memory.decisions
          .sort(
            (a, b) =>
              new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime()
          )
          .slice(0, agentConfig.maxDecisionCount);
      }

      // Save to storage
      await this.saveMemory(agent, memory);

      const writeTime = Date.now() - startTime;
      await this.recordWriteMetric(agent, writeTime);

      return { success: true, data: decision.toJSON() };
    } catch (error) {
      return {
        success: false,
        error: `Failed to record decision: ${(error as Error).message}`,
      };
    }
  }

  // ============================================================================
  // METRICS OPERATIONS
  // ============================================================================

  /**
   * Get metrics report for an agent
   */
  async getMetrics(agent: AgentName): Promise<MetricsReport | null> {
    if (!this.isEnabledForAgent(agent)) {
      return null;
    }

    try {
      const memory = await this.getMemory(agent);
      const patterns = memory.patterns.map((p) => new PatternModel(p));
      const solutions = memory.solutions.map((s) => new SolutionModel(s));
      const decisions = memory.decisions.map((d) => new DecisionModel(d));

      const activePatterns = patterns.filter((p) => p.isActive);
      const activeSolutions = solutions.filter((s) => s.isActive);
      const activeDecisions = decisions.filter((d) => d.isActive);

      const avgPatternConfidence =
        activePatterns.length > 0
          ? activePatterns.reduce((sum, p) => sum + p.confidenceScore, 0) / activePatterns.length
          : 0;

      const avgSolutionConfidence =
        activeSolutions.length > 0
          ? activeSolutions.reduce((sum, s) => sum + s.calculateConfidence(), 0) /
            activeSolutions.length
          : 0;

      const avgConfidence = (avgPatternConfidence + avgSolutionConfidence) / 2;

      const memoryUsageBytes = await this.store.getAgentMemorySize(agent);

      // Simple health score based on confidence and active items
      const healthScore = Math.min(
        (avgConfidence * 0.5 +
          (activePatterns.length > 0 ? 0.25 : 0) +
          (activeSolutions.length > 0 ? 0.25 : 0)) *
          1.0,
        1.0
      );

      return {
        agent,
        totalPatterns: patterns.length,
        activePatterns: activePatterns.length,
        totalSolutions: solutions.length,
        activeSolutions: activeSolutions.length,
        totalDecisions: decisions.length,
        activeDecisions: activeDecisions.length,
        avgConfidence,
        memoryUsageBytes,
        healthScore,
      };
    } catch (error) {
      return null;
    }
  }

  /**
   * Get metrics for all agents
   */
  async getAllMetrics(): Promise<MetricsReport[]> {
    const agents = await this.store.listAgents();
    const reports: MetricsReport[] = [];

    for (const agent of agents) {
      const report = await this.getMetrics(agent);
      if (report) {
        reports.push(report);
      }
    }

    return reports;
  }

  // ============================================================================
  // MANAGEMENT OPERATIONS
  // ============================================================================

  /**
   * Clear all memory for an agent
   */
  async clearAgentMemory(agent: AgentName, createBackup: boolean = true): Promise<OperationResult> {
    try {
      if (createBackup) {
        await this.store.backupAgentMemory(agent);
      }

      await this.store.deleteAgentMemory(agent);
      this.memoryCache.delete(agent);
      this.cacheTimestamps.delete(agent);

      return { success: true };
    } catch (error) {
      return {
        success: false,
        error: `Failed to clear agent memory: ${(error as Error).message}`,
      };
    }
  }

  /**
   * Export agent memory
   */
  async exportMemory(agent: AgentName): Promise<OperationResult<MemoryData>> {
    try {
      const memory = await this.store.loadAgentMemory(agent);
      return { success: true, data: memory };
    } catch (error) {
      return {
        success: false,
        error: `Failed to export memory: ${(error as Error).message}`,
      };
    }
  }

  /**
   * Import agent memory
   */
  async importMemory(agent: AgentName, data: MemoryData): Promise<OperationResult> {
    try {
      await this.store.saveAgentMemory(agent, data);
      this.memoryCache.delete(agent); // Invalidate cache
      return { success: true };
    } catch (error) {
      return {
        success: false,
        error: `Failed to import memory: ${(error as Error).message}`,
      };
    }
  }

  /**
   * List all agents with memory
   */
  async listAgents(): Promise<AgentName[]> {
    return await this.store.listAgents();
  }

  /**
   * Get total memory usage
   */
  async getTotalMemoryUsage(): Promise<number> {
    return await this.store.getTotalMemorySize();
  }

  // ============================================================================
  // INTERNAL HELPER METHODS
  // ============================================================================

  /**
   * Get memory for an agent (with caching)
   */
  private async getMemory(agent: AgentName): Promise<MemoryData> {
    const now = Date.now();
    const cached = this.memoryCache.get(agent);
    const timestamp = this.cacheTimestamps.get(agent);

    // Return cached if still valid
    if (cached && timestamp && now - timestamp < this.cacheTTL) {
      return cached;
    }

    // Load from storage
    const memory = await this.store.loadAgentMemory(agent);
    this.memoryCache.set(agent, memory);
    this.cacheTimestamps.set(agent, now);

    return memory;
  }

  /**
   * Save memory for an agent
   */
  private async saveMemory(agent: AgentName, memory: MemoryData): Promise<void> {
    await this.store.saveAgentMemory(agent, memory);
    this.memoryCache.set(agent, memory);
    this.cacheTimestamps.set(agent, Date.now());
  }

  /**
   * Record query metric (for performance tracking)
   */
  private async recordQueryMetric(_agent: AgentName, _latencyMs: number): Promise<void> {
    // TODO: Implement metrics collection
    // This will be handled by MetricsCollector in next phase
  }

  /**
   * Record write metric (for performance tracking)
   */
  private async recordWriteMetric(_agent: AgentName, _latencyMs: number): Promise<void> {
    // TODO: Implement metrics collection
    // This will be handled by MetricsCollector in next phase
  }
}
