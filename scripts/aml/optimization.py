#!/usr/bin/env python3
"""
AML Memory Optimization System

Implements memory compression, lazy loading, searchable indices,
bloom filters, cache warming, and garbage collection.

Author: Loom Framework
Version: 1.0.0
"""

import json
import gzip
import hashlib
import pickle
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional, Set, Tuple, Iterator
from dataclasses import dataclass, asdict
from datetime import datetime
from collections import OrderedDict
import struct


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class IndexEntry:
    """Entry in the memory index for fast lookups"""
    id: str
    agent: str
    item_type: str  # 'pattern', 'solution', 'decision'
    timestamp: str
    tags: List[str]
    confidence: float
    success_rate: float
    file_path: str
    offset: int  # Byte offset in file for lazy loading
    size: int  # Size in bytes


@dataclass
class CacheStats:
    """Statistics for the cache system"""
    hits: int = 0
    misses: int = 0
    evictions: int = 0
    size_bytes: int = 0
    max_size_bytes: int = 10 * 1024 * 1024  # 10MB default

    @property
    def hit_rate(self) -> float:
        """Calculate cache hit rate"""
        total = self.hits + self.misses
        return self.hits / total if total > 0 else 0.0


class BloomFilter:
    """
    Space-efficient probabilistic data structure for membership testing.

    Used to quickly check if a pattern ID or tag exists before
    performing expensive disk I/O operations.
    """

    def __init__(self, capacity: int = 10000, error_rate: float = 0.01):
        """
        Initialize bloom filter.

        Args:
            capacity: Expected number of items
            error_rate: Desired false positive rate
        """
        self.capacity = capacity
        self.error_rate = error_rate

        # Calculate optimal size and hash count
        self.size = self._optimal_size(capacity, error_rate)
        self.hash_count = self._optimal_hash_count(self.size, capacity)

        # Bit array
        self.bits = [False] * self.size

    def add(self, item: str) -> None:
        """Add an item to the bloom filter"""
        for i in range(self.hash_count):
            index = self._hash(item, i) % self.size
            self.bits[index] = True

    def contains(self, item: str) -> bool:
        """Check if item might be in the set (false positives possible)"""
        for i in range(self.hash_count):
            index = self._hash(item, i) % self.size
            if not self.bits[index]:
                return False
        return True

    def _hash(self, item: str, seed: int) -> int:
        """Generate hash with seed"""
        h = hashlib.sha256(f"{item}{seed}".encode()).digest()
        return struct.unpack('<Q', h[:8])[0]

    @staticmethod
    def _optimal_size(capacity: int, error_rate: float) -> int:
        """Calculate optimal bit array size"""
        import math
        m = -(capacity * math.log(error_rate)) / (math.log(2) ** 2)
        return int(m)

    @staticmethod
    def _optimal_hash_count(size: int, capacity: int) -> int:
        """Calculate optimal number of hash functions"""
        import math
        k = (size / capacity) * math.log(2)
        return max(1, int(k))

    def to_bytes(self) -> bytes:
        """Serialize to bytes for storage"""
        data = {
            'capacity': self.capacity,
            'error_rate': self.error_rate,
            'size': self.size,
            'hash_count': self.hash_count,
            'bits': self.bits
        }
        return pickle.dumps(data)

    @classmethod
    def from_bytes(cls, data: bytes) -> 'BloomFilter':
        """Deserialize from bytes"""
        stored = pickle.loads(data)
        bf = cls(stored['capacity'], stored['error_rate'])
        bf.size = stored['size']
        bf.hash_count = stored['hash_count']
        bf.bits = stored['bits']
        return bf


