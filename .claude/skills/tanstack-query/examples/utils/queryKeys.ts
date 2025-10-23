// utils/queryKeys.ts
// Centralized definition of TanStack Query keys for better organization and type safety.

export const todoKeys = {
  all: ['todos'] as const,
  detail: (id: string) => ['todos', id] as const,
  // Add more specific keys as needed
};

export const userKeys = {
  all: ['users'] as const,
  detail: (id: string) => ['users', id] as const,
};

// Add more key groups for other entities as your application grows.

// Example of how to use these keys:
// import { todoKeys } from './queryKeys';
// queryClient.invalidateQueries(todoKeys.all);
// queryClient.invalidateQueries(todoKeys.detail('123'));
