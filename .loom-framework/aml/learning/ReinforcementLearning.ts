/**
 * Reinforcement Learning Module - Q-learning for agent decision optimization
 *
 * This module implements a sophisticated RL system for agent learning:
 * - Q-learning algorithm with temporal difference learning
 * - State-action value table management
 * - ε-greedy exploration vs exploitation balancing
 * - Reward shaping for different outcomes
 * - Experience replay for efficient learning
 * - Policy gradient hints for complex decisions
 */

import { AgentName } from '../types/common';

/**
 * State representation for Q-learning
 *
 * State encodes:
 * - Context features (project type, complexity, etc.)
 * - Agent internal state (recent successes, confidence)
 * - Task characteristics (urgency, risk, novelty)
 */
export interface State {
  id: string;
  features: Record<string, number | string | boolean>;
  timestamp: string;
  agentState: {
    recentSuccessRate: number;
    confidenceLevel: number;
    energyLevel: number; // Simulates agent "fatigue" or "momentum"
  };
}

/**
 * Action representation
 */
export interface Action {
  id: string;
  type: string;
  patternId?: string;
  parameters: Record<string, unknown>;
  estimatedCost: number; // Computational/time cost
  riskLevel: 'low' | 'medium' | 'high';
}

/**
 * Reward signal after action execution
 */
export interface Reward {
  value: number; // -1 to +1
  components: {
    successBonus: number; // Did action succeed?
    efficiencyBonus: number; // Was it fast?
    qualityBonus: number; // Was output high quality?
    noveltyBonus: number; // Did we learn something new?
    riskPenalty: number; // Did we take unnecessary risks?
  };
  feedback?: string;
}

/**
 * Experience tuple for replay learning
 */
export interface Experience {
  state: State;
  action: Action;
  reward: Reward;
  nextState: State;
  timestamp: string;
}

/**
 * Q-value entry
 */
interface QValue {
  value: number;
  updateCount: number;
  lastUpdated: string;
  confidence: number;
}

/**
 * Configuration for reinforcement learning
 */
export interface ReinforcementLearningConfig {
  // Q-learning parameters
  learning: {
    learningRate: number; // α (alpha): 0-1, how fast to update Q-values (default: 0.1)
    discountFactor: number; // γ (gamma): 0-1, importance of future rewards (default: 0.9)
    initialQValue: number; // Starting Q-value for unknown state-action pairs (default: 0.5)
  };

  // Exploration vs Exploitation
  exploration: {
    epsilon: number; // ε: probability of random action (default: 0.2)
    epsilonDecay: number; // Decay rate per episode (default: 0.995)
    epsilonMin: number; // Minimum epsilon (default: 0.01)
    explorationBonus: number; // Bonus for trying new actions (default: 0.1)
  };

  // Reward shaping
  rewards: {
    successReward: number; // Reward for successful action (default: 1.0)
    failureReward: number; // Penalty for failed action (default: -0.5)
    efficiencyMultiplier: number; // Multiplier for time savings (default: 0.3)
    qualityMultiplier: number; // Multiplier for quality improvements (default: 0.4)
    noveltyReward: number; // Bonus for exploration (default: 0.2)
    riskPenalty: number; // Penalty for high-risk actions (default: -0.2)
  };

  // Experience replay
  replay: {
    enabled: boolean; // Enable experience replay (default: true)
    bufferSize: number; // Max experiences to store (default: 10000)
    batchSize: number; // Training batch size (default: 32)
    replayFrequency: number; // How often to replay (default: every 10 actions)
  };

  // Q-table management
  qtable: {
    maxSize: number; // Maximum Q-table entries (default: 100000)
    pruneThreshold: number; // Remove entries below this confidence (default: 0.1)
    pruneInterval: number; // Prune every N updates (default: 1000)
  };
}

/**
 * Default configuration
 */
const DEFAULT_CONFIG: ReinforcementLearningConfig = {
  learning: {
    learningRate: 0.1,
    discountFactor: 0.9,
    initialQValue: 0.5,
  },
  exploration: {
    epsilon: 0.2,
    epsilonDecay: 0.995,
    epsilonMin: 0.01,
    explorationBonus: 0.1,
  },
  rewards: {
    successReward: 1.0,
    failureReward: -0.5,
    efficiencyMultiplier: 0.3,
    qualityMultiplier: 0.4,
    noveltyReward: 0.2,
    riskPenalty: -0.2,
  },
  replay: {
    enabled: true,
    bufferSize: 10000,
    batchSize: 32,
    replayFrequency: 10,
  },
  qtable: {
    maxSize: 100000,
    pruneThreshold: 0.1,
    pruneInterval: 1000,
  },
};