class LRUCache:
    """
    Least Recently Used cache for memory items.

    Keeps frequently accessed patterns in memory for fast retrieval.
    """

    def __init__(self, max_size_bytes: int = 10 * 1024 * 1024):
        """
        Initialize LRU cache.

        Args:
            max_size_bytes: Maximum cache size in bytes
        """
        self.max_size = max_size_bytes
        self.cache: OrderedDict[str, Tuple[Any, int]] = OrderedDict()
        self.stats = CacheStats(max_size_bytes=max_size_bytes)

    def get(self, key: str) -> Optional[Any]:
        """Get item from cache"""
        if key in self.cache:
            # Move to end (most recently used)
            self.cache.move_to_end(key)
            self.stats.hits += 1
            return self.cache[key][0]

        self.stats.misses += 1
        return None

    def put(self, key: str, value: Any, size: int) -> None:
        """Put item in cache"""
        # If key exists, update it
        if key in self.cache:
            old_size = self.cache[key][1]
            self.stats.size_bytes -= old_size

        self.cache[key] = (value, size)
        self.stats.size_bytes += size
        self.cache.move_to_end(key)

        # Evict items if over limit
        while self.stats.size_bytes > self.max_size and self.cache:
            evicted_key, (_, evicted_size) = self.cache.popitem(last=False)
            self.stats.size_bytes -= evicted_size
            self.stats.evictions += 1
            logger.debug(f"Evicted {evicted_key} from cache ({evicted_size} bytes)")

    def clear(self) -> None:
        """Clear the cache"""
        self.cache.clear()
        self.stats.size_bytes = 0

    def get_stats(self) -> CacheStats:
        """Get cache statistics"""
        return self.stats


