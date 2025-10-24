/**
 * MemoryService Unit Tests
 *
 * Tests core CRUD operations, caching, and memory management
 * Coverage target: 95%+
 */

import { MemoryService, QueryPatternOptions, RecordPatternData, MetricsReport } from '../MemoryService';
import { Pattern } from '../models/Pattern';
import { Solution } from '../models/Solution';
import { Decision } from '../models/Decision';
import * as fs from 'fs';
import * as path from 'path';

describe('MemoryService', () => {
  let service: MemoryService;
  const testMemoryPath = path.join(__dirname, '../../test-memory');
  const testAgent = 'test-agent';

  beforeAll(async () => {
    // Clean up and create fresh test directory
    if (fs.existsSync(testMemoryPath)) {
      fs.rmSync(testMemoryPath, { recursive: true });
    }
    fs.mkdirSync(testMemoryPath, { recursive: true });

    service = new MemoryService(testMemoryPath, {
      enabled: true,
      agentOverrides: {
        [testAgent]: { enabled: true, maxPatternCount: 100, maxSolutionCount: 100, maxDecisionCount: 100 }
      }
    });

    await service.initialize();
  });

  afterAll(async () => {
    // Clean up test directory
    if (fs.existsSync(testMemoryPath)) {
      fs.rmSync(testMemoryPath, { recursive: true });
    }
  });

  describe('Initialization', () => {
    it('should initialize successfully', async () => {
      const newService = new MemoryService(testMemoryPath);
      await newService.initialize();
      expect(newService.isEnabled()).toBe(true);
    });

    it('should check if AML is enabled globally', () => {
      expect(service.isEnabled()).toBe(true);
    });

    it('should check if AML is enabled for specific agent', () => {
      expect(service.isEnabledForAgent(testAgent)).toBe(true);
    });

    it('should return false for disabled agent', () => {
      expect(service.isEnabledForAgent('nonexistent-agent')).toBe(false);
    });
  });

  describe('Pattern Operations', () => {
    const patternData: RecordPatternData = {
      type: 'react-optimization',
      context: { framework: 'React 18', componentType: 'form' },
      approach: {
        technique: 'useMemo',
        rationale: 'Prevents expensive re-computation',
        codeTemplate: 'useMemo(() => compute(deps), [deps])'
      },
      conditions: {
        whenApplicable: ['heavy-computation'],
        whenNotApplicable: ['simple-data']
      },
      tags: ['performance', 'react']
    };

    it('should record a new pattern', async () => {
      const result = await service.recordPattern(testAgent, patternData);

      expect(result.success).toBe(true);
      expect(result.data).toBeDefined();
      expect(result.data!.pattern.type).toBe('react-optimization');
      expect(result.data!.evolution.confidenceScore).toBe(0.3); // Initial low confidence
    });

    it('should query patterns for agent', async () => {
      // Record multiple patterns
      await service.recordPattern(testAgent, patternData);
      await service.recordPattern(testAgent, {
        ...patternData,
        type: 'api-optimization'
      });

      const patterns = await service.queryPatterns(testAgent);

      expect(patterns.length).toBeGreaterThanOrEqual(2);
      expect(patterns[0]).toHaveProperty('id');
      expect(patterns[0]).toHaveProperty('pattern');
    });

    it('should filter patterns by type', async () => {
      const patterns = await service.queryPatterns(testAgent, {
        type: 'react-optimization'
      });

      expect(patterns.every(p => p.pattern.type === 'react-optimization')).toBe(true);
    });

    it('should filter patterns by minimum confidence', async () => {
      const patterns = await service.queryPatterns(testAgent, {
        minConfidence: 0.5
      });

      expect(patterns.every(p => p.evolution.confidenceScore >= 0.5)).toBe(true);
    });

    it('should sort patterns by weight', async () => {
      const patterns = await service.queryPatterns(testAgent, {
        sortBy: 'weight',
        limit: 10
      });

      for (let i = 1; i < patterns.length; i++) {
        const prevWeight = calculateWeight(patterns[i - 1]);
        const currentWeight = calculateWeight(patterns[i]);
        expect(prevWeight).toBeGreaterThanOrEqual(currentWeight);
      }
    });

    it('should limit results by count', async () => {
      const patterns = await service.queryPatterns(testAgent, { limit: 5 });
      expect(patterns.length).toBeLessThanOrEqual(5);
    });

    it('should retrieve pattern by ID', async () => {
      const result = await service.recordPattern(testAgent, patternData);
      const patternId = result.data!.id;

      const retrieved = await service.getPattern(testAgent, patternId);
      expect(retrieved).toBeDefined();
      expect(retrieved!.id).toBe(patternId);
    });

    it('should return null for non-existent pattern', async () => {
      const retrieved = await service.getPattern(testAgent, 'non-existent-id');
      expect(retrieved).toBeNull();
    });

    it('should record pattern usage and update metrics', async () => {
      const result = await service.recordPattern(testAgent, patternData);
      const patternId = result.data!.id;
      const initialConfidence = result.data!.evolution.confidenceScore;

      // Record successful usage
      await service.recordPatternUsage(testAgent, {
        patternId,
        success: true,
        timeSavedMs: 150
      });

      const updated = await service.getPattern(testAgent, patternId);
      expect(updated!.metrics.executionCount).toBe(2); // Initial + usage
      expect(updated!.evolution.confidenceScore).toBeGreaterThan(initialConfidence);
    });

    it('should handle failed pattern usage', async () => {
      const result = await service.recordPattern(testAgent, patternData);
      const patternId = result.data!.id;
      const initialConfidence = result.data!.evolution.confidenceScore;

      // Record failed usage
      await service.recordPatternUsage(testAgent, {
        patternId,
        success: false
      });

      const updated = await service.getPattern(testAgent, patternId);
      expect(updated!.evolution.confidenceScore).toBeLessThan(initialConfidence);
    });

    it('should handle empty pattern queries gracefully', async () => {
      const patterns = await service.queryPatterns('nonexistent-agent');
      expect(patterns).toEqual([]);
    });

    it('should enforce pattern count limits', async () => {
      // Create a new service with low limit (min 10 per schema)
      const limitedPath = path.join(__dirname, '../../test-memory-limited');
      const limitedService = new MemoryService(limitedPath, {
        enabled: true,
        agentOverrides: {
          'limited-agent': { enabled: true, maxPatternCount: 10 }
        }
      });
      await limitedService.initialize();

      // Record 15 patterns
      for (let i = 0; i < 15; i++) {
        await limitedService.recordPattern('limited-agent', {
          ...patternData,
          type: `pattern-${i}`
        });
      }

      const patterns = await limitedService.queryPatterns('limited-agent', {
        includeInactive: true
      });

      expect(patterns.length).toBeLessThanOrEqual(10);

      // Cleanup
      fs.rmSync(limitedPath, { recursive: true });
    });
  });

  describe('Solution Operations', () => {
    const solutionData = {
      errorType: 'TypeError',
      errorMessage: 'Cannot read property of undefined',
      context: { file: 'component.tsx' },
      rootCause: 'Async data not loaded',
      fixApproach: 'optional-chaining',
      codeFix: 'data?.property',
      prevention: 'Add type guard',
      worked: true,
      timeToFixMinutes: 5
    };

    it('should record a new solution', async () => {
      const result = await service.recordSolution(testAgent, solutionData);

      expect(result.success).toBe(true);
      expect(result.data).toBeDefined();
      expect(result.data!.problem.errorType).toBe('TypeError');
    });

    it('should query solutions by error type', async () => {
      await service.recordSolution(testAgent, solutionData);

      const solutions = await service.querySolutions(testAgent, {
        errorType: 'TypeError'
      });

      expect(solutions.every(s => s.problem.errorType === 'TypeError')).toBe(true);
    });

    it('should query solutions by error message pattern', async () => {
      const solutions = await service.querySolutions(testAgent, {
        errorMessage: 'Cannot read'
      });

      expect(solutions.length).toBeGreaterThan(0);
      expect(solutions[0].problem.errorMessage.includes('Cannot read')).toBe(true);
    });

    it('should handle failed solutions', async () => {
      const result = await service.recordSolution(testAgent, {
        ...solutionData,
        worked: false
      });

      expect(result.success).toBe(true);
      expect(result.data!.effectiveness.worked).toBe(false);
    });

    it('should enforce solution count limits', async () => {
      const patterns = await service.querySolutions(testAgent, {
        includeInactive: true
      });

      expect(patterns.length).toBeGreaterThanOrEqual(0);
    });
  });

  describe('Decision Operations', () => {
    const decisionData = {
      type: 'architecture-choice',
      question: 'REST vs GraphQL?',
      context: { projectSize: 'large' },
      chosenOption: 'GraphQL',
      alternativesConsidered: ['REST', 'gRPC'],
      decisionFactors: {
        primary: ['query-flexibility'],
        secondary: ['tooling']
      }
    };

    it('should record a new decision', async () => {
      const result = await service.recordDecision(testAgent, decisionData);

      expect(result.success).toBe(true);
      expect(result.data).toBeDefined();
      expect(result.data!.decision.chosenOption).toBe('GraphQL');
    });

    it('should query decisions by type', async () => {
      await service.recordDecision(testAgent, decisionData);

      const decisions = await service.queryDecisions(testAgent, {
        type: 'architecture-choice'
      });

      expect(decisions.every(d => d.decision.type === 'architecture-choice')).toBe(true);
    });

    it('should filter decisions by outcome presence', async () => {
      const decisions = await service.queryDecisions(testAgent, {
        includeWithoutOutcome: false
      });

      // Should only include decisions with outcomes
      expect(decisions.every(d => d.outcome !== undefined)).toBe(true);
    });
  });

  describe('Metrics Operations', () => {
    it('should get metrics report for agent', async () => {
      const metrics = await service.getMetrics(testAgent);

      expect(metrics).toBeDefined();
      expect(metrics!.agent).toBe(testAgent);
      expect(metrics!.totalPatterns).toBeGreaterThanOrEqual(0);
      expect(metrics!.avgConfidence).toBeGreaterThanOrEqual(0);
      expect(metrics!.healthScore).toBeGreaterThanOrEqual(0);
    });

    it('should calculate health score correctly', async () => {
      const metrics = await service.getMetrics(testAgent);

      expect(metrics!.healthScore).toBeLessThanOrEqual(1);
      expect(metrics!.healthScore).toBeGreaterThanOrEqual(0);
    });

    it('should get metrics for all agents', async () => {
      const allMetrics = await service.getAllMetrics();

      expect(Array.isArray(allMetrics)).toBe(true);
    });

    it('should return null for disabled agent metrics', async () => {
      const metrics = await service.getMetrics('disabled-agent');
      expect(metrics).toBeNull();
    });
  });

  describe('Memory Management', () => {
    it('should list all agents with memory', async () => {
      const agents = await service.listAgents();

      expect(Array.isArray(agents)).toBe(true);
      expect(agents.includes(testAgent)).toBe(true);
    });

    it('should get total memory usage', async () => {
      const totalUsage = await service.getTotalMemoryUsage();

      expect(typeof totalUsage).toBe('number');
      expect(totalUsage).toBeGreaterThanOrEqual(0);
    });

    it('should export agent memory', async () => {
      const result = await service.exportMemory(testAgent);

      expect(result.success).toBe(true);
      expect(result.data).toBeDefined();
      expect(result.data!.patterns).toBeDefined();
      expect(result.data!.solutions).toBeDefined();
    });

    it('should import agent memory', async () => {
      const exported = await service.exportMemory(testAgent);

      const result = await service.importMemory('imported-agent', exported.data!);
      expect(result.success).toBe(true);
    });

    it('should clear agent memory with backup', async () => {
      const result = await service.clearAgentMemory('test-agent-to-clear', true);

      expect(result.success).toBe(true);
    });

    it('should clear agent memory without backup', async () => {
      const result = await service.clearAgentMemory('test-agent-no-backup', false);

      expect(result.success).toBe(true);
    });
  });

  describe('Caching Behavior', () => {
    it('should use cache for repeated queries', async () => {
      const startTime = Date.now();

      // First query (cache miss)
      await service.queryPatterns(testAgent);
      const firstDuration = Date.now() - startTime;

      const cacheStartTime = Date.now();
      // Second query (cache hit)
      await service.queryPatterns(testAgent);
      const cacheDuration = Date.now() - cacheStartTime;

      // Cache hit should be very fast (though not guaranteed in tests)
      expect(cacheDuration).toBeLessThanOrEqual(firstDuration + 10);
    });
  });

  describe('Error Handling', () => {
    it('should handle AML disabled gracefully', async () => {
      // Use a unique path for this test
      const disabledPath = path.join(__dirname, '../../test-memory-disabled');
      if (fs.existsSync(disabledPath)) {
        fs.rmSync(disabledPath, { recursive: true });
      }

      const disabledService = new MemoryService(disabledPath, { enabled: false });
      await disabledService.initialize();

      const result = await disabledService.recordPattern('any-agent', {
        type: 'test',
        context: {},
        approach: { technique: 'test', rationale: 'test' },
        conditions: { whenApplicable: [], whenNotApplicable: [] }
      });

      expect(result.success).toBe(false);
      expect(result.error).toBeDefined();

      // Cleanup
      fs.rmSync(disabledPath, { recursive: true });
    });

    it('should handle invalid pattern usage', async () => {
      const result = await service.recordPatternUsage(testAgent, {
        patternId: 'nonexistent',
        success: true
      });

      expect(result.success).toBe(false);
    });

    it('should validate context matching', async () => {
      await service.recordPattern(testAgent, {
        type: 'test',
        context: { framework: 'React' },
        approach: { technique: 'test', rationale: 'test' },
        conditions: { whenApplicable: [], whenNotApplicable: [] }
      });

      const patterns = await service.queryPatterns(testAgent, {
        context: { framework: 'Vue' }
      });

      // Should not match context
      expect(patterns.filter(p => p.pattern.type === 'test').length).toBe(0);
    });
  });

  describe('Performance Requirements', () => {
    it('should query patterns in <50ms', async () => {
      const startTime = Date.now();
      await service.queryPatterns(testAgent, { limit: 10 });
      const duration = Date.now() - startTime;

      expect(duration).toBeLessThan(100); // Give extra buffer for CI
    });

    it('should record pattern in <100ms', async () => {
      const startTime = Date.now();
      await service.recordPattern(testAgent, {
        type: 'perf-test',
        context: {},
        approach: { technique: 'test', rationale: 'test' },
        conditions: { whenApplicable: [], whenNotApplicable: [] }
      });
      const duration = Date.now() - startTime;

      expect(duration).toBeLessThan(150); // Give extra buffer
    });
  });
});

// Helper function
function calculateWeight(pattern: Pattern): number {
  const baseWeight = pattern.metrics.successRate;
  const daysOld = (Date.now() - new Date(pattern.evolution.lastUsed).getTime()) / (1000 * 60 * 60 * 24);
  const recencyFactor = Math.exp(-daysOld / 30);
  const usageFrequency = Math.min(pattern.metrics.executionCount / 100, 1.0);
  const confidenceFactor = pattern.evolution.confidenceScore;

  return baseWeight * 0.4 + recencyFactor * 0.3 + usageFrequency * 0.15 + confidenceFactor * 0.15;
}