/**
 * Reinforcement Learning Module
 *
 * Philosophy:
 * - Agents should learn optimal policies through trial and error
 * - Balance exploration (trying new things) with exploitation (using known good patterns)
 * - Reward not just success, but efficiency and quality
 * - Learn from past experiences through replay
 * - Adapt learning rate based on confidence
 */
export class ReinforcementLearningModule {
  private config: ReinforcementLearningConfig;
  private qTable: Map<string, Map<string, QValue>>; // state -> action -> Q-value
  private experienceBuffer: Experience[];
  private updateCount: number;
  private currentEpsilon: number;
  private performanceHistory: Map<string, number[]>; // Track performance per agent

  constructor(config: Partial<ReinforcementLearningConfig> = {}) {
    this.config = this.mergeConfig(config);
    this.qTable = new Map();
    this.experienceBuffer = [];
    this.updateCount = 0;
    this.currentEpsilon = this.config.exploration.epsilon;
    this.performanceHistory = new Map();
  }

  /**
   * Select best action for given state (with ε-greedy exploration)
   *
   * Algorithm:
   * - With probability ε: choose random action (exploration)
   * - With probability 1-ε: choose action with highest Q-value (exploitation)
   * - Add exploration bonus to unvisited actions
   */
  selectAction(
    state: State,
    availableActions: Action[],
    _agentName: AgentName,
    forceExploit: boolean = false
  ): Action {
    if (availableActions.length === 0) {
      throw new Error('No available actions');
    }

    // Exploration vs Exploitation decision
    const shouldExplore = !forceExploit && Math.random() < this.currentEpsilon;

    if (shouldExplore) {
      // Random exploration
      const randomIndex = Math.floor(Math.random() * availableActions.length);
      return availableActions[randomIndex];
    }

    // Exploitation: choose best action based on Q-values
    const stateKey = this.getStateKey(state);
    const stateQValues = this.qTable.get(stateKey);

    let bestAction = availableActions[0];
    let bestValue = -Infinity;

    for (const action of availableActions) {
      const actionKey = this.getActionKey(action);
      let qValue = this.config.learning.initialQValue;

      if (stateQValues?.has(actionKey)) {
        const qEntry = stateQValues.get(actionKey)!;
        qValue = qEntry.value;

        // Reduce Q-value by risk penalty
        if (action.riskLevel === 'high') {
          qValue += this.config.rewards.riskPenalty;
        } else if (action.riskLevel === 'medium') {
          qValue += this.config.rewards.riskPenalty * 0.5;
        }
      } else {
        // Exploration bonus for never-tried actions
        qValue += this.config.exploration.explorationBonus;
      }

      if (qValue > bestValue) {
        bestValue = qValue;
        bestAction = action;
      }
    }

    return bestAction;
  }

  /**
   * Update Q-values based on action outcome (Q-learning update rule)
   *
   * Q(s,a) ← Q(s,a) + α[r + γ max Q(s',a') - Q(s,a)]
   *
   * Where:
   * - α (alpha): learning rate
   * - r: immediate reward
   * - γ (gamma): discount factor
   * - s': next state
   * - a': best action in next state
   */
  updateQValue(
    state: State,
    action: Action,
    reward: Reward,
    nextState: State,
    agentName: AgentName
  ): void {
    const stateKey = this.getStateKey(state);
    const actionKey = this.getActionKey(action);
    const nextStateKey = this.getStateKey(nextState);

    // Get current Q-value
    if (!this.qTable.has(stateKey)) {
      this.qTable.set(stateKey, new Map());
    }

    const stateQValues = this.qTable.get(stateKey)!;
    const currentQEntry = stateQValues.get(actionKey) || {
      value: this.config.learning.initialQValue,
      updateCount: 0,
      lastUpdated: new Date().toISOString(),
      confidence: 0.1,
    };

    // Get max Q-value for next state
    const nextStateQValues = this.qTable.get(nextStateKey);
    let maxNextQ = this.config.learning.initialQValue;

    if (nextStateQValues) {
      for (const qEntry of nextStateQValues.values()) {
        maxNextQ = Math.max(maxNextQ, qEntry.value);
      }
    }

    // Calculate TD target: r + γ * max Q(s',a')
    const tdTarget =
      reward.value + this.config.learning.discountFactor * maxNextQ;

    // Calculate TD error: TD target - current Q
    const tdError = tdTarget - currentQEntry.value;

    // Adaptive learning rate based on confidence
    const adaptiveLearningRate = this.calculateAdaptiveLearningRate(
      currentQEntry.updateCount,
      currentQEntry.confidence
    );

    // Update Q-value: Q(s,a) ← Q(s,a) + α * TD error
    const newQValue = currentQEntry.value + adaptiveLearningRate * tdError;

    // Update confidence (more updates = higher confidence)
    const newConfidence = Math.min(
      currentQEntry.confidence + 0.05,
      1.0
    );

    // Store updated Q-value
    stateQValues.set(actionKey, {
      value: newQValue,
      updateCount: currentQEntry.updateCount + 1,
      lastUpdated: new Date().toISOString(),
      confidence: newConfidence,
    });

    // Add to experience buffer for replay
    if (this.config.replay.enabled) {
      this.addExperience({
        state,
        action,
        reward,
        nextState,
        timestamp: new Date().toISOString(),
      });
    }

    this.updateCount++;

    // Track performance
    this.trackPerformance(agentName, reward.value);

    // Decay epsilon
    this.decayEpsilon();

    // Periodic maintenance
    if (this.updateCount % this.config.replay.replayFrequency === 0) {
      if (this.config.replay.enabled) {
        this.replayExperiences();
      }
    }

    if (this.updateCount % this.config.qtable.pruneInterval === 0) {
      this.pruneQTable();
    }
  }

