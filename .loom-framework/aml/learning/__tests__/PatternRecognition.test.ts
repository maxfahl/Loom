/**
 * PatternRecognition Test Suite
 */

import { describe, it, expect, beforeEach } from '@jest/globals';
import { PatternRecognitionEngine, AgentAction, ActionSequence } from '../PatternRecognition';
import { Pattern } from '../../models/Pattern';

describe('PatternRecognition', () => {
  let recognizer: PatternRecognitionEngine;

  beforeEach(() => {
    recognizer = new PatternRecognitionEngine();
  });

  describe('Sequence Extraction', () => {
    it('should extract action sequences', () => {
      const actions: AgentAction[] = [
        {
          type: 'read',
          timestamp: new Date().toISOString(),
          context: { target: 'file.ts' },
          parameters: { file: 'file.ts' },
          outcome: 'success',
          durationMs: 100
        },
        {
          type: 'edit',
          timestamp: new Date(Date.now() + 100).toISOString(),
          context: { target: 'file.ts' },
          parameters: { file: 'file.ts' },
          outcome: 'success',
          durationMs: 200
        },
        {
          type: 'test',
          timestamp: new Date(Date.now() + 200).toISOString(),
          context: { target: 'file.test.ts' },
          parameters: { file: 'file.test.ts' },
          outcome: 'success',
          durationMs: 150
        }
      ];

      const sequences = recognizer.extractSequences(actions, 'test-agent');

      expect(sequences).toBeDefined();
      expect(sequences.length).toBeGreaterThan(0);
    });

    it('should group temporal sequences', () => {
      const now = Date.now();
      const actions: AgentAction[] = [
        {
          type: 'read',
          timestamp: new Date(now).toISOString(),
          context: {},
          parameters: {},
          outcome: 'success',
          durationMs: 50
        },
        {
          type: 'edit',
          timestamp: new Date(now + 50).toISOString(),
          context: {},
          parameters: {},
          outcome: 'success',
          durationMs: 50
        },
        {
          type: 'test',
          timestamp: new Date(now + 5000).toISOString(), // Large gap
          context: {},
          parameters: {},
          outcome: 'success',
          durationMs: 100
        }
      ];

      const sequences = recognizer.extractSequences(actions, 'test-agent');

      // Should extract at least one sequence from these actions
      expect(sequences.length).toBeGreaterThanOrEqual(1);
    });
  });

  describe('Similarity Matching', () => {
    it('should calculate similarity between patterns', () => {
      const seq1: ActionSequence = {
        actions: [
          {
            type: 'react-optimization',
            timestamp: new Date().toISOString(),
            context: { framework: 'React' },
            parameters: { approach: 'useMemo' },
            outcome: 'success',
            durationMs: 100
          }
        ],
        startTime: new Date().toISOString(),
        endTime: new Date(Date.now() + 100).toISOString(),
        frequency: 1,
        avgDuration: 100
      };

      const seq2: ActionSequence = {
        actions: [
          {
            type: 'react-optimization',
            timestamp: new Date().toISOString(),
            context: { framework: 'React' },
            parameters: { approach: 'useMemo' },
            outcome: 'success',
            durationMs: 100
          }
        ],
        startTime: new Date().toISOString(),
        endTime: new Date(Date.now() + 100).toISOString(),
        frequency: 1,
        avgDuration: 100
      };

      const similarity = recognizer.calculateCosineSimilarity(seq1, seq2);

      expect(similarity).toBeGreaterThan(0.8);
    });

    it('should detect dissimilar patterns', () => {
      const seq1: ActionSequence = {
        actions: [
          {
            type: 'frontend',
            timestamp: new Date().toISOString(),
            context: {},
            parameters: { approach: 'React' },
            outcome: 'success',
            durationMs: 100
          }
        ],
        startTime: new Date().toISOString(),
        endTime: new Date(Date.now() + 100).toISOString(),
        frequency: 1,
        avgDuration: 100
      };

      const seq2: ActionSequence = {
        actions: [
          {
            type: 'backend',
            timestamp: new Date().toISOString(),
            context: {},
            parameters: { approach: 'Express' },
            outcome: 'success',
            durationMs: 100
          }
        ],
        startTime: new Date().toISOString(),
        endTime: new Date(Date.now() + 100).toISOString(),
        frequency: 1,
        avgDuration: 100
      };

      const similarity = recognizer.calculateCosineSimilarity(seq1, seq2);

      expect(similarity).toBeLessThan(0.8);
    });
  });

  describe('Pattern Validation', () => {
    it('should validate statistically significant patterns', () => {
      const sequence: ActionSequence = {
        actions: Array(20).fill(null).map(() => ({
          type: 'test-action',
          timestamp: new Date().toISOString(),
          context: {},
          parameters: {},
          outcome: 'success',
          durationMs: 100
        })),
        startTime: new Date().toISOString(),
        endTime: new Date(Date.now() + 100).toISOString(),
        frequency: 20,
        avgDuration: 100
      };

      const result = recognizer.validatePattern(sequence, []);

      expect(result.valid).toBe(true);
    });

    it('should reject patterns without enough data', () => {
      const sequence: ActionSequence = {
        actions: [
          {
            type: 'test-action',
            timestamp: new Date().toISOString(),
            context: {},
            parameters: {},
            outcome: 'success',
            durationMs: 100
          }
        ],
        startTime: new Date().toISOString(),
        endTime: new Date(Date.now() + 100).toISOString(),
        frequency: 2,
        avgDuration: 100
      };

      const result = recognizer.validatePattern(sequence, []);

      // Should be false due to low frequency (< 3 minimum)
      expect(result.valid).toBe(false);
    });
  });

  describe('Pattern Evolution', () => {
    it('should track pattern refinements', () => {
      const pattern: Pattern = {
        id: 'a0b1c2d3-e4f5-6789-abcd-ef0123456789',
        agent: 'test-agent',
        timestamp: new Date().toISOString(),
        pattern: {
          type: 'test-pattern',
          context: {},
          approach: {
            technique: 'test-technique',
            rationale: 'test rationale'
          },
          conditions: {
            whenApplicable: ['condition1'],
            whenNotApplicable: ['condition2']
          }
        },
        metrics: {
          successRate: 0.5,
          executionCount: 0,
          avgTimeSavedMs: 100,
          errorPreventionCount: 0
        },
        evolution: {
          created: new Date().toISOString(),
          lastUsed: new Date().toISOString(),
          refinements: 0,
          confidenceScore: 0.5
        },
        tags: [],
        active: true
      };

      const initialRefinements = pattern.evolution.refinements;

      // Track successful usage
      recognizer.trackEvolution(pattern, { success: true, timestamp: new Date().toISOString() });
      recognizer.trackEvolution(pattern, { success: true, timestamp: new Date().toISOString() });

      // Refinements should increase with usage
      expect(pattern.evolution.refinements).toBeGreaterThan(initialRefinements);
    });
  });
});
