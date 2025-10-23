#!/usr/bin/env python3
"""
AML Monitoring & Alerting System

Implements memory usage monitoring, performance degradation detection,
alerting for memory limits, health checks, and diagnostic tools.

Author: Loom Framework
Version: 1.0.0
"""

import json
import time
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from enum import Enum


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class HealthStatus(Enum):
    """Health status levels"""
    HEALTHY = "healthy"
    WARNING = "warning"
    CRITICAL = "critical"
    UNKNOWN = "unknown"


class AlertLevel(Enum):
    """Alert severity levels"""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


@dataclass
class MemoryMetrics:
    """Memory usage metrics"""
    timestamp: str
    total_size_bytes: int
    agent_count: int
    pattern_count: int
    solution_count: int
    decision_count: int
    avg_pattern_size_bytes: float
    largest_agent: str
    largest_agent_size_bytes: int
    compressed_files: int
    uncompressed_files: int
    index_size_bytes: int


@dataclass
class PerformanceMetrics:
    """Performance metrics"""
    timestamp: str
    avg_query_time_ms: float
    cache_hit_rate: float
    index_build_time_ms: float
    backup_time_ms: float
    prune_time_ms: float


@dataclass
class Alert:
    """Alert object"""
    id: str
    timestamp: str
    level: AlertLevel
    category: str
    message: str
    details: Dict[str, Any]
    resolved: bool = False
    resolved_at: Optional[str] = None


@dataclass
class HealthCheck:
    """Health check result"""
    timestamp: str
    status: HealthStatus
    checks: Dict[str, bool]
    warnings: List[str]
    errors: List[str]
    metrics: Dict[str, Any]


