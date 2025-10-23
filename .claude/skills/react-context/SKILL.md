---
Name: react-context
Version: 1.0.0
Category: Web Development / React
Tags: React, Context API, useContext, global state, prop drilling, state management
Description: Guiding Claude on effective and idiomatic use of React Context for state management.
---

# React Context Skill

## 1. Skill Purpose

This skill enables Claude to understand, generate, and review React code utilizing the Context API (`createContext`, `Provider`, `Consumer`, `useContext`) for efficient global state management and avoiding prop drilling. It emphasizes best practices for performance, maintainability, and appropriate use cases.

## 2. When to Activate This Skill

Activate when:
- Managing global application state (e.g., user authentication, theme, language settings).
- Avoiding prop drilling in deeply nested component trees.
- Sharing data that is considered "global" for a subtree of components.
- Creating a custom state management solution for a specific domain.
- Reviewing existing React Context API implementations.
- Discussing alternatives to prop drilling or simple global state.

## 3. Core Knowledge

- **`createContext`**: Creating a Context object.
- **`Context.Provider`**: The component that provides the value to its descendants.
- **`Context.Consumer`**: (Legacy) A component that subscribes to context changes.
- **`useContext`**: The primary hook for consuming context in functional components.
- **Provider Placement**: Placing the `Provider` component as high up in the component tree as possible.
- **Default Values**: Providing a default value to `createContext` for testing and fallback.
- **Performance Considerations**:
    - Re-renders: All consumers re-render when the context value changes.
    - Memoization: Using `React.memo`, `useMemo`, and `useCallback` to optimize performance.
    - Splitting Contexts: Creating smaller, more focused contexts instead of a single monolithic one.
    - Selector Pattern: Subscribing only to specific parts of the context.
- **Combining with Hooks**: Using `useState` or `useReducer` within the `Provider` to manage the context's state.

## 4. Key Guidance for Claude

### Always Recommend (✅ best practices)
- ✅ Use `useContext` for consuming context in functional components.
- ✅ Create specific, focused contexts instead of a single, large context.
- ✅ Place the `Provider` as high as necessary in the component tree.
- ✅ Provide a default value to `createContext` for better testability and fallbacks.
- ✅ Combine Context with `useState` or `useReducer` for managing the context's state.
- ✅ Memoize the `value` prop passed to `Context.Provider` using `useMemo` if it's an object or array and contains values that don't change frequently, to prevent unnecessary re-renders of consumers.
- ✅ Use `React.memo` for consumer components if they are pure and their props (including context values) don't frequently change.
- ✅ Consider a "selector pattern" for large contexts to allow consumers to subscribe only to relevant parts.
- ✅ Use Context for truly global or subtree-global data that changes infrequently.

### Never Recommend (❌ anti-patterns)
- ❌ Using Context for every piece of state; prefer local state (`useState`) or prop drilling for localized data.
- ❌ Creating a single, monolithic context for all application state, as this leads to frequent re-renders of all consumers.
- ❌ Passing a new object or array literal directly as the `value` prop to `Context.Provider` on every render without `useMemo`, as this will cause all consumers to re-render unnecessarily.
- ❌ Using `Context.Consumer` in new functional components; `useContext` is the modern and preferred approach.
- ❌ Overusing Context for complex state logic that would be better handled by dedicated state management libraries (e.g., Redux, Zustand) in large applications.
- ❌ Deeply nesting many unrelated Context Providers, which can make the component tree hard to read and manage.

### Common Questions & Responses (FAQ format)
- **Q: When should I use React Context instead of prop drilling?**
    - A: Use Context when data needs to be accessed by many components at different nesting levels, and passing props manually becomes cumbersome ("prop drilling"). For data only relevant to a few components, prop drilling is often simpler.
- **Q: How can I prevent unnecessary re-renders when using Context?**
    - A: Split your global state into smaller, more specific contexts. Memoize the `value` prop of your `Provider` using `useMemo`. Use `React.memo` for consumer components. Consider a selector pattern if your context value is large and consumers only need parts of it.
- **Q: Is React Context a replacement for Redux?**
    - A: Not entirely. Context is great for simpler global state and dependency injection. For very large applications with complex state logic, middleware, and a need for a predictable state container, libraries like Redux (often with Redux Toolkit) might still be more suitable. Context can be used *with* `useReducer` to build a Redux-like store, but it doesn't provide all the features out-of-the-box.
- **Q: How do I update the context value?**
    - A: The context value is typically managed by state (`useState` or `useReducer`) within the `Provider` component. The `Provider` then exposes the current state and a function to update it (e.g., a `setState` function or a `dispatch` function) through its `value` prop.

## 5. Anti-Patterns to Flag

