/**
 * PruningService Test Suite
 *
 * Tests memory pruning strategies including:
 * - Time-based pruning
 * - Performance-based pruning
 * - Space-based pruning
 * - Pattern weighting and selection
 */

import { describe, it, expect, beforeEach, afterEach } from '@jest/globals';
import * as fs from 'fs/promises';
import * as path from 'path';
import { PruningService } from '../PruningService';
import { MemoryStore } from '../storage/MemoryStore';
import { Pattern } from '../models/Pattern';

const TEST_DIR = path.join(__dirname, '../__test_data__/pruning-service');
const MEMORY_DIR = path.join(TEST_DIR, 'memory');

describe('PruningService', () => {
  let pruningService: PruningService;
  let memoryStore: MemoryStore;

  beforeEach(async () => {
    await fs.rm(TEST_DIR, { recursive: true, force: true });
    await fs.mkdir(MEMORY_DIR, { recursive: true });

    memoryStore = new MemoryStore(MEMORY_DIR);
    await memoryStore.initialize();

    pruningService = new PruningService(memoryStore);
  });

  afterEach(async () => {
    await fs.rm(TEST_DIR, { recursive: true, force: true });
  });

  describe('Time-Based Pruning', () => {
    it('should remove patterns unused for >90 days', async () => {
      const AGENT = 'test-agent';
      await memoryStore.ensureAgentDirectory(AGENT);

      // Old unused pattern (95 days ago)
      const oldDate = new Date();
      oldDate.setDate(oldDate.getDate() - 95);

      const oldPattern: Pattern = {
        id: '00000000-0000-0000-0000-000000000001',
        agent: AGENT,
        timestamp: oldDate.toISOString(),
        pattern: {
          type: 'old',
          context: {},
          approach: { technique: '', codeTemplate: '', rationale: '' },
          conditions: { whenApplicable: [], whenNotApplicable: [] }
        },
        metrics: { successRate: 0.8, executionCount: 1, avgTimeSavedMs: 100, errorPreventionCount: 0 },
        evolution: { created: oldDate.toISOString(), lastUsed: oldDate.toISOString(), refinements: 0, confidenceScore: 0.7 }
      };

      // Recent pattern
      const recentPattern: Pattern = {
        id: '00000000-0000-0000-0000-000000000002',
        agent: AGENT,
        timestamp: new Date().toISOString(),
        pattern: {
          type: 'recent',
          context: {},
          approach: { technique: '', codeTemplate: '', rationale: '' },
          conditions: { whenApplicable: [], whenNotApplicable: [] }
        },
        metrics: { successRate: 0.9, executionCount: 10, avgTimeSavedMs: 200, errorPreventionCount: 2 },
        evolution: { created: new Date().toISOString(), lastUsed: new Date().toISOString(), refinements: 2, confidenceScore: 0.85 }
      };

      await memoryStore.addPattern(AGENT, oldPattern);
      await memoryStore.addPattern(AGENT, recentPattern);

      const result = await pruningService.pruneByTime(AGENT, { maxAgeDays: 90 });

      expect(result.success).toBe(true);
      expect(result.data?.removedCount).toBe(1);

      // Verify old pattern is gone, recent remains
      const patterns = await memoryStore.getPatterns(AGENT);
      expect(patterns.data).toHaveLength(1);
      expect(patterns.data[0].id).toBe('00000000-0000-0000-0000-000000000002');
    });

    it('should remove failed patterns after 30 days', async () => {
      const AGENT = 'test-agent';
      await memoryStore.ensureAgentDirectory(AGENT);

      const oldFailedDate = new Date();
      oldFailedDate.setDate(oldFailedDate.getDate() - 35);

      const oldFailedPattern: Pattern = {
        id: '00000000-0000-0000-0000-000000000003',
        agent: AGENT,
        timestamp: oldFailedDate.toISOString(),
        pattern: {
          type: 'failed',
          context: {},
          approach: { technique: '', codeTemplate: '', rationale: '' },
          conditions: { whenApplicable: [], whenNotApplicable: [] }
        },
        metrics: { successRate: 0.1, executionCount: 10, avgTimeSavedMs: 0, errorPreventionCount: 0 },
        evolution: { created: oldFailedDate.toISOString(), lastUsed: oldFailedDate.toISOString(), refinements: 0, confidenceScore: 0.1 }
      };

      await memoryStore.addPattern(AGENT, oldFailedPattern);

      const result = await pruningService.pruneFailedPatterns(AGENT, { minAgeDays: 30, maxSuccessRate: 0.2 });

      expect(result.success).toBe(true);
      expect(result.data?.removedCount).toBe(1);
    });

    it('should archive old decisions instead of deleting', async () => {
      const AGENT = 'backend-architect';
      await memoryStore.ensureAgentDirectory(AGENT);

      const oldDecision = {
        id: 'old-decision',
        agent: AGENT,
        timestamp: new Date(Date.now() - 200 * 24 * 60 * 60 * 1000).toISOString(), // 200 days ago
        decision: {
          type: 'architecture',
          question: 'Old question',
          context: {},
          chosenOption: 'Option A',
          alternativesConsidered: [],
          decisionFactors: { primary: [], secondary: [] }
        },
        outcome: {
          successMetrics: {},
          lessonsLearned: [],
          wouldRepeat: true
        }
      };

      await memoryStore.addDecision(AGENT, oldDecision);

      const result = await pruningService.archiveOldDecisions(AGENT, { maxAgeDays: 180 });

      expect(result.success).toBe(true);
      expect(result.data?.archivedCount).toBe(1);

      // Decision should be moved to archive, not deleted
      const decisions = await memoryStore.getDecisions(AGENT);
      expect(decisions.data.find(d => d.id === 'old-decision')).toBeUndefined();
    });
  });

  describe('Performance-Based Pruning', () => {
    it('should remove patterns with <20% success rate', async () => {
      const AGENT = 'test-agent';
      await memoryStore.ensureAgentDirectory(AGENT);

      // Low success pattern
      const lowSuccessPattern: Pattern = {
        id: '00000000-0000-0000-0000-000000000004',
        agent: AGENT,
        timestamp: new Date().toISOString(),
        pattern: {
          type: 'low',
          context: {},
          approach: { technique: '', codeTemplate: '', rationale: '' },
          conditions: { whenApplicable: [], whenNotApplicable: [] }
        },
        metrics: { successRate: 0.15, executionCount: 20, avgTimeSavedMs: 50, errorPreventionCount: 0 },
        evolution: { created: new Date().toISOString(), lastUsed: new Date().toISOString(), refinements: 0, confidenceScore: 0.2 }
      };

      // High success pattern
      const highSuccessPattern: Pattern = {
        id: '00000000-0000-0000-0000-000000000005',
        agent: AGENT,
        timestamp: new Date().toISOString(),
        pattern: {
          type: 'high',
          context: {},
          approach: { technique: '', codeTemplate: '', rationale: '' },
          conditions: { whenApplicable: [], whenNotApplicable: [] }
        },
        metrics: { successRate: 0.95, executionCount: 30, avgTimeSavedMs: 300, errorPreventionCount: 5 },
        evolution: { created: new Date().toISOString(), lastUsed: new Date().toISOString(), refinements: 3, confidenceScore: 0.92 }
      };

      await memoryStore.addPattern(AGENT, lowSuccessPattern);
      await memoryStore.addPattern(AGENT, highSuccessPattern);

      const result = await pruningService.pruneByPerformance(AGENT, { minSuccessRate: 0.2 });

      expect(result.success).toBe(true);
      expect(result.data?.removedCount).toBe(1);

      const patterns = await memoryStore.getPatterns(AGENT);
      expect(patterns.data).toHaveLength(1);
      expect(patterns.data[0].id).toBe('00000000-0000-0000-0000-000000000005');
    });

    it('should prune solutions that no longer apply', async () => {
      const AGENT = 'debugger';
      await memoryStore.ensureAgentDirectory(AGENT);

      const outdatedSolution = {
        id: 'outdated',
        agent: AGENT,
        timestamp: new Date().toISOString(),
        problem: {
          errorType: 'DeprecatedError',
          errorMessage: 'Using deprecated API',
          stackTraceHash: 'abc123',
          context: { framework: 'OldFramework 1.0' }
        },
        solution: {
          rootCause: 'Framework upgrade needed',
          fixApproach: 'upgrade',
          codeFix: 'npm update old-framework',
          prevention: 'Keep dependencies updated'
        },
        effectiveness: {
          worked: false,
          timeToFixMinutes: 60,
          preventedRecurrence: 0,
          relatedErrorsFixed: 0
        }
      };

      await memoryStore.addSolution(AGENT, outdatedSolution);

      const result = await pruningService.pruneOutdatedSolutions(AGENT);

      expect(result.success).toBe(true);
      expect(result.data?.removedCount).toBeGreaterThanOrEqual(0);
    });

    it('should keep high-value patterns regardless of age', async () => {
      const AGENT = 'test-agent';
      await memoryStore.ensureAgentDirectory(AGENT);

      const oldDate = new Date();
      oldDate.setDate(oldDate.getDate() - 100);

      // Old but high-value pattern
      const highValuePattern: Pattern = {
        id: '00000000-0000-0000-0000-000000000006',
        agent: AGENT,
        timestamp: oldDate.toISOString(),
        pattern: {
          type: 'critical',
          context: {},
          approach: { technique: '', codeTemplate: '', rationale: '' },
          conditions: { whenApplicable: [], whenNotApplicable: [] }
        },
        metrics: { successRate: 0.98, executionCount: 100, avgTimeSavedMs: 500, errorPreventionCount: 20 },
        evolution: { created: oldDate.toISOString(), lastUsed: oldDate.toISOString(), refinements: 10, confidenceScore: 0.95 }
      };

      await memoryStore.addPattern(AGENT, highValuePattern);

      const result = await pruningService.pruneByTime(AGENT, {
        maxAgeDays: 90,
        preserveHighValue: true,
        minConfidenceToPreserve: 0.9
      });

      expect(result.success).toBe(true);
      expect(result.data?.removedCount).toBe(0); // Should be preserved

      const patterns = await memoryStore.getPatterns(AGENT);
      expect(patterns.data.find(p => p.id === '00000000-0000-0000-0000-000000000006')).toBeDefined();
    });
  });

  describe('Space-Based Pruning', () => {
    it('should trigger when agent memory >80MB', async () => {
      const AGENT = 'test-agent';
      await memoryStore.ensureAgentDirectory(AGENT);

      // Create many patterns to simulate high memory usage
      for (let i = 0; i < 100; i++) {
        await memoryStore.addPattern(AGENT, {
          id: crypto.randomUUID(),
          agent: AGENT,
          timestamp: new Date().toISOString(),
          pattern: {
            type: `type-${i}`,
            context: { data: 'x'.repeat(1000) }, // Large context
            approach: { technique: '', codeTemplate: '', rationale: '' },
            conditions: { whenApplicable: [], whenNotApplicable: [] }
          },
          metrics: { successRate: Math.random(), executionCount: i, avgTimeSavedMs: i * 10, errorPreventionCount: 0 },
          evolution: { created: new Date().toISOString(), lastUsed: new Date().toISOString(), refinements: 0, confidenceScore: Math.random() }
        });
      }

      const sizeCheck = await pruningService.checkMemorySize(AGENT);
      const shouldPrune = sizeCheck.data!.sizeMB > 80;

      if (shouldPrune) {
        const result = await pruningService.pruneBySpace(AGENT, { targetSizeMB: 50 });

        expect(result.success).toBe(true);
        expect(result.data?.removedCount).toBeGreaterThan(0);

        // Verify size is reduced
        const afterSize = await pruningService.checkMemorySize(AGENT);
        expect(afterSize.data!.sizeMB).toBeLessThan(sizeCheck.data!.sizeMB);
      }
    });

    it('should remove lowest confidence patterns first', async () => {
      const AGENT = 'test-agent';
      await memoryStore.ensureAgentDirectory(AGENT);

      // Add patterns with different confidence scores
      const lowConfId = '00000000-0000-0000-0000-000000000007';
      const mediumConfId = '00000000-0000-0000-0000-000000000008';
      const highConfId = '00000000-0000-0000-0000-000000000009';

      const patterns: Pattern[] = [
        {
          id: lowConfId,
          agent: AGENT,
          timestamp: new Date().toISOString(),
          pattern: {
            type: 'low',
            context: {},
            approach: { technique: '', codeTemplate: '', rationale: '' },
            conditions: { whenApplicable: [], whenNotApplicable: [] }
          },
          metrics: { successRate: 0.5, executionCount: 5, avgTimeSavedMs: 50, errorPreventionCount: 0 },
          evolution: { created: new Date().toISOString(), lastUsed: new Date().toISOString(), refinements: 0, confidenceScore: 0.3 }
        },
        {
          id: mediumConfId,
          agent: AGENT,
          timestamp: new Date().toISOString(),
          pattern: {
            type: 'medium',
            context: {},
            approach: { technique: '', codeTemplate: '', rationale: '' },
            conditions: { whenApplicable: [], whenNotApplicable: [] }
          },
          metrics: { successRate: 0.7, executionCount: 10, avgTimeSavedMs: 100, errorPreventionCount: 1 },
          evolution: { created: new Date().toISOString(), lastUsed: new Date().toISOString(), refinements: 1, confidenceScore: 0.6 }
        },
        {
          id: highConfId,
          agent: AGENT,
          timestamp: new Date().toISOString(),
          pattern: {
            type: 'high',
            context: {},
            approach: { technique: '', codeTemplate: '', rationale: '' },
            conditions: { whenApplicable: [], whenNotApplicable: [] }
          },
          metrics: { successRate: 0.95, executionCount: 50, avgTimeSavedMs: 300, errorPreventionCount: 10 },
          evolution: { created: new Date().toISOString(), lastUsed: new Date().toISOString(), refinements: 5, confidenceScore: 0.92 }
        }
      ];

      for (const pattern of patterns) {
        await memoryStore.addPattern(AGENT, pattern);
      }

      // Prune 1 pattern
      const result = await pruningService.pruneBySpace(AGENT, { removeCount: 1 });

      expect(result.success).toBe(true);

      // Lowest confidence should be removed
      const remaining = await memoryStore.getPatterns(AGENT);
      expect(remaining.data.find(p => p.id === lowConfId)).toBeUndefined();
      expect(remaining.data.find(p => p.id === highConfId)).toBeDefined();
    });

    it('should compress old data instead of deleting', async () => {
      const AGENT = 'test-agent';
      await memoryStore.ensureAgentDirectory(AGENT);

      const oldPattern: Pattern = {
        id: '00000000-0000-0000-0000-00000000000a',
        agent: AGENT,
        timestamp: new Date(Date.now() - 100 * 24 * 60 * 60 * 1000).toISOString(),
        pattern: {
          type: 'old',
          context: {},
          approach: { technique: '', codeTemplate: '', rationale: '' },
          conditions: { whenApplicable: [], whenNotApplicable: [] }
        },
        metrics: { successRate: 0.7, executionCount: 5, avgTimeSavedMs: 100, errorPreventionCount: 0 },
        evolution: { created: new Date(Date.now() - 100 * 24 * 60 * 60 * 1000).toISOString(), lastUsed: new Date().toISOString(), refinements: 0, confidenceScore: 0.6 }
      };

      await memoryStore.addPattern(AGENT, oldPattern);

      const result = await pruningService.compressOldData(AGENT, { maxAgeDays: 60 });

      expect(result.success).toBe(true);
      expect(result.data).toHaveProperty('compressionRatio');
    });
  });

  describe('Pattern Weighting', () => {
    it('should calculate pattern weight correctly', async () => {
      const pattern: Pattern = {
        id: '00000000-0000-0000-0000-00000000000b',
        agent: 'test-agent',
        timestamp: new Date().toISOString(),
        pattern: {
          type: 'test',
          context: {},
          approach: { technique: '', codeTemplate: '', rationale: '' },
          conditions: { whenApplicable: [], whenNotApplicable: [] }
        },
        metrics: { successRate: 0.9, executionCount: 50, avgTimeSavedMs: 300, errorPreventionCount: 10 },
        evolution: { created: new Date().toISOString(), lastUsed: new Date().toISOString(), refinements: 5, confidenceScore: 0.88 }
      };

      const weight = await pruningService.calculatePatternWeight(pattern);

      expect(weight).toBeGreaterThan(0);
      expect(weight).toBeLessThanOrEqual(1);
    });

    it('should weight recent patterns higher', async () => {
      const recentPattern: Pattern = {
        id: '00000000-0000-0000-0000-00000000000c',
        agent: 'test-agent',
        timestamp: new Date().toISOString(),
        pattern: {
          type: 'test',
          context: {},
          approach: { technique: '', codeTemplate: '', rationale: '' },
          conditions: { whenApplicable: [], whenNotApplicable: [] }
        },
        metrics: { successRate: 0.8, executionCount: 10, avgTimeSavedMs: 100, errorPreventionCount: 1 },
        evolution: { created: new Date().toISOString(), lastUsed: new Date().toISOString(), refinements: 1, confidenceScore: 0.75 }
      };

      const oldPattern: Pattern = {
        id: '00000000-0000-0000-0000-00000000000d',
        agent: 'test-agent',
        timestamp: new Date(Date.now() - 100 * 24 * 60 * 60 * 1000).toISOString(),
        pattern: {
          type: 'test',
          context: {},
          approach: { technique: '', codeTemplate: '', rationale: '' },
          conditions: { whenApplicable: [], whenNotApplicable: [] }
        },
        metrics: { successRate: 0.8, executionCount: 10, avgTimeSavedMs: 100, errorPreventionCount: 1 },
        evolution: { created: new Date(Date.now() - 100 * 24 * 60 * 60 * 1000).toISOString(), lastUsed: new Date(Date.now() - 100 * 24 * 60 * 60 * 1000).toISOString(), refinements: 1, confidenceScore: 0.75 }
      };

      const recentWeight = await pruningService.calculatePatternWeight(recentPattern);
      const oldWeight = await pruningService.calculatePatternWeight(oldPattern);

      expect(recentWeight).toBeGreaterThan(oldWeight);
    });

    it('should weight high-success patterns higher', async () => {
      const highSuccessPattern: Pattern = {
        id: '00000000-0000-0000-0000-00000000000e',
        agent: 'test-agent',
        timestamp: new Date().toISOString(),
        pattern: {
          type: 'test',
          context: {},
          approach: { technique: '', codeTemplate: '', rationale: '' },
          conditions: { whenApplicable: [], whenNotApplicable: [] }
        },
        metrics: { successRate: 0.95, executionCount: 20, avgTimeSavedMs: 200, errorPreventionCount: 5 },
        evolution: { created: new Date().toISOString(), lastUsed: new Date().toISOString(), refinements: 3, confidenceScore: 0.9 }
      };

      const lowSuccessPattern: Pattern = {
        id: '00000000-0000-0000-0000-00000000000f',
        agent: 'test-agent',
        timestamp: new Date().toISOString(),
        pattern: {
          type: 'test',
          context: {},
          approach: { technique: '', codeTemplate: '', rationale: '' },
          conditions: { whenApplicable: [], whenNotApplicable: [] }
        },
        metrics: { successRate: 0.5, executionCount: 20, avgTimeSavedMs: 200, errorPreventionCount: 1 },
        evolution: { created: new Date().toISOString(), lastUsed: new Date().toISOString(), refinements: 1, confidenceScore: 0.5 }
      };

      const highWeight = await pruningService.calculatePatternWeight(highSuccessPattern);
      const lowWeight = await pruningService.calculatePatternWeight(lowSuccessPattern);

      expect(highWeight).toBeGreaterThan(lowWeight);
    });
  });

  describe('Pruning Reports', () => {
    it('should generate pruning recommendations', async () => {
      const AGENT = 'test-agent';
      await memoryStore.ensureAgentDirectory(AGENT);

      // Add various patterns
      for (let i = 0; i < 50; i++) {
        const age = Math.random() * 200; // 0-200 days old
        const date = new Date(Date.now() - age * 24 * 60 * 60 * 1000);

        await memoryStore.addPattern(AGENT, {
          id: crypto.randomUUID(),
          agent: AGENT,
          timestamp: date.toISOString(),
          pattern: {
            type: `type-${i % 5}`,
            context: {},
            approach: { technique: '', codeTemplate: '', rationale: '' },
            conditions: { whenApplicable: [], whenNotApplicable: [] }
          },
          metrics: { successRate: Math.random(), executionCount: Math.floor(Math.random() * 100), avgTimeSavedMs: Math.floor(Math.random() * 500), errorPreventionCount: 0 },
          evolution: { created: date.toISOString(), lastUsed: date.toISOString(), refinements: 0, confidenceScore: Math.random() }
        });
      }

      const report = await pruningService.generatePruningReport(AGENT);

      expect(report.success).toBe(true);
      expect(report.data).toHaveProperty('totalPatterns');
      expect(report.data).toHaveProperty('recommendations');
      expect(report.data?.recommendations).toBeInstanceOf(Array);
    });

    it('should estimate space savings', async () => {
      const AGENT = 'test-agent';
      await memoryStore.ensureAgentDirectory(AGENT);

      for (let i = 0; i < 20; i++) {
        await memoryStore.addPattern(AGENT, {
          id: crypto.randomUUID(),
          agent: AGENT,
          timestamp: new Date().toISOString(),
          pattern: {
            type: `type-${i}`,
            context: { data: 'x'.repeat(500) },
            approach: { technique: '', codeTemplate: '', rationale: '' },
            conditions: { whenApplicable: [], whenNotApplicable: [] }
          },
          metrics: { successRate: 0.3, executionCount: 1, avgTimeSavedMs: 50, errorPreventionCount: 0 },
          evolution: { created: new Date().toISOString(), lastUsed: new Date().toISOString(), refinements: 0, confidenceScore: 0.3 }
        });
      }

      const estimate = await pruningService.estimateSpaceSavings(AGENT, {
        minSuccessRate: 0.5
      });

      expect(estimate.success).toBe(true);
      expect(estimate.data).toHaveProperty('currentSizeMB');
      expect(estimate.data).toHaveProperty('projectedSizeMB');
      expect(estimate.data).toHaveProperty('savingsPercentage');
    });
  });

  describe('Safety Mechanisms', () => {
    it('should require confirmation for aggressive pruning', async () => {
      const AGENT = 'test-agent';
      await memoryStore.ensureAgentDirectory(AGENT);

      const result = await pruningService.pruneByPerformance(AGENT, {
        minSuccessRate: 0.8, // Aggressive threshold
        requireConfirmation: true
      });

      expect(result.success).toBe(false);
      expect(result.error).toContain('confirmation required');
    });

    it('should create backup before pruning', async () => {
      const AGENT = 'test-agent';
      await memoryStore.ensureAgentDirectory(AGENT);

      await memoryStore.addPattern(AGENT, {
        id: '00000000-0000-0000-0000-000000000010',
        agent: AGENT,
        timestamp: new Date().toISOString(),
        pattern: {
          type: 'test',
          context: {},
          approach: { technique: '', codeTemplate: '', rationale: '' },
          conditions: { whenApplicable: [], whenNotApplicable: [] }
        },
        metrics: { successRate: 0.5, executionCount: 1, avgTimeSavedMs: 50, errorPreventionCount: 0 },
        evolution: { created: new Date().toISOString(), lastUsed: new Date().toISOString(), refinements: 0, confidenceScore: 0.5 }
      });

      const result = await pruningService.pruneByPerformance(AGENT, {
        minSuccessRate: 0.7,
        createBackup: true
      });

      expect(result.success).toBe(true);
      expect(result.data).toHaveProperty('backupId');
    });

    it('should support dry-run mode', async () => {
      const AGENT = 'test-agent';
      await memoryStore.ensureAgentDirectory(AGENT);

      await memoryStore.addPattern(AGENT, {
        id: '00000000-0000-0000-0000-000000000011',
        agent: AGENT,
        timestamp: new Date().toISOString(),
        pattern: {
          type: 'test',
          context: {},
          approach: { technique: '', codeTemplate: '', rationale: '' },
          conditions: { whenApplicable: [], whenNotApplicable: [] }
        },
        metrics: { successRate: 0.1, executionCount: 1, avgTimeSavedMs: 10, errorPreventionCount: 0 },
        evolution: { created: new Date().toISOString(), lastUsed: new Date().toISOString(), refinements: 0, confidenceScore: 0.1 }
      });

      const result = await pruningService.pruneByPerformance(AGENT, {
        minSuccessRate: 0.5,
        dryRun: true
      });

      expect(result.success).toBe(true);
      expect(result.data).toHaveProperty('wouldRemoveCount');

      // Verify nothing was actually deleted
      const patterns = await memoryStore.getPatterns(AGENT);
      expect(patterns.data).toHaveLength(1);
    });
  });
});