class MemoryMonitor:
    """
    Monitors memory usage and performance metrics.

    Features:
    - Real-time memory usage tracking
    - Performance degradation detection
    - Automated alerting
    - Health checks
    """

    def __init__(self, memory_path: Path, config: Optional[Dict[str, Any]] = None):
        """
        Initialize memory monitor.

        Args:
            memory_path: Path to .loom/memory directory
            config: Monitor configuration
        """
        self.memory_path = Path(memory_path)
        self.config = config or {
            'agent_memory_warning_mb': 60,
            'agent_memory_critical_mb': 80,
            'global_memory_warning_mb': 600,
            'global_memory_critical_mb': 800,
            'cache_hit_rate_warning': 0.5,
            'query_time_warning_ms': 100,
            'alert_retention_days': 7
        }

        # Monitoring data
        self.metrics_dir = memory_path / 'monitoring'
        self.metrics_dir.mkdir(parents=True, exist_ok=True)

        self.metrics_file = self.metrics_dir / 'metrics.json'
        self.alerts_file = self.metrics_dir / 'alerts.json'
        self.health_file = self.metrics_dir / 'health.json'

        # Load existing data
        self.alerts: List[Alert] = self._load_alerts()

    def collect_memory_metrics(self) -> MemoryMetrics:
        """
        Collect current memory usage metrics.

        Returns:
            MemoryMetrics object
        """
        total_size = 0
        agent_sizes = {}
        pattern_count = 0
        solution_count = 0
        decision_count = 0
        compressed_files = 0
        uncompressed_files = 0
        pattern_sizes = []

        # Scan agent directories
        for agent_dir in self.memory_path.iterdir():
            if not agent_dir.is_dir() or agent_dir.name in ['global', 'config', 'backup', 'monitoring']:
                continue

            agent_size = 0

            # Count items and sizes
            for file_name in ['patterns.json', 'solutions.json', 'decisions.json']:
                for suffix in ['', '.gz']:
                    file_path = agent_dir / (file_name + suffix)
                    if file_path.exists():
                        file_size = file_path.stat().st_size
                        agent_size += file_size
                        total_size += file_size

                        if suffix == '.gz':
                            compressed_files += 1
                        else:
                            uncompressed_files += 1

                        # Count items
                        try:
                            items = self._load_json(file_path)
                            if 'patterns' in file_name:
                                pattern_count += len(items)
                                pattern_sizes.extend([len(json.dumps(item)) for item in items])
                            elif 'solutions' in file_name:
                                solution_count += len(items)
                            elif 'decisions' in file_name:
                                decision_count += len(items)
                        except Exception as e:
                            logger.warning(f"Error counting items in {file_path}: {e}")

            agent_sizes[agent_dir.name] = agent_size

        # Find largest agent
        if agent_sizes:
            largest_agent = max(agent_sizes.items(), key=lambda x: x[1])
        else:
            largest_agent = ('none', 0)

        # Get index size
        index_size = 0
        index_file = self.memory_path / 'global' / 'index.json'
        if index_file.exists():
            index_size = index_file.stat().st_size

        # Calculate average pattern size
        avg_pattern_size = sum(pattern_sizes) / len(pattern_sizes) if pattern_sizes else 0

        metrics = MemoryMetrics(
            timestamp=datetime.now().isoformat(),
            total_size_bytes=total_size,
            agent_count=len(agent_sizes),
            pattern_count=pattern_count,
            solution_count=solution_count,
            decision_count=decision_count,
            avg_pattern_size_bytes=avg_pattern_size,
            largest_agent=largest_agent[0],
            largest_agent_size_bytes=largest_agent[1],
            compressed_files=compressed_files,
            uncompressed_files=uncompressed_files,
            index_size_bytes=index_size
        )

        # Save metrics
        self._save_metrics(metrics)

        # Check for alerts
        self._check_memory_alerts(metrics)

        return metrics

    def collect_performance_metrics(self) -> PerformanceMetrics:
        """
        Collect performance metrics.

        Returns:
            PerformanceMetrics object
        """
        timestamp = datetime.now().isoformat()

        # Measure query time
        query_times = []
        for _ in range(10):
            start = time.time()
            self._sample_query()
            query_times.append((time.time() - start) * 1000)

        avg_query_time = sum(query_times) / len(query_times)

        # Get cache hit rate (if available)
        cache_hit_rate = self._get_cache_hit_rate()

        # Get operation times from logs
        index_build_time = self._get_last_operation_time('index_build')
        backup_time = self._get_last_operation_time('backup')
        prune_time = self._get_last_operation_time('prune')

        metrics = PerformanceMetrics(
            timestamp=timestamp,
            avg_query_time_ms=avg_query_time,
            cache_hit_rate=cache_hit_rate,
            index_build_time_ms=index_build_time,
            backup_time_ms=backup_time,
            prune_time_ms=prune_time
        )

        # Check for performance alerts
        self._check_performance_alerts(metrics)

        return metrics

    def run_health_check(self) -> HealthCheck:
        """
        Run comprehensive health check.

        Returns:
            HealthCheck object
        """
        timestamp = datetime.now().isoformat()
        checks = {}
        warnings = []
        errors = []

        # Check 1: Memory directory structure
        checks['directory_structure'] = all([
            self.memory_path.exists(),
            (self.memory_path / 'global').exists(),
            (self.memory_path / 'config').exists()
        ])
        if not checks['directory_structure']:
            errors.append("Memory directory structure is incomplete")

        # Check 2: Memory limits
        metrics = self.collect_memory_metrics()
        checks['memory_within_limits'] = metrics.total_size_bytes < (self.config['global_memory_critical_mb'] * 1024 * 1024)
        if not checks['memory_within_limits']:
            errors.append(f"Memory usage exceeds critical limit: {metrics.total_size_bytes / 1024 / 1024:.1f}MB")

        # Check 3: Index exists and is recent
        index_file = self.memory_path / 'global' / 'index.json'
        checks['index_exists'] = index_file.exists()
        if checks['index_exists']:
            index_age = time.time() - index_file.stat().st_mtime
            if index_age > 86400:  # 24 hours
                warnings.append(f"Index is outdated ({index_age / 3600:.1f} hours old)")
        else:
            warnings.append("Index does not exist")

        # Check 4: Recent backup exists
        backup_dir = self.memory_path.parent / 'memory-backup'
        checks['recent_backup'] = False
        if backup_dir.exists():
            backups = list(backup_dir.glob('full_*'))
            if backups:
                latest_backup = max(backups, key=lambda p: p.stat().st_mtime)
                backup_age = time.time() - latest_backup.stat().st_mtime
                checks['recent_backup'] = backup_age < 86400  # 24 hours

                if not checks['recent_backup']:
                    warnings.append(f"Latest backup is {backup_age / 3600:.1f} hours old")
        else:
            warnings.append("No backups found")

        # Check 5: File integrity
        checks['file_integrity'] = True
        for agent_dir in self.memory_path.iterdir():
            if not agent_dir.is_dir() or agent_dir.name in ['global', 'config', 'backup', 'monitoring']:
                continue

            for file_name in ['patterns.json', 'solutions.json', 'decisions.json']:
                file_path = agent_dir / file_name
                if file_path.exists():
                    try:
                        self._load_json(file_path)
                    except Exception as e:
                        checks['file_integrity'] = False
                        errors.append(f"Corrupted file: {file_path} - {e}")

        # Check 6: Performance
        perf_metrics = self.collect_performance_metrics()
        checks['performance_ok'] = perf_metrics.avg_query_time_ms < self.config['query_time_warning_ms']
        if not checks['performance_ok']:
            warnings.append(f"Query performance degraded: {perf_metrics.avg_query_time_ms:.2f}ms")

        # Determine overall status
        if errors:
            status = HealthStatus.CRITICAL
        elif warnings:
            status = HealthStatus.WARNING
        else:
            status = HealthStatus.HEALTHY

        health = HealthCheck(
            timestamp=timestamp,
            status=status,
            checks=checks,
            warnings=warnings,
            errors=errors,
            metrics={
                'total_size_mb': metrics.total_size_bytes / 1024 / 1024,
                'agent_count': metrics.agent_count,
                'pattern_count': metrics.pattern_count,
                'avg_query_time_ms': perf_metrics.avg_query_time_ms,
                'cache_hit_rate': perf_metrics.cache_hit_rate
            }
        )

        # Save health check result
        self._save_health_check(health)

        return health

    def create_alert(
        self,
        level: AlertLevel,
        category: str,
        message: str,
        details: Dict[str, Any]
    ) -> Alert:
        """
        Create a new alert.

        Args:
            level: Alert severity level
            category: Alert category (memory, performance, backup, etc.)
            message: Alert message
            details: Additional details

        Returns:
            Alert object
        """
        alert = Alert(
            id=f"alert_{int(time.time())}",
            timestamp=datetime.now().isoformat(),
            level=level,
            category=category,
            message=message,
            details=details
        )

        self.alerts.append(alert)
        self._save_alerts()

        # Log alert
        log_level = {
            AlertLevel.INFO: logging.INFO,
            AlertLevel.WARNING: logging.WARNING,
            AlertLevel.ERROR: logging.ERROR,
            AlertLevel.CRITICAL: logging.CRITICAL
        }[level]

        logger.log(log_level, f"[{category}] {message}")

        return alert

    def resolve_alert(self, alert_id: str) -> bool:
        """Resolve an alert"""
        for alert in self.alerts:
            if alert.id == alert_id and not alert.resolved:
                alert.resolved = True
                alert.resolved_at = datetime.now().isoformat()
                self._save_alerts()
                logger.info(f"Resolved alert: {alert_id}")
                return True
        return False

    def get_active_alerts(self) -> List[Alert]:
        """Get all unresolved alerts"""
        return [a for a in self.alerts if not a.resolved]

    def get_metrics_history(self, hours: int = 24) -> List[MemoryMetrics]:
        """Get metrics history for the past N hours"""
        cutoff = datetime.now() - timedelta(hours=hours)
        history = []

        if self.metrics_file.exists():
            try:
                with open(self.metrics_file, 'r') as f:
                    data = json.load(f)

                for entry in data.get('history', []):
                    timestamp = datetime.fromisoformat(entry['timestamp'])
                    if timestamp >= cutoff:
                        history.append(MemoryMetrics(**entry))

            except Exception as e:
                logger.error(f"Error loading metrics history: {e}")

        return history

    def generate_report(self) -> Dict[str, Any]:
        """Generate comprehensive monitoring report"""
        memory_metrics = self.collect_memory_metrics()
        perf_metrics = self.collect_performance_metrics()
        health = self.run_health_check()
        active_alerts = self.get_active_alerts()

        report = {
            'timestamp': datetime.now().isoformat(),
            'status': health.status.value,
            'memory': {
                'total_mb': memory_metrics.total_size_bytes / 1024 / 1024,
                'agents': memory_metrics.agent_count,
                'patterns': memory_metrics.pattern_count,
                'solutions': memory_metrics.solution_count,
                'decisions': memory_metrics.decision_count,
                'largest_agent': {
                    'name': memory_metrics.largest_agent,
                    'size_mb': memory_metrics.largest_agent_size_bytes / 1024 / 1024
                }
            },
            'performance': {
                'avg_query_time_ms': perf_metrics.avg_query_time_ms,
                'cache_hit_rate': perf_metrics.cache_hit_rate,
                'index_build_time_ms': perf_metrics.index_build_time_ms
            },
            'health_checks': {
                'status': health.status.value,
                'passed': sum(1 for v in health.checks.values() if v),
                'total': len(health.checks),
                'warnings': health.warnings,
                'errors': health.errors
            },
            'alerts': {
                'active': len(active_alerts),
                'by_level': {
                    level.value: len([a for a in active_alerts if a.level == level])
                    for level in AlertLevel
                }
            }
        }

        return report

    # Helper methods

    def _check_memory_alerts(self, metrics: MemoryMetrics) -> None:
        """Check memory metrics and create alerts if needed"""
        total_mb = metrics.total_size_bytes / 1024 / 1024

        # Global memory alerts
        if total_mb >= self.config['global_memory_critical_mb']:
            self.create_alert(
                AlertLevel.CRITICAL,
                'memory',
                f"Global memory usage critical: {total_mb:.1f}MB",
                {'total_mb': total_mb, 'limit_mb': self.config['global_memory_critical_mb']}
            )
        elif total_mb >= self.config['global_memory_warning_mb']:
            self.create_alert(
                AlertLevel.WARNING,
                'memory',
                f"Global memory usage high: {total_mb:.1f}MB",
                {'total_mb': total_mb, 'limit_mb': self.config['global_memory_warning_mb']}
            )

        # Agent memory alerts
        agent_mb = metrics.largest_agent_size_bytes / 1024 / 1024
        if agent_mb >= self.config['agent_memory_critical_mb']:
            self.create_alert(
                AlertLevel.CRITICAL,
                'memory',
                f"Agent {metrics.largest_agent} memory critical: {agent_mb:.1f}MB",
                {'agent': metrics.largest_agent, 'size_mb': agent_mb}
            )

    def _check_performance_alerts(self, metrics: PerformanceMetrics) -> None:
        """Check performance metrics and create alerts if needed"""
        # Query time alerts
        if metrics.avg_query_time_ms >= self.config['query_time_warning_ms']:
            self.create_alert(
                AlertLevel.WARNING,
                'performance',
                f"Query performance degraded: {metrics.avg_query_time_ms:.2f}ms",
                {'avg_query_time_ms': metrics.avg_query_time_ms}
            )

        # Cache hit rate alerts
        if metrics.cache_hit_rate < self.config['cache_hit_rate_warning']:
            self.create_alert(
                AlertLevel.WARNING,
                'performance',
                f"Low cache hit rate: {metrics.cache_hit_rate:.1%}",
                {'cache_hit_rate': metrics.cache_hit_rate}
            )

    def _sample_query(self) -> None:
        """Perform a sample query to measure performance"""
        # Load a random patterns file
        for agent_dir in self.memory_path.iterdir():
            if agent_dir.is_dir() and agent_dir.name not in ['global', 'config', 'backup', 'monitoring']:
                patterns_file = agent_dir / 'patterns.json'
                if patterns_file.exists():
                    try:
                        self._load_json(patterns_file)
                        return
                    except Exception:
                        pass

    def _get_cache_hit_rate(self) -> float:
        """Get cache hit rate from optimization module"""
        try:
            from .optimization import LazyMemoryLoader
            loader = LazyMemoryLoader(self.memory_path)
            stats = loader.get_cache_stats()
            return stats.hit_rate
        except Exception:
            return 0.0

    def _get_last_operation_time(self, operation: str) -> float:
        """Get last recorded time for an operation"""
        # Placeholder - would integrate with actual operation logging
        return 0.0

    def _load_json(self, file_path: Path) -> List[Dict[str, Any]]:
        """Load JSON file with gzip support"""
        import gzip

        try:
            if file_path.suffix == '.gz':
                with gzip.open(file_path, 'rt', encoding='utf-8') as f:
                    return json.load(f)
            else:
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"Error loading {file_path}: {e}")
            return []

    def _save_metrics(self, metrics: MemoryMetrics) -> None:
        """Save metrics to file"""
        try:
            # Load existing history
            history = []
            if self.metrics_file.exists():
                with open(self.metrics_file, 'r') as f:
                    data = json.load(f)
                    history = data.get('history', [])

            # Add new metrics
            history.append(asdict(metrics))

            # Keep only last 1000 entries
            history = history[-1000:]

            # Save
            with open(self.metrics_file, 'w') as f:
                json.dump({'history': history}, f, indent=2)

        except Exception as e:
            logger.error(f"Error saving metrics: {e}")

    def _load_alerts(self) -> List[Alert]:
        """Load alerts from file"""
        alerts = []

        if self.alerts_file.exists():
            try:
                with open(self.alerts_file, 'r') as f:
                    data = json.load(f)

                for alert_data in data.get('alerts', []):
                    alert_data['level'] = AlertLevel(alert_data['level'])
                    alerts.append(Alert(**alert_data))

            except Exception as e:
                logger.error(f"Error loading alerts: {e}")

        return alerts

    def _save_alerts(self) -> None:
        """Save alerts to file"""
        try:
            data = {'alerts': []}

            for alert in self.alerts:
                alert_data = asdict(alert)
                alert_data['level'] = alert.level.value
                data['alerts'].append(alert_data)

            with open(self.alerts_file, 'w') as f:
                json.dump(data, f, indent=2)

        except Exception as e:
            logger.error(f"Error saving alerts: {e}")

    def _save_health_check(self, health: HealthCheck) -> None:
        """Save health check result"""
        try:
            health_data = asdict(health)
            health_data['status'] = health.status.value

            with open(self.health_file, 'w') as f:
                json.dump(health_data, f, indent=2)

        except Exception as e:
            logger.error(f"Error saving health check: {e}")


