import React, { useState, useCallback, memo } from 'react';

// A memoized child component that only re-renders if its props change
interface ButtonProps {
  onClick: () => void;
  children: React.ReactNode;
}

const MemoizedButton = memo<ButtonProps>(({ onClick, children }) => {
  console.log(`Rendering MemoizedButton: ${children}`);
  return <button onClick={onClick}>{children}</button>;
});

/**
 * @function UseCallbackMemoizedButton
 * @description Demonstrates `useCallback` to prevent unnecessary re-renders of a memoized child component.
 */
const UseCallbackMemoizedButton: React.FC = () => {
  const [count, setCount] = useState(0);
  const [otherCount, setOtherCount] = useState(0);

  // This function will be re-created on every render if not memoized
  const handleClick = () => {
    setCount(prevCount => prevCount + 1);
  };

  // Memoize handleClick using useCallback. It will only change if `setCount` changes (which it won't).
  const memoizedHandleClick = useCallback(() => {
    setCount(prevCount => prevCount + 1);
  }, []); // Empty dependency array means this function is stable across renders

  // This function will also be re-created on every render if not memoized
  const handleOtherClick = () => {
    setOtherCount(prevCount => prevCount + 1);
  };

  return (
    <div>
      <h2>useCallback Example</h2>
      <p>Count: {count}</p>
      <p>Other Count: {otherCount}</p>

      {/* This button's onClick is not memoized, so MemoizedButton will re-render if parent re-renders */}
      <MemoizedButton onClick={handleClick}>Increment Count (Non-memoized callback)</MemoizedButton>

      {/* This button's onClick is memoized, so MemoizedButton will NOT re-render unless its props actually change */}
      <MemoizedButton onClick={memoizedHandleClick}>Increment Count (Memoized callback)</MemoizedButton>

      <button onClick={handleOtherClick}>Increment Other Count (Triggers parent re-render)</button>
    </div>
  );
};

export default UseCallbackMemoizedButton;
