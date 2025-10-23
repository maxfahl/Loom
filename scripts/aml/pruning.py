#!/usr/bin/env python3
"""
AML Memory Pruning System

Implements time-based, performance-based, and space-based pruning strategies
to maintain optimal memory usage while preserving valuable patterns.

Author: Loom Framework
Version: 1.0.0
"""

import json
import gzip
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass, asdict
from enum import Enum


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class PruneStrategy(Enum):
    """Pruning strategy types"""
    TIME_BASED = "time_based"
    PERFORMANCE_BASED = "performance_based"
    SPACE_BASED = "space_based"
    MANUAL = "manual"


class PruneReason(Enum):
    """Reason for pruning a memory item"""
    UNUSED_TOO_LONG = "unused_too_long"
    LOW_SUCCESS_RATE = "low_success_rate"
    NEGATIVE_OUTCOME = "negative_outcome"
    OUTDATED_SOLUTION = "outdated_solution"
    MEMORY_LIMIT_EXCEEDED = "memory_limit_exceeded"
    LOW_CONFIDENCE = "low_confidence"
    FAILED_VALIDATION = "failed_validation"
    MANUAL_DELETION = "manual_deletion"


@dataclass
class PruneConfig:
    """Configuration for pruning operations"""
    # Time-based thresholds (in days)
    pattern_max_age_days: int = 90
    decision_max_age_days: int = 180
    failed_pattern_max_age_days: int = 30
    solution_max_age_days: int = 365

    # Performance-based thresholds
    min_success_rate: float = 0.20
    min_confidence_score: float = 0.15
    min_execution_count: int = 3

    # Space-based thresholds (in bytes)
    agent_memory_limit: int = 80 * 1024 * 1024  # 80MB
    global_memory_limit: int = 800 * 1024 * 1024  # 800MB

    # Safety settings
    preserve_high_value: bool = True
    high_value_threshold: float = 0.85
    dry_run: bool = False
    create_backup: bool = True


@dataclass
class PruneResult:
    """Result of a pruning operation"""
    strategy: PruneStrategy
    agent: Optional[str]
    items_pruned: int
    items_archived: int
    items_compressed: int
    space_freed_bytes: int
    duration_seconds: float
    errors: List[str]
    summary: Dict[PruneReason, int]

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        result = asdict(self)
        result['strategy'] = self.strategy.value
        result['summary'] = {k.value: v for k, v in self.summary.items()}
        return result


@dataclass
class MemoryItem:
    """Generic memory item (pattern, solution, or decision)"""
    id: str
    agent: str
    item_type: str  # 'pattern', 'solution', 'decision'
    timestamp: datetime
    last_used: Optional[datetime]
    success_rate: Optional[float]
    confidence_score: Optional[float]
    execution_count: Optional[int]
    size_bytes: int
    active: bool
    data: Dict[str, Any]


