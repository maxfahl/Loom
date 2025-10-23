/**
 * Enhanced Encryption - AES-256-GCM with HMAC integrity, key rotation, and context separation
 *
 * Security Features:
 * - AES-256-GCM authenticated encryption
 * - HMAC-SHA256 integrity verification (defense in depth)
 * - PBKDF2 key derivation with context separation
 * - Automatic key rotation support
 * - Backward compatibility with legacy format
 * - Secure memory management
 *
 * Performance Targets:
 * - Encryption: <5ms for 10KB
 * - Key derivation: <100ms (with caching)
 * - Total overhead: <5%
 */

import * as crypto from 'crypto';
import { KeychainManager } from './KeychainManager';

/**
 * Enhanced encrypted data format (v2)
 */
export interface EnhancedEncryptedData {
  version: number;              // Format version (2 for enhanced)
  algorithm: string;            // 'aes-256-gcm'
  kdf: string;                  // 'pbkdf2-sha256'
  kdf_iterations: number;       // PBKDF2 iterations (100,000+)
  salt: string;                 // Base64 salt for KDF
  iv: string;                   // Base64 IV
  authTag: string;              // Base64 GCM auth tag
  ciphertext: string;           // Base64 encrypted data
  hmac: string;                 // Base64 HMAC-SHA256 for defense in depth
  timestamp: string;            // ISO timestamp
  context?: string;             // Optional context for key separation
}

/**
 * Legacy encrypted data format (v1) - for backward compatibility
 */
export interface LegacyEncryptedData {
  encrypted: string;
  iv: string;
  authTag: string;
  algorithm: string;
}

/**
 * Derived key cache entry
 */
interface KeyCacheEntry {
  key: Buffer;
  expiresAt: number;
}

/**
 * Enhanced encryption service with production-grade security
 */
export class EnhancedEncryption {
  private readonly VERSION = 2;
  private readonly ALGORITHM = 'aes-256-gcm';
  private readonly KDF_ALGORITHM = 'pbkdf2-sha256';
  private readonly KDF_ITERATIONS = 100000;  // OWASP recommendation
  private readonly IV_LENGTH = 12;            // 96 bits for GCM
  private readonly AUTH_TAG_LENGTH = 16;      // 128 bits
  private readonly SALT_LENGTH = 32;          // 256 bits
  private readonly KEY_LENGTH = 32;           // 256 bits for AES-256
  private readonly KEY_CACHE_TTL = 5 * 60 * 1000; // 5 minutes

  private keychainManager: KeychainManager;
  private masterKey: Buffer | null = null;
  private keyCache: Map<string, KeyCacheEntry> = new Map();

  constructor() {
    this.keychainManager = new KeychainManager();
  }

  /**
   * Initialize encryption service with master key from OS keychain
   */
  async initialize(): Promise<void> {
    this.masterKey = await this.keychainManager.getOrCreateMasterKey();
  }

  /**
   * Encrypt data with enhanced security
   *
   * @param data - Plaintext data to encrypt
   * @param context - Optional context for key derivation (e.g., agent name, project ID)
   * @returns Enhanced encrypted data structure
   */
  async encrypt(data: string, context?: string): Promise<EnhancedEncryptedData> {
    if (!this.masterKey) {
      await this.initialize();
    }

    const startTime = Date.now();

    try {
      // 1. Generate random salt for key derivation
      const salt = crypto.randomBytes(this.SALT_LENGTH);

      // 2. Derive encryption key with context separation
      const derivedKey = this.deriveKey(this.masterKey!, salt, context);

      // 3. Generate random IV (NEVER reuse!)
      const iv = crypto.randomBytes(this.IV_LENGTH);

      // 4. Encrypt with AES-256-GCM
      const cipher = crypto.createCipheriv(this.ALGORITHM, derivedKey, iv, {
        authTagLength: this.AUTH_TAG_LENGTH
      });

      const ciphertext = Buffer.concat([
        cipher.update(data, 'utf8'),
        cipher.final()
      ]);

      // 5. Get GCM authentication tag
      const authTag = cipher.getAuthTag();

      // 6. Generate HMAC for defense in depth
      const hmac = this.generateHMAC(ciphertext, derivedKey);

      // 7. Wipe derived key from memory
      derivedKey.fill(0);

      const encryptionTime = Date.now() - startTime;
      if (encryptionTime > 5 && data.length <= 10240) {
        console.warn(`⚠️  Encryption took ${encryptionTime}ms for ${data.length} bytes (target: <5ms for 10KB)`);
      }

      // 8. Return encrypted data
      return {
        version: this.VERSION,
        algorithm: this.ALGORITHM,
        kdf: this.KDF_ALGORITHM,
        kdf_iterations: this.KDF_ITERATIONS,
        salt: salt.toString('base64'),
        iv: iv.toString('base64'),
        authTag: authTag.toString('base64'),
        ciphertext: ciphertext.toString('base64'),
        hmac: hmac.toString('base64'),
        timestamp: new Date().toISOString(),
        context
      };
    } catch (error) {
      // Don't leak plaintext in error messages
      throw new Error(`Encryption failed: ${(error as Error).message}`);
    }
  }

