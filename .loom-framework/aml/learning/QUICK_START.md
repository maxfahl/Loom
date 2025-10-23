# AML Learning Algorithms - Quick Start Guide

## 5-Minute Integration

### 1. Basic Setup

```typescript
import {
  PatternRecognitionEngine,
  SuccessWeightingSystem,
  CrossAgentLearning,
  ReinforcementLearningModule,
  TrendAnalysisSystem,
} from '@loom/aml/learning';

// Initialize with defaults
const learning = {
  patterns: new PatternRecognitionEngine(),
  weighting: new SuccessWeightingSystem(),
  crossAgent: new CrossAgentLearning(),
  rl: new ReinforcementLearningModule(),
  trends: new TrendAnalysisSystem(),
};
```

### 2. Pattern Recognition

```typescript
// Extract patterns from agent history
const actions = await getAgentHistory('frontend-developer');
const sequences = learning.patterns.extractSequences(actions, 'frontend-developer');
const commonPatterns = learning.patterns.findCommonSubsequences(sequences);

// Validate a pattern
const validation = learning.patterns.validatePattern(sequence, existingPatterns);
if (validation.valid) {
  // Pattern is statistically significant
  savePattern(sequence);
}
```

### 3. Success Weighting

```typescript
// Calculate weight for decision making
const weight = learning.weighting.calculatePatternWeight(
  pattern,
  currentContext,
  projectMetadata
);

if (weight.recommendationStrength === 'very-strong') {
  console.log(`High confidence: ${weight.totalWeight.toFixed(2)}`);
  console.log(`Factors: ${JSON.stringify(weight.factors)}`);
}

// Adjust thresholds dynamically
learning.weighting.adjustThresholds(patternId);
```

### 4. Cross-Agent Learning

```typescript
// Register agents
learning.crossAgent.registerAgent({
  name: 'frontend-developer',
  capabilities: ['react', 'typescript'],
  domains: ['frontend'],
  focusAreas: ['performance'],
  complexity: 'advanced',
  learningRate: 0.15,
});

// Check compatibility
const compat = learning.crossAgent.checkCompatibility('frontend-dev', 'backend-dev');

// Share pattern if compatible
if (compat.compatible) {
  const adapted = learning.crossAgent.adaptPattern(pattern, 'source', 'target');
}
```

### 5. Reinforcement Learning

```typescript
// Select action
const action = learning.rl.selectAction(
  state,
  availableActions,
  'frontend-developer'
);

// Execute and get result...

// Shape reward
const reward = learning.rl.shapeReward(
  result.success,
  result.timeSavedMs,
  result.qualityScore,
  result.isNovel,
  action.riskLevel
);

// Update Q-values
learning.rl.updateQValue(state, action, reward, nextState, 'frontend-developer');
```

### 6. Trend Analysis

```typescript
// Record performance over time
learning.trends.recordDataPoint(patternId, successRate);

// Analyze trends
const trend = learning.trends.analyzeTrends(patternId, 'frontend-developer');

if (trend.direction === 'declining') {
  console.warn(`Pattern ${patternId} performance declining`);
  console.log('Recommendations:', trend.recommendations);
}

// Get learning rate suggestion
const adjustment = learning.trends.recommendLearningRateAdjustment(
  patternId,
  currentRate
);
```

---

## Common Patterns

### Pattern Discovery Loop

```typescript
async function discoverPatterns(agentName: string) {
  // 1. Get history
  const actions = await getAgentHistory(agentName);

  // 2. Extract sequences
  const sequences = learning.patterns.extractSequences(actions, agentName);

  // 3. Find common patterns
  const common = learning.patterns.findCommonSubsequences(sequences);

  // 4. Validate and save
  for (const seq of common) {
    const validation = learning.patterns.validatePattern(seq, existingPatterns);

    if (validation.valid && validation.pValue < 0.05) {
      const pattern = convertToPattern(seq);
      await savePattern(pattern);
    }
  }
}
```

### Weighted Decision Making

