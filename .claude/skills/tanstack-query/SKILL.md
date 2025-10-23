---
Name: tanstack-query
Version: 1.0.0
Category: Web Development / Data Management
Tags: react-query, tanstack-query, data-fetching, state-management, typescript, react
Description: Efficient data fetching, caching, and state management for React applications using TanStack Query.
---

# TanStack Query Skill

## 1. Skill Purpose

This skill enables Claude to effectively utilize TanStack Query (formerly React Query) for robust and efficient data fetching, caching, synchronization, and server state management in React applications. It focuses on simplifying complex asynchronous operations, reducing boilerplate, and improving application performance and user experience through intelligent caching and automatic updates.

## 2. When to Activate This Skill

Activate this skill when:
*   A React application requires fetching, caching, and updating server-side data.
*   There's a need to manage loading, error, and success states for API calls declaratively.
*   Optimistic UI updates are desired for mutations (create, update, delete operations).
*   The application needs to handle data synchronization across multiple components or tabs.
*   Performance is critical, and intelligent caching strategies (e.g., stale-while-revalidate) are beneficial.
*   Working with TypeScript to ensure type-safe data operations.

## 3. Core Knowledge

Claude should understand the following fundamental concepts and APIs of TanStack Query:

*   **`useQuery`**: Hook for fetching and subscribing to query data.
*   **`useMutation`**: Hook for performing server-side data mutations.
*   **`QueryClient`**: The central instance that manages all queries and mutations.
*   **`QueryClientProvider`**: Context provider to make the `QueryClient` available throughout the React tree.
*   **Query Keys**: Unique identifiers for queries, crucial for caching and invalidation. Best practices involve using arrays for hierarchical keys (e.g., `['todos', todoId]`).
*   **Query Options**:
    *   `staleTime`: How long data is considered "fresh" before it becomes "stale" (default: 0). Stale data will be refetched in the background.
    *   `cacheTime`: How long inactive query data remains in the cache (default: 5 minutes).
    *   `refetchOnWindowFocus`, `refetchOnReconnect`, `refetchInterval`: Control automatic refetching behavior.
    *   `retry`: Number of times to retry a failed query.
*   **Mutations**:
    *   `onSuccess`, `onError`, `onSettled`: Callbacks for handling mutation outcomes.
    *   Optimistic Updates: Updating the UI before the server response, then rolling back on error.
*   **Query Invalidation and Refetching**: Using `queryClient.invalidateQueries` and `queryClient.refetchQueries` to trigger data updates.
*   **TypeScript Integration**: Leveraging generics and type inference for type-safe query and mutation hooks.
*   **Devtools**: Understanding the importance and usage of TanStack Query Devtools for debugging and monitoring.

## 4. Key Guidance for Claude

### Always Recommend (✅ Best Practices)

*   **Strongly Typed Query Keys**: Always define query keys using `as const` or a dedicated type to ensure type safety and prevent typos during invalidation. Structure them hierarchically for better organization and targeted invalidation.
    ```typescript
    // GOOD: Strongly typed and hierarchical query keys
    const queryKeys = {
      todos: ['todos'] as const,
      todo: (id: string) => ['todos', id] as const,
      users: ['users'] as const,
    };

    // Usage
    queryClient.invalidateQueries(queryKeys.todos);
    queryClient.invalidateQueries(queryKeys.todo('123'));
    ```
*   **Custom Hooks for Queries and Mutations**: Encapsulate `useQuery` and `useMutation` logic within custom hooks (`useTodos`, `useAddTodo`) to promote reusability, maintainability, and separation of concerns.
    ```typescript
    // hooks/useTodos.ts
    import { useQuery } from '@tanstack/react-query';
    import { getTodos } from '../api/todos';
    import { queryKeys } from '../utils/queryKeys';

    export const useTodos = () => {
      return useQuery({
        queryKey: queryKeys.todos,
        queryFn: getTodos,
      });
    };

    // hooks/useAddTodo.ts
    import { useMutation, useQueryClient } from '@tanstack/react-query';
    import { addTodo } from '../api/todos';
    import { queryKeys } from '../utils/queryKeys';

    export const useAddTodo = () => {
      const queryClient = useQueryClient();
      return useMutation({
        mutationFn: addTodo,
        onSuccess: () => {
          queryClient.invalidateQueries(queryKeys.todos);
        },
      });
    };
    ```
