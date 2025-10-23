// config.d.ts

declare interface AppConfig {
  apiUrl: string;
  timeout: number;
  debugMode: boolean;
}

declare interface FeatureFlags {
  newDashboard: boolean;
  betaSearch: boolean;
}

declare interface UserSettings {
  theme: 'light' | 'dark';
  notifications: boolean;
}

export { AppConfig, FeatureFlags, UserSettings };
