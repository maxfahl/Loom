#!/usr/bin/env python3
"""
AML Command-Line Interface

Unified CLI for all AML memory management operations.

Usage:
    aml-cli.py <memory_path> <command> [options]

Commands:
    prune       - Prune memory based on various strategies
    optimize    - Optimize memory (compress, index, cache)
    backup      - Backup operations (create, restore, list)
    migrate     - Schema migration operations
    monitor     - Monitoring and health checks
    gc          - Run garbage collection

Author: Loom Framework
Version: 1.0.0
"""

import sys
import argparse
import logging
from pathlib import Path
from datetime import datetime

# Import AML modules
from pruning import (
    MemoryPruner, PruneStrategy, PruneConfig, prune_memory
)
from optimization import (
    MemoryIndex, LazyMemoryLoader, MemoryCompressor, GarbageCollector
)
from backup import (
    BackupManager, BackupConfig, automated_backup_job
)
from migration import (
    MigrationManager
)
from monitoring import (
    MemoryMonitor, HealthStatus
)


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('aml-cli')


def cmd_prune(args):
    """Execute pruning command"""
    print(f"🗑️  Pruning memory at {args.memory_path}")
    print(f"   Strategies: {', '.join(args.strategies)}")
    print(f"   Dry run: {args.dry_run}")
    print()

    config = PruneConfig(dry_run=args.dry_run)

    if args.aggressive:
        config.pattern_max_age_days = 60
        config.decision_max_age_days = 120
        config.min_success_rate = 0.30

    results = prune_memory(
        args.memory_path,
        args.strategies,
        agents=args.agents,
        config=config.__dict__,
        dry_run=args.dry_run
    )

    # Display results
    total_pruned = sum(r.items_pruned for r in results)
    total_archived = sum(r.items_archived for r in results)
    total_freed = sum(r.space_freed_bytes for r in results)

    print("✅ Pruning complete!")
    print(f"   Items pruned: {total_pruned}")
    print(f"   Items archived: {total_archived}")
    print(f"   Space freed: {total_freed / 1024 / 1024:.2f}MB")

    for result in results:
        if result.summary:
            print(f"\n   {result.strategy.value}:")
            for reason, count in result.summary.items():
                print(f"     - {reason.value}: {count}")


def cmd_optimize(args):
    """Execute optimization command"""
    memory_path = Path(args.memory_path)

    if args.operation == 'index':
        print("🔍 Building memory index...")
        index = MemoryIndex(memory_path)
        count = index.build_index(force=True)
        print(f"✅ Indexed {count} items")

    elif args.operation == 'compress':
        print("🗜️  Compressing old files...")
        count = MemoryCompressor.compress_directory(memory_path, age_days=args.age_days or 30)
        print(f"✅ Compressed {count} files")

    elif args.operation == 'warm-cache':
        print("🔥 Warming cache...")
        loader = LazyMemoryLoader(memory_path)
        loader.index.build_index()
        count = loader.warm_cache(agents=args.agents)
        stats = loader.get_cache_stats()
        print(f"✅ Warmed cache with {count} items")
        print(f"   Cache size: {stats.size_bytes / 1024 / 1024:.2f}MB")
        print(f"   Hit rate: {stats.hit_rate:.1%}")

    elif args.operation == 'gc':
        print("🧹 Running garbage collection...")
        gc = GarbageCollector(memory_path)
        stats = gc.collect(dry_run=args.dry_run)
        print(f"✅ Garbage collection complete:")
        print(f"   Invalid items: {stats['invalid_items']}")
        print(f"   Duplicates: {stats['duplicates']}")
        print(f"   Empty files: {stats['empty_files']}")

    elif args.operation == 'all':
        print("⚡ Running full optimization...")

        # Build index
        index = MemoryIndex(memory_path)
        index_count = index.build_index(force=True)
        print(f"   ✓ Indexed {index_count} items")

        # Compress files
        compress_count = MemoryCompressor.compress_directory(memory_path, age_days=30)
        print(f"   ✓ Compressed {compress_count} files")

        # Warm cache
        loader = LazyMemoryLoader(memory_path)
        cache_count = loader.warm_cache()
        print(f"   ✓ Warmed cache with {cache_count} items")

        # Garbage collection
        gc = GarbageCollector(memory_path)
        gc_stats = gc.collect(dry_run=False)
        print(f"   ✓ Cleaned {gc_stats['invalid_items']} invalid items")

        print("\n✅ Full optimization complete!")


