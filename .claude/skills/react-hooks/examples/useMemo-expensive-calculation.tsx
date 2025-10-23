import React, { useState, useMemo } from 'react';

/**
 * @function UseMemoExpensiveCalculation
 * @description Demonstrates `useMemo` to memoize the result of an expensive calculation.
 */
const UseMemoExpensiveCalculation: React.FC = () => {
  const [number, setNumber] = useState(1);
  const [multiplier, setMultiplier] = useState(1);
  const [reRenders, setReRenders] = useState(0);

  // Simulate an expensive calculation
  const expensiveCalculation = (num: number, mult: number) => {
    console.log('Performing expensive calculation...');
    // This loop simulates a heavy computation
    let result = 0;
    for (let i = 0; i < 100000000; i++) {
      result += num * mult;
    }
    return result;
  };

  // Without useMemo, expensiveCalculation would run on every re-render
  // const calculatedValue = expensiveCalculation(number, multiplier);

  // With useMemo, expensiveCalculation only runs when `number` or `multiplier` changes
  const memoizedCalculatedValue = useMemo(() => {
    return expensiveCalculation(number, multiplier);
  }, [number, multiplier]);

  // Increment re-render count on every component re-render
  React.useEffect(() => {
    setReRenders(prev => prev + 1);
  });

  return (
    <div>
      <h2>useMemo Example: Expensive Calculation</h2>
      <p>Component Re-renders: {reRenders}</p>
      <div>
        <label>Number: </label>
        <input
          type="number"
          value={number}
          onChange={(e) => setNumber(Number(e.target.value))}
        />
      </div>
      <div>
        <label>Multiplier: </label>
        <input
          type="number"
          value={multiplier}
          onChange={(e) => setMultiplier(Number(e.target.value))}
        />
      </div>
      <p>Calculated Value: {memoizedCalculatedValue}</p>
      <button onClick={() => setReRenders(0)}>Reset Re-renders</button>
    </div>
  );
};

export default UseMemoExpensiveCalculation;
