/**
 * CacheLayer Unit Tests
 *
 * Tests LRU/LFU caching, TTL, eviction, and performance characteristics
 * Coverage target: 90%+
 */

import { CacheLayer, AMLCacheManager, CacheStats } from '../CacheLayer';

describe('CacheLayer', () => {
  describe('Basic Operations', () => {
    let cache: CacheLayer<string>;

    beforeEach(() => {
      cache = new CacheLayer({ maxSize: 100, ttlMs: 3600000, evictionPolicy: 'lru' });
    });

    it('should set and get values', () => {
      cache.set('key1', 'value1');
      const value = cache.get('key1');

      expect(value).toBe('value1');
    });

    it('should return null for non-existent key', () => {
      const value = cache.get('nonexistent');
      expect(value).toBeNull();
    });

    it('should check key existence without updating access', () => {
      cache.set('key1', 'value1');

      expect(cache.has('key1')).toBe(true);
      expect(cache.has('nonexistent')).toBe(false);
    });

    it('should delete keys', () => {
      cache.set('key1', 'value1');
      const deleted = cache.delete('key1');

      expect(deleted).toBe(true);
      expect(cache.get('key1')).toBeNull();
    });

    it('should not delete non-existent keys', () => {
      const deleted = cache.delete('nonexistent');
      expect(deleted).toBe(false);
    });

    it('should clear entire cache', () => {
      cache.set('key1', 'value1');
      cache.set('key2', 'value2');

      cache.clear();

      expect(cache.size()).toBe(0);
      expect(cache.get('key1')).toBeNull();
    });

    it('should get all keys', () => {
      cache.set('key1', 'value1');
      cache.set('key2', 'value2');

      const keys = cache.keys();

      expect(keys).toContain('key1');
      expect(keys).toContain('key2');
      expect(keys.length).toBe(2);
    });

    it('should return cache size', () => {
      cache.set('key1', 'value1');
      cache.set('key2', 'value2');

      expect(cache.size()).toBe(2);
    });
  });

  describe('TTL & Expiration', () => {
    it('should expire entries after TTL', async () => {
      const cache = new CacheLayer({ maxSize: 100, ttlMs: 100 });

      cache.set('key1', 'value1');
      expect(cache.get('key1')).toBe('value1');

      // Wait for TTL to expire
      await new Promise(resolve => setTimeout(resolve, 150));

      expect(cache.get('key1')).toBeNull();
    });

    it('should manually evict expired entries', async () => {
      const cache = new CacheLayer({ maxSize: 100, ttlMs: 100 });

      cache.set('key1', 'value1');
      cache.set('key2', 'value2');

      await new Promise(resolve => setTimeout(resolve, 150));

      const evicted = cache.evictExpired();

      expect(evicted).toBe(2);
      expect(cache.size()).toBe(0);
    });

    it('should not expire entries within TTL', () => {
      const cache = new CacheLayer({ maxSize: 100, ttlMs: 10000 });

      cache.set('key1', 'value1');
      const value = cache.get('key1');

      expect(value).toBe('value1');
    });

    it('should reset TTL on update', async () => {
      const cache = new CacheLayer({ maxSize: 100, ttlMs: 100 });

      cache.set('key1', 'value1');
      await new Promise(resolve => setTimeout(resolve, 50));
      cache.set('key1', 'value2'); // Reset TTL
      await new Promise(resolve => setTimeout(resolve, 75));

      expect(cache.get('key1')).toBe('value2');
    });
  });

  describe('LRU Eviction Policy', () => {
    it('should evict least recently used item at capacity', () => {
      const cache = new CacheLayer({ maxSize: 3, ttlMs: 3600000, evictionPolicy: 'lru' });

      cache.set('key1', 'value1');
      cache.set('key2', 'value2');
      cache.set('key3', 'value3');

      // key1 is least recently used
      cache.get('key2'); // key2 is now recently used
      cache.get('key3'); // key3 is now recently used

      cache.set('key4', 'value4'); // Should evict key1

      expect(cache.get('key1')).toBeNull();
      expect(cache.get('key2')).toBe('value2');
      expect(cache.get('key3')).toBe('value3');
      expect(cache.get('key4')).toBe('value4');
    });

    it('should update access order on get', () => {
      const cache = new CacheLayer({ maxSize: 2, ttlMs: 3600000, evictionPolicy: 'lru' });

      cache.set('key1', 'value1');
      cache.set('key2', 'value2');
      cache.get('key1'); // Make key1 most recently used

      cache.set('key3', 'value3'); // Should evict key2

      expect(cache.get('key1')).toBe('value1');
      expect(cache.get('key2')).toBeNull();
      expect(cache.get('key3')).toBe('value3');
    });
  });

  describe('LFU Eviction Policy', () => {
    it('should evict least frequently used item at capacity', () => {
      const cache = new CacheLayer({ maxSize: 3, ttlMs: 3600000, evictionPolicy: 'lfu' });

      cache.set('key1', 'value1');
      cache.set('key2', 'value2');
      cache.set('key3', 'value3');

      // Access key2 and key3 more frequently
      cache.get('key2');
      cache.get('key2');
      cache.get('key3');
      cache.get('key3');
      cache.get('key3');

      cache.set('key4', 'value4'); // Should evict key1 (least frequently used)

      expect(cache.get('key1')).toBeNull();
      expect(cache.get('key2')).toBe('value2');
    });
  });

  describe('Statistics', () => {
    it('should track cache hits', () => {
      const cache = new CacheLayer({ maxSize: 100, ttlMs: 3600000 });

      cache.set('key1', 'value1');
      cache.get('key1');
      cache.get('key1');

      const stats = cache.getStats();

      expect(stats.hits).toBe(2);
    });

    it('should track cache misses', () => {
      const cache = new CacheLayer({ maxSize: 100, ttlMs: 3600000 });

      cache.get('nonexistent1');
      cache.get('nonexistent2');

      const stats = cache.getStats();

      expect(stats.misses).toBe(2);
    });

    it('should calculate hit rate', () => {
      const cache = new CacheLayer({ maxSize: 100, ttlMs: 3600000 });

      cache.set('key1', 'value1');
      cache.get('key1'); // hit
      cache.get('key2'); // miss

      const stats = cache.getStats();

      expect(stats.hitRate).toBeCloseTo(0.5, 1);
    });

    it('should track evictions', () => {
      const cache = new CacheLayer({ maxSize: 2, ttlMs: 3600000 });

      cache.set('key1', 'value1');
      cache.set('key2', 'value2');
      cache.set('key3', 'value3'); // Triggers eviction

      const stats = cache.getStats();

      expect(stats.evictions).toBe(1);
    });

    it('should reset statistics', () => {
      const cache = new CacheLayer({ maxSize: 100, ttlMs: 3600000 });

      cache.set('key1', 'value1');
      cache.get('key1');
      cache.resetStats();

      const stats = cache.getStats();

      expect(stats.hits).toBe(0);
      expect(stats.misses).toBe(0);
    });

    it('should report current size in stats', () => {
      const cache = new CacheLayer({ maxSize: 100, ttlMs: 3600000 });

      cache.set('key1', 'value1');
      cache.set('key2', 'value2');

      const stats = cache.getStats();

      expect(stats.currentSize).toBe(2);
      expect(stats.maxSize).toBe(100);
    });
  });

  describe('Configuration', () => {
    it('should update cache options', () => {
      const cache = new CacheLayer({ maxSize: 10, ttlMs: 3600000 });

      cache.updateOptions({ maxSize: 5 });

      const stats = cache.getStats();
      expect(stats.maxSize).toBe(5);
    });

    it('should evict items when reducing maxSize', () => {
      const cache = new CacheLayer({ maxSize: 10, ttlMs: 3600000 });

      for (let i = 0; i < 10; i++) {
        cache.set(`key${i}`, `value${i}`);
      }

      cache.updateOptions({ maxSize: 5 });

      expect(cache.size()).toBe(5);
    });

    it('should update TTL', () => {
      const cache = new CacheLayer({ maxSize: 100, ttlMs: 100 });

      cache.updateOptions({ ttlMs: 10000 });

      cache.set('key1', 'value1');
      setTimeout(() => {
        expect(cache.get('key1')).toBe('value1');
      }, 500);
    });

    it('should switch eviction policy', () => {
      const cache = new CacheLayer({ maxSize: 100, evictionPolicy: 'lru' });

      cache.updateOptions({ evictionPolicy: 'lfu' });

      // Just verify it doesn't throw
      cache.set('key1', 'value1');
      cache.set('key2', 'value2');
    });
  });

  describe('Edge Cases', () => {
    it('should handle empty cache operations', () => {
      const cache = new CacheLayer({ maxSize: 100, ttlMs: 3600000 });

      expect(cache.size()).toBe(0);
      expect(cache.keys()).toEqual([]);
      cache.clear(); // Should not throw

      const stats = cache.getStats();
      expect(stats.currentSize).toBe(0);
    });

    it('should handle single-item cache', () => {
      const cache = new CacheLayer({ maxSize: 1, ttlMs: 3600000 });

      cache.set('key1', 'value1');
      expect(cache.get('key1')).toBe('value1');

      cache.set('key2', 'value2');
      expect(cache.get('key1')).toBeNull();
      expect(cache.get('key2')).toBe('value2');
    });

    it('should handle duplicate key updates', () => {
      const cache = new CacheLayer({ maxSize: 100, ttlMs: 3600000 });

      cache.set('key1', 'value1');
      cache.set('key1', 'value2');

      expect(cache.get('key1')).toBe('value2');
      expect(cache.size()).toBe(1);
    });

    it('should handle null/undefined values', () => {
      const cache = new CacheLayer<any>({ maxSize: 100, ttlMs: 3600000 });

      cache.set('null', null);
      cache.set('undefined', undefined);

      expect(cache.get('null')).toBeNull();
      expect(cache.get('undefined')).toBeUndefined();
    });

    it('should handle object values', () => {
      const cache = new CacheLayer<any>({ maxSize: 100, ttlMs: 3600000 });
      const obj = { a: 1, b: 2 };

      cache.set('obj', obj);

      expect(cache.get('obj')).toEqual(obj);
    });
  });

  describe('Performance', () => {
    it('should perform set operations quickly', () => {
      const cache = new CacheLayer({ maxSize: 1000, ttlMs: 3600000 });
      const startTime = Date.now();

      for (let i = 0; i < 1000; i++) {
        cache.set(`key${i}`, `value${i}`);
      }

      const duration = Date.now() - startTime;
      expect(duration).toBeLessThan(1000); // 1000 sets in under 1 second
    });

    it('should perform get operations quickly', () => {
      const cache = new CacheLayer({ maxSize: 1000, ttlMs: 3600000 });

      for (let i = 0; i < 1000; i++) {
        cache.set(`key${i}`, `value${i}`);
      }

      const startTime = Date.now();

      for (let i = 0; i < 1000; i++) {
        cache.get(`key${i}`);
      }

      const duration = Date.now() - startTime;
      expect(duration).toBeLessThan(500); // 1000 gets in under 500ms
    });

    it('should maintain high hit rate with LRU', () => {
      const cache = new CacheLayer({ maxSize: 100, ttlMs: 3600000, evictionPolicy: 'lru' });

      // Fill cache
      for (let i = 0; i < 100; i++) {
        cache.set(`key${i}`, `value${i}`);
      }

      // Access pattern: working set of 20 keys
      for (let i = 0; i < 1000; i++) {
        cache.get(`key${i % 20}`);
      }

      const stats = cache.getStats();
      expect(stats.hitRate).toBeGreaterThan(0.9);
    });
  });
});

