/**
 * ReinforcementLearning Test Suite
 */

import { describe, it, expect } from '@jest/globals';
import { ReinforcementLearner } from '../ReinforcementLearning';

describe('ReinforcementLearning', () => {
  let learner: ReinforcementLearner;

  beforeEach(() => {
    learner = new ReinforcementLearner({ learningRate: 0.1, discountFactor: 0.9 });
  });

  describe('Q-Learning', () => {
    it('should update Q-values based on rewards', () => {
      const state = { context: 'react-component' };
      const action = { type: 'useMemo' };
      const reward = 1.0;

      const initialQ = learner.getQValue(state, action);
      learner.updateQValue(state, action, reward, state);
      const updatedQ = learner.getQValue(state, action);

      expect(updatedQ).toBeGreaterThan(initialQ);
    });

    it('should learn from multiple experiences', () => {
      const state = { context: 'api-call' };
      const action = { type: 'cache' };

      for (let i = 0; i < 10; i++) {
        learner.updateQValue(state, action, 1.0, state);
      }

      const qValue = learner.getQValue(state, action);
      expect(qValue).toBeGreaterThan(0.5);
    });
  });

  describe('Exploration vs Exploitation', () => {
    it('should balance exploration and exploitation', () => {
      learner.setEpsilon(0.3); // 30% exploration

      const state = { context: 'test' };
      const actions = [{ type: 'a' }, { type: 'b' }, { type: 'c' }];

      let explorationCount = 0;
      for (let i = 0; i < 100; i++) {
        const action = learner.selectAction(state, actions);
        if (learner.wasExploration()) explorationCount++;
      }

      expect(explorationCount).toBeGreaterThan(20);
      expect(explorationCount).toBeLessThan(40);
    });
  });

  describe('Experience Replay', () => {
    it('should store and replay experiences', () => {
      const experience = {
        state: { context: 'test' },
        action: { type: 'action' },
        reward: 1.0,
        nextState: { context: 'test-complete' }
      };

      learner.storeExperience(experience);
      const experiences = learner.sampleExperiences(1);

      expect(experiences).toHaveLength(1);
      expect(experiences[0]).toMatchObject(experience);
    });
  });
});
