import React, { createContext, useContext, useState, useMemo, ReactNode } from 'react';

// --- Theme Context ---
interface ThemeContextType {
  theme: 'light' | 'dark';
  toggleTheme: () => void;
}
const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

export const ThemeProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [theme, setTheme] = useState<'light' | 'dark'>('light');
  const toggleTheme = () => setTheme(prev => (prev === 'light' ? 'dark' : 'light'));
  const value = useMemo(() => ({ theme, toggleTheme }), [theme]);
  return <ThemeContext.Provider value={value}>{children}</ThemeContext.Provider>;
};

export const useTheme = () => {
  const context = useContext(ThemeContext);
  if (context === undefined) throw new Error('useTheme must be used within a ThemeProvider');
  return context;
};

// --- Language Context ---
interface LanguageContextType {
  lang: 'en' | 'es';
  setLang: (lang: 'en' | 'es') => void;
}
const LanguageContext = createContext<LanguageContextType | undefined>(undefined);

export const LanguageProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [lang, setLang] = useState<'en' | 'es'>('en');
  const value = useMemo(() => ({ lang, setLang }), [lang]);
  return <LanguageContext.Provider value={value}>{children}</LanguageContext.Provider>;
};

export const useLanguage = () => {
  const context = useContext(LanguageContext);
  if (context === undefined) throw new Error('useLanguage must be used within a LanguageProvider');
  return context;
};

// --- User Settings Context ---
interface UserSettingsContextType {
  notificationsEnabled: boolean;
  toggleNotifications: () => void;
}
const UserSettingsContext = createContext<UserSettingsContextType | undefined>(undefined);

export const UserSettingsProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [notificationsEnabled, setNotificationsEnabled] = useState(true);
  const toggleNotifications = () => setNotificationsEnabled(prev => !prev);
  const value = useMemo(() => ({ notificationsEnabled, toggleNotifications }), [notificationsEnabled]);
  return <UserSettingsContext.Provider value={value}>{children}</UserSettingsContext.Provider>;
};

export const useUserSettings = () => {
  const context = useContext(UserSettingsContext);
  if (context === undefined) throw new Error('useUserSettings must be used within a UserSettingsProvider');
  return context;
};

// --- Combined Provider ---
interface AppProviderProps {
  children: ReactNode;
}

export const AppProvider: React.FC<AppProviderProps> = ({ children }) => {
  return (
    <ThemeProvider>
      <LanguageProvider>
        <UserSettingsProvider>
          {children}
        </UserSettingsProvider>
      </LanguageProvider>
    </ThemeProvider>
  );
};

// --- Example Components ---
const Header: React.FC = () => {
  const { theme } = useTheme();
  const { lang } = useLanguage();
  return (
    <header style={{ background: theme === 'light' ? '#eee' : '#444', color: theme === 'light' ? '#333' : '#eee', padding: '10px' }}>
      <h1>Multi-Context App ({lang.toUpperCase()})</h1>
    </header>
  );
};

const SettingsPanel: React.FC = () => {
  const { theme, toggleTheme } = useTheme();
  const { lang, setLang } = useLanguage();
  const { notificationsEnabled, toggleNotifications } = useUserSettings();

  return (
    <div style={{ padding: '20px', border: '1px solid #ccc', margin: '20px 0' }}>
      <h3>Settings</h3>
      <div>
        <label>Theme:</label>
        <button onClick={toggleTheme}>Switch to {theme === 'light' ? 'Dark' : 'Light'}</button>
      </div>
      <div>
        <label>Language:</label>
        <select value={lang} onChange={(e) => setLang(e.target.value as 'en' | 'es')}>
          <option value="en">English</option>
          <option value="es">Spanish</option>
        </select>
      </div>
      <div>
        <label>
          <input type="checkbox" checked={notificationsEnabled} onChange={toggleNotifications} />
          Enable Notifications
        </label>
      </div>
    </div>
  );
};

const Content: React.FC = () => {
  const { theme } = useTheme();
  const { lang } = useLanguage();
  const { notificationsEnabled } = useUserSettings();

  const messages = {
    en: {
      welcome: "Welcome to the multi-context example!",
      notifications: notificationsEnabled ? "Notifications are ON." : "Notifications are OFF.",
    },
    es: {
      welcome: "¡Bienvenido al ejemplo de multi-contexto!",
      notifications: notificationsEnabled ? "Las notificaciones están ACTIVADAS." : "Las notificaciones están DESACTIVADAS.",
    },
  };

  return (
    <main style={{ background: theme === 'light' ? '#fff' : '#222', color: theme === 'light' ? '#222' : '#fff', padding: '20px' }}>
      <p>{messages[lang].welcome}</p>
      <p>{messages[lang].notifications}</p>
    </main>
  );
};

const MultiContextExample: React.FC = () => {
  return (
    <AppProvider>
      <Header />
      <SettingsPanel />
      <Content />
    </AppProvider>
  );
};

export default MultiContextExample;
