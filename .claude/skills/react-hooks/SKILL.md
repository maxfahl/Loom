---
Name: react-hooks
Version: 1.0.0
Category: Web Development / React
Tags: React, Hooks, useState, useEffect, useContext, useRef, useCallback, useMemo, custom hooks
Description: Guiding Claude on effective and idiomatic use of React Hooks for state and side effects.
---

# React Hooks Skill

## 1. Skill Purpose

This skill enables Claude to understand, generate, and review React code utilizing Hooks (`useState`, `useEffect`, `useContext`, `useRef`, `useCallback`, `useMemo`, custom hooks) for managing component state, side effects, and logic reuse. It emphasizes best practices for performance, maintainability, and adherence to React's rules of Hooks.

## 2. When to Activate This Skill

Activate when:
- Generating new React functional components.
- Refactoring class components to functional components.
- Implementing state management within functional components.
- Managing side effects (data fetching, subscriptions, DOM manipulation).
- Optimizing React component performance.
- Creating reusable logic across components (custom hooks).
- Reviewing existing React functional component code.
- Discussing React state management patterns.

## 3. Core Knowledge

- **`useState`**: Managing local component state.
- **`useEffect`**: Handling side effects (data fetching, subscriptions, manual DOM changes).
- **`useContext`**: Consuming context for global state or shared data.
- **`useRef`**: Accessing DOM elements or persisting mutable values across renders without causing re-renders.
- **`useCallback`**: Memoizing functions to prevent unnecessary re-renders of child components.
- **`useMemo`**: Memoizing expensive computations to prevent unnecessary recalculations.
- **`useReducer`**: Managing complex state logic, especially when state transitions depend on previous state or involve multiple related values.
- **Custom Hooks**: Extracting and reusing stateful logic.
- **Rules of Hooks**:
    - Only call Hooks at the Top Level (not inside loops, conditions, or nested functions).
    - Only Call Hooks from React Functions (functional components or custom hooks).
- **Dependency Arrays**: Correctly specifying dependencies for `useEffect`, `useCallback`, and `useMemo` to prevent stale closures and unnecessary re-runs.
- **Cleanup Functions**: Returning a function from `useEffect` to clean up resources.

## 4. Key Guidance for Claude

### Always Recommend (✅ best practices)
- ✅ Always adhere to the Rules of Hooks.
- ✅ Use descriptive names for state variables and custom hooks.
- ✅ Provide a dependency array for `useEffect`, `useCallback`, and `useMemo`.
- ✅ Implement cleanup functions in `useEffect` for subscriptions, timers, or event listeners.
- ✅ Extract complex or repetitive logic into custom hooks for reusability.
- ✅ Use `useState` for simple state and `useReducer` for complex state logic.
- ✅ Use `useContext` for sharing data across multiple components without prop drilling.
- ✅ Memoize expensive computations with `useMemo` and functions with `useCallback` when performance is critical (e.g., passing callbacks to memoized child components).
- ✅ Separate concerns by using multiple `useEffect` calls for unrelated side effects.

### Never Recommend (❌ anti-patterns)
- ❌ Calling Hooks inside loops, conditions, or nested functions.
- ❌ Calling Hooks from regular JavaScript functions (non-React functions).
- ❌ Omitting the dependency array for `useEffect` when it has dependencies, leading to stale closures or infinite loops.
- ❌ Putting non-primitive values (objects, arrays, functions) directly into dependency arrays without memoization, causing unnecessary re-renders.
- ❌ Overusing `useCallback` and `useMemo` for trivial computations, as memoization itself has a cost.
- ❌ Directly modifying state variables; always use the state setter function.
- ❌ Performing heavy computations directly in the render phase; use `useMemo` or move to `useEffect`.

### Common Questions & Responses (FAQ format)
- **Q: When should I use `useState` vs `useReducer`?**
    - A: Use `useState` for simple state management (e.g., toggles, input values). Use `useReducer` for more complex state logic, especially when state updates depend on the previous state, involve multiple sub-values, or when you want to centralize state update logic.
- **Q: How do I prevent `useEffect` from running on every render?**
    - A: Provide a dependency array as the second argument to `useEffect`. It will only re-run when one of its dependencies changes. An empty array `[]` means it runs once after the initial render and cleans up on unmount.
- **Q: What is a "stale closure" and how do I avoid it?**
    - A: A stale closure occurs when a function (often inside `useEffect`) captures an outdated value of a variable from an earlier render. Avoid it by ensuring all variables used inside `useEffect` (that change across renders) are included in its dependency array.
- **Q: When should I create a custom hook?**
    - A: Create a custom hook when you have stateful logic that needs to be reused across multiple components, or when a component's logic becomes complex and can be abstracted into a more focused, reusable unit.

