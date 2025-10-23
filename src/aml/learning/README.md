# AML Learning Algorithms

This directory contains the core learning algorithms that power the Agent Memory & Learning (AML) system in Loom. These algorithms enable agents to learn from experience, adapt to changing conditions, and share knowledge across the agent ecosystem.

## Overview

The learning system consists of five interconnected modules:

1. **Pattern Recognition** - Identifies repeatable patterns from agent actions
2. **Success Weighting** - Calculates multi-factor weights for decision making
3. **Cross-Agent Learning** - Enables knowledge sharing and pattern adaptation
4. **Reinforcement Learning** - Q-learning for optimal policy discovery
5. **Trend Analysis** - Detects performance patterns and forecasts future behavior

## Modules

### 1. Pattern Recognition Engine

**File**: `PatternRecognition.ts`

**Purpose**: Extract and identify repeatable patterns from agent action histories.

**Key Algorithms**:
- **Sequence Extraction**: Sliding window with temporal grouping
- **Similarity Matching**: Ensemble of cosine similarity, edit distance, and semantic comparison
- **Pattern Scoring**: Multi-factor weighted scoring system
- **Statistical Validation**: Chi-square significance testing

**Configuration**:
```typescript
const config = {
  minSequenceLength: 2,        // Minimum actions in pattern
  maxSequenceLength: 10,       // Maximum actions to consider
  minFrequency: 3,             // Minimum occurrences required
  minSimilarity: 0.7,          // Similarity threshold (0-1)
  significanceThreshold: 0.05, // p-value for significance
  temporalWindow: 300000,      // 5 minutes in ms
};
```

**Usage Example**:
```typescript
import { PatternRecognitionEngine } from './learning';

const engine = new PatternRecognitionEngine(config);

// Extract sequences from action history
const sequences = engine.extractSequences(actions, 'frontend-developer');

// Find common patterns
const common = engine.findCommonSubsequences(sequences);

// Score patterns
const score = engine.scorePattern(sequence, existingPatterns, context);

// Validate pattern significance
const validation = engine.validatePattern(sequence, existingPatterns);
```

**Algorithm Details**:

*Sliding Window Extraction*:
- Iterates over action history with windows of size N (2 to 10)
- Groups actions within temporal window (5 minutes default)
- Normalizes sequences to handle variations

*Similarity Ensemble*:
- Cosine Similarity (40%): Feature vector comparison
- Edit Distance (30%): Structural similarity (Levenshtein)
- Semantic Similarity (30%): Action type and outcome matching

*Statistical Validation*:
- Chi-square test for significance
- Minimum frequency requirement
- Success rate threshold
- p-value < 0.05 for acceptance

---

### 2. Success Weighting System

**File**: `SuccessWeighting.ts`

**Purpose**: Calculate dynamic weights for patterns based on multiple factors.

**Key Features**:
- Multi-factor weighting (success rate, recency, complexity, project fit)
- Exponential recency decay
- Dynamic threshold adjustment
- Confidence interval calculation
- Performance history tracking

**Weighting Formula**:
```
Weight = BaseSuccessRate × 0.4 +
         RecencyFactor × 0.3 +
         ComplexityFactor × 0.1 +
         ProjectFitFactor × 0.2
```

**Configuration**:
```typescript
const config = {
  weights: {
    baseSuccessRate: 0.4,
    recencyFactor: 0.3,
    complexityFactor: 0.1,
    projectFitFactor: 0.2,
  },
  recency: {
    halfLifeDays: 30,      // Days until weight halves
    maxAgeDays: 180,       // Maximum age before floor
    floorWeight: 0.1,      // Minimum recency weight
  },
  complexity: {
    maxSteps: 10,          // Steps before penalty
    penaltyFactor: 0.1,    // Penalty per additional step
  },
  confidence: {
    minSampleSize: 10,     // Samples for high confidence
    confidenceLevel: 0.95, // Z-score confidence level
  },
  thresholds: {
    enabled: true,
    adjustmentRate: 0.05,
    minWeight: 0.3,
    maxWeight: 0.85,
  },
};
```