  /**
   * Shape reward based on outcome components
   *
   * Combines multiple reward signals:
   * - Success/failure (primary signal)
   * - Efficiency (time/resource usage)
   * - Quality (code quality, test coverage)
   * - Novelty (learning new patterns)
   * - Risk (unnecessary risk-taking)
   */
  shapeReward(
    success: boolean,
    timeSavedMs: number,
    qualityScore: number,
    isNovel: boolean,
    riskLevel: 'low' | 'medium' | 'high'
  ): Reward {
    const components = {
      successBonus: success
        ? this.config.rewards.successReward
        : this.config.rewards.failureReward,

      efficiencyBonus:
        timeSavedMs > 0
          ? Math.min(timeSavedMs / 1000, 1.0) * this.config.rewards.efficiencyMultiplier
          : 0,

      qualityBonus: qualityScore * this.config.rewards.qualityMultiplier,

      noveltyBonus: isNovel ? this.config.rewards.noveltyReward : 0,

      riskPenalty:
        riskLevel === 'high'
          ? this.config.rewards.riskPenalty
          : riskLevel === 'medium'
            ? this.config.rewards.riskPenalty * 0.5
            : 0,
    };

    const totalReward =
      components.successBonus +
      components.efficiencyBonus +
      components.qualityBonus +
      components.noveltyBonus +
      components.riskPenalty;

    // Clamp to [-1, 1]
    const clampedReward = Math.max(-1, Math.min(1, totalReward));

    return {
      value: clampedReward,
      components,
    };
  }

  /**
   * Get Q-value for state-action pair
   */
  getQValue(state: State, action: Action): number {
    const stateKey = this.getStateKey(state);
    const actionKey = this.getActionKey(action);

    const qEntry = this.qTable.get(stateKey)?.get(actionKey);
    return qEntry?.value ?? this.config.learning.initialQValue;
  }

  /**
   * Get best action for state (greedy selection, no exploration)
   */
  getBestAction(state: State, availableActions: Action[]): Action | null {
    if (availableActions.length === 0) {
      return null;
    }

    let bestAction = availableActions[0];
    let bestValue = this.getQValue(state, bestAction);

    for (const action of availableActions.slice(1)) {
      const qValue = this.getQValue(state, action);
      if (qValue > bestValue) {
        bestValue = qValue;
        bestAction = action;
      }
    }

    return bestAction;
  }

  /**
   * Get learning statistics
   */
  getStatistics(agentName?: AgentName): {
    totalUpdates: number;
    qTableSize: number;
    experienceBufferSize: number;
    currentEpsilon: number;
    avgPerformance: number;
    recentTrend: 'improving' | 'stable' | 'declining';
  } {
    const avgPerformance = agentName
      ? this.calculateAvgPerformance(agentName)
      : this.calculateOverallPerformance();

    const recentTrend = agentName
      ? this.calculateTrend(agentName)
      : 'stable';

    return {
      totalUpdates: this.updateCount,
      qTableSize: this.getQTableSize(),
      experienceBufferSize: this.experienceBuffer.length,
      currentEpsilon: this.currentEpsilon,
      avgPerformance,
      recentTrend,
    };
  }

  /**
   * Reset epsilon to initial value (for new learning phase)
   */
  resetEpsilon(): void {
    this.currentEpsilon = this.config.exploration.epsilon;
  }

