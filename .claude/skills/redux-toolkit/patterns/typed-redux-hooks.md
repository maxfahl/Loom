# Typed Redux Hooks

When using Redux Toolkit with TypeScript, it's crucial to properly type your `useDispatch` and `useSelector` hooks to get full type safety and autocompletion throughout your application. This pattern involves creating custom, pre-typed versions of these hooks.

## Problem

Directly using `useDispatch` and `useSelector` from `react-redux` often requires manual type assertions or leads to `any` types, reducing the benefits of TypeScript.

```typescript
// BAD: Manual typing or implicit 'any'
import { useDispatch, useSelector } from 'react-redux';

const dispatch = useDispatch(); // dispatch is 'any' or requires manual assertion
const count = useSelector((state: any) => state.counter.value); // state is 'any'
```

## Solution

Create a separate `hooks.ts` file that exports pre-typed versions of `useDispatch` and `useSelector`. These custom hooks will infer the correct types for your `RootState` and `AppDispatch` from your Redux store configuration.

### `src/app/store.ts` (or `store.ts` in examples)

```typescript
import { configureStore } from '@reduxjs/toolkit';
import counterReducer from '../features/counter/counterSlice';
// ... other reducers and RTK Query setup

export const store = configureStore({
  reducer: {
    counter: counterReducer,
    // ...
  },
});

// Infer the RootState and AppDispatch types from the store itself
export type RootState = ReturnType<typeof store.getState>;
// Inferred type: {posts: PostsState, comments: CommentsState, users: UsersState}
export type AppDispatch = typeof store.dispatch;
```

### `src/app/hooks.ts` (or `hooks.ts` in examples)

```typescript
import { useDispatch, useSelector } from 'react-redux';
import type { TypedUseSelectorHook } from 'react-redux';
import type { RootState, AppDispatch } from './store'; // Adjust path as needed

// Use throughout your app instead of plain useDispatch and useSelector
// These hooks are pre-typed with your app's RootState and AppDispatch
export const useAppDispatch: () => AppDispatch = useDispatch;
export const useAppSelector: TypedUseSelectorHook<RootState> = useSelector;
```

### Usage in Components

```typescript
import React from 'react';
import { useAppSelector, useAppDispatch } from '../../app/hooks'; // Adjust path
import { increment, decrement } from '../features/counter/counterSlice';

const Counter: React.FC = () => {
  const count = useAppSelector((state) => state.counter.value); // Fully typed state
  const dispatch = useAppDispatch(); // Fully typed dispatch

  return (
    <div>
      <span>{count}</span>
      <button onClick={() => dispatch(increment())}>Increment</button>
      <button onClick={() => dispatch(decrement())}>Decrement</button>
    </div>
  );
};

export default Counter;
```

## Benefits

*   **Full Type Safety**: Ensures that `state` in `useSelector` and `dispatch` in `useDispatch` calls are correctly typed, catching errors at compile time.
*   **Improved Developer Experience**: Provides autocompletion and type hints in your IDE for your Redux state and actions.
*   **Reduced Boilerplate**: Avoids the need to manually type `useDispatch` and `useSelector` in every component.
*   **Consistency**: Promotes a consistent way of interacting with the Redux store across your application.
