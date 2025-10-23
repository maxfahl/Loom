/**
 * Common types used across the AML system
 */

export type AgentName = string;
export type PatternId = string;
export type SolutionId = string;
export type DecisionId = string;
export type Timestamp = string; // ISO 8601 format

export interface Context {
  [key: string]: string | number | boolean | Context | Context[];
}

export interface TimeRange {
  start: Timestamp;
  end: Timestamp;
}

export interface QueryOptions {
  limit?: number;
  offset?: number;
  sortBy?: string;
  sortOrder?: 'asc' | 'desc';
  includeInactive?: boolean;
}

export interface ValidationResult {
  valid: boolean;
  errors?: string[];
}

export interface OperationResult<T = void> {
  success: boolean;
  data?: T;
  error?: string;
}
