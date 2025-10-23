---
Name: react-js-development
Version: 1.0.0
Category: Web Development / Frontend
Tags: React, JavaScript, TypeScript, Frontend, UI, Hooks, Components
Description: Guides Claude in building modern, performant, and maintainable React.js applications with TypeScript.
---

# React.js Development Skill

## 1. Skill Purpose

This skill enables Claude to assist in developing robust, scalable, and high-performance React.js applications using modern best practices, functional components, Hooks, and TypeScript. It covers component architecture, state management, performance optimization, and testing strategies.

## 2. When to Activate This Skill

Activate this skill whenever the task involves:
*   Creating new React components, hooks, or contexts.
*   Refactoring existing React code.
*   Implementing state management solutions in React.
*   Optimizing React application performance.
*   Writing tests for React components or hooks.
*   Debugging React-related issues.
*   Discussing architectural patterns for React applications.

## 3. Core Knowledge

Claude should possess fundamental knowledge of:

*   **React Fundamentals:** JSX, Virtual DOM, component lifecycle (conceptual understanding for functional components).
*   **Functional Components & Hooks:** `useState`, `useEffect`, `useContext`, `useRef`, `useMemo`, `useCallback`, custom hooks.
*   **TypeScript:** Type definitions, interfaces, generics, utility types (`Partial`, `Omit`).
*   **Component Architecture:** Component composition, separation of concerns (presentational vs. container, smart vs. dumb).
*   **State Management:** Local component state, Context API, and popular libraries like Zustand, Jotai, or Redux Toolkit.
*   **Performance Optimization:** Memoization, code splitting, lazy loading, virtualization, React Server Components (RSCs) concepts.
*   **Testing:** React Testing Library (RTL) principles, Jest/Vitest basics, unit, integration, and end-to-end testing concepts.
*   **Modern Ecosystem:** Awareness of frameworks like Next.js, Remix, and build tools like Vite.

## 4. Key Guidance for Claude

### Always Recommend (✅ Best Practices)

*   ✅ **Functional Components & Hooks:** Prioritize functional components and React Hooks for all new development.
*   ✅ **TypeScript:** Use TypeScript for all React projects to ensure type safety, improve maintainability, and catch errors early.
*   ✅ **Small, Focused Components:** Design components to be small, reusable, and responsible for a single piece of UI or logic.
*   ✅ **Custom Hooks for Logic Reusability:** Extract reusable stateful logic into custom hooks (prefixed with `use`) to keep components clean and focused on rendering.
*   ✅ **Feature-Based File Structure:** Organize code by feature or domain (e.g., `src/features/auth/components/Login.tsx`) rather than by type.
*   ✅ **React Testing Library (RTL):** Use RTL for testing components, focusing on user behavior and accessibility rather than internal implementation details.
*   ✅ **Memoization (Judiciously):** Apply `React.memo`, `useMemo`, and `useCallback` to prevent unnecessary re-renders, but only after profiling and identifying performance bottlenecks. Avoid premature optimization.
*   ✅ **Context API for Thematic/Global Data:** Use React Context for application-wide data that rarely changes (e.g., theme, authentication status) to avoid prop drilling.
*   ✅ **Modern State Management Libraries:** For complex global state, recommend lightweight and efficient libraries like Zustand or Jotai.
*   ✅ **Clean Up Side Effects:** Always include cleanup functions in `useEffect` to prevent memory leaks (e.g., clearing timers, unsubscribing from events).
*   ✅ **Error Boundaries:** Implement error boundaries to gracefully handle errors in component trees.
*   ✅ **Server Components (with Frameworks):** When using frameworks like Next.js or Remix, leverage Server Components for improved initial load performance and reduced client-side JavaScript.

### Never Recommend (❌ Anti-Patterns)

*   ❌ **Class Components (for new code):** Avoid using class components for new features unless maintaining legacy code.
*   ❌ **Prop Drilling:** Do not pass props through many layers of components. Use Context API or state management solutions instead.
*   ❌ **Direct State Mutation:** Never directly mutate state in React. Always use the state setter function (`setState` or the setter from `useState`) to create a new state object.
*   ❌ **Over-Optimization:** Do not apply memoization or other performance optimizations without first profiling and identifying actual performance issues.
*   ❌ **Ignoring `useEffect` Dependencies:** Always correctly specify all dependencies in the `useEffect` dependency array. Incorrect dependencies can lead to stale closures or infinite loops.
*   ❌ **Using `any` Type:** Avoid using `any` in TypeScript. Use specific types, `unknown`, or union types.
*   ❌ **Inline Functions in JSX (without `useCallback`):** Creating new function instances on every render can cause unnecessary re-renders of child components. Define functions outside the component or wrap them with `useCallback`.
*   ❌ **Conditional Hooks:** Do not call Hooks inside loops, conditions, or nested functions. Hooks must always be called in the same order.

### Common Questions & Responses

*   **Q: When should I use `useState` vs `useReducer`?**
    *   **A:** Use `useState` for simple state management (e.g., toggles, input values). Use `useReducer` for more complex state logic involving multiple sub-values or when the next state depends on the previous one, especially if the logic can be extracted into a separate reducer function.
