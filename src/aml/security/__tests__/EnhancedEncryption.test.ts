/**
 * EnhancedEncryption Test Suite
 */

import { describe, it, expect } from '@jest/globals';
import { EnhancedEncryption } from '../EnhancedEncryption';

describe('EnhancedEncryption', () => {
  let encryption: EnhancedEncryption;

  beforeEach(() => {
    encryption = new EnhancedEncryption();
  });

  describe('AES-256-GCM Encryption', () => {
    it('should encrypt and decrypt data correctly', async () => {
      const data = { sensitive: 'data', value: 12345 };
      const password = 'test-password';

      const encrypted = await encryption.encrypt(data, password);
      const decrypted = await encryption.decrypt(encrypted, password);

      expect(decrypted).toEqual(data);
    });

    it('should produce different ciphertext for same data', async () => {
      const data = { test: 'value' };
      const password = 'password';

      const encrypted1 = await encryption.encrypt(data, password);
      const encrypted2 = await encryption.encrypt(data, password);

      expect(encrypted1).not.toBe(encrypted2); // Different due to unique IV
    });

    it('should fail with wrong password', async () => {
      const data = { secret: 'data' };
      const encrypted = await encryption.encrypt(data, 'correct-password');

      await expect(
        encryption.decrypt(encrypted, 'wrong-password')
      ).rejects.toThrow();
    });
  });

  describe('HMAC Integrity Verification', () => {
    it('should detect tampered data', async () => {
      const data = { value: 'original' };
      const password = 'password';

      const encrypted = await encryption.encrypt(data, password);

      // Tamper with ciphertext
      const tampered = encrypted.slice(0, -10) + 'tampered!!';

      await expect(
        encryption.decrypt(tampered, password)
      ).rejects.toThrow(/integrity/i);
    });

    it('should verify untampered data', async () => {
      const data = { value: 'original' };
      const password = 'password';

      const encrypted = await encryption.encrypt(data, password);
      const isValid = await encryption.verifyIntegrity(encrypted);

      expect(isValid).toBe(true);
    });
  });

  describe('Key Derivation', () => {
    it('should derive same key from same password', async () => {
      const password = 'test-password';
      const salt = 'test-salt';

      const key1 = await encryption.deriveKey(password, salt);
      const key2 = await encryption.deriveKey(password, salt);

      expect(key1).toEqual(key2);
    });

    it('should derive different keys with different salts', async () => {
      const password = 'test-password';

      const key1 = await encryption.deriveKey(password, 'salt1');
      const key2 = await encryption.deriveKey(password, 'salt2');

      expect(key1).not.toEqual(key2);
    });
  });

  describe('Performance', () => {
    it('should encrypt 10KB in <5ms', async () => {
      const data = { content: 'x'.repeat(10000) };
      const password = 'password';

      const start = Date.now();
      await encryption.encrypt(data, password);
      const duration = Date.now() - start;

      expect(duration).toBeLessThan(5);
    });

    it('should decrypt 10KB in <5ms', async () => {
      const data = { content: 'x'.repeat(10000) };
      const password = 'password';

      const encrypted = await encryption.encrypt(data, password);

      const start = Date.now();
      await encryption.decrypt(encrypted, password);
      const duration = Date.now() - start;

      expect(duration).toBeLessThan(5);
    });
  });
});
