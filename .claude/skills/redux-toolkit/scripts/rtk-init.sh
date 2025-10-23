#!/bin/bash

# rtk-init.sh
# Description: Initializes a new React project (using Vite) with Redux Toolkit,
#              including a basic store, typed hooks, and a sample counter slice.
# Usage: ./rtk-init.sh [project_name]
#        If project_name is not provided, it defaults to 'react-rtk-app'.

set -e # Exit immediately if a command exits with a non-zero status.

PROJECT_NAME=${1:-react-rtk-app}

echo "Initializing React + Redux Toolkit project: $PROJECT_NAME"

# 1. Create a new React project with Vite and TypeScript
echo "Creating React project with Vite and TypeScript..."
npm create vite "$PROJECT_NAME" -- --template react-ts > /dev/null
cd "$PROJECT_NAME"

# 2. Install Redux Toolkit and React-Redux
echo "Installing Redux Toolkit and React-Redux..."
npm install @reduxjs/toolkit react-redux > /dev/null
npm install -D @types/react-redux > /dev/null

# 3. Create src/app directory
mkdir -p src/app

# 4. Create src/app/store.ts
echo "Creating src/app/store.ts..."
cat << EOF > src/app/store.ts
import { configureStore } from '@reduxjs/toolkit';
import counterReducer from '../features/counter/counterSlice';

export const store = configureStore({
  reducer: {
    counter: counterReducer,
  },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
EOF

# 5. Create src/app/hooks.ts
echo "Creating src/app/hooks.ts..."
cat << EOF > src/app/hooks.ts
import { useDispatch, useSelector } from 'react-redux';
import type { TypedUseSelectorHook } from 'react-redux';
import type { RootState, AppDispatch } from './store';

export const useAppDispatch: () => AppDispatch = useDispatch;
export const useAppSelector: TypedUseSelectorHook<RootState> = useSelector;
EOF

# 6. Create src/features/counter directory and counterSlice.ts
mkdir -p src/features/counter
echo "Creating src/features/counter/counterSlice.ts..."
cat << EOF > src/features/counter/counterSlice.ts
import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface CounterState {
  value: number;
}

const initialState: CounterState = {
  value: 0,
};

export const counterSlice = createSlice({
  name: 'counter',
  initialState,
  reducers: {
    increment: (state) => {
      state.value += 1;
    },
    decrement: (state) => {
      state.value -= 1;
    },
    incrementByAmount: (state, action: PayloadAction<number>) => {
      state.value += action.payload;
    },
  },
});

export const { increment, decrement, incrementByAmount } = counterSlice.actions;

export default counterSlice.reducer;
EOF

# 7. Create src/features/counter/Counter.tsx (component)
echo "Creating src/features/counter/Counter.tsx..."
cat << EOF > src/features/counter/Counter.tsx
import React from 'react';
import { useAppSelector, useAppDispatch } from '../../app/hooks';
import { increment, decrement, incrementByAmount } from './counterSlice';

const Counter: React.FC = () => {
  const count = useAppSelector((state) => state.counter.value);
  const dispatch = useAppDispatch();

  return (
    <div>
      <h2>Counter: {count}</h2>
      <button onClick={() => dispatch(increment())}>Increment</button>
      <button onClick={() => dispatch(decrement())}>Decrement</button>
      <button onClick={() => dispatch(incrementByAmount(5))}>Increment by 5</button>
    </div>
  );
};

export default Counter;
EOF

# 8. Update src/App.tsx to use the Redux store and Counter component
echo "Updating src/App.tsx..."
cat << EOF > src/App.tsx
import React from 'react';
import { Provider } from 'react-redux';
import { store } from './app/store';
import Counter from './features/counter/Counter';

function App() {
  return (
    <Provider store={store}>
      <div className="App">
        <header className="App-header">
          <h1>Vite + React + Redux Toolkit</h1>
          <Counter />
        </header>
      </div>
    </Provider>
  );
}

export default App;
EOF

echo "Project '$PROJECT_NAME' initialized successfully!"
echo ""
echo "To get started:"
echo "  cd $PROJECT_NAME"
echo "  npm install"
echo "  npm run dev"
