---
Name: redux-toolkit
Version: 1.0.0
Category: State Management / Frontend
Tags: redux, redux toolkit, rtk, react, typescript, state management, createSlice, createAsyncThunk, rtk query
Description: Enables Claude to efficiently implement and manage state in React applications using Redux Toolkit with TypeScript, including RTK Query for data fetching.
---

## 2. Skill Purpose

This skill provides Claude with the expertise to build scalable, maintainable, and type-safe React applications using Redux Toolkit. It covers the core features of RTK, best practices for structuring state, handling asynchronous logic with `createAsyncThunk`, managing data fetching and caching with RTK Query, and integrating seamlessly with TypeScript. The goal is to reduce boilerplate, improve developer experience, and ensure robust state management.

## 3. When to Activate This Skill

Activate this skill when:
*   Developing a new React application that requires robust state management.
*   Refactoring an existing Redux application to use Redux Toolkit.
*   Implementing complex data fetching, caching, and invalidation logic.
*   Building features that involve asynchronous operations and need clear loading/error states.
*   Ensuring type safety and a good developer experience in a Redux-powered React application.
*   Organizing application state in a modular and scalable way.

## 4. Core Knowledge

*   **Redux Toolkit Core**: `configureStore`, `createSlice`, `createAction`, `createReducer`.
*   **Asynchronous Logic**: `createAsyncThunk` for handling promises and API calls.
*   **Data Fetching**: RTK Query (`createApi`, `fetchBaseQuery`, `endpoints`, `useQuery`, `useMutation`).
*   **State Structure**: Normalized state, `createEntityAdapter`.
*   **TypeScript Integration**: `RootState`, `AppDispatch`, typed `useSelector` and `useDispatch` hooks.
*   **Middleware**: Redux Thunk (built-in), listeners middleware (advanced).
*   **Selectors**: `reselect` (`createSelector`) for memoized selectors.
*   **Immutability**: Immer.js (integrated into `createSlice`).
*   **React-Redux Integration**: `Provider`, `useSelector`, `useDispatch`.
*   **Project Structure**: Feature-sliced design.

## 5. Key Guidance for Claude

*   **Always Recommend** (✅ best practices)
    *   ✅ Always use Redux Toolkit for new Redux projects to leverage its opinionated setup and reduce boilerplate.
    *   ✅ Adopt a TypeScript-first approach, defining types for state, actions, and using typed hooks (`useAppDispatch`, `useAppSelector`).
    *   ✅ Organize state into logical "slices" using `createSlice`, with each slice managing a specific feature or domain.
    *   ✅ Use `createAsyncThunk` for all asynchronous logic, handling `pending`, `fulfilled`, and `rejected` states in `extraReducers`.
    *   ✅ Implement RTK Query for all data fetching, caching, and invalidation needs to minimize boilerplate and optimize performance.
    *   ✅ Normalize complex data structures using `createEntityAdapter` for efficient updates and lookups.
    *   ✅ Create memoized selectors with `createSelector` (from Reselect) to prevent unnecessary re-renders and optimize performance.
    *   ✅ Handle errors robustly in `createAsyncThunk` using `rejectWithValue` to pass detailed error payloads.
    *   ✅ Maintain clear loading and error states within each slice for better UI feedback.
    *   ✅ Structure your application with a feature-based approach, co-locating Redux logic with related components.

*   **Never Recommend** (❌ anti-patterns)
    *   ❌ Never use plain Redux (`createStore`, manual action types, switch-case reducers) for new projects; always prefer Redux Toolkit.
    *   ❌ Avoid direct mutation of Redux state outside of `createSlice` reducers (Immer handles this safely within slices).
    *   ❌ Do not over-normalize or under-normalize state; find a balance that suits the application's complexity.
    *   ❌ Never put UI-specific state (e.g., form input values, modal open/close) into Redux unless it needs to be shared globally or persisted. Use React's local state instead.
    *   ❌ Avoid creating overly large or "god" slices that manage too many unrelated pieces of state.
    *   ❌ Do not skip type definitions for Redux state and actions in TypeScript projects.
    *   ❌ Never directly import the Redux store into components; always use `useSelector` and `useDispatch` hooks.
    *   ❌ Avoid complex manual caching logic for API data; leverage RTK Query's built-in caching and invalidation.

