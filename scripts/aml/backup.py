#!/usr/bin/env python3
"""
AML Backup & Restore System

Implements automated backups, incremental backups, point-in-time recovery,
backup rotation, and disaster recovery procedures.

Author: Loom Framework
Version: 1.0.0
"""

import json
import gzip
import shutil
import hashlib
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class BackupType(Enum):
    """Type of backup"""
    FULL = "full"
    INCREMENTAL = "incremental"
    DIFFERENTIAL = "differential"


@dataclass
class BackupMetadata:
    """Metadata for a backup"""
    backup_id: str
    backup_type: BackupType
    timestamp: str
    source_path: str
    backup_path: str
    agents: List[str]
    total_size_bytes: int
    file_count: int
    checksums: Dict[str, str]  # file_path -> sha256 hash
    parent_backup_id: Optional[str] = None  # For incremental backups
    compressed: bool = True
    encrypted: bool = False


@dataclass
class BackupConfig:
    """Configuration for backup operations"""
    backup_root: Path
    retention_days: int = 30
    max_backups: int = 100
    compression_level: int = 9
    incremental_enabled: bool = True
    verify_after_backup: bool = True
    backup_schedule: str = "daily"  # daily, hourly, weekly


@dataclass
class RestoreResult:
    """Result of a restore operation"""
    success: bool
    restored_files: int
    total_size_bytes: int
    errors: List[str]
    duration_seconds: float