  /**
   * Decrypt data (supports both v2 and v1 formats)
   *
   * @param encryptedData - Encrypted data structure
   * @returns Decrypted plaintext
   * @throws Error if decryption or authentication fails
   */
  async decrypt(encryptedData: EnhancedEncryptedData | LegacyEncryptedData): Promise<string> {
    if (!this.masterKey) {
      await this.initialize();
    }

    // Check format version
    if ('version' in encryptedData && encryptedData.version === this.VERSION) {
      return this.decryptV2(encryptedData as EnhancedEncryptedData);
    } else {
      // Legacy format (v1)
      return this.decryptV1(encryptedData as LegacyEncryptedData);
    }
  }

  /**
   * Decrypt v2 format with HMAC verification
   */
  private async decryptV2(encryptedData: EnhancedEncryptedData): Promise<string> {
    try {
      // 1. Parse encrypted components
      const salt = Buffer.from(encryptedData.salt, 'base64');
      const iv = Buffer.from(encryptedData.iv, 'base64');
      const authTag = Buffer.from(encryptedData.authTag, 'base64');
      const ciphertext = Buffer.from(encryptedData.ciphertext, 'base64');
      const expectedHMAC = Buffer.from(encryptedData.hmac, 'base64');

      // 2. Derive same encryption key
      const derivedKey = this.deriveKey(this.masterKey!, salt, encryptedData.context);

      // 3. Verify HMAC first (fail fast if tampered)
      if (!this.verifyHMAC(ciphertext, derivedKey, expectedHMAC)) {
        derivedKey.fill(0);
        throw new Error('HMAC verification failed - data may be tampered');
      }

      // 4. Decrypt with AES-256-GCM
      const decipher = crypto.createDecipheriv(this.ALGORITHM, derivedKey, iv, {
        authTagLength: this.AUTH_TAG_LENGTH
      });

      decipher.setAuthTag(authTag);

      const plaintext = Buffer.concat([
        decipher.update(ciphertext),
        decipher.final()
      ]).toString('utf8');

      // 5. Wipe derived key
      derivedKey.fill(0);

      return plaintext;
    } catch (error) {
      // Don't leak ciphertext in error messages
      throw new Error(`Decryption failed: ${(error as Error).message}`);
    }
  }

  /**
   * Decrypt v1 format (backward compatibility)
   */
  private async decryptV1(encryptedData: LegacyEncryptedData): Promise<string> {
    if (!this.masterKey) {
      throw new Error('Master key not initialized');
    }

    try {
      const iv = Buffer.from(encryptedData.iv, 'base64');
      const authTag = Buffer.from(encryptedData.authTag, 'base64');
      const encrypted = Buffer.from(encryptedData.encrypted, 'base64');

      // Use master key directly (legacy behavior)
      const decipher = crypto.createDecipheriv(this.ALGORITHM, this.masterKey, iv, {
        authTagLength: this.AUTH_TAG_LENGTH
      });

      decipher.setAuthTag(authTag);

      const plaintext = Buffer.concat([
        decipher.update(encrypted),
        decipher.final()
      ]).toString('utf8');

      return plaintext;
    } catch (error) {
      throw new Error(`Legacy decryption failed: ${(error as Error).message}`);
    }
  }

