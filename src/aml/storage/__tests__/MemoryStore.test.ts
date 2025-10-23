/**
 * MemoryStore Test Suite
 *
 * Tests the high-level memory store operations including:
 * - Agent memory CRUD operations
 * - Pattern, solution, and decision management
 * - Global data operations
 * - Backup and restore
 */

import { describe, it, expect, beforeEach, afterEach } from '@jest/globals';
import * as fs from 'fs/promises';
import * as path from 'path';
import { MemoryStore } from '../MemoryStore';
import { Pattern, Solution, Decision } from '../../models';

const TEST_MEMORY_DIR = path.join(__dirname, '../../__test_data__/memory-store');

describe('MemoryStore', () => {
  let store: MemoryStore;

  beforeEach(async () => {
    // Clean up test directory
    await fs.rm(TEST_MEMORY_DIR, { recursive: true, force: true });
    await fs.mkdir(TEST_MEMORY_DIR, { recursive: true });

    store = new MemoryStore(TEST_MEMORY_DIR);
    await store.initialize();
  });

  afterEach(async () => {
    // Clean up test directory
    await fs.rm(TEST_MEMORY_DIR, { recursive: true, force: true });
  });

  describe('Initialization', () => {
    it('should create directory structure on initialization', async () => {
      const dirs = await fs.readdir(TEST_MEMORY_DIR);

      expect(dirs).toContain('global');
      expect(dirs).toContain('audit');
      expect(dirs).toContain('backup');
    });

    it('should create config file', async () => {
      const configPath = path.join(TEST_MEMORY_DIR, 'config.json');
      await fs.access(configPath); // Should not throw

      const config = JSON.parse(await fs.readFile(configPath, 'utf-8'));
      expect(config).toHaveProperty('version');
      expect(config).toHaveProperty('enabled');
    });

    it('should handle existing directory gracefully', async () => {
      // Initialize twice
      const store2 = new MemoryStore(TEST_MEMORY_DIR);
      await expect(store2.initialize()).resolves.not.toThrow();
    });
  });

  describe('Agent Memory Management', () => {
    const AGENT = 'frontend-developer';

    it('should create agent memory directory', async () => {
      await store.ensureAgentDirectory(AGENT);

      const agentDir = path.join(TEST_MEMORY_DIR, AGENT);
      await fs.access(agentDir); // Should not throw

      const files = await fs.readdir(agentDir);
      expect(files).toContain('patterns.json');
      expect(files).toContain('solutions.json');
      expect(files).toContain('decisions.json');
      expect(files).toContain('metrics.json');
    });

    it('should initialize empty memory files', async () => {
      await store.ensureAgentDirectory(AGENT);

      const patterns = await store.getPatterns(AGENT);
      const solutions = await store.getSolutions(AGENT);
      const decisions = await store.getDecisions(AGENT);

      expect(patterns.data).toEqual([]);
      expect(solutions.data).toEqual([]);
      expect(decisions.data).toEqual([]);
    });

    it('should list all agents', async () => {
      await store.ensureAgentDirectory('frontend-developer');
      await store.ensureAgentDirectory('backend-architect');
      await store.ensureAgentDirectory('test-automator');

      const agents = await store.listAgents();

      expect(agents.data).toHaveLength(3);
      expect(agents.data).toContain('frontend-developer');
      expect(agents.data).toContain('backend-architect');
      expect(agents.data).toContain('test-automator');
    });
  });

  describe('Pattern Operations', () => {
    const AGENT = 'frontend-developer';

    beforeEach(async () => {
      await store.ensureAgentDirectory(AGENT);
    });

    it('should add pattern', async () => {
      const pattern: Pattern = {
        id: 'pattern-1',
        agent: AGENT,
        timestamp: new Date().toISOString(),
        pattern: {
          type: 'react-optimization',
          context: { framework: 'React 18' },
          approach: {
            technique: 'useMemo',
            codeTemplate: 'const memoized = useMemo(() => compute(deps), [deps])',
            rationale: 'Prevents expensive re-computations'
          },
          conditions: {
            whenApplicable: ['heavy-computation'],
            whenNotApplicable: ['simple-components']
          }
        },
        metrics: {
          successRate: 0.95,
          executionCount: 10,
          avgTimeSavedMs: 230,
          errorPreventionCount: 2
        },
        evolution: {
          created: new Date().toISOString(),
          lastUsed: new Date().toISOString(),
          refinements: 0,
          confidenceScore: 0.85
        }
      };

      const result = await store.addPattern(AGENT, pattern);

      expect(result.success).toBe(true);

      // Verify it was saved
      const patterns = await store.getPatterns(AGENT);
      expect(patterns.data).toHaveLength(1);
      expect(patterns.data[0].id).toBe('pattern-1');
    });

    it('should get patterns for agent', async () => {
      const patterns: Pattern[] = [
        {
          id: 'p1',
          agent: AGENT,
          timestamp: new Date().toISOString(),
          pattern: {
            type: 'react-optimization',
            context: {},
            approach: { technique: 'useMemo', codeTemplate: '', rationale: '' },
            conditions: { whenApplicable: [], whenNotApplicable: [] }
          },
          metrics: { successRate: 0.9, executionCount: 5, avgTimeSavedMs: 100, errorPreventionCount: 0 },
          evolution: { created: new Date().toISOString(), lastUsed: new Date().toISOString(), refinements: 0, confidenceScore: 0.8 }
        },
        {
          id: 'p2',
          agent: AGENT,
          timestamp: new Date().toISOString(),
          pattern: {
            type: 'state-management',
            context: {},
            approach: { technique: 'useState', codeTemplate: '', rationale: '' },
            conditions: { whenApplicable: [], whenNotApplicable: [] }
          },
          metrics: { successRate: 0.85, executionCount: 8, avgTimeSavedMs: 150, errorPreventionCount: 1 },
          evolution: { created: new Date().toISOString(), lastUsed: new Date().toISOString(), refinements: 1, confidenceScore: 0.75 }
        }
      ];

      for (const pattern of patterns) {
        await store.addPattern(AGENT, pattern);
      }

      const result = await store.getPatterns(AGENT);

      expect(result.success).toBe(true);
      expect(result.data).toHaveLength(2);
    });

    it('should update existing pattern', async () => {
      const pattern: Pattern = {
        id: 'p1',
        agent: AGENT,
        timestamp: new Date().toISOString(),
        pattern: {
          type: 'test-pattern',
          context: {},
          approach: { technique: 'old', codeTemplate: '', rationale: '' },
          conditions: { whenApplicable: [], whenNotApplicable: [] }
        },
        metrics: { successRate: 0.5, executionCount: 1, avgTimeSavedMs: 50, errorPreventionCount: 0 },
        evolution: { created: new Date().toISOString(), lastUsed: new Date().toISOString(), refinements: 0, confidenceScore: 0.5 }
      };

      await store.addPattern(AGENT, pattern);

      // Update pattern
      pattern.pattern.approach.technique = 'new';
      pattern.metrics.successRate = 0.9;
      pattern.evolution.confidenceScore = 0.85;

      await store.updatePattern(AGENT, pattern);

      const result = await store.getPatterns(AGENT);
      const updated = result.data.find(p => p.id === 'p1');

      expect(updated?.pattern.approach.technique).toBe('new');
      expect(updated?.metrics.successRate).toBe(0.9);
      expect(updated?.evolution.confidenceScore).toBe(0.85);
    });

    it('should delete pattern', async () => {
      const pattern: Pattern = {
        id: 'p1',
        agent: AGENT,
        timestamp: new Date().toISOString(),
        pattern: {
          type: 'test',
          context: {},
          approach: { technique: '', codeTemplate: '', rationale: '' },
          conditions: { whenApplicable: [], whenNotApplicable: [] }
        },
        metrics: { successRate: 0.5, executionCount: 1, avgTimeSavedMs: 0, errorPreventionCount: 0 },
        evolution: { created: new Date().toISOString(), lastUsed: new Date().toISOString(), refinements: 0, confidenceScore: 0.5 }
      };

      await store.addPattern(AGENT, pattern);

      const deleteResult = await store.deletePattern(AGENT, 'p1');

      expect(deleteResult.success).toBe(true);

      const patterns = await store.getPatterns(AGENT);
      expect(patterns.data).toHaveLength(0);
    });
  });

  describe('Solution Operations', () => {
    const AGENT = 'debugger';

    beforeEach(async () => {
      await store.ensureAgentDirectory(AGENT);
    });

    it('should add solution', async () => {
      const solution: Solution = {
        id: 'sol-1',
        agent: AGENT,
        timestamp: new Date().toISOString(),
        problem: {
          errorType: 'TypeError',
          errorMessage: 'Cannot read property of undefined',
          stackTraceHash: 'abc123',
          context: { fileType: 'typescript', framework: 'React' }
        },
        solution: {
          rootCause: 'Async data not loaded',
          fixApproach: 'optional-chaining',
          codeFix: 'const value = data?.x ?? defaultValue',
          prevention: 'TypeScript strict null checks'
        },
        effectiveness: {
          worked: true,
          timeToFixMinutes: 5,
          preventedRecurrence: 3,
          relatedErrorsFixed: 1
        }
      };

      const result = await store.addSolution(AGENT, solution);

      expect(result.success).toBe(true);

      const solutions = await store.getSolutions(AGENT);
      expect(solutions.data).toHaveLength(1);
      expect(solutions.data[0].id).toBe('sol-1');
    });

    it('should find solution by error signature', async () => {
      const solution: Solution = {
        id: 'sol-1',
        agent: AGENT,
        timestamp: new Date().toISOString(),
        problem: {
          errorType: 'TypeError',
          errorMessage: 'Cannot read property of undefined',
          stackTraceHash: 'abc123',
          context: {}
        },
        solution: {
          rootCause: 'Null reference',
          fixApproach: 'null-check',
          codeFix: 'if (obj) { ... }',
          prevention: 'Defensive programming'
        },
        effectiveness: {
          worked: true,
          timeToFixMinutes: 2,
          preventedRecurrence: 5,
          relatedErrorsFixed: 2
        }
      };

      await store.addSolution(AGENT, solution);

      // Search for similar error
      const solutions = await store.getSolutions(AGENT);
      const found = solutions.data.find(s =>
        s.problem.errorType === 'TypeError' &&
        s.problem.errorMessage.includes('Cannot read property')
      );

      expect(found).toBeDefined();
      expect(found?.solution.fixApproach).toBe('null-check');
    });
  });

  describe('Decision Operations', () => {
    const AGENT = 'backend-architect';

    beforeEach(async () => {
      await store.ensureAgentDirectory(AGENT);
    });

    it('should add decision', async () => {
      const decision: Decision = {
        id: 'dec-1',
        agent: AGENT,
        timestamp: new Date().toISOString(),
        decision: {
          type: 'architecture-choice',
          question: 'REST vs GraphQL',
          context: { projectSize: 'large', teamSize: 8 },
          chosenOption: 'GraphQL',
          alternativesConsidered: ['REST', 'gRPC'],
          decisionFactors: {
            primary: ['query-flexibility'],
            secondary: ['tooling-maturity']
          }
        },
        outcome: {
          successMetrics: {
            developmentSpeed: 1.2,
            apiPerformance: 0.9,
            clientSatisfaction: 0.85
          },
          lessonsLearned: ['Requires training', 'Caching is crucial'],
          wouldRepeat: true
        }
      };

      const result = await store.addDecision(AGENT, decision);

      expect(result.success).toBe(true);

      const decisions = await store.getDecisions(AGENT);
      expect(decisions.data).toHaveLength(1);
    });

    it('should track decision outcomes', async () => {
      const decision: Decision = {
        id: 'dec-1',
        agent: AGENT,
        timestamp: new Date().toISOString(),
        decision: {
          type: 'database-choice',
          question: 'SQL vs NoSQL',
          context: {},
          chosenOption: 'PostgreSQL',
          alternativesConsidered: ['MongoDB'],
          decisionFactors: { primary: ['ACID'], secondary: [] }
        },
        outcome: {
          successMetrics: { reliability: 0.99 },
          lessonsLearned: [],
          wouldRepeat: true
        }
      };

      await store.addDecision(AGENT, decision);

      const decisions = await store.getDecisions(AGENT);
      const found = decisions.data.find(d => d.id === 'dec-1');

      expect(found?.outcome.wouldRepeat).toBe(true);
      expect(found?.outcome.successMetrics.reliability).toBe(0.99);
    });
  });

  describe('Global Data Operations', () => {
    it('should store cross-agent patterns', async () => {
      const crossAgentData = {
        sharedPatterns: [
          { patternId: 'p1', usedBy: ['frontend-developer', 'mobile-developer'] }
        ]
      };

      await store.setGlobalData('cross-agent', crossAgentData);

      const result = await store.getGlobalData('cross-agent');

      expect(result.success).toBe(true);
      expect(result.data).toEqual(crossAgentData);
    });

    it('should store project metadata', async () => {
      const metadata = {
        projectName: 'TestProject',
        framework: 'React',
        startDate: '2025-01-01'
      };

      await store.setGlobalData('project-meta', metadata);

      const result = await store.getGlobalData('project-meta');

      expect(result.data).toEqual(metadata);
    });
  });

  describe('Backup and Restore', () => {
    const AGENT = 'frontend-developer';

    it('should create backup of agent memory', async () => {
      await store.ensureAgentDirectory(AGENT);

      // Add some data
      const pattern: Pattern = {
        id: 'p1',
        agent: AGENT,
        timestamp: new Date().toISOString(),
        pattern: {
          type: 'test',
          context: {},
          approach: { technique: '', codeTemplate: '', rationale: '' },
          conditions: { whenApplicable: [], whenNotApplicable: [] }
        },
        metrics: { successRate: 0.8, executionCount: 3, avgTimeSavedMs: 100, errorPreventionCount: 0 },
        evolution: { created: new Date().toISOString(), lastUsed: new Date().toISOString(), refinements: 0, confidenceScore: 0.7 }
      };
      await store.addPattern(AGENT, pattern);

      const backupResult = await store.backupAgentMemory(AGENT);

      expect(backupResult.success).toBe(true);
      expect(backupResult.data).toHaveProperty('backupId');

      // Verify backup file exists
      const backupDir = path.join(TEST_MEMORY_DIR, 'backup');
      const backups = await fs.readdir(backupDir);
      expect(backups.length).toBeGreaterThan(0);
    });

    it('should restore from backup', async () => {
      await store.ensureAgentDirectory(AGENT);

      // Create original data
      const pattern: Pattern = {
        id: 'original',
        agent: AGENT,
        timestamp: new Date().toISOString(),
        pattern: {
          type: 'original-pattern',
          context: {},
          approach: { technique: 'original', codeTemplate: '', rationale: '' },
          conditions: { whenApplicable: [], whenNotApplicable: [] }
        },
        metrics: { successRate: 0.9, executionCount: 5, avgTimeSavedMs: 200, errorPreventionCount: 1 },
        evolution: { created: new Date().toISOString(), lastUsed: new Date().toISOString(), refinements: 0, confidenceScore: 0.85 }
      };
      await store.addPattern(AGENT, pattern);

      // Create backup
      const backup = await store.backupAgentMemory(AGENT);

      // Modify data
      await store.deletePattern(AGENT, 'original');

      // Restore from backup
      const restoreResult = await store.restoreAgentMemory(AGENT, backup.data!.backupId);

      expect(restoreResult.success).toBe(true);

      // Verify original data is back
      const patterns = await store.getPatterns(AGENT);
      const restored = patterns.data.find(p => p.id === 'original');
      expect(restored).toBeDefined();
      expect(restored?.pattern.type).toBe('original-pattern');
    });
  });

  describe('Performance', () => {
    it('should handle large number of patterns', async () => {
      const AGENT = 'test-agent';
      await store.ensureAgentDirectory(AGENT);

      const patterns: Pattern[] = Array.from({ length: 1000 }, (_, i) => ({
        id: `pattern-${i}`,
        agent: AGENT,
        timestamp: new Date().toISOString(),
        pattern: {
          type: `type-${i % 10}`,
          context: { index: i },
          approach: { technique: `tech-${i}`, codeTemplate: '', rationale: '' },
          conditions: { whenApplicable: [], whenNotApplicable: [] }
        },
        metrics: { successRate: Math.random(), executionCount: i, avgTimeSavedMs: i * 10, errorPreventionCount: 0 },
        evolution: { created: new Date().toISOString(), lastUsed: new Date().toISOString(), refinements: 0, confidenceScore: Math.random() }
      }));

      // Batch add patterns
      const start = Date.now();
      for (const pattern of patterns) {
        await store.addPattern(AGENT, pattern);
      }
      const duration = Date.now() - start;

      // Should complete in reasonable time (< 10 seconds for 1000 patterns)
      expect(duration).toBeLessThan(10000);

      const result = await store.getPatterns(AGENT);
      expect(result.data).toHaveLength(1000);
    });
  });
});
