/**
 * Metrics Collector - Performance and usage tracking
 *
 * Collects and aggregates metrics for monitoring AML system health and performance.
 * Tracks query latency, cache hit rates, learning progress, and storage usage.
 */

import { AgentName, Timestamp } from './types/common';
import { Metrics, MetricsModel, PerformanceMetrics, LearningMetrics, UsageMetrics, StorageMetrics } from './models/Metrics';

export interface MetricEvent {
  agent: AgentName;
  timestamp: Timestamp;
  type: 'query' | 'write' | 'pattern_use' | 'solution_use' | 'decision_ref';
  latencyMs?: number;
  success?: boolean;
  metadata?: Record<string, unknown>;
}

export interface AggregatedMetrics {
  period: 'hourly' | 'daily' | 'weekly' | 'monthly';
  startTime: Timestamp;
  endTime: Timestamp;
  agents: Map<AgentName, Metrics>;
}

/**
 * Metrics Collector class
 */
export class MetricsCollector {
  private eventBuffer: MetricEvent[];
  private bufferSize: number;
  private flushInterval: number;
  private flushTimer: NodeJS.Timeout | null;
  private aggregates: Map<string, AggregatedMetrics>;

  // Running counters per agent
  private queryLatencies: Map<AgentName, number[]>;
  private writeLatencies: Map<AgentName, number[]>;
  private cacheHits: Map<AgentName, number>;
  private cacheMisses: Map<AgentName, number>;

  constructor(bufferSize: number = 100, flushIntervalMs: number = 60000) {
    this.eventBuffer = [];
    this.bufferSize = bufferSize;
    this.flushInterval = flushIntervalMs;
    this.flushTimer = null;
    this.aggregates = new Map();

    this.queryLatencies = new Map();
    this.writeLatencies = new Map();
    this.cacheHits = new Map();
    this.cacheMisses = new Map();
  }

  /**
   * Start collecting metrics
   */
  start(): void {
    if (this.flushTimer) return;

    this.flushTimer = setInterval(() => {
      this.flush();
    }, this.flushInterval);
  }

  /**
   * Stop collecting metrics
   */
  stop(): void {
    if (this.flushTimer) {
      clearInterval(this.flushTimer);
      this.flushTimer = null;
    }
    this.flush(); // Final flush
  }

  /**
   * Record a metric event
   */
  recordEvent(event: MetricEvent): void {
    this.eventBuffer.push(event);

    // Update running counters
    switch (event.type) {
      case 'query':
        if (event.latencyMs !== undefined) {
          if (!this.queryLatencies.has(event.agent)) {
            this.queryLatencies.set(event.agent, []);
          }
          this.queryLatencies.get(event.agent)!.push(event.latencyMs);
        }
        break;

      case 'write':
        if (event.latencyMs !== undefined) {
          if (!this.writeLatencies.has(event.agent)) {
            this.writeLatencies.set(event.agent, []);
          }
          this.writeLatencies.get(event.agent)!.push(event.latencyMs);
        }
        break;
    }

    // Auto-flush if buffer is full
    if (this.eventBuffer.length >= this.bufferSize) {
      this.flush();
    }
  }

  /**
   * Record query metric
   */
  recordQuery(agent: AgentName, latencyMs: number, cacheHit: boolean = false): void {
    this.recordEvent({
      agent,
      timestamp: new Date().toISOString(),
      type: 'query',
      latencyMs,
      metadata: { cacheHit },
    });

    // Update cache stats
    if (cacheHit) {
      this.cacheHits.set(agent, (this.cacheHits.get(agent) || 0) + 1);
    } else {
      this.cacheMisses.set(agent, (this.cacheMisses.get(agent) || 0) + 1);
    }
  }

  /**
   * Record write metric
   */
  recordWrite(agent: AgentName, latencyMs: number): void {
    this.recordEvent({
      agent,
      timestamp: new Date().toISOString(),
      type: 'write',
      latencyMs,
    });
  }

  /**
   * Record pattern usage
   */
  recordPatternUsage(agent: AgentName, success: boolean, timeSavedMs?: number): void {
    this.recordEvent({
      agent,
      timestamp: new Date().toISOString(),
      type: 'pattern_use',
      success,
      metadata: { timeSavedMs },
    });
  }

