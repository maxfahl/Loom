# Normalized State with `createEntityAdapter`

When dealing with collections of data where items have unique IDs (e.g., users, posts, products), storing them in a normalized fashion is a best practice. This means storing items in an object keyed by their IDs, rather than in an array. Redux Toolkit's `createEntityAdapter` simplifies managing this normalized state.

## Problem

Storing collections as arrays can lead to inefficiencies and complexities:
*   **Inefficient Updates**: Updating a single item in an array requires mapping over the entire array, which can be slow for large collections.
*   **Referential Equality Issues**: Changes to an item might not trigger re-renders correctly if not handled carefully.
*   **Duplicate Data**: The same item might appear in multiple arrays, leading to inconsistencies.

## Solution

Use `createEntityAdapter` to manage normalized state. It provides a set of pre-built reducers and selectors for adding, updating, removing, and selecting entities from a state object.

### `src/features/users/usersSlice.ts`

```typescript
import { createSlice, createEntityAdapter, createAsyncThunk } from '@reduxjs/toolkit';
import type { RootState } from '../../app/store';

interface User {
  id: string;
  name: string;
  email: string;
}

// Create an entity adapter for users
const usersAdapter = createEntityAdapter<User>({
  // Assume IDs are stored in a field named `id`
  selectId: (user) => user.id,
  // Keep the "all IDs" array sorted based on user name
  sortComparer: (a, b) => a.name.localeCompare(b.name),
});

// Define an async thunk to fetch users
export const fetchUsers = createAsyncThunk(
  'users/fetchUsers',
  async () => {
    const response = await fetch('https://jsonplaceholder.typicode.com/users');
    const data: any[] = await response.json();
    // Map to our User interface, ensuring IDs are strings
    return data.map(user => ({ ...user, id: String(user.id) }));
  }
);

const usersSlice = createSlice({
  name: 'users',
  // `getInitialState` returns a new `{ ids: [], entities: {} }` object
  initialState: usersAdapter.getInitialState({
    loading: 'idle' as 'idle' | 'pending' | 'succeeded' | 'failed',
    error: null as string | null,
  }),
  reducers: {
    // Can add custom reducers here if needed
    addUser: usersAdapter.addOne,
    updateUser: usersAdapter.updateOne,
    removeUser: usersAdapter.removeOne,
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchUsers.pending, (state) => {
        state.loading = 'pending';
      })
      .addCase(fetchUsers.fulfilled, (state, action) => {
        state.loading = 'succeeded';
        // Add all fetched users to the state
        usersAdapter.setAll(state, action.payload);
      })
      .addCase(fetchUsers.rejected, (state, action) => {
        state.loading = 'failed';
        state.error = action.error.message || 'Failed to fetch users';
      });
  },
});

export const { addUser, updateUser, removeUser } = usersSlice.actions;

// Export the customized selectors for this adapter. Selector can be re-exported from the slice file.
export const {
  selectAll: selectAllUsers,
  selectById: selectUserById,
  selectIds: selectUserIds,
} = usersAdapter.getSelectors((state: RootState) => state.users);

export default usersSlice.reducer;
```

### `src/app/store.ts` (integration)

```typescript
import { configureStore } from '@reduxjs/toolkit';
import usersReducer from '../features/users/usersSlice';

export const store = configureStore({
  reducer: {
    users: usersReducer,
    // ... other reducers
  },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
```

### Usage in Components

```typescript
import React, { useEffect } from 'react';
import { useAppSelector, useAppDispatch } from '../../app/hooks';
import { fetchUsers, selectAllUsers, selectUserById } from './usersSlice';

const UsersList: React.FC = () => {
  const dispatch = useAppDispatch();
  const users = useAppSelector(selectAllUsers);
  const loadingStatus = useAppSelector((state) => state.users.loading);
  const error = useAppSelector((state) => state.users.error);

  useEffect(() => {
    if (loadingStatus === 'idle') {
      dispatch(fetchUsers());
    }
  }, [loadingStatus, dispatch]);

  if (loadingStatus === 'pending') {
    return <div>Loading users...</div>;
  }

  if (loadingStatus === 'failed') {
    return <div>Error: {error}</div>;
  }

  return (
    <div>
      <h2>Users</h2>
      <ul>
        {users.map((user) => (
          <li key={user.id}>{user.name} ({user.email})</li>
        ))}
      </ul>
    </div>
  );
};

export default UsersList;
```

## Benefits

*   **Optimized Performance**: Efficient updates and lookups for individual items by ID.
*   **Reduced Boilerplate**: `createEntityAdapter` provides pre-built reducers and selectors, reducing manual code.
*   **Consistency**: Enforces a consistent structure for managing collections of entities.
*   **Simplified Logic**: Makes it easier to manage relationships between entities.

## Considerations

*   **ID Requirement**: Requires each entity to have a unique ID.
*   **Initial Setup**: A small initial setup is required to define the adapter and integrate it into the slice.
