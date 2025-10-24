/**
 * Configuration Manager - Handles loading, saving, and managing AML configuration
 */

import * as fs from 'fs/promises';
import * as path from 'path';
import {
  AMLConfig,
  AgentConfig,
  DEFAULT_AML_CONFIG,
  validateConfig,
  mergeConfig,
  getAgentConfig,
} from './schema';

export class ConfigManager {
  private config: AMLConfig;
  private configPath: string;
  private loaded: boolean = false;

  constructor(configPath?: string) {
    this.configPath = configPath || path.join(process.cwd(), '.loom/memory/config.json');
    this.config = { ...DEFAULT_AML_CONFIG };
  }

  /**
   * Load configuration from file
   */
  async load(): Promise<void> {
    try {
      const fileContent = await fs.readFile(this.configPath, 'utf-8');
      const userConfig = JSON.parse(fileContent);

      const validation = validateConfig(userConfig);
      if (!validation.valid) {
        throw new Error(`Invalid configuration: ${validation.errors?.join(', ')}`);
      }

      this.config = validation.config!;
      this.loaded = true;
    } catch (error) {
      if ((error as NodeJS.ErrnoException).code === 'ENOENT') {
        // File doesn't exist, use defaults and create it
        await this.save();
        this.loaded = true;
      } else {
        throw new Error(`Failed to load configuration: ${(error as Error).message}`);
      }
    }
  }

  /**
   * Save current configuration to file
   */
  async save(): Promise<void> {
    try {
      // Ensure directory exists
      const dir = path.dirname(this.configPath);
      await fs.mkdir(dir, { recursive: true });

      // Write config file with pretty formatting
      await fs.writeFile(this.configPath, JSON.stringify(this.config, null, 2), 'utf-8');
    } catch (error) {
      throw new Error(`Failed to save configuration: ${(error as Error).message}`);
    }
  }

  /**
   * Get current configuration
   */
  getConfig(): AMLConfig {
    if (!this.loaded) {
      throw new Error('Configuration not loaded. Call load() first.');
    }
    return { ...this.config };
  }

  /**
   * Update configuration
   */
  async updateConfig(updates: Partial<AMLConfig>): Promise<void> {
    this.config = mergeConfig({ ...this.config, ...updates });
    await this.save();
  }

  /**
   * Get configuration for a specific agent
   */
  getAgentConfig(agentName: string): ReturnType<typeof getAgentConfig> {
    if (!this.loaded) {
      throw new Error('Configuration not loaded. Call load() first.');
    }
    return getAgentConfig(this.config, agentName);
  }

  /**
   * Update agent-specific configuration
   */
  async updateAgentConfig(agentName: string, agentConfig: Partial<AgentConfig>): Promise<void> {
    if (!this.config.agentOverrides) {
      this.config.agentOverrides = {};
    }

    this.config.agentOverrides[agentName] = {
      ...this.config.agentOverrides[agentName],
      ...agentConfig,
    };

    await this.save();
  }

  /**
   * Enable/disable AML globally
   */
  async setEnabled(enabled: boolean): Promise<void> {
    this.config.enabled = enabled;
    await this.save();
  }

  /**
   * Enable/disable AML for specific agent
   */
  async setAgentEnabled(agentName: string, enabled: boolean): Promise<void> {
    await this.updateAgentConfig(agentName, { enabled, agent: agentName });
  }

  /**
   * Reset configuration to defaults
   */
  async reset(): Promise<void> {
    this.config = { ...DEFAULT_AML_CONFIG };
    await this.save();
  }

  /**
   * Load configuration from environment variables
   */
  loadFromEnv(): void {
    const env = process.env;

    // Global settings
    if (env.AML_ENABLED !== undefined) {
      this.config.enabled = env.AML_ENABLED === 'true';
    }

    // Storage settings
    if (env.AML_STORAGE_PATH) {
      this.config.storage.path = env.AML_STORAGE_PATH;
    }
    if (env.AML_ENCRYPTION !== undefined) {
      this.config.storage.encryption = env.AML_ENCRYPTION === 'true';
    }
    if (env.AML_COMPRESSION !== undefined) {
      this.config.storage.compression = env.AML_COMPRESSION === 'true';
    }
    if (env.AML_MAX_SIZE_GB) {
      this.config.storage.maxSizeGb = parseFloat(env.AML_MAX_SIZE_GB);
    }

    // Learning settings
    if (env.AML_LEARNING_RATE) {
      this.config.learning.learningRate = parseFloat(env.AML_LEARNING_RATE);
    }
    if (env.AML_MIN_CONFIDENCE) {
      this.config.learning.minConfidence = parseFloat(env.AML_MIN_CONFIDENCE);
    }

    // Performance settings
    if (env.AML_CACHE_ENABLED !== undefined) {
      this.config.performance.cacheEnabled = env.AML_CACHE_ENABLED === 'true';
    }
    if (env.AML_QUERY_TIMEOUT_MS) {
      this.config.performance.queryTimeoutMs = parseInt(env.AML_QUERY_TIMEOUT_MS, 10);
    }

    // Validate merged config
    const validation = validateConfig(this.config);
    if (!validation.valid) {
      throw new Error(`Invalid environment configuration: ${validation.errors?.join(', ')}`);
    }
  }

  /**
   * Export configuration for sharing
   */
  exportConfig(): string {
    return JSON.stringify(this.config, null, 2);
  }

  /**
   * Import configuration from string
   */
  async importConfig(configJson: string): Promise<void> {
    try {
      const imported = JSON.parse(configJson);
      const validation = validateConfig(imported);

      if (!validation.valid) {
        throw new Error(`Invalid configuration: ${validation.errors?.join(', ')}`);
      }

      this.config = validation.config!;
      await this.save();
    } catch (error) {
      throw new Error(`Failed to import configuration: ${(error as Error).message}`);
    }
  }

  /**
   * Get configuration file path
   */
  getConfigPath(): string {
    return this.configPath;
  }

  /**
   * Check if configuration is loaded
   */
  isLoaded(): boolean {
    return this.loaded;
  }
}

// Singleton instance
let configManagerInstance: ConfigManager | null = null;

/**
 * Get singleton configuration manager instance
 */
export function getConfigManager(configPath?: string): ConfigManager {
  if (!configManagerInstance) {
    configManagerInstance = new ConfigManager(configPath);
  }
  return configManagerInstance;
}

/**
 * Reset singleton (useful for testing)
 */
export function resetConfigManager(): void {
  configManagerInstance = null;
}
