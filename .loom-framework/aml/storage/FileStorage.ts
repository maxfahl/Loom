/**
 * File Storage - Handles reading/writing JSON files with locking and compression
 */

import * as fs from 'fs/promises';
import * as path from 'path';
import * as lockfile from 'proper-lockfile';
import * as pako from 'pako';

export interface StorageOptions {
  compression?: boolean;
  encoding?: BufferEncoding;
  lockTimeout?: number;
  lockRetries?: number;
}

export class FileStorage {
  private basePath: string;
  private options: Required<StorageOptions>;

  constructor(basePath: string, options: StorageOptions = {}) {
    this.basePath = basePath;
    this.options = {
      compression: options.compression ?? true,
      encoding: options.encoding ?? 'utf-8',
      lockTimeout: options.lockTimeout ?? 10000,
      lockRetries: options.lockRetries ?? 20,
    };
  }

  /**
   * Read JSON data from file with optional compression support
   */
  async read<T>(filePath: string): Promise<T | null> {
    const fullPath = path.join(this.basePath, filePath);

    try {
      // Check if file exists
      await fs.access(fullPath);

      // Acquire lock for reading
      const release = await lockfile.lock(fullPath, {
        retries: {
          retries: this.options.lockRetries,
          maxTimeout: this.options.lockTimeout,
        },
        stale: 30000, // Locks older than 30s are stale
        realpath: false,
      });

      try {
        const rawData = await fs.readFile(fullPath);

        // Check if data is compressed (gzip magic number: 0x1f 0x8b)
        const isCompressed = rawData[0] === 0x1f && rawData[1] === 0x8b;

        let jsonString: string;
        if (isCompressed) {
          const decompressed = pako.ungzip(rawData);
          jsonString = new TextDecoder().decode(decompressed);
        } else {
          jsonString = rawData.toString(this.options.encoding);
        }

        return JSON.parse(jsonString) as T;
      } finally {
        await release();
      }
    } catch (error) {
      if ((error as NodeJS.ErrnoException).code === 'ENOENT') {
        return null; // File doesn't exist
      }
      throw new Error(`Failed to read ${filePath}: ${(error as Error).message}`);
    }
  }

  /**
   * Write JSON data to file with optional compression
   */
  async write<T>(filePath: string, data: T): Promise<void> {
    const fullPath = path.join(this.basePath, filePath);
    const dir = path.dirname(fullPath);

    try {
      // Ensure directory exists
      await fs.mkdir(dir, { recursive: true });

      // Acquire lock for writing
      const lockPath = `${fullPath}.lock`;
      await fs.mkdir(path.dirname(lockPath), { recursive: true });

      let release: (() => Promise<void>) | null = null;

      try {
        // Try to acquire lock
        release = await lockfile.lock(fullPath, {
          retries: {
            retries: this.options.lockRetries,
            maxTimeout: this.options.lockTimeout,
          },
          stale: 30000, // Locks older than 30s are stale
          realpath: false,
        });
      } catch (error) {
        // If file doesn't exist, we can't lock it, so proceed without lock
        if ((error as Error).message.includes('ENOENT')) {
          release = null;
        } else {
          throw error;
        }
      }

      try {
        const jsonString = JSON.stringify(data, null, 2);

        let buffer: Buffer;
        if (this.options.compression) {
          const compressed = pako.gzip(jsonString);
          buffer = Buffer.from(compressed);
        } else {
          buffer = Buffer.from(jsonString, this.options.encoding);
        }

        // Atomic write using temp file
        const tempPath = `${fullPath}.tmp`;
        await fs.writeFile(tempPath, buffer);
        await fs.rename(tempPath, fullPath);
      } finally {
        if (release) {
          await release();
        }
      }
    } catch (error) {
      throw new Error(`Failed to write ${filePath}: ${(error as Error).message}`);
    }
  }

  /**
   * Delete a file
   */
  async delete(filePath: string): Promise<boolean> {
    const fullPath = path.join(this.basePath, filePath);

    try {
      await fs.unlink(fullPath);
      return true;
    } catch (error) {
      if ((error as NodeJS.ErrnoException).code === 'ENOENT') {
        return false; // File didn't exist
      }
      throw new Error(`Failed to delete ${filePath}: ${(error as Error).message}`);
    }
  }