*   **Common Questions & Responses** (FAQ format)
    *   **Q: When should I use `createAsyncThunk` versus RTK Query?**
        *   A: Use RTK Query for almost all data fetching, caching, and invalidation. `createAsyncThunk` is better suited for complex asynchronous logic that doesn't involve direct data fetching (e.g., interacting with browser APIs, complex calculations, or when you need very fine-grained control over the async flow that RTK Query doesn't provide).
    *   **Q: How do I handle global state that isn't related to data fetching?**
        *   A: Use regular `createSlice` definitions for global application state (e.g., theme settings, user preferences, authentication status) that isn't managed by RTK Query.
    *   **Q: My component is re-rendering too often. How can I optimize?**
        *   A: Ensure you are using memoized selectors (`createSelector`) to derive data from the Redux store. Also, check if you are selecting too much state or if your component's props are changing unnecessarily.
    *   **Q: How do I set up Redux Toolkit with TypeScript?**
        *   A: Define `RootState` and `AppDispatch` types from your store, and create custom typed `useAppDispatch` and `useAppSelector` hooks. This ensures type safety throughout your application.
    *   **Q: What is the recommended project structure for Redux Toolkit?**
        *   A: A feature-based structure is recommended, where each feature has its own folder containing its slice, components, and potentially RTK Query API definitions. Global store configuration and typed hooks typically reside in an `app/` directory.

## 6. Anti-Patterns to Flag

*   **Anti-Pattern: Manual Redux Setup (without RTK)**
    ```typescript
    // BAD: Legacy Redux setup with boilerplate
    import { createStore, combineReducers, applyMiddleware } from 'redux';
    import thunk from 'redux-thunk';

    const initialState = { count: 0 };
    function counterReducer(state = initialState, action: any) {
      switch (action.type) {
        case 'INCREMENT': return { ...state, count: state.count + 1 };
        case 'DECREMENT': return { ...state, count: state.count - 1 };
        default: return state;
      }
    }
    const rootReducer = combineReducers({ counter: counterReducer });
    const store = createStore(rootReducer, applyMiddleware(thunk));
    ```
    ```typescript
    // GOOD: Redux Toolkit setup with configureStore and createSlice
    import { configureStore, createSlice, PayloadAction } from '@reduxjs/toolkit';

    interface CounterState {
      count: number;
    }

    const initialState: CounterState = {
      count: 0,
    };

    const counterSlice = createSlice({
      name: 'counter',
      initialState,
      reducers: {
        increment: (state) => {
          state.count += 1;
        },
        decrement: (state) => {
          state.count -= 1;
        },
        incrementByAmount: (state, action: PayloadAction<number>) => {
          state.count += action.payload;
        },
      },
    });

    export const { increment, decrement, incrementByAmount } = counterSlice.actions;
    export const counterReducer = counterSlice.reducer;

    export const store = configureStore({
      reducer: {
        counter: counterReducer,
      },
    });

    export type RootState = ReturnType<typeof store.getState>;
    export type AppDispatch = typeof store.dispatch;
    ```

*   **Anti-Pattern: Direct State Mutation (outside `createSlice`)**
    ```typescript
    // BAD: Directly mutating state in a non-Immer-protected reducer
    const badReducer = (state = { items: [] }, action: any) => {
      if (action.type === 'ADD_ITEM') {
        state.items.push(action.payload); // Direct mutation!
        return state;
      }
      return state;
    };
    ```
    ```typescript
    // GOOD: Using createSlice, which leverages Immer for safe mutations
    import { createSlice, PayloadAction } from '@reduxjs/toolkit';

    interface Item { id: string; name: string; }
    interface ItemsState { items: Item[]; }

    const initialState: ItemsState = { items: [] };

    const itemsSlice = createSlice({
      name: 'items',
      initialState,
      reducers: {
        addItem: (state, action: PayloadAction<Item>) => {
          state.items.push(action.payload); // Safe mutation thanks to Immer
        },
        removeItem: (state, action: PayloadAction<string>) => {
          state.items = state.items.filter(item => item.id !== action.payload);
        },
      },
    });

    export const { addItem, removeItem } = itemsSlice.actions;
    export default itemsSlice.reducer;
    ```

