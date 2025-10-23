import React, { createContext, useContext, useState, useMemo, ReactNode } from 'react';

// 1. Define the Context's Data Shape
interface ThemeContextType {
  theme: 'light' | 'dark';
  toggleTheme: () => void;
}

// 2. Create the Context with a default value
const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

// 3. Create a Provider Component
interface ThemeProviderProps {
  children: ReactNode;
}

export const ThemeProvider: React.FC<ThemeProviderProps> = ({ children }) => {
  const [theme, setTheme] = useState<'light' | 'dark'>('light');

  const toggleTheme = () => {
    setTheme(prevTheme => (prevTheme === 'light' ? 'dark' : 'light'));
  };

  // Memoize the context value to prevent unnecessary re-renders of consumers
  const contextValue = useMemo(() => ({
    theme,
    toggleTheme,
  }), [theme]);

  return (
    <ThemeContext.Provider value={contextValue}>
      {children}
    </ThemeContext.Provider>
  );
};

// 4. Create a Custom Hook to consume the Context
export const useTheme = () => {
  const context = useContext(ThemeContext);
  if (context === undefined) {
    throw new Error('useTheme must be used within a ThemeProvider');
  }
  return context;
};

// Example of a component consuming the theme context
const ThemeDisplay: React.FC = () => {
  const { theme, toggleTheme } = useTheme();

  return (
    <div style={{
      background: theme === 'light' ? '#f0f0f0' : '#333',
      color: theme === 'light' ? '#333' : '#f0f0f0',
      padding: '20px',
      borderRadius: '8px',
      textAlign: 'center',
      marginTop: '20px'
    }}>
      <p>Current Theme: {theme}</p>
      <button onClick={toggleTheme}>Toggle Theme</button>
    </div>
  );
};

const SimpleThemeContext: React.FC = () => {
  return (
    <ThemeProvider>
      <h1>Simple Theme Context Example</h1>
      <ThemeDisplay />
    </ThemeProvider>
  );
};

export default SimpleThemeContext;
