/**
 * KeychainManager - Cross-platform OS keychain integration for secure key storage
 *
 * Supports:
 * - macOS: Keychain Access
 * - Windows: DPAPI (Data Protection API)
 * - Linux: libsecret (GNOME Keyring / KDE Wallet)
 *
 * Fallback: Environment variable with security warning
 */

import * as crypto from 'crypto';
import * as os from 'os';
import { execSync } from 'child_process';
import * as fs from 'fs';
import * as path from 'path';

/**
 * Security error for keychain operations
 */
export class KeychainError extends Error {
  constructor(message: string, public readonly code: string) {
    super(message);
    this.name = 'KeychainError';
  }
}

/**
 * Keychain operation result
 */
export interface KeychainResult {
  success: boolean;
  message?: string;
}

/**
 * Cross-platform keychain manager
 */
export class KeychainManager {
  private readonly FALLBACK_ENV_VAR = 'LOOM_AML_MASTER_KEY';
  private readonly KEY_LENGTH = 32; // 256 bits

  private platform: NodeJS.Platform;
  private backend: MacOSKeychain | WindowsDPAPI | LinuxSecretService | FallbackKeyStore;

  constructor() {
    this.platform = os.platform();

    const serviceName = 'com.loom.aml';
    const accountName = 'master-encryption-key';

    // Initialize platform-specific backend
    switch (this.platform) {
      case 'darwin':
        this.backend = new MacOSKeychain(serviceName, accountName);
        break;
      case 'win32':
        this.backend = new WindowsDPAPI(serviceName, accountName);
        break;
      case 'linux':
        this.backend = new LinuxSecretService(serviceName, accountName);
        break;
      default:
        console.warn(`⚠️  Unsupported platform: ${this.platform}. Using fallback key storage.`);
        this.backend = new FallbackKeyStore(this.FALLBACK_ENV_VAR);
    }
  }

  /**
   * Store encryption key in OS keychain
   *
   * @param keyId - Unique identifier for the key (e.g., 'master', 'backup')
   * @param key - Encryption key (32 bytes)
   * @throws KeychainError if storage fails
   */
  async storeKey(keyId: string, key: Buffer): Promise<void> {
    // Validate inputs
    this.validateKeyId(keyId);
    this.validateKey(key);

    try {
      await this.backend.store(keyId, key);
    } catch (error) {
      throw new KeychainError(
        `Failed to store key '${keyId}': ${(error as Error).message}`,
        'STORE_FAILED'
      );
    }
  }

  /**
   * Retrieve encryption key from OS keychain
   *
   * @param keyId - Unique identifier for the key
   * @returns Encryption key (32 bytes)
   * @throws KeychainError if retrieval fails
   */
  async retrieveKey(keyId: string): Promise<Buffer> {
    this.validateKeyId(keyId);

    try {
      const key = await this.backend.retrieve(keyId);
      this.validateKey(key);
      return key;
    } catch (error) {
      throw new KeychainError(
        `Failed to retrieve key '${keyId}': ${(error as Error).message}`,
        'RETRIEVE_FAILED'
      );
    }
  }

  /**
   * Delete encryption key from OS keychain
   *
   * @param keyId - Unique identifier for the key
   */
  async deleteKey(keyId: string): Promise<void> {
    this.validateKeyId(keyId);

    try {
      await this.backend.delete(keyId);
    } catch (error) {
      // Ignore deletion errors (key might not exist)
      console.warn(`Warning: Could not delete key '${keyId}': ${(error as Error).message}`);
    }
  }

  /**
   * Rotate encryption key
   *
   * @param oldKeyId - Current key identifier
   * @param newKeyId - New key identifier
   * @returns New encryption key
   */
  async rotateKey(oldKeyId: string, newKeyId: string): Promise<Buffer> {
    this.validateKeyId(oldKeyId);
    this.validateKeyId(newKeyId);

    try {
      // Generate new key
      const newKey = crypto.randomBytes(this.KEY_LENGTH);

      // Store new key
      await this.storeKey(newKeyId, newKey);

      // Verify new key was stored
      const verified = await this.retrieveKey(newKeyId);
      if (!verified.equals(newKey)) {
        throw new Error('Key verification failed after storage');
      }

      // Delete old key (optional, keep for rollback)
      // await this.deleteKey(oldKeyId);

      return newKey;
    } catch (error) {
      throw new KeychainError(
        `Key rotation failed: ${(error as Error).message}`,
        'ROTATION_FAILED'
      );
    }
  }