**Usage Example**:
```typescript
import { SuccessWeightingSystem } from './learning';

const system = new SuccessWeightingSystem(config);

// Calculate weight for pattern
const result = system.calculatePatternWeight(pattern, currentContext, projectMetadata);

console.log(result.totalWeight);                    // 0.87
console.log(result.recommendationStrength);         // 'very-strong'
console.log(result.factors.baseSuccessRate);        // 0.92
console.log(result.confidenceInterval);             // { lower: 0.82, upper: 0.92 }

// Adjust thresholds dynamically
const thresholds = system.adjustThresholds(patternId);
```

**Recency Decay**:
```
RecencyFactor = max(floorWeight, e^(-age / halfLife))
```

This ensures recent patterns are preferred while preventing complete obsolescence.

**Complexity Penalty**:
```
ComplexityFactor = max(0.1, 1 - log(complexity + 1) / log(2) × penaltyFactor)
```

Simpler patterns score higher, following Occam's Razor principle.

---

### 3. Cross-Agent Learning

**File**: `CrossAgentLearning.ts`

**Purpose**: Enable knowledge sharing and pattern adaptation across agents.

**Key Features**:
- Agent compatibility checking (capabilities, domains, focus areas)
- Pattern adaptation algorithm
- Knowledge sharing protocol
- Conflict resolution (weighted voting)
- Consensus mechanism
- Cross-pollination tracking

**Compatibility Scoring**:
```
CompatibilityScore = CapabilityOverlap × 0.4 +
                     DomainOverlap × 0.4 +
                     FocusAreaAlignment × 0.2
```

**Configuration**:
```typescript
const config = {
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
```

**Usage Example**:
```typescript
import { CrossAgentLearning } from './learning';

const cal = new CrossAgentLearning(config);

// Register agent profiles
cal.registerAgent({
  name: 'frontend-developer',
  capabilities: ['react', 'typescript', 'testing'],
  domains: ['frontend', 'ui'],
  focusAreas: ['performance', 'accessibility'],
  complexity: 'advanced',
  learningRate: 0.15,
});

// Check compatibility
const compatibility = cal.checkCompatibility('frontend-developer', 'backend-architect');

// Adapt pattern for target agent
const adapted = cal.adaptPattern(pattern, 'frontend-developer', 'mobile-developer');

// Share pattern with compatible agents
const sharedPatterns = cal.sharePattern('test-automator', pattern);

// Resolve conflicts
const consensus = cal.resolveConflict(conflict);
```

**Adaptation Algorithm**:
1. Preserve core approach and rationale
2. Adjust terminology to target vocabulary
3. Modify complexity based on agent level
4. Update context for target domain
5. Reduce confidence proportionally

**Conflict Resolution**:
- Weighted voting based on success rate (40%), confidence (20%), usage (10%), expertise (30%)
- Quorum requirement for validity
- Tiebreaker rules (configurable)
- Minority opinion tracking

---

### 4. Reinforcement Learning Module

**File**: `ReinforcementLearning.ts`

**Purpose**: Q-learning algorithm for optimal policy discovery.

**Key Features**:
- Q-learning with temporal difference updates
- ε-greedy exploration vs exploitation
- Reward shaping (success, efficiency, quality, novelty, risk)
- Experience replay for efficient learning
- Adaptive learning rate
- Q-table pruning

**Q-Learning Update Rule**:
```
Q(s,a) ← Q(s,a) + α[r + γ × max Q(s',a') - Q(s,a)]

Where:
- α (alpha): learning rate (0.1 default)
- r: immediate reward
- γ (gamma): discount factor (0.9 default)
- s': next state
- a': best action in next state
```

**Configuration**:
```typescript
const config = {
  learning: {
    learningRate: 0.1,        // α (alpha)
    discountFactor: 0.9,      // γ (gamma)
    initialQValue: 0.5,
  },
  exploration: {
    epsilon: 0.2,             // ε exploration rate
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
```

