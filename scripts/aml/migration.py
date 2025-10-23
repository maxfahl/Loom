#!/usr/bin/env python3
"""
AML Schema Migration System

Handles schema migrations, data transformations, version detection,
and backward compatibility for the AML memory system.

Author: Loom Framework
Version: 1.0.0
"""

import json
import gzip
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass
from datetime import datetime
from enum import Enum


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class SchemaVersion(Enum):
    """Supported schema versions"""
    V1_0_0 = "1.0.0"
    V1_1_0 = "1.1.0"
    V1_2_0 = "1.2.0"
    V2_0_0 = "2.0.0"


@dataclass
class MigrationResult:
    """Result of a migration operation"""
    success: bool
    from_version: str
    to_version: str
    items_migrated: int
    files_updated: int
    errors: List[str]
    duration_seconds: float
    backup_created: bool


class MigrationStep:
    """Base class for migration steps"""

    def __init__(self, from_version: SchemaVersion, to_version: SchemaVersion):
        """
        Initialize migration step.

        Args:
            from_version: Source schema version
            to_version: Target schema version
        """
        self.from_version = from_version
        self.to_version = to_version

    def can_migrate(self, current_version: str) -> bool:
        """Check if this step can migrate from current version"""
        return current_version == self.from_version.value

    def migrate_pattern(self, pattern: Dict[str, Any]) -> Dict[str, Any]:
        """Migrate a pattern to new schema"""
        raise NotImplementedError

    def migrate_solution(self, solution: Dict[str, Any]) -> Dict[str, Any]:
        """Migrate a solution to new schema"""
        raise NotImplementedError

    def migrate_decision(self, decision: Dict[str, Any]) -> Dict[str, Any]:
        """Migrate a decision to new schema"""
        raise NotImplementedError


class Migration_1_0_to_1_1(MigrationStep):
    """Migration from v1.0.0 to v1.1.0"""

    def __init__(self):
        super().__init__(SchemaVersion.V1_0_0, SchemaVersion.V1_1_0)

    def migrate_pattern(self, pattern: Dict[str, Any]) -> Dict[str, Any]:
        """
        v1.1.0 changes:
        - Add 'tags' field
        - Add 'active' field
        - Normalize timestamp format
        """
        migrated = pattern.copy()

        # Add tags if missing
        if 'tags' not in migrated:
            migrated['tags'] = []

        # Add active field if missing
        if 'active' not in migrated:
            migrated['active'] = True

        # Normalize timestamp
        if 'timestamp' in migrated:
            migrated['timestamp'] = self._normalize_timestamp(migrated['timestamp'])

        # Normalize evolution timestamps
        if 'evolution' in migrated:
            evolution = migrated['evolution']
            if 'created' in evolution:
                evolution['created'] = self._normalize_timestamp(evolution['created'])
            if 'lastUsed' in evolution:
                evolution['lastUsed'] = self._normalize_timestamp(evolution['lastUsed'])

        return migrated

    def migrate_solution(self, solution: Dict[str, Any]) -> Dict[str, Any]:
        """Migrate solution schema"""
        migrated = solution.copy()

        # Add tags if missing
        if 'tags' not in migrated:
            migrated['tags'] = []

        # Normalize timestamp
        if 'timestamp' in migrated:
            migrated['timestamp'] = self._normalize_timestamp(migrated['timestamp'])

        return migrated

    def migrate_decision(self, decision: Dict[str, Any]) -> Dict[str, Any]:
        """Migrate decision schema"""
        migrated = decision.copy()

        # Add tags if missing
        if 'tags' not in migrated:
            migrated['tags'] = []

        # Normalize timestamp
        if 'timestamp' in migrated:
            migrated['timestamp'] = self._normalize_timestamp(migrated['timestamp'])

        return migrated

    @staticmethod
    def _normalize_timestamp(ts: str) -> str:
        """Ensure ISO 8601 format"""
        try:
            dt = datetime.fromisoformat(ts.replace('Z', '+00:00'))
            return dt.isoformat()
        except Exception:
            return ts


