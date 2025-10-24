/**
 * ReinforcementLearning Test Suite
 */

import { describe, it, expect, beforeEach } from '@jest/globals';
import { ReinforcementLearningModule, State, Action, Reward } from '../ReinforcementLearning';

describe('ReinforcementLearning', () => {
  let learner: ReinforcementLearningModule;

  beforeEach(() => {
    learner = new ReinforcementLearningModule({ learningRate: 0.1, discountFactor: 0.9 });
  });

  describe('Q-Learning', () => {
    it('should update Q-values based on rewards', () => {
      const state: State = {
        id: 'state-1',
        features: { context: 'react-component', complexity: 5 },
        timestamp: new Date().toISOString(),
        agentState: { recentSuccessRate: 0.8, confidenceLevel: 0.7, energyLevel: 0.9 }
      };

      const action: Action = {
        id: 'action-1',
        type: 'useMemo',
        parameters: {},
        estimatedCost: 0.1,
        riskLevel: 'low'
      };

      const reward: Reward = {
        value: 1.0,
        components: {
          successBonus: 1.0,
          efficiencyBonus: 0.5,
          qualityBonus: 0.8,
          noveltyBonus: 0.3,
          riskPenalty: 0.0
        }
      };

      const initialQ = learner.getQValue(state, action);
      learner.updateQValue(state, action, reward, state);
      const updatedQ = learner.getQValue(state, action);

      expect(updatedQ).toBeGreaterThan(initialQ);
    });

    it('should learn from multiple experiences', () => {
      const state: State = {
        id: 'state-2',
        features: { context: 'api-call', type: 'cache' },
        timestamp: new Date().toISOString(),
        agentState: { recentSuccessRate: 0.8, confidenceLevel: 0.7, energyLevel: 0.9 }
      };

      const action: Action = {
        id: 'action-2',
        type: 'cache',
        parameters: {},
        estimatedCost: 0.1,
        riskLevel: 'low'
      };

      const reward: Reward = {
        value: 1.0,
        components: {
          successBonus: 1.0,
          efficiencyBonus: 0.5,
          qualityBonus: 0.8,
          noveltyBonus: 0.3,
          riskPenalty: 0.0
        }
      };

      for (let i = 0; i < 10; i++) {
        learner.updateQValue(state, action, reward, state);
      }

      const qValue = learner.getQValue(state, action);
      expect(qValue).toBeGreaterThan(0.5);
    });
  });

  describe('Exploration vs Exploitation', () => {
    it('should balance exploration and exploitation', () => {
      const state: State = {
        id: 'state-3',
        features: { context: 'test' },
        timestamp: new Date().toISOString(),
        agentState: { recentSuccessRate: 0.8, confidenceLevel: 0.7, energyLevel: 0.9 }
      };

      const actions: Action[] = [
        { id: 'a1', type: 'a', parameters: {}, estimatedCost: 0.1, riskLevel: 'low' },
        { id: 'a2', type: 'b', parameters: {}, estimatedCost: 0.1, riskLevel: 'low' },
        { id: 'a3', type: 'c', parameters: {}, estimatedCost: 0.1, riskLevel: 'low' }
      ];

      // Initialize Q-values for one action to be higher
      const reward: Reward = {
        value: 1.0,
        components: {
          successBonus: 1.0,
          efficiencyBonus: 0.5,
          qualityBonus: 0.8,
          noveltyBonus: 0.3,
          riskPenalty: 0.0
        }
      };
      learner.updateQValue(state, actions[0], reward, state);

      let exploitCount = 0;
      for (let i = 0; i < 100; i++) {
        const selectedAction = learner.selectAction(state, actions, 'test-agent');
        if (selectedAction.id === 'a1') exploitCount++;
      }

      // Should mostly exploit the best action but occasionally explore
      expect(exploitCount).toBeGreaterThan(60);
      expect(exploitCount).toBeLessThan(100);
    });
  });

  describe('Experience Replay', () => {
    it('should maintain Q-table statistics', () => {
      const state: State = {
        id: 'state-4',
        features: { context: 'test' },
        timestamp: new Date().toISOString(),
        agentState: { recentSuccessRate: 0.8, confidenceLevel: 0.7, energyLevel: 0.9 }
      };

      const action: Action = {
        id: 'action-4',
        type: 'action',
        parameters: {},
        estimatedCost: 0.1,
        riskLevel: 'low'
      };

      const reward: Reward = {
        value: 1.0,
        components: {
          successBonus: 1.0,
          efficiencyBonus: 0.5,
          qualityBonus: 0.8,
          noveltyBonus: 0.3,
          riskPenalty: 0.0
        }
      };

      learner.updateQValue(state, action, reward, state);

      const stats = learner.getStatistics();
      expect(stats.qTableSize).toBeGreaterThan(0);
      expect(stats.totalUpdates).toBeGreaterThan(0);
    });
  });
});