  /**
   * Check if key exists in keychain
   *
   * @param keyId - Unique identifier for the key
   * @returns true if key exists, false otherwise
   */
  async hasKey(keyId: string): Promise<boolean> {
    this.validateKeyId(keyId);

    try {
      await this.retrieveKey(keyId);
      return true;
    } catch {
      return false;
    }
  }

  /**
   * Get or create master encryption key
   *
   * @returns Master encryption key (32 bytes)
   */
  async getOrCreateMasterKey(): Promise<Buffer> {
    const keyId = 'master';

    try {
      // Try to retrieve existing key
      return await this.retrieveKey(keyId);
    } catch {
      // Generate and store new key
      const newKey = crypto.randomBytes(this.KEY_LENGTH);
      await this.storeKey(keyId, newKey);

      console.log('✓ Generated new master encryption key');

      return newKey;
    }
  }

  /**
   * Get platform information
   */
  getPlatformInfo(): { platform: string; backend: string; secure: boolean } {
    return {
      platform: this.platform,
      backend: this.backend.constructor.name,
      secure: !(this.backend instanceof FallbackKeyStore)
    };
  }

  /**
   * Validate key ID format
   */
  private validateKeyId(keyId: string): void {
    if (!keyId || typeof keyId !== 'string') {
      throw new KeychainError('Key ID must be a non-empty string', 'INVALID_KEY_ID');
    }

    // Only allow alphanumeric, hyphens, and underscores
    if (!/^[a-zA-Z0-9_-]+$/.test(keyId)) {
      throw new KeychainError(
        'Key ID must contain only alphanumeric characters, hyphens, and underscores',
        'INVALID_KEY_ID'
      );
    }

    if (keyId.length > 100) {
      throw new KeychainError('Key ID must be 100 characters or less', 'INVALID_KEY_ID');
    }
  }

  /**
   * Validate encryption key
   */
  private validateKey(key: Buffer): void {
    if (!Buffer.isBuffer(key)) {
      throw new KeychainError('Key must be a Buffer', 'INVALID_KEY');
    }

    if (key.length !== this.KEY_LENGTH) {
      throw new KeychainError(
        `Key must be exactly ${this.KEY_LENGTH} bytes (got ${key.length})`,
        'INVALID_KEY_LENGTH'
      );
    }

    // Check for all-zero key (security risk)
    const isAllZero = key.every(byte => byte === 0);
    if (isAllZero) {
      throw new KeychainError('Key cannot be all zeros', 'WEAK_KEY');
    }
  }
}

/**
 * Base interface for keychain backends
 */
interface KeychainBackend {
  store(keyId: string, key: Buffer): Promise<void>;
  retrieve(keyId: string): Promise<Buffer>;
  delete(keyId: string): Promise<void>;
}

/**
 * macOS Keychain backend
 */
class MacOSKeychain implements KeychainBackend {
  constructor(
    private serviceName: string,
    private accountName: string
  ) {}

  async store(keyId: string, key: Buffer): Promise<void> {
    const keyBase64 = key.toString('base64');
    const account = `${this.accountName}-${keyId}`;

    try {
      // Delete existing key first (security add-generic-password fails if exists)
      await this.delete(keyId);
    } catch {
      // Ignore if doesn't exist
    }

    // Store in keychain using security command
    const command = `security add-generic-password -a "${account}" -s "${this.serviceName}" -w "${keyBase64}" -U`;

    try {
      execSync(command, { stdio: 'pipe' });
    } catch (error) {
      throw new Error(`macOS Keychain storage failed: ${(error as Error).message}`);
    }

    // Wipe sensitive data from memory
    this.wipeString(keyBase64);
  }