class MemoryIndex:
    """
    Searchable index for fast pattern/solution/decision lookups.

    Maintains:
    - ID index for O(1) lookups
    - Tag index for fast filtering
    - Bloom filter for existence checks
    """

    def __init__(self, memory_path: Path):
        """Initialize the memory index"""
        self.memory_path = Path(memory_path)
        self.index_file = memory_path / 'global' / 'index.json'
        self.bloom_file = memory_path / 'global' / 'bloom.dat'

        # In-memory indices
        self.id_index: Dict[str, IndexEntry] = {}
        self.tag_index: Dict[str, Set[str]] = {}  # tag -> set of IDs
        self.agent_index: Dict[str, Set[str]] = {}  # agent -> set of IDs
        self.bloom: Optional[BloomFilter] = None

        # Load existing index
        self._load_index()

    def build_index(self, force: bool = False) -> int:
        """
        Build or rebuild the index from scratch.

        Args:
            force: Force rebuild even if index exists

        Returns:
            Number of items indexed
        """
        if not force and self.id_index:
            logger.info("Index already loaded, use force=True to rebuild")
            return len(self.id_index)

        logger.info("Building memory index...")
        self.id_index.clear()
        self.tag_index.clear()
        self.agent_index.clear()

        # Initialize bloom filter
        self.bloom = BloomFilter(capacity=50000)

        item_count = 0

        # Scan all agent directories
        for agent_dir in self.memory_path.iterdir():
            if not agent_dir.is_dir() or agent_dir.name in ['global', 'config', 'backup']:
                continue

            agent_name = agent_dir.name

            # Index patterns
            patterns_file = agent_dir / 'patterns.json'
            if patterns_file.exists():
                items = self._load_json_file(patterns_file)
                for item in items:
                    self._index_item(item, agent_name, 'pattern', str(patterns_file))
                    item_count += 1

            # Index solutions
            solutions_file = agent_dir / 'solutions.json'
            if solutions_file.exists():
                items = self._load_json_file(solutions_file)
                for item in items:
                    self._index_item(item, agent_name, 'solution', str(solutions_file))
                    item_count += 1

            # Index decisions
            decisions_file = agent_dir / 'decisions.json'
            if decisions_file.exists():
                items = self._load_json_file(decisions_file)
                for item in items:
                    self._index_item(item, agent_name, 'decision', str(decisions_file))
                    item_count += 1

        # Save index
        self._save_index()

        logger.info(f"Indexed {item_count} items across {len(self.agent_index)} agents")
        return item_count

    def search(
        self,
        agent: Optional[str] = None,
        tags: Optional[List[str]] = None,
        item_type: Optional[str] = None,
        min_confidence: float = 0.0,
        min_success_rate: float = 0.0
    ) -> List[IndexEntry]:
        """
        Search the index with filters.

        Args:
            agent: Filter by agent name
            tags: Filter by tags (AND logic)
            item_type: Filter by type (pattern/solution/decision)
            min_confidence: Minimum confidence score
            min_success_rate: Minimum success rate

        Returns:
            List of matching index entries
        """
        results = set(self.id_index.keys())

        # Filter by agent
        if agent and agent in self.agent_index:
            results &= self.agent_index[agent]

        # Filter by tags (AND logic)
        if tags:
            for tag in tags:
                if tag in self.tag_index:
                    results &= self.tag_index[tag]
                else:
                    return []  # Tag doesn't exist

        # Apply remaining filters
        filtered = []
        for item_id in results:
            entry = self.id_index[item_id]

            if item_type and entry.item_type != item_type:
                continue
            if entry.confidence < min_confidence:
                continue
            if entry.success_rate < min_success_rate:
                continue

            filtered.append(entry)

        # Sort by confidence * success_rate (relevance score)
        filtered.sort(key=lambda e: e.confidence * e.success_rate, reverse=True)

        return filtered

    def exists(self, item_id: str) -> bool:
        """Check if an item exists (uses bloom filter first)"""
        if self.bloom and not self.bloom.contains(item_id):
            return False
        return item_id in self.id_index

    def get(self, item_id: str) -> Optional[IndexEntry]:
        """Get index entry by ID"""
        return self.id_index.get(item_id)

    def add_item(self, item: Dict[str, Any], agent: str, item_type: str, file_path: str) -> None:
        """Add a new item to the index"""
        self._index_item(item, agent, item_type, file_path)
        self._save_index()

    def remove_item(self, item_id: str) -> None:
        """Remove an item from the index"""
        if item_id not in self.id_index:
            return

        entry = self.id_index[item_id]

        # Remove from tag index
        for tag in entry.tags:
            if tag in self.tag_index:
                self.tag_index[tag].discard(item_id)
                if not self.tag_index[tag]:
                    del self.tag_index[tag]

        # Remove from agent index
        if entry.agent in self.agent_index:
            self.agent_index[entry.agent].discard(item_id)

        # Remove from ID index
        del self.id_index[item_id]

        self._save_index()

    def _index_item(self, item: Dict[str, Any], agent: str, item_type: str, file_path: str) -> None:
        """Add item to indices"""
        item_id = item.get('id')
        if not item_id:
            return

        # Extract metadata
        timestamp = item.get('timestamp', '')
        tags = item.get('tags', [])

        # Extract metrics
        metrics = item.get('metrics', {})
        evolution = item.get('evolution', {})
        confidence = evolution.get('confidenceScore', 0.5)
        success_rate = metrics.get('successRate', 0.5)

        # Create index entry
        entry = IndexEntry(
            id=item_id,
            agent=agent,
            item_type=item_type,
            timestamp=timestamp,
            tags=tags,
            confidence=confidence,
            success_rate=success_rate,
            file_path=file_path,
            offset=0,  # TODO: Calculate actual offset for lazy loading
            size=len(json.dumps(item))
        )

        # Add to ID index
        self.id_index[item_id] = entry

        # Add to bloom filter
        if self.bloom:
            self.bloom.add(item_id)

        # Add to tag index
        for tag in tags:
            if tag not in self.tag_index:
                self.tag_index[tag] = set()
            self.tag_index[tag].add(item_id)

        # Add to agent index
        if agent not in self.agent_index:
            self.agent_index[agent] = set()
        self.agent_index[agent].add(item_id)

    def _load_json_file(self, file_path: Path) -> List[Dict[str, Any]]:
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

    def _load_index(self) -> None:
        """Load index from disk"""
        if not self.index_file.exists():
            return

        try:
            with open(self.index_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Reconstruct indices
            for entry_data in data.get('entries', []):
                entry = IndexEntry(**entry_data)
                self.id_index[entry.id] = entry

                # Rebuild tag index
                for tag in entry.tags:
                    if tag not in self.tag_index:
                        self.tag_index[tag] = set()
                    self.tag_index[tag].add(entry.id)

                # Rebuild agent index
                if entry.agent not in self.agent_index:
                    self.agent_index[entry.agent] = set()
                self.agent_index[entry.agent].add(entry.id)

            # Load bloom filter
            if self.bloom_file.exists():
                with open(self.bloom_file, 'rb') as f:
                    self.bloom = BloomFilter.from_bytes(f.read())

            logger.info(f"Loaded index with {len(self.id_index)} items")

        except Exception as e:
            logger.error(f"Error loading index: {e}")

    def _save_index(self) -> None:
        """Save index to disk"""
        try:
            self.index_file.parent.mkdir(parents=True, exist_ok=True)

            # Convert to serializable format
            entries = [asdict(entry) for entry in self.id_index.values()]

            with open(self.index_file, 'w', encoding='utf-8') as f:
                json.dump({'entries': entries, 'version': '1.0.0'}, f, indent=2)

            # Save bloom filter
            if self.bloom:
                with open(self.bloom_file, 'wb') as f:
                    f.write(self.bloom.to_bytes())

            logger.info(f"Saved index with {len(entries)} items")

        except Exception as e:
            logger.error(f"Error saving index: {e}")


class LazyMemoryLoader:
    """
    Lazy loading system for memory files.

    Only loads memory items when accessed, reducing memory footprint
    for agents with large memory stores.
    """

    def __init__(self, memory_path: Path, cache_size: int = 10 * 1024 * 1024):
        """
        Initialize lazy loader.

        Args:
            memory_path: Path to .loom/memory directory
            cache_size: Size of LRU cache in bytes
        """
        self.memory_path = Path(memory_path)
        self.cache = LRUCache(max_size_bytes=cache_size)
        self.index = MemoryIndex(memory_path)

    def load_item(self, item_id: str) -> Optional[Dict[str, Any]]:
        """
        Load a single item by ID (with caching).

        Args:
            item_id: Unique ID of the item

        Returns:
            Item data or None if not found
        """
        # Check cache first
        cached = self.cache.get(item_id)
        if cached is not None:
            return cached

        # Check if item exists in index
        entry = self.index.get(item_id)
        if not entry:
            return None

        # Load from file
        try:
            file_path = Path(entry.file_path)
            items = self._load_json_file(file_path)

            # Find the specific item
            for item in items:
                if item.get('id') == item_id:
                    # Cache it
                    self.cache.put(item_id, item, entry.size)
                    return item

        except Exception as e:
            logger.error(f"Error loading item {item_id}: {e}")

        return None

    def load_items_by_filter(
        self,
        agent: Optional[str] = None,
        tags: Optional[List[str]] = None,
        item_type: Optional[str] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Load items matching filters.

        Args:
            agent: Filter by agent name
            tags: Filter by tags
            item_type: Filter by type
            limit: Maximum number of items to return

        Returns:
            List of matching items
        """
        # Search index
        entries = self.index.search(agent=agent, tags=tags, item_type=item_type)[:limit]

        # Load items
        items = []
        for entry in entries:
            item = self.load_item(entry.id)
            if item:
                items.append(item)

        return items

    def warm_cache(self, agents: Optional[List[str]] = None) -> int:
        """
        Pre-load high-value items into cache.

        Args:
            agents: Optional list of agents to warm cache for

        Returns:
            Number of items loaded into cache
        """
        logger.info("Warming cache with high-value patterns...")

        # Load top patterns by value score
        entries = self.index.search(
            agent=agents[0] if agents and len(agents) == 1 else None,
            min_confidence=0.7,
            min_success_rate=0.7
        )

        loaded = 0
        cache_limit = int(self.cache.max_size * 0.8)  # Use 80% of cache

        for entry in entries:
            if self.cache.stats.size_bytes >= cache_limit:
                break

            item = self.load_item(entry.id)
            if item:
                loaded += 1

        logger.info(f"Warmed cache with {loaded} items ({self.cache.stats.size_bytes / 1024 / 1024:.2f}MB)")
        return loaded

    def get_cache_stats(self) -> CacheStats:
        """Get cache statistics"""
        return self.cache.get_stats()

    def _load_json_file(self, file_path: Path) -> List[Dict[str, Any]]:
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


class MemoryCompressor:
    """
    Compression utilities for memory files.

    Automatically compresses old or large memory files to save space.
    """

    @staticmethod
    def compress_file(file_path: Path, delete_original: bool = True, level: int = 9) -> Optional[Path]:
        """
        Compress a file using gzip.

        Args:
            file_path: Path to file to compress
            delete_original: Whether to delete original after compression
            level: Compression level (1-9, 9 is highest)

        Returns:
            Path to compressed file or None on error
        """
        if file_path.suffix == '.gz':
            logger.info(f"{file_path} already compressed")
            return file_path

        try:
            compressed_path = file_path.with_suffix(file_path.suffix + '.gz')

            with open(file_path, 'rb') as f_in:
                with gzip.open(compressed_path, 'wb', compresslevel=level) as f_out:
                    f_out.writelines(f_in)

            original_size = file_path.stat().st_size
            compressed_size = compressed_path.stat().st_size
            ratio = (1 - compressed_size / original_size) * 100

            logger.info(f"Compressed {file_path.name}: {original_size / 1024:.1f}KB -> {compressed_size / 1024:.1f}KB ({ratio:.1f}% reduction)")

            if delete_original:
                file_path.unlink()

            return compressed_path

        except Exception as e:
            logger.error(f"Error compressing {file_path}: {e}")
            return None

    @staticmethod
    def compress_directory(directory: Path, age_days: int = 30) -> int:
        """
        Compress all eligible files in a directory.

        Args:
            directory: Directory to process
            age_days: Compress files older than this many days

        Returns:
            Number of files compressed
        """
        count = 0
        cutoff_date = datetime.now().timestamp() - (age_days * 24 * 60 * 60)

        for file_path in directory.rglob('*.json'):
            # Skip if already compressed
            if file_path.suffix == '.gz':
                continue

            # Check age
            if file_path.stat().st_mtime < cutoff_date:
                if MemoryCompressor.compress_file(file_path):
                    count += 1

        return count


class GarbageCollector:
    """
    Garbage collection for orphaned and invalid memory entries.

    Identifies and removes:
    - Items with missing required fields
    - Duplicate entries
    - Orphaned index entries
    """

    def __init__(self, memory_path: Path):
        """Initialize garbage collector"""
        self.memory_path = Path(memory_path)

    def collect(self, dry_run: bool = False) -> Dict[str, int]:
        """
        Run garbage collection.

        Args:
            dry_run: If True, don't actually delete anything

        Returns:
            Dictionary with counts of items collected
        """
        stats = {
            'invalid_items': 0,
            'duplicates': 0,
            'orphaned_indices': 0,
            'empty_files': 0
        }

        logger.info("Running garbage collection...")

        # Collect invalid and duplicate items
        seen_ids = set()

        for agent_dir in self.memory_path.iterdir():
            if not agent_dir.is_dir() or agent_dir.name in ['global', 'config', 'backup']:
                continue

            for file_name in ['patterns.json', 'solutions.json', 'decisions.json']:
                file_path = agent_dir / file_name
                if not file_path.exists():
                    continue

                try:
                    items = self._load_json(file_path)
                    if not items:
                        stats['empty_files'] += 1
                        if not dry_run:
                            file_path.unlink()
                        continue

                    valid_items = []

                    for item in items:
                        # Check for required fields
                        if not self._is_valid_item(item):
                            stats['invalid_items'] += 1
                            continue

                        # Check for duplicates
                        item_id = item.get('id')
                        if item_id in seen_ids:
                            stats['duplicates'] += 1
                            continue

                        seen_ids.add(item_id)
                        valid_items.append(item)

                    # Write back if changes were made
                    if len(valid_items) < len(items) and not dry_run:
                        self._save_json(file_path, valid_items)

                except Exception as e:
                    logger.error(f"Error processing {file_path}: {e}")

        logger.info(f"Garbage collection complete: {stats}")
        return stats

    def _is_valid_item(self, item: Dict[str, Any]) -> bool:
        """Check if item has all required fields"""
        required_fields = ['id', 'agent', 'timestamp']
        return all(field in item for field in required_fields)

    def _load_json(self, file_path: Path) -> List[Dict[str, Any]]:
        """Load JSON file"""
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
        print("Usage: python optimization.py <memory_path> <command>")
        print("Commands:")
        print("  build-index    - Build searchable index")
        print("  compress       - Compress old files")
        print("  warm-cache     - Warm up cache")
        print("  gc             - Run garbage collection")
        sys.exit(1)

    memory_path = Path(sys.argv[1])
    command = sys.argv[2]

    if command == 'build-index':
        index = MemoryIndex(memory_path)
        count = index.build_index(force=True)
        print(f"Indexed {count} items")

    elif command == 'compress':
        count = MemoryCompressor.compress_directory(memory_path, age_days=30)
        print(f"Compressed {count} files")

    elif command == 'warm-cache':
        loader = LazyMemoryLoader(memory_path)
        loader.index.build_index()
        count = loader.warm_cache()
        stats = loader.get_cache_stats()
        print(f"Warmed cache with {count} items")
        print(f"Hit rate: {stats.hit_rate:.2%}")

    elif command == 'gc':
        gc = GarbageCollector(memory_path)
        stats = gc.collect(dry_run=False)
        print("Garbage collection stats:", stats)

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
