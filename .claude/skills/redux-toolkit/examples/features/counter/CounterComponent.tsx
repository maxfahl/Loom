import React from 'react';
import { useAppSelector, useAppDispatch } from '../../../examples/hooks';
import { increment, decrement, incrementByAmount } from './counterSlice';

const CounterComponent: React.FC = () => {
  const count = useAppSelector((state) => state.counter.value);
  const dispatch = useAppDispatch();

  return (
    <div>
      <h2>Counter: {count}</h2>
      <button onClick={() => dispatch(increment())}>Increment</button>
      <button onClick={() => dispatch(decrement())}>Decrement</button>
      <button onClick={() => dispatch(incrementByAmount(5))}>Increment by 5</button>
    </div>
  );
};

export default CounterComponent;