  /**
   * Check if file exists
   */
  async exists(filePath: string): Promise<boolean> {
    const fullPath = path.join(this.basePath, filePath);
    try {
      await fs.access(fullPath);
      return true;
    } catch {
      return false;
    }
  }

  /**
   * List files in directory
   */
  async list(dirPath: string = ''): Promise<string[]> {
    const fullPath = path.join(this.basePath, dirPath);

    try {
      const entries = await fs.readdir(fullPath, { withFileTypes: true });
      return entries.filter((entry) => entry.isFile()).map((entry) => entry.name);
    } catch (error) {
      if ((error as NodeJS.ErrnoException).code === 'ENOENT') {
        return [];
      }
      throw new Error(`Failed to list directory ${dirPath}: ${(error as Error).message}`);
    }
  }

  /**
   * Get file size in bytes
   */
  async getSize(filePath: string): Promise<number> {
    const fullPath = path.join(this.basePath, filePath);

    try {
      const stats = await fs.stat(fullPath);
      return stats.size;
    } catch (error) {
      if ((error as NodeJS.ErrnoException).code === 'ENOENT') {
        return 0;
      }
      throw new Error(`Failed to get size of ${filePath}: ${(error as Error).message}`);
    }
  }

  /**
   * Get total size of directory in bytes
   */
  async getDirectorySize(dirPath: string = ''): Promise<number> {
    try {
      const files = await this.listRecursive(dirPath);
      let totalSize = 0;

      for (const file of files) {
        totalSize += await this.getSize(path.join(dirPath, file));
      }

      return totalSize;
    } catch (error) {
      throw new Error(
        `Failed to get directory size for ${dirPath}: ${(error as Error).message}`
      );
    }
  }

  /**
   * List files recursively
   */
  async listRecursive(dirPath: string = ''): Promise<string[]> {
    const fullPath = path.join(this.basePath, dirPath);
    const files: string[] = [];

    try {
      const entries = await fs.readdir(fullPath, { withFileTypes: true });

      for (const entry of entries) {
        const relativePath = path.join(dirPath, entry.name);

        if (entry.isFile()) {
          files.push(entry.name);
        } else if (entry.isDirectory()) {
          const subFiles = await this.listRecursive(relativePath);
          files.push(...subFiles.map((f) => path.join(entry.name, f)));
        }
      }

      return files;
    } catch (error) {
      if ((error as NodeJS.ErrnoException).code === 'ENOENT') {
        return [];
      }
      throw new Error(`Failed to list directory recursively ${dirPath}: ${(error as Error).message}`);
    }
  }

  /**
   * Create backup of a file
   */
  async backup(filePath: string, backupPath?: string): Promise<string> {
    const fullPath = path.join(this.basePath, filePath);
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    const defaultBackupPath = `${filePath}.backup-${timestamp}`;
    const targetPath = backupPath || defaultBackupPath;
    const fullBackupPath = path.join(this.basePath, targetPath);

    try {
      await fs.mkdir(path.dirname(fullBackupPath), { recursive: true });
      await fs.copyFile(fullPath, fullBackupPath);
      return targetPath;
    } catch (error) {
      throw new Error(`Failed to backup ${filePath}: ${(error as Error).message}`);
    }
  }

  /**
   * Restore from backup
   */
  async restore(backupPath: string, targetPath: string): Promise<void> {
    const fullBackupPath = path.join(this.basePath, backupPath);
    const fullTargetPath = path.join(this.basePath, targetPath);

    try {
      await fs.mkdir(path.dirname(fullTargetPath), { recursive: true });
      await fs.copyFile(fullBackupPath, fullTargetPath);
    } catch (error) {
      throw new Error(
        `Failed to restore from ${backupPath} to ${targetPath}: ${(error as Error).message}`
      );
    }
  }

  /**
   * Get base path
   */
  getBasePath(): string {
    return this.basePath;
  }

  /**
   * Initialize storage (create base directory)
   */
  async initialize(): Promise<void> {
    try {
      await fs.mkdir(this.basePath, { recursive: true });
    } catch (error) {
      throw new Error(`Failed to initialize storage: ${(error as Error).message}`);
    }
  }
}
