"use client";

import React, { useState, useEffect } from 'react';

export default function ClientComponentWithState() {
  const [count, setCount] = useState(0);
  const [message, setMessage] = useState('');

  useEffect(() => {
    // This effect runs once after the initial render (like componentDidMount)
    // and cleans up when the component unmounts (like componentWillUnmount).
    console.log('ClientComponentWithState mounted!');
    setMessage('Component mounted!');

    const timer = setTimeout(() => {
      setMessage('Message updated after 2 seconds!');
    }, 2000);

    return () => {
      console.log('ClientComponentWithState unmounted!');
      clearTimeout(timer);
    };
  }, []); // Empty dependency array means it runs once on mount and cleans up on unmount

  useEffect(() => {
    // This effect runs whenever `count` changes.
    console.log('Count changed:', count);
  }, [count]); // Dependency array includes `count`

  const increment = () => {
    setCount(prevCount => prevCount + 1);
  };

  const decrement = () => {
    setCount(prevCount => prevCount - 1);
  };

  return (
    <div>
      <h1>Client Component with State and Effects</h1>
      <p>Count: {count}</p>
      <button onClick={increment}>Increment</button>
      <button onClick={decrement}>Decrement</button>
      <p>{message}</p>
    </div>
  );
}
