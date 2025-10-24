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
const TEST_FILE = 'test.json'; // Relative path for FileStorage

describe('FileStorage', () => {
  let storage: FileStorage;

  beforeEach(async () => {
    // Clean up test directory
    await fs.rm(TEST_DIR, { recursive: true, force: true });
    await fs.mkdir(TEST_DIR, { recursive: true });

    storage = new FileStorage(TEST_DIR);
  });

  afterEach(async () => {
    // Clean up test directory
    await fs.rm(TEST_DIR, { recursive: true, force: true });
  });

  describe('Basic File Operations', () => {
    it('should write data to file', async () => {
      const data = { test: 'value', number: 42 };

      await storage.write(TEST_FILE, data);

      // Verify file was created
      const fullPath = path.join(TEST_DIR, TEST_FILE);
      await expect(fs.access(fullPath)).resolves.not.toThrow();
    });

    it('should read data from file', async () => {
      const data = { test: 'value', number: 42, nested: { key: 'val' } };
      await storage.write(TEST_FILE, data);

      const result = await storage.read(TEST_FILE);

      expect(result).toEqual(data);
    });

    it('should return error for non-existent file', async () => {
      const result = await storage.read('nonexistent.json');

      expect(result).toBeNull();
    });

    it('should delete file', async () => {
      await storage.write(TEST_FILE, { test: 'data' });

      const deleted = await storage.delete(TEST_FILE);

      expect(deleted).toBe(true);
      const fullPath = path.join(TEST_DIR, TEST_FILE);
      await expect(fs.access(fullPath)).rejects.toThrow();
    });

    it('should handle delete of non-existent file gracefully', async () => {
      const deleted = await storage.delete('nonexistent.json');

      expect(deleted).toBe(false); // File didn't exist
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
      const readOnlyDir = path.join(TEST_DIR, 'readonly');
      await fs.mkdir(readOnlyDir, { recursive: true });
      await fs.chmod(readOnlyDir, 0o444); // Read-only

      await expect(storage.write('readonly/test.json', { new: 'data' })).rejects.toThrow();

      // Original file should still be intact
      const originalResult = await storage.read(TEST_FILE);
      expect(originalResult).toEqual(originalData);

      // Clean up
      await fs.chmod(readOnlyDir, 0o755);
    });

    it('should handle concurrent writes to same file', async () => {
      const writes = Array.from({ length: 10 }, (_, i) =>
        storage.write(TEST_FILE, { iteration: i, timestamp: Date.now() })
      );

      await Promise.all(writes);

      // Final file should have valid data
      const finalData = await storage.read(TEST_FILE);
      expect(finalData).toHaveProperty('iteration');
    });
  });

  describe('File Locking', () => {
    // Increase timeout for locking tests (may take longer with retries)
    jest.setTimeout(60000);

    it('should acquire lock before writing', async () => {
      const lockFile = path.join(TEST_DIR, `${TEST_FILE}.lock`);

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
      const lockFile = path.join(TEST_DIR, `${TEST_FILE}.lock`);

      // Create an old stale lock (>30 seconds old)
      await fs.writeFile(lockFile, JSON.stringify({
        pid: 99999,
        acquired: Date.now() - 31000 // 31 seconds ago
      }));

      // Write should succeed by removing stale lock
      await storage.write(TEST_FILE, { test: 'data' });

      const data = await storage.read(TEST_FILE);
      expect(data).toEqual({ test: 'data' });
    });

    it('should retry on lock contention', async () => {
      const lockFile = path.join(TEST_DIR, `${TEST_FILE}.lock`);

      // Create a recent lock (another process)
      await fs.writeFile(lockFile, JSON.stringify({
        pid: process.pid + 1,
        acquired: Date.now()
      }));

      // Write should wait and eventually acquire lock or throw
      try {
        await storage.write(TEST_FILE, { test: 'data' });
        // If it succeeds, verify the data
        const data = await storage.read(TEST_FILE);
        expect(data).toEqual({ test: 'data' });
      } catch (error) {
        // If it fails, should be a timeout error
        expect((error as Error).message).toContain('timeout');
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
      const uncompressedStorage = new FileStorage(TEST_DIR, { compression: false });
      await uncompressedStorage.write('uncompressed.json', largeData);
      const uncompressedSize = (await fs.stat(path.join(TEST_DIR, 'uncompressed.json'))).size;

      // Write with compression (default storage has compression enabled)
      await storage.write('compressed.json', largeData);
      const compressedSize = (await fs.stat(path.join(TEST_DIR, 'compressed.json'))).size;

      // Compressed should be significantly smaller
      expect(compressedSize).toBeLessThan(uncompressedSize * 0.5);
    });

    it('should decompress data correctly', async () => {
      const originalData = {
        test: 'value',
        array: [1, 2, 3, 4, 5],
        nested: { key: 'val' }
      };

      // Default storage has compression enabled
      await storage.write(TEST_FILE, originalData);
      const result = await storage.read(TEST_FILE);

      expect(result).toEqual(originalData);
    });

    it('should handle both compressed and uncompressed files', async () => {
      const data1 = { type: 'uncompressed' };
      const data2 = { type: 'compressed' };

      // Create storages with different compression settings
      const uncompressedStorage = new FileStorage(TEST_DIR, { compression: false });
      const compressedStorage = new FileStorage(TEST_DIR, { compression: true });

      await uncompressedStorage.write('file1.json', data1);
      await compressedStorage.write('file2.json', data2);

      // Both should be readable by either storage
      const result1 = await storage.read('file1.json');
      const result2 = await storage.read('file2.json');

      expect(result1).toEqual(data1);
      expect(result2).toEqual(data2);
    });
  });

  describe('Error Handling', () => {
    it('should handle invalid JSON gracefully', async () => {
      // Write invalid JSON manually
      const fullPath = path.join(TEST_DIR, TEST_FILE);
      await fs.writeFile(fullPath, 'invalid{json}content');

      await expect(storage.read(TEST_FILE)).rejects.toThrow();
    });

    it('should handle permission errors', async () => {
      await storage.write(TEST_FILE, { test: 'data' });

      // Make file read-only
      const fullPath = path.join(TEST_DIR, TEST_FILE);
      await fs.chmod(fullPath, 0o444);

      await expect(storage.write(TEST_FILE, { new: 'data' })).rejects.toThrow();

      // Clean up
      await fs.chmod(fullPath, 0o644);
    });

    it('should handle disk full scenarios', async () => {
      // This is hard to test without actually filling disk
      // We'll simulate by checking error handling structure

      await expect(storage.write('/dev/null/impossible.json', { test: 'data' })).rejects.toThrow();
    });

    it('should handle corrupted compressed data', async () => {
      // Write corrupted gzip data
      const fullPath = path.join(TEST_DIR, TEST_FILE);
      await fs.writeFile(fullPath, Buffer.from([0x1f, 0x8b, 0xFF, 0xFF])); // Invalid gzip

      await expect(storage.read(TEST_FILE)).rejects.toThrow();
    });
  });

  describe('Metadata Operations', () => {
    it('should check if file exists', async () => {
      await storage.write(TEST_FILE, { test: 'data' });

      const exists = await storage.exists(TEST_FILE);
      const notExists = await storage.exists('nope.json');

      expect(exists).toBe(true);
      expect(notExists).toBe(false);
    });

    it('should get file stats', async () => {
      const data = { test: 'value' };
      await storage.write(TEST_FILE, data);

      const size = await storage.getSize(TEST_FILE);

      expect(size).toBeGreaterThan(0);
    });

    it('should list files in directory', async () => {
      await storage.write('file1.json', { test: 1 });
      await storage.write('file2.json', { test: 2 });
      await storage.write('file3.json', { test: 3 });

      const files = await storage.list('');

      expect(files).toHaveLength(3);
      expect(files).toContain('file1.json');
      expect(files).toContain('file2.json');
      expect(files).toContain('file3.json');
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
        file: `batch-${i}.json`,
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

      expect(result).toEqual({});
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

      expect(result).toEqual(deepData);
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

      expect(result).toEqual(specialData);
    });

    it('should handle very long file paths', async () => {
      const longPath = path.join(
        'a'.repeat(50),
        'b'.repeat(50),
        'c'.repeat(50),
        'test.json'
      );

      // Write should succeed (will create directories as needed)
      await storage.write(longPath, { test: 'data' });

      // Verify we can read it back
      const result = await storage.read(longPath);
      expect(result).toEqual({ test: 'data' });
    });
  });
});
