"""
AML Memory Management System

Provides memory management capabilities for the Agent Memory & Learning framework:
- Pruning strategies (time, performance, space-based)
- Optimization (compression, indexing, caching)
- Backup and restore with incremental support
- Schema migration with version detection
- Monitoring, health checks, and alerting

Author: Loom Framework
Version: 1.0.0
"""

from .pruning import (
    MemoryPruner,
    PruneStrategy,
    PruneConfig,
    PruneReason,
    PruneResult,
    prune_memory
)

from .optimization import (
    BloomFilter,
    LRUCache,
    MemoryIndex,
    LazyMemoryLoader,
    MemoryCompressor,
    GarbageCollector,
    IndexEntry,
    CacheStats
)

from .backup import (
    BackupManager,
    BackupType,
    BackupConfig,
    BackupMetadata,
    RestoreResult,
    automated_backup_job
)

from .migration import (
    MigrationManager,
    SchemaVersion,
    MigrationStep,
    MigrationResult
)

from .monitoring import (
    MemoryMonitor,
    HealthStatus,
    AlertLevel,
    MemoryMetrics,
    PerformanceMetrics,
    Alert,
    HealthCheck
)

__version__ = "1.0.0"
__author__ = "Loom Framework"

__all__ = [
    # Pruning
    "MemoryPruner",
    "PruneStrategy",
    "PruneConfig",
    "PruneReason",
    "PruneResult",
    "prune_memory",

    # Optimization
    "BloomFilter",
    "LRUCache",
    "MemoryIndex",
    "LazyMemoryLoader",
    "MemoryCompressor",
    "GarbageCollector",
    "IndexEntry",
    "CacheStats",

    # Backup
    "BackupManager",
    "BackupType",
    "BackupConfig",
    "BackupMetadata",
    "RestoreResult",
    "automated_backup_job",

    # Migration
    "MigrationManager",
    "SchemaVersion",
    "MigrationStep",
    "MigrationResult",

    # Monitoring
    "MemoryMonitor",
    "HealthStatus",
    "AlertLevel",
    "MemoryMetrics",
    "PerformanceMetrics",
    "Alert",
    "HealthCheck",
]