class MemoryPruner:
    """
    Core pruning engine that implements all pruning strategies.

    This class provides intelligent memory management by identifying
    and removing low-value patterns, outdated solutions, and failed
    decisions while preserving high-value learning data.
    """

    def __init__(self, memory_path: Path, config: Optional[PruneConfig] = None):
        """
        Initialize the memory pruner.

        Args:
            memory_path: Path to .loom/memory directory
            config: Pruning configuration (uses defaults if not provided)
        """
        self.memory_path = Path(memory_path)
        self.config = config or PruneConfig()
        self.backup_path = self.memory_path.parent / 'memory-backup'

        # Statistics tracking
        self.stats = {
            'total_items_scanned': 0,
            'total_items_pruned': 0,
            'total_space_freed': 0,
            'errors': []
        }

    def prune_all(
        self,
        strategies: List[PruneStrategy],
        agent_filter: Optional[List[str]] = None
    ) -> List[PruneResult]:
        """
        Execute multiple pruning strategies across all agents.

        Args:
            strategies: List of pruning strategies to apply
            agent_filter: Optional list of agents to process (all if None)

        Returns:
            List of PruneResult objects for each strategy applied
        """
        results = []
        agents = self._get_agents(agent_filter)

        logger.info(f"Starting pruning with strategies: {[s.value for s in strategies]}")
        logger.info(f"Processing {len(agents)} agents")

        for strategy in strategies:
            if strategy == PruneStrategy.TIME_BASED:
                result = self._prune_time_based(agents)
            elif strategy == PruneStrategy.PERFORMANCE_BASED:
                result = self._prune_performance_based(agents)
            elif strategy == PruneStrategy.SPACE_BASED:
                result = self._prune_space_based(agents)
            else:
                logger.warning(f"Unknown strategy: {strategy}")
                continue

            results.append(result)
            logger.info(f"Strategy {strategy.value}: pruned {result.items_pruned} items, freed {result.space_freed_bytes / 1024 / 1024:.2f}MB")

        return results

    def _prune_time_based(self, agents: List[str]) -> PruneResult:
        """
        Prune based on time thresholds.

        Removes:
        - Patterns unused for >90 days
        - Decisions older than 6 months
        - Failed patterns after 30 days
        """
        start_time = datetime.now()
        items_pruned = 0
        items_archived = 0
        space_freed = 0
        errors = []
        summary: Dict[PruneReason, int] = {}

        now = datetime.now()

        for agent in agents:
            agent_path = self.memory_path / agent
            if not agent_path.exists():
                continue

            try:
                # Process patterns
                patterns_file = agent_path / 'patterns.json'
                if patterns_file.exists():
                    patterns = self._load_json(patterns_file)
                    original_count = len(patterns)
                    original_size = patterns_file.stat().st_size

                    patterns, pruned = self._filter_by_time(
                        patterns,
                        'pattern',
                        now,
                        self.config.pattern_max_age_days,
                        PruneReason.UNUSED_TOO_LONG
                    )

                    if pruned:
                        items_pruned += len(pruned)
                        summary[PruneReason.UNUSED_TOO_LONG] = summary.get(PruneReason.UNUSED_TOO_LONG, 0) + len(pruned)

                        if not self.config.dry_run:
                            self._save_json(patterns_file, patterns)
                            space_freed += original_size - patterns_file.stat().st_size

                # Process decisions
                decisions_file = agent_path / 'decisions.json'
                if decisions_file.exists():
                    decisions = self._load_json(decisions_file)
                    original_size = decisions_file.stat().st_size

                    decisions, pruned = self._filter_by_time(
                        decisions,
                        'decision',
                        now,
                        self.config.decision_max_age_days,
                        PruneReason.UNUSED_TOO_LONG
                    )

                    if pruned:
                        # Archive old decisions instead of deleting
                        if not self.config.dry_run:
                            self._archive_items(agent, 'decisions', pruned)
                        items_archived += len(pruned)

                        if not self.config.dry_run:
                            self._save_json(decisions_file, decisions)
                            space_freed += original_size - decisions_file.stat().st_size

                # Process failed patterns (more aggressive)
                if patterns_file.exists():
                    patterns = self._load_json(patterns_file)
                    original_size = patterns_file.stat().st_size

                    patterns, pruned = self._filter_failed_patterns(
                        patterns,
                        now,
                        self.config.failed_pattern_max_age_days
                    )

                    if pruned:
                        items_pruned += len(pruned)
                        summary[PruneReason.LOW_SUCCESS_RATE] = summary.get(PruneReason.LOW_SUCCESS_RATE, 0) + len(pruned)

                        if not self.config.dry_run:
                            self._save_json(patterns_file, patterns)
                            space_freed += original_size - patterns_file.stat().st_size

            except Exception as e:
                error_msg = f"Error pruning {agent}: {str(e)}"
                logger.error(error_msg)
                errors.append(error_msg)

        duration = (datetime.now() - start_time).total_seconds()

        return PruneResult(
            strategy=PruneStrategy.TIME_BASED,
            agent=None,
            items_pruned=items_pruned,
            items_archived=items_archived,
            items_compressed=0,
            space_freed_bytes=space_freed,
            duration_seconds=duration,
            errors=errors,
            summary=summary
        )

    def _prune_performance_based(self, agents: List[str]) -> PruneResult:
        """
        Prune based on performance metrics.

        Removes:
        - Patterns with <20% success rate
        - Solutions that no longer apply
        - Decisions with negative outcomes
        """
        start_time = datetime.now()
        items_pruned = 0
        items_archived = 0
        space_freed = 0
        errors = []
        summary: Dict[PruneReason, int] = {}

        for agent in agents:
            agent_path = self.memory_path / agent
            if not agent_path.exists():
                continue

            try:
                # Process patterns
                patterns_file = agent_path / 'patterns.json'
                if patterns_file.exists():
                    patterns = self._load_json(patterns_file)
                    original_size = patterns_file.stat().st_size

                    filtered_patterns = []
                    pruned_count = 0

                    for pattern in patterns:
                        if self._should_prune_by_performance(pattern, 'pattern'):
                            pruned_count += 1
                            reason = self._get_prune_reason(pattern, 'pattern')
                            summary[reason] = summary.get(reason, 0) + 1
                        else:
                            filtered_patterns.append(pattern)

                    if pruned_count > 0:
                        items_pruned += pruned_count

                        if not self.config.dry_run:
                            self._save_json(patterns_file, filtered_patterns)
                            space_freed += original_size - patterns_file.stat().st_size

                # Process solutions
                solutions_file = agent_path / 'solutions.json'
                if solutions_file.exists():
                    solutions = self._load_json(solutions_file)
                    original_size = solutions_file.stat().st_size

                    filtered_solutions = []
                    pruned_count = 0

                    for solution in solutions:
                        if self._should_prune_by_performance(solution, 'solution'):
                            pruned_count += 1
                            summary[PruneReason.OUTDATED_SOLUTION] = summary.get(PruneReason.OUTDATED_SOLUTION, 0) + 1
                        else:
                            filtered_solutions.append(solution)

                    if pruned_count > 0:
                        items_pruned += pruned_count

                        if not self.config.dry_run:
                            self._save_json(solutions_file, filtered_solutions)
                            space_freed += original_size - solutions_file.stat().st_size

                # Process decisions with negative outcomes
                decisions_file = agent_path / 'decisions.json'
                if decisions_file.exists():
                    decisions = self._load_json(decisions_file)
                    original_size = decisions_file.stat().st_size

                    filtered_decisions = []
                    archived = []

                    for decision in decisions:
                        if self._has_negative_outcome(decision):
                            archived.append(decision)
                            summary[PruneReason.NEGATIVE_OUTCOME] = summary.get(PruneReason.NEGATIVE_OUTCOME, 0) + 1
                        else:
                            filtered_decisions.append(decision)

                    if archived:
                        if not self.config.dry_run:
                            self._archive_items(agent, 'negative_decisions', archived)
                        items_archived += len(archived)

                        if not self.config.dry_run:
                            self._save_json(decisions_file, filtered_decisions)
                            space_freed += original_size - decisions_file.stat().st_size

            except Exception as e:
                error_msg = f"Error in performance-based pruning for {agent}: {str(e)}"
                logger.error(error_msg)
                errors.append(error_msg)

        duration = (datetime.now() - start_time).total_seconds()

        return PruneResult(
            strategy=PruneStrategy.PERFORMANCE_BASED,
            agent=None,
            items_pruned=items_pruned,
            items_archived=items_archived,
            items_compressed=0,
            space_freed_bytes=space_freed,
            duration_seconds=duration,
            errors=errors,
            summary=summary
        )

    def _prune_space_based(self, agents: List[str]) -> PruneResult:
        """
        Prune based on space constraints.

        Triggers when:
        - Agent memory >80MB
        - Global memory >800MB

        Actions:
        - Remove lowest confidence patterns first
        - Compress old decisions
        """
        start_time = datetime.now()
        items_pruned = 0
        items_compressed = 0
        space_freed = 0
        errors = []
        summary: Dict[PruneReason, int] = {}

        # Check global memory usage
        total_size = self._get_total_size()
        global_limit_exceeded = total_size > self.config.global_memory_limit

        if global_limit_exceeded:
            logger.warning(f"Global memory limit exceeded: {total_size / 1024 / 1024:.2f}MB / {self.config.global_memory_limit / 1024 / 1024:.2f}MB")

        for agent in agents:
            agent_path = self.memory_path / agent
            if not agent_path.exists():
                continue

            try:
                agent_size = self._get_directory_size(agent_path)
                agent_limit_exceeded = agent_size > self.config.agent_memory_limit

                if agent_limit_exceeded or global_limit_exceeded:
                    logger.info(f"Pruning {agent}: {agent_size / 1024 / 1024:.2f}MB")

                    # Calculate how much space we need to free
                    if agent_limit_exceeded:
                        target_reduction = agent_size - (self.config.agent_memory_limit * 0.7)  # Free to 70% of limit
                    else:
                        # Proportional reduction for global limit
                        target_reduction = agent_size * 0.2  # Remove 20%

                    space_freed_agent = 0

                    # Step 1: Compress old decisions
                    decisions_file = agent_path / 'decisions.json'
                    if decisions_file.exists() and decisions_file.suffix != '.gz':
                        original_size = decisions_file.stat().st_size
                        if not self.config.dry_run:
                            self._compress_file(decisions_file)
                        compressed_size = (agent_path / 'decisions.json.gz').stat().st_size if not self.config.dry_run else original_size // 3
                        space_freed_agent += original_size - compressed_size
                        items_compressed += 1

                    # Step 2: Remove low-confidence patterns
                    if space_freed_agent < target_reduction:
                        patterns_file = agent_path / 'patterns.json'
                        if patterns_file.exists():
                            patterns = self._load_json(patterns_file)
                            original_size = patterns_file.stat().st_size

                            # Sort by confidence/value score
                            patterns_with_scores = [(p, self._calculate_value_score(p)) for p in patterns]
                            patterns_with_scores.sort(key=lambda x: x[1], reverse=True)

                            # Remove lowest value patterns until we hit target
                            kept_patterns = []
                            current_freed = 0
                            bytes_per_pattern = original_size / len(patterns) if patterns else 0

                            for pattern, score in patterns_with_scores:
                                # Preserve high-value patterns
                                if self.config.preserve_high_value and score >= self.config.high_value_threshold:
                                    kept_patterns.append(pattern)
                                elif current_freed < (target_reduction - space_freed_agent):
                                    current_freed += bytes_per_pattern
                                    items_pruned += 1
                                    summary[PruneReason.MEMORY_LIMIT_EXCEEDED] = summary.get(PruneReason.MEMORY_LIMIT_EXCEEDED, 0) + 1
                                else:
                                    kept_patterns.append(pattern)

                            if not self.config.dry_run:
                                self._save_json(patterns_file, kept_patterns)

                            space_freed_agent += original_size - (len(kept_patterns) * bytes_per_pattern)

                    space_freed += int(space_freed_agent)

            except Exception as e:
                error_msg = f"Error in space-based pruning for {agent}: {str(e)}"
                logger.error(error_msg)
                errors.append(error_msg)

        duration = (datetime.now() - start_time).total_seconds()

        return PruneResult(
            strategy=PruneStrategy.SPACE_BASED,
            agent=None,
            items_pruned=items_pruned,
            items_archived=0,
            items_compressed=items_compressed,
            space_freed_bytes=space_freed,
            duration_seconds=duration,
            errors=errors,
            summary=summary
        )

    # Helper methods

    def _get_agents(self, agent_filter: Optional[List[str]] = None) -> List[str]:
        """Get list of agents to process"""
        all_agents = [d.name for d in self.memory_path.iterdir() if d.is_dir() and d.name != 'global' and d.name != 'config']

        if agent_filter:
            return [a for a in all_agents if a in agent_filter]
        return all_agents

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
        """Save JSON file with pretty printing"""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Error saving {file_path}: {e}")
            raise

    def _compress_file(self, file_path: Path) -> None:
        """Compress a file using gzip"""
        try:
            compressed_path = file_path.with_suffix(file_path.suffix + '.gz')

            with open(file_path, 'rb') as f_in:
                with gzip.open(compressed_path, 'wb', compresslevel=9) as f_out:
                    f_out.writelines(f_in)

            # Remove original file
            file_path.unlink()
            logger.info(f"Compressed {file_path.name} -> {compressed_path.name}")

        except Exception as e:
            logger.error(f"Error compressing {file_path}: {e}")
            raise

    def _filter_by_time(
        self,
        items: List[Dict[str, Any]],
        item_type: str,
        now: datetime,
        max_age_days: int,
        reason: PruneReason
    ) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        """Filter items by age"""
        kept = []
        pruned = []

        for item in items:
            last_used = self._get_last_used_date(item)
            age_days = (now - last_used).days if last_used else 999

            if age_days > max_age_days:
                pruned.append(item)
            else:
                kept.append(item)

        return kept, pruned

    def _filter_failed_patterns(
        self,
        patterns: List[Dict[str, Any]],
        now: datetime,
        max_age_days: int
    ) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        """Filter patterns that have consistently failed"""
        kept = []
        pruned = []

        for pattern in patterns:
            metrics = pattern.get('metrics', {})
            success_rate = metrics.get('successRate', 1.0)
            execution_count = metrics.get('executionCount', 0)

            # Must have enough data to judge
            if execution_count >= self.config.min_execution_count:
                if success_rate < 0.3:  # Failed pattern threshold
                    created = self._parse_timestamp(pattern.get('timestamp'))
                    if created and (now - created).days > max_age_days:
                        pruned.append(pattern)
                        continue

            kept.append(pattern)

        return kept, pruned

    def _should_prune_by_performance(self, item: Dict[str, Any], item_type: str) -> bool:
        """Determine if item should be pruned based on performance"""
        if item_type == 'pattern':
            metrics = item.get('metrics', {})
            evolution = item.get('evolution', {})

            success_rate = metrics.get('successRate', 1.0)
            confidence = evolution.get('confidenceScore', 1.0)
            execution_count = metrics.get('executionCount', 0)

            # Need enough data to judge
            if execution_count < self.config.min_execution_count:
                return False

            # Check if performance is too low
            if success_rate < self.config.min_success_rate:
                return True

            # Check if confidence is too low
            if confidence < self.config.min_confidence_score:
                return True

        elif item_type == 'solution':
            effectiveness = item.get('effectiveness', {})
            worked = effectiveness.get('worked', True)

            # Remove solutions that didn't work
            if not worked:
                return True

        return False

    def _has_negative_outcome(self, decision: Dict[str, Any]) -> bool:
        """Check if a decision had a negative outcome"""
        outcome = decision.get('outcome', {})
        would_repeat = outcome.get('would_repeat', True)

        # Check if there are negative success metrics
        success_metrics = outcome.get('success_metrics', {})
        if success_metrics:
            avg_metric = sum(success_metrics.values()) / len(success_metrics)
            if avg_metric < 0.5:
                return True

        return not would_repeat

    def _calculate_value_score(self, pattern: Dict[str, Any]) -> float:
        """Calculate overall value score for a pattern"""
        metrics = pattern.get('metrics', {})
        evolution = pattern.get('evolution', {})

        success_rate = metrics.get('successRate', 0.5)
        confidence = evolution.get('confidenceScore', 0.3)
        execution_count = metrics.get('executionCount', 1)
        time_saved = metrics.get('avgTimeSavedMs', 0)

        # Weighted value score
        base_value = success_rate * 0.4
        confidence_value = confidence * 0.3
        usage_value = min(execution_count / 50, 1.0) * 0.2
        time_value = min(time_saved / 1000, 1.0) * 0.1

        return base_value + confidence_value + usage_value + time_value

    def _get_prune_reason(self, item: Dict[str, Any], item_type: str) -> PruneReason:
        """Determine the reason for pruning"""
        if item_type == 'pattern':
            metrics = item.get('metrics', {})
            evolution = item.get('evolution', {})

            success_rate = metrics.get('successRate', 1.0)
            confidence = evolution.get('confidenceScore', 1.0)

            if success_rate < self.config.min_success_rate:
                return PruneReason.LOW_SUCCESS_RATE
            if confidence < self.config.min_confidence_score:
                return PruneReason.LOW_CONFIDENCE

        return PruneReason.LOW_CONFIDENCE

    def _archive_items(self, agent: str, category: str, items: List[Dict[str, Any]]) -> None:
        """Archive items to backup location"""
        try:
            archive_path = self.backup_path / 'archives' / agent
            archive_path.mkdir(parents=True, exist_ok=True)

            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            archive_file = archive_path / f"{category}_{timestamp}.json.gz"

            with gzip.open(archive_file, 'wt', encoding='utf-8') as f:
                json.dump(items, f, indent=2, ensure_ascii=False)

            logger.info(f"Archived {len(items)} items to {archive_file}")

        except Exception as e:
            logger.error(f"Error archiving items: {e}")

    def _get_last_used_date(self, item: Dict[str, Any]) -> Optional[datetime]:
        """Extract last used date from item"""
        # Try evolution.lastUsed first (patterns)
        evolution = item.get('evolution', {})
        if 'lastUsed' in evolution:
            return self._parse_timestamp(evolution['lastUsed'])

        # Try timestamp field
        if 'timestamp' in item:
            return self._parse_timestamp(item['timestamp'])

        return None

    def _parse_timestamp(self, timestamp_str: Optional[str]) -> Optional[datetime]:
        """Parse ISO 8601 timestamp"""
        if not timestamp_str:
            return None

        try:
            # Handle both with and without microseconds
            if '.' in timestamp_str:
                return datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
            else:
                return datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
        except Exception:
            return None

    def _get_directory_size(self, path: Path) -> int:
        """Calculate total size of directory"""
        total = 0
        for item in path.rglob('*'):
            if item.is_file():
                total += item.stat().st_size
        return total

    def _get_total_size(self) -> int:
        """Calculate total size of all memory"""
        return self._get_directory_size(self.memory_path)