  /**
   * Export Q-table for persistence
   */
  exportQTable(): Record<string, Record<string, QValue>> {
    const exported: Record<string, Record<string, QValue>> = {};

    for (const [stateKey, actions] of this.qTable.entries()) {
      exported[stateKey] = {};
      for (const [actionKey, qValue] of actions.entries()) {
        exported[stateKey][actionKey] = { ...qValue };
      }
    }

    return exported;
  }

  /**
   * Import Q-table from persistence
   */
  importQTable(data: Record<string, Record<string, QValue>>): void {
    this.qTable.clear();

    for (const [stateKey, actions] of Object.entries(data)) {
      const actionMap = new Map<string, QValue>();
      for (const [actionKey, qValue] of Object.entries(actions)) {
        actionMap.set(actionKey, qValue);
      }
      this.qTable.set(stateKey, actionMap);
    }
  }

  /**
   * Clear all learning data
   */
  reset(): void {
    this.qTable.clear();
    this.experienceBuffer = [];
    this.updateCount = 0;
    this.currentEpsilon = this.config.exploration.epsilon;
    this.performanceHistory.clear();
  }

  // ============================================================================
  // Private Helper Methods
  // ============================================================================

  /**
   * Generate state key for Q-table lookup
   */
  private getStateKey(state: State): string {
    // Hash state features into a key
    const features = Object.entries(state.features)
      .sort(([a], [b]) => a.localeCompare(b))
      .map(([k, v]) => `${k}:${v}`)
      .join('|');

    const agentState = `${state.agentState.recentSuccessRate.toFixed(2)}:${state.agentState.confidenceLevel.toFixed(2)}`;

    return `${features}|${agentState}`;
  }

  /**
   * Generate action key for Q-table lookup
   */
  private getActionKey(action: Action): string {
    return `${action.type}:${action.patternId || 'none'}:${action.riskLevel}`;
  }

  /**
   * Calculate adaptive learning rate
   *
   * - Early learning: higher rate
   * - Later learning: lower rate (more stable)
   * - Low confidence: higher rate (more adjustment needed)
   */
  private calculateAdaptiveLearningRate(updateCount: number, confidence: number): number {
    const baseLearningRate = this.config.learning.learningRate;

    // Decay based on update count (fewer updates = faster learning)
    const countFactor = 1 / (1 + updateCount * 0.01);

    // Increase for low confidence
    const confidenceFactor = 1 + (1 - confidence) * 0.5;

    return baseLearningRate * countFactor * confidenceFactor;
  }

  /**
   * Decay epsilon over time (reduce exploration)
   */
  private decayEpsilon(): void {
    this.currentEpsilon = Math.max(
      this.config.exploration.epsilonMin,
      this.currentEpsilon * this.config.exploration.epsilonDecay
    );
  }

  /**
   * Add experience to replay buffer
   */
  private addExperience(experience: Experience): void {
    this.experienceBuffer.push(experience);

    // Remove oldest if buffer is full
    if (this.experienceBuffer.length > this.config.replay.bufferSize) {
      this.experienceBuffer.shift();
    }
  }

  /**
   * Replay random batch of experiences for learning
   *
   * Experience replay improves learning by:
   * - Breaking correlation between consecutive updates
   * - Reusing past experiences multiple times
   * - Improving sample efficiency
   */
  private replayExperiences(): void {
    if (this.experienceBuffer.length < this.config.replay.batchSize) {
      return;
    }

    // Sample random batch
    const batch: Experience[] = [];
    const batchSize = Math.min(this.config.replay.batchSize, this.experienceBuffer.length);

    for (let i = 0; i < batchSize; i++) {
      const idx = Math.floor(Math.random() * this.experienceBuffer.length);
      batch.push(this.experienceBuffer[idx]);
    }

    // Update Q-values for batch
    for (const exp of batch) {
      // Recalculate with current Q-table (may have updated since experience)
      const stateKey = this.getStateKey(exp.state);
      const actionKey = this.getActionKey(exp.action);
      const nextStateKey = this.getStateKey(exp.nextState);

      const currentQEntry = this.qTable.get(stateKey)?.get(actionKey);
      if (!currentQEntry) continue;

      const nextStateQValues = this.qTable.get(nextStateKey);
      let maxNextQ = this.config.learning.initialQValue;

      if (nextStateQValues) {
        for (const qEntry of nextStateQValues.values()) {
          maxNextQ = Math.max(maxNextQ, qEntry.value);
        }
      }

      const tdTarget = exp.reward.value + this.config.learning.discountFactor * maxNextQ;
      const tdError = tdTarget - currentQEntry.value;

      // Smaller learning rate for replay (don't overwrite recent learning)
      const replayLearningRate = this.config.learning.learningRate * 0.5;
      const newQValue = currentQEntry.value + replayLearningRate * tdError;

      this.qTable.get(stateKey)!.set(actionKey, {
        ...currentQEntry,
        value: newQValue,
      });
    }
  }

