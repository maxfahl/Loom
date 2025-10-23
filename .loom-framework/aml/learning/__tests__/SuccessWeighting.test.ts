/**
 * Unit tests for Success Weighting System
 */

import { SuccessWeightingSystem } from '../SuccessWeighting';
import { Pattern } from '../../models/Pattern';

describe('SuccessWeightingSystem', () => {
  let system: SuccessWeightingSystem;

  beforeEach(() => {
    system = new SuccessWeightingSystem();
  });

  describe('calculatePatternWeight', () => {
    it('should calculate weight with all factors', () => {
      const pattern: Pattern = {
        id: '123',
        agent: 'test-agent',
        timestamp: new Date().toISOString(),
        pattern: {
          type: 'test-pattern',
          context: { framework: 'React' },
          approach: {
            technique: 'test-technique',
            rationale: 'test rationale',
          },
          conditions: {
            whenApplicable: ['test'],
            whenNotApplicable: [],
          },
        },
        metrics: {
          successRate: 0.9,
          executionCount: 50,
          avgTimeSavedMs: 1000,
          errorPreventionCount: 5,
        },
        evolution: {
          created: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000).toISOString(),
          lastUsed: new Date(Date.now() - 1 * 24 * 60 * 60 * 1000).toISOString(),
          refinements: 10,
          confidenceScore: 0.85,
        },
        active: true,
      };

      const result = system.calculatePatternWeight(pattern);

      expect(result.totalWeight).toBeGreaterThan(0);
      expect(result.totalWeight).toBeLessThanOrEqual(1);
      expect(result.factors.baseSuccessRate).toBeGreaterThan(0);
      expect(result.factors.recencyFactor).toBeGreaterThan(0);
      expect(result.factors.complexityFactor).toBeGreaterThan(0);
      expect(result.confidence).toBeGreaterThan(0);
    });

    it('should give higher weight to recent patterns', () => {
      const recentPattern: Pattern = {
        id: '1',
        agent: 'test',
        timestamp: new Date().toISOString(),
        pattern: {
          type: 'test',
          context: {},
          approach: { technique: 'test', rationale: 'test' },
          conditions: { whenApplicable: [], whenNotApplicable: [] },
        },
        metrics: {
          successRate: 0.8,
          executionCount: 10,
          avgTimeSavedMs: 100,
          errorPreventionCount: 0,
        },
        evolution: {
          created: new Date().toISOString(),
          lastUsed: new Date().toISOString(),
          refinements: 1,
          confidenceScore: 0.7,
        },
        active: true,
      };

      const oldPattern: Pattern = {
        ...recentPattern,
        id: '2',
        evolution: {
          ...recentPattern.evolution,
          lastUsed: new Date(Date.now() - 90 * 24 * 60 * 60 * 1000).toISOString(),
        },
      };

      const recentWeight = system.calculatePatternWeight(recentPattern);
      const oldWeight = system.calculatePatternWeight(oldPattern);

      expect(recentWeight.factors.recencyFactor).toBeGreaterThan(
        oldWeight.factors.recencyFactor
      );
    });

    it('should prefer simpler patterns', () => {
      const simplePattern: Pattern = {
        id: '1',
        agent: 'test',
        timestamp: new Date().toISOString(),
        pattern: {
          type: 'simple',
          context: { a: 'b' },
          approach: {
            technique: 'simple',
            rationale: 'simple',
            steps: ['step1'],
          },
          conditions: { whenApplicable: ['case1'], whenNotApplicable: [] },
        },
        metrics: {
          successRate: 0.8,
          executionCount: 10,
          avgTimeSavedMs: 100,
          errorPreventionCount: 0,
        },
        evolution: {
          created: new Date().toISOString(),
          lastUsed: new Date().toISOString(),
          refinements: 1,
          confidenceScore: 0.7,
        },
        active: true,
      };

      const complexPattern: Pattern = {
        ...simplePattern,
        id: '2',
        pattern: {
          ...simplePattern.pattern,
          context: { a: 'b', c: 'd', e: 'f', g: 'h' },
          approach: {
            ...simplePattern.pattern.approach,
            steps: Array(15).fill('step'),
          },
          conditions: {
            whenApplicable: Array(10).fill('case'),
            whenNotApplicable: Array(5).fill('case'),
          },
        },
      };

      const simpleWeight = system.calculatePatternWeight(simplePattern);
      const complexWeight = system.calculatePatternWeight(complexPattern);

      expect(simpleWeight.factors.complexityFactor).toBeGreaterThan(
        complexWeight.factors.complexityFactor
      );
    });

    it('should consider context fit when provided', () => {
      const pattern: Pattern = {
        id: '1',
        agent: 'test',
        timestamp: new Date().toISOString(),
        pattern: {
          type: 'test',
          context: { framework: 'React', version: '18' },
          approach: { technique: 'test', rationale: 'test' },
          conditions: { whenApplicable: [], whenNotApplicable: [] },
        },
        metrics: {
          successRate: 0.8,
          executionCount: 10,
          avgTimeSavedMs: 100,
          errorPreventionCount: 0,
        },
        evolution: {
          created: new Date().toISOString(),
          lastUsed: new Date().toISOString(),
          refinements: 1,
          confidenceScore: 0.7,
        },
        active: true,
      };

      const matchingContext = { framework: 'React', version: '18' };
      const differentContext = { framework: 'Vue', version: '3' };

      const matchingResult = system.calculatePatternWeight(pattern, matchingContext);
      const differentResult = system.calculatePatternWeight(pattern, differentContext);

      expect(matchingResult.factors.projectFitFactor).toBeGreaterThan(
        differentResult.factors.projectFitFactor
      );
    });
  });

  describe('calculateConfidenceInterval', () => {
    it('should return wider intervals for small samples', () => {
      const smallSample = system.calculateConfidenceInterval(0.8, 5, 0.8);
      const largeSample = system.calculateConfidenceInterval(0.8, 100, 0.8);

      const smallWidth = smallSample.upper - smallSample.lower;
      const largeWidth = largeSample.upper - largeSample.lower;

      expect(smallWidth).toBeGreaterThan(largeWidth);
    });

    it('should keep intervals within [0, 1] bounds', () => {
      const interval = system.calculateConfidenceInterval(0.95, 50, 0.95);

      expect(interval.lower).toBeGreaterThanOrEqual(0);
      expect(interval.upper).toBeLessThanOrEqual(1);
    });

    it('should return full range for very small samples', () => {
      const interval = system.calculateConfidenceInterval(0.5, 2, 0.5);

      expect(interval.lower).toBe(0);
      expect(interval.upper).toBe(1);
    });
  });

  describe('adjustThresholds', () => {
    it('should lower threshold for improving patterns', () => {
      // Simulate improving pattern
      for (let i = 0; i < 20; i++) {
        const pattern: Pattern = {
          id: 'test-pattern',
          agent: 'test',
          timestamp: new Date().toISOString(),
          pattern: {
            type: 'test',
            context: {},
            approach: { technique: 'test', rationale: 'test' },
            conditions: { whenApplicable: [], whenNotApplicable: [] },
          },
          metrics: {
            successRate: 0.9,
            executionCount: i + 1,
            avgTimeSavedMs: 100,
            errorPreventionCount: 0,
          },
          evolution: {
            created: new Date().toISOString(),
            lastUsed: new Date().toISOString(),
            refinements: i,
            confidenceScore: 0.8,
          },
          active: true,
        };

        system.calculatePatternWeight(pattern);
      }

      const initialThresholds = system.getThresholds();
      system.adjustThresholds('test-pattern');
      const adjustedThresholds = system.getThresholds();

      expect(adjustedThresholds.minWeight).toBeLessThanOrEqual(initialThresholds.minWeight);
    });

    it('should raise threshold for declining patterns', () => {
      // Simulate declining pattern
      for (let i = 0; i < 20; i++) {
        const pattern: Pattern = {
          id: 'declining-pattern',
          agent: 'test',
          timestamp: new Date().toISOString(),
          pattern: {
            type: 'test',
            context: {},
            approach: { technique: 'test', rationale: 'test' },
            conditions: { whenApplicable: [], whenNotApplicable: [] },
          },
          metrics: {
            successRate: Math.max(0.2, 0.9 - i * 0.03),
            executionCount: i + 1,
            avgTimeSavedMs: 100,
            errorPreventionCount: 0,
          },
          evolution: {
            created: new Date().toISOString(),
            lastUsed: new Date().toISOString(),
            refinements: i,
            confidenceScore: 0.5,
          },
          active: true,
        };

        system.calculatePatternWeight(pattern);
      }

      const initialThresholds = system.getThresholds();
      system.adjustThresholds('declining-pattern');
      const adjustedThresholds = system.getThresholds();

      expect(adjustedThresholds.minWeight).toBeGreaterThanOrEqual(initialThresholds.minWeight);
    });
  });

  describe('recommendation strength', () => {
    it('should classify very strong recommendations correctly', () => {
      const pattern: Pattern = {
        id: '1',
        agent: 'test',
        timestamp: new Date().toISOString(),
        pattern: {
          type: 'test',
          context: {},
          approach: { technique: 'test', rationale: 'test' },
          conditions: { whenApplicable: [], whenNotApplicable: [] },
        },
        metrics: {
          successRate: 0.95,
          executionCount: 100,
          avgTimeSavedMs: 1000,
          errorPreventionCount: 10,
        },
        evolution: {
          created: new Date().toISOString(),
          lastUsed: new Date().toISOString(),
          refinements: 50,
          confidenceScore: 0.95,
        },
        active: true,
      };

      const result = system.calculatePatternWeight(pattern);

      expect(result.recommendationStrength).toBe('very-strong');
    });

    it('should classify weak recommendations correctly', () => {
      const pattern: Pattern = {
        id: '1',
        agent: 'test',
        timestamp: new Date().toISOString(),
        pattern: {
          type: 'test',
          context: {},
          approach: { technique: 'test', rationale: 'test' },
          conditions: { whenApplicable: [], whenNotApplicable: [] },
        },
        metrics: {
          successRate: 0.4,
          executionCount: 3,
          avgTimeSavedMs: 10,
          errorPreventionCount: 0,
        },
        evolution: {
          created: new Date().toISOString(),
          lastUsed: new Date().toISOString(),
          refinements: 1,
          confidenceScore: 0.3,
        },
        active: true,
      };

      const result = system.calculatePatternWeight(pattern);

      expect(result.recommendationStrength).toBe('weak');
    });
  });

  describe('performance history', () => {
    it('should track performance over time', () => {
      const patternId = 'history-test';

      for (let i = 0; i < 5; i++) {
        const pattern: Pattern = {
          id: patternId,
          agent: 'test',
          timestamp: new Date().toISOString(),
          pattern: {
            type: 'test',
            context: {},
            approach: { technique: 'test', rationale: 'test' },
            conditions: { whenApplicable: [], whenNotApplicable: [] },
          },
          metrics: {
            successRate: 0.8,
            executionCount: i + 1,
            avgTimeSavedMs: 100,
            errorPreventionCount: 0,
          },
          evolution: {
            created: new Date().toISOString(),
            lastUsed: new Date().toISOString(),
            refinements: i,
            confidenceScore: 0.7,
          },
          active: true,
        };

        system.calculatePatternWeight(pattern);
      }

      const history = system.getPerformanceHistory(patternId);

      expect(history).toBeDefined();
      expect(history!.totalUsages).toBe(5);
    });

    it('should clear history when requested', () => {
      const patternId = 'clear-test';

      const pattern: Pattern = {
        id: patternId,
        agent: 'test',
        timestamp: new Date().toISOString(),
        pattern: {
          type: 'test',
          context: {},
          approach: { technique: 'test', rationale: 'test' },
          conditions: { whenApplicable: [], whenNotApplicable: [] },
        },
        metrics: {
          successRate: 0.8,
          executionCount: 1,
          avgTimeSavedMs: 100,
          errorPreventionCount: 0,
        },
        evolution: {
          created: new Date().toISOString(),
          lastUsed: new Date().toISOString(),
          refinements: 0,
          confidenceScore: 0.7,
        },
        active: true,
      };

      system.calculatePatternWeight(pattern);
      expect(system.getPerformanceHistory(patternId)).toBeDefined();

      system.clearHistory();
      expect(system.getPerformanceHistory(patternId)).toBeUndefined();
    });
  });

  describe('edge cases', () => {
    it('should handle patterns with zero execution count', () => {
      const pattern: Pattern = {
        id: '1',
        agent: 'test',
        timestamp: new Date().toISOString(),
        pattern: {
          type: 'test',
          context: {},
          approach: { technique: 'test', rationale: 'test' },
          conditions: { whenApplicable: [], whenNotApplicable: [] },
        },
        metrics: {
          successRate: 0,
          executionCount: 0,
          avgTimeSavedMs: 0,
          errorPreventionCount: 0,
        },
        evolution: {
          created: new Date().toISOString(),
          lastUsed: new Date().toISOString(),
          refinements: 0,
          confidenceScore: 0.3,
        },
        active: true,
      };

      const result = system.calculatePatternWeight(pattern);

      expect(result.totalWeight).toBeGreaterThan(0);
      expect(result.confidence).toBeGreaterThan(0);
    });

    it('should handle very old patterns gracefully', () => {
      const pattern: Pattern = {
        id: '1',
        agent: 'test',
        timestamp: new Date().toISOString(),
        pattern: {
          type: 'test',
          context: {},
          approach: { technique: 'test', rationale: 'test' },
          conditions: { whenApplicable: [], whenNotApplicable: [] },
        },
        metrics: {
          successRate: 0.9,
          executionCount: 50,
          avgTimeSavedMs: 100,
          errorPreventionCount: 5,
        },
        evolution: {
          created: new Date(Date.now() - 365 * 24 * 60 * 60 * 1000).toISOString(),
          lastUsed: new Date(Date.now() - 365 * 24 * 60 * 60 * 1000).toISOString(),
          refinements: 10,
          confidenceScore: 0.8,
        },
        active: true,
      };

      const result = system.calculatePatternWeight(pattern);

      expect(result.factors.recencyFactor).toBeLessThan(0.2);
      expect(result.totalWeight).toBeGreaterThan(0);
    });
  });
});