def prune_memory(
    memory_path: str,
    strategies: List[str],
    agents: Optional[List[str]] = None,
    config: Optional[Dict[str, Any]] = None,
    dry_run: bool = False
) -> List[PruneResult]:
    """
    Main entry point for memory pruning.

    Args:
        memory_path: Path to .loom/memory directory
        strategies: List of strategy names ('time_based', 'performance_based', 'space_based')
        agents: Optional list of specific agents to prune
        config: Optional configuration overrides
        dry_run: If True, don't actually modify files

    Returns:
        List of PruneResult objects
    """
    # Parse strategies
    strategy_enums = []
    for s in strategies:
        try:
            strategy_enums.append(PruneStrategy(s))
        except ValueError:
            logger.warning(f"Unknown strategy: {s}")

    # Build config
    prune_config = PruneConfig(**(config or {}))
    prune_config.dry_run = dry_run

    # Create pruner and execute
    pruner = MemoryPruner(Path(memory_path), prune_config)
    results = pruner.prune_all(strategy_enums, agents)

    return results


if __name__ == '__main__':
    import sys

    # Simple CLI for testing
    if len(sys.argv) < 2:
        print("Usage: python pruning.py <memory_path> [strategies...]")
        print("Strategies: time_based, performance_based, space_based")
        sys.exit(1)

    memory_path = sys.argv[1]
    strategies = sys.argv[2:] if len(sys.argv) > 2 else ['time_based', 'performance_based']

    results = prune_memory(memory_path, strategies, dry_run=True)

    for result in results:
        print(f"\n=== {result.strategy.value.upper()} ===")
        print(f"Items pruned: {result.items_pruned}")
        print(f"Items archived: {result.items_archived}")
        print(f"Items compressed: {result.items_compressed}")
        print(f"Space freed: {result.space_freed_bytes / 1024 / 1024:.2f}MB")
        print(f"Duration: {result.duration_seconds:.2f}s")

        if result.summary:
            print("\nSummary by reason:")
            for reason, count in result.summary.items():
                print(f"  {reason.value}: {count}")

        if result.errors:
            print("\nErrors:")
            for error in result.errors:
                print(f"  - {error}")
