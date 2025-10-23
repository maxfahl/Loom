# AML Memory Management System

**Phase 5: Memory Management & Pruning**

Comprehensive Python-based memory management system for the Agent Memory & Learning (AML) framework.

## Overview

This system provides intelligent memory management capabilities:

- **Pruning**: Time-based, performance-based, and space-based pruning strategies
- **Optimization**: Compression, lazy loading, searchable indices, bloom filters, cache warming
- **Backup & Restore**: Automated backups with incremental support and point-in-time recovery
- **Migration**: Schema migration with backward compatibility
- **Monitoring**: Real-time monitoring, health checks, and alerting

## Components

### 1. Pruning System (`pruning.py`)

Removes low-value patterns while preserving critical learning data.

**Strategies:**
- **Time-based**: Remove patterns unused for >90 days, decisions >6 months, failed patterns >30 days
- **Performance-based**: Remove patterns with <20% success rate, outdated solutions, negative outcomes
- **Space-based**: Trigger when agent >80MB or global >800MB, remove lowest confidence patterns

**Usage:**
```bash
python pruning.py <memory_path> time_based performance_based
```

### 2. Optimization System (`optimization.py`)

Optimizes memory usage and query performance.

**Features:**
- **Bloom Filter**: O(1) existence checks with <1% false positive rate
- **LRU Cache**: 10MB cache with automatic eviction
- **Memory Index**: Fast pattern/solution/decision lookups
- **Compression**: gzip compression (typically 70-80% reduction)
- **Lazy Loading**: Load patterns on-demand, not upfront
- **Garbage Collection**: Remove invalid/duplicate entries

**Usage:**
```bash
# Build searchable index
python optimization.py <memory_path> build-index

# Compress old files
python optimization.py <memory_path> compress

# Warm cache with high-value patterns
python optimization.py <memory_path> warm-cache

# Run garbage collection
python optimization.py <memory_path> gc
```

### 3. Backup System (`backup.py`)

Automated backup with incremental support.

**Features:**
- **Full Backups**: Complete memory snapshot
- **Incremental Backups**: Only changed files since last backup
- **Point-in-Time Recovery**: Restore to specific datetime
- **Verification**: SHA-256 checksums for integrity
- **Rotation**: Automatic cleanup of old backups (30 days retention)

**Usage:**
```bash
# Create full backup
python backup.py <memory_path> full

# Create incremental backup
python backup.py <memory_path> incremental

# Restore backup
python backup.py <memory_path> restore <backup_id>

# List backups
python backup.py <memory_path> list

# Verify backup integrity
python backup.py <memory_path> verify <backup_id>

# Automated backup job (for cron)
python backup.py <memory_path> auto
```

### 4. Migration System (`migration.py`)

Schema migration with version detection.

**Supported Versions:**
- v1.0.0 → v1.1.0: Add tags and active fields
- v1.1.0 → v1.2.0: Add metadata and variations
- v1.2.0 → v2.0.0: Restructure metrics and lifecycle (breaking)

**Usage:**
```bash
# Detect current version
python migration.py <memory_path> detect

# Migrate to latest
python migration.py <memory_path> migrate-latest

# Migrate to specific version
python migration.py <memory_path> migrate 1.2.0
```

### 5. Monitoring System (`monitoring.py`)

Real-time monitoring and health checks.

**Features:**
- **Memory Metrics**: Size, counts, largest agent tracking
- **Performance Metrics**: Query time, cache hit rate, operation times
- **Health Checks**: 6 comprehensive checks (structure, limits, index, backup, integrity, performance)
- **Alerting**: INFO, WARNING, ERROR, CRITICAL alerts with resolution tracking
- **Reports**: JSON reports for integration

**Usage:**
```bash
# Collect memory metrics
python monitoring.py <memory_path> metrics

# Run health check
python monitoring.py <memory_path> health

# Show active alerts
python monitoring.py <memory_path> alerts

# Generate report
python monitoring.py <memory_path> report
```

## Unified CLI (`aml-cli.py`)

Single entry point for all operations.

### Installation

```bash
# Make executable
chmod +x aml-cli.py

# Optionally create symlink
ln -s $(pwd)/aml-cli.py /usr/local/bin/aml
```

### Usage

```bash
# Prune memory
aml <memory_path> prune --strategies time_based performance_based
aml <memory_path> prune --aggressive --dry-run

# Optimize memory
aml <memory_path> optimize all
aml <memory_path> optimize index
aml <memory_path> optimize compress --age-days 30

# Backup operations
aml <memory_path> backup create
aml <memory_path> backup create --incremental
aml <memory_path> backup restore --backup-id full_20250123_100000
aml <memory_path> backup list

# Schema migration
aml <memory_path> migrate detect
aml <memory_path> migrate migrate --version 1.2.0

# Monitoring
aml <memory_path> monitor health
aml <memory_path> monitor metrics
aml <memory_path> monitor alerts
```

## Testing

Comprehensive unit tests for all components.

```bash
# Run all tests
python test_memory_management.py

# Run specific test suite
python -m unittest test_memory_management.TestMemoryPruner
python -m unittest test_memory_management.TestBackupManager
```

**Test Coverage:**
- Memory pruning (time, performance, space-based)
- Bloom filter operations
- LRU cache eviction
- Index building and searching
- Full and incremental backups
- Backup restoration
- Schema migration
- Health checks and alerting
- Garbage collection

## Architecture

```
scripts/aml/
├── pruning.py              # Pruning strategies
├── optimization.py         # Optimization utilities
├── backup.py              # Backup & restore
├── migration.py           # Schema migration
├── monitoring.py          # Monitoring & alerts
├── aml-cli.py            # Unified CLI
├── test_memory_management.py  # Unit tests
└── README.md             # This file
```