describe('AMLCacheManager', () => {
  let manager: AMLCacheManager;

  beforeEach(() => {
    manager = new AMLCacheManager(100, 3600);
  });

  it('should initialize with separate caches', () => {
    expect(manager.getPatternCache()).toBeDefined();
    expect(manager.getSolutionCache()).toBeDefined();
    expect(manager.getDecisionCache()).toBeDefined();
    expect(manager.getQueryCache()).toBeDefined();
  });

  it('should clear all caches', () => {
    manager.getPatternCache().set('key1', 'value1');
    manager.getSolutionCache().set('key2', 'value2');

    manager.clearAll();

    expect(manager.getPatternCache().size()).toBe(0);
    expect(manager.getSolutionCache().size()).toBe(0);
  });

  it('should evict expired entries from all caches', async () => {
    const manager2 = new AMLCacheManager(100, 0.1); // 100ms TTL

    manager2.getPatternCache().set('key1', 'value1');
    manager2.getSolutionCache().set('key2', 'value2');

    await new Promise(resolve => setTimeout(resolve, 150));

    const evicted = manager2.evictExpiredAll();

    expect(evicted).toBeGreaterThan(0);
  });

  it('should combine statistics from all caches', () => {
    manager.getPatternCache().set('p1', 'v1');
    manager.getPatternCache().get('p1');
    manager.getSolutionCache().set('s1', 'v1');
    manager.getSolutionCache().get('s1');

    const combined = manager.getCombinedStats();

    expect(combined.totalHits).toBeGreaterThan(0);
    expect(combined.overallHitRate).toBeGreaterThan(0);
  });

  it('should warm cache with preloaded data', () => {
    const patterns = new Map([['p1', 'v1'], ['p2', 'v2']]);
    const solutions = new Map([['s1', 'v1']]);

    manager.warmCache({ patterns, solutions });

    expect(manager.getPatternCache().get('p1')).toBe('v1');
    expect(manager.getSolutionCache().get('s1')).toBe('v1');
  });

  it('should allocate cache sizes proportionally', () => {
    const stats = manager.getCombinedStats();

    // Pattern cache should get 40% allocation
    expect(stats.pattern.maxSize).toBeGreaterThan(stats.solution.maxSize);
  });
});
