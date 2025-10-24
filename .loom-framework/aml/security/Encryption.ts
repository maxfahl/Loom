/**
 * Encryption - AES-256-GCM encryption for sensitive memory data
 */

import * as crypto from 'crypto';

export interface EncryptionOptions {
  algorithm?: string;
  keyLength?: number;
  ivLength?: number;
  authTagLength?: number;
}

export interface EncryptedData {
  encrypted: string; // Base64 encoded
  iv: string; // Base64 encoded initialization vector
  authTag: string; // Base64 encoded authentication tag
  algorithm: string;
}

export class Encryption {
  private algorithm: string;
  private keyLength: number;
  private ivLength: number;
  private key: Buffer | null = null;

  constructor(options: EncryptionOptions = {}) {
    this.algorithm = options.algorithm || 'aes-256-gcm';
    this.keyLength = options.keyLength || 32; // 256 bits
    this.ivLength = options.ivLength || 16; // 128 bits
  }

  /**
   * Set encryption key
   */
  setKey(key: string | Buffer): void {
    if (typeof key === 'string') {
      // Derive key from password using PBKDF2
      this.key = crypto.pbkdf2Sync(key, 'loom-aml-salt', 100000, this.keyLength, 'sha512');
    } else {
      if (key.length !== this.keyLength) {
        throw new Error(`Key must be ${this.keyLength} bytes long`);
      }
      this.key = key;
    }
  }

  /**
   * Generate a random encryption key
   */
  generateKey(): Buffer {
    return crypto.randomBytes(this.keyLength);
  }

  /**
   * Encrypt data
   */
  encrypt(data: string): EncryptedData {
    if (!this.key) {
      throw new Error('Encryption key not set. Call setKey() first.');
    }

    try {
      // Generate random IV
      const iv = crypto.randomBytes(this.ivLength);

      // Create cipher
      const cipher = crypto.createCipheriv(this.algorithm, this.key, iv);

      // Encrypt data
      let encrypted = cipher.update(data, 'utf8', 'base64');
      encrypted += cipher.final('base64');

      // Get authentication tag
      const authTag = (cipher as any).getAuthTag();

      return {
        encrypted,
        iv: iv.toString('base64'),
        authTag: authTag.toString('base64'),
        algorithm: this.algorithm,
      };
    } catch (error) {
      throw new Error(`Encryption failed: ${(error as Error).message}`);
    }
  }

  /**
   * Decrypt data
   */
  decrypt(encryptedData: EncryptedData): string {
    if (!this.key) {
      throw new Error('Encryption key not set. Call setKey() first.');
    }

    try {
      // Parse IV and auth tag
      const iv = Buffer.from(encryptedData.iv, 'base64');
      const authTag = Buffer.from(encryptedData.authTag, 'base64');

      // Create decipher
      const decipher = crypto.createDecipheriv(this.algorithm, this.key, iv);

      // Set authentication tag
      (decipher as any).setAuthTag(authTag);

      // Decrypt data
      let decrypted = decipher.update(encryptedData.encrypted, 'base64', 'utf8');
      decrypted += decipher.final('utf8');

      return decrypted;
    } catch (error) {
      throw new Error(`Decryption failed: ${(error as Error).message}`);
    }
  }

  /**
   * Encrypt object to JSON
   */
  encryptObject<T>(obj: T): EncryptedData {
    const jsonString = JSON.stringify(obj);
    return this.encrypt(jsonString);
  }

  /**
   * Decrypt JSON to object
   */
  decryptObject<T>(encryptedData: EncryptedData): T {
    const jsonString = this.decrypt(encryptedData);
    return JSON.parse(jsonString) as T;
  }

  /**
   * Hash data using SHA-256
   */
  static hash(data: string): string {
    return crypto.createHash('sha256').update(data).digest('hex');
  }

  /**
   * Generate random token
   */
  static generateToken(length: number = 32): string {
    return crypto.randomBytes(length).toString('hex');
  }

  /**
   * Verify if key is set
   */
  isKeySet(): boolean {
    return this.key !== null;
  }

  /**
   * Clear encryption key from memory
   */
  clearKey(): void {
    if (this.key) {
      this.key.fill(0); // Zero out key bytes
      this.key = null;
    }
  }
}
