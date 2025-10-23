/**
 * Trend Analysis Module - Detects performance patterns, anomalies, and forecasts
 *
 * This module implements:
 * - Anomaly detection for pattern degradation
 * - Performance trend forecasting using time series analysis
 * - Seasonal pattern recognition
 * - Adaptive learning rate adjustment
 * - Change point detection
 * - Predictive maintenance for patterns
 */

import { Pattern } from '../models/Pattern';
import { AgentName } from '../types/common';

/**
 * Time series data point
 */
export interface DataPoint {
  timestamp: string;
  value: number;
  metadata?: Record<string, unknown>;
}

/**
 * Trend analysis result
 */
export interface TrendResult {
  direction: 'improving' | 'stable' | 'declining' | 'volatile';
  slope: number; // Rate of change
  confidence: number; // 0-1
  forecast: DataPoint[]; // Future predictions
  anomalies: AnomalyDetection[];
  seasonality?: SeasonalPattern;
  recommendations: string[];
}

/**
 * Anomaly detection result
 */
export interface AnomalyDetection {
  timestamp: string;
  actualValue: number;
  expectedValue: number;
  deviation: number; // Standard deviations from expected
  severity: 'low' | 'medium' | 'high' | 'critical';
  type: 'spike' | 'drop' | 'shift' | 'outlier';
  potentialCauses?: string[];
}

/**
 * Seasonal pattern
 */
export interface SeasonalPattern {
  detected: boolean;
  period: number; // In time units
  amplitude: number;
  phase: number;
  confidence: number;
}

/**
 * Change point detection result
 */
export interface ChangePoint {
  timestamp: string;
  beforeMean: number;
  afterMean: number;
  significance: number; // p-value
  type: 'improvement' | 'degradation' | 'shift';
}

/**
 * Adaptive learning rate recommendation
 */
export interface LearningRateAdjustment {
  currentRate: number;
  recommendedRate: number;
  rationale: string;
  confidence: number;
  expectedImpact: string;
}

/**
 * Performance forecast
 */
export interface PerformanceForecast {
  horizon: number; // How many time steps ahead
  predictions: DataPoint[];
  confidenceIntervals: Array<{ lower: number; upper: number }>;
  method: 'linear' | 'exponential' | 'moving-average' | 'arima';
  accuracy: number; // Historical accuracy
}

/**
 * Configuration for trend analysis
 */
export interface TrendAnalysisConfig {
  // Anomaly detection
  anomaly: {
    sensitivityLevel: 'low' | 'medium' | 'high'; // How easily to flag anomalies
    windowSize: number; // Rolling window for baseline calculation
    stdDevThreshold: number; // Standard deviations for anomaly (default: 3.0)
    minDataPoints: number; // Minimum data for detection (default: 10)
  };

  // Trend detection
  trend: {
    windowSize: number; // Window for trend calculation (default: 20)
    smoothingFactor: number; // Exponential smoothing alpha (default: 0.3)
    significanceThreshold: number; // p-value for significance (default: 0.05)
  };

  // Forecasting
  forecast: {
    horizonSteps: number; // How far to forecast (default: 10)
    method: 'linear' | 'exponential' | 'moving-average' | 'auto'; // Default: auto
    confidenceLevel: number; // Confidence interval (default: 0.95)
  };

  // Seasonality detection
  seasonality: {
    enabled: boolean; // Enable seasonality detection (default: true)
    minPeriod: number; // Minimum period to check (default: 7)
    maxPeriod: number; // Maximum period to check (default: 30)
    significanceThreshold: number; // Threshold for detection (default: 0.7)
  };

  // Learning rate adaptation
  learningRate: {
    minRate: number; // Minimum learning rate (default: 0.01)
    maxRate: number; // Maximum learning rate (default: 0.5)
    adjustmentFactor: number; // How much to adjust (default: 0.1)
    stabilityWindow: number; // Window for stability check (default: 10)
  };
}

/**
 * Default configuration
 */