**Usage Example**:
```typescript
import { ReinforcementLearningModule } from './learning';

const rl = new ReinforcementLearningModule(config);

// Select action (ε-greedy)
const action = rl.selectAction(state, availableActions, 'frontend-developer');

// Execute action and get outcome...

// Shape reward
const reward = rl.shapeReward(
  success,
  timeSavedMs,
  qualityScore,
  isNovel,
  riskLevel
);

// Update Q-values
rl.updateQValue(state, action, reward, nextState, 'frontend-developer');

// Get statistics
const stats = rl.getStatistics('frontend-developer');
console.log(stats.avgPerformance);      // 0.72
console.log(stats.recentTrend);         // 'improving'
console.log(stats.qTableSize);          // 1523
```

**Reward Shaping**:
```
Reward = SuccessBonus +
         EfficiencyBonus +
         QualityBonus +
         NoveltyBonus +
         RiskPenalty

Clamped to [-1, 1]
```

**Experience Replay**:
- Stores past experiences in buffer
- Randomly samples batch for training
- Breaks correlation between consecutive updates
- Improves sample efficiency

---

### 5. Trend Analysis System

**File**: `TrendAnalysis.ts`

**Purpose**: Detect performance patterns, anomalies, and forecast future behavior.

**Key Features**:
- Anomaly detection (Z-score, rolling statistics)
- Performance trend forecasting (linear, exponential, moving average)
- Seasonal pattern recognition (autocorrelation)
- Change point detection (CUSUM algorithm)
- Adaptive learning rate recommendations

**Anomaly Detection**:
- Z-score method with rolling window
- Sensitivity levels (low, medium, high)
- Anomaly types: spike, drop, shift, outlier
- Severity classification: low, medium, high, critical

**Configuration**:
```typescript
const config = {
  anomaly: {
    sensitivityLevel: 'medium',
    windowSize: 20,
    stdDevThreshold: 3.0,
    minDataPoints: 10,
  },
  trend: {
    windowSize: 20,
    smoothingFactor: 0.3,
    significanceThreshold: 0.05,
  },
  forecast: {
    horizonSteps: 10,
    method: 'auto',  // or 'linear', 'exponential', 'moving-average'
    confidenceLevel: 0.95,
  },
  seasonality: {
    enabled: true,
    minPeriod: 7,
    maxPeriod: 30,
    significanceThreshold: 0.7,
  },
  learningRate: {
    minRate: 0.01,
    maxRate: 0.5,
    adjustmentFactor: 0.1,
    stabilityWindow: 10,
  },
};
```

**Usage Example**:
```typescript
import { TrendAnalysisSystem } from './learning';

const tas = new TrendAnalysisSystem(config);

// Record data points over time
tas.recordDataPoint(patternId, successRate, metadata);

// Analyze trends
const trend = tas.analyzeTrends(patternId, 'frontend-developer');

console.log(trend.direction);           // 'improving'
console.log(trend.slope);               // 0.023
console.log(trend.confidence);          // 0.89
console.log(trend.forecast);            // Array of future predictions
console.log(trend.anomalies);           // Detected anomalies
console.log(trend.seasonality);         // Seasonal pattern if detected
console.log(trend.recommendations);     // Actionable recommendations

// Detect anomalies
const anomalies = tas.detectAnomalies(patternId);

// Forecast performance
const forecast = tas.forecastPerformance(patternId);

// Detect change points
const changePoints = tas.detectChangePoints(patternId);

// Get learning rate recommendation
const adjustment = tas.recommendLearningRateAdjustment(patternId, currentRate);
```

**Forecasting Methods**:

*Linear Regression*:
- Uses least squares for trend line
- Best for steady trends
- R-squared for confidence

*Exponential Smoothing*:
- Weighted moving average
- Good for volatile data
- Configurable smoothing factor (α)

*Moving Average*:
- Simple average of recent window
- Robust to outliers
- Constant prediction

*Auto-Selection*:
- Analyzes data characteristics
- Chooses best method automatically
- Checks for exponential patterns and volatility