  async retrieve(keyId: string): Promise<Buffer> {
    const account = `${this.accountName}-${keyId}`;
    const command = `security find-generic-password -a "${account}" -s "${this.serviceName}" -w`;

    try {
      const keyBase64 = execSync(command, {
        encoding: 'utf8',
        stdio: ['pipe', 'pipe', 'pipe']
      }).trim();

      const key = Buffer.from(keyBase64, 'base64');

      // Wipe base64 string
      this.wipeString(keyBase64);

      return key;
    } catch (error) {
      throw new Error(`macOS Keychain retrieval failed: ${(error as Error).message}`);
    }
  }

  async delete(keyId: string): Promise<void> {
    const account = `${this.accountName}-${keyId}`;
    const command = `security delete-generic-password -a "${account}" -s "${this.serviceName}"`;

    try {
      execSync(command, { stdio: 'pipe' });
    } catch {
      // Ignore errors (key might not exist)
    }
  }

  private wipeString(str: string): void {
    // Attempt to wipe string from memory (best effort)
    if (typeof str === 'string') {
      // This doesn't truly wipe immutable strings, but it's a signal
      str = '';
    }
  }
}

/**
 * Windows DPAPI backend
 */
class WindowsDPAPI implements KeychainBackend {
  constructor(
    _serviceName: string,
    _accountName: string
  ) {
    // serviceName and accountName are not used by Windows DPAPI
    // (kept for interface consistency)
  }

  async store(keyId: string, key: Buffer): Promise<void> {
    const keyHex = key.toString('hex');
    const keyPath = this.getKeyPath(keyId);

    // PowerShell script to encrypt and store using DPAPI
    const psScript = `
      $key = "${keyHex}"
      $secureKey = ConvertTo-SecureString -String $key -AsPlainText -Force
      $encrypted = ConvertFrom-SecureString -SecureString $secureKey

      # Ensure directory exists
      $dir = Split-Path -Path "${keyPath}"
      if (-not (Test-Path $dir)) {
        New-Item -Path $dir -ItemType Directory -Force | Out-Null
      }

      # Write encrypted key
      Set-Content -Path "${keyPath}" -Value $encrypted -Force
    `.replace(/\n/g, '; ');

    try {
      execSync(`powershell -Command "${psScript}"`, { stdio: 'pipe' });
    } catch (error) {
      throw new Error(`Windows DPAPI storage failed: ${(error as Error).message}`);
    }

    // Wipe hex string
    this.wipeString(keyHex);
  }

  async retrieve(keyId: string): Promise<Buffer> {
    const keyPath = this.getKeyPath(keyId);

    // PowerShell script to retrieve and decrypt using DPAPI
    const psScript = `
      if (-not (Test-Path "${keyPath}")) {
        throw "Key not found"
      }

      $encrypted = Get-Content -Path "${keyPath}"
      $secureKey = ConvertTo-SecureString -String $encrypted
      $ptr = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($secureKey)
      $key = [System.Runtime.InteropServices.Marshal]::PtrToStringBSTR($ptr)
      [System.Runtime.InteropServices.Marshal]::ZeroFreeBSTR($ptr)
      Write-Output $key
    `.replace(/\n/g, '; ');

    try {
      const keyHex = execSync(`powershell -Command "${psScript}"`, {
        encoding: 'utf8',
        stdio: ['pipe', 'pipe', 'pipe']
      }).trim();

      const key = Buffer.from(keyHex, 'hex');

      // Wipe hex string
      this.wipeString(keyHex);

      return key;
    } catch (error) {
      throw new Error(`Windows DPAPI retrieval failed: ${(error as Error).message}`);
    }
  }

  async delete(keyId: string): Promise<void> {
    const keyPath = this.getKeyPath(keyId);

    try {
      if (fs.existsSync(keyPath)) {
        fs.unlinkSync(keyPath);
      }
    } catch {
      // Ignore errors
    }
  }

