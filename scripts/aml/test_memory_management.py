#!/usr/bin/env python3
"""
Comprehensive Unit Tests for AML Memory Management

Tests all components: pruning, optimization, backup, migration, and monitoring.

Author: Loom Framework
Version: 1.0.0
"""

import json
import gzip
import shutil
import tempfile
import unittest
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, Any, List

# Import modules to test
from pruning import (
    MemoryPruner, PruneStrategy, PruneConfig, PruneReason
)
from optimization import (
    BloomFilter, LRUCache, MemoryIndex, LazyMemoryLoader,
    MemoryCompressor, GarbageCollector
)
from backup import (
    BackupManager, BackupType, BackupConfig
)
from migration import (
    MigrationManager, SchemaVersion, Migration_1_0_to_1_1
)
from monitoring import (
    MemoryMonitor, HealthStatus, AlertLevel
)


class TestMemoryPruner(unittest.TestCase):
    """Test cases for memory pruning"""

    def setUp(self):
        """Set up test environment"""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.memory_path = self.temp_dir / 'memory'
        self.memory_path.mkdir(parents=True)

        # Create test data
        self._create_test_agent('test-agent')

    def tearDown(self):
        """Clean up test environment"""
        shutil.rmtree(self.temp_dir)

    def _create_test_agent(self, agent_name: str) -> None:
        """Create test agent with sample data"""
        agent_dir = self.memory_path / agent_name
        agent_dir.mkdir(parents=True, exist_ok=True)

        # Create old pattern (should be pruned)
        old_pattern = {
            'id': 'pattern-1',
            'agent': agent_name,
            'timestamp': (datetime.now() - timedelta(days=100)).isoformat(),
            'pattern': {'type': 'test'},
            'metrics': {'successRate': 0.5, 'executionCount': 5},
            'evolution': {
                'lastUsed': (datetime.now() - timedelta(days=100)).isoformat(),
                'confidenceScore': 0.5
            },
            'active': True
        }

        # Create recent pattern (should be kept)
        recent_pattern = {
            'id': 'pattern-2',
            'agent': agent_name,
            'timestamp': datetime.now().isoformat(),
            'pattern': {'type': 'test'},
            'metrics': {'successRate': 0.95, 'executionCount': 50},
            'evolution': {
                'lastUsed': datetime.now().isoformat(),
                'confidenceScore': 0.9
            },
            'active': True
        }

        # Create failed pattern (should be pruned)
        failed_pattern = {
            'id': 'pattern-3',
            'agent': agent_name,
            'timestamp': (datetime.now() - timedelta(days=40)).isoformat(),
            'pattern': {'type': 'test'},
            'metrics': {'successRate': 0.1, 'executionCount': 10},
            'evolution': {
                'lastUsed': (datetime.now() - timedelta(days=40)).isoformat(),
                'confidenceScore': 0.2
            },
            'active': True
        }

        with open(agent_dir / 'patterns.json', 'w') as f:
            json.dump([old_pattern, recent_pattern, failed_pattern], f)

    def test_time_based_pruning(self):
        """Test time-based pruning removes old patterns"""
        config = PruneConfig(pattern_max_age_days=90)
        pruner = MemoryPruner(self.memory_path, config)

        result = pruner._prune_time_based(['test-agent'])

        self.assertGreater(result.items_pruned, 0)
        self.assertEqual(result.strategy, PruneStrategy.TIME_BASED)

        # Verify old pattern was removed
        with open(self.memory_path / 'test-agent' / 'patterns.json', 'r') as f:
            patterns = json.load(f)

        pattern_ids = [p['id'] for p in patterns]
        self.assertNotIn('pattern-1', pattern_ids)
        self.assertIn('pattern-2', pattern_ids)

    def test_performance_based_pruning(self):
        """Test performance-based pruning removes low success patterns"""
        config = PruneConfig(min_success_rate=0.20)
        pruner = MemoryPruner(self.memory_path, config)

        result = pruner._prune_performance_based(['test-agent'])

        self.assertGreater(result.items_pruned, 0)

        # Verify failed pattern was removed
        with open(self.memory_path / 'test-agent' / 'patterns.json', 'r') as f:
            patterns = json.load(f)

        pattern_ids = [p['id'] for p in patterns]
        self.assertNotIn('pattern-3', pattern_ids)

    def test_space_based_pruning(self):
        """Test space-based pruning when memory limits exceeded"""
        # Create large data to exceed limits
        for i in range(100):
            self._create_test_agent(f'agent-{i}')

        config = PruneConfig(
            agent_memory_limit=10 * 1024,  # 10KB
            preserve_high_value=True
        )
        pruner = MemoryPruner(self.memory_path, config)

        result = pruner._prune_space_based([f'agent-{i}' for i in range(100)])

        # Should have pruned or compressed something
        self.assertTrue(result.items_pruned > 0 or result.items_compressed > 0)