if __name__ == '__main__':
    import sys

    if len(sys.argv) < 3:
        print("Usage: python monitoring.py <memory_path> <command>")
        print("Commands:")
        print("  metrics       - Collect and display memory metrics")
        print("  performance   - Collect and display performance metrics")
        print("  health        - Run health check")
        print("  alerts        - Show active alerts")
        print("  report        - Generate comprehensive report")
        sys.exit(1)

    memory_path = Path(sys.argv[1])
    command = sys.argv[2]

    monitor = MemoryMonitor(memory_path)

    if command == 'metrics':
        metrics = monitor.collect_memory_metrics()
        print(f"\n=== Memory Metrics ===")
        print(f"Total size: {metrics.total_size_bytes / 1024 / 1024:.2f}MB")
        print(f"Agents: {metrics.agent_count}")
        print(f"Patterns: {metrics.pattern_count}")
        print(f"Solutions: {metrics.solution_count}")
        print(f"Decisions: {metrics.decision_count}")
        print(f"Largest agent: {metrics.largest_agent} ({metrics.largest_agent_size_bytes / 1024 / 1024:.2f}MB)")

    elif command == 'performance':
        metrics = monitor.collect_performance_metrics()
        print(f"\n=== Performance Metrics ===")
        print(f"Avg query time: {metrics.avg_query_time_ms:.2f}ms")
        print(f"Cache hit rate: {metrics.cache_hit_rate:.1%}")

    elif command == 'health':
        health = monitor.run_health_check()
        print(f"\n=== Health Check ===")
        print(f"Status: {health.status.value.upper()}")
        print(f"\nChecks:")
        for check, passed in health.checks.items():
            status = "✓" if passed else "✗"
            print(f"  {status} {check}")

        if health.warnings:
            print(f"\nWarnings:")
            for warning in health.warnings:
                print(f"  - {warning}")

        if health.errors:
            print(f"\nErrors:")
            for error in health.errors:
                print(f"  - {error}")

    elif command == 'alerts':
        alerts = monitor.get_active_alerts()
        print(f"\n=== Active Alerts ({len(alerts)}) ===")
        for alert in alerts:
            print(f"[{alert.level.value.upper()}] {alert.category}: {alert.message}")
            print(f"  Time: {alert.timestamp}")
            print(f"  Details: {alert.details}")
            print()

    elif command == 'report':
        report = monitor.generate_report()
        print(f"\n=== Monitoring Report ===")
        print(json.dumps(report, indent=2))

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
