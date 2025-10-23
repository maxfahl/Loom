/**
 * Learning Algorithms Module Index
 *
 * Exports all learning algorithm components for the AML system
 */

// Pattern Recognition
export {
  PatternRecognitionEngine,
  type AgentAction,
  type ActionSequence,
  type PatternMatch,
  type PatternRecognitionConfig,
} from './PatternRecognition';

// Success Weighting
export {
  SuccessWeightingSystem,
  type WeightResult,
  type SuccessWeightingConfig,
} from './SuccessWeighting';

// Cross-Agent Learning
export {
  CrossAgentLearning,
  type AgentProfile,
  type CompatibilityResult,
  type AdaptedPattern,
  type SharingRecord,
  type PatternConflict,
  type ConsensusResult,
  type CrossAgentLearningConfig,
} from './CrossAgentLearning';

// Reinforcement Learning
export {
  ReinforcementLearningModule,
  type State,
  type Action,
  type Reward,
  type Experience,
  type ReinforcementLearningConfig,
} from './ReinforcementLearning';

// Trend Analysis
export {
  TrendAnalysisSystem,
  type DataPoint,
  type TrendResult,
  type AnomalyDetection,
  type SeasonalPattern,
  type ChangePoint,
  type LearningRateAdjustment,
  type PerformanceForecast,
  type TrendAnalysisConfig,
} from './TrendAnalysis';