class TestBloomFilter(unittest.TestCase):
    """Test cases for Bloom filter"""

    def test_add_and_contains(self):
        """Test adding items and checking membership"""
        bf = BloomFilter(capacity=1000, error_rate=0.01)

        # Add items
        items = ['pattern-1', 'pattern-2', 'pattern-3']
        for item in items:
            bf.add(item)

        # Check membership
        for item in items:
            self.assertTrue(bf.contains(item))

        # Check non-member (may have false positive)
        self.assertFalse(bf.contains('pattern-999'))

    def test_serialization(self):
        """Test bloom filter serialization"""
        bf = BloomFilter(capacity=100)
        bf.add('test-1')
        bf.add('test-2')

        # Serialize
        data = bf.to_bytes()

        # Deserialize
        bf2 = BloomFilter.from_bytes(data)

        # Verify
        self.assertTrue(bf2.contains('test-1'))
        self.assertTrue(bf2.contains('test-2'))


class TestLRUCache(unittest.TestCase):
    """Test cases for LRU cache"""

    def test_basic_operations(self):
        """Test basic cache operations"""
        cache = LRUCache(max_size_bytes=1000)

        # Add items
        cache.put('key1', {'data': 'value1'}, 100)
        cache.put('key2', {'data': 'value2'}, 100)

        # Retrieve items
        self.assertIsNotNone(cache.get('key1'))
        self.assertIsNone(cache.get('key3'))

    def test_eviction(self):
        """Test LRU eviction policy"""
        cache = LRUCache(max_size_bytes=250)

        # Add items
        cache.put('key1', 'value1', 100)
        cache.put('key2', 'value2', 100)
        cache.put('key3', 'value3', 100)  # Should evict key1

        # key1 should be evicted
        self.assertIsNone(cache.get('key1'))
        self.assertIsNotNone(cache.get('key2'))
        self.assertIsNotNone(cache.get('key3'))


class TestMemoryIndex(unittest.TestCase):
    """Test cases for memory index"""

    def setUp(self):
        """Set up test environment"""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.memory_path = self.temp_dir / 'memory'
        self.memory_path.mkdir(parents=True)
        (self.memory_path / 'global').mkdir()

        # Create test agent data
        agent_dir = self.memory_path / 'test-agent'
        agent_dir.mkdir()

        patterns = [
            {
                'id': 'p1',
                'agent': 'test-agent',
                'timestamp': datetime.now().isoformat(),
                'pattern': {'type': 'react'},
                'metrics': {'successRate': 0.9, 'executionCount': 10},
                'evolution': {'confidenceScore': 0.8},
                'tags': ['react', 'optimization']
            }
        ]

        with open(agent_dir / 'patterns.json', 'w') as f:
            json.dump(patterns, f)

    def tearDown(self):
        """Clean up test environment"""
        shutil.rmtree(self.temp_dir)

    def test_build_index(self):
        """Test index building"""
        index = MemoryIndex(self.memory_path)
        count = index.build_index(force=True)

        self.assertGreater(count, 0)
        self.assertTrue(index.exists('p1'))

    def test_search(self):
        """Test index search"""
        index = MemoryIndex(self.memory_path)
        index.build_index(force=True)

        # Search by agent
        results = index.search(agent='test-agent')
        self.assertEqual(len(results), 1)

        # Search by tags
        results = index.search(tags=['react'])
        self.assertEqual(len(results), 1)

        # Search with filters
        results = index.search(min_confidence=0.7, min_success_rate=0.8)
        self.assertEqual(len(results), 1)