def cmd_backup(args):
    """Execute backup command"""
    memory_path = Path(args.memory_path)
    manager = BackupManager(memory_path)

    if args.operation == 'create':
        if args.incremental:
            print("💾 Creating incremental backup...")
            metadata = manager.create_incremental_backup()
        else:
            print("💾 Creating full backup...")
            metadata = manager.create_full_backup(agents=args.agents)

        print(f"✅ Backup created: {metadata.backup_id}")
        print(f"   Type: {metadata.backup_type.value}")
        print(f"   Files: {metadata.file_count}")
        print(f"   Size: {metadata.total_size_bytes / 1024 / 1024:.2f}MB")
        print(f"   Path: {metadata.backup_path}")

    elif args.operation == 'restore':
        if not args.backup_id:
            print("❌ Error: backup_id required for restore")
            sys.exit(1)

        print(f"♻️  Restoring backup: {args.backup_id}")
        result = manager.restore_backup(args.backup_id, dry_run=args.dry_run)

        if result.success:
            print(f"✅ Restore successful!")
            print(f"   Files restored: {result.restored_files}")
            print(f"   Size: {result.total_size_bytes / 1024 / 1024:.2f}MB")
        else:
            print(f"❌ Restore failed with {len(result.errors)} errors:")
            for error in result.errors[:5]:
                print(f"   - {error}")

    elif args.operation == 'list':
        backups = manager.list_backups()
        print(f"📋 Found {len(backups)} backups:\n")
        for backup in backups[:20]:  # Show latest 20
            age = datetime.now() - datetime.fromisoformat(backup.timestamp)
            print(f"   {backup.backup_id}")
            print(f"   ├─ Type: {backup.backup_type.value}")
            print(f"   ├─ Date: {backup.timestamp} ({age.days}d ago)")
            print(f"   ├─ Size: {backup.total_size_bytes / 1024 / 1024:.2f}MB")
            print(f"   └─ Files: {backup.file_count}")
            print()

    elif args.operation == 'rotate':
        print("🔄 Rotating old backups...")
        deleted = manager.rotate_backups()
        print(f"✅ Deleted {deleted} old backups")

    elif args.operation == 'verify':
        if not args.backup_id:
            print("❌ Error: backup_id required for verify")
            sys.exit(1)

        print(f"🔍 Verifying backup: {args.backup_id}")
        if manager.verify_backup(args.backup_id):
            print("✅ Backup verification successful")
        else:
            print("❌ Backup verification FAILED")
            sys.exit(1)

    elif args.operation == 'auto':
        print("🤖 Running automated backup job...")
        automated_backup_job(memory_path)
        print("✅ Automated backup complete")


def cmd_migrate(args):
    """Execute migration command"""
    memory_path = Path(args.memory_path)
    manager = MigrationManager(memory_path)

    if args.operation == 'detect':
        version = manager.detect_version()
        print(f"📊 Current schema version: {version}")

    elif args.operation == 'migrate':
        if args.version:
            print(f"🔄 Migrating to version {args.version}...")
            current = manager.detect_version()
            result = manager.migrate(current, args.version, backup=not args.no_backup)
        else:
            print("🔄 Migrating to latest version...")
            result = manager.migrate_to_latest(backup=not args.no_backup)

        if result.success:
            print(f"✅ Migration successful!")
            print(f"   {result.from_version} → {result.to_version}")
            print(f"   Items migrated: {result.items_migrated}")
            print(f"   Files updated: {result.files_updated}")
            print(f"   Duration: {result.duration_seconds:.2f}s")
            if result.backup_created:
                print("   Backup created: Yes")
        else:
            print(f"❌ Migration failed:")
            for error in result.errors:
                print(f"   - {error}")
            sys.exit(1)