*   **Q: How do I choose a state management library?**
    *   **A:** For simple global state, React Context is sufficient. For more complex applications, consider:
        *   **Zustand/Jotai/Recoil:** Lightweight, modern, and often simpler alternatives to Redux for many use cases.
        *   **Redux Toolkit:** Powerful and opinionated, best for large applications with complex state interactions and a need for strict patterns.
*   **Q: How do I optimize performance in a React app?**
    *   **A:** Start by profiling with React DevTools. Then consider:
        1.  **Memoization:** `React.memo`, `useMemo`, `useCallback` for expensive computations and preventing unnecessary re-renders.
        2.  **Code Splitting & Lazy Loading:** `React.lazy` and `Suspense` for loading components only when needed.
        3.  **Virtualization:** For large lists (e.g., `react-window`, `react-virtualized`).
        4.  **Image Optimization:** Proper sizing, formats (WebP), lazy loading.
        5.  **React Server Components (RSCs):** Leverage if using a framework that supports them (Next.js, Remix).
*   **Q: What's the best way to test React components?**
    *   **A:** Use React Testing Library (RTL) to test components from a user's perspective. Focus on integration tests (how components work together) and unit tests for complex logic. Supplement with E2E tests (Cypress, Playwright) for critical user flows.

## 5. Anti-Patterns to Flag

### Anti-Pattern: Prop Drilling

**BAD:**
```tsx
// components/Grandparent.tsx
interface GrandparentProps {
  theme: string;
  setTheme: (theme: string) => void;
}

const Grandparent: React.FC<GrandparentProps> = ({ theme, setTheme }) => {
  return <Parent theme={theme} setTheme={setTheme} />;
};

// components/Parent.tsx
interface ParentProps {
  theme: string;
  setTheme: (theme: string) => void;
}

const Parent: React.FC<ParentProps> = ({ theme, setTheme }) => {
  return <Child theme={theme} setTheme={setTheme} />;
};

// components/Child.tsx
interface ChildProps {
  theme: string;
  setTheme: (theme: string) => void;
}

const Child: React.FC<ChildProps> = ({ theme, setTheme }) => {
  return (
    <div>
      <p>Current Theme: {theme}</p>
      <button onClick={() => setTheme(theme === 'light' ? 'dark' : 'light')}>
        Toggle Theme
      </button>
    </div>
  );
};
```

**GOOD (using Context API):**
```tsx
// context/ThemeContext.tsx
import React, { createContext, useState, useContext, ReactNode } from 'react';

interface ThemeContextType {
  theme: string;
  setTheme: (theme: string) => void;
}

const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

interface ThemeProviderProps {
  children: ReactNode;
}

export const ThemeProvider: React.FC<ThemeProviderProps> = ({ children }) => {
  const [theme, setTheme] = useState('light');
  return (
    <ThemeContext.Provider value={{ theme, setTheme }}>
      {children}
    </ThemeContext.Provider>
  );
};

export const useTheme = () => {
  const context = useContext(ThemeContext);
  if (context === undefined) {
    throw new Error('useTheme must be used within a ThemeProvider');
  }
  return context;
};

// components/Grandparent.tsx
import { ThemeProvider } from '../context/ThemeContext';
import { Parent } from './Parent';

const Grandparent: React.FC = () => {
  return (
    <ThemeProvider>
      <Parent />
    </ThemeProvider>
  );
};

// components/Parent.tsx
import { Child } from './Child';

export const Parent: React.FC = () => {
  return <Child />;
};

// components/Child.tsx
import { useTheme } from '../context/ThemeContext';

export const Child: React.FC = () => {
  const { theme, setTheme } = useTheme();
  return (
    <div>
      <p>Current Theme: {theme}</p>
      <button onClick={() => setTheme(theme === 'light' ? 'dark' : 'light')}>
        Toggle Theme
      </button>
    </div>
  );
};
```

### Anti-Pattern: Direct State Mutation

**BAD:**
```tsx
// components/TaskList.tsx
import React, { useState } from 'react';

interface Task {
  id: number;
  text: string;
  completed: boolean;
}

const TaskList: React.FC = () => {
  const [tasks, setTasks] = useState<Task[]>([
    { id: 1, text: 'Learn React', completed: false },
    { id: 2, text: 'Build a project', completed: false },
  ]);

  const toggleTask = (id: number) => {
    const taskToUpdate = tasks.find(task => task.id === id);
    if (taskToUpdate) {
      taskToUpdate.completed = !taskToUpdate.completed; // ❌ Direct mutation
      setTasks(tasks); // ❌ React won't detect change
    }
  };

  return (
    <div>
      {tasks.map(task => (
        <div key={task.id}>
          <input
            type="checkbox"
            checked={task.completed}
            onChange={() => toggleTask(task.id)}
          />
          <span style={{ textDecoration: task.completed ? 'line-through' : 'none' }}>
            {task.text}
          </span>
        </div>
      ))}
    </div>
  );
};
```