---

## Integration Example

Here's how to use all modules together in an agent:

```typescript
import {
  PatternRecognitionEngine,
  SuccessWeightingSystem,
  CrossAgentLearning,
  ReinforcementLearningModule,
  TrendAnalysisSystem,
} from './learning';

// Initialize all systems
const patternEngine = new PatternRecognitionEngine();
const weightingSystem = new SuccessWeightingSystem();
const crossAgentLearning = new CrossAgentLearning();
const reinforcementLearning = new ReinforcementLearningModule();
const trendAnalysis = new TrendAnalysisSystem();

// Agent execution cycle
async function executeAgentTask(agent: string, task: Task) {
  // 1. Extract patterns from history
  const actions = await getAgentHistory(agent);
  const sequences = patternEngine.extractSequences(actions, agent);
  const patterns = patternEngine.findCommonSubsequences(sequences);

  // 2. Weight patterns for decision making
  const weightedPatterns = patterns.map(seq => {
    // Convert sequence to pattern...
    const weight = weightingSystem.calculatePatternWeight(pattern, task.context);
    return { pattern, weight };
  });

  // 3. Check for cross-agent patterns
  const sharedPatterns = await getCrossAgentPatterns(agent);
  const compatiblePatterns = sharedPatterns.filter(p => {
    const compat = crossAgentLearning.checkCompatibility(p.sourceAgent, agent);
    return compat.compatible;
  });

  // 4. Select action using RL
  const state = buildState(task, agent);
  const availableActions = buildActions(weightedPatterns, compatiblePatterns);
  const selectedAction = reinforcementLearning.selectAction(state, availableActions, agent);

  // 5. Execute action
  const result = await executeAction(selectedAction);

  // 6. Calculate reward
  const reward = reinforcementLearning.shapeReward(
    result.success,
    result.timeSavedMs,
    result.qualityScore,
    result.isNovel,
    selectedAction.riskLevel
  );

  // 7. Update Q-values
  const nextState = buildState(task, agent);
  reinforcementLearning.updateQValue(state, selectedAction, reward, nextState, agent);

  // 8. Record for trend analysis
  trendAnalysis.recordDataPoint(selectedAction.patternId, result.successRate);

  // 9. Analyze trends periodically
  if (shouldAnalyzeTrends()) {
    const trend = trendAnalysis.analyzeTrends(selectedAction.patternId, agent);

    if (trend.direction === 'declining') {
      // Pattern degrading - investigate or replace
      console.warn(`Pattern ${selectedAction.patternId} is declining`);
    }

    // Adjust learning rate if needed
    const adjustment = trendAnalysis.recommendLearningRateAdjustment(
      selectedAction.patternId,
      reinforcementLearning.config.learning.learningRate
    );

    if (adjustment.recommendedRate !== adjustment.currentRate) {
      // Update learning rate
      reinforcementLearning.config.learning.learningRate = adjustment.recommendedRate;
    }
  }

  // 10. Share successful patterns
  if (result.success && result.successRate > 0.85) {
    crossAgentLearning.sharePattern(agent, pattern);
  }

  return result;
}
```

---

## Mathematical Foundations

### Pattern Recognition

**Cosine Similarity**:
```
similarity = (A · B) / (||A|| × ||B||)

where A and B are feature vectors
```

**Edit Distance (Levenshtein)**:
```
dp[i][j] = min(
  dp[i-1][j] + 1,      // deletion
  dp[i][j-1] + 1,      // insertion
  dp[i-1][j-1] + cost  // substitution
)

normalized = 1 - distance / max(len(A), len(B))
```

**Chi-Square Significance**:
```
χ² = Σ[(observed - expected)² / expected]

p-value ≈ e^(-χ²/2)
```

### Success Weighting

**Exponential Decay**:
```
weight = e^(-t/τ)

where τ = halfLife / ln(2)
```

**Wilson Score Interval**:
```
center = (p + z²/2n) / (1 + z²/n)
margin = z × sqrt((p(1-p)/n + z²/4n²)) / (1 + z²/n)

CI = [center - margin, center + margin]
```

