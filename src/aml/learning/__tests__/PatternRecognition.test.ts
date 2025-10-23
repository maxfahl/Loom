/**
 * PatternRecognition Test Suite
 */

import { describe, it, expect } from '@jest/globals';
import { PatternRecognizer } from '../PatternRecognition';

describe('PatternRecognition', () => {
  let recognizer: PatternRecognizer;

  beforeEach(() => {
    recognizer = new PatternRecognizer();
  });

  describe('Sequence Extraction', () => {
    it('should extract action sequences', () => {
      const actions = [
        { type: 'read', target: 'file.ts', timestamp: Date.now() },
        { type: 'edit', target: 'file.ts', timestamp: Date.now() + 100 },
        { type: 'test', target: 'file.test.ts', timestamp: Date.now() + 200 }
      ];

      const sequences = recognizer.extractSequences(actions);

      expect(sequences).toBeDefined();
      expect(sequences.length).toBeGreaterThan(0);
    });

    it('should group temporal sequences', () => {
      const actions = [
        { type: 'read', timestamp: Date.now() },
        { type: 'edit', timestamp: Date.now() + 50 },
        { type: 'test', timestamp: Date.now() + 5000 } // Large gap
      ];

      const sequences = recognizer.extractSequences(actions, { maxGapMs: 1000 });

      expect(sequences.length).toBe(2); // Two separate sequences due to gap
    });
  });

  describe('Similarity Matching', () => {
    it('should calculate similarity between patterns', () => {
      const pattern1 = {
        type: 'react-optimization',
        approach: 'useMemo',
        context: { framework: 'React' }
      };

      const pattern2 = {
        type: 'react-optimization',
        approach: 'useMemo',
        context: { framework: 'React' }
      };

      const similarity = recognizer.calculateSimilarity(pattern1, pattern2);

      expect(similarity).toBeGreaterThan(0.8);
    });

    it('should detect dissimilar patterns', () => {
      const pattern1 = { type: 'frontend', approach: 'React' };
      const pattern2 = { type: 'backend', approach: 'Express' };

      const similarity = recognizer.calculateSimilarity(pattern1, pattern2);

      expect(similarity).toBeLessThan(0.3);
    });
  });

  describe('Pattern Validation', () => {
    it('should validate statistically significant patterns', () => {
      const pattern = {
        successCount: 15,
        failureCount: 2,
        totalUses: 17
      };

      const isValid = recognizer.validatePattern(pattern, { significance: 0.05 });

      expect(isValid).toBe(true);
    });

    it('should reject patterns without enough data', () => {
      const pattern = {
        successCount: 2,
        failureCount: 0,
        totalUses: 2
      };

      const isValid = recognizer.validatePattern(pattern, { minSampleSize: 5 });

      expect(isValid).toBe(false);
    });
  });

  describe('Pattern Evolution', () => {
    it('should track pattern refinements', () => {
      const pattern = {
        id: 'p1',
        refinements: 0,
        confidence: 0.5
      };

      recognizer.recordSuccess(pattern);
      recognizer.recordSuccess(pattern);

      expect(pattern.refinements).toBeGreaterThan(0);
      expect(pattern.confidence).toBeGreaterThan(0.5);
    });
  });
});