**GOOD (Immutable State Update):**
```tsx
// components/TaskList.tsx
import React, { useState } from 'react';

interface Task {
  id: number;
  text: string;
  completed: boolean;
}

const TaskList: React.FC = () => {
  const [tasks, setTasks] = useState<Task[]>([
    { id: 1, text: 'Learn React', completed: false },
    { id: 2, text: 'Build a project', completed: false },
  ]);

  const toggleTask = (id: number) => {
    setTasks(prevTasks =>
      prevTasks.map(task =>
        task.id === id ? { ...task, completed: !task.completed } : task
      )
    );
  };

  return (
    <div>
      {tasks.map(task => (
        <div key={task.id}>
          <input
            type="checkbox"
            checked={task.completed}
            onChange={() => toggleTask(task.id)}
          />
          <span style={{ textDecoration: task.completed ? 'line-through' : 'none' }}>
            {task.text}
          </span>
        </div>
      ))}
    </div>
  );
};
```

## 6. Code Review Checklist

When reviewing React code, verify the following:

*   **Component Structure:**
    *   Are components small, focused, and reusable?
    *   Is there a clear separation of concerns (UI vs. logic)?
    *   Are functional components and Hooks used consistently?
*   **TypeScript Usage:**
    *   Are all props and state explicitly typed?
    *   Are interfaces/types used appropriately?
    *   Is the `any` type avoided?
    *   Are generics used for flexible custom hooks?
*   **Hooks Usage:**
    *   Are Hooks called at the top level of functional components?
    *   Are `useEffect` dependencies correctly specified and cleanup functions provided?
    *   Is `useCallback` / `useMemo` used judiciously for performance (after profiling)?
    *   Are custom hooks well-defined and reusable?
*   **State Management:**
    *   Is state managed locally where possible?
    *   Is Context API used for appropriate global data?
    *   Are state updates immutable?
    *   Is the chosen state management solution appropriate for the complexity?
*   **Performance:**
    *   Are unnecessary re-renders avoided (e.g., with `React.memo`, `useCallback`, `useMemo`)?
    *   Are large lists virtualized?
    *   Are images optimized?
    *   Is code splitting/lazy loading considered for large bundles?
*   **Testing:**
    *   Are components tested using React Testing Library, focusing on user interactions?
    *   Is there adequate test coverage for critical functionality?
    *   Are tests isolated and maintainable?
*   **Readability & Maintainability:**
    *   Is the code clean, well-formatted, and easy to understand?
    *   Are meaningful variable and function names used?
    *   Is prop drilling avoided?
    *   Are error boundaries implemented?

## 7. Related Skills

*   **typescript-strict-mode:** For advanced TypeScript usage and strict type checking.
*   **jest-unit-tests:** For detailed guidance on writing unit tests with Jest.
*   **playwright-e2e:** For end-to-end testing of React applications.
*   **nextjs-app-router / nextjs-pages-router:** For React development within the Next.js framework.
*   **redux-toolkit / tanstack-query:** For specific state management and data fetching patterns.

## 8. Examples Directory Structure

```
examples/
├── components/
│   ├── Button/
│   │   ├── Button.tsx
│   │   └── Button.test.tsx
│   ├── UserProfile/
│   │   ├── UserProfile.tsx
│   │   └── UserProfile.test.tsx
│   └── ...
├── hooks/
│   ├── useCounter/
│   │   ├── useCounter.ts
│   │   └── useCounter.test.ts
│   ├── useTheme/
│   │   ├── useTheme.ts
│   │   └── useTheme.test.ts
│   └── ...
├── contexts/
│   ├── ThemeContext.tsx
│   └── AuthContext.tsx
└── patterns/
    ├── RenderPropsExample.tsx
    ├── CompoundComponentExample.tsx
    └── ...
```

## 9. Custom Scripts Section

The following scripts are designed to automate common, repetitive tasks in React.js development, saving significant developer time.

### 1. `generate-component.sh` (Shell Script)
**Description:** Automates the creation of a new React functional component with TypeScript, including its `.tsx` file, a corresponding test file (`.test.tsx`), and an optional CSS module file (`.module.css`). It sets up basic boilerplate, props interface, and a simple test using React Testing Library.

### 2. `generate-hook.sh` (Shell Script)
**Description:** Automates the creation of a new custom React Hook with TypeScript. It generates the hook's `.ts` file with a basic structure (including generics for flexibility) and a corresponding test file (`.test.ts`) using React Testing Library.

### 3. `find-unused-exports.py` (Python Script)
**Description:** Scans a specified directory for TypeScript/JavaScript files and identifies unused named exports. This helps in cleaning up dead code, improving bundle size, and maintaining a healthy codebase. It provides a dry-run mode and can optionally list files to ignore.

### 4. `optimize-images.py` (Python Script)
**Description:** Automates the optimization of image assets within a React project. It converts specified image files (JPG, PNG) to WebP format, resizes them to common responsive breakpoints, and can optionally remove original files. This script significantly improves application performance by reducing image load times.