## 7. Code Review Checklist

*   [ ] Is Redux Toolkit used for all Redux-related logic?
*   [ ] Are TypeScript types correctly defined for all state, actions, and selectors?
*   [ ] Are `useAppDispatch` and `useAppSelector` hooks used instead of raw `useDispatch` and `useSelector`?
*   [ ] Is state organized into logical slices using `createSlice`?
*   [ ] Is `createAsyncThunk` used for asynchronous operations, with `pending`, `fulfilled`, and `rejected` states handled?
*   [ ] Is RTK Query used for data fetching and caching where applicable?
*   [ ] Are `createEntityAdapter` and normalized state used for complex data relationships?
*   [ ] Are memoized selectors (`createSelector`) used to optimize state derivations?
*   [ ] Is error handling robust, especially in `createAsyncThunk` with `rejectWithValue`?
*   [ ] Is the application structure feature-based, co-locating related Redux and React code?
*   [ ] Are there no direct mutations of Redux state outside of `createSlice` reducers?
*   [ ] Is UI-specific state managed locally within React components, not in Redux?

## 8. Related Skills

*   `react-hooks`: For understanding fundamental React hooks used with Redux Toolkit.
*   `typescript-strict-mode`: For ensuring high-quality TypeScript code in Redux Toolkit applications.
*   `rest-api-design`: For understanding API design principles relevant to RTK Query.
*   `clean-architecture`: For broader architectural patterns that can be applied to Redux Toolkit applications.

## 9. Examples Directory Structure

```
examples/
├── store.ts
├── hooks.ts
├── features/
│   ├── counter/
│   │   ├── counterSlice.ts
│   │   └── CounterComponent.tsx
│   └── posts/
│       ├── postsSlice.ts
│       ├── postsApi.ts
│       └── PostsList.tsx
└── App.tsx
```

## 10. Custom Scripts Section

Here are 4 automation scripts that save significant time for Redux Toolkit development:

1.  **`rtk-init.sh`**: Initializes a new React project (e.g., with Vite or Create React App) and sets up Redux Toolkit with a basic store, typed hooks, and a sample counter slice.
    *   **Usage Examples:**
        ```bash
        ./scripts/rtk-init.sh
        ./scripts/rtk-init.sh my-new-rtk-app
        ```
2.  **`generate-slice.py`**: Generates a new Redux Toolkit slice file (`.ts`) with boilerplate for `createSlice`, including initial state, reducers, and optional `createAsyncThunk` placeholders.
    *   **Usage Examples:**
        ```bash
        python scripts/generate-slice.py products
        python scripts/generate-slice.py user-profile -a
        python scripts/generate-slice.py settings -o src/app
        ```
3.  **`generate-rtk-api.py`**: Generates a new RTK Query API slice file (`.ts`) with boilerplate for `createApi`, including `baseQuery` and example `endpoints` (query and mutation).
    *   **Usage Examples:**
        ```bash
        python scripts/generate-rtk-api.py users --base-url https://api.example.com/v1/
        python scripts/generate-rtk-api.py products -o src/services/api
        ```
4.  **`migrate-legacy-reducer.py`**: Helps migrate a legacy Redux reducer (switch-case) to a Redux Toolkit `createSlice` format, suggesting changes for actions and reducers.
    *   **Usage Examples:**
        ```bash
        python scripts/migrate-legacy-reducer.py src/reducers/userReducer.js
        python scripts/migrate-legacy-reducer.py src/old/productReducer.ts -s products --dry-run
        ```
