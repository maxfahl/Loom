/**
 * @typedef {import('./config').AppConfig} AppConfig
 * @typedef {import('./config').FeatureFlags} FeatureFlags
 */

/** @type {AppConfig} */
const appConfig = {
  apiUrl: "https://api.example.com",
  timeout: 5000,
  debugMode: true,
};

/** @type {FeatureFlags} */
const featureFlags = {
  newDashboard: true,
  betaSearch: false,
};

/**
 * Initializes the application with the given configuration.
 * @param {AppConfig} config - The application configuration.
 * @param {FeatureFlags} flags - The feature flags.
 */
function initializeApp(config, flags) {
  console.log("App initialized with config:", config);
  console.log("Feature flags:", flags);
}

initializeApp(appConfig, featureFlags);