```typescript
async function selectBestPattern(
  patterns: Pattern[],
  context: Context
): Promise<Pattern> {
  // Calculate weights
  const weighted = patterns.map((pattern) => ({
    pattern,
    weight: learning.weighting.calculatePatternWeight(pattern, context),
  }));

  // Sort by total weight
  weighted.sort((a, b) => b.weight.totalWeight - a.weight.totalWeight);

  // Return best with high confidence
  const best = weighted[0];
  if (best.weight.recommendationStrength === 'weak') {
    console.warn('Low confidence in best pattern');
  }

  return best.pattern;
}
```

### Cross-Agent Pattern Sharing

```typescript
async function shareSuccessfulPattern(
  sourceAgent: string,
  pattern: Pattern
): Promise<void> {
  // Check if pattern is successful enough
  if (pattern.metrics.successRate < 0.85) {
    return; // Not successful enough
  }

  // Share with compatible agents
  const shared = learning.crossAgent.sharePattern(sourceAgent, pattern);

  console.log(`Shared with ${shared.length} agents`);

  // Store adapted patterns
  for (const adapted of shared) {
    await saveAdaptedPattern(adapted);
  }
}
```

### RL Training Loop

```typescript
async function trainAgent(agentName: string, episodes: number): Promise<void> {
  for (let episode = 0; episode < episodes; episode++) {
    let state = await getInitialState();

    while (!isTerminal(state)) {
      // Select action
      const actions = await getAvailableActions(state);
      const action = learning.rl.selectAction(state, actions, agentName);

      // Execute
      const result = await executeAction(action);
      const nextState = await getNextState(result);

      // Calculate reward
      const reward = learning.rl.shapeReward(
        result.success,
        result.timeSavedMs,
        result.qualityScore,
        result.isNovel,
        action.riskLevel
      );

      // Update Q-values
      learning.rl.updateQValue(state, action, reward, nextState, agentName);

      state = nextState;
    }

    // Decay epsilon
    if (episode % 10 === 0) {
      const stats = learning.rl.getStatistics(agentName);
      console.log(`Episode ${episode}: ${stats.avgPerformance.toFixed(2)}`);
    }
  }
}
```

### Performance Monitoring

```typescript
async function monitorPatternPerformance(patternId: string): Promise<void> {
  // Record latest performance
  const pattern = await getPattern(patternId);
  learning.trends.recordDataPoint(patternId, pattern.metrics.successRate);

  // Analyze trends
  const trend = learning.trends.analyzeTrends(patternId);

  if (!trend) return;

  // Check for issues
  if (trend.direction === 'declining') {
    await alertTeam(`Pattern ${patternId} declining`);
  }

  // Check for anomalies
  const anomalies = trend.anomalies.filter((a) => a.severity === 'critical');
  if (anomalies.length > 0) {
    await investigateAnomalies(patternId, anomalies);
  }

  // Adjust learning rate if needed
  const adjustment = learning.trends.recommendLearningRateAdjustment(
    patternId,
    currentRate
  );

  if (Math.abs(adjustment.recommendedRate - adjustment.currentRate) > 0.05) {
    await updateLearningRate(patternId, adjustment.recommendedRate);
  }
}
```

---

## Configuration Presets

### Development (Fast Learning)

```typescript
const devConfig = {
  patterns: {
    minFrequency: 2,
    minSimilarity: 0.6,
    significanceThreshold: 0.1,
  },
  weighting: {
    recency: { halfLifeDays: 15 }, // Recent patterns preferred
  },
  rl: {
    exploration: { epsilon: 0.3 }, // High exploration
    learning: { learningRate: 0.2 }, // Fast learning
  },
  trends: {
    anomaly: { sensitivityLevel: 'high' }, // Catch all issues
  },
};
```

### Production (Stable)

```typescript
const prodConfig = {
  patterns: {
    minFrequency: 5,
    minSimilarity: 0.8,
    significanceThreshold: 0.01,
  },
  weighting: {
    recency: { halfLifeDays: 30 },
  },
  rl: {
    exploration: { epsilon: 0.1 },
    learning: { learningRate: 0.05 },
  },
  trends: {
    anomaly: { sensitivityLevel: 'low' },
  },
};
```

### Testing (Reproducible)

```typescript
const testConfig = {
  patterns: {
    minFrequency: 3,
    minSimilarity: 0.7,
  },
  weighting: {
    thresholds: { enabled: false }, // No dynamic adjustment
  },
  rl: {
    exploration: { epsilon: 0 }, // No exploration (deterministic)
    replay: { enabled: false }, // No experience replay
  },
  trends: {
    forecast: { method: 'linear' }, // Deterministic forecasting
  },
};
```