### Reinforcement Learning

**Q-Learning Update**:
```
Q(s,a) ← Q(s,a) + α[r + γ max Q(s',a') - Q(s,a)]
              TD target    current Q
         ←---------------→
              TD error
```

**ε-Greedy Selection**:
```
action = random() < ε ? random_action() : argmax Q(s,a)
```

### Trend Analysis

**Linear Regression (Least Squares)**:
```
slope = (n∑xy - ∑x∑y) / (n∑x² - (∑x)²)

R² = 1 - SS_residual / SS_total
```

**Z-Score Anomaly Detection**:
```
z = (x - μ) / σ

anomaly if |z| > threshold (typically 3)
```

**Autocorrelation**:
```
r(k) = Σ[(x_i - μ)(x_{i+k} - μ)] / Σ[(x_i - μ)²]
```

---

## Performance Considerations

### Memory Usage

- **Pattern Recognition**: O(n²) for sequence extraction, caching recommended
- **Success Weighting**: O(1) per calculation, O(n) history storage
- **Cross-Agent Learning**: O(n × m) for n agents and m patterns
- **Reinforcement Learning**: O(s × a) for s states and a actions, pruning essential
- **Trend Analysis**: O(n) for n data points, sliding windows for large datasets

### Computational Complexity

- **Pattern Matching**: O(n × m) for n patterns and m features
- **Q-Value Update**: O(1) per update
- **Trend Forecasting**: O(n) for linear methods, O(n²) for advanced methods
- **Anomaly Detection**: O(w) for window size w

### Optimization Tips

1. **Enable Caching**: Pattern recognition benefits greatly from caching
2. **Prune Regularly**: Q-table and pattern storage need periodic pruning
3. **Batch Processing**: Use experience replay batches efficiently
4. **Lazy Loading**: Load historical data only when needed
5. **Compression**: Compress old data for storage efficiency

---

## Testing

Comprehensive test coverage includes:

- **Unit Tests**: Each module tested independently
- **Integration Tests**: Cross-module interactions
- **Performance Tests**: Scalability and efficiency
- **Edge Cases**: Boundary conditions and error handling

Run tests:
```bash
npm test                          # All tests
npm test SuccessWeighting        # Specific module
npm test -- --coverage           # With coverage report
```

---

## Future Enhancements

### Planned Features

1. **Neural Network Integration**: Deep RL for complex patterns
2. **Federated Learning**: Privacy-preserving cross-project learning
3. **Multi-Armed Bandits**: Contextual bandits for exploration
4. **Hierarchical RL**: Learn at multiple abstraction levels
5. **Meta-Learning**: Learn how to learn faster

### Research Areas

- **Transfer Learning**: Better cross-agent knowledge transfer
- **Curriculum Learning**: Progressive difficulty in learning
- **Imitation Learning**: Learn from expert demonstrations
- **Inverse RL**: Infer reward functions from behavior

---

## References

### Academic Papers

1. Sutton & Barto (2018): "Reinforcement Learning: An Introduction"
2. Watkins (1989): "Learning from Delayed Rewards" (Q-Learning)
3. Mnih et al. (2015): "Human-level control through deep RL"
4. Silver et al. (2016): "Mastering the game of Go with deep RL"

### Industry Applications

- AlphaGo: Multi-agent learning and self-play
- OpenAI Five: Distributed RL at scale
- Waymo: RL for autonomous driving
- Netflix: Contextual bandits for recommendations

---

## Contributing

When adding new algorithms:

1. **Document thoroughly**: Include mathematical foundations
2. **Test comprehensively**: Unit tests with >90% coverage
3. **Optimize carefully**: Profile before optimizing
4. **Maintain consistency**: Follow existing patterns
5. **Consider trade-offs**: Document complexity and limitations

---

## License

Part of the Loom Framework - MIT License

---

**Last Updated**: 2025-10-23
**Version**: 1.0.0
**Maintainers**: Loom Core Team