def cmd_monitor(args):
    """Execute monitoring command"""
    memory_path = Path(args.memory_path)
    monitor = MemoryMonitor(memory_path)

    if args.operation == 'metrics':
        print("📊 Collecting memory metrics...\n")
        metrics = monitor.collect_memory_metrics()

        print("Memory Usage:")
        print(f"   Total size: {metrics.total_size_bytes / 1024 / 1024:.2f}MB")
        print(f"   Agents: {metrics.agent_count}")
        print(f"   Patterns: {metrics.pattern_count:,}")
        print(f"   Solutions: {metrics.solution_count:,}")
        print(f"   Decisions: {metrics.decision_count:,}")
        print(f"   Largest agent: {metrics.largest_agent} ({metrics.largest_agent_size_bytes / 1024 / 1024:.2f}MB)")

    elif args.operation == 'health':
        print("🏥 Running health check...\n")
        health = monitor.run_health_check()

        status_emoji = {
            HealthStatus.HEALTHY: "✅",
            HealthStatus.WARNING: "⚠️",
            HealthStatus.CRITICAL: "🚨",
            HealthStatus.UNKNOWN: "❓"
        }

        print(f"Status: {status_emoji[health.status]} {health.status.value.upper()}\n")

        print("Checks:")
        for check, passed in health.checks.items():
            symbol = "✓" if passed else "✗"
            print(f"   {symbol} {check}")

        if health.warnings:
            print("\n⚠️  Warnings:")
            for warning in health.warnings:
                print(f"   - {warning}")

        if health.errors:
            print("\n🚨 Errors:")
            for error in health.errors:
                print(f"   - {error}")

    elif args.operation == 'alerts':
        alerts = monitor.get_active_alerts()
        print(f"🚨 Active Alerts: {len(alerts)}\n")

        if alerts:
            for alert in alerts:
                emoji = {
                    'info': 'ℹ️',
                    'warning': '⚠️',
                    'error': '❌',
                    'critical': '🚨'
                }.get(alert.level.value, '•')

                print(f"{emoji} [{alert.level.value.upper()}] {alert.category}")
                print(f"   {alert.message}")
                print(f"   Time: {alert.timestamp}")
                print()
        else:
            print("✅ No active alerts")

    elif args.operation == 'report':
        print("📄 Generating monitoring report...\n")
        report = monitor.generate_report()

        import json
        print(json.dumps(report, indent=2))


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description='AML Memory Management CLI',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument('memory_path', help='Path to .loom/memory directory')

    subparsers = parser.add_subparsers(dest='command', help='Command to execute')

    # Prune command
    prune_parser = subparsers.add_parser('prune', help='Prune memory')
    prune_parser.add_argument(
        '--strategies',
        nargs='+',
        default=['time_based', 'performance_based'],
        choices=['time_based', 'performance_based', 'space_based'],
        help='Pruning strategies to apply'
    )
    prune_parser.add_argument('--agents', nargs='+', help='Specific agents to prune')
    prune_parser.add_argument('--dry-run', action='store_true', help='Preview changes without applying')
    prune_parser.add_argument('--aggressive', action='store_true', help='Use aggressive pruning thresholds')

    # Optimize command
    opt_parser = subparsers.add_parser('optimize', help='Optimize memory')
    opt_parser.add_argument(
        'operation',
        choices=['index', 'compress', 'warm-cache', 'gc', 'all'],
        help='Optimization operation'
    )
    opt_parser.add_argument('--agents', nargs='+', help='Specific agents for cache warming')
    opt_parser.add_argument('--age-days', type=int, help='Age threshold for compression')
    opt_parser.add_argument('--dry-run', action='store_true', help='Preview changes')

    # Backup command
    backup_parser = subparsers.add_parser('backup', help='Backup operations')
    backup_parser.add_argument(
        'operation',
        choices=['create', 'restore', 'list', 'rotate', 'verify', 'auto'],
        help='Backup operation'
    )
    backup_parser.add_argument('--backup-id', help='Backup ID for restore/verify')
    backup_parser.add_argument('--agents', nargs='+', help='Specific agents to backup')
    backup_parser.add_argument('--incremental', action='store_true', help='Create incremental backup')
    backup_parser.add_argument('--dry-run', action='store_true', help='Preview restore')

    # Migrate command
    migrate_parser = subparsers.add_parser('migrate', help='Schema migration')
    migrate_parser.add_argument(
        'operation',
        choices=['detect', 'migrate'],
        help='Migration operation'
    )
    migrate_parser.add_argument('--version', help='Target version for migration')
    migrate_parser.add_argument('--no-backup', action='store_true', help='Skip pre-migration backup')

    # Monitor command
    monitor_parser = subparsers.add_parser('monitor', help='Monitoring and health')
    monitor_parser.add_argument(
        'operation',
        choices=['metrics', 'health', 'alerts', 'report'],
        help='Monitoring operation'
    )

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    # Verify memory path exists
    memory_path = Path(args.memory_path)
    if not memory_path.exists():
        print(f"❌ Error: Memory path does not exist: {memory_path}")
        sys.exit(1)

    # Execute command
    try:
        if args.command == 'prune':
            cmd_prune(args)
        elif args.command == 'optimize':
            cmd_optimize(args)
        elif args.command == 'backup':
            cmd_backup(args)
        elif args.command == 'migrate':
            cmd_migrate(args)
        elif args.command == 'monitor':
            cmd_monitor(args)
        else:
            print(f"❌ Unknown command: {args.command}")
            sys.exit(1)

    except Exception as e:
        logger.exception("Command failed")
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