## 5. Anti-Patterns to Flag

```typescript
// BAD: Missing dependency in useEffect, leading to stale `count`
function Counter() {
  const [count, setCount] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      console.log(count); // Will always log 0 if count is not in dependency array
      setCount(count + 1); // Will always increment from 0
    }, 1000);
    return () => clearInterval(interval);
  }, []); // ❌ Missing `count` in dependency array

  return <div>{count}</div>;
}

// GOOD: Correct dependency array for useEffect
function CounterGood() {
  const [count, setCount] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      console.log(count);
      setCount(prevCount => prevCount + 1); // Using functional update to avoid `count` in dependencies
    }, 1000);
    return () => clearInterval(interval);
  }, [count]); // ✅ `count` is in dependency array, or use functional update for setCount

  return <div>{count}</div>;
}

// BAD: Overusing useCallback for a simple function
function MyComponentBad({ onClick }) {
  const handleClick = useCallback(() => {
    // Simple logic
    onClick();
  }, [onClick]); // ❌ Unnecessary memoization for a simple function

  return <button onClick={handleClick}>Click me</button>;
}

// GOOD: Only use useCallback when necessary (e.g., passing to memoized child)
function MyComponentGood({ onClick }) {
  // If onClick is stable or passed to a non-memoized component, useCallback might not be needed
  // If passing to a React.memo child, then useCallback is appropriate.
  const handleClick = useCallback(() => {
    // Potentially complex logic or passed to a memoized child
    onClick();
  }, [onClick]);

  return <button onClick={handleClick}>Click me</button>;
}

// BAD: Conditional Hook call
function MyConditionalHookBad({ shouldRender }) {
  if (shouldRender) {
    const [value, setValue] = useState(0); // ❌ Hook called conditionally
    return <div>{value}</div>;
  }
  return null;
}

// GOOD: Unconditional Hook call
function MyConditionalHookGood({ shouldRender }) {
  const [value, setValue] = useState(0); // ✅ Hook called unconditionally at top level

  if (!shouldRender) {
    return null;
  }
  return <div>{value}</div>;
}
```

## 6. Code Review Checklist
- [ ] Are all Hooks called at the top level of functional components or custom hooks?
- [ ] Is a dependency array provided for `useEffect`, `useCallback`, and `useMemo`?
- [ ] Are all dependencies correctly listed in the dependency arrays? (No missing dependencies, no unnecessary ones).
- [ ] Are cleanup functions implemented in `useEffect` where necessary (subscriptions, timers, event listeners)?
- [ ] Is `useState` used for simple state and `useReducer` for complex state logic?
- [ ] Is `useContext` used appropriately for global state or shared data?
- [ ] Are custom hooks used to abstract and reuse stateful logic?
- [ ] Are `useCallback` and `useMemo` used judiciously for performance optimization, not for trivial cases?
- [ ] Are state updates performed using the setter function (e.g., `setCount(prevCount => prevCount + 1)`) rather than direct mutation?
- [ ] Is the code readable and well-organized, with clear variable names?

## 7. Related Skills
- `react-context`
- `nextjs-app-router` (for React components in Next.js)

## 8. Examples Directory Structure
- `examples/`
    - `useState-counter.tsx`
    - `useEffect-data-fetching.tsx`
    - `useContext-theme-switcher.tsx`
    - `useRef-input-focus.tsx`
    - `useCallback-memoized-button.tsx`
    - `useMemo-expensive-calculation.tsx`
    - `useReducer-complex-form.tsx`
    - `custom-hook-use-toggle.ts`

## 9. Custom Scripts Section

### 9.1. `generate-custom-hook.sh`
- **Purpose**: Automates the creation of a custom React Hook boilerplate, including a basic test file.
- **Usage**: `./scripts/generate-custom-hook.sh <HookName>`

### 9.2. `generate-functional-component.sh`
- **Purpose**: Automates the creation of a functional React component with optional `useState` and `useEffect` boilerplate, and a basic test file.
- **Usage**: `./scripts/generate-functional-component.sh <ComponentName> [--state] [--effect]`

### 9.3. `analyze-effect-dependencies.py`
- **Purpose**: Scans a TypeScript/JavaScript file for `useEffect` calls and provides suggestions for potential dependency array issues (e.g., missing dependencies, unnecessary dependencies).
- **Usage**: `python scripts/analyze-effect-dependencies.py <filePath>`

### 9.4. `refactor-to-use-reducer.py`
- **Purpose**: Helps refactor a component that uses multiple `useState` calls into a single `useReducer` call, generating the reducer function and initial state.
- **Usage**: `python scripts/refactor-to-use-reducer.py <filePath> <componentName>`