  private getKeyPath(keyId: string): string {
    const appData = process.env.LOCALAPPDATA || path.join(os.homedir(), 'AppData', 'Local');
    return path.join(appData, 'Loom', 'AML', `${keyId}.key`);
  }

  private wipeString(str: string): void {
    if (typeof str === 'string') {
      str = '';
    }
  }
}

/**
 * Linux Secret Service backend (libsecret)
 */
class LinuxSecretService implements KeychainBackend {
  constructor(
    private serviceName: string,
    private accountName: string
  ) {}

  async store(keyId: string, key: Buffer): Promise<void> {
    const keyBase64 = key.toString('base64');
    const label = `Loom AML - ${keyId}`;
    const attribute = `${this.accountName}-${keyId}`;

    // Use secret-tool (part of libsecret)
    const command = `echo "${keyBase64}" | secret-tool store --label="${label}" ${this.serviceName} ${attribute}`;

    try {
      execSync(command, { stdio: 'pipe', shell: '/bin/bash' });
    } catch (error) {
      // Check if secret-tool is installed
      try {
        execSync('which secret-tool', { stdio: 'pipe' });
      } catch {
        throw new Error(
          'secret-tool not found. Please install libsecret-tools: sudo apt-get install libsecret-tools'
        );
      }

      throw new Error(`Linux Secret Service storage failed: ${(error as Error).message}`);
    }

    // Wipe sensitive data
    this.wipeString(keyBase64);
  }

  async retrieve(keyId: string): Promise<Buffer> {
    const attribute = `${this.accountName}-${keyId}`;
    const command = `secret-tool lookup ${this.serviceName} ${attribute}`;

    try {
      const keyBase64 = execSync(command, {
        encoding: 'utf8',
        stdio: ['pipe', 'pipe', 'pipe']
      }).trim();

      const key = Buffer.from(keyBase64, 'base64');

      // Wipe base64 string
      this.wipeString(keyBase64);

      return key;
    } catch (error) {
      throw new Error(`Linux Secret Service retrieval failed: ${(error as Error).message}`);
    }
  }

  async delete(keyId: string): Promise<void> {
    const attribute = `${this.accountName}-${keyId}`;
    const command = `secret-tool clear ${this.serviceName} ${attribute}`;

    try {
      execSync(command, { stdio: 'pipe' });
    } catch {
      // Ignore errors
    }
  }

  private wipeString(str: string): void {
    if (typeof str === 'string') {
      str = '';
    }
  }
}

/**
 * Fallback key store using environment variable
 *
 * ⚠️ WARNING: This is NOT secure and should only be used for testing/CI
 */
class FallbackKeyStore implements KeychainBackend {
  private keys: Map<string, Buffer> = new Map();
  private warned = false;

  constructor(private envVarName: string) {
    if (!this.warned) {
      console.warn('⚠️  WARNING: Using fallback key storage. Keys are NOT secure!');
      console.warn(`⚠️  Set ${envVarName} environment variable or use a supported OS.`);
      this.warned = true;
    }
  }

  async store(keyId: string, key: Buffer): Promise<void> {
    // Store in memory (lost on process exit)
    this.keys.set(keyId, Buffer.from(key));

    // Also write to environment variable (if possible)
    if (keyId === 'master') {
      process.env[this.envVarName] = key.toString('base64');
    }
  }

  async retrieve(keyId: string): Promise<Buffer> {
    // Try memory first
    const memKey = this.keys.get(keyId);
    if (memKey) {
      return Buffer.from(memKey);
    }

    // Try environment variable
    const envValue = process.env[this.envVarName];
    if (keyId === 'master' && envValue) {
      const key = Buffer.from(envValue, 'base64');
      this.keys.set(keyId, key);
      return key;
    }

    throw new Error(`Key '${keyId}' not found in fallback store`);
  }

  async delete(keyId: string): Promise<void> {
    this.keys.delete(keyId);

    if (keyId === 'master') {
      delete process.env[this.envVarName];
    }
  }
}