---

## Debugging

### Enable Verbose Logging

```typescript
// Add to each module
const config = {
  debug: true,
  logLevel: 'verbose',
};
```

### Inspect Internal State

```typescript
// Pattern Recognition
console.log('Cache size:', learning.patterns.sequenceCache.size);
learning.patterns.clearCache(); // Clear if too large

// Success Weighting
const history = learning.weighting.getPerformanceHistory(patternId);
console.log('Performance history:', history);

// RL Module
const stats = learning.rl.getStatistics(agentName);
console.log('RL stats:', stats);

// Trend Analysis
const anomalies = learning.trends.getAnomalies(patternId);
console.log('Anomalies:', anomalies);
```

### Export/Import State

```typescript
// Export Q-table for inspection
const qTable = learning.rl.exportQTable();
fs.writeFileSync('q-table.json', JSON.stringify(qTable, null, 2));

// Import Q-table
const loaded = JSON.parse(fs.readFileSync('q-table.json'));
learning.rl.importQTable(loaded);
```

---

## Performance Tips

### 1. Enable Caching

```typescript
// Pattern recognition benefits most
const patterns = new PatternRecognitionEngine({
  cacheSize: 1000, // Cache common queries
});
```

### 2. Prune Regularly

```typescript
// RL module prunes automatically, but can trigger manually
if (learning.rl.getStatistics().qTableSize > 50000) {
  learning.rl.pruneQTable();
}
```

### 3. Batch Operations

```typescript
// Process multiple patterns at once
const weights = patterns.map((p) =>
  learning.weighting.calculatePatternWeight(p, context)
);
```

### 4. Lazy Load History

```typescript
// Only load when needed
const trend = learning.trends.analyzeTrends(patternId);
if (trend && trend.direction === 'declining') {
  const fullHistory = await loadFullHistory(patternId);
}
```

### 5. Use Indexes

```typescript
// Create pattern indexes for fast lookup
const patternIndex = new Map<string, Pattern>();
for (const pattern of patterns) {
  patternIndex.set(pattern.id, pattern);
}
```

---

## Common Issues

### Issue: Patterns Not Being Detected

**Solution**: Lower thresholds

```typescript
const config = {
  minFrequency: 2, // Was 3
  minSimilarity: 0.6, // Was 0.7
  significanceThreshold: 0.1, // Was 0.05
};
```

### Issue: Too Many False Positives

**Solution**: Raise thresholds

```typescript
const config = {
  minFrequency: 5,
  minSimilarity: 0.8,
  significanceThreshold: 0.01,
};
```

### Issue: RL Not Learning

**Solution**: Increase exploration

```typescript
const config = {
  exploration: {
    epsilon: 0.3, // Was 0.2
    epsilonDecay: 0.999, // Slower decay
  },
  learning: {
    learningRate: 0.15, // Was 0.1
  },
};
```

### Issue: Memory Usage Too High

**Solution**: Enable pruning

```typescript
const config = {
  qtable: {
    maxSize: 50000, // Reduce
    pruneThreshold: 0.2, // Increase
    pruneInterval: 500, // More frequent
  },
};
```

### Issue: Anomalies Everywhere

**Solution**: Reduce sensitivity

```typescript
const config = {
  anomaly: {
    sensitivityLevel: 'low',
    stdDevThreshold: 4.0, // Was 3.0
  },
};
```

---

## Next Steps

1. **Read Full Documentation**: See `README.md` for complete details
2. **Run Tests**: `npm test` to verify setup
3. **Try Examples**: Use patterns above in your code
4. **Monitor Performance**: Track metrics from day one
5. **Tune Configuration**: Adjust based on your use case

---

## Support

- **Documentation**: `.loom-framework/aml/learning/README.md`
- **Implementation Plan**: `/tmp/AML_IMPLEMENTATION_PLAN.md`
- **Phase Summary**: `/tmp/LEARNING_ALGORITHMS_SUMMARY.md`

---

**Last Updated**: 2025-10-23
**Version**: 1.0.0
