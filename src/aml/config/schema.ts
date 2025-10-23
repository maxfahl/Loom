/**
 * Configuration schemas and validation for AML system
 */

import { z } from 'zod';

// Storage configuration
export const StorageConfigSchema = z.object({
  backend: z.enum(['filesystem']).default('filesystem'),
  path: z.string().default('.loom/memory'),
  encryption: z.boolean().default(true),
  compression: z.boolean().default(true),
  maxSizeGb: z.number().min(0.1).max(10).default(1),
  backupEnabled: z.boolean().default(true),
  backupPath: z.string().default('.loom/memory-backup'),
  backupSchedule: z.enum(['hourly', 'daily', 'weekly']).default('daily'),
});

// Learning configuration
export const LearningConfigSchema = z.object({
  minConfidence: z.number().min(0).max(1).default(0.3),
  promotionThreshold: z.number().int().min(1).default(3),
  learningRate: z.number().min(0).max(1).default(0.1),
  discountFactor: z.number().min(0).max(1).default(0.9),
  explorationRate: z.number().min(0).max(1).default(0.2),
});

// Pruning configuration
export const PruningConfigSchema = z.object({
  enabled: z.boolean().default(true),
  schedule: z.enum(['hourly', 'daily', 'weekly']).default('daily'),
  maxAgeDays: z.number().int().min(1).default(90),
  minConfidence: z.number().min(0).max(1).default(0.2),
  minUsageRate: z.number().min(0).default(0.1),
  aggressiveMode: z.boolean().default(false),
});

// Sharing configuration
export const SharingConfigSchema = z.object({
  crossAgent: z.boolean().default(true),
  crossProject: z.boolean().default(false),
  telemetry: z.enum(['none', 'anonymous', 'full']).default('anonymous'),
  syncEnabled: z.boolean().default(false),
  syncPath: z.string().optional(),
});

// Performance configuration
export const PerformanceConfigSchema = z.object({
  cacheEnabled: z.boolean().default(true),
  cacheMaxSizeMb: z.number().min(10).max(1000).default(100),
  cacheTtlSeconds: z.number().int().min(60).default(3600),
  queryTimeoutMs: z.number().int().min(10).max(5000).default(50),
  writeTimeoutMs: z.number().int().min(50).max(10000).default(100),
  indexingEnabled: z.boolean().default(true),
});

// Agent-specific configuration
export const AgentConfigSchema = z.object({
  agent: z.string(),
  enabled: z.boolean().default(true),
  memoryLimitMb: z.number().min(10).max(500).default(100),
  learning: LearningConfigSchema.partial().optional(),
  focusAreas: z.array(z.string()).optional(),
  maxPatternCount: z.number().int().min(10).default(500),
  maxSolutionCount: z.number().int().min(10).default(300),
  maxDecisionCount: z.number().int().min(10).default(200),
});

// Global AML configuration
export const AMLConfigSchema = z.object({
  version: z.string().default('1.0.0'),
  enabled: z.boolean().default(true),
  storage: StorageConfigSchema,
  learning: LearningConfigSchema,
  pruning: PruningConfigSchema,
  sharing: SharingConfigSchema,
  performance: PerformanceConfigSchema,
  agentOverrides: z.record(AgentConfigSchema.partial()).optional(),
});

// TypeScript types
export type StorageConfig = z.infer<typeof StorageConfigSchema>;
export type LearningConfig = z.infer<typeof LearningConfigSchema>;
export type PruningConfig = z.infer<typeof PruningConfigSchema>;
export type SharingConfig = z.infer<typeof SharingConfigSchema>;
export type PerformanceConfig = z.infer<typeof PerformanceConfigSchema>;
export type AgentConfig = z.infer<typeof AgentConfigSchema>;
export type AMLConfig = z.infer<typeof AMLConfigSchema>;

/**
 * Default configuration
 */
export const DEFAULT_AML_CONFIG: AMLConfig = {
  version: '1.0.0',
  enabled: true,
  storage: {
    backend: 'filesystem',
    path: '.loom/memory',
    encryption: true,
    compression: true,
    maxSizeGb: 1,
    backupEnabled: true,
    backupPath: '.loom/memory-backup',
    backupSchedule: 'daily',
  },
  learning: {
    minConfidence: 0.3,
    promotionThreshold: 3,
    learningRate: 0.1,
    discountFactor: 0.9,
    explorationRate: 0.2,
  },
  pruning: {
    enabled: true,
    schedule: 'daily',
    maxAgeDays: 90,
    minConfidence: 0.2,
    minUsageRate: 0.1,
    aggressiveMode: false,
  },
  sharing: {
    crossAgent: true,
    crossProject: false,
    telemetry: 'anonymous',
    syncEnabled: false,
  },
  performance: {
    cacheEnabled: true,
    cacheMaxSizeMb: 100,
    cacheTtlSeconds: 3600,
    queryTimeoutMs: 50,
    writeTimeoutMs: 100,
    indexingEnabled: true,
  },
};

/**
 * Validate and parse configuration
 */
export function validateConfig(config: unknown): {
  valid: boolean;
  config?: AMLConfig;
  errors?: string[];
} {
  const result = AMLConfigSchema.safeParse(config);
  if (result.success) {
    return { valid: true, config: result.data };
  }
  return {
    valid: false,
    errors: result.error.errors.map((e) => `${e.path.join('.')}: ${e.message}`),
  };
}

/**
 * Merge user config with defaults
 */
export function mergeConfig(userConfig: Partial<AMLConfig>): AMLConfig {
  return AMLConfigSchema.parse({
    ...DEFAULT_AML_CONFIG,
    ...userConfig,
    storage: { ...DEFAULT_AML_CONFIG.storage, ...userConfig.storage },
    learning: { ...DEFAULT_AML_CONFIG.learning, ...userConfig.learning },
    pruning: { ...DEFAULT_AML_CONFIG.pruning, ...userConfig.pruning },
    sharing: { ...DEFAULT_AML_CONFIG.sharing, ...userConfig.sharing },
    performance: { ...DEFAULT_AML_CONFIG.performance, ...userConfig.performance },
  });
}

/**
 * Get effective configuration for an agent (with overrides)
 */
export function getAgentConfig(
  globalConfig: AMLConfig,
  agentName: string
): {
  enabled: boolean;
  memoryLimitMb: number;
  learning: LearningConfig;
  maxPatternCount: number;
  maxSolutionCount: number;
  maxDecisionCount: number;
} {
  const override = globalConfig.agentOverrides?.[agentName];

  return {
    enabled: override?.enabled ?? globalConfig.enabled,
    memoryLimitMb: override?.memoryLimitMb ?? 100,
    learning: {
      ...globalConfig.learning,
      ...override?.learning,
    },
    maxPatternCount: override?.maxPatternCount ?? 500,
    maxSolutionCount: override?.maxSolutionCount ?? 300,
    maxDecisionCount: override?.maxDecisionCount ?? 200,
  };
}