  /**
   * Record solution usage
   */
  recordSolutionUsage(agent: AgentName, success: boolean): void {
    this.recordEvent({
      agent,
      timestamp: new Date().toISOString(),
      type: 'solution_use',
      success,
    });
  }

  /**
   * Record decision reference
   */
  recordDecisionReference(agent: AgentName): void {
    this.recordEvent({
      agent,
      timestamp: new Date().toISOString(),
      type: 'decision_ref',
    });
  }

  /**
   * Get current performance metrics for an agent
   */
  getPerformanceMetrics(agent: AgentName): PerformanceMetrics {
    const queryLats = this.queryLatencies.get(agent) || [];
    const writeLats = this.writeLatencies.get(agent) || [];
    const hits = this.cacheHits.get(agent) || 0;
    const misses = this.cacheMisses.get(agent) || 0;

    const avgQueryLatencyMs =
      queryLats.length > 0 ? queryLats.reduce((a, b) => a + b, 0) / queryLats.length : 0;
    const avgWriteLatencyMs =
      writeLats.length > 0 ? writeLats.reduce((a, b) => a + b, 0) / writeLats.length : 0;
    const cacheHitRate = hits + misses > 0 ? hits / (hits + misses) : 0;

    return {
      avgQueryLatencyMs,
      avgWriteLatencyMs,
      cacheHitRate,
      totalQueries: queryLats.length,
      totalWrites: writeLats.length,
    };
  }

  /**
   * Get aggregated metrics for a period
   */
  getAggregatedMetrics(
    period: 'hourly' | 'daily' | 'weekly' | 'monthly',
    startTime?: Timestamp
  ): AggregatedMetrics | null {
    const key = this.getAggregateKey(period, startTime);
    return this.aggregates.get(key) || null;
  }

  /**
   * Calculate SLA compliance (query < 50ms, write < 100ms)
   */
  calculateSLACompliance(agent: AgentName): {
    queryCompliance: number;
    writeCompliance: number;
    overallCompliance: number;
  } {
    const queryLats = this.queryLatencies.get(agent) || [];
    const writeLats = this.writeLatencies.get(agent) || [];

    const queryCompliant = queryLats.filter((lat) => lat < 50).length;
    const writeCompliant = writeLats.filter((lat) => lat < 100).length;

    const queryCompliance = queryLats.length > 0 ? queryCompliant / queryLats.length : 1.0;
    const writeCompliance = writeLats.length > 0 ? writeCompliant / writeLats.length : 1.0;
    const overallCompliance = (queryCompliance + writeCompliance) / 2;

    return {
      queryCompliance,
      writeCompliance,
      overallCompliance,
    };
  }

  /**
   * Get percentile latency
   */
  getPercentileLatency(
    agent: AgentName,
    type: 'query' | 'write',
    percentile: number
  ): number {
    const latencies =
      type === 'query'
        ? this.queryLatencies.get(agent) || []
        : this.writeLatencies.get(agent) || [];

    if (latencies.length === 0) return 0;

    const sorted = [...latencies].sort((a, b) => a - b);
    const index = Math.ceil((percentile / 100) * sorted.length) - 1;
    return sorted[Math.max(0, index)];
  }

  /**
   * Get event count for agent
   */
  getEventCount(
    agent: AgentName,
    type?: 'query' | 'write' | 'pattern_use' | 'solution_use' | 'decision_ref'
  ): number {
    let events = this.eventBuffer.filter((e) => e.agent === agent);
    if (type) {
      events = events.filter((e) => e.type === type);
    }
    return events.length;
  }

  /**
   * Clear metrics for agent
   */
  clearAgentMetrics(agent: AgentName): void {
    this.queryLatencies.delete(agent);
    this.writeLatencies.delete(agent);
    this.cacheHits.delete(agent);
    this.cacheMisses.delete(agent);
    this.eventBuffer = this.eventBuffer.filter((e) => e.agent !== agent);
  }

  /**
   * Clear all metrics
   */
  clearAll(): void {
    this.eventBuffer = [];
    this.queryLatencies.clear();
    this.writeLatencies.clear();
    this.cacheHits.clear();
    this.cacheMisses.clear();
    this.aggregates.clear();
  }