  /**
   * Prune low-confidence Q-table entries
   */
  private pruneQTable(): void {
    let prunedCount = 0;

    for (const [stateKey, actions] of this.qTable.entries()) {
      const toRemove: string[] = [];

      for (const [actionKey, qEntry] of actions.entries()) {
        if (qEntry.confidence < this.config.qtable.pruneThreshold) {
          toRemove.push(actionKey);
        }
      }

      for (const key of toRemove) {
        actions.delete(key);
        prunedCount++;
      }

      // Remove empty state entries
      if (actions.size === 0) {
        this.qTable.delete(stateKey);
      }
    }

    // If still too large, prune oldest entries
    if (this.getQTableSize() > this.config.qtable.maxSize) {
      this.pruneOldestEntries();
    }
  }

  /**
   * Prune oldest Q-table entries when size limit exceeded
   */
  private pruneOldestEntries(): void {
    const allEntries: Array<[string, string, QValue]> = [];

    for (const [stateKey, actions] of this.qTable.entries()) {
      for (const [actionKey, qValue] of actions.entries()) {
        allEntries.push([stateKey, actionKey, qValue]);
      }
    }

    // Sort by last updated (oldest first)
    allEntries.sort((a, b) =>
      new Date(a[2].lastUpdated).getTime() - new Date(b[2].lastUpdated).getTime()
    );

    // Remove oldest 20%
    const toRemove = Math.floor(allEntries.length * 0.2);
    for (let i = 0; i < toRemove; i++) {
      const [stateKey, actionKey] = allEntries[i];
      this.qTable.get(stateKey)?.delete(actionKey);
    }
  }

  /**
   * Track agent performance
   */
  private trackPerformance(agentName: AgentName, reward: number): void {
    if (!this.performanceHistory.has(agentName)) {
      this.performanceHistory.set(agentName, []);
    }

    const history = this.performanceHistory.get(agentName)!;
    history.push(reward);

    // Keep only recent history (last 100 actions)
    if (history.length > 100) {
      history.shift();
    }
  }

  /**
   * Calculate average performance for agent
   */
  private calculateAvgPerformance(agentName: AgentName): number {
    const history = this.performanceHistory.get(agentName);
    if (!history || history.length === 0) {
      return 0;
    }

    return history.reduce((sum, r) => sum + r, 0) / history.length;
  }

  /**
   * Calculate overall performance across all agents
   */
  private calculateOverallPerformance(): number {
    let totalReward = 0;
    let totalCount = 0;

    for (const history of this.performanceHistory.values()) {
      totalReward += history.reduce((sum, r) => sum + r, 0);
      totalCount += history.length;
    }

    return totalCount === 0 ? 0 : totalReward / totalCount;
  }

  /**
   * Calculate performance trend
   */
  private calculateTrend(agentName: AgentName): 'improving' | 'stable' | 'declining' {
    const history = this.performanceHistory.get(agentName);
    if (!history || history.length < 10) {
      return 'stable';
    }

    const recentSize = Math.min(20, Math.floor(history.length / 2));
    const recent = history.slice(-recentSize);
    const older = history.slice(-2 * recentSize, -recentSize);

    const recentAvg = recent.reduce((sum, r) => sum + r, 0) / recent.length;
    const olderAvg = older.reduce((sum, r) => sum + r, 0) / older.length;

    const diff = recentAvg - olderAvg;

    if (diff > 0.1) return 'improving';
    if (diff < -0.1) return 'declining';
    return 'stable';
  }

  /**
   * Get total Q-table size
   */
  private getQTableSize(): number {
    let size = 0;
    for (const actions of this.qTable.values()) {
      size += actions.size;
    }
    return size;
  }

  /**
   * Merge user config with defaults
   */
  private mergeConfig(
    userConfig: Partial<ReinforcementLearningConfig>
  ): ReinforcementLearningConfig {
    return {
      learning: { ...DEFAULT_CONFIG.learning, ...userConfig.learning },
      exploration: { ...DEFAULT_CONFIG.exploration, ...userConfig.exploration },
      rewards: { ...DEFAULT_CONFIG.rewards, ...userConfig.rewards },
      replay: { ...DEFAULT_CONFIG.replay, ...userConfig.replay },
      qtable: { ...DEFAULT_CONFIG.qtable, ...userConfig.qtable },
    };
  }
}
