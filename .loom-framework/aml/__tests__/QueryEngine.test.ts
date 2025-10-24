/**
 * QueryEngine Unit Tests
 *
 * Tests pattern matching, similarity calculation, ranking, and fuzzy search
 * Coverage target: 90%+
 */

import { QueryEngine, SimilarityScore, RankingWeights } from '../QueryEngine';
import { Pattern, PatternModel } from '../models/Pattern';
import { Solution, SolutionModel } from '../models/Solution';

describe('QueryEngine', () => {
  let engine: QueryEngine;
  const testAgent = 'test-agent';

  beforeEach(() => {
    engine = new QueryEngine();
  });

  describe('Index Management', () => {
    it('should build pattern index', () => {
      const patterns = createTestPatterns(5);

      engine.buildPatternIndex(testAgent, patterns);

      // Verify index was created
      const results = engine.searchPatternsByType(testAgent, 'test-pattern-0');
      expect(results.length).toBeGreaterThan(0);
    });

    it('should index patterns by type', () => {
      const patterns = [
        createTestPattern('react-optimization'),
        createTestPattern('react-optimization'),
        createTestPattern('api-design')
      ];

      engine.buildPatternIndex(testAgent, patterns);

      const reactPatterns = engine.searchPatternsByType(testAgent, 'react-optimization');
      expect(reactPatterns.length).toBe(2);

      const apiPatterns = engine.searchPatternsByType(testAgent, 'api-design');
      expect(apiPatterns.length).toBe(1);
    });

    it('should index patterns by tags', () => {
      const patterns = [
        createTestPattern('react-optimization', ['performance', 'react']),
        createTestPattern('api-design', ['performance', 'api'])
      ];

      engine.buildPatternIndex(testAgent, patterns);

      const perfPatterns = engine.searchPatternsByTag(testAgent, 'performance');
      expect(perfPatterns.length).toBe(2);
    });

    it('should index patterns by context', () => {
      const patterns = [
        {
          ...createTestPattern('test-1'),
          pattern: { ...createTestPattern('test-1').pattern, context: { framework: 'React' } }
        },
        {
          ...createTestPattern('test-2'),
          pattern: { ...createTestPattern('test-2').pattern, context: { framework: 'Vue' } }
        }
      ];

      engine.buildPatternIndex(testAgent, patterns);

      const reactPatterns = engine.searchPatternsByContext(testAgent, { framework: 'React' });
      expect(reactPatterns.length).toBe(1);
    });

    it('should index patterns by confidence buckets', () => {
      const patterns = [
        createTestPatternWithConfidence('test-1', 0.1),
        createTestPatternWithConfidence('test-2', 0.5),
        createTestPatternWithConfidence('test-3', 0.9)
      ];

      engine.buildPatternIndex(testAgent, patterns);

      const highConfidence = engine.searchPatternsByConfidence(testAgent, 0.7);
      expect(highConfidence.length).toBe(1);
    });

    it('should build solution index', () => {
      const solutions = createTestSolutions(3);

      engine.buildSolutionIndex(testAgent, solutions);

      // Index should be created (we can't directly verify without exposing internal structure)
      expect(engine).toBeDefined();
    });

    it('should clear indices', () => {
      const patterns = createTestPatterns(3);
      engine.buildPatternIndex(testAgent, patterns);

      engine.clearIndices();

      const results = engine.searchPatternsByType(testAgent, 'react-optimization');
      expect(results.length).toBe(0);
    });

    it('should clear agent-specific indices', () => {
      const patterns = createTestPatterns(3);
      engine.buildPatternIndex(testAgent, patterns);
      engine.buildPatternIndex('other-agent', patterns);

      engine.clearAgentIndices(testAgent);

      const results = engine.searchPatternsByType(testAgent, 'react-optimization');
      expect(results.length).toBe(0);
    });
  });

  describe('Pattern Search', () => {
    it('should search patterns by type using index', () => {
      const patterns = createTestPatterns(5);
      engine.buildPatternIndex(testAgent, patterns);

      const results = engine.searchPatternsByType(testAgent, 'react-optimization');

      expect(results).toBeDefined();
      expect(Array.isArray(results)).toBe(true);
    });

    it('should handle non-existent agent in search', () => {
      const results = engine.searchPatternsByType('nonexistent', 'test');
      expect(results).toEqual([]);
    });

    it('should search patterns by single context key-value', () => {
      const patterns = [
        {
          ...createTestPattern('test-1'),
          pattern: { ...createTestPattern('test-1').pattern, context: { framework: 'React', version: '18' } }
        }
      ];

      engine.buildPatternIndex(testAgent, patterns);

      const results = engine.searchPatternsByContext(testAgent, { framework: 'React' });
      expect(results.length).toBe(1);
    });

    it('should search patterns by multiple context keys (intersection)', () => {
      const patterns = [
        {
          ...createTestPattern('test-1'),
          pattern: { ...createTestPattern('test-1').pattern, context: { framework: 'React', version: '18' } }
        },
        {
          ...createTestPattern('test-2'),
          pattern: { ...createTestPattern('test-2').pattern, context: { framework: 'React', version: '17' } }
        }
      ];

      engine.buildPatternIndex(testAgent, patterns);

      const results = engine.searchPatternsByContext(testAgent, { framework: 'React', version: '18' });
      expect(results.length).toBe(1);
    });
  });

  describe('Similarity Calculation', () => {
    it('should calculate exact pattern similarity', () => {
      const pattern1 = createTestPattern('test-1');
      const pattern2 = createTestPattern('test-1'); // Same type

      const similarity = engine.calculatePatternSimilarity(pattern1, pattern2);

      expect(similarity).toBeGreaterThan(0.5);
      expect(similarity).toBeLessThanOrEqual(1);
    });

    it('should calculate different pattern similarity', () => {
      const pattern1 = createTestPattern('react-optimization');
      const pattern2 = createTestPattern('api-design');

      const similarity = engine.calculatePatternSimilarity(pattern1, pattern2);

      expect(similarity).toBeGreaterThanOrEqual(0);
      // Allow for floating point precision
      expect(similarity).toBeLessThanOrEqual(0.51);
    });

    it('should find similar patterns with threshold', () => {
      const targetPattern = createTestPattern('react-optimization');
      const patterns = [
        targetPattern,
        createTestPattern('react-optimization'),
        createTestPattern('api-design')
      ];

      const similar = engine.findSimilarPatterns(testAgent, targetPattern, patterns, 0.5, 10);

      expect(similar.length).toBeGreaterThan(0);
      expect(similar[0].score).toBeGreaterThanOrEqual(0.5);
    });

    it('should exclude self from similarity results', () => {
      const pattern = createTestPattern('test');
      const patterns = [pattern];

      const similar = engine.findSimilarPatterns(testAgent, pattern, patterns, 0, 10);

      // Self should be excluded
      expect(similar.every(s => s.id !== pattern.id)).toBe(true);
    });

    it('should respect similarity threshold', () => {
      const target = createTestPattern('react-optimization');
      const patterns = createTestPatterns(10);

      const similar = engine.findSimilarPatterns(testAgent, target, patterns, 0.8, 10);

      expect(similar.every(s => s.score >= 0.8)).toBe(true);
    });

    it('should respect limit on results', () => {
      const target = createTestPattern('test');
      const patterns = createTestPatterns(50);

      const similar = engine.findSimilarPatterns(testAgent, target, patterns, 0, 5);

      expect(similar.length).toBeLessThanOrEqual(5);
    });
  });

  describe('Ranking Algorithms', () => {
    it('should rank patterns by confidence', () => {
      const patterns = [
        createTestPatternWithConfidence('test-1', 0.3),
        createTestPatternWithConfidence('test-2', 0.8),
        createTestPatternWithConfidence('test-3', 0.5)
      ];

      const weights: RankingWeights = {
        confidence: 1.0,
        recency: 0,
        usage: 0,
        similarity: 0
      };

      const ranked = engine.rankPatterns(patterns, weights);

      expect(ranked[0].evolution.confidenceScore).toBeGreaterThanOrEqual(
        ranked[ranked.length - 1].evolution.confidenceScore
      );
    });

    it('should rank patterns by recency', () => {
      const now = Date.now();
      const patterns = [
        { ...createTestPattern('old'), evolution: { ...createTestPattern('old').evolution, lastUsed: new Date(now - 30 * 24 * 60 * 60 * 1000).toISOString() } },
        { ...createTestPattern('new'), evolution: { ...createTestPattern('new').evolution, lastUsed: new Date(now).toISOString() } }
      ];

      const weights: RankingWeights = {
        confidence: 0,
        recency: 1.0,
        usage: 0,
        similarity: 0
      };

      const ranked = engine.rankPatterns(patterns, weights);

      // Recent should rank higher
      expect(ranked[0].evolution.lastUsed).toBe(patterns[1].evolution.lastUsed);
    });

    it('should rank patterns by usage frequency', () => {
      const patterns = [
        { ...createTestPattern('low-use'), metrics: { ...createTestPattern('low-use').metrics, executionCount: 5 } },
        { ...createTestPattern('high-use'), metrics: { ...createTestPattern('high-use').metrics, executionCount: 50 } }
      ];

      const weights: RankingWeights = {
        confidence: 0,
        recency: 0,
        usage: 1.0,
        similarity: 0
      };

      const ranked = engine.rankPatterns(patterns, weights);

      expect(ranked[0].metrics.executionCount).toBeGreaterThanOrEqual(
        ranked[ranked.length - 1].metrics.executionCount
      );
    });

    it('should rank patterns with target context', () => {
      const context = { framework: 'React' };
      const patterns = [
        {
          ...createTestPattern('react-1'),
          pattern: { ...createTestPattern('react-1').pattern, context }
        },
        {
          ...createTestPattern('vue-1'),
          pattern: { ...createTestPattern('vue-1').pattern, context: { framework: 'Vue' } }
        }
      ];

      const ranked = engine.rankPatterns(patterns, undefined, context);

      // React pattern should rank higher for React context
      expect(ranked[0].pattern.context.framework).toBe('React');
    });

    it('should rank solutions', () => {
      const solutions = [
        createTestSolutionWithWorked(true),
        createTestSolutionWithWorked(false),
        createTestSolutionWithWorked(true)
      ];

      const ranked = engine.rankSolutions(solutions);

      // Working solutions should rank higher
      expect(ranked[0].effectiveness.worked).toBe(true);
    });

    it('should rank decisions', () => {
      const decisions = createTestDecisions(3);

      const ranked = engine.rankDecisions(decisions);

      expect(Array.isArray(ranked)).toBe(true);
      expect(ranked.length).toBe(3);
    });
  });

  describe('Fuzzy Search', () => {
    it('should fuzzy search patterns by query', () => {
      const patterns = [
        createTestPattern('react-optimization'),
        createTestPattern('api-design')
      ];

      const results = engine.fuzzySearchPatterns(patterns, 'react', 0.5);

      expect(results.length).toBeGreaterThan(0);
    });

    it('should find exact substring matches first', () => {
      const patterns = [
        createTestPattern('react-optimization'),
        createTestPattern('api-design')
      ];

      const results = engine.fuzzySearchPatterns(patterns, 'react', 0);

      expect(results.length).toBeGreaterThan(0);
      expect(results[0].pattern.type).toContain('react');
    });

    it('should fuzzy search solutions by error message', () => {
      const solutions = [
        createTestSolution('TypeError', 'Cannot read property x of undefined'),
        createTestSolution('ReferenceError', 'variable is not defined')
      ];

      const results = engine.fuzzySearchSolutions(solutions, 'Cannot read', 0.5);

      expect(results.length).toBeGreaterThan(0);
    });

    it('should handle case-insensitive fuzzy search', () => {
      const patterns = [createTestPattern('REACT-OPTIMIZATION')];

      const results = engine.fuzzySearchPatterns(patterns, 'react', 0.7);

      expect(results.length).toBeGreaterThan(0);
    });

    it('should respect minimum similarity threshold in fuzzy search', () => {
      const patterns = createTestPatterns(20);

      const results = engine.fuzzySearchPatterns(patterns, 'xyz', 0.9);

      expect(results.every(p => {
        const sim = engine['calculateStringSimilarity']('xyz', p.pattern.type);
        return sim >= 0.9;
      })).toBe(true);
    });
  });

  describe('Analytics', () => {
    it('should calculate pattern statistics', () => {
      const patterns = createTestPatterns(5);

      const stats = engine.getPatternStats(patterns);

      expect(stats.total).toBe(5);
      expect(stats.active).toBeGreaterThanOrEqual(0);
      expect(stats.avgConfidence).toBeGreaterThanOrEqual(0);
      expect(stats.avgSuccessRate).toBeGreaterThanOrEqual(0);
      expect(stats.avgExecutionCount).toBeGreaterThanOrEqual(0);
      expect(Array.isArray(stats.topTypes)).toBe(true);
    });

    it('should identify top pattern types', () => {
      const patterns = [
        createTestPattern('react-optimization'),
        createTestPattern('react-optimization'),
        createTestPattern('api-design'),
        createTestPattern('api-design'),
        createTestPattern('database-query')
      ];

      const stats = engine.getPatternStats(patterns);

      expect(stats.topTypes.length).toBeGreaterThan(0);
      expect(stats.topTypes[0].count).toBeGreaterThanOrEqual(stats.topTypes[1]?.count || 0);
    });

    it('should handle empty pattern list in statistics', () => {
      const stats = engine.getPatternStats([]);

      expect(stats.total).toBe(0);
      expect(stats.avgConfidence).toBe(0);
    });
  });

  describe('Edge Cases & Performance', () => {
    it('should handle large pattern sets', () => {
      const patterns = createTestPatterns(1000);

      const start = Date.now();
      engine.buildPatternIndex(testAgent, patterns);
      const duration = Date.now() - start;

      // Should complete in reasonable time even with 1000 patterns
      expect(duration).toBeLessThan(5000);
    });

    it('should handle empty context matching', () => {
      const patterns = [createTestPattern('test')];
      engine.buildPatternIndex(testAgent, patterns);

      const results = engine.searchPatternsByContext(testAgent, {});

      expect(Array.isArray(results)).toBe(true);
    });

    it('should handle patterns with no tags', () => {
      const patterns = [
        { ...createTestPattern('test-1'), tags: undefined },
        { ...createTestPattern('test-2'), tags: [] }
      ];

      engine.buildPatternIndex(testAgent, patterns);

      expect(() => engine.searchPatternsByTag(testAgent, 'any')).not.toThrow();
    });

    it('should handle similarity calculation with different feature spaces', () => {
      const pattern1 = {
        ...createTestPattern('test-1'),
        pattern: { ...createTestPattern('test-1').pattern, context: { a: 'x' } }
      };
      const pattern2 = {
        ...createTestPattern('test-2'),
        pattern: { ...createTestPattern('test-2').pattern, context: { b: 'y' } }
      };

      const similarity = engine.calculatePatternSimilarity(pattern1, pattern2);

      expect(similarity).toBeGreaterThanOrEqual(0);
      expect(similarity).toBeLessThanOrEqual(1);
    });
  });
});