class Migration_1_1_to_1_2(MigrationStep):
    """Migration from v1.1.0 to v1.2.0"""

    def __init__(self):
        super().__init__(SchemaVersion.V1_1_0, SchemaVersion.V1_2_0)

    def migrate_pattern(self, pattern: Dict[str, Any]) -> Dict[str, Any]:
        """
        v1.2.0 changes:
        - Add 'metadata' field with usage analytics
        - Add 'variations' field for pattern variations
        """
        migrated = pattern.copy()

        # Add metadata field
        if 'metadata' not in migrated:
            migrated['metadata'] = {
                'created_by': 'migration',
                'last_modified': datetime.now().isoformat(),
                'version': '1.2.0'
            }

        # Add variations field
        if 'variations' not in migrated:
            migrated['variations'] = []

        return migrated

    def migrate_solution(self, solution: Dict[str, Any]) -> Dict[str, Any]:
        """Migrate solution schema"""
        migrated = solution.copy()

        # Add metadata field
        if 'metadata' not in migrated:
            migrated['metadata'] = {
                'created_by': 'migration',
                'last_modified': datetime.now().isoformat(),
                'version': '1.2.0'
            }

        return migrated

    def migrate_decision(self, decision: Dict[str, Any]) -> Dict[str, Any]:
        """Migrate decision schema"""
        migrated = decision.copy()

        # Add metadata field
        if 'metadata' not in migrated:
            migrated['metadata'] = {
                'created_by': 'migration',
                'last_modified': datetime.now().isoformat(),
                'version': '1.2.0'
            }

        return migrated


class Migration_1_2_to_2_0(MigrationStep):
    """Migration from v1.2.0 to v2.0.0 (breaking changes)"""

    def __init__(self):
        super().__init__(SchemaVersion.V1_2_0, SchemaVersion.V2_0_0)

    def migrate_pattern(self, pattern: Dict[str, Any]) -> Dict[str, Any]:
        """
        v2.0.0 changes:
        - Restructure metrics into separate categories
        - Split evolution into lifecycle
        - Add semantic versioning for patterns
        """
        migrated = {
            'id': pattern['id'],
            'agent': pattern['agent'],
            'timestamp': pattern['timestamp'],
            'version': '2.0.0',
            'pattern': pattern['pattern'],
            'tags': pattern.get('tags', []),
            'active': pattern.get('active', True)
        }

        # Restructure metrics
        old_metrics = pattern.get('metrics', {})
        migrated['performance'] = {
            'success_rate': old_metrics.get('successRate', 0.5),
            'execution_count': old_metrics.get('executionCount', 0),
            'avg_time_saved_ms': old_metrics.get('avgTimeSavedMs', 0),
            'error_prevention_count': old_metrics.get('errorPreventionCount', 0)
        }

        # Restructure evolution into lifecycle
        old_evolution = pattern.get('evolution', {})
        migrated['lifecycle'] = {
            'created_at': old_evolution.get('created', pattern['timestamp']),
            'last_used_at': old_evolution.get('lastUsed', pattern['timestamp']),
            'refinement_count': old_evolution.get('refinements', 0),
            'confidence': old_evolution.get('confidenceScore', 0.5)
        }

        # Add metadata
        migrated['metadata'] = pattern.get('metadata', {
            'version': '2.0.0',
            'migrated_at': datetime.now().isoformat()
        })

        return migrated

    def migrate_solution(self, solution: Dict[str, Any]) -> Dict[str, Any]:
        """Migrate solution schema"""
        # Similar restructuring for solutions
        migrated = solution.copy()
        migrated['version'] = '2.0.0'

        if 'metadata' not in migrated:
            migrated['metadata'] = {
                'version': '2.0.0',
                'migrated_at': datetime.now().isoformat()
            }

        return migrated

    def migrate_decision(self, decision: Dict[str, Any]) -> Dict[str, Any]:
        """Migrate decision schema"""
        # Similar restructuring for decisions
        migrated = decision.copy()
        migrated['version'] = '2.0.0'

        if 'metadata' not in migrated:
            migrated['metadata'] = {
                'version': '2.0.0',
                'migrated_at': datetime.now().isoformat()
            }

        return migrated


