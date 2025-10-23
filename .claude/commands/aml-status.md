---
description: Display comprehensive AML memory statistics and learning metrics
model: sonnet
argument-hint: [--agent agent-name] [--detailed] [--trends]
---

# /aml-status - Agent Memory & Learning System Status

## What This Command Does

Displays comprehensive memory statistics, learning metrics, and pattern insights for all agents or a specific agent. Provides visual representation of memory usage, success rates, and learning trends to help you understand how your agents are improving over time.

## Process

1. **Read AML Configuration**:
   - Check if AML is enabled globally (`.loom/memory/config.json`)
   - Read global memory metrics
   - Identify which agents have AML enabled

2. **Query Memory Statistics**:
   - Load pattern counts per agent
   - Load solution counts per agent
   - Load decision records per agent
   - Calculate memory usage in MB
   - Compute success rates and confidence scores

3. **Calculate Learning Metrics**:
   - Analyze pattern usage frequency
   - Track success rate trends over time
   - Identify top-performing patterns
   - Measure learning velocity (new patterns per week)
   - Calculate memory efficiency (overhead percentage)

4. **Generate Visual Report**:
   ```
   ========================================
   Agent Memory & Learning System Status
   ========================================

   Overall Statistics:
   ├── Total Patterns: 1,247
   ├── Total Solutions: 892
   ├── Total Decisions: 453
   ├── Success Rate: 94.3%
   ├── Memory Usage: 127 MB / 1 GB (12.7%)
   └── Learning Rate: +12% this week

   Top Performing Agents:
   1. frontend-developer: 98% success, 234 patterns, 45 MB
   2. test-automator: 96% success, 189 patterns, 32 MB
   3. backend-architect: 93% success, 156 patterns, 28 MB

   Recent Learning Highlights:
   • Discovered optimal React render pattern (+40% perf)
   • Resolved recurring TypeScript error family (12 fixes)
   • Identified API rate limiting strategy (97% success)

   Learning Velocity:
   ├── This Week: 47 new patterns (+12%)
   ├── Last Week: 42 new patterns (+10%)
   └── Trend: Accelerating

   Memory Health:
   ├── Cache Hit Rate: 87% (target: 80%+)
   ├── Query Latency: 34ms avg (target: <50ms)
   ├── Pruning Status: Last run 2 days ago
   └── Backup Status: Last backup 1 day ago
   ```

5. **Display Agent-Specific Details** (if --agent specified):
   ```
   ========================================
   Agent: frontend-developer
   ========================================

   Memory Statistics:
   ├── Patterns: 234 (45 MB)
   ├── Solutions: 178 (12 MB)
   ├── Decisions: 89 (8 MB)
   └── Total: 65 MB / 100 MB (65%)

   Success Metrics:
   ├── Overall Success Rate: 98%
   ├── Pattern Confidence: 0.92 avg
   ├── Error Prevention: 47 errors avoided
   └── Time Saved: 8.3 hours this month

   Top Patterns:
   1. React.memo optimization (99% success, 47 uses)
   2. useMemo with deps (97% success, 39 uses)
   3. Custom hooks pattern (95% success, 31 uses)

   Learning Focus Areas:
   ├── React patterns: 89 patterns
   ├── Performance optimization: 67 patterns
   ├── Accessibility: 34 patterns
   ├── State management: 28 patterns
   └── Testing: 16 patterns

   Recent Activity:
   ├── Last pattern learned: 2 hours ago
   ├── Most used pattern today: React.memo optimization (5 times)
   └── Patterns learned this week: 8 new
   ```

6. **Display Trends** (if --trends specified):
   - Show learning curves over time
   - Display success rate evolution
   - Show memory growth patterns
   - Identify seasonal patterns

## Filtering Options

### By Agent
```bash
/aml-status --agent frontend-developer
```
Shows detailed statistics for a specific agent only.

### Detailed View
```bash
/aml-status --detailed
```
Includes full breakdowns of patterns, solutions, and decisions with code snippets.

### Trends Analysis
```bash
/aml-status --trends
```
Shows historical trends with ASCII charts:
```
Pattern Learning Rate (Last 30 Days)

60 │                                    ╭─
50 │                              ╭─────╯
40 │                        ╭─────╯
30 │                  ╭─────╯
20 │            ╭─────╯
10 │      ╭─────╯
 0 ├──────╯
   └────────────────────────────────────
   Oct 1        Oct 15        Oct 30
```

