# AML Memory Management - Quick Reference

## 🚀 Common Commands

### Daily Operations

```bash
# Check memory health
aml .loom/memory monitor health

# View memory metrics
aml .loom/memory monitor metrics

# Check active alerts
aml .loom/memory monitor alerts
```

### Weekly Maintenance

```bash
# Prune old/unused patterns
aml .loom/memory prune --strategies time_based performance_based

# Optimize memory
aml .loom/memory optimize all

# Create backup
aml .loom/memory backup create
```

### Troubleshooting

```bash
# Memory too large?
aml .loom/memory prune --aggressive
aml .loom/memory optimize compress

# Slow queries?
aml .loom/memory optimize index
aml .loom/memory optimize warm-cache

# Corrupted data?
aml .loom/memory optimize gc
aml .loom/memory backup restore --backup-id <latest>

# Need to migrate?
aml .loom/memory migrate detect
aml .loom/memory migrate migrate
```

## 📊 Key Thresholds

| Metric | Warning | Critical |
|--------|---------|----------|
| Agent memory | 60MB | 80MB |
| Global memory | 600MB | 800MB |
| Pattern age | 60 days | 90 days |
| Success rate | 30% | 20% |
| Query time | 50ms | 100ms |
| Cache hit rate | 60% | 50% |

## 🔧 Configuration Snippets

### Aggressive Pruning
```python
PruneConfig(
    pattern_max_age_days=60,
    min_success_rate=0.30,
    preserve_high_value=True
)
```

### Fast Backups
```python
BackupConfig(
    compression_level=6,  # Lower = faster
    incremental_enabled=True,
    verify_after_backup=False
)
```

### Performance Monitoring
```python
config = {
    'query_time_warning_ms': 50,
    'cache_hit_rate_warning': 0.70
}
```

## 📅 Cron Schedule

```bash
# /etc/cron.d/aml-maintenance

# Daily backup at 2 AM
0 2 * * * cd /project && aml .loom/memory backup auto

# Weekly prune (Sunday 3 AM)
0 3 * * 0 cd /project && aml .loom/memory prune

# Daily health check at 6 AM
0 6 * * * cd /project && aml .loom/memory monitor health

# Monthly optimize (1st at 4 AM)
0 4 1 * * cd /project && aml .loom/memory optimize all
```

## 🚨 Emergency Procedures

### Disk Full
```bash
# Immediate space recovery
aml .loom/memory prune --strategies space_based
aml .loom/memory optimize compress --age-days 0
aml .loom/memory optimize gc
```

### Data Corruption
```bash
# Clean and rebuild
aml .loom/memory optimize gc
aml .loom/memory optimize index
# If still broken:
aml .loom/memory backup list
aml .loom/memory backup restore --backup-id <latest>
```

### Performance Degraded
```bash
# Quick fixes
aml .loom/memory optimize index      # Rebuild index
aml .loom/memory optimize warm-cache # Warm cache
aml .loom/memory optimize gc         # Clean garbage
```

### Rollback After Bad Prune
```bash
# Restore from automatic pre-prune backup
aml .loom/memory backup list | grep "Pre-prune"
aml .loom/memory backup restore --backup-id <backup_id>
```

## 💡 Best Practices

✅ **DO**:
- Always use `--dry-run` first
- Monitor health daily
- Backup before major operations
- Prune regularly (weekly)
- Keep backups for 30+ days
- Test restores occasionally

❌ **DON'T**:
- Prune without backup
- Delete backups manually
- Skip health checks
- Ignore alerts
- Run multiple operations simultaneously
- Modify memory files directly

## 📈 Performance Tips

1. **Slow queries?**
   - Rebuild index weekly
   - Warm cache on startup
   - Use filters to narrow search

2. **Large memory?**
   - Enable compression
   - Prune regularly
   - Archive old decisions

3. **Backup too slow?**
   - Use incremental backups
   - Lower compression level
   - Backup during off-hours

4. **Cache misses?**
   - Increase cache size
   - Warm cache with more patterns
   - Check access patterns

## 🔍 Monitoring Cheatsheet

```bash
# Quick health check
aml .loom/memory monitor health

# Detailed metrics
aml .loom/memory monitor metrics

# Performance metrics
aml .loom/memory monitor report | jq '.performance'

# Memory breakdown
aml .loom/memory monitor report | jq '.memory'

# Active alerts
aml .loom/memory monitor alerts

# Historical metrics (requires manual query)
cat .loom/memory/monitoring/metrics.json | jq '.history[-10:]'
```

## 📦 File Locations

```
.loom/
├── memory/                 # Memory data
│   ├── agent-name/        # Per-agent memory
│   ├── global/            # Cross-agent data
│   ├── config/            # Configuration
│   └── monitoring/        # Monitoring data
├── memory-backup/         # Backups
│   ├── full_*/           # Full backups
│   ├── incr_*/           # Incremental backups
│   ├── archives/         # Archived data
│   └── backup_metadata.json
└── scripts/aml/          # Management scripts
    ├── aml-cli.py        # Main CLI
    ├── pruning.py
    ├── optimization.py
    ├── backup.py
    ├── migration.py
    └── monitoring.py
```

## 🐛 Common Errors

### `ImportError: No module named 'pruning'`
```bash
export PYTHONPATH="$(pwd)/scripts/aml:$PYTHONPATH"
```

### `PermissionError: [Errno 13]`
```bash
chmod -R u+w .loom/memory
```

### `JSONDecodeError`
```bash
# File corrupted, restore from backup
aml .loom/memory backup restore --backup-id <latest>
```

### `Backup not found`
```bash
# Check backup list
aml .loom/memory backup list
# Use correct backup ID format: full_YYYYMMDD_HHMMSS
```

## 📞 Support

For issues or questions:
1. Check `scripts/aml/README.md` for detailed docs
2. Review `scripts/aml/IMPLEMENTATION_SUMMARY.md` for architecture
3. Consult main AML plan: `tmp/AML_IMPLEMENTATION_PLAN.md`
4. Run tests: `python scripts/aml/test_memory_management.py`

## 🎯 Decision Matrix

| Scenario | Action |
|----------|--------|
| Memory >70% limit | Prune (time + performance) |
| Memory >85% limit | Prune (all strategies, aggressive) |
| Queries >50ms | Rebuild index, warm cache |
| Cache hit <60% | Warm cache with more patterns |
| Many alerts | Run health check, address issues |
| Before migration | Create full backup |
| Before pruning | Automatic backup (built-in) |
| Weekly maintenance | Prune + optimize + backup |
| Monthly deep clean | Full optimize, rotate backups |

---

**Version**: 1.0.0
**Last Updated**: 2025-10-23
**Maintained by**: Loom Framework Team