*   **Optimistic Updates for Mutations**: Implement optimistic updates for a smoother user experience, especially for actions like adding or deleting items. Always include `onMutate`, `onError`, and `onSettled` for robust rollback.
    ```typescript
    // Example optimistic update for adding a todo
    import { useMutation, useQueryClient } from '@tanstack/react-query';
    import { addTodo, Todo } from '../api/todos';
    import { queryKeys } from '../utils/queryKeys';

    export const useAddTodoOptimistic = () => {
      const queryClient = useQueryClient();
      return useMutation({
        mutationFn: addTodo,
        onMutate: async (newTodo: Todo) => {
          await queryClient.cancelQueries(queryKeys.todos);
          const previousTodos = queryClient.getQueryData<Todo[]>(queryKeys.todos);
          queryClient.setQueryData<Todo[]>(queryKeys.todos, (old) => [...(old || []), newTodo]);
          return { previousTodos };
        },
        onError: (err, newTodo, context) => {
          queryClient.setQueryData(queryKeys.todos, context?.previousTodos);
        },
        onSettled: () => {
          queryClient.invalidateQueries(queryKeys.todos);
        },
      });
    };
    ```
*   **Leverage `staleTime` and `cacheTime`**: Configure these options appropriately to balance data freshness with performance. `staleTime` controls how long data is considered fresh, while `cacheTime` controls how long inactive data stays in memory.
*   **Use Devtools**: Always recommend installing and using `@tanstack/react-query-devtools` for easier debugging, monitoring, and understanding query states.

### Never Recommend (❌ Anti-Patterns)

*   **Direct `fetch`/`axios` in Components**: Avoid making direct API calls within `useEffect` or component render logic. Always wrap data fetching with `useQuery` or `useMutation`.
    ```typescript
    // BAD: Manual data fetching
    import React, { useState, useEffect } from 'react';
    import axios from 'axios';

    function TodoList() {
      const [todos, setTodos] = useState([]);
      const [loading, setLoading] = useState(true);
      const [error, setError] = useState(null);

      useEffect(() => {
        const fetchTodos = async () => {
          try {
            const response = await axios.get('/api/todos');
            setTodos(response.data);
          } catch (err) {
            setError(err);
          } finally {
            setLoading(false);
          }
        };
        fetchTodos();
      }, []);

      if (loading) return <div>Loading...</div>;
      if (error) return <div>Error: {error.message}</div>;
      return (
        <ul>
          {todos.map((todo) => (
            <li key={todo.id}>{todo.title}</li>
          ))}
        </ul>
      );
    }
    ```
*   **Generic/Untyped Query Keys**: Avoid using simple strings or untyped arrays for query keys, as this makes invalidation difficult and prone to errors.
    ```typescript
    // BAD: Generic query key
    useQuery(['todos'], getTodos);
    // Invalidation becomes ambiguous if there are other 'todos' related queries
    ```
*   **Over-fetching or Under-fetching**: Design API endpoints and queries to fetch exactly what's needed, avoiding unnecessary data transfer or multiple requests for related data.

### Common Questions & Responses (FAQ Format)

*   **Q: How do I invalidate a specific query after a mutation?**
    *   **A:** Use `queryClient.invalidateQueries(queryKeys.yourSpecificKey)` or `queryClient.invalidateQueries({ queryKey: queryKeys.yourSpecificKey })`. For example, `queryClient.invalidateQueries(queryKeys.todo('123'))` to invalidate a single todo, or `queryClient.invalidateQueries(queryKeys.todos)` to invalidate all todos.
*   **Q: When should I use `staleTime` versus `cacheTime`?**
    *   **A:** `staleTime` determines how long data is considered fresh. While fresh, `useQuery` will not refetch on re-mounts. Once stale, it will refetch in the background. `cacheTime` determines how long inactive query data remains in the cache. After `cacheTime`, the data is garbage collected. Use `staleTime` to control refetching behavior and `cacheTime` to manage memory usage.
*   **Q: How can I prefetch data?**
    *   **A:** Use `queryClient.prefetchQuery` in an event handler or `useEffect` to fetch data before it's needed, improving perceived performance.
    *   ```typescript
        // Example prefetching
        const handleMouseEnter = () => {
          queryClient.prefetchQuery({
            queryKey: queryKeys.todo('456'),
            queryFn: () => getTodo('456'),
          });
        };
        ```

## 5. Anti-Patterns to Flag

### Anti-Pattern: Manual State Management for Server Data