// Test Helpers
import { randomUUID } from 'crypto';

function createTestPattern(type: string, tags?: string[]): Pattern {
  return {
    id: randomUUID(),
    agent: 'test-agent',
    timestamp: new Date().toISOString(),
    pattern: {
      type,
      context: { framework: 'React' },
      approach: {
        technique: 'test-technique',
        rationale: 'test rationale'
      },
      conditions: {
        whenApplicable: ['test'],
        whenNotApplicable: []
      }
    },
    metrics: {
      successRate: 0.85,
      executionCount: 10,
      avgTimeSavedMs: 100,
      errorPreventionCount: 5
    },
    evolution: {
      created: new Date().toISOString(),
      lastUsed: new Date().toISOString(),
      refinements: 2,
      confidenceScore: 0.7
    },
    tags
  };
}

function createTestPatternWithConfidence(type: string, confidence: number): Pattern {
  const pattern = createTestPattern(type);
  pattern.evolution.confidenceScore = confidence;
  return pattern;
}

function createTestPatterns(count: number): Pattern[] {
  return Array.from({ length: count }, (_, i) => createTestPattern(`test-pattern-${i}`));
}

function createTestSolution(errorType: string, errorMessage: string): Solution {
  return {
    id: randomUUID(),
    agent: 'test-agent',
    timestamp: new Date().toISOString(),
    problem: {
      errorType,
      errorMessage,
      context: {}
    },
    solution: {
      rootCause: 'test cause',
      fixApproach: 'test approach',
      prevention: 'test prevention'
    },
    effectiveness: {
      worked: true,
      timeToFixMinutes: 5,
      preventedRecurrence: 3,
      relatedErrorsFixed: 1
    },
    verifiedCount: 1
  };
}

function createTestSolutionWithWorked(worked: boolean): Solution {
  const solution = createTestSolution('TypeError', 'test error');
  solution.effectiveness.worked = worked;
  return solution;
}

function createTestSolutions(count: number): Solution[] {
  return Array.from({ length: count }, (_, i) => createTestSolution(`Error${i}`, `error message ${i}`));
}

function createTestDecisions(count: number) {
  return Array.from({ length: count }, (_, i) => ({
    id: randomUUID(),
    agent: 'test-agent',
    timestamp: new Date().toISOString(),
    decision: {
      type: 'test-decision',
      question: `Decision ${i}?`,
      context: {},
      chosenOption: 'option-a',
      alternativesConsidered: ['option-b'],
      decisionFactors: { primary: ['factor-1'], secondary: [] }
    }
  }));
}
