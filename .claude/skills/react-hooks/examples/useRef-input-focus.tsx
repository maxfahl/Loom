import React, { useRef } from 'react';

/**
 * @function UseRefInputFocus
 * @description Demonstrates using `useRef` to directly access a DOM element (input) and focus it.
 */
const UseRefInputFocus: React.FC = () => {
  const inputRef = useRef<HTMLInputElement>(null);

  const focusInput = () => {
    if (inputRef.current) {
      inputRef.current.focus();
    }
  };

  return (
    <div>
      <h2>useRef Example: Input Focus</h2>
      <input type="text" ref={inputRef} placeholder="Click button to focus me" />
      <button onClick={focusInput}>Focus Input</button>
    </div>
  );
};

export default UseRefInputFocus;