class MigrationManager:
    """
    Manages schema migrations for the AML system.

    Features:
    - Automatic version detection
    - Step-by-step migration path
    - Backward compatibility layer
    - Rollback support
    """

    def __init__(self, memory_path: Path):
        """Initialize migration manager"""
        self.memory_path = Path(memory_path)
        self.version_file = memory_path / 'config' / 'schema_version.json'

        # Register migration steps
        self.migrations: List[MigrationStep] = [
            Migration_1_0_to_1_1(),
            Migration_1_1_to_1_2(),
            Migration_1_2_to_2_0(),
        ]

    def detect_version(self) -> str:
        """
        Detect current schema version.

        Returns:
            Version string (e.g., "1.0.0")
        """
        # Check version file first
        if self.version_file.exists():
            try:
                with open(self.version_file, 'r') as f:
                    data = json.load(f)
                    return data.get('version', '1.0.0')
            except Exception as e:
                logger.warning(f"Error reading version file: {e}")

        # Try to detect from data structure
        return self._detect_version_from_data()

    def _detect_version_from_data(self) -> str:
        """Detect version by analyzing data structure"""
        # Sample a few patterns to determine version
        for agent_dir in self.memory_path.iterdir():
            if not agent_dir.is_dir() or agent_dir.name in ['global', 'config', 'backup']:
                continue

            patterns_file = agent_dir / 'patterns.json'
            if patterns_file.exists():
                patterns = self._load_json(patterns_file)
                if patterns:
                    pattern = patterns[0]

                    # Check for v2.0.0 features
                    if 'version' in pattern and pattern['version'] == '2.0.0':
                        return '2.0.0'

                    # Check for v1.2.0 features
                    if 'metadata' in pattern:
                        return '1.2.0'

                    # Check for v1.1.0 features
                    if 'tags' in pattern and 'active' in pattern:
                        return '1.1.0'

                    # Default to v1.0.0
                    return '1.0.0'

        return '1.0.0'

    def migrate_to_latest(self, backup: bool = True) -> MigrationResult:
        """
        Migrate to the latest schema version.

        Args:
            backup: Whether to create backup before migration

        Returns:
            MigrationResult object
        """
        current_version = self.detect_version()
        target_version = self._get_latest_version()

        logger.info(f"Migrating from {current_version} to {target_version}")

        if current_version == target_version:
            logger.info("Already at latest version")
            return MigrationResult(
                success=True,
                from_version=current_version,
                to_version=target_version,
                items_migrated=0,
                files_updated=0,
                errors=[],
                duration_seconds=0.0,
                backup_created=False
            )

        return self.migrate(current_version, target_version, backup)

    def migrate(
        self,
        from_version: str,
        to_version: str,
        backup: bool = True
    ) -> MigrationResult:
        """
        Migrate from one version to another.

        Args:
            from_version: Source version
            to_version: Target version
            backup: Whether to create backup

        Returns:
            MigrationResult object
        """
        start_time = datetime.now()
        items_migrated = 0
        files_updated = 0
        errors = []

        # Create backup if requested
        backup_created = False
        if backup:
            try:
                from .backup import BackupManager
                manager = BackupManager(self.memory_path)
                manager.create_full_backup(description=f"Pre-migration backup: {from_version} -> {to_version}")
                backup_created = True
                logger.info("Created pre-migration backup")
            except Exception as e:
                error_msg = f"Failed to create backup: {e}"
                logger.error(error_msg)
                errors.append(error_msg)
                # Continue anyway - user chose to migrate

        # Build migration path
        migration_path = self._build_migration_path(from_version, to_version)
        if not migration_path:
            error_msg = f"No migration path found from {from_version} to {to_version}"
            logger.error(error_msg)
            return MigrationResult(
                success=False,
                from_version=from_version,
                to_version=to_version,
                items_migrated=0,
                files_updated=0,
                errors=[error_msg],
                duration_seconds=0.0,
                backup_created=backup_created
            )

        logger.info(f"Migration path: {' -> '.join([step.to_version.value for step in migration_path])}")

        # Execute migrations
        for step in migration_path:
            logger.info(f"Applying migration: {step.from_version.value} -> {step.to_version.value}")

            step_items, step_files, step_errors = self._apply_migration_step(step)
            items_migrated += step_items
            files_updated += step_files
            errors.extend(step_errors)

        # Update version file
        if not errors:
            self._save_version(to_version)

        duration = (datetime.now() - start_time).total_seconds()
        success = len(errors) == 0

        logger.info(f"Migration {'complete' if success else 'completed with errors'}: {items_migrated} items, {files_updated} files in {duration:.2f}s")

        return MigrationResult(
            success=success,
            from_version=from_version,
            to_version=to_version,
            items_migrated=items_migrated,
            files_updated=files_updated,
            errors=errors,
            duration_seconds=duration,
            backup_created=backup_created
        )

    def _apply_migration_step(self, step: MigrationStep) -> Tuple[int, int, List[str]]:
        """Apply a single migration step"""
        items_migrated = 0
        files_updated = 0
        errors = []

        for agent_dir in self.memory_path.iterdir():
            if not agent_dir.is_dir() or agent_dir.name in ['global', 'config', 'backup']:
                continue

            # Migrate patterns
            patterns_file = agent_dir / 'patterns.json'
            if patterns_file.exists():
                try:
                    patterns = self._load_json(patterns_file)
                    migrated_patterns = [step.migrate_pattern(p) for p in patterns]

                    self._save_json(patterns_file, migrated_patterns)
                    items_migrated += len(migrated_patterns)
                    files_updated += 1

                except Exception as e:
                    error_msg = f"Error migrating patterns for {agent_dir.name}: {e}"
                    logger.error(error_msg)
                    errors.append(error_msg)

            # Migrate solutions
            solutions_file = agent_dir / 'solutions.json'
            if solutions_file.exists():
                try:
                    solutions = self._load_json(solutions_file)
                    migrated_solutions = [step.migrate_solution(s) for s in solutions]

                    self._save_json(solutions_file, migrated_solutions)
                    items_migrated += len(migrated_solutions)
                    files_updated += 1

                except Exception as e:
                    error_msg = f"Error migrating solutions for {agent_dir.name}: {e}"
                    logger.error(error_msg)
                    errors.append(error_msg)

            # Migrate decisions
            decisions_file = agent_dir / 'decisions.json'
            if decisions_file.exists():
                try:
                    decisions = self._load_json(decisions_file)
                    migrated_decisions = [step.migrate_decision(d) for d in decisions]

                    self._save_json(decisions_file, migrated_decisions)
                    items_migrated += len(migrated_decisions)
                    files_updated += 1

                except Exception as e:
                    error_msg = f"Error migrating decisions for {agent_dir.name}: {e}"
                    logger.error(error_msg)
                    errors.append(error_msg)

        return items_migrated, files_updated, errors

    def _build_migration_path(
        self,
        from_version: str,
        to_version: str
    ) -> Optional[List[MigrationStep]]:
        """Build the shortest migration path between versions"""
        path = []
        current = from_version

        # Simple linear path for now
        for migration in self.migrations:
            if migration.can_migrate(current):
                path.append(migration)
                current = migration.to_version.value

                if current == to_version:
                    return path

        return None if path and current != to_version else path

    def _get_latest_version(self) -> str:
        """Get the latest supported version"""
        if self.migrations:
            return self.migrations[-1].to_version.value
        return '1.0.0'

    def _save_version(self, version: str) -> None:
        """Save schema version to file"""
        try:
            self.version_file.parent.mkdir(parents=True, exist_ok=True)

            data = {
                'version': version,
                'updated_at': datetime.now().isoformat(),
                'migration_history': []
            }

            with open(self.version_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)

            logger.info(f"Updated schema version to {version}")

        except Exception as e:
            logger.error(f"Error saving version file: {e}")

    def _load_json(self, file_path: Path) -> List[Dict[str, Any]]:
        """Load JSON file with gzip support"""
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

    def _save_json(self, file_path: Path, data: List[Dict[str, Any]]) -> None:
        """Save JSON file"""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Error saving {file_path}: {e}")


