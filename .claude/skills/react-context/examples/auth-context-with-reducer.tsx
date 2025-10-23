import React, { createContext, useContext, useReducer, useMemo, ReactNode, useCallback } from 'react';

// 1. Define State and Action Types
interface AuthState {
  isAuthenticated: boolean;
  user: { id: string; name: string; email: string } | null;
  token: string | null;
  isLoading: boolean;
  error: string | null;
}

type AuthAction =
  | { type: 'LOGIN_REQUEST' }
  | { type: 'LOGIN_SUCCESS'; payload: { user: AuthState['user']; token: string } }
  | { type: 'LOGIN_FAILURE'; payload: { error: string } }
  | { type: 'LOGOUT' };

// 2. Define Initial State
const initialAuthState: AuthState = {
  isAuthenticated: false,
  user: null,
  token: null,
  isLoading: false,
  error: null,
};

// 3. Create the Reducer Function
function authReducer(state: AuthState, action: AuthAction): AuthState {
  switch (action.type) {
    case 'LOGIN_REQUEST':
      return { ...state, isLoading: true, error: null };
    case 'LOGIN_SUCCESS':
      return {
        ...state,
        isAuthenticated: true,
        user: action.payload.user,
        token: action.payload.token,
        isLoading: false,
        error: null,
      };
    case 'LOGIN_FAILURE':
      return { ...state, isAuthenticated: false, user: null, token: null, isLoading: false, error: action.payload.error };
    case 'LOGOUT':
      return { ...initialAuthState };
    default:
      return state;
  }
}

// 4. Define the Context's Data Shape
interface AuthContextType extends AuthState {
  login: (username: string, password: string) => Promise<void>;
  logout: () => void;
}

// 5. Create the Context
const AuthContext = createContext<AuthContextType | undefined>(undefined);

// 6. Create a Provider Component
interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [state, dispatch] = useReducer(authReducer, initialAuthState);

  const login = useCallback(async (username, password) => {
    dispatch({ type: 'LOGIN_REQUEST' });
    try {
      // Simulate API call
      const response = await new Promise<{ user: AuthState['user']; token: string }>((resolve, reject) => {
        setTimeout(() => {
          if (username === 'user' && password === 'password') {
            resolve({
              user: { id: '1', name: 'Test User', email: 'test@example.com' },
              token: 'fake-jwt-token',
            });
          } else {
            reject(new Error('Invalid credentials'));
          }
        }, 1000);
      });
      dispatch({ type: 'LOGIN_SUCCESS', payload: response });
    } catch (err: any) {
      dispatch({ type: 'LOGIN_FAILURE', payload: { error: err.message } });
    }
  }, []);

  const logout = useCallback(() => {
    dispatch({ type: 'LOGOUT' });
  }, []);

  const contextValue = useMemo(() => ({
    ...state,
    login,
    logout,
  }), [state, login, logout]);

  return (
    <AuthContext.Provider value={contextValue}>
      {children}
    </AuthContext.Provider>
  );
};

// 7. Create a Custom Hook to consume the Context
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

// Example Components
const LoginForm: React.FC = () => {
  const { login, isLoading, error } = useAuth();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    await login(username, password);
  };

  return (
    <form onSubmit={handleSubmit}>
      <h3>Login</h3>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <div>
        <label>Username:</label>
        <input type="text" value={username} onChange={(e) => setUsername(e.target.value)} />
      </div>
      <div>
        <label>Password:</label>
        <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
      </div>
      <button type="submit" disabled={isLoading}>
        {isLoading ? 'Logging in...' : 'Login'}
      </button>
    </form>
  );
};

const UserProfile: React.FC = () => {
  const { isAuthenticated, user, logout } = useAuth();

  if (!isAuthenticated || !user) {
    return <p>Not logged in.</p>;
  }

  return (
    <div>
      <h3>Welcome, {user.name}!</h3>
      <p>Email: {user.email}</p>
      <button onClick={logout}>Logout</button>
    </div>
  );
};

const AuthContextWithReducer: React.FC = () => {
  const { isAuthenticated } = useAuth();

  return (
    <AuthProvider>
      <h1>Auth Context with useReducer Example</h1>
      {isAuthenticated ? <UserProfile /> : <LoginForm />}
    </AuthProvider>
  );
};

export default AuthContextWithReducer;