```typescript
// BAD: Monolithic context, causing all consumers to re-render on any change
interface AppState {
  user: { name: string; id: string } | null;
  theme: 'light' | 'dark';
  notifications: string[];
  settings: { sound: boolean; language: string };
}

const AppContext = createContext<AppState | undefined>(undefined);

const AppProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [state, setState] = useState<AppState>({ /* initial state */ });
  // Any update to user, theme, notifications, or settings will re-render ALL consumers
  return <AppContext.Provider value={state}>{children}</AppContext.Provider>;
};

// GOOD: Split contexts for better performance and separation of concerns
interface UserContextType {
  user: { name: string; id: string } | null;
  setUser: (user: { name: string; id: string } | null) => void;
}
const UserContext = createContext<UserContextType | undefined>(undefined);

interface ThemeContextType {
  theme: 'light' | 'dark';
  toggleTheme: () => void;
}
const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

const UserProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<UserContextType['user']>(null);
  const value = useMemo(() => ({ user, setUser }), [user]); // Memoize value
  return <UserContext.Provider value={value}>{children}</UserContext.Provider>;
};

const ThemeProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [theme, setTheme] = useState<'light' | 'dark'>('light');
  const toggleTheme = useCallback(() => {
    setTheme(prev => (prev === 'light' ? 'dark' : 'light'));
  }, []);
  const value = useMemo(() => ({ theme, toggleTheme }), [theme, toggleTheme]); // Memoize value
  return <ThemeContext.Provider value={value}>{children}</useContext.Provider>;
};

// BAD: Passing a new object literal directly as value prop without memoization
const MyProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [count, setCount] = useState(0);
  // ❌ `value` object is new on every render, causing all consumers to re-render
  return <MyContext.Provider value={{ count, setCount }}>{children}</MyContext.Provider>;
};

// GOOD: Memoizing the value prop
const MyProviderGood: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [count, setCount] = useState(0);
  const value = useMemo(() => ({ count, setCount }), [count]); // ✅ `value` is memoized
  return <MyContext.Provider value={value}>{children}</MyContext.Provider>;
};

// BAD: Using Context.Consumer in modern functional components
const MyComponentBad: React.FC = () => {
  return (
    <MyContext.Consumer>
      {(value) => <div>{value.data}</div>}
    </MyContext.Consumer>
  );
};

// GOOD: Using useContext hook
const MyComponentGood: React.FC = () => {
  const value = useContext(MyContext);
  return <div>{value?.data}</div>;
};
```

## 6. Code Review Checklist
- [ ] Is `useContext` used for consuming context in functional components?
- [ ] Are contexts specific and focused, avoiding monolithic global state?
- [ ] Is the `Provider` placed appropriately high in the component tree?
- [ ] Is the `value` prop passed to `Context.Provider` memoized using `useMemo` if it's an object or array?
- [ ] Are `useState` or `useReducer` used within the `Provider` to manage the context's state?
- [ ] Are `React.memo` or other memoization techniques applied to consumer components where performance is critical?
- [ ] Is Context used for truly global/subtree-global data, not for localized state?
- [ ] Is a default value provided to `createContext`?
- [ ] Are there any `Context.Consumer` components that could be replaced with `useContext`?

## 7. Related Skills
- `react-hooks` (especially `useState`, `useReducer`, `useMemo`, `useCallback`)

## 8. Examples Directory Structure
- `examples/`
    - `simple-theme-context.tsx`
    - `auth-context-with-reducer.tsx`
    - `multi-context-example.tsx`
    - `context-selector-pattern.tsx`

## 9. Custom Scripts Section

### 9.1. `generate-context.sh`
- **Purpose**: Automates the creation of a React Context boilerplate, including `createContext`, a `Provider` component, and a custom `useContext` hook.
- **Usage**: `./scripts/generate-context.sh <ContextName>`

### 9.2. `refactor-consumer-to-usecontext.py`
- **Purpose**: Helps refactor `Context.Consumer` components to use the `useContext` hook, providing a guide for manual conversion.
- **Usage**: `python scripts/refactor-consumer-to-usecontext.py <filePath>`

### 9.3. `analyze-context-re-renders.py`
- **Purpose**: Scans a TypeScript/JavaScript file for `Context.Provider` usage and identifies potential re-render issues if the `value` prop is not memoized.
- **Usage**: `python scripts/analyze-context-re-renders.py <filePath>`

### 9.4. `generate-nested-context.sh`
- **Purpose**: Generates a boilerplate for a nested context structure, demonstrating how to combine multiple contexts effectively.
- **Usage**: `./scripts/generate-nested-context.sh <ParentContextName> <ChildContextName1> [ChildContextName2...]`