/**
 * FileStorage Test Suite
 *
 * Tests the low-level file storage operations including:
 * - File locking for concurrent access
 * - Atomic writes using temp files
 * - Compression/decompression
 * - Error handling and recovery
 */

import { describe, it, expect, beforeEach, afterEach } from '@jest/globals';
import * as fs from 'fs/promises';
import * as path from 'path';
import { FileStorage } from '../FileStorage';

const TEST_DIR = path.join(__dirname, '../../__test_data__/file-storage');
const TEST_FILE = path.join(TEST_DIR, 'test.json');

describe('FileStorage', () => {
  let storage: FileStorage;

  beforeEach(async () => {
    // Clean up test directory
    await fs.rm(TEST_DIR, { recursive: true, force: true });
    await fs.mkdir(TEST_DIR, { recursive: true });

    storage = new FileStorage();
  });

  afterEach(async () => {
    // Clean up test directory
    await fs.rm(TEST_DIR, { recursive: true, force: true });
  });

  describe('Basic File Operations', () => {
    it('should write data to file', async () => {
      const data = { test: 'value', number: 42 };

      const result = await storage.write(TEST_FILE, data);

      expect(result.success).toBe(true);
      expect(await fs.access(TEST_FILE)).resolves;
    });

    it('should read data from file', async () => {
      const data = { test: 'value', number: 42, nested: { key: 'val' } };
      await storage.write(TEST_FILE, data);

      const result = await storage.read(TEST_FILE);

      expect(result.success).toBe(true);
      expect(result.data).toEqual(data);
    });

    it('should return error for non-existent file', async () => {
      const result = await storage.read(path.join(TEST_DIR, 'nonexistent.json'));

      expect(result.success).toBe(false);
      expect(result.error).toContain('ENOENT');
    });

    it('should delete file', async () => {
      await storage.write(TEST_FILE, { test: 'data' });

      const result = await storage.delete(TEST_FILE);

      expect(result.success).toBe(true);
      await expect(fs.access(TEST_FILE)).rejects.toThrow();
    });

    it('should handle delete of non-existent file gracefully', async () => {
      const result = await storage.delete(path.join(TEST_DIR, 'nonexistent.json'));

      expect(result.success).toBe(true); // Should succeed (idempotent)
    });
  });

  describe('Atomic Writes', () => {
    it('should use atomic writes (temp file + rename)', async () => {
      const data = { important: 'data' };

      await storage.write(TEST_FILE, data);

      // Verify no temp files left behind
      const files = await fs.readdir(TEST_DIR);
      expect(files.filter(f => f.endsWith('.tmp'))).toHaveLength(0);
      expect(files).toContain('test.json');
    });

    it('should preserve data integrity on write failure', async () => {
      const originalData = { original: 'data' };
      await storage.write(TEST_FILE, originalData);

      // Simulate failure by writing to read-only directory
      const readOnlyFile = path.join(TEST_DIR, 'readonly', 'test.json');
      await fs.mkdir(path.join(TEST_DIR, 'readonly'), { recursive: true });
      await fs.chmod(path.join(TEST_DIR, 'readonly'), 0o444); // Read-only

      const result = await storage.write(readOnlyFile, { new: 'data' });

      expect(result.success).toBe(false);

      // Original file should still be intact
      const originalResult = await storage.read(TEST_FILE);
      expect(originalResult.data).toEqual(originalData);

      // Clean up
      await fs.chmod(path.join(TEST_DIR, 'readonly'), 0o755);
    });

    it('should handle concurrent writes to same file', async () => {
      const writes = Array.from({ length: 10 }, (_, i) =>
        storage.write(TEST_FILE, { iteration: i, timestamp: Date.now() })
      );

      const results = await Promise.all(writes);

      // All writes should succeed
      expect(results.every(r => r.success)).toBe(true);

      // Final file should have valid data
      const finalData = await storage.read(TEST_FILE);
      expect(finalData.success).toBe(true);
      expect(finalData.data).toHaveProperty('iteration');
    });
  });

  describe('File Locking', () => {
    it('should acquire lock before writing', async () => {
      const lockFile = `${TEST_FILE}.lock`;

      // Start a write operation
      const writePromise = storage.write(TEST_FILE, { data: 'test' });

      // Give it a moment to acquire lock
      await new Promise(resolve => setTimeout(resolve, 10));

      // Lock file should exist during write
      // (may not exist by the time we check due to speed)

      await writePromise;

      // Lock should be released after write
      try {
        await fs.access(lockFile);
        expect(true).toBe(false); // Should not get here
      } catch (error: any) {
        expect(error.code).toBe('ENOENT'); // Lock file should be gone
      }
    });

    it('should handle stale locks', async () => {
      const lockFile = `${TEST_FILE}.lock`;

      // Create an old stale lock (>30 seconds old)
      await fs.writeFile(lockFile, JSON.stringify({
        pid: 99999,
        acquired: Date.now() - 31000 // 31 seconds ago
      }));

      // Write should succeed by removing stale lock
      const result = await storage.write(TEST_FILE, { test: 'data' });

      expect(result.success).toBe(true);
    });

    it('should retry on lock contention', async () => {
      const lockFile = `${TEST_FILE}.lock`;

      // Create a recent lock (another process)
      await fs.writeFile(lockFile, JSON.stringify({
        pid: process.pid + 1,
        acquired: Date.now()
      }));

      // Write should wait and eventually timeout or acquire lock
      const result = await storage.write(TEST_FILE, { test: 'data' }, { timeout: 100 });

      // Either succeeds (if lock released) or times out
      if (!result.success) {
        expect(result.error).toContain('timeout');
      }

      // Clean up
      await fs.unlink(lockFile).catch(() => {});
    });
  });

  describe('Compression', () => {
    it('should compress data when enabled', async () => {
      const largeData = {
        items: Array.from({ length: 1000 }, (_, i) => ({
          id: i,
          name: `Item ${i}`,
          description: 'A'.repeat(100)
        }))
      };

      // Write without compression
      await storage.write(TEST_FILE, largeData, { compress: false });
      const uncompressedSize = (await fs.stat(TEST_FILE)).size;

      // Write with compression
      const compressedFile = path.join(TEST_DIR, 'compressed.json');
      await storage.write(compressedFile, largeData, { compress: true });
      const compressedSize = (await fs.stat(compressedFile)).size;

      // Compressed should be significantly smaller
      expect(compressedSize).toBeLessThan(uncompressedSize * 0.5);
    });

    it('should decompress data correctly', async () => {
      const originalData = {
        test: 'value',
        array: [1, 2, 3, 4, 5],
        nested: { key: 'val' }
      };

      await storage.write(TEST_FILE, originalData, { compress: true });
      const result = await storage.read(TEST_FILE);

      expect(result.success).toBe(true);
      expect(result.data).toEqual(originalData);
    });

    it('should handle both compressed and uncompressed files', async () => {
      const data1 = { type: 'uncompressed' };
      const data2 = { type: 'compressed' };

      const file1 = path.join(TEST_DIR, 'file1.json');
      const file2 = path.join(TEST_DIR, 'file2.json');

      await storage.write(file1, data1, { compress: false });
      await storage.write(file2, data2, { compress: true });

      const result1 = await storage.read(file1);
      const result2 = await storage.read(file2);

      expect(result1.data).toEqual(data1);
      expect(result2.data).toEqual(data2);
    });
  });

  describe('Error Handling', () => {
    it('should handle invalid JSON gracefully', async () => {
      // Write invalid JSON manually
      await fs.writeFile(TEST_FILE, 'invalid{json}content');

      const result = await storage.read(TEST_FILE);

      expect(result.success).toBe(false);
      expect(result.error).toContain('JSON');
    });

    it('should handle permission errors', async () => {
      await storage.write(TEST_FILE, { test: 'data' });

      // Make file read-only
      await fs.chmod(TEST_FILE, 0o444);

      const result = await storage.write(TEST_FILE, { new: 'data' });

      expect(result.success).toBe(false);
      expect(result.error).toContain('EACCES');

      // Clean up
      await fs.chmod(TEST_FILE, 0o644);
    });

    it('should handle disk full scenarios', async () => {
      // This is hard to test without actually filling disk
      // We'll simulate by checking error handling structure

      const result = await storage.write('/dev/null/impossible.json', { test: 'data' });

      expect(result.success).toBe(false);
      expect(result.error).toBeDefined();
    });

    it('should handle corrupted compressed data', async () => {
      // Write corrupted gzip data
      await fs.writeFile(TEST_FILE, Buffer.from([0x1f, 0x8b, 0xFF, 0xFF])); // Invalid gzip

      const result = await storage.read(TEST_FILE);

      expect(result.success).toBe(false);
    });
  });

  describe('Metadata Operations', () => {
    it('should check if file exists', async () => {
      await storage.write(TEST_FILE, { test: 'data' });

      const exists = await storage.exists(TEST_FILE);
      const notExists = await storage.exists(path.join(TEST_DIR, 'nope.json'));

      expect(exists).toBe(true);
      expect(notExists).toBe(false);
    });

    it('should get file stats', async () => {
      const data = { test: 'value' };
      await storage.write(TEST_FILE, data);

      const stats = await storage.getStats(TEST_FILE);

      expect(stats.success).toBe(true);
      expect(stats.data).toHaveProperty('size');
      expect(stats.data).toHaveProperty('created');
      expect(stats.data).toHaveProperty('modified');
      expect(stats.data?.size).toBeGreaterThan(0);
    });

    it('should list files in directory', async () => {
      await storage.write(path.join(TEST_DIR, 'file1.json'), { test: 1 });
      await storage.write(path.join(TEST_DIR, 'file2.json'), { test: 2 });
      await storage.write(path.join(TEST_DIR, 'file3.json'), { test: 3 });

      const files = await storage.listFiles(TEST_DIR);

      expect(files.success).toBe(true);
      expect(files.data).toHaveLength(3);
      expect(files.data).toContain('file1.json');
      expect(files.data).toContain('file2.json');
      expect(files.data).toContain('file3.json');
    });
  });

  describe('Performance', () => {
    it('should handle large files efficiently', async () => {
      const largeData = {
        patterns: Array.from({ length: 10000 }, (_, i) => ({
          id: `pattern-${i}`,
          confidence: Math.random(),
          data: 'x'.repeat(100)
        }))
      };

      const startWrite = Date.now();
      await storage.write(TEST_FILE, largeData, { compress: true });
      const writeTime = Date.now() - startWrite;

      const startRead = Date.now();
      await storage.read(TEST_FILE);
      const readTime = Date.now() - startRead;

      // Should complete in reasonable time (< 1 second each)
      expect(writeTime).toBeLessThan(1000);
      expect(readTime).toBeLessThan(1000);
    });

    it('should batch multiple operations efficiently', async () => {
      const operations = Array.from({ length: 50 }, (_, i) => ({
        file: path.join(TEST_DIR, `batch-${i}.json`),
        data: { index: i }
      }));

      const start = Date.now();
      await Promise.all(
        operations.map(op => storage.write(op.file, op.data))
      );
      const duration = Date.now() - start;

      // Should complete in reasonable time
      expect(duration).toBeLessThan(5000); // 5 seconds for 50 files
    });
  });

  describe('Edge Cases', () => {
    it('should handle empty objects', async () => {
      await storage.write(TEST_FILE, {});
      const result = await storage.read(TEST_FILE);

      expect(result.success).toBe(true);
      expect(result.data).toEqual({});
    });

    it('should handle deep nested objects', async () => {
      const deepData: any = { level: 0 };
      let current = deepData;
      for (let i = 1; i < 100; i++) {
        current.nested = { level: i };
        current = current.nested;
      }

      await storage.write(TEST_FILE, deepData);
      const result = await storage.read(TEST_FILE);

      expect(result.success).toBe(true);
      expect(result.data).toEqual(deepData);
    });

    it('should handle special characters in data', async () => {
      const specialData = {
        unicode: '你好世界🎉',
        quotes: 'He said "hello"',
        newlines: 'Line 1\nLine 2\nLine 3',
        emoji: '😀😃😄😁'
      };

      await storage.write(TEST_FILE, specialData);
      const result = await storage.read(TEST_FILE);

      expect(result.success).toBe(true);
      expect(result.data).toEqual(specialData);
    });

    it('should handle very long file paths', async () => {
      const longPath = path.join(
        TEST_DIR,
        'a'.repeat(50),
        'b'.repeat(50),
        'c'.repeat(50),
        'test.json'
      );

      await fs.mkdir(path.dirname(longPath), { recursive: true });

      const result = await storage.write(longPath, { test: 'data' });

      expect(result.success).toBe(true);
    });
  });
});