### By Date Range
```bash
/aml-status --since "2025-10-01" --until "2025-10-23"
```
Filter statistics to specific time period.

### By Confidence
```bash
/aml-status --min-confidence 0.8
```
Show only high-confidence patterns (80%+).

## Troubleshooting Indicators

The status report includes health checks:

**Healthy System:**
```
✓ Memory usage: 127 MB / 1 GB (normal)
✓ Cache hit rate: 87% (excellent)
✓ Query latency: 34ms avg (optimal)
✓ Backup status: 1 day ago (current)
✓ Learning rate: +12% (growing)
```

**Issues Detected:**
```
⚠ Memory usage: 897 MB / 1 GB (high - pruning recommended)
⚠ Cache hit rate: 62% (low - rebuild indices)
⚠ Query latency: 127ms avg (slow - check indices)
✓ Backup status: 6 hours ago (current)
⚠ Learning rate: -3% (declining - check patterns)
```

**Critical Issues:**
```
✗ Memory usage: 1.02 GB / 1 GB (OVER LIMIT - prune now)
✗ Cache hit rate: 41% (critical - rebuild immediately)
✗ Query latency: 243ms avg (critical - performance issue)
✗ Backup status: 8 days ago (STALE - backup now)
✗ Learning rate: -18% (concerning - investigate)
```

## Integration with CI/CD

The status command can output JSON for programmatic access:

```bash
/aml-status --format json > aml-metrics.json
```

Example JSON output:
```json
{
  "timestamp": "2025-10-23T10:30:00Z",
  "overall": {
    "total_patterns": 1247,
    "total_solutions": 892,
    "success_rate": 0.943,
    "memory_usage_mb": 127,
    "memory_limit_mb": 1024,
    "learning_rate_change": 0.12
  },
  "agents": [
    {
      "name": "frontend-developer",
      "success_rate": 0.98,
      "patterns": 234,
      "memory_mb": 45,
      "last_used": "2025-10-23T08:15:00Z"
    }
  ],
  "health": {
    "cache_hit_rate": 0.87,
    "query_latency_ms": 34,
    "backup_age_hours": 24,
    "status": "healthy"
  }
}
```

## Recommended Skills

- `data-visualization` - For generating ASCII charts
- `performance-profiling` - For analyzing memory efficiency
- `metrics-analysis` - For computing learning trends

Use these skills to enhance status reporting and identify optimization opportunities.

**Skill Troubleshooting Authority**: If any referenced skill does not work or any script within the skill does not work, Claude Code has the authority to fix them.

## Arguments

- `--agent [name]`: Show statistics for specific agent only
- `--detailed`: Include full pattern/solution breakdowns with code snippets
- `--trends`: Show historical trends with visualizations
- `--since [date]`: Filter to patterns learned after date (ISO 8601 format)
- `--until [date]`: Filter to patterns learned before date (ISO 8601 format)
- `--min-confidence [0.0-1.0]`: Show only patterns above confidence threshold
- `--format [text|json]`: Output format (default: text)
- `--health-check`: Focus on system health indicators only

## Examples

**Basic status:**
```
/aml-status
```
Shows overall system statistics and top agents.

**Agent-specific details:**
```
/aml-status --agent frontend-developer --detailed
```
Shows comprehensive statistics for frontend-developer agent including top patterns with code snippets.

**Learning trends:**
```
/aml-status --trends
```
Shows visual charts of learning velocity and success rates over time.

**Health check:**
```
/aml-status --health-check
```
Quick health status for monitoring and alerts.

**JSON export for CI/CD:**
```
/aml-status --format json --agent backend-architect > metrics.json
```
Exports metrics in JSON format for automated tracking.

**High-confidence patterns only:**
```
/aml-status --min-confidence 0.9 --detailed
```
Shows only patterns with 90%+ confidence scores.

## Notes

- The status command is read-only and never modifies memory
- Query performance is optimized for <50ms response time
- All timestamps are in ISO 8601 format
- Memory usage includes index overhead
- Success rates are calculated from last 100 uses of each pattern
- Learning rate compares current week to previous week
- Cache hit rate measures how often patterns are found vs searched
- Backup status shows time since last automatic backup

## When to Run

Run `/aml-status` regularly to:
- Monitor learning progress
- Identify top-performing patterns
- Detect memory usage issues before they become critical
- Validate that agents are learning effectively
- Track improvement velocity
- Debug learning issues (low success rates, declining trends)
- Generate reports for stakeholders
- Optimize memory allocation per agent