  /**
   * Derive encryption key from master key using PBKDF2 with context separation
   *
   * @param masterKey - Master key from OS keychain
   * @param salt - Random salt
   * @param context - Optional context for key separation
   * @returns Derived encryption key
   */
  private deriveKey(masterKey: Buffer, salt: Buffer, context?: string): Buffer {
    // Check cache first
    const cacheKey = this.getCacheKey(salt, context);
    const cached = this.keyCache.get(cacheKey);

    if (cached && Date.now() < cached.expiresAt) {
      return Buffer.from(cached.key); // Return copy
    }

    const startTime = Date.now();

    // Apply context-based key separation if provided
    let derivationInput = masterKey;

    if (context) {
      // Hash context and XOR with master key
      const contextHash = crypto.createHash('sha256').update(context).digest();

      derivationInput = Buffer.alloc(this.KEY_LENGTH);
      for (let i = 0; i < this.KEY_LENGTH; i++) {
        derivationInput[i] = masterKey[i] ^ contextHash[i];
      }
    }

    // Derive key using PBKDF2
    const derivedKey = crypto.pbkdf2Sync(
      derivationInput,
      salt,
      this.KDF_ITERATIONS,
      this.KEY_LENGTH,
      'sha256'
    );

    // Wipe temporary input
    if (context && derivationInput !== masterKey) {
      derivationInput.fill(0);
    }

    const derivationTime = Date.now() - startTime;
    if (derivationTime > 100) {
      console.warn(`⚠️  Key derivation took ${derivationTime}ms (target: <100ms)`);
    }

    // Cache the derived key
    this.keyCache.set(cacheKey, {
      key: Buffer.from(derivedKey),
      expiresAt: Date.now() + this.KEY_CACHE_TTL
    });

    // Clean up old cache entries
    this.cleanupKeyCache();

    return derivedKey;
  }

  /**
   * Generate HMAC-SHA256 for integrity verification
   */
  private generateHMAC(data: Buffer, key: Buffer): Buffer {
    const hmac = crypto.createHmac('sha256', key);
    hmac.update(data);
    return hmac.digest();
  }

  /**
   * Verify HMAC using constant-time comparison
   */
  private verifyHMAC(data: Buffer, key: Buffer, expectedHMAC: Buffer): boolean {
    const actualHMAC = this.generateHMAC(data, key);

    // Constant-time comparison to prevent timing attacks
    try {
      return crypto.timingSafeEqual(actualHMAC, expectedHMAC);
    } catch {
      return false; // Length mismatch
    }
  }

  /**
   * Get cache key for derived key
   */
  private getCacheKey(salt: Buffer, context?: string): string {
    const saltHex = salt.toString('hex');
    return context ? `${saltHex}:${context}` : saltHex;
  }

  /**
   * Clean up expired cache entries
   */
  private cleanupKeyCache(): void {
    const now = Date.now();

    for (const [key, entry] of this.keyCache.entries()) {
      if (now >= entry.expiresAt) {
        // Wipe key before deleting
        entry.key.fill(0);
        this.keyCache.delete(key);
      }
    }
  }

  /**
   * Encrypt object to JSON
   */
  async encryptObject<T>(obj: T, context?: string): Promise<EnhancedEncryptedData> {
    const jsonString = JSON.stringify(obj);
    return this.encrypt(jsonString, context);
  }

  /**
   * Decrypt JSON to object
   */
  async decryptObject<T>(encryptedData: EnhancedEncryptedData | LegacyEncryptedData): Promise<T> {
    const jsonString = await this.decrypt(encryptedData);
    return JSON.parse(jsonString) as T;
  }

  /**
   * Rotate master encryption key
   *
   * @returns New master key
   */
  async rotateMasterKey(): Promise<Buffer> {
    const newKey = await this.keychainManager.rotateKey('master', `master-${Date.now()}`);

    // Update in-memory key
    if (this.masterKey) {
      this.masterKey.fill(0);
    }
    this.masterKey = newKey;

    // Clear key cache (keys derived from old master)
    this.clearKeyCache();

    return Buffer.from(newKey); // Return copy
  }

  /**
   * Clear all cached derived keys from memory
   */
  clearKeyCache(): void {
    for (const entry of this.keyCache.values()) {
      entry.key.fill(0);
    }
    this.keyCache.clear();
  }

  /**
   * Clear master key from memory
   */
  clearMasterKey(): void {
    if (this.masterKey) {
      this.masterKey.fill(0);
      this.masterKey = null;
    }
    this.clearKeyCache();
  }

  /**
   * Static hash function using SHA-256
   */
  static hash(data: string): string {
    return crypto.createHash('sha256').update(data).digest('hex');
  }

  /**
   * Static token generation
   */
  static generateToken(length: number = 32): string {
    return crypto.randomBytes(length).toString('hex');
  }
}