class BackupManager:
    """
    Manages automated backups with incremental support and rotation.

    Features:
    - Full and incremental backups
    - Point-in-time recovery
    - Automatic rotation (30 days retention)
    - Backup verification with checksums
    - Disaster recovery procedures
    """

    def __init__(self, memory_path: Path, config: Optional[BackupConfig] = None):
        """
        Initialize backup manager.

        Args:
            memory_path: Path to .loom/memory directory
            config: Backup configuration (uses defaults if not provided)
        """
        self.memory_path = Path(memory_path)
        self.config = config or BackupConfig(
            backup_root=self.memory_path.parent / 'memory-backup'
        )

        # Ensure backup directory exists
        self.config.backup_root.mkdir(parents=True, exist_ok=True)

        # Metadata file
        self.metadata_file = self.config.backup_root / 'backup_metadata.json'
        self.backups: Dict[str, BackupMetadata] = {}
        self._load_metadata()

    def create_full_backup(
        self,
        agents: Optional[List[str]] = None,
        description: str = ""
    ) -> BackupMetadata:
        """
        Create a full backup of memory data.

        Args:
            agents: Specific agents to backup (all if None)
            description: Optional description for this backup

        Returns:
            BackupMetadata object
        """
        logger.info("Creating full backup...")
        start_time = datetime.now()

        # Generate backup ID
        backup_id = f"full_{start_time.strftime('%Y%m%d_%H%M%S')}"
        backup_dir = self.config.backup_root / backup_id
        backup_dir.mkdir(parents=True, exist_ok=True)

        # Get agents to backup
        agents_to_backup = agents or self._get_all_agents()

        # Track backup stats
        file_count = 0
        total_size = 0
        checksums = {}

        # Backup each agent
        for agent in agents_to_backup:
            agent_src = self.memory_path / agent
            if not agent_src.exists():
                logger.warning(f"Agent directory not found: {agent}")
                continue

            agent_dst = backup_dir / agent
            agent_dst.mkdir(parents=True, exist_ok=True)

            # Backup agent files
            for file_name in ['patterns.json', 'solutions.json', 'decisions.json', 'metrics.json', 'context.json', 'index.json']:
                src_file = agent_src / file_name
                if not src_file.exists():
                    continue

                # Copy and compress
                dst_file = agent_dst / f"{file_name}.gz"
                checksum = self._copy_and_compress(src_file, dst_file)

                if checksum:
                    checksums[f"{agent}/{file_name}"] = checksum
                    file_count += 1
                    total_size += dst_file.stat().st_size

        # Backup global data
        global_src = self.memory_path / 'global'
        if global_src.exists():
            global_dst = backup_dir / 'global'
            global_dst.mkdir(parents=True, exist_ok=True)

            for file_path in global_src.glob('*'):
                if file_path.is_file():
                    dst_file = global_dst / f"{file_path.name}.gz"
                    checksum = self._copy_and_compress(file_path, dst_file)

                    if checksum:
                        checksums[f"global/{file_path.name}"] = checksum
                        file_count += 1
                        total_size += dst_file.stat().st_size

        # Create metadata
        metadata = BackupMetadata(
            backup_id=backup_id,
            backup_type=BackupType.FULL,
            timestamp=start_time.isoformat(),
            source_path=str(self.memory_path),
            backup_path=str(backup_dir),
            agents=agents_to_backup,
            total_size_bytes=total_size,
            file_count=file_count,
            checksums=checksums,
            compressed=True
        )

        # Save metadata
        self.backups[backup_id] = metadata
        self._save_metadata()

        # Verify backup if enabled
        if self.config.verify_after_backup:
            if not self._verify_backup(metadata):
                logger.error("Backup verification failed!")
                raise RuntimeError("Backup verification failed")

        duration = (datetime.now() - start_time).total_seconds()
        logger.info(f"Full backup complete: {file_count} files, {total_size / 1024 / 1024:.2f}MB in {duration:.2f}s")

        return metadata

    def create_incremental_backup(self, base_backup_id: Optional[str] = None) -> BackupMetadata:
        """
        Create an incremental backup (only changed files since last backup).

        Args:
            base_backup_id: ID of base backup (uses latest if None)

        Returns:
            BackupMetadata object
        """
        logger.info("Creating incremental backup...")
        start_time = datetime.now()

        # Find base backup
        if base_backup_id:
            if base_backup_id not in self.backups:
                raise ValueError(f"Base backup not found: {base_backup_id}")
            base_backup = self.backups[base_backup_id]
        else:
            # Use latest full backup
            base_backup = self._get_latest_full_backup()
            if not base_backup:
                logger.warning("No full backup found, creating full backup instead")
                return self.create_full_backup()

        # Generate backup ID
        backup_id = f"incr_{start_time.strftime('%Y%m%d_%H%M%S')}"
        backup_dir = self.config.backup_root / backup_id
        backup_dir.mkdir(parents=True, exist_ok=True)

        # Track backup stats
        file_count = 0
        total_size = 0
        checksums = {}

        # Backup only changed files
        for agent in base_backup.agents:
            agent_src = self.memory_path / agent
            if not agent_src.exists():
                continue

            for file_name in ['patterns.json', 'solutions.json', 'decisions.json', 'metrics.json', 'context.json', 'index.json']:
                src_file = agent_src / file_name
                if not src_file.exists():
                    continue

                # Calculate current checksum
                current_checksum = self._calculate_checksum(src_file)
                base_checksum = base_backup.checksums.get(f"{agent}/{file_name}")

                # Only backup if changed
                if current_checksum != base_checksum:
                    agent_dst = backup_dir / agent
                    agent_dst.mkdir(parents=True, exist_ok=True)

                    dst_file = agent_dst / f"{file_name}.gz"
                    checksum = self._copy_and_compress(src_file, dst_file)

                    if checksum:
                        checksums[f"{agent}/{file_name}"] = checksum
                        file_count += 1
                        total_size += dst_file.stat().st_size

        # Create metadata
        metadata = BackupMetadata(
            backup_id=backup_id,
            backup_type=BackupType.INCREMENTAL,
            timestamp=start_time.isoformat(),
            source_path=str(self.memory_path),
            backup_path=str(backup_dir),
            agents=base_backup.agents,
            total_size_bytes=total_size,
            file_count=file_count,
            checksums=checksums,
            parent_backup_id=base_backup.backup_id,
            compressed=True
        )

        # Save metadata
        self.backups[backup_id] = metadata
        self._save_metadata()

        duration = (datetime.now() - start_time).total_seconds()
        logger.info(f"Incremental backup complete: {file_count} files, {total_size / 1024 / 1024:.2f}MB in {duration:.2f}s")

        return metadata

    def restore_backup(
        self,
        backup_id: str,
        target_path: Optional[Path] = None,
        agents: Optional[List[str]] = None,
        dry_run: bool = False
    ) -> RestoreResult:
        """
        Restore memory from a backup.

        Args:
            backup_id: ID of backup to restore
            target_path: Path to restore to (uses original path if None)
            agents: Specific agents to restore (all if None)
            dry_run: If True, don't actually restore files

        Returns:
            RestoreResult object
        """
        logger.info(f"Restoring backup: {backup_id}")
        start_time = datetime.now()

        if backup_id not in self.backups:
            raise ValueError(f"Backup not found: {backup_id}")

        metadata = self.backups[backup_id]
        target = Path(target_path) if target_path else self.memory_path

        errors = []
        restored_count = 0
        total_size = 0

        # Build restore chain for incremental backups
        restore_chain = self._build_restore_chain(backup_id)

        # Filter agents if specified
        agents_to_restore = agents or metadata.agents

        # Restore files in order (base first, then incrementals)
        for chain_id in restore_chain:
            chain_metadata = self.backups[chain_id]
            backup_dir = Path(chain_metadata.backup_path)

            for agent in agents_to_restore:
                agent_backup = backup_dir / agent
                if not agent_backup.exists():
                    continue

                agent_target = target / agent
                if not dry_run:
                    agent_target.mkdir(parents=True, exist_ok=True)

                # Restore agent files
                for backup_file in agent_backup.glob('*.gz'):
                    target_file = agent_target / backup_file.stem  # Remove .gz

                    try:
                        if not dry_run:
                            self._decompress_and_copy(backup_file, target_file)

                        restored_count += 1
                        total_size += backup_file.stat().st_size

                    except Exception as e:
                        error_msg = f"Error restoring {backup_file}: {e}"
                        logger.error(error_msg)
                        errors.append(error_msg)

            # Restore global data
            global_backup = backup_dir / 'global'
            if global_backup.exists():
                global_target = target / 'global'
                if not dry_run:
                    global_target.mkdir(parents=True, exist_ok=True)

                for backup_file in global_backup.glob('*.gz'):
                    target_file = global_target / backup_file.stem

                    try:
                        if not dry_run:
                            self._decompress_and_copy(backup_file, target_file)

                        restored_count += 1
                        total_size += backup_file.stat().st_size

                    except Exception as e:
                        error_msg = f"Error restoring {backup_file}: {e}"
                        logger.error(error_msg)
                        errors.append(error_msg)

        duration = (datetime.now() - start_time).total_seconds()
        success = len(errors) == 0

        logger.info(f"Restore {'complete' if success else 'completed with errors'}: {restored_count} files, {total_size / 1024 / 1024:.2f}MB in {duration:.2f}s")

        return RestoreResult(
            success=success,
            restored_files=restored_count,
            total_size_bytes=total_size,
            errors=errors,
            duration_seconds=duration
        )

    def point_in_time_restore(
        self,
        target_datetime: datetime,
        target_path: Optional[Path] = None
    ) -> RestoreResult:
        """
        Restore memory to a specific point in time.

        Args:
            target_datetime: Datetime to restore to
            target_path: Path to restore to (uses original path if None)

        Returns:
            RestoreResult object
        """
        logger.info(f"Point-in-time restore to {target_datetime.isoformat()}")

        # Find latest backup before target time
        target_backup = None
        target_timestamp = target_datetime.timestamp()

        for backup_id, metadata in self.backups.items():
            backup_time = datetime.fromisoformat(metadata.timestamp).timestamp()

            if backup_time <= target_timestamp:
                if not target_backup or backup_time > datetime.fromisoformat(target_backup.timestamp).timestamp():
                    target_backup = metadata

        if not target_backup:
            raise ValueError(f"No backup found before {target_datetime.isoformat()}")

        logger.info(f"Using backup: {target_backup.backup_id} from {target_backup.timestamp}")

        return self.restore_backup(target_backup.backup_id, target_path)

    def rotate_backups(self) -> int:
        """
        Remove old backups based on retention policy.

        Returns:
            Number of backups deleted
        """
        logger.info("Rotating backups...")

        cutoff_date = datetime.now() - timedelta(days=self.config.retention_days)
        to_delete = []

        # Find backups older than retention period
        for backup_id, metadata in self.backups.items():
            backup_time = datetime.fromisoformat(metadata.timestamp)

            if backup_time < cutoff_date:
                to_delete.append(backup_id)

        # Keep at least the most recent full backup
        if to_delete:
            latest_full = self._get_latest_full_backup()
            if latest_full and latest_full.backup_id in to_delete:
                to_delete.remove(latest_full.backup_id)

        # Delete old backups
        deleted_count = 0
        for backup_id in to_delete:
            try:
                metadata = self.backups[backup_id]
                backup_dir = Path(metadata.backup_path)

                if backup_dir.exists():
                    shutil.rmtree(backup_dir)

                del self.backups[backup_id]
                deleted_count += 1

                logger.info(f"Deleted backup: {backup_id}")

            except Exception as e:
                logger.error(f"Error deleting backup {backup_id}: {e}")

        # Save updated metadata
        self._save_metadata()

        logger.info(f"Rotation complete: deleted {deleted_count} backups")
        return deleted_count

    def list_backups(self) -> List[BackupMetadata]:
        """List all available backups"""
        return sorted(
            self.backups.values(),
            key=lambda m: m.timestamp,
            reverse=True
        )

    def get_backup_info(self, backup_id: str) -> Optional[BackupMetadata]:
        """Get metadata for a specific backup"""
        return self.backups.get(backup_id)

    def verify_backup(self, backup_id: str) -> bool:
        """Verify backup integrity using checksums"""
        if backup_id not in self.backups:
            logger.error(f"Backup not found: {backup_id}")
            return False

        return self._verify_backup(self.backups[backup_id])

    # Helper methods

    def _get_all_agents(self) -> List[str]:
        """Get list of all agents in memory"""
        agents = []
        for item in self.memory_path.iterdir():
            if item.is_dir() and item.name not in ['global', 'config', 'backup']:
                agents.append(item.name)
        return agents

    def _copy_and_compress(self, src: Path, dst: Path) -> str:
        """Copy and compress a file, return checksum"""
        try:
            # Read source
            with open(src, 'rb') as f_in:
                data = f_in.read()

            # Calculate checksum
            checksum = hashlib.sha256(data).hexdigest()

            # Write compressed
            with gzip.open(dst, 'wb', compresslevel=self.config.compression_level) as f_out:
                f_out.write(data)

            return checksum

        except Exception as e:
            logger.error(f"Error copying {src} -> {dst}: {e}")
            return ""

    def _decompress_and_copy(self, src: Path, dst: Path) -> None:
        """Decompress and copy a file"""
        with gzip.open(src, 'rb') as f_in:
            with open(dst, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)

    def _calculate_checksum(self, file_path: Path) -> str:
        """Calculate SHA-256 checksum of a file"""
        sha256 = hashlib.sha256()

        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(8192), b''):
                sha256.update(chunk)

        return sha256.hexdigest()

    def _verify_backup(self, metadata: BackupMetadata) -> bool:
        """Verify backup integrity"""
        logger.info(f"Verifying backup: {metadata.backup_id}")

        backup_dir = Path(metadata.backup_path)
        errors = 0

        for file_path, expected_checksum in metadata.checksums.items():
            parts = file_path.split('/')
            backup_file = backup_dir / parts[0] / f"{parts[1]}.gz"

            if not backup_file.exists():
                logger.error(f"Missing file in backup: {file_path}")
                errors += 1
                continue

            # Decompress and calculate checksum
            try:
                with gzip.open(backup_file, 'rb') as f:
                    data = f.read()
                    actual_checksum = hashlib.sha256(data).hexdigest()

                if actual_checksum != expected_checksum:
                    logger.error(f"Checksum mismatch for {file_path}")
                    errors += 1

            except Exception as e:
                logger.error(f"Error verifying {file_path}: {e}")
                errors += 1

        if errors == 0:
            logger.info("Backup verification successful")
            return True
        else:
            logger.error(f"Backup verification failed: {errors} errors")
            return False

    def _get_latest_full_backup(self) -> Optional[BackupMetadata]:
        """Get the most recent full backup"""
        full_backups = [
            m for m in self.backups.values()
            if m.backup_type == BackupType.FULL
        ]

        if not full_backups:
            return None

        return max(full_backups, key=lambda m: m.timestamp)

    def _build_restore_chain(self, backup_id: str) -> List[str]:
        """Build chain of backups needed for restore (base + incrementals)"""
        chain = [backup_id]
        current_id = backup_id

        # Walk back to base backup
        while True:
            metadata = self.backups[current_id]

            if metadata.backup_type == BackupType.FULL:
                break

            if metadata.parent_backup_id:
                chain.insert(0, metadata.parent_backup_id)
                current_id = metadata.parent_backup_id
            else:
                break

        return chain

    def _load_metadata(self) -> None:
        """Load backup metadata from disk"""
        if not self.metadata_file.exists():
            return

        try:
            with open(self.metadata_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            for backup_data in data.get('backups', []):
                backup_data['backup_type'] = BackupType(backup_data['backup_type'])
                metadata = BackupMetadata(**backup_data)
                self.backups[metadata.backup_id] = metadata

            logger.info(f"Loaded metadata for {len(self.backups)} backups")

        except Exception as e:
            logger.error(f"Error loading metadata: {e}")

    def _save_metadata(self) -> None:
        """Save backup metadata to disk"""
        try:
            data = {
                'version': '1.0.0',
                'backups': []
            }

            for metadata in self.backups.values():
                backup_data = asdict(metadata)
                backup_data['backup_type'] = metadata.backup_type.value
                data['backups'].append(backup_data)

            with open(self.metadata_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

        except Exception as e:
            logger.error(f"Error saving metadata: {e}")


def automated_backup_job(memory_path: Path, config: Optional[BackupConfig] = None) -> None:
    """
    Automated backup job (run via cron or scheduler).

    Creates incremental backups and rotates old backups.
    """
    manager = BackupManager(memory_path, config)

    try:
        # Create incremental backup (or full if no base exists)
        if manager.config.incremental_enabled:
            metadata = manager.create_incremental_backup()
        else:
            metadata = manager.create_full_backup()

        logger.info(f"Backup complete: {metadata.backup_id}")

        # Rotate old backups
        deleted = manager.rotate_backups()
        logger.info(f"Rotated {deleted} old backups")

    except Exception as e:
        logger.error(f"Backup job failed: {e}")
        raise


if __name__ == '__main__':
    import sys

    if len(sys.argv) < 3:
        print("Usage: python backup.py <memory_path> <command> [args...]")
        print("Commands:")
        print("  full                    - Create full backup")
        print("  incremental             - Create incremental backup")
        print("  restore <backup_id>     - Restore from backup")
        print("  list                    - List all backups")
        print("  rotate                  - Rotate old backups")
        print("  verify <backup_id>      - Verify backup integrity")
        print("  auto                    - Run automated backup job")
        sys.exit(1)

    memory_path = Path(sys.argv[1])
    command = sys.argv[2]

    manager = BackupManager(memory_path)

    if command == 'full':
        metadata = manager.create_full_backup()
        print(f"Full backup created: {metadata.backup_id}")
        print(f"  Files: {metadata.file_count}")
        print(f"  Size: {metadata.total_size_bytes / 1024 / 1024:.2f}MB")

    elif command == 'incremental':
        metadata = manager.create_incremental_backup()
        print(f"Incremental backup created: {metadata.backup_id}")
        print(f"  Files: {metadata.file_count}")
        print(f"  Size: {metadata.total_size_bytes / 1024 / 1024:.2f}MB")

    elif command == 'restore':
        if len(sys.argv) < 4:
            print("Error: backup_id required")
            sys.exit(1)

        backup_id = sys.argv[3]
        result = manager.restore_backup(backup_id, dry_run=False)

        if result.success:
            print(f"Restore successful: {result.restored_files} files")
        else:
            print(f"Restore completed with errors:")
            for error in result.errors:
                print(f"  - {error}")

    elif command == 'list':
        backups = manager.list_backups()
        print(f"Found {len(backups)} backups:")
        for backup in backups:
            print(f"  {backup.backup_id} ({backup.backup_type.value}) - {backup.timestamp}")
            print(f"    Files: {backup.file_count}, Size: {backup.total_size_bytes / 1024 / 1024:.2f}MB")

    elif command == 'rotate':
        deleted = manager.rotate_backups()
        print(f"Rotated {deleted} old backups")

    elif command == 'verify':
        if len(sys.argv) < 4:
            print("Error: backup_id required")
            sys.exit(1)

        backup_id = sys.argv[3]
        if manager.verify_backup(backup_id):
            print("Backup verification successful")
        else:
            print("Backup verification FAILED")
            sys.exit(1)

    elif command == 'auto':
        automated_backup_job(memory_path)

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