## Configuration

### Pruning Configuration

```python
from pruning import PruneConfig

config = PruneConfig(
    # Time thresholds
    pattern_max_age_days=90,
    decision_max_age_days=180,
    failed_pattern_max_age_days=30,

    # Performance thresholds
    min_success_rate=0.20,
    min_confidence_score=0.15,
    min_execution_count=3,

    # Space thresholds
    agent_memory_limit=80 * 1024 * 1024,  # 80MB
    global_memory_limit=800 * 1024 * 1024,  # 800MB

    # Safety
    preserve_high_value=True,
    high_value_threshold=0.85,
    dry_run=False,
    create_backup=True
)
```

### Backup Configuration

```python
from backup import BackupConfig

config = BackupConfig(
    backup_root=Path('.loom/memory-backup'),
    retention_days=30,
    max_backups=100,
    compression_level=9,
    incremental_enabled=True,
    verify_after_backup=True,
    backup_schedule='daily'
)
```

### Monitoring Configuration

```python
config = {
    'agent_memory_warning_mb': 60,
    'agent_memory_critical_mb': 80,
    'global_memory_warning_mb': 600,
    'global_memory_critical_mb': 800,
    'cache_hit_rate_warning': 0.5,
    'query_time_warning_ms': 100,
    'alert_retention_days': 7
}
```

## Performance Characteristics

### Pruning
- **Time-based**: O(n) where n = number of patterns
- **Performance-based**: O(n)
- **Space-based**: O(n log n) due to sorting

### Optimization
- **Bloom Filter**: O(1) lookups, ~10KB per 10,000 items
- **Index Building**: O(n) initial build, O(1) lookups
- **Compression**: 70-80% size reduction, ~100ms per MB
- **Cache**: O(1) access, 80%+ hit rate after warmup

### Backup
- **Full Backup**: ~500ms per 10MB
- **Incremental Backup**: ~100ms per 10MB (only changed files)
- **Restore**: ~400ms per 10MB
- **Verification**: ~200ms per 10MB

### Migration
- **v1.0 → v1.1**: ~50ms per 1000 items
- **v1.1 → v1.2**: ~75ms per 1000 items
- **v1.2 → v2.0**: ~150ms per 1000 items (restructuring)

## Integration with TypeScript

These Python scripts complement the TypeScript AML implementation:

- **Python**: Maintenance, batch operations, CLI tools, scheduled jobs
- **TypeScript**: Runtime operations, agent integration, real-time queries

Both systems read/write the same JSON format in `.loom/memory/`.

## Automated Tasks

### Cron Jobs

```bash
# Daily backup at 2 AM
0 2 * * * cd /path/to/loom && python scripts/aml/backup.py .loom/memory auto

# Weekly pruning (Sunday 3 AM)
0 3 * * 0 cd /path/to/loom && python scripts/aml/aml-cli.py .loom/memory prune

# Daily health check at 6 AM
0 6 * * * cd /path/to/loom && python scripts/aml/monitoring.py .loom/memory health

# Monthly index rebuild (1st of month, 4 AM)
0 4 1 * * cd /path/to/loom && python scripts/aml/optimization.py .loom/memory build-index
```

## Error Recovery

### Corrupted Memory

```bash
# Run garbage collection
aml .loom/memory optimize gc

# Rebuild index
aml .loom/memory optimize index

# If still broken, restore from backup
aml .loom/memory backup list
aml .loom/memory backup restore --backup-id <latest_backup>
```

### Memory Limit Exceeded

```bash
# Aggressive pruning
aml .loom/memory prune --strategies time_based performance_based space_based --aggressive

# Compress files
aml .loom/memory optimize compress

# Check results
aml .loom/memory monitor metrics
```

### Performance Degradation

```bash
# Rebuild index
aml .loom/memory optimize index

# Warm cache
aml .loom/memory optimize warm-cache

# Run garbage collection
aml .loom/memory optimize gc

# Check performance
aml .loom/memory monitor health
```

## Best Practices

1. **Run backups before major operations** (pruning, migration)
2. **Use dry-run first** to preview changes
3. **Monitor health regularly** (daily health checks)
4. **Prune periodically** (weekly or when memory >70% limit)
5. **Keep backups for 30+ days** for disaster recovery
6. **Test restores occasionally** to verify backup integrity
7. **Rotate backups automatically** to manage storage
8. **Set up alerts** for critical conditions

## Troubleshooting

### Import Errors

Ensure all modules are in the same directory or on Python path:

```bash
export PYTHONPATH="$(pwd)/scripts/aml:$PYTHONPATH"
```

### Permission Errors

Ensure write access to memory directory:

```bash
chmod -R u+w .loom/memory
```

### Memory Still Large After Pruning

Try:
1. Aggressive pruning mode
2. Compression of old files
3. Garbage collection
4. Check for large individual patterns

### Slow Queries

Try:
1. Rebuild index
2. Warm cache
3. Compress old files
4. Run garbage collection

## Future Enhancements

- [ ] Parallel processing for large memory stores
- [ ] Distributed backup to cloud storage
- [ ] Machine learning-based pruning decisions
- [ ] Real-time alerting via webhooks/email
- [ ] Web dashboard for monitoring
- [ ] Pattern deduplication algorithms
- [ ] Automatic schema migration on startup
- [ ] Compressed index format
- [ ] Query result caching
- [ ] Memory defragmentation

## License

Part of the Loom Framework - see main repository for license details.

## Support

For issues or questions, consult the main AML implementation plan:
`/Users/maxfahl/Fahl/Common/Loom/tmp/AML_IMPLEMENTATION_PLAN.md`