  /**
   * Get summary report
   */
  getSummary(): {
    totalEvents: number;
    totalAgents: number;
    avgQueryLatency: number;
    avgWriteLatency: number;
    overallCacheHitRate: number;
    slaCompliance: number;
  } {
    const agents = new Set(this.eventBuffer.map((e) => e.agent));
    const allQueryLats = Array.from(this.queryLatencies.values()).flat();
    const allWriteLats = Array.from(this.writeLatencies.values()).flat();

    const avgQueryLatency =
      allQueryLats.length > 0 ? allQueryLats.reduce((a, b) => a + b, 0) / allQueryLats.length : 0;
    const avgWriteLatency =
      allWriteLats.length > 0 ? allWriteLats.reduce((a, b) => a + b, 0) / allWriteLats.length : 0;

    const totalHits = Array.from(this.cacheHits.values()).reduce((a, b) => a + b, 0);
    const totalMisses = Array.from(this.cacheMisses.values()).reduce((a, b) => a + b, 0);
    const overallCacheHitRate = totalHits + totalMisses > 0 ? totalHits / (totalHits + totalMisses) : 0;

    const queryCompliant = allQueryLats.filter((lat) => lat < 50).length;
    const writeCompliant = allWriteLats.filter((lat) => lat < 100).length;
    const totalChecks = allQueryLats.length + allWriteLats.length;
    const slaCompliance =
      totalChecks > 0 ? (queryCompliant + writeCompliant) / totalChecks : 1.0;

    return {
      totalEvents: this.eventBuffer.length,
      totalAgents: agents.size,
      avgQueryLatency,
      avgWriteLatency,
      overallCacheHitRate,
      slaCompliance,
    };
  }

  // ============================================================================
  // PRIVATE METHODS
  // ============================================================================

  /**
   * Flush buffered events and create aggregates
   */
  private flush(): void {
    if (this.eventBuffer.length === 0) return;

    // Group events by agent
    const eventsByAgent = new Map<AgentName, MetricEvent[]>();
    for (const event of this.eventBuffer) {
      if (!eventsByAgent.has(event.agent)) {
        eventsByAgent.set(event.agent, []);
      }
      eventsByAgent.get(event.agent)!.push(event);
    }

    // Create aggregates for each period
    const now = new Date();
    const periods: Array<'hourly' | 'daily' | 'weekly' | 'monthly'> = [
      'hourly',
      'daily',
      'weekly',
      'monthly',
    ];

    for (const period of periods) {
      const key = this.getAggregateKey(period);
      const aggregate = this.aggregates.get(key) || this.createEmptyAggregate(period);

      for (const [agent, events] of eventsByAgent.entries()) {
        // Update aggregate with events
        // This is simplified - full implementation would update all metric fields
        const perfMetrics = this.getPerformanceMetrics(agent);
        // Store would happen here
      }

      this.aggregates.set(key, aggregate);
    }

    // Clear buffer
    this.eventBuffer = [];
  }

  /**
   * Get aggregate key for period
   */
  private getAggregateKey(
    period: 'hourly' | 'daily' | 'weekly' | 'monthly',
    timestamp?: Timestamp
  ): string {
    const date = timestamp ? new Date(timestamp) : new Date();

    switch (period) {
      case 'hourly':
        return `${date.getFullYear()}-${date.getMonth()}-${date.getDate()}-${date.getHours()}`;
      case 'daily':
        return `${date.getFullYear()}-${date.getMonth()}-${date.getDate()}`;
      case 'weekly':
        const weekNum = Math.floor(date.getDate() / 7);
        return `${date.getFullYear()}-${date.getMonth()}-W${weekNum}`;
      case 'monthly':
        return `${date.getFullYear()}-${date.getMonth()}`;
    }
  }

  /**
   * Create empty aggregate
   */
  private createEmptyAggregate(period: 'hourly' | 'daily' | 'weekly' | 'monthly'): AggregatedMetrics {
    return {
      period,
      startTime: new Date().toISOString(),
      endTime: new Date().toISOString(),
      agents: new Map(),
    };
  }
}