class TestBackupManager(unittest.TestCase):
    """Test cases for backup management"""

    def setUp(self):
        """Set up test environment"""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.memory_path = self.temp_dir / 'memory'
        self.memory_path.mkdir(parents=True)

        # Create test data
        agent_dir = self.memory_path / 'test-agent'
        agent_dir.mkdir()

        with open(agent_dir / 'patterns.json', 'w') as f:
            json.dump([{'id': 'p1', 'data': 'test'}], f)

    def tearDown(self):
        """Clean up test environment"""
        shutil.rmtree(self.temp_dir)

    def test_full_backup(self):
        """Test full backup creation"""
        manager = BackupManager(self.memory_path)
        metadata = manager.create_full_backup()

        self.assertEqual(metadata.backup_type, BackupType.FULL)
        self.assertGreater(metadata.file_count, 0)
        self.assertTrue(Path(metadata.backup_path).exists())

    def test_incremental_backup(self):
        """Test incremental backup"""
        manager = BackupManager(self.memory_path)

        # Create full backup
        full_backup = manager.create_full_backup()

        # Modify data
        agent_dir = self.memory_path / 'test-agent'
        with open(agent_dir / 'patterns.json', 'w') as f:
            json.dump([{'id': 'p1', 'data': 'modified'}], f)

        # Create incremental backup
        incr_backup = manager.create_incremental_backup(full_backup.backup_id)

        self.assertEqual(incr_backup.backup_type, BackupType.INCREMENTAL)
        self.assertEqual(incr_backup.parent_backup_id, full_backup.backup_id)

    def test_restore(self):
        """Test backup restore"""
        manager = BackupManager(self.memory_path)

        # Create backup
        metadata = manager.create_full_backup()

        # Delete original data
        shutil.rmtree(self.memory_path / 'test-agent')

        # Restore
        result = manager.restore_backup(metadata.backup_id)

        self.assertTrue(result.success)
        self.assertTrue((self.memory_path / 'test-agent' / 'patterns.json').exists())


class TestMigrationManager(unittest.TestCase):
    """Test cases for schema migration"""

    def setUp(self):
        """Set up test environment"""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.memory_path = self.temp_dir / 'memory'
        self.memory_path.mkdir(parents=True)
        (self.memory_path / 'config').mkdir()

        # Create v1.0.0 pattern (without tags and active fields)
        agent_dir = self.memory_path / 'test-agent'
        agent_dir.mkdir()

        old_pattern = {
            'id': 'p1',
            'agent': 'test-agent',
            'timestamp': '2025-01-01T10:00:00Z',
            'pattern': {'type': 'test'},
            'metrics': {'successRate': 0.9, 'executionCount': 10},
            'evolution': {
                'created': '2025-01-01T10:00:00Z',
                'lastUsed': '2025-01-10T10:00:00Z',
                'confidenceScore': 0.8
            }
        }

        with open(agent_dir / 'patterns.json', 'w') as f:
            json.dump([old_pattern], f)

    def tearDown(self):
        """Clean up test environment"""
        shutil.rmtree(self.temp_dir)

    def test_version_detection(self):
        """Test schema version detection"""
        manager = MigrationManager(self.memory_path)
        version = manager.detect_version()

        self.assertEqual(version, '1.0.0')

    def test_migration_1_0_to_1_1(self):
        """Test migration from v1.0.0 to v1.1.0"""
        migration = Migration_1_0_to_1_1()

        old_pattern = {
            'id': 'p1',
            'agent': 'test',
            'timestamp': '2025-01-01T10:00:00Z',
            'pattern': {'type': 'test'},
            'metrics': {},
            'evolution': {}
        }

        new_pattern = migration.migrate_pattern(old_pattern)

        # Should have added tags and active fields
        self.assertIn('tags', new_pattern)
        self.assertIn('active', new_pattern)
        self.assertEqual(new_pattern['active'], True)

    def test_full_migration(self):
        """Test full migration process"""
        manager = MigrationManager(self.memory_path)

        # Migrate to v1.1.0
        result = manager.migrate('1.0.0', '1.1.0', backup=False)

        self.assertTrue(result.success)
        self.assertGreater(result.items_migrated, 0)

        # Verify migrated pattern has new fields
        with open(self.memory_path / 'test-agent' / 'patterns.json', 'r') as f:
            patterns = json.load(f)

        self.assertIn('tags', patterns[0])
        self.assertIn('active', patterns[0])


