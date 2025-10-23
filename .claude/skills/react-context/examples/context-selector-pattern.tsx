import React, { createContext, useContext, useState, useEffect, useRef, ReactNode, useReducer } from 'react';

// 1. Define the Context's Data Shape
interface StoreState {
  count: number;
  text: string;
  user: { name: string; age: number };
}

interface StoreContextType {
  state: StoreState;
  dispatch: React.Dispatch<StoreAction>;
}

type StoreAction =
  | { type: 'INCREMENT' }
  | { type: 'DECREMENT' }
  | { type: 'SET_TEXT'; payload: string }
  | { type: 'SET_USER_NAME'; payload: string }
  | { type: 'SET_USER_AGE'; payload: number };

// 2. Initial State and Reducer
const initialStoreState: StoreState = {
  count: 0,
  text: 'Hello',
  user: { name: 'Alice', age: 30 },
};

function storeReducer(state: StoreState, action: StoreAction): StoreState {
  switch (action.type) {
    case 'INCREMENT':
      return { ...state, count: state.count + 1 };
    case 'DECREMENT':
      return { ...state, count: state.count - 1 };
    case 'SET_TEXT':
      return { ...state, text: action.payload };
    case 'SET_USER_NAME':
      return { ...state, user: { ...state.user, name: action.payload } };
    case 'SET_USER_AGE':
      return { ...state, user: { ...state.user, age: action.payload } };
    default:
      return state;
  }
}

// 3. Create the Context
const StoreContext = createContext<StoreContextType | undefined>(undefined);

// 4. Create a Provider Component
interface StoreProviderProps {
  children: ReactNode;
}

export const StoreProvider: React.FC<StoreProviderProps> = ({ children }) => {
  const [state, dispatch] = useReducer(storeReducer, initialStoreState);

  // Memoize the context value to prevent unnecessary re-renders of consumers
  const contextValue = useRef({ state, dispatch });
  contextValue.current = { state, dispatch }; // Always keep current value updated

  return (
    <StoreContext.Provider value={contextValue.current}>
      {children}
    </StoreContext.Provider>
  );
};

// 5. Custom Hook for Context Selection
// This is a simplified implementation of a context selector.
// In a real-world scenario, you might use a library or `useSyncExternalStore` for better performance.
export function useContextSelector<T>(selector: (state: StoreState) => T): T {
  const context = useContext(StoreContext);
  if (context === undefined) {
    throw new Error('useContextSelector must be used within a StoreProvider');
  }

  const selectedValue = selector(context.state);
  const [value, setValue] = useState(selectedValue);
  const latestSelector = useRef(selector);
  latestSelector.current = selector;

  useEffect(() => {
    // This effect runs whenever the context's state changes.
    // We re-evaluate the selector and update local state only if the selected value has changed.
    const newSelectedValue = latestSelector.current(context.state);
    if (newSelectedValue !== value) { // Simple shallow comparison
      setValue(newSelectedValue);
    }
  }, [context.state, value]); // Depend on context.state and local value

  return value;
}

// --- Example Components ---

const CounterDisplay: React.FC = () => {
  // Only re-renders when count changes
  const count = useContextSelector(state => state.count);
  console.log('Rendering CounterDisplay');
  return <p>Count: {count}</p>;
};

const TextDisplay: React.FC = () => {
  // Only re-renders when text changes
  const text = useContextSelector(state => state.text);
  console.log('Rendering TextDisplay');
  return <p>Text: {text}</p>;
};

const UserNameDisplay: React.FC = () => {
  // Only re-renders when user.name changes
  const userName = useContextSelector(state => state.user.name);
  console.log('Rendering UserNameDisplay');
  return <p>User Name: {userName}</p>;
};

const UserAgeDisplay: React.FC = () => {
  // Only re-renders when user.age changes
  const userAge = useContextSelector(state => state.user.age);
  console.log('Rendering UserAgeDisplay');
  return <p>User Age: {userAge}</p>;
};

const Controls: React.FC = () => {
  const context = useContext(StoreContext);
  if (!context) return null; // Should not happen with the check in useContextSelector

  const { dispatch } = context;

  return (
    <div>
      <button onClick={() => dispatch({ type: 'INCREMENT' })}>Increment Count</button>
      <button onClick={() => dispatch({ type: 'DECREMENT' })}>Decrement Count</button>
      <input
        type="text"
        value={useContextSelector(state => state.text)} // Use selector for input value
        onChange={(e) => dispatch({ type: 'SET_TEXT', payload: e.target.value })}
        placeholder="Set Text"
      />
      <input
        type="text"
        value={useContextSelector(state => state.user.name)} // Use selector for input value
        onChange={(e) => dispatch({ type: 'SET_USER_NAME', payload: e.target.value })}
        placeholder="Set User Name"
      />
      <input
        type="number"
        value={useContextSelector(state => state.user.age)} // Use selector for input value
        onChange={(e) => dispatch({ type: 'SET_USER_AGE', payload: Number(e.target.value) })}
        placeholder="Set User Age"
      />
    </div>
  );
};

const ContextSelectorPattern: React.FC = () => {
  return (
    <StoreProvider>
      <h2>Context Selector Pattern Example</h2>
      <p>Open console to see re-render logs.</p>
      <Controls />
      <hr />
      <CounterDisplay />
      <TextDisplay />
      <UserNameDisplay />
      <UserAgeDisplay />
    </StoreProvider>
  );
};

export default ContextSelectorPattern;