const DEFAULT_CONFIG: TrendAnalysisConfig = {
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
    method: 'auto',
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

/**
 * Trend Analysis System
 *
 * Philosophy:
 * - Patterns degrade over time as codebases evolve
 * - Early detection prevents costly failures
 * - Trends reveal underlying system dynamics
 * - Adaptive learning rates optimize convergence
 * - Seasonality matters in development patterns
 */
export class TrendAnalysisSystem {
  private config: TrendAnalysisConfig;
  private historicalData: Map<string, DataPoint[]>; // patternId -> time series
  private detectedAnomalies: Map<string, AnomalyDetection[]>;
  private changePoints: Map<string, ChangePoint[]>;
  private forecastCache: Map<string, PerformanceForecast>;

  constructor(config: Partial<TrendAnalysisConfig> = {}) {
    this.config = this.mergeConfig(config);
    this.historicalData = new Map();
    this.detectedAnomalies = new Map();
    this.changePoints = new Map();
    this.forecastCache = new Map();
  }

  /**
   * Add data point to time series
   */
  recordDataPoint(patternId: string, value: number, metadata?: Record<string, unknown>): void {
    if (!this.historicalData.has(patternId)) {
      this.historicalData.set(patternId, []);
    }

    const dataPoint: DataPoint = {
      timestamp: new Date().toISOString(),
      value,
      metadata,
    };

    this.historicalData.get(patternId)!.push(dataPoint);

    // Invalidate forecast cache
    this.forecastCache.delete(patternId);
  }

  /**
   * Analyze trends for a pattern
   *
   * Combines multiple analysis techniques:
   * - Linear regression for trend direction
   * - Moving average for smoothing
   * - Standard deviation for volatility
   * - Forecasting for future performance
   */
  analyzeTrends(patternId: string, agentName?: AgentName): TrendResult | null {
    const data = this.historicalData.get(patternId);

    if (!data || data.length < this.config.anomaly.minDataPoints) {
      return null;
    }

    // Calculate trend using linear regression
    const { slope, confidence } = this.calculateLinearTrend(data);

    // Determine direction
    let direction: 'improving' | 'stable' | 'declining' | 'volatile';
    const volatility = this.calculateVolatility(data);

    if (volatility > 0.3) {
      direction = 'volatile';
    } else if (slope > 0.01) {
      direction = 'improving';
    } else if (slope < -0.01) {
      direction = 'declining';
    } else {
      direction = 'stable';
    }

    // Detect anomalies
    const anomalies = this.detectAnomalies(patternId, data);

    // Forecast future performance
    const forecast = this.forecastPerformance(patternId, data);

    // Detect seasonality
    const seasonality = this.config.seasonality.enabled
      ? this.detectSeasonality(data)
      : undefined;

    // Generate recommendations
    const recommendations = this.generateRecommendations(
      direction,
      slope,
      anomalies,
      volatility,
      seasonality
    );

    return {
      direction,
      slope,
      confidence,
      forecast: forecast.predictions,
      anomalies,
      seasonality,
      recommendations,
    };
  }

  /**
   * Detect anomalies in pattern performance
   *
   * Uses statistical methods:
   * - Z-score for outlier detection
   * - Moving average for baseline
   * - Interquartile range for robust detection
   */
  detectAnomalies(patternId: string, data?: DataPoint[]): AnomalyDetection[] {
    const timeSeries = data || this.historicalData.get(patternId);

    if (!timeSeries || timeSeries.length < this.config.anomaly.minDataPoints) {
      return [];
    }

    const anomalies: AnomalyDetection[] = [];
    const windowSize = this.config.anomaly.windowSize;

    // Calculate rolling statistics
    for (let i = windowSize; i < timeSeries.length; i++) {
      const window = timeSeries.slice(i - windowSize, i);
      const currentPoint = timeSeries[i];

      const mean = this.calculateMean(window.map((d) => d.value));
      const stdDev = this.calculateStdDev(window.map((d) => d.value), mean);

      // Z-score
      const zScore = stdDev === 0 ? 0 : (currentPoint.value - mean) / stdDev;

      // Adjust threshold based on sensitivity
      const threshold = this.getAnomalyThreshold();

      if (Math.abs(zScore) > threshold) {
        const deviation = Math.abs(zScore);

        // Determine severity
        let severity: 'low' | 'medium' | 'high' | 'critical';
        if (deviation > threshold * 2) severity = 'critical';
        else if (deviation > threshold * 1.5) severity = 'high';
        else if (deviation > threshold * 1.2) severity = 'medium';
        else severity = 'low';

        // Determine type
        let type: 'spike' | 'drop' | 'shift' | 'outlier';
        if (zScore > threshold) {
          type = deviation > threshold * 1.5 ? 'spike' : 'outlier';
        } else {
          type = deviation > threshold * 1.5 ? 'drop' : 'outlier';
        }

        // Check for persistent shift
        if (i < timeSeries.length - 3) {
          const next3 = timeSeries.slice(i + 1, i + 4);
          const next3Mean = this.calculateMean(next3.map((d) => d.value));
          if (Math.abs(next3Mean - mean) / stdDev > threshold * 0.5) {
            type = 'shift';
          }
        }

        const anomaly: AnomalyDetection = {
          timestamp: currentPoint.timestamp,
          actualValue: currentPoint.value,
          expectedValue: mean,
          deviation,
          severity,
          type,
          potentialCauses: this.inferAnomalyCauses(type, severity, currentPoint.metadata),
        };

        anomalies.push(anomaly);
      }
    }

    // Store for reference
    this.detectedAnomalies.set(patternId, anomalies);

    return anomalies;
  }

  /**
   * Forecast future performance
   *
   * Uses appropriate method based on data characteristics
   */
  forecastPerformance(patternId: string, data?: DataPoint[]): PerformanceForecast {
    // Check cache first
    if (this.forecastCache.has(patternId)) {
      const cached = this.forecastCache.get(patternId)!;
      // Cache valid for 1 hour
      const cacheAge = Date.now() - new Date(cached.predictions[0]?.timestamp || 0).getTime();
      if (cacheAge < 3600000) {
        return cached;
      }
    }

    const timeSeries = data || this.historicalData.get(patternId);

    if (!timeSeries || timeSeries.length < this.config.anomaly.minDataPoints) {
      return this.getEmptyForecast();
    }

    // Auto-select method if configured
    let method = this.config.forecast.method;
    if (method === 'auto') {
      method = this.selectForecastMethod(timeSeries);
    }

    // Generate forecast based on method
    let forecast: PerformanceForecast;

    switch (method) {
      case 'linear':
        forecast = this.linearForecast(timeSeries);
        break;
      case 'exponential':
        forecast = this.exponentialForecast(timeSeries);
        break;
      case 'moving-average':
        forecast = this.movingAverageForecast(timeSeries);
        break;
      default:
        forecast = this.linearForecast(timeSeries);
    }

    // Cache result
    this.forecastCache.set(patternId, forecast);

    return forecast;
  }

  /**
   * Detect seasonal patterns
   *
   * Uses autocorrelation to find repeating patterns
   */
  detectSeasonality(data: DataPoint[]): SeasonalPattern | undefined {
    if (data.length < this.config.seasonality.maxPeriod * 2) {
      return undefined;
    }

    const values = data.map((d) => d.value);
    let maxCorrelation = 0;
    let bestPeriod = 0;

    // Test different periods
    for (
      let period = this.config.seasonality.minPeriod;
      period <= this.config.seasonality.maxPeriod;
      period++
    ) {
      const correlation = this.calculateAutocorrelation(values, period);

      if (correlation > maxCorrelation) {
        maxCorrelation = correlation;
        bestPeriod = period;
      }
    }

    // Check if significant
    if (maxCorrelation < this.config.seasonality.significanceThreshold) {
      return {
        detected: false,
        period: 0,
        amplitude: 0,
        phase: 0,
        confidence: maxCorrelation,
      };
    }

    // Calculate amplitude and phase
    const { amplitude, phase } = this.calculateSeasonalComponents(values, bestPeriod);

    return {
      detected: true,
      period: bestPeriod,
      amplitude,
      phase,
      confidence: maxCorrelation,
    };
  }

  /**
   * Detect change points (significant regime changes)
   *
   * Uses cumulative sum (CUSUM) algorithm
   */
  detectChangePoints(patternId: string): ChangePoint[] {
    const data = this.historicalData.get(patternId);

    if (!data || data.length < this.config.trend.windowSize * 2) {
      return [];
    }

    const changePoints: ChangePoint[] = [];
    const values = data.map((d) => d.value);
    const mean = this.calculateMean(values);
    const stdDev = this.calculateStdDev(values, mean);

    // CUSUM algorithm
    let cumSum = 0;
    const threshold = stdDev * 4; // Sensitivity threshold

    for (let i = 1; i < values.length; i++) {
      cumSum += values[i] - mean;

      if (Math.abs(cumSum) > threshold) {
        // Potential change point detected
        const windowBefore = values.slice(Math.max(0, i - 10), i);
        const windowAfter = values.slice(i, Math.min(values.length, i + 10));

        const beforeMean = this.calculateMean(windowBefore);
        const afterMean = this.calculateMean(windowAfter);

        // Significance test (t-test approximation)
        const significance = this.calculateSignificance(windowBefore, windowAfter);

        if (significance < this.config.trend.significanceThreshold) {
          const type: 'improvement' | 'degradation' | 'shift' =
            afterMean > beforeMean ? 'improvement' : afterMean < beforeMean ? 'degradation' : 'shift';

          changePoints.push({
            timestamp: data[i].timestamp,
            beforeMean,
            afterMean,
            significance,
            type,
          });

          // Reset cumulative sum
          cumSum = 0;
        }
      }
    }

    this.changePoints.set(patternId, changePoints);
    return changePoints;
  }

  /**
   * Recommend adaptive learning rate adjustments
   *
   * Based on:
   * - Performance stability
   * - Trend direction
   * - Volatility
   * - Recent anomalies
   */
  recommendLearningRateAdjustment(
    patternId: string,
    currentRate: number
  ): LearningRateAdjustment {
    const trend = this.analyzeTrends(patternId);

    if (!trend) {
      return {
        currentRate,
        recommendedRate: currentRate,
        rationale: 'Insufficient data for adjustment',
        confidence: 0,
        expectedImpact: 'none',
      };
    }

    let recommendedRate = currentRate;
    let rationale = '';
    let expectedImpact = '';

    // Adjust based on trend direction
    if (trend.direction === 'declining') {
      // Increase learning rate to adapt faster
      recommendedRate = Math.min(
        this.config.learningRate.maxRate,
        currentRate * (1 + this.config.learningRate.adjustmentFactor)
      );
      rationale = 'Performance declining - increase learning rate to adapt faster';
      expectedImpact = 'Faster adaptation to changing patterns';
    } else if (trend.direction === 'improving') {
      // Decrease learning rate to preserve gains
      recommendedRate = Math.max(
        this.config.learningRate.minRate,
        currentRate * (1 - this.config.learningRate.adjustmentFactor * 0.5)
      );
      rationale = 'Performance improving - decrease learning rate to stabilize';
      expectedImpact = 'More stable performance, preserve improvements';
    } else if (trend.direction === 'volatile') {
      // Increase rate slightly to find stability
      recommendedRate = Math.min(
        this.config.learningRate.maxRate,
        currentRate * (1 + this.config.learningRate.adjustmentFactor * 0.5)
      );
      rationale = 'Performance volatile - adjust learning rate to find optimal point';
      expectedImpact = 'Reduced volatility, more consistent performance';
    } else {
      // Stable - maintain current rate
      rationale = 'Performance stable - maintain current learning rate';
      expectedImpact = 'Continued stable performance';
    }

    // Adjust for recent anomalies
    if (trend.anomalies.length > 0) {
      const recentAnomalies = trend.anomalies.slice(-3);
      const criticalAnomalies = recentAnomalies.filter((a) => a.severity === 'critical');

      if (criticalAnomalies.length > 0) {
        recommendedRate = Math.min(
          this.config.learningRate.maxRate,
          recommendedRate * 1.2
        );
        rationale += '. Critical anomalies detected - increase rate for faster recovery';
      }
    }

    return {
      currentRate,
      recommendedRate,
      rationale,
      confidence: trend.confidence,
      expectedImpact,
    };
  }

  /**
   * Get all detected anomalies for a pattern
   */
  getAnomalies(patternId: string): AnomalyDetection[] {
    return this.detectedAnomalies.get(patternId) || [];
  }

  /**
   * Get all detected change points
   */
  getChangePoints(patternId: string): ChangePoint[] {
    return this.changePoints.get(patternId) || [];
  }

  /**
   * Clear historical data for a pattern
   */
  clearHistory(patternId: string): void {
    this.historicalData.delete(patternId);
    this.detectedAnomalies.delete(patternId);
    this.changePoints.delete(patternId);
    this.forecastCache.delete(patternId);
  }

  // ============================================================================
  // Private Helper Methods
  // ============================================================================

  /**
   * Calculate linear trend using least squares regression
   */
  private calculateLinearTrend(data: DataPoint[]): { slope: number; confidence: number } {
    const n = data.length;
    const x = data.map((_, i) => i);
    const y = data.map((d) => d.value);

    const sumX = x.reduce((a, b) => a + b, 0);
    const sumY = y.reduce((a, b) => a + b, 0);
    const sumXY = x.reduce((sum, xi, i) => sum + xi * y[i], 0);
    const sumX2 = x.reduce((sum, xi) => sum + xi * xi, 0);

    const slope = (n * sumXY - sumX * sumY) / (n * sumX2 - sumX * sumX);

    // Calculate R-squared for confidence
    const yMean = sumY / n;
    const yPred = x.map((xi) => slope * xi + (sumY - slope * sumX) / n);
    const ssTotal = y.reduce((sum, yi) => sum + Math.pow(yi - yMean, 2), 0);
    const ssResidual = y.reduce((sum, yi, i) => sum + Math.pow(yi - yPred[i], 2), 0);
    const rSquared = 1 - ssResidual / ssTotal;

    return {
      slope,
      confidence: Math.max(0, Math.min(1, rSquared)),
    };
  }

  /**
   * Calculate volatility (standard deviation / mean)
   */
  private calculateVolatility(data: DataPoint[]): number {
    const values = data.map((d) => d.value);
    const mean = this.calculateMean(values);
    const stdDev = this.calculateStdDev(values, mean);

    return mean === 0 ? 0 : stdDev / Math.abs(mean);
  }

  /**
   * Get anomaly threshold based on sensitivity
   */
  private getAnomalyThreshold(): number {
    const sensitivity = this.config.anomaly.sensitivityLevel;
    const baseThreshold = this.config.anomaly.stdDevThreshold;

    switch (sensitivity) {
      case 'low':
        return baseThreshold * 1.5; // More conservative
      case 'high':
        return baseThreshold * 0.7; // More aggressive
      default:
        return baseThreshold;
    }
  }

  /**
   * Infer potential causes of anomalies
   */
  private inferAnomalyCauses(
    type: string,
    severity: string,
    metadata?: Record<string, unknown>
  ): string[] {
    const causes: string[] = [];

    if (type === 'drop' || type === 'spike') {
      causes.push('Sudden code change or deployment');
      causes.push('Environmental change (dependencies, infrastructure)');
    }

    if (type === 'shift') {
      causes.push('Systematic change in codebase');
      causes.push('Pattern becoming obsolete');
    }

    if (severity === 'critical') {
      causes.push('Breaking change in dependencies');
      causes.push('Major refactoring affecting pattern applicability');
    }

    // Add metadata-based causes if available
    if (metadata?.framework) {
      causes.push(`Framework update: ${metadata.framework}`);
    }

    return causes;
  }

  /**
   * Select best forecast method based on data characteristics
   */
  private selectForecastMethod(
    data: DataPoint[]
  ): 'linear' | 'exponential' | 'moving-average' {
    const values = data.map((d) => d.value);

    // Check for exponential growth/decay
    const ratios: number[] = [];
    for (let i = 1; i < values.length; i++) {
      if (values[i - 1] !== 0) {
        ratios.push(values[i] / values[i - 1]);
      }
    }

    const ratioStdDev = this.calculateStdDev(
      ratios,
      this.calculateMean(ratios)
    );

    if (ratioStdDev < 0.1) {
      // Consistent ratio suggests exponential
      return 'exponential';
    }

    // Check volatility
    const volatility = this.calculateVolatility(data);

    if (volatility > 0.3) {
      // High volatility - use moving average
      return 'moving-average';
    }

    // Default to linear
    return 'linear';
  }

  /**
   * Linear forecast
   */
  private linearForecast(data: DataPoint[]): PerformanceForecast {
    const { slope } = this.calculateLinearTrend(data);
    const lastValue = data[data.length - 1].value;
    const lastTime = new Date(data[data.length - 1].timestamp).getTime();

    const predictions: DataPoint[] = [];
    const confidenceIntervals: Array<{ lower: number; upper: number }> = [];

    // Calculate confidence interval width
    const stdDev = this.calculateStdDev(
      data.map((d) => d.value),
      this.calculateMean(data.map((d) => d.value))
    );

    for (let i = 1; i <= this.config.forecast.horizonSteps; i++) {
      const predictedValue = lastValue + slope * i;
      const intervalWidth = stdDev * 1.96 * Math.sqrt(i); // 95% CI

      predictions.push({
        timestamp: new Date(lastTime + i * 86400000).toISOString(), // Daily
        value: predictedValue,
      });

      confidenceIntervals.push({
        lower: predictedValue - intervalWidth,
        upper: predictedValue + intervalWidth,
      });
    }

    return {
      horizon: this.config.forecast.horizonSteps,
      predictions,
      confidenceIntervals,
      method: 'linear',
      accuracy: 0.8, // Simplified
    };
  }

  /**
   * Exponential forecast
   */
  private exponentialForecast(data: DataPoint[]): PerformanceForecast {
    const alpha = this.config.trend.smoothingFactor;
    let smoothed = data[0].value;

    // Calculate exponentially weighted moving average
    for (let i = 1; i < data.length; i++) {
      smoothed = alpha * data[i].value + (1 - alpha) * smoothed;
    }

    const lastTime = new Date(data[data.length - 1].timestamp).getTime();
    const predictions: DataPoint[] = [];
    const confidenceIntervals: Array<{ lower: number; upper: number }> = [];

    for (let i = 1; i <= this.config.forecast.horizonSteps; i++) {
      predictions.push({
        timestamp: new Date(lastTime + i * 86400000).toISOString(),
        value: smoothed,
      });

      confidenceIntervals.push({
        lower: smoothed * 0.9,
        upper: smoothed * 1.1,
      });
    }

    return {
      horizon: this.config.forecast.horizonSteps,
      predictions,
      confidenceIntervals,
      method: 'exponential',
      accuracy: 0.75,
    };
  }

  /**
   * Moving average forecast
   */
  private movingAverageForecast(data: DataPoint[]): PerformanceForecast {
    const windowSize = Math.min(this.config.trend.windowSize, data.length);
    const recentData = data.slice(-windowSize);
    const average = this.calculateMean(recentData.map((d) => d.value));

    const lastTime = new Date(data[data.length - 1].timestamp).getTime();
    const predictions: DataPoint[] = [];
    const confidenceIntervals: Array<{ lower: number; upper: number }> = [];

    const stdDev = this.calculateStdDev(
      recentData.map((d) => d.value),
      average
    );

    for (let i = 1; i <= this.config.forecast.horizonSteps; i++) {
      predictions.push({
        timestamp: new Date(lastTime + i * 86400000).toISOString(),
        value: average,
      });

      confidenceIntervals.push({
        lower: average - stdDev * 1.96,
        upper: average + stdDev * 1.96,
      });
    }

    return {
      horizon: this.config.forecast.horizonSteps,
      predictions,
      confidenceIntervals,
      method: 'moving-average',
      accuracy: 0.7,
    };
  }

  /**
   * Calculate autocorrelation for lag
   */
  private calculateAutocorrelation(values: number[], lag: number): number {
    if (lag >= values.length) return 0;

    const mean = this.calculateMean(values);
    let numerator = 0;
    let denominator = 0;

    for (let i = 0; i < values.length - lag; i++) {
      numerator += (values[i] - mean) * (values[i + lag] - mean);
    }

    for (let i = 0; i < values.length; i++) {
      denominator += Math.pow(values[i] - mean, 2);
    }

    return denominator === 0 ? 0 : numerator / denominator;
  }

  /**
   * Calculate seasonal amplitude and phase
   */
  private calculateSeasonalComponents(
    values: number[],
    period: number
  ): { amplitude: number; phase: number } {
    // Simplified calculation
    const cycles = Math.floor(values.length / period);
    let maxDiff = 0;

    for (let i = 0; i < cycles; i++) {
      const cycle = values.slice(i * period, (i + 1) * period);
      const max = Math.max(...cycle);
      const min = Math.min(...cycle);
      maxDiff = Math.max(maxDiff, max - min);
    }

    return {
      amplitude: maxDiff / 2,
      phase: 0, // Simplified
    };
  }

  /**
   * Calculate statistical significance (simplified t-test)
   */
  private calculateSignificance(sample1: number[], sample2: number[]): number {
    const mean1 = this.calculateMean(sample1);
    const mean2 = this.calculateMean(sample2);
    const stdDev1 = this.calculateStdDev(sample1, mean1);
    const stdDev2 = this.calculateStdDev(sample2, mean2);

    const n1 = sample1.length;
    const n2 = sample2.length;

    const pooledStdDev = Math.sqrt(
      (stdDev1 * stdDev1) / n1 + (stdDev2 * stdDev2) / n2
    );

    if (pooledStdDev === 0) return 1.0;

    const tStat = Math.abs(mean1 - mean2) / pooledStdDev;

    // Approximate p-value (simplified)
    return Math.exp(-tStat);
  }

  /**
   * Generate recommendations based on analysis
   */
  private generateRecommendations(
    direction: string,
    slope: number,
    anomalies: AnomalyDetection[],
    volatility: number,
    seasonality?: SeasonalPattern
  ): string[] {
    const recommendations: string[] = [];

    if (direction === 'declining') {
      recommendations.push('Pattern performance declining - consider updating or replacing');
      recommendations.push('Investigate recent code changes that may affect pattern applicability');
    }

    if (direction === 'volatile') {
      recommendations.push('High volatility detected - pattern may be context-dependent');
      recommendations.push('Consider splitting into multiple specialized patterns');
    }

    if (anomalies.length > 3) {
      recommendations.push('Frequent anomalies detected - pattern may need refinement');
    }

    if (seasonality?.detected) {
      recommendations.push(
        `Seasonal pattern detected (period: ${seasonality.period}) - adjust usage timing`
      );
    }

    if (direction === 'stable' && slope > 0) {
      recommendations.push('Pattern performing well - consider sharing with other agents');
    }

    return recommendations;
  }

  /**
   * Calculate mean
   */
  private calculateMean(values: number[]): number {
    return values.length === 0 ? 0 : values.reduce((a, b) => a + b, 0) / values.length;
  }

  /**
   * Calculate standard deviation
   */
  private calculateStdDev(values: number[], mean: number): number {
    if (values.length < 2) return 0;

    const variance =
      values.reduce((sum, val) => sum + Math.pow(val - mean, 2), 0) / (values.length - 1);

    return Math.sqrt(variance);
  }

  /**
   * Get empty forecast for insufficient data
   */
  private getEmptyForecast(): PerformanceForecast {
    return {
      horizon: 0,
      predictions: [],
      confidenceIntervals: [],
      method: 'linear',
      accuracy: 0,
    };
  }

  /**
   * Merge user config with defaults
   */
  private mergeConfig(userConfig: Partial<TrendAnalysisConfig>): TrendAnalysisConfig {
    return {
      anomaly: { ...DEFAULT_CONFIG.anomaly, ...userConfig.anomaly },
      trend: { ...DEFAULT_CONFIG.trend, ...userConfig.trend },
      forecast: { ...DEFAULT_CONFIG.forecast, ...userConfig.forecast },
      seasonality: { ...DEFAULT_CONFIG.seasonality, ...userConfig.seasonality },
      learningRate: { ...DEFAULT_CONFIG.learningRate, ...userConfig.learningRate },
    };
  }
}