class TestMemoryMonitor(unittest.TestCase):
    """Test cases for monitoring"""

    def setUp(self):
        """Set up test environment"""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.memory_path = self.temp_dir / 'memory'
        self.memory_path.mkdir(parents=True)
        (self.memory_path / 'global').mkdir()
        (self.memory_path / 'config').mkdir()

        # Create test data
        agent_dir = self.memory_path / 'test-agent'
        agent_dir.mkdir()

        with open(agent_dir / 'patterns.json', 'w') as f:
            json.dump([{'id': 'p1', 'data': 'test' * 100}] * 10, f)

    def tearDown(self):
        """Clean up test environment"""
        shutil.rmtree(self.temp_dir)

    def test_collect_metrics(self):
        """Test metrics collection"""
        monitor = MemoryMonitor(self.memory_path)
        metrics = monitor.collect_memory_metrics()

        self.assertGreater(metrics.total_size_bytes, 0)
        self.assertGreater(metrics.pattern_count, 0)
        self.assertEqual(metrics.agent_count, 1)

    def test_health_check(self):
        """Test health check"""
        monitor = MemoryMonitor(self.memory_path)
        health = monitor.run_health_check()

        self.assertIn(health.status, [HealthStatus.HEALTHY, HealthStatus.WARNING])
        self.assertGreater(len(health.checks), 0)

    def test_alert_creation(self):
        """Test alert creation"""
        monitor = MemoryMonitor(self.memory_path)

        alert = monitor.create_alert(
            AlertLevel.WARNING,
            'test',
            'Test alert',
            {'key': 'value'}
        )

        self.assertEqual(alert.level, AlertLevel.WARNING)
        self.assertFalse(alert.resolved)

        # Resolve alert
        monitor.resolve_alert(alert.id)

        # Check it's resolved
        active_alerts = monitor.get_active_alerts()
        self.assertEqual(len(active_alerts), 0)


class TestGarbageCollector(unittest.TestCase):
    """Test cases for garbage collection"""

    def setUp(self):
        """Set up test environment"""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.memory_path = self.temp_dir / 'memory'
        self.memory_path.mkdir(parents=True)

        # Create test data with invalid items
        agent_dir = self.memory_path / 'test-agent'
        agent_dir.mkdir()

        valid_pattern = {
            'id': 'p1',
            'agent': 'test-agent',
            'timestamp': datetime.now().isoformat(),
            'pattern': {'type': 'test'}
        }

        invalid_pattern = {
            'id': 'p2',
            # Missing required 'agent' field
            'timestamp': datetime.now().isoformat()
        }

        with open(agent_dir / 'patterns.json', 'w') as f:
            json.dump([valid_pattern, invalid_pattern], f)

    def tearDown(self):
        """Clean up test environment"""
        shutil.rmtree(self.temp_dir)

    def test_garbage_collection(self):
        """Test garbage collection removes invalid items"""
        gc = GarbageCollector(self.memory_path)
        stats = gc.collect(dry_run=False)

        self.assertGreater(stats['invalid_items'], 0)

        # Verify invalid item was removed
        with open(self.memory_path / 'test-agent' / 'patterns.json', 'r') as f:
            patterns = json.load(f)

        self.assertEqual(len(patterns), 1)
        self.assertEqual(patterns[0]['id'], 'p1')


def run_tests():
    """Run all test suites"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add all test cases
    suite.addTests(loader.loadTestsFromTestCase(TestMemoryPruner))
    suite.addTests(loader.loadTestsFromTestCase(TestBloomFilter))
    suite.addTests(loader.loadTestsFromTestCase(TestLRUCache))
    suite.addTests(loader.loadTestsFromTestCase(TestMemoryIndex))
    suite.addTests(loader.loadTestsFromTestCase(TestBackupManager))
    suite.addTests(loader.loadTestsFromTestCase(TestMigrationManager))
    suite.addTests(loader.loadTestsFromTestCase(TestMemoryMonitor))
    suite.addTests(loader.loadTestsFromTestCase(TestGarbageCollector))

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    return result.wasSuccessful()


if __name__ == '__main__':
    import sys
    success = run_tests()
    sys.exit(0 if success else 1)