```typescript
// BAD: Manual state management with useState and useEffect
import React, { useState, useEffect } from 'react';
import axios from 'axios';

interface Post {
  id: number;
  title: string;
  body: string;
}

function PostList() {
  const [posts, setPosts] = useState<Post[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchPosts = async () => {
      try {
        const response = await axios.get<Post[]>('https://jsonplaceholder.typicode.com/posts');
        setPosts(response.data);
      } catch (err: any) {
        setError(err.message);
      } finally {
        setIsLoading(false);
      }
    };
    fetchPosts();
  }, []);

  if (isLoading) return <div>Loading posts...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div>
      <h1>Posts</h1>
      <ul>
        {posts.map((post) => (
          <li key={post.id}>{post.title}</li>
        ))}
      </ul>
    </div>
  );
}
```

```typescript
// GOOD: Using TanStack Query for server state management
import React from 'react';
import { useQuery } from '@tanstack/react-query';
import axios from 'axios';

interface Post {
  id: number;
  title: string;
  body: string;
}

const getPosts = async (): Promise<Post[]> => {
  const { data } = await axios.get<Post[]>('https://jsonplaceholder.typicode.com/posts');
  return data;
};

const postKeys = {
  all: ['posts'] as const,
  detail: (id: number) => ['posts', id] as const,
};

function usePosts() {
  return useQuery({
    queryKey: postKeys.all,
    queryFn: getPosts,
  });
}

function PostList() {
  const { data: posts, isLoading, isError, error } = usePosts();

  if (isLoading) return <div>Loading posts...</div>;
  if (isError) return <div>Error: {(error as Error).message}</div>;

  return (
    <div>
      <h1>Posts</h1>
      <ul>
        {posts?.map((post) => (
          <li key={post.id}>{post.title}</li>
        ))}
      </ul>
    </div>
  );
}
```

## 6. Code Review Checklist

*   [ ] Are all data fetching and mutation operations encapsulated in custom hooks?
*   [ ] Are query keys defined using `as const` and structured hierarchically for clarity and type safety?
*   [ ] Is `staleTime` configured appropriately for each query to optimize refetching behavior?
*   [ ] Are optimistic updates implemented for mutations where a quick UI response is beneficial, with proper rollback logic?
*   [ ] Is error handling robust for both queries and mutations, providing meaningful feedback to the user?
*   [ ] Are `select` options used in `useQuery` to transform or select only necessary data, preventing unnecessary re-renders?
*   [ ] Is the `QueryClientProvider` configured at a high enough level in the component tree?
*   [ ] Are TanStack Query Devtools integrated and used during development?
*   [ ] Are `enabled` options used for dependent queries to prevent unnecessary fetches?

## 7. Related Skills

*   `react-patterns`: For general React component and hook best practices.
*   `typescript-strict-mode`: For ensuring robust type safety across the application, including data structures used with TanStack Query.

## 8. Examples Directory Structure

```
examples/
├── hooks/
│   ├── useTodos.ts         // Custom hook for fetching todos
│   ├── useAddTodo.ts       // Custom hook for adding a todo (with optimistic update)
│   └── useUpdateTodo.ts    // Custom hook for updating a todo
├── components/
│   ├── TodoList.tsx        // Component displaying a list of todos
│   └── AddTodoForm.tsx     // Component for adding a new todo
└── utils/
    └── queryKeys.ts        // Centralized definition of query keys
```

## 9. Custom Scripts Section

For TanStack Query, developers often face repetitive tasks related to generating boilerplate for hooks, managing query keys, and ensuring cache consistency. The following scripts aim to automate these pain points.

### Script 1: `generate-query-hook.sh`

*   **Description**: Automates the creation of a new `useQuery` or `useMutation` custom hook file, including basic TypeScript types, a structured query key definition, and placeholder logic. This reduces boilerplate and ensures consistency.

### Script 2: `invalidate-query-cli.py`

*   **Description**: A Python command-line interface (CLI) tool to programmatically invalidate TanStack Query caches. This is particularly useful for triggering cache invalidations from backend services, CI/CD pipelines, or external events, ensuring data freshness across distributed systems.

### Script 3: `query-key-linter.py`

*   **Description**: A Python script that acts as a linter for TanStack Query keys. It scans TypeScript files to enforce best practices such as using `as const` for type inference, hierarchical structuring, and adherence to naming conventions, preventing common invalidation bugs.
