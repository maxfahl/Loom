/**
 * ACP Agent Communication Tests
 *
 * Tests for Agent Communication Protocol integration
 * Based on ACP/A2A standards (Linux Foundation)
 */

import { describe, test, expect, beforeEach } from '@jest/globals';
import TestHelper from '../utils/test-helpers';

// Mock ACP Agent implementation
class MockACPAgent {
  private manifest: {
    name: string;
    description: string;
    capabilities: string[];
  };

  constructor(name: string, capabilities: string[] = []) {
    this.manifest = {
      name,
      description: `Mock agent: ${name}`,
      capabilities,
    };
  }

  getManifest() {
    return this.manifest;
  }

  async run(input: any): Promise<any> {
    return {
      status: 'completed',
      output: {
        agent: this.manifest.name,
        input,
        timestamp: Date.now(),
      },
    };
  }

  async *stream(input: any): AsyncGenerator<any> {
    yield { type: 'thought', content: 'Processing...' };
    await new Promise((r) => setTimeout(r, 10));
    yield { type: 'result', content: `Processed by ${this.manifest.name}` };
  }
}

describe('ACP Agent Communication', () => {
  describe('Agent Manifest', () => {
    test('should create valid agent manifest', () => {
      const agent = new MockACPAgent('test-agent', ['typescript', 'testing']);

      const manifest = agent.getManifest();

      expect(manifest).toHaveProperty('name');
      expect(manifest).toHaveProperty('description');
      expect(manifest).toHaveProperty('capabilities');
      expect(manifest.capabilities).toContain('typescript');
    });

    test('should support capability discovery', () => {
      const agents = [
        new MockACPAgent('frontend-dev', ['react', 'typescript']),
        new MockACPAgent('backend-dev', ['node', 'typescript']),
        new MockACPAgent('db-expert', ['postgresql', 'sql']),
      ];

      const typescriptAgents = agents.filter((agent) =>
        agent.getManifest().capabilities.includes('typescript')
      );

      expect(typescriptAgents).toHaveLength(2);
    });
  });

  describe('Agent Execution', () => {
    let agent: MockACPAgent;

    beforeEach(() => {
      agent = new MockACPAgent('test-agent');
    });

    test('should execute synchronous run', async () => {
      const input = { task: 'test task' };
      const result = await agent.run(input);

      expect(result.status).toBe('completed');
      expect(result.output).toHaveProperty('agent');
      expect(result.output.input).toEqual(input);
    });

    test('should support streaming responses', async () => {
      const input = { task: 'streaming task' };
      const chunks: any[] = [];

      for await (const chunk of agent.stream(input)) {
        chunks.push(chunk);
      }

      expect(chunks.length).toBeGreaterThan(0);
      expect(chunks.some((c) => c.type === 'thought')).toBe(true);
      expect(chunks.some((c) => c.type === 'result')).toBe(true);
    });
  });

  describe('Multi-Agent Coordination', () => {
    test('should coordinate multiple agents sequentially', async () => {
      const coordinator = new MockACPAgent('coordinator');
      const worker1 = new MockACPAgent('worker-1');
      const worker2 = new MockACPAgent('worker-2');

      // Simulate coordinator delegating to workers
      const task = { type: 'complex-task' };

      const step1 = await coordinator.run({ delegate: 'worker-1', task });
      const step2 = await worker1.run(task);
      const step3 = await worker2.run(task);

      expect(step1.status).toBe('completed');
      expect(step2.status).toBe('completed');
      expect(step3.status).toBe('completed');
    });

    test('should coordinate multiple agents in parallel', async () => {
      const agents = [
        new MockACPAgent('parallel-1'),
        new MockACPAgent('parallel-2'),
        new MockACPAgent('parallel-3'),
      ];

      const task = { type: 'parallel-task' };
      const startTime = Date.now();

      const results = await Promise.all(agents.map((agent) => agent.run(task)));

      const duration = Date.now() - startTime;

      expect(results).toHaveLength(3);
      expect(results.every((r) => r.status === 'completed')).toBe(true);
      expect(duration).toBeLessThan(100); // Should complete quickly in parallel
    });
  });

  describe('Agent Selection and Routing', () => {
    test('should select agent based on capabilities', () => {
      const agents = [
        new MockACPAgent('react-pro', ['react', 'frontend']),
        new MockACPAgent('node-pro', ['node', 'backend']),
        new MockACPAgent('full-stack', ['react', 'node', 'typescript']),
      ];

      const selectAgent = (capability: string) =>
        agents.find((agent) =>
          agent.getManifest().capabilities.includes(capability)
        );

      const reactAgent = selectAgent('react');
      const nodeAgent = selectAgent('node');

      expect(reactAgent?.getManifest().name).toBe('react-pro');
      expect(nodeAgent?.getManifest().name).toBe('node-pro');
    });

    test('should handle agent selection with multiple matches', () => {
      const agents = [
        new MockACPAgent('specialist', ['typescript']),
        new MockACPAgent('generalist', ['typescript', 'javascript', 'python']),
      ];

      const typescriptAgents = agents.filter((agent) =>
        agent.getManifest().capabilities.includes('typescript')
      );

      expect(typescriptAgents).toHaveLength(2);

      // Should prefer specialist over generalist (fewer capabilities = more focused)
      const selected = typescriptAgents.reduce((best, current) => {
        const bestCount = best.getManifest().capabilities.length;
        const currentCount = current.getManifest().capabilities.length;
        return currentCount < bestCount ? current : best;
      });

      expect(selected.getManifest().name).toBe('specialist');
    });
  });

  describe('Agent Context and State', () => {
    test('should maintain context across invocations', async () => {
      const agent = new MockACPAgent('stateful-agent');
      const session = { id: 'session-123', context: new Map() };

      // Simulate stateful interaction
      const result1 = await agent.run({
        session: session.id,
        message: 'Initialize',
      });
      session.context.set('initialized', true);

      const result2 = await agent.run({
        session: session.id,
        message: 'Continue',
      });

      expect(result1.status).toBe('completed');
      expect(result2.status).toBe('completed');
      expect(session.context.get('initialized')).toBe(true);
    });

    test('should support session isolation', async () => {
      const agent = new MockACPAgent('multi-session-agent');

      const session1 = { id: 'session-1', data: 'data-1' };
      const session2 = { id: 'session-2', data: 'data-2' };

      const result1 = await agent.run({ session: session1.id });
      const result2 = await agent.run({ session: session2.id });

      expect(result1.output.input.session).toBe('session-1');
      expect(result2.output.input.session).toBe('session-2');
    });
  });

  describe('Error Handling and Recovery', () => {
    test('should handle agent errors gracefully', async () => {
      const faultyAgent = new MockACPAgent('faulty-agent');

      // Override run to throw error
      faultyAgent.run = async () => {
        throw new Error('Agent execution failed');
      };

      try {
        await faultyAgent.run({ task: 'test' });
        fail('Should have thrown error');
      } catch (error: any) {
        expect(error.message).toBe('Agent execution failed');
      }
    });

    test('should support fallback agents', async () => {
      const primaryAgent = new MockACPAgent('primary');
      const fallbackAgent = new MockACPAgent('fallback');

      primaryAgent.run = async () => {
        throw new Error('Primary failed');
      };

      let result;
      try {
        result = await primaryAgent.run({ task: 'test' });
      } catch (error) {
        // Fallback to backup agent
        result = await fallbackAgent.run({ task: 'test' });
      }

      expect(result.status).toBe('completed');
      expect(result.output.agent).toBe('fallback');
    });
  });

  describe('Agent Performance Monitoring', () => {
    test('should track agent execution time', async () => {
      const agent = new MockACPAgent('timed-agent');

      const startTime = Date.now();
      const result = await agent.run({ task: 'test' });
      const duration = Date.now() - startTime;

      expect(duration).toBeLessThan(1000); // Should complete quickly
      expect(result.status).toBe('completed');
    });

    test('should handle timeout scenarios', async () => {
      const slowAgent = new MockACPAgent('slow-agent');

      slowAgent.run = async () => {
        await new Promise((r) => setTimeout(r, 100));
        return { status: 'completed', output: {} };
      };

      const timeout = 50;
      const timeoutPromise = new Promise((_, reject) =>
        setTimeout(() => reject(new Error('Timeout')), timeout)
      );

      try {
        await Promise.race([slowAgent.run({}), timeoutPromise]);
        fail('Should have timed out');
      } catch (error: any) {
        expect(error.message).toBe('Timeout');
      }
    });
  });
});

describe('ACP Message Structure', () => {
  test('should create valid ACP message format', () => {
    const message = {
      role: 'user',
      parts: [
        {
          content: 'Test message',
          contentType: 'text/plain',
        },
      ],
    };

    expect(message).toHaveProperty('role');
    expect(message).toHaveProperty('parts');
    expect(message.parts[0]).toHaveProperty('content');
    expect(message.parts[0]).toHaveProperty('contentType');
  });

  test('should support multimodal messages', () => {
    const message = {
      role: 'user',
      parts: [
        { content: 'Text content', contentType: 'text/plain' },
        { content: 'base64ImageData', contentType: 'image/png' },
        { content: '{"key": "value"}', contentType: 'application/json' },
      ],
    };

    expect(message.parts).toHaveLength(3);
    expect(message.parts.map((p) => p.contentType)).toEqual([
      'text/plain',
      'image/png',
      'application/json',
    ]);
  });
});