if __name__ == '__main__':
    import sys

    if len(sys.argv) < 3:
        print("Usage: python migration.py <memory_path> <command> [args...]")
        print("Commands:")
        print("  detect              - Detect current schema version")
        print("  migrate-latest      - Migrate to latest version")
        print("  migrate <version>   - Migrate to specific version")
        sys.exit(1)

    memory_path = Path(sys.argv[1])
    command = sys.argv[2]

    manager = MigrationManager(memory_path)

    if command == 'detect':
        version = manager.detect_version()
        print(f"Current schema version: {version}")

    elif command == 'migrate-latest':
        result = manager.migrate_to_latest(backup=True)

        if result.success:
            print(f"Migration successful:")
            print(f"  {result.from_version} -> {result.to_version}")
            print(f"  Items migrated: {result.items_migrated}")
            print(f"  Files updated: {result.files_updated}")
            print(f"  Duration: {result.duration_seconds:.2f}s")
        else:
            print(f"Migration failed:")
            for error in result.errors:
                print(f"  - {error}")
            sys.exit(1)

    elif command == 'migrate':
        if len(sys.argv) < 4:
            print("Error: target version required")
            sys.exit(1)

        current_version = manager.detect_version()
        target_version = sys.argv[3]

        result = manager.migrate(current_version, target_version, backup=True)

        if result.success:
            print(f"Migration successful: {result.items_migrated} items migrated")
        else:
            print(f"Migration failed:")
            for error in result.errors:
                print(f"  - {error}")
            sys.exit(1)

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